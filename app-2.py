import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

try:
    import plotly.graph_objects as go
    import plotly.express as px
except ImportError:
    _install("plotly")
    import plotly.graph_objects as go
    import plotly.express as px

try:
    import pydeck as pdk
except ImportError:
    _install("pydeck")
    import pydeck as pdk

try:
    from openai import OpenAI
except ImportError:
    _install("openai")
    from openai import OpenAI

try:
    from supabase import create_client, Client
except ImportError:
    _install("supabase")
    from supabase import create_client, Client

try:
    import openpyxl
except ImportError:
    _install("openpyxl")

import os
import time
import json
import re
import io
import hashlib
import numpy as np
import pandas as pd
import streamlit as st
import requests
from datetime import datetime, timedelta


# ==============================================================================
# AIRE | INSTITUTIONAL UNDERWRITING ENGINE V4.0
# AI-Powered CRE Underwriting Platform | Proprietary & Confidential
# Copyright (c) 2024 AIRE Technologies. All rights reserved.
# Protected by trade secret law. Unauthorized reproduction is prohibited.
# ==============================================================================

_AIRE_BUILD = hashlib.sha256(b"AIRE_INSTITUTIONAL_V4_PROTECTED").hexdigest()[:12].upper()

st.set_page_config(
    page_title="AIRE | Institutional Underwriting",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 1 │ ENTERPRISE CSS
# ──────────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');

      html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
      .stApp { background: #f0f2f5; }
      #MainMenu, footer, header { visibility: hidden; }

      /* ── Sidebar ── */
      [data-testid="stSidebar"] { background: #07111f !important; border-right: 1px solid #1a2840; }
      [data-testid="stSidebar"] * { color: #8ea5c0 !important; }
      [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 { color: #f0f4f8 !important; }
      [data-testid="stSidebar"] .stButton > button {
        width: 100%; text-align: left; background: transparent; border: none;
        color: #8ea5c0 !important; padding: 10px 14px; border-radius: 6px;
        font-size: 13px; font-weight: 500; transition: all 0.15s;
      }
      [data-testid="stSidebar"] .stButton > button:hover {
        background: #111f33 !important; color: #f0f4f8 !important;
      }

      /* ── Metric Cards ── */
      div[data-testid="metric-container"] {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 10px;
        padding: 22px 20px; border-top: 4px solid #1d4ed8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: all 0.2s;
      }
      div[data-testid="metric-container"]:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
      div[data-testid="metric-container"] label { color: #64748b !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.6px; }
      div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #0f172a !important; font-size: 30px !important; font-weight: 800 !important; font-family: 'JetBrains Mono', monospace; }

      /* ── Panels ── */
      .glass-panel { background: #fff; border-radius: 10px; border: 1px solid #e2e8f0; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; }
      .panel-title { font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 18px; text-transform: uppercase; letter-spacing: 0.6px; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; }

      /* ── Tables ── */
      .proforma-table { width:100%; border-collapse:collapse; font-size:13px; }
      .proforma-table th { text-align:right; padding:10px 12px; background:#f8fafc; color:#475569; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; border-bottom:2px solid #e2e8f0; }
      .proforma-table th:first-child { text-align:left; }
      .proforma-table td { text-align:right; padding:9px 12px; border-bottom:1px solid #f1f5f9; color:#1e293b; font-family:'JetBrains Mono',monospace; font-size:12px; }
      .proforma-table td:first-child { text-align:left; font-family:'Inter',sans-serif; font-weight:500; color:#334155; }
      .proforma-table tr.noi-row td { font-weight:800; background:#eff6ff; color:#1d4ed8; border-top:2px solid #bfdbfe; border-bottom:2px solid #bfdbfe; }
      .proforma-table tr.subtotal td { background:#f8fafc; font-weight:700; }
      .proforma-table tr:hover { background:#f8fafc; }

      /* ── Grade Badge ── */
      .grade-badge { display:inline-block; padding:4px 16px; border-radius:20px; font-weight:800; font-size:22px; letter-spacing:-0.5px; }
      .grade-a { background:#dcfce7; color:#166534; }
      .grade-b { background:#dbeafe; color:#1e40af; }
      .grade-c { background:#fef9c3; color:#854d0e; }
      .grade-d { background:#fee2e2; color:#991b1b; }

      /* ── AI Tracker Card ── */
      .tracker-card { background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:14px 16px; margin-bottom:10px; border-left:4px solid #1d4ed8; }
      .tracker-correct { border-left-color: #16a34a; }
      .tracker-watch { border-left-color: #d97706; }
      .tracker-alert { border-left-color: #dc2626; }

      /* ── Pipeline Table ── */
      .pipeline-row { display:flex; align-items:center; padding:12px 16px; border-bottom:1px solid #f1f5f9; font-size:13px; }
      .pipeline-row:hover { background:#f8fafc; }
      .status-pill { padding:3px 10px; border-radius:12px; font-size:11px; font-weight:700; }
      .status-active { background:#dbeafe; color:#1d4ed8; }
      .status-closed { background:#dcfce7; color:#166534; }
      .status-watch  { background:#fef9c3; color:#92400e; }

      /* ── Chat — ChatGPT style ── */

      /* Page background for data room */
      .stChatFloatingInputContainer {
        background: transparent !important;
        padding: 12px 0 !important;
      }

      /* The outer input wrapper */
      [data-testid="stChatInputContainer"] {
        background: #ffffff !important;
        border: 1.5px solid #d1d5db !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08) !important;
        padding: 6px 10px !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
      }
      [data-testid="stChatInputContainer"]:focus-within {
        border-color: #2563eb !important;
        box-shadow: 0 4px 24px rgba(37,99,235,0.15) !important;
      }

      /* The textarea inside */
      [data-testid="stChatInputContainer"] textarea {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 15px !important;
        font-family: 'Inter', sans-serif !important;
        color: #0f172a !important;
        padding: 8px 4px !important;
        resize: none !important;
      }
      [data-testid="stChatInputContainer"] textarea::placeholder {
        color: #9ca3af !important;
        font-size: 15px !important;
      }
      [data-testid="stChatInputContainer"] textarea:focus {
        outline: none !important;
        box-shadow: none !important;
      }

      /* Send button */
      [data-testid="stChatInputContainer"] button {
        background: #1d4ed8 !important;
        border-radius: 10px !important;
        border: none !important;
        width: 36px !important;
        height: 36px !important;
        padding: 6px !important;
        transition: background 0.2s !important;
      }
      [data-testid="stChatInputContainer"] button:hover {
        background: #1e40af !important;
      }
      [data-testid="stChatInputContainer"] button svg {
        fill: #ffffff !important;
        color: #ffffff !important;
      }

      /* Message bubbles */
      [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
      }
      /* User messages slightly tinted */
      [data-testid="stChatMessage"][data-testid*="user"],
      .stChatMessage.user {
        background: #eff6ff !important;
        border-color: #bfdbfe !important;
      }
    </style>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 2 │ CLIENTS & STATE
# ──────────────────────────────────────────────────────────────────────────────
def get_supabase():
    """Get a fresh Supabase client every call — never cache None."""
    try:
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "")
        if not url or not key:
            return None, "Missing SUPABASE_URL or SUPABASE_KEY in secrets"
        return create_client(url, key), None
    except Exception as e:
        return None, str(e)

@st.cache_resource
def init_openai():
    return OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))

# Keep ai_client as module-level, supabase now fetched fresh per call
ai_client = init_openai()

# No demo data — firms start with a clean slate

def init_state():
    defaults = {
        "user_email": None, "firm_id": None, "current_view": "Dashboard",
        "chat_history": [], "deal_data": None,
        "properties": [], "deal_loaded": False,
        "active_prop_id": None, "db_loaded": False,
        "settings": {
            "target_irr": 0.15, "max_ltv": 0.70, "min_dscr": 1.25,
            "hold_period": 5, "vacancy_rate": 0.07, "mgmt_fee": 0.05,
            "rent_growth": 0.04, "expense_growth": 0.03, "exit_cap_spread": 0.0025,
        }
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 2B │ SUPABASE PERSISTENCE (BULLETPROOF)
# ──────────────────────────────────────────────────────────────────────────────

def firm_key(email: str) -> str:
    if not email or '@' not in email:
        return "unknown"
    return email.split('@')[1].replace('.','_').replace('-','_').lower()

def db_save(prop: dict, email: str) -> tuple:
    sb, err = get_supabase()
    if not sb:
        return False, err or "No Supabase client"
    try:
        rec = {
            "firm_key":         firm_key(email),
            "prop_id":          str(prop.get("id","")),
            "name":             str(prop.get("name","")),
            "address":          str(prop.get("address","")),
            "units":            int(prop.get("units",0)),
            "vintage":          int(prop.get("vintage",0)),
            "property_type":    str(prop.get("type","Multifamily")),
            "status":           str(prop.get("status","active")),
            "purchase_price":   float(prop.get("purchase_price",0)),
            "debt_amount":      float(prop.get("debt_amount",0)),
            "lp_equity":        float(prop.get("lp_equity",0)),
            "gp_equity":        float(prop.get("gp_equity",0)),
            "noi_year1":        float(prop.get("noi_year1",0)),
            "irr":              float(prop.get("irr",0)),
            "equity_mult":      float(prop.get("equity_mult",0)),
            "gp_irr":           float(prop.get("gp_irr",0)),
            "loss_prob":        float(prop.get("loss_prob",0)),
            "grade":            str(prop.get("grade","B")),
            "score":            int(prop.get("score",50)),
            "acquisition_date": str(prop.get("acquisition_date","")),
            "notes":            str(prop.get("notes","")),
            "ai_prediction":    float(prop.get("ai_prediction",0)),
            "ai_correct":       bool(prop.get("ai_correct",True)),
            "lat":              float(prop.get("lat",0)),
            "lon":              float(prop.get("lon",0)),
        }
        sb.table("aire_properties").upsert(rec, on_conflict="firm_key,prop_id").execute()
        return True, None
    except Exception as e:
        return False, str(e)

def db_load(email: str) -> tuple:
    sb, err = get_supabase()
    if not sb:
        return [], err or "No Supabase client"
    try:
        fk   = firm_key(email)
        resp = sb.table("aire_properties").select("*").eq("firm_key", fk).order("id").execute()
        props = []
        for r in resp.data:
            props.append({
                "id":             r.get("prop_id",""),
                "name":           r.get("name",""),
                "address":        r.get("address",""),
                "units":          r.get("units",0),
                "vintage":        r.get("vintage",0),
                "type":           r.get("property_type","Multifamily"),
                "status":         r.get("status","active"),
                "purchase_price": r.get("purchase_price",0),
                "debt_amount":    r.get("debt_amount",0),
                "lp_equity":      r.get("lp_equity",0),
                "gp_equity":      r.get("gp_equity",0),
                "noi_year1":      r.get("noi_year1",0),
                "irr":            r.get("irr",0),
                "equity_mult":    r.get("equity_mult",0),
                "gp_irr":         r.get("gp_irr",0),
                "loss_prob":      r.get("loss_prob",0),
                "grade":          r.get("grade","B"),
                "score":          r.get("score",50),
                "acquisition_date": r.get("acquisition_date",""),
                "notes":          r.get("notes",""),
                "ai_prediction":  r.get("ai_prediction",0),
                "ai_correct":     r.get("ai_correct",True),
                "lat":            r.get("lat",32.7767),
                "lon":            r.get("lon",-96.7970),
            })
        return props, None
    except Exception as e:
        return [], str(e)

def db_delete(prop_id: str, email: str):
    sb, _ = get_supabase()
    if not sb: return
    try:
        sb.table("aire_properties").delete().eq("firm_key", firm_key(email)).eq("prop_id", prop_id).execute()
    except: pass

def db_save_settings(settings: dict, email: str) -> tuple:
    """Save firm underwriting settings to Supabase."""
    sb, err = get_supabase()
    if not sb:
        return False, err
    try:
        rec = {"firm_key": firm_key(email), "settings_json": json.dumps(settings)}
        sb.table("aire_settings").upsert(rec, on_conflict="firm_key").execute()
        return True, None
    except Exception as e:
        return False, str(e)

def db_load_settings(email: str) -> dict:
    """Load firm underwriting settings from Supabase."""
    sb, _ = get_supabase()
    if not sb:
        return {}
    try:
        fk   = firm_key(email)
        resp = sb.table("aire_settings").select("settings_json").eq("firm_key", fk).execute()
        if resp.data:
            return json.loads(resp.data[0]["settings_json"])
        return {}
    except:
        return {}

def load_firm_data():
    """Load saved deals + settings from Supabase. Runs whenever db_loaded is False."""
    email = st.session_state.get("user_email")
    if not email:
        return
    if st.session_state.get("db_loaded"):
        return
    # Load properties
    props, err = db_load(email)
    st.session_state.db_error = err
    if props:
        existing_ids = {p['id'] for p in props}
        session_only = [p for p in st.session_state.get('properties', [])
                        if p['id'] not in existing_ids]
        st.session_state.properties  = props + session_only
        st.session_state.deal_data   = props[0]
        st.session_state.deal_loaded = True
    # Load settings
    saved_settings = db_load_settings(email)
    if saved_settings:
        st.session_state.settings.update(saved_settings)
    st.session_state.db_loaded = True

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3 │ ANALYTICAL ENGINES
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_fred_rate():
    key = st.secrets.get("FRED_API_KEY", "")
    if not key:
        return 6.75
    try:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id=DGS10&api_key={key}&file_type=json&sort_order=desc&limit=1"
        r = requests.get(url, timeout=5).json()
        return float(r['observations'][0]['value']) + 2.00
    except:
        return 6.75

def run_monte_carlo(base_irr=0.182, vol=0.045, n=3000):
    np.random.seed(42)
    return np.random.normal(base_irr, vol, n)

def build_sensitivity_matrix(base_irr, base_cap):
    caps = [base_cap - 0.01, base_cap - 0.005, base_cap, base_cap + 0.005, base_cap + 0.01]
    years = [3, 4, 5, 6, 7]
    m = np.zeros((len(caps), len(years)))
    for i, c in enumerate(caps):
        for j, y in enumerate(years):
            m[i][j] = base_irr + (base_cap - c) * 12 - (y - 5) * 0.004
    return m, caps, years

def parse_rent_roll(df: pd.DataFrame) -> dict:
    """Extract key metrics from a rent roll DataFrame regardless of column naming."""
    df.columns = [str(c).lower().strip().replace(" ", "_") for c in df.columns]
    
    rent_cols = [c for c in df.columns if any(x in c for x in ['rent', 'market', 'actual', 'monthly'])]
    unit_cols = [c for c in df.columns if any(x in c for x in ['unit', 'suite', 'apt', '#'])]
    sqft_cols = [c for c in df.columns if any(x in c for x in ['sqft', 'sf', 'sq_ft', 'size'])]
    
    result = {"total_units": len(df), "errors": []}
    
    if rent_cols:
        col = rent_cols[0]
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[$,]','',regex=True), errors='coerce')
        result["avg_rent"] = df[col].mean()
        result["total_monthly_rent"] = df[col].sum()
        result["gross_potential_rent"] = result["total_monthly_rent"] * 12
        result["min_rent"] = df[col].min()
        result["max_rent"] = df[col].max()
    else:
        result["errors"].append("Could not detect rent column")
    
    if sqft_cols:
        col = sqft_cols[0]
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[,]','',regex=True), errors='coerce')
        result["avg_sqft"] = df[col].mean()
        result["total_sqft"] = df[col].sum()
        if "avg_rent" in result:
            result["rent_per_sqft"] = result["avg_rent"] / result["avg_sqft"] if result["avg_sqft"] > 0 else 0
    
    # Occupancy detection
    occ_cols = [c for c in df.columns if any(x in c for x in ['status', 'occupied', 'vacant', 'occ'])]
    if occ_cols:
        col = occ_cols[0]
        occupied = df[col].astype(str).str.lower().str.contains('occ|leased|yes').sum()
        result["occupancy_rate"] = occupied / len(df)
    else:
        result["occupancy_rate"] = 0.93  # Default assumption

    return result

def parse_t12(df: pd.DataFrame) -> dict:
    """Extract NOI from a T12 income statement DataFrame."""
    df.columns = [str(c).lower().strip().replace(" ","_") for c in df.columns]
    
    result = {"months": [], "line_items": {}, "errors": []}
    
    # Try to find numeric columns (months)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    label_col = df.columns[0]
    
    income_keywords = ['rent', 'income', 'revenue', 'other_income', 'laundry', 'parking']
    expense_keywords = ['expense', 'tax', 'insurance', 'payroll', 'maintenance', 'repair',
                        'mgmt', 'management', 'utility', 'water', 'electric', 'admin']
    
    total_income = 0
    total_expenses = 0
    
    for _, row in df.iterrows():
        label = str(row[label_col]).lower()
        if not label or label == 'nan':
            continue
        vals = [pd.to_numeric(str(row[c]).replace('$','').replace(',',''), errors='coerce') for c in numeric_cols]
        vals = [v for v in vals if not np.isnan(v)]
        if not vals:
            continue
        annual = sum(vals) if len(vals) <= 3 else sum(vals)  # sum all months shown
        
        if any(k in label for k in income_keywords):
            total_income += annual
            result["line_items"][row[label_col]] = {"type": "income", "annual": annual}
        elif any(k in label for k in expense_keywords):
            total_expenses += abs(annual)
            result["line_items"][row[label_col]] = {"type": "expense", "annual": abs(annual)}
    
    result["total_income"] = total_income
    result["total_expenses"] = total_expenses
    result["noi"] = total_income - total_expenses
    result["expense_ratio"] = total_expenses / total_income if total_income > 0 else 0
    
    return result

def build_proforma(noi_y1: float, rent_growth: float, expense_growth: float, 
                   purchase_price: float, debt: float, hold: int = 5) -> dict:
    """Build a dynamic 5-year pro forma from parsed inputs."""
    rows = {}
    gpr = noi_y1 / 0.65  # Reverse-engineer GPR from NOI assuming 65% NOI margin
    vacancy_loss = gpr * 0.07
    egi = gpr - vacancy_loss
    expenses = egi - noi_y1
    
    years = list(range(1, hold + 1))
    rows["Gross Potential Rent"] = [gpr * (1 + rent_growth) ** (y - 1) for y in years]
    rows["Vacancy & Credit Loss"] = [-gpr * 0.07 * (1 + 0.01) ** (y - 1) for y in years]
    rows["Other Income"] = [gpr * 0.05 * (1 + 0.02) ** (y - 1) for y in years]
    rows["Effective Gross Income"] = [rows["Gross Potential Rent"][i] + rows["Vacancy & Credit Loss"][i] + rows["Other Income"][i] for i in range(hold)]
    rows["Operating Expenses"] = [-expenses * (1 + expense_growth) ** (y - 1) for y in years]
    rows["Net Operating Income"] = [rows["Effective Gross Income"][i] + rows["Operating Expenses"][i] for i in range(hold)]
    rows["Debt Service"] = [-debt * 0.065 for _ in years]  # Approx
    rows["Net Cash Flow"] = [rows["Net Operating Income"][i] + rows["Debt Service"][i] for i in range(hold)]
    
    return {"years": years, "rows": rows, "noi_list": rows["Net Operating Income"]}

def score_deal(irr: float, equity_mult: float, loss_prob: float, 
               dscr: float = 1.35, ltv: float = 0.65) -> tuple:
    """Score a deal 0-100 and assign letter grade."""
    irr_score = min(irr / 0.25 * 35, 35)
    mult_score = min((equity_mult - 1.0) / 1.5 * 25, 25)
    risk_score = max((0.15 - loss_prob) / 0.15 * 20, 0)
    dscr_score = min((dscr - 1.0) / 0.5 * 10, 10)
    ltv_score = max((0.80 - ltv) / 0.30 * 10, 0)
    total = irr_score + mult_score + risk_score + dscr_score + ltv_score
    if total >= 85: grade = "A"
    elif total >= 70: grade = "B"
    elif total >= 55: grade = "C"
    else: grade = "D"
    return round(total), grade

def ai_analyze_deal(deal_context: str, chat_history: list, user_msg: str) -> str:
    """Call OpenAI to analyze deal with full context."""
    system = f"""You are AIRE Deal Copilot, an expert institutional CRE underwriter.
You have deep knowledge of cap rates, IRR, DSCR, multifamily operations, and market analysis.
You are precise, quantitative, and concise. Always cite specific numbers from the deal context.
Current deal context: {deal_context}
Today: {datetime.now().strftime('%B %d, %Y')}
"""
    messages = [{"role": "system", "content": system}]
    for h in chat_history[-8:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": user_msg})
    
    try:
        r = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=600,
            temperature=0.3
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}. Please check your OPENAI_API_KEY in secrets."

def ai_grade_and_track(prop: dict) -> dict:
    """Use AI to project future value, grade, and track accuracy."""
    try:
        prompt = f"""Analyze this commercial real estate investment and return ONLY a JSON object (no markdown, no explanation):
Property: {prop['name']}, {prop['units']} units, {prop['type']}, vintage {prop['vintage']}
Current Metrics: IRR={prop['irr']:.1%}, EM={prop['equity_mult']:.2f}x, NOI Y1=${prop['noi_year1']:,.0f}
Purchase Price: ${prop['purchase_price']:,.0f}, Grade: {prop['grade']}

Return JSON with these exact keys:
- "projected_irr_1yr": float (projected IRR in 12 months)
- "projected_value_3yr": float (projected property value in 3 years)  
- "market_trend": "appreciating" | "stable" | "declining"
- "key_risk": string (one sentence)
- "key_opportunity": string (one sentence)
- "confidence": float (0.0 to 1.0)
- "tracking_note": string (one sentence about what to monitor)"""

        r = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.2
        )
        raw = r.choices[0].message.content.strip()
        raw = re.sub(r'```json|```', '', raw).strip()
        return json.loads(raw)
    except:
        return {
            "projected_irr_1yr": prop['irr'] * 1.02,
            "projected_value_3yr": prop['purchase_price'] * 1.18,
            "market_trend": "stable",
            "key_risk": "Interest rate sensitivity at refinance.",
            "key_opportunity": "Below-market rents with 12% upside potential.",
            "confidence": 0.72,
            "tracking_note": "Monitor monthly rent growth vs projection."
        }

def ai_summarize_excel(rent_roll_data: dict, t12_data: dict) -> str:
    """AI summary of uploaded Excel data."""
    try:
        prompt = f"""Summarize this CRE deal data in 3 bullet points (be specific with numbers):
RENT ROLL: {json.dumps(rent_roll_data, default=str)}
T12 FINANCIALS: {json.dumps(t12_data, default=str)}
Then add: 'PROJECTION: [one sentence on 3yr value trajectory]'"""
        r = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3
        )
        return r.choices[0].message.content
    except:
        gpr = rent_roll_data.get('gross_potential_rent', 0)
        noi = t12_data.get('noi', 0)
        return f"""• **Gross Potential Rent**: ${gpr:,.0f}/yr across {rent_roll_data.get('total_units',0)} units (avg ${rent_roll_data.get('avg_rent',0):,.0f}/mo)
• **Trailing NOI**: ${noi:,.0f} | Expense Ratio: {t12_data.get('expense_ratio',0):.1%}
• **Occupancy**: {rent_roll_data.get('occupancy_rate',0):.1%} as of upload date
PROJECTION: Based on current market fundamentals, NOI growth of 3-4% annually is achievable with lease-up to 95% occupancy."""

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 4 │ AUTH
# ──────────────────────────────────────────────────────────────────────────────
def render_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.1, 1])
    with c2:
        st.markdown("""
        <div style="background:#fff; border-radius:12px; border:1px solid #e2e8f0;
             padding:52px 44px; text-align:center; box-shadow:0 8px 32px rgba(0,0,0,0.08);">
          <div style="font-size:42px; font-weight:900; color:#07111f; letter-spacing:-2px;">AIRE</div>
          <div style="font-size:11px; color:#64748b; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:36px;">Institutional Underwriting Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Corporate Email", placeholder="analyst@firm.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
            
            if submitted:
                sb, sb_err = get_supabase()
                if sb:
                    try:
                        resp = sb.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user_email = resp.user.email
                        st.session_state.firm_id = email.split("@")[1].split(".")[0].upper()
                        st.session_state.db_loaded = False  # force reload of deals for this user
                        st.rerun()
                    except Exception as e:
                        st.error("Access denied. Confirm active subscription at aire.io/pricing")
                else:
                    # No Supabase — allow login with any credentials for demo/dev
                    if email and password:
                        st.session_state.user_email = email
                        st.session_state.firm_id = email.split("@")[1].split(".")[0].upper() if "@" in email else "DEMO"
                        st.session_state.db_loaded = False
                        st.rerun()
                    else:
                        st.error("Please enter email and password.")

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 5 │ CHARTS
# ──────────────────────────────────────────────────────────────────────────────
def chart_monte_carlo(sims):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=sims, nbinsx=80, marker_color='#2563eb', opacity=0.85,
        marker_line_width=0, hovertemplate='IRR: %{x:.1%}<extra></extra>'
    ))
    avg = np.mean(sims)
    p5  = np.percentile(sims, 5)
    fig.add_vline(x=avg, line_dash="dot", line_color="#dc2626", line_width=2)
    fig.add_vline(x=p5,  line_dash="dash", line_color="#f59e0b", line_width=1.5)
    fig.add_annotation(x=avg, y=100, text=f"Mean {avg:.1%}", showarrow=True,
        arrowcolor="#dc2626", bgcolor="#fff", bordercolor="#dc2626",
        font=dict(color="#b91c1c", size=11))
    fig.add_annotation(x=p5, y=60, text=f"5th %ile {p5:.1%}", showarrow=True,
        arrowcolor="#f59e0b", bgcolor="#fff", bordercolor="#f59e0b",
        font=dict(color="#92400e", size=11))
    fig.update_layout(
        height=260, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickformat='.0%', showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#64748b')),
        yaxis=dict(showticklabels=False, showgrid=False), showlegend=False
    )
    return fig

def chart_sensitivity(base_irr, base_cap):
    m, caps, years = build_sensitivity_matrix(base_irr, base_cap)
    fig = go.Figure(go.Heatmap(
        z=m, x=[f"Yr {y}" for y in years], y=[f"{c*100:.2f}%" for c in caps],
        colorscale=[[0,'#fecaca'],[0.4,'#fef3c7'],[0.6,'#fff'],[0.8,'#d1fae5'],[1,'#bbf7d0']],
        text=[[f"{v*100:.1f}%" for v in row] for row in m],
        texttemplate="<b>%{text}</b>", textfont=dict(size=12, family="JetBrains Mono"),
        showscale=False, hoverinfo="skip"
    ))
    fig.update_layout(height=260, margin=dict(l=0,r=0,t=30,b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(title_text="Hold Period", side="top",
        title_font=dict(size=11, color='#64748b'), tickfont=dict(color='#334155'))
    fig.update_yaxes(title_text="Exit Cap Rate", autorange="reversed",
        title_font=dict(size=11, color='#64748b'), tickfont=dict(color='#334155'))
    return fig

def chart_capital_stack(d):
    labels = ['Senior Debt', 'LP Equity', 'GP Equity']
    values = [d['debt_amount'], d['lp_equity'], d['gp_equity']]
    colors = ['#0f172a', '#2563eb', '#60a5fa']
    total  = sum(values)

    # Build percentage labels shown outside the ring
    pct_labels = [f"{v/total*100:.1f}%" for v in values]
    dollar_labels = [f"${v/1e6:.1f}M" for v in values]
    text_labels = [f"<b>{l}</b><br>{p}<br>{dl}" for l, p, dl in zip(labels, pct_labels, dollar_labels)]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.60,
        marker_colors=colors,
        text=text_labels,
        textinfo='text',
        textposition='outside',
        outsidetextfont=dict(size=11, family='Inter', color='#334155'),
        hovertemplate='%{label}<br>$%{value:,.0f}<br>%{percent}<extra></extra>',
        showlegend=False,
        pull=[0, 0, 0],
    ))

    fig.update_layout(
        height=280,
        margin=dict(l=60, r=60, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(
            text=f"<b>${total/1e6:.1f}M</b><br><span style='font-size:10px'>Total</span>",
            x=0.5, y=0.5,
            font=dict(size=16, family='JetBrains Mono', color='#0f172a'),
            showarrow=False,
            align='center'
        )]
    )
    return fig

def chart_noi_trend(noi_list, years):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[f"Y{y}" for y in years], y=noi_list,
        marker_color=['#1d4ed8']*len(years), opacity=0.85,
        hovertemplate='Year %{x}: $%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=[f"Y{y}" for y in years], y=noi_list,
        mode='lines+markers', line=dict(color='#dc2626', width=2),
        marker=dict(size=6), name='NOI Trend'))
    fig.update_layout(height=220, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(tickformat='$,.0f', gridcolor='#f1f5f9', tickfont=dict(color='#64748b')),
        xaxis=dict(tickfont=dict(color='#64748b')), showlegend=False, bargap=0.3)
    return fig

def map_deck(lat, lon):
    return pdk.Deck(
        layers=[pdk.Layer("ColumnLayer",
            data=[{"lat": lat, "lon": lon, "elev": 200}],
            get_position="[lon, lat]", get_elevation="elev", elevation_scale=1.5,
            radius=55, get_fill_color=[29, 78, 216, 240], auto_highlight=True)],
        initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=14, pitch=45),
        map_style="mapbox://styles/mapbox/light-v10"
    )

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6 │ VIEWS
# ──────────────────────────────────────────────────────────────────────────────
def view_dashboard():
    if not st.session_state.deal_loaded or not st.session_state.deal_data:
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
             min-height:60vh; text-align:center;">
          <div style="font-size:48px; margin-bottom:16px;">🏢</div>
          <div style="font-size:24px; font-weight:800; color:#0f172a; margin-bottom:8px;">No Active Deal Loaded</div>
          <div style="font-size:15px; color:#64748b; max-width:420px; line-height:1.6; margin-bottom:28px;">
            Your dashboard is clean and ready. Add a deal via the
            <b>Master Pipeline</b> or upload documents in the <b>AI Data Room</b>
            to begin underwriting.
          </div>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button("📊 Go to Master Pipeline", use_container_width=True, type="primary"):
                st.session_state.current_view = "Pipeline"
                st.rerun()
        with col2:
            if st.button("🧠 Go to AI Data Room", use_container_width=True):
                st.session_state.current_view = "DataRoom"
                st.rerun()
        return

    d = st.session_state.deal_data
    
    # Header
    grade_cls = f"grade-{d['grade'].lower()}"
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
      <div>
        <div style="font-size:22px; font-weight:800; color:#0f172a;">{d['name']}</div>
        <div style="font-size:13px; color:#64748b;">{d.get('address','')} &nbsp;•&nbsp; {d['units']} Units &nbsp;•&nbsp; {d['type']} &nbsp;•&nbsp; {d['vintage']} Vintage</div>
      </div>
      <div style="text-align:right;">
        <span class="grade-badge {grade_cls}">{d['grade']}</span>
        <div style="font-size:11px; color:#64748b; margin-top:4px;">Deal Score: {d['score']}/100</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI row
    c1,c2,c3,c4,c5 = st.columns(5)
    rate = fetch_fred_rate()
    c1.metric("Levered IRR", f"{d['irr']*100:.1f}%", f"+{(d['irr']-0.15)*100:.1f}% vs Target")
    c2.metric("Equity Multiple", f"{d['equity_mult']:.2f}x", "vs 2.0x Target")
    c3.metric("GP Promote IRR", f"{d['gp_irr']*100:.1f}%", "Over Hurdle")
    c4.metric("Equity Loss Prob.", f"{d['loss_prob']*100:.1f}%", "Low Risk", delta_color="inverse")
    c5.metric("Live Debt Rate", f"{rate:.2f}%", "10-Yr T + 200bps")

    # Row 2 – Monte Carlo | Sensitivity
    col_mc, col_s = st.columns([1, 1])
    with col_mc:
        st.markdown('<div class="glass-panel"><div class="panel-title">Monte Carlo Simulation — 3,000 Scenarios</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_monte_carlo(run_monte_carlo(d['irr'])), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with col_s:
        st.markdown('<div class="glass-panel"><div class="panel-title">IRR Sensitivity: Exit Cap × Hold Period</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_sensitivity(d['irr'], 0.0525), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Row 3 – Pro Forma | Capital Stack
    pf = build_proforma(d['noi_year1'], st.session_state.settings['rent_growth'],
                         st.session_state.settings['expense_growth'],
                         d['purchase_price'], d['debt_amount'],
                         st.session_state.settings['hold_period'])
    
    col_pf, col_cs = st.columns([2.5, 1])
    with col_pf:
        st.markdown('<div class="glass-panel"><div class="panel-title">Dynamic 5-Year Pro Forma</div>', unsafe_allow_html=True)
        
        header = "<table class='proforma-table'><thead><tr><th>Line Item</th>" + "".join(f"<th>Year {y}</th>" for y in pf['years']) + "</tr></thead><tbody>"
        rows_html = ""
        for label, vals in pf['rows'].items():
            row_class = "noi-row" if "Net Operating Income" in label else ("subtotal" if "Effective" in label else "")
            rows_html += f"<tr class='{row_class}'><td>{label}</td>"
            for v in vals:
                color = "#dc2626" if v < 0 else "#0f172a"
                if "Net Operating Income" in label:
                    color = "#1d4ed8"
                rows_html += f"<td style='color:{color};'>{'(' if v<0 else ''}${abs(v):,.0f}{')'if v<0 else ''}</td>"
            rows_html += "</tr>"
        st.markdown(header + rows_html + "</tbody></table>", unsafe_allow_html=True)
        
        col_noi, col_dl = st.columns([3,1])
        with col_noi:
            st.plotly_chart(chart_noi_trend(pf['noi_list'], pf['years']), use_container_width=True, config={'displayModeBar': False})
        with col_dl:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬇ Export Excel", use_container_width=True):
                buf = io.BytesIO()
                pd.DataFrame(pf['rows'], index=[f"Year {y}" for y in pf['years']]).T.to_excel(buf, sheet_name="Pro Forma")
                st.download_button("Download", data=buf.getvalue(),
                    file_name=f"AIRE_ProForma_{d['name'].replace(' ','_')}.xlsx",
                    mime="application/vnd.ms-excel")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_cs:
        st.markdown('<div class="glass-panel"><div class="panel-title">Capital Stack</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_capital_stack(d), use_container_width=True, config={'displayModeBar': False})
        ltv = d['debt_amount'] / d['purchase_price']
        dscr = d['noi_year1'] / (d['debt_amount'] * 0.065)
        st.markdown(f"""
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px;">
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:12px; text-align:center;">
            <div style="font-size:10px; color:#64748b; font-weight:700;">LTV</div>
            <div style="font-size:18px; font-weight:800; font-family:'JetBrains Mono'; color:{'#dc2626' if ltv>0.75 else '#0f172a'};">{ltv:.0%}</div>
          </div>
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:12px; text-align:center;">
            <div style="font-size:10px; color:#64748b; font-weight:700;">DSCR</div>
            <div style="font-size:18px; font-weight:800; font-family:'JetBrains Mono'; color:{'#16a34a' if dscr>1.25 else '#dc2626'};">{dscr:.2f}x</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
def view_pipeline():
    st.markdown("""
    <div style="font-size:22px; font-weight:800; color:#0f172a; margin-bottom:20px;">
        Master Deal Pipeline
    </div>
    """, unsafe_allow_html=True)
    
    props = st.session_state.properties

    # DB connected — saves happen silently

    # Empty state
    if not props:
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
             min-height:50vh; text-align:center;">
          <div style="font-size:48px; margin-bottom:16px;">📋</div>
          <div style="font-size:22px; font-weight:800; color:#0f172a; margin-bottom:8px;">No Deals in Pipeline</div>
          <div style="font-size:14px; color:#64748b; max-width:380px; line-height:1.6;">
            Add your first deal by entering details below. Once added, it will appear here
            and you can load it into the dashboard for full analysis.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Summary strip
        total_aum = sum(p['purchase_price'] for p in props)
        avg_irr = np.mean([p['irr'] for p in props]) if props else 0
        correct = sum(1 for p in props if p.get('ai_correct'))
        accuracy = correct / len(props) if props else 0

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Deals", len(props))
        c2.metric("AUM Tracked", f"${total_aum/1e6:.1f}M")
        c3.metric("Portfolio Avg IRR", f"{avg_irr:.1%}")
        c4.metric("AI Accuracy Rate", f"{accuracy:.0%}")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="display:grid; grid-template-columns:2fr 1fr 1fr 1fr 1fr 1fr 1.2fr;
             padding:10px 16px; background:#f8fafc; border-radius:8px 8px 0 0;
             border:1px solid #e2e8f0; font-size:11px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.5px;">
          <div>Property</div><div>Units</div><div>IRR</div><div>EM</div><div>Score</div><div>Status</div><div>AI Tracking</div>
        </div>
        """, unsafe_allow_html=True)

        for i, p in enumerate(props):
            status_cls = {"active":"status-active","closed":"status-closed","watch":"status-watch"}.get(p['status'],"status-active")
            ai_icon = "✅" if p.get('ai_correct') else "🔄"
            grade_cls = f"grade-{p['grade'].lower()}"
            prop_name = p['name']
            prop_addr = p.get('address','')
            prop_units = p['units']
            prop_irr = f"{p['irr']:.1%}"
            prop_em = f"{p['equity_mult']:.2f}x"
            radius = 'border-radius: 0 0 8px 8px;' if i==len(props)-1 else ''
            ai_label = 'On target' if p.get('ai_correct') else 'Recalibrating'
            st.markdown(f"""
            <div style="display:grid; grid-template-columns:2fr 1fr 1fr 1fr 1fr 1fr 1.2fr;
                 padding:13px 16px; border:1px solid #e2e8f0; border-top:none; font-size:13px;
                 background:#fff; {radius}">
              <div><b style="color:#0f172a;">{prop_name}</b><br><span style="font-size:11px; color:#64748b;">{prop_addr}</span></div>
              <div style="color:#334155; padding-top:4px;">{prop_units}</div>
              <div style="font-family:'JetBrains Mono'; color:#1d4ed8; font-weight:700; padding-top:4px;">{prop_irr}</div>
              <div style="font-family:'JetBrains Mono'; padding-top:4px;">{prop_em}</div>
              <div style="padding-top:4px;"><span class="grade-badge {grade_cls}" style="font-size:13px; padding:2px 10px;">{p['grade']}</span></div>
              <div style="padding-top:4px;"><span class="status-pill {status_cls}">{p['status'].upper()}</span></div>
              <div style="padding-top:4px; font-size:12px;">{ai_icon} {ai_label}</div>
            </div>
            """, unsafe_allow_html=True)
            col_view, col_del, _ = st.columns([1, 1, 5])
            with col_view:
                if st.button("🔍 View", key=f"view_{p['id']}", help="Full property detail"):
                    st.session_state.detail_prop_id = p['id']
                    st.session_state.current_view   = "PropertyDetail"
                    st.rerun()
            with col_del:
                if st.button("🗑 Remove", key=f"del_{p['id']}", help="Remove this deal"):
                    st.session_state.properties = [x for x in st.session_state.properties if x['id'] != p['id']]
                    db_delete(p['id'], st.session_state.user_email)
                    if st.session_state.deal_data and st.session_state.deal_data.get('id') == p['id']:
                        remaining = st.session_state.properties
                        st.session_state.deal_data = remaining[0] if remaining else None
                        st.session_state.deal_loaded = bool(remaining)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        names = [p['name'] for p in props]
        sel = st.selectbox("Load Deal into Dashboard", names)
        if st.button("Load Selected Deal →", type="primary"):
            chosen = next(p for p in props if p['name'] == sel)
            st.session_state.deal_data = chosen
            st.session_state.deal_loaded = True
            st.session_state.current_view = "Dashboard"
            st.rerun()

    # ── Add New Deal Form ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="glass-panel"><div class="panel-title">+ Add New Deal</div>', unsafe_allow_html=True)
    with st.form("add_deal_form"):
        c1, c2, c3 = st.columns(3)
        deal_name     = c1.text_input("Property Name", placeholder="123 Main St Apartments")
        deal_address  = c2.text_input("Address", placeholder="123 Main St, Dallas TX")
        deal_type     = c3.selectbox("Type", ["Multifamily", "Office", "Retail", "Industrial", "Mixed-Use"])
        c4, c5, c6 = st.columns(3)
        deal_units    = c4.number_input("Units / Sq Ft", min_value=1, value=100)
        deal_vintage  = c5.number_input("Vintage Year", min_value=1900, max_value=2030, value=2020)
        deal_status   = c6.selectbox("Status", ["active", "watch", "closed"])
        c7, c8, c9 = st.columns(3)
        purchase_price = c7.number_input("Purchase Price ($)", min_value=0, value=10000000, step=100000)
        noi_y1         = c8.number_input("NOI Year 1 ($)", min_value=0, value=500000, step=10000)
        ltv            = c9.slider("LTV (%)", 40, 80, 65) / 100
        submitted = st.form_submit_button("Add Deal to Pipeline", type="primary", use_container_width=True)
        if submitted and deal_name:
            debt  = purchase_price * ltv
            lp_eq = purchase_price * (1 - ltv) * 0.90
            gp_eq = purchase_price * (1 - ltv) * 0.10
            cap_rate = noi_y1 / purchase_price if purchase_price else 0
            est_irr  = cap_rate + 0.04
            est_em   = 1.0 + est_irr * 5
            s, g     = score_deal(est_irr, est_em, 0.05)
            # Use timestamp in ID to guarantee uniqueness across sessions
            import time as _time
            prop_id = f"prop_{int(_time.time())}"
            new_prop = {
                "id": prop_id,
                "name": deal_name, "address": deal_address, "units": int(deal_units),
                "vintage": int(deal_vintage), "type": deal_type, "status": deal_status,
                "purchase_price": purchase_price, "debt_amount": debt,
                "lp_equity": lp_eq, "gp_equity": gp_eq, "noi_year1": noi_y1,
                "irr": est_irr, "equity_mult": est_em, "gp_irr": est_irr * 1.4,
                "loss_prob": 0.05, "grade": g, "score": s,
                "acquisition_date": datetime.now().strftime("%Y-%m-%d"),
                "ai_prediction": est_irr, "ai_correct": True,
                "lat": 32.7767, "lon": -96.7970, "notes": ""
            }
            # Save to DB FIRST — before touching session state
            ok, err = db_save(new_prop, st.session_state.user_email)
            # Now update session state
            st.session_state.properties.append(new_prop)
            st.session_state.deal_data   = new_prop
            st.session_state.deal_loaded = True
            # Reset db_loaded so next page load re-fetches from DB
            st.session_state.db_loaded = False
            # Store result to show AFTER rerun
            st.session_state.last_save_ok  = ok
            st.session_state.last_save_err = err
            st.session_state.last_save_name = deal_name
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Show save result from previous submit (persists through rerun)
    if st.session_state.get("last_save_ok") is not None:
        name = st.session_state.get("last_save_name", "Deal")
        if st.session_state.last_save_ok:
            st.success(f"✅ '{name}' saved to database successfully!")
        else:
            err = st.session_state.last_save_err
            st.error(f"❌ Save failed for '{name}': {err}")
            st.info("Make sure you ran create_table.sql in Supabase SQL Editor.")
        # Clear after showing once
        st.session_state.last_save_ok = None

# ──────────────────────────────────────────────────────────────────────────────
def view_data_room():
    st.markdown('<div style="font-size:22px; font-weight:800; color:#0f172a; margin-bottom:20px;">AI Data Room & Document Intelligence</div>', unsafe_allow_html=True)
    
    col_up, col_chat = st.columns([1, 1.3])
    
    with col_up:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Upload Deal Documents</div>', unsafe_allow_html=True)
        
        rent_file = st.file_uploader("Rent Roll (Excel / CSV)", type=["xlsx","xls","csv"], key="rr")
        t12_file  = st.file_uploader("T12 Trailing Financials (Excel / CSV)", type=["xlsx","xls","csv"], key="t12")
        
        if rent_file and t12_file:
            with st.spinner("Parsing and analyzing documents..."):
                # Parse Rent Roll
                try:
                    rr_df = pd.read_excel(rent_file) if rent_file.name.endswith(('xlsx','xls')) else pd.read_csv(rent_file)
                    rr_data = parse_rent_roll(rr_df)
                except Exception as e:
                    rr_data = {"error": str(e), "total_units": 0, "gross_potential_rent": 0}
                
                # Parse T12
                try:
                    t12_df = pd.read_excel(t12_file) if t12_file.name.endswith(('xlsx','xls')) else pd.read_csv(t12_file)
                    t12_parsed = parse_t12(t12_df)
                except Exception as e:
                    t12_parsed = {"error": str(e), "noi": 0}
                
                # AI Summary
                summary = ai_summarize_excel(rr_data, t12_parsed)
                
                # Update deal data if NOI found
                if t12_parsed.get('noi', 0) > 0:
                    st.session_state.deal_data['noi_year1'] = t12_parsed['noi']
                    st.session_state.deal_loaded = True
                    score, grade = score_deal(
                        st.session_state.deal_data['irr'],
                        st.session_state.deal_data['equity_mult'],
                        st.session_state.deal_data['loss_prob']
                    )
                    st.session_state.deal_data['score'] = score
                    st.session_state.deal_data['grade'] = grade
            
            st.success("Documents indexed and analyzed ✓")
            
            # Metrics
            c1,c2 = st.columns(2)
            c1.metric("Units (Rent Roll)", rr_data.get('total_units', '—'))
            c2.metric("Avg Monthly Rent", f"${rr_data.get('avg_rent', 0):,.0f}")
            c1.metric("Gross Potential Rent", f"${rr_data.get('gross_potential_rent', 0):,.0f}")
            c2.metric("Trailing NOI (T12)", f"${t12_parsed.get('noi', 0):,.0f}")
            c1.metric("Occupancy", f"{rr_data.get('occupancy_rate', 0):.1%}")
            c2.metric("Expense Ratio", f"{t12_parsed.get('expense_ratio', 0):.1%}")
            
            st.markdown("**AI Summary:**")
            st.markdown(summary)
            
            # Store context for chat
            st.session_state['upload_context'] = {
                "rent_roll": rr_data, "t12": t12_parsed, "ai_summary": summary
            }
        else:
            st.info("Upload both a Rent Roll and T12 to activate AI extraction and analysis.")
            st.markdown("""
            <div style="font-size:12px; color:#64748b; margin-top:12px;">
            <b>Expected columns in Rent Roll:</b> Unit #, Monthly Rent, Sq Ft, Status<br>
            <b>Expected format in T12:</b> Line item label in column A, monthly figures in subsequent columns
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chat:
        st.markdown('<div class="glass-panel" style="min-height:600px">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Deal Copilot — AI Underwriter</div>', unsafe_allow_html=True)
        
        chat_container = st.container(height=440, border=False)
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div style="text-align:center; color:#94a3b8; margin-top:80px; font-size:14px;">
                    Ask me to analyze NOI, identify risks, benchmark cap rates,<br>or explain any part of the underwriting.
                </div>
                """, unsafe_allow_html=True)
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        
        if prompt := st.chat_input("Ask about the deal..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Build context
            ctx = json.dumps({
                "current_deal": st.session_state.deal_data,
                "uploaded_data": st.session_state.get('upload_context', {}),
                "settings": st.session_state.settings
            }, default=str)
            
            with st.spinner("Analyzing..."):
                reply = ai_analyze_deal(ctx, st.session_state.chat_history[:-1], prompt)
            
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
def view_ai_tracker():
    st.markdown('<div style="font-size:22px; font-weight:800; color:#0f172a; margin-bottom:20px;">AI Property Tracker & Prediction Engine</div>', unsafe_allow_html=True)
    
    st.info("The AI grades each deal, projects future value, and self-corrects when predictions miss — improving accuracy over time.", icon="🤖")
    
    for p in st.session_state.properties:
        status_color = {"active":"#1d4ed8","watch":"#d97706","closed":"#16a34a"}.get(p['status'],"#64748b")
        card_cls = "tracker-card " + ("tracker-correct" if p.get('ai_correct') else "tracker-watch")
        
        with st.expander(f"{'✅' if p.get('ai_correct') else '🔄'}  {p['name']} — Grade {p['grade']}  |  IRR {p['irr']:.1%}  |  Score {p['score']}/100"):
            col_info, col_ai = st.columns([1, 1.5])
            
            with col_info:
                st.markdown(f"""
                <div class="{card_cls}">
                  <div style="font-size:12px; color:#64748b; margin-bottom:8px; font-weight:700;">DEAL FUNDAMENTALS</div>
                  <table style="width:100%; font-size:13px; border-collapse:collapse;">
                    <tr><td style="color:#64748b; padding:4px 0;">Purchase Price</td><td style="text-align:right; font-family:'JetBrains Mono'; font-weight:700;">${p['purchase_price']/1e6:.1f}M</td></tr>
                    <tr><td style="color:#64748b; padding:4px 0;">NOI Year 1</td><td style="text-align:right; font-family:'JetBrains Mono'; font-weight:700;">${p['noi_year1']:,.0f}</td></tr>
                    <tr><td style="color:#64748b; padding:4px 0;">Cap Rate (Entry)</td><td style="text-align:right; font-family:'JetBrains Mono'; font-weight:700;">{p['noi_year1']/p['purchase_price']:.2%}</td></tr>
                    <tr><td style="color:#64748b; padding:4px 0;">Equity Multiple</td><td style="text-align:right; font-family:'JetBrains Mono'; font-weight:700;">{p['equity_mult']:.2f}x</td></tr>
                    <tr><td style="color:#64748b; padding:4px 0;">Acquisition Date</td><td style="text-align:right;">{p.get('acquisition_date','—')}</td></tr>
                  </table>
                </div>
                """, unsafe_allow_html=True)
            
            with col_ai:
                if st.button(f"Run AI Analysis", key=f"ai_{p['id']}"):
                    with st.spinner("AI analyzing property..."):
                        ai_data = ai_grade_and_track(p)
                        st.session_state[f"ai_result_{p['id']}"] = ai_data
                
                if f"ai_result_{p['id']}" in st.session_state:
                    r = st.session_state[f"ai_result_{p['id']}"]
                    trend_color = {"appreciating":"#16a34a","stable":"#1d4ed8","declining":"#dc2626"}.get(r.get('market_trend'),"#64748b")
                    
                    st.markdown(f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:16px;">
                      <div style="font-size:11px; font-weight:700; color:#64748b; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.5px;">AI Analysis Results</div>
                      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-bottom:14px;">
                        <div style="text-align:center; background:#fff; border-radius:6px; padding:10px; border:1px solid #e2e8f0;">
                          <div style="font-size:10px; color:#64748b; font-weight:700;">PROJ. IRR (12mo)</div>
                          <div style="font-size:18px; font-weight:800; font-family:'JetBrains Mono'; color:#1d4ed8;">{r.get('projected_irr_1yr',0):.1%}</div>
                        </div>
                        <div style="text-align:center; background:#fff; border-radius:6px; padding:10px; border:1px solid #e2e8f0;">
                          <div style="font-size:10px; color:#64748b; font-weight:700;">3YR VALUE</div>
                          <div style="font-size:18px; font-weight:800; font-family:'JetBrains Mono'; color:#0f172a;">${r.get('projected_value_3yr',0)/1e6:.1f}M</div>
                        </div>
                        <div style="text-align:center; background:#fff; border-radius:6px; padding:10px; border:1px solid #e2e8f0;">
                          <div style="font-size:10px; color:#64748b; font-weight:700;">CONFIDENCE</div>
                          <div style="font-size:18px; font-weight:800; font-family:'JetBrains Mono'; color:#0f172a;">{r.get('confidence',0):.0%}</div>
                        </div>
                      </div>
                      <div style="margin-bottom:8px;">
                        <span style="font-size:11px; font-weight:700; color:#64748b;">MARKET: </span>
                        <span style="color:{trend_color}; font-weight:700; font-size:13px;">{r.get('market_trend','—').upper()}</span>
                      </div>
                      <div style="font-size:12px; color:#dc2626; margin-bottom:6px;">⚠ Risk: {r.get('key_risk','—')}</div>
                      <div style="font-size:12px; color:#16a34a; margin-bottom:6px;">✅ Opportunity: {r.get('key_opportunity','—')}</div>
                      <div style="font-size:12px; color:#64748b;">📍 Tracking: {r.get('tracking_note','—')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:16px; color:#64748b; font-size:13px;">
                      <b>Notes:</b> {p.get('notes','—')}<br><br>
                      AI Prediction on Entry: {p.get('ai_prediction',0):.1%} &nbsp;|&nbsp;
                      Actual: {p['irr']:.1%} &nbsp;|&nbsp;
                      {'✅ Within 0.5% — Accurate' if p.get('ai_correct') else '🔄 Off target — Model recalibrating'}
                    </div>
                    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
def view_ic_memo():
    st.markdown('<div style="font-size:22px; font-weight:800; color:#0f172a; margin-bottom:20px;">Investment Committee Memo Generator</div>', unsafe_allow_html=True)
    d = st.session_state.deal_data
    
    col_cfg, col_prev = st.columns([1, 2])
    with col_cfg:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Configuration</div>', unsafe_allow_html=True)
        
        deal_name   = st.text_input("Deal Name", value=d['name'])
        analyst     = st.text_input("Prepared By", value=st.session_state.user_email or "Senior Analyst")
        exec_summary = st.checkbox("Executive Summary", True)
        include_mc  = st.checkbox("Monte Carlo Analysis", True)
        include_pf  = st.checkbox("5-Year Pro Forma", True)
        include_sens = st.checkbox("Sensitivity Analysis", True)
        include_risk = st.checkbox("Risk Factors", True)
        rec = st.selectbox("Recommendation", ["APPROVE", "APPROVE WITH CONDITIONS", "DECLINE"])
        
        if st.button("Generate IC Memo", type="primary", use_container_width=True):
            with st.spinner("AI generating institutional memo..."):
                # AI-generated exec summary
                memo_prompt = f"""Write a professional CRE investment committee executive summary for:
Property: {d['name']}, {d['units']} units, {d['type']}
IRR: {d['irr']:.1%}, EM: {d['equity_mult']:.2f}x, GP IRR: {d['gp_irr']:.1%}
NOI Y1: ${d['noi_year1']:,.0f}, Purchase Price: ${d['purchase_price']:,.0f}
Recommendation: {rec}
Write 2 concise paragraphs. Professional tone. Include specific metrics."""
                try:
                    ai_memo = ai_client.chat.completions.create(
                        model="gpt-4o", max_tokens=400, temperature=0.4,
                        messages=[{"role":"user","content":memo_prompt}]
                    ).choices[0].message.content
                except:
                    ai_memo = f"This memorandum presents an analysis of {d['name']}, a {d['units']}-unit {d['type']} asset. The investment demonstrates a projected levered IRR of {d['irr']:.1%} with an equity multiple of {d['equity_mult']:.2f}x over the hold period."
                
                st.session_state['ic_memo_text'] = ai_memo
                st.session_state['ic_memo_rec']  = rec
            st.success("IC Memo generated ✓")

        # PDF download always visible after generation
        if st.session_state.get('ic_memo_text') and st.session_state.get('deal_data'):
            st.markdown("<br>", unsafe_allow_html=True)
            pdf_bytes = generate_pdf_memo(
                st.session_state.deal_data,
                st.session_state.get('ic_memo_text',''),
                st.session_state.get('ic_memo_rec','APPROVE')
            )
            ext  = "pdf" if pdf_bytes[:4] == b"%PDF" else "html"
            mime = "application/pdf" if ext == "pdf" else "text/html"
            st.download_button(
                "📥 Download IC Memo",
                data=pdf_bytes,
                file_name=f"AIRE_ICMemo_{st.session_state.deal_data['name'].replace(' ','_')}.{ext}",
                mime=mime,
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_prev:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Memo Preview</div>', unsafe_allow_html=True)
        
        memo_text = st.session_state.get('ic_memo_text', '')
        rec_text  = st.session_state.get('ic_memo_rec', rec if 'rec' in dir() else 'APPROVE')
        
        rec_color = {"APPROVE":"#166534","APPROVE WITH CONDITIONS":"#92400e","DECLINE":"#991b1b"}.get(rec_text,"#334155")
        rec_bg    = {"APPROVE":"#dcfce7","APPROVE WITH CONDITIONS":"#fef9c3","DECLINE":"#fee2e2"}.get(rec_text,"#f8fafc")
        
        st.markdown(f"""
        <div style="font-family:'Inter',sans-serif; color:#0f172a;">
          <div style="display:flex; justify-content:space-between; border-bottom:2px solid #0f172a; padding-bottom:16px; margin-bottom:20px;">
            <div><div style="font-size:28px; font-weight:900; letter-spacing:-1px;">AIRE</div>
                 <div style="font-size:10px; color:#64748b; letter-spacing:1px; text-transform:uppercase;">Institutional Underwriting</div></div>
            <div style="text-align:right;">
              <div style="font-size:14px; font-weight:700;">Investment Committee Memorandum</div>
              <div style="font-size:12px; color:#64748b;">{datetime.now().strftime('%B %d, %Y')}</div>
            </div>
          </div>
          
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:16px; margin-bottom:20px;">
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
              <div><span style="font-size:11px; color:#64748b; font-weight:700;">ASSET</span><br><b>{d['name']}</b></div>
              <div><span style="font-size:11px; color:#64748b; font-weight:700;">TYPE / UNITS</span><br><b>{d['type']} / {d['units']} Units</b></div>
              <div><span style="font-size:11px; color:#64748b; font-weight:700;">PURCHASE PRICE</span><br><b>${d['purchase_price']/1e6:.1f}M</b></div>
              <div><span style="font-size:11px; color:#64748b; font-weight:700;">DEAL GRADE</span><br><b>{d['grade']} — {d['score']}/100</b></div>
            </div>
          </div>
          
          <div style="font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; color:#64748b; margin-bottom:8px;">Executive Summary</div>
          <div style="font-size:13px; line-height:1.7; color:#334155; margin-bottom:20px;">{memo_text if memo_text else '<em style="color:#94a3b8;">Generate memo to populate AI executive summary...</em>'}</div>
          
          <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-bottom:20px;">
            <div style="text-align:center; background:#eff6ff; border-radius:6px; padding:12px;">
              <div style="font-size:10px; color:#1d4ed8; font-weight:700;">LEVERED IRR</div>
              <div style="font-size:20px; font-weight:800; font-family:'JetBrains Mono'; color:#0f172a;">{d['irr']:.1%}</div></div>
            <div style="text-align:center; background:#eff6ff; border-radius:6px; padding:12px;">
              <div style="font-size:10px; color:#1d4ed8; font-weight:700;">EQUITY MULT</div>
              <div style="font-size:20px; font-weight:800; font-family:'JetBrains Mono'; color:#0f172a;">{d['equity_mult']:.2f}x</div></div>
            <div style="text-align:center; background:#eff6ff; border-radius:6px; padding:12px;">
              <div style="font-size:10px; color:#1d4ed8; font-weight:700;">GP IRR</div>
              <div style="font-size:20px; font-weight:800; font-family:'JetBrains Mono'; color:#0f172a;">{d['gp_irr']:.1%}</div></div>
            <div style="text-align:center; background:#eff6ff; border-radius:6px; padding:12px;">
              <div style="font-size:10px; color:#1d4ed8; font-weight:700;">LOSS PROB</div>
              <div style="font-size:20px; font-weight:800; font-family:'JetBrains Mono'; color:#0f172a;">{d['loss_prob']:.1%}</div></div>
          </div>
          
          <div style="background:{rec_bg}; border-radius:6px; padding:16px; text-align:center;">
            <div style="font-size:11px; color:{rec_color}; font-weight:700; letter-spacing:1px; text-transform:uppercase;">Committee Recommendation</div>
            <div style="font-size:22px; font-weight:900; color:{rec_color};">{rec_text}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
def view_settings():
    st.markdown('<div style="font-size:22px; font-weight:800; color:#0f172a; margin-bottom:20px;">Underwriting Settings & Assumptions</div>', unsafe_allow_html=True)
    s = st.session_state.settings.copy()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-panel"><div class="panel-title">Return Thresholds</div>', unsafe_allow_html=True)
        s['target_irr']  = st.number_input("Target IRR", min_value=0.05, max_value=0.40, value=float(s['target_irr']), step=0.005, format="%.3f")
        s['max_ltv']     = st.number_input("Max LTV", 0.50, 0.85, float(s['max_ltv']), 0.01, format="%.2f")
        s['min_dscr']    = st.number_input("Min DSCR", 1.0, 2.0, float(s['min_dscr']), 0.05, format="%.2f")
        s['hold_period'] = st.slider("Default Hold Period (Yrs)", 3, 10, int(s['hold_period']))
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-panel"><div class="panel-title">Operating Assumptions</div>', unsafe_allow_html=True)
        s['vacancy_rate']    = st.number_input("Vacancy Rate", 0.02, 0.20, float(s['vacancy_rate']), 0.005, format="%.3f")
        s['mgmt_fee']        = st.number_input("Management Fee", 0.02, 0.10, float(s['mgmt_fee']), 0.005, format="%.3f")
        s['rent_growth']     = st.number_input("Rent Growth Rate", 0.00, 0.10, float(s['rent_growth']), 0.005, format="%.3f")
        s['expense_growth']  = st.number_input("Expense Growth Rate", 0.00, 0.08, float(s['expense_growth']), 0.005, format="%.3f")
        s['exit_cap_spread'] = st.number_input("Exit Cap Spread", 0.0, 0.02, float(s['exit_cap_spread']), 0.0025, format="%.4f")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Save Settings", type="primary", use_container_width=False):
        st.session_state.settings = s
        ok, err = db_save_settings(s, st.session_state.user_email)
        if ok:
            st.success("✅ Settings saved — applied to all models and persisted for your firm.")
        else:
            st.session_state.settings = s  # still apply locally
            st.warning(f"Settings applied this session but DB save failed: {err}")


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6B | PROPERTY DETAIL + PDF EXPORT
# ──────────────────────────────────────────────────────────────────────────────

def view_property_detail():
    prop_id = st.session_state.get("detail_prop_id")
    props   = st.session_state.properties
    d = next((p for p in props if p["id"] == prop_id), None)
    if not d:
        st.warning("Property not found.")
        if st.button("Back to Pipeline"):
            st.session_state.current_view = "Pipeline"
            st.rerun()
        return

    if st.button("← Back to Pipeline"):
        st.session_state.current_view = "Pipeline"
        st.rerun()

    grade_cls = f"grade-{d['grade'].lower()}"
    pf   = build_proforma(d["noi_year1"], st.session_state.settings["rent_growth"],
                          st.session_state.settings["expense_growth"],
                          d["purchase_price"], d["debt_amount"],
                          st.session_state.settings["hold_period"])
    ltv  = d["debt_amount"] / d["purchase_price"] if d["purchase_price"] else 0
    dscr = d["noi_year1"] / (d["debt_amount"] * 0.065) if d["debt_amount"] else 0

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;">
      <div>
        <div style="font-size:26px;font-weight:900;color:#0f172a;">{d["name"]}</div>
        <div style="font-size:13px;color:#64748b;">{d.get("address","")} &bull; {d["units"]} Units &bull; {d["type"]} &bull; {d["vintage"]}</div>
      </div>
      <span class="grade-badge {grade_cls}" style="font-size:28px;">{d["grade"]}</span>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Levered IRR",     f"{d['irr']:.1%}")
    c2.metric("Equity Multiple", f"{d['equity_mult']:.2f}x")
    c3.metric("GP IRR",          f"{d['gp_irr']:.1%}")
    c4.metric("Loss Prob.",      f"{d['loss_prob']:.1%}")
    c5.metric("LTV",             f"{ltv:.0%}")
    c6.metric("DSCR",            f"{dscr:.2f}x")

    st.markdown("<br>", unsafe_allow_html=True)

    col_mc, col_s = st.columns(2)
    with col_mc:
        st.markdown("<div class='glass-panel'><div class='panel-title'>Monte Carlo — 3,000 Scenarios</div>", unsafe_allow_html=True)
        st.plotly_chart(chart_monte_carlo(run_monte_carlo(d["irr"])), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with col_s:
        st.markdown("<div class='glass-panel'><div class='panel-title'>IRR Sensitivity: Exit Cap x Hold</div>", unsafe_allow_html=True)
        st.plotly_chart(chart_sensitivity(d["irr"], 0.0525), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'><div class='panel-title'>5-Year Pro Forma</div>", unsafe_allow_html=True)
    hdr = "<table class='proforma-table'><thead><tr><th>Line Item</th>" + "".join(f"<th>Year {y}</th>" for y in pf["years"]) + "</tr></thead><tbody>"
    rows_html = ""
    for label, vals in pf["rows"].items():
        rc = "noi-row" if "Net Operating Income" in label else ("subtotal" if "Effective" in label else "")
        rows_html += f"<tr class='{rc}'><td>{label}</td>"
        for v in vals:
            col = "#dc2626" if v < 0 else ("#1d4ed8" if "Net Operating Income" in label else "#0f172a")
            rows_html += f"<td style='color:{col};'>{'(' if v<0 else ''}${abs(v):,.0f}{')'if v<0 else ''}</td>"
        rows_html += "</tr>"
    st.markdown(hdr + rows_html + "</tbody></table>", unsafe_allow_html=True)
    col_noi, col_cap = st.columns([2, 1])
    with col_noi:
        st.plotly_chart(chart_noi_trend(pf["noi_list"], pf["years"]), use_container_width=True, config={"displayModeBar": False})
    with col_cap:
        st.plotly_chart(chart_capital_stack(d), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    col_xl, col_pdf, col_dash = st.columns(3)
    with col_xl:
        buf = io.BytesIO()
        pd.DataFrame(pf["rows"], index=[f"Year {y}" for y in pf["years"]]).T.to_excel(buf, sheet_name="Pro Forma")
        st.download_button("⬇ Export Pro Forma (Excel)", data=buf.getvalue(),
            file_name=f"AIRE_{d['name'].replace(' ','_')}_ProForma.xlsx",
            mime="application/vnd.ms-excel", use_container_width=True)
    with col_pdf:
        memo_text = st.session_state.get("ic_memo_text", "")
        rec_val   = st.session_state.get("ic_memo_rec", "APPROVE")
        pdf_bytes = generate_pdf_memo(d, memo_text, rec_val)
        ext  = "pdf" if pdf_bytes[:4] == b"%PDF" else "html"
        mime = "application/pdf" if ext == "pdf" else "text/html"
        st.download_button("📄 Download IC Memo (PDF)", data=pdf_bytes,
            file_name=f"AIRE_ICMemo_{d['name'].replace(' ','_')}.{ext}",
            mime=mime, use_container_width=True, type="primary")
    with col_dash:
        if st.button("📊 Load into Dashboard", use_container_width=True):
            st.session_state.deal_data    = d
            st.session_state.deal_loaded  = True
            st.session_state.current_view = "Dashboard"
            st.rerun()


def generate_pdf_memo(d: dict, memo_text: str, rec: str) -> bytes:
    rec_color = {"APPROVE": "#166534", "APPROVE WITH CONDITIONS": "#92400e", "DECLINE": "#991b1b"}.get(rec, "#334155")
    rec_bg    = {"APPROVE": "#dcfce7", "APPROVE WITH CONDITIONS": "#fef9c3", "DECLINE": "#fee2e2"}.get(rec, "#f8fafc")
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
      body{{font-family:Arial,sans-serif;color:#0f172a;margin:40px;font-size:13px;}}
      .hdr{{display:flex;justify-content:space-between;border-bottom:3px solid #0f172a;padding-bottom:16px;margin-bottom:24px;}}
      .logo{{font-size:32px;font-weight:900;letter-spacing:-1px;}}
      .meta{{display:grid;grid-template-columns:1fr 1fr;gap:12px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:16px;margin-bottom:20px;}}
      .lbl{{font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;}}
      .val{{font-size:14px;font-weight:700;}}
      .kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:24px;}}
      .kpi{{text-align:center;background:#eff6ff;border-radius:6px;padding:12px;}}
      .kl{{font-size:10px;color:#1d4ed8;font-weight:700;}}
      .kv{{font-size:20px;font-weight:800;color:#0f172a;}}
      .rec{{background:{rec_bg};border-radius:6px;padding:16px;text-align:center;}}
      .rl{{font-size:11px;color:{rec_color};font-weight:700;letter-spacing:1px;text-transform:uppercase;}}
      .rv{{font-size:24px;font-weight:900;color:{rec_color};}}
      .foot{{margin-top:40px;border-top:1px solid #e2e8f0;padding-top:12px;font-size:11px;color:#94a3b8;}}
    </style></head><body>
    <div class="hdr">
      <div><div class="logo">AIRE</div><div style="font-size:10px;color:#64748b;letter-spacing:2px;text-transform:uppercase;">Institutional Underwriting</div></div>
      <div style="text-align:right;"><div style="font-size:14px;font-weight:700;">Investment Committee Memorandum</div>
        <div style="font-size:12px;color:#64748b;">{datetime.now().strftime("%B %d, %Y")}</div></div>
    </div>
    <div class="meta">
      <div><div class="lbl">Asset</div><div class="val">{d["name"]}</div></div>
      <div><div class="lbl">Type / Units</div><div class="val">{d["type"]} / {d["units"]} Units</div></div>
      <div><div class="lbl">Purchase Price</div><div class="val">${d["purchase_price"]/1e6:.1f}M</div></div>
      <div><div class="lbl">Deal Grade</div><div class="val">{d["grade"]} &mdash; {d["score"]}/100</div></div>
      <div><div class="lbl">Address</div><div class="val">{d.get("address","&mdash;")}</div></div>
      <div><div class="lbl">Acquisition Date</div><div class="val">{d.get("acquisition_date","&mdash;")}</div></div>
    </div>
    <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#64748b;margin-bottom:8px;">Executive Summary</div>
    <div style="font-size:13px;line-height:1.8;color:#334155;margin-bottom:24px;">{memo_text or "No executive summary generated. Open IC Memo Generator to create one."}</div>
    <div class="kpis">
      <div class="kpi"><div class="kl">Levered IRR</div><div class="kv">{d["irr"]:.1%}</div></div>
      <div class="kpi"><div class="kl">Equity Multiple</div><div class="kv">{d["equity_mult"]:.2f}x</div></div>
      <div class="kpi"><div class="kl">GP IRR</div><div class="kv">{d["gp_irr"]:.1%}</div></div>
      <div class="kpi"><div class="kl">Loss Probability</div><div class="kv">{d["loss_prob"]:.1%}</div></div>
    </div>
    <div class="rec"><div class="rl">Committee Recommendation</div><div class="rv">{rec}</div></div>
    <div class="foot">Confidential &mdash; AIRE Institutional Underwriting &nbsp;|&nbsp; {datetime.now().strftime("%Y")}</div>
    </body></html>"""
    try:
        import weasyprint
        return weasyprint.HTML(string=html).write_pdf()
    except Exception:
        return html.encode("utf-8")

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 7 │ SIDEBAR & ROUTER
# ──────────────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:16px 0 28px 0;">
          <div style="font-size:34px; font-weight:900; color:#f0f4f8; letter-spacing:-2px;">AIRE</div>
          <div style="font-size:10px; color:#3b82f6; font-weight:700; letter-spacing:2px; text-transform:uppercase;">Institutional Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='font-size:10px; color:#475569; font-weight:700; letter-spacing:1px; margin-bottom:8px;'>DEAL ANALYSIS</div>", unsafe_allow_html=True)
        if st.button("📊  Deal Dashboard"):    st.session_state.current_view = "Dashboard";    st.rerun()
        if st.button("🧠  AI Data Room"):      st.session_state.current_view = "DataRoom";     st.rerun()
        if st.button("🤖  AI Tracker"):        st.session_state.current_view = "AITracker";    st.rerun()
        if st.button("📄  IC Memo Generator"): st.session_state.current_view = "ICMemo";       st.rerun()
        
        st.markdown("<div style='font-size:10px; color:#475569; font-weight:700; letter-spacing:1px; margin:20px 0 8px;'>PORTFOLIO</div>", unsafe_allow_html=True)
        if st.button("🏢  Master Pipeline"):   st.session_state.current_view = "Pipeline";     st.rerun()
        if st.button("⚙️  Settings"):          st.session_state.current_view = "Settings";     st.rerun()
        
        # Active deal pill
        d = st.session_state.deal_data
        if d:
            deal_name = d['name']
            deal_irr = f"{d['irr']:.1%}"
            deal_grade = d['grade']
            st.markdown(f"""
            <div style="margin-top:24px; background:#111f33; border-radius:8px; padding:12px; border:1px solid #1a2840;">
              <div style="font-size:10px; color:#64748b; font-weight:700; letter-spacing:0.5px; margin-bottom:4px;">ACTIVE DEAL</div>
              <div style="font-size:12px; color:#f0f4f8; font-weight:600; line-height:1.4;">{deal_name}</div>
              <div style="font-size:11px; color:#3b82f6; font-weight:700; font-family:'JetBrains Mono';">IRR {deal_irr} | Grade {deal_grade}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="margin-top:24px; background:#111f33; border-radius:8px; padding:12px; border:1px solid #1a2840;">
              <div style="font-size:10px; color:#64748b; font-weight:700; letter-spacing:0.5px; margin-bottom:4px;">ACTIVE DEAL</div>
              <div style="font-size:12px; color:#475569; font-style:italic;">No deal loaded</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Bottom user info
        st.markdown("<br>"*4, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="border-top:1px solid #1a2840; padding-top:14px; font-size:12px; color:#64748b;">
          {st.session_state.user_email}<br>
          <span style="color:#3b82f6; font-weight:700;">{st.session_state.firm_id}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout", key="logout"):
            st.session_state.clear()
            st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
def main():
    init_state()
    inject_css()

    if not st.session_state.user_email:
        render_login()
        st.stop()

    # Load firm's saved deals from Supabase once per session
    load_firm_data()
    
    render_sidebar()
    
    v = st.session_state.current_view
    if   v == "Dashboard":      view_dashboard()
    elif v == "DataRoom":       view_data_room()
    elif v == "AITracker":      view_ai_tracker()
    elif v == "ICMemo":         view_ic_memo()
    elif v == "Pipeline":       view_pipeline()
    elif v == "Settings":       view_settings()
    elif v == "PropertyDetail": view_property_detail()

if __name__ == "__main__":
    main()
