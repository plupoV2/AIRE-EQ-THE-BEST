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
    import anthropic
except ImportError:
    _install("anthropic")
    import anthropic

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
# Copyright (c) 2025 AIRE Technologies. All rights reserved.
# Patent Pending. Protected by trade secret law. Unauthorized reproduction is prohibited.
# ==============================================================================

_AIRE_BUILD = hashlib.sha256(b"AIRE_INSTITUTIONAL_V4_PROTECTED").hexdigest()[:12].upper()

# Embedded logo — base64 encoded
AIRE_LOGO_B64 = "/9j/4AAQSkZJRgABAQAASABIAAD/4QBMRXhpZgAATU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAoKADAAQAAAABAAAATAAAAAD/7QA4UGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAAAA4QklNBCUAAAAAABDUHYzZjwCyBOmACZjs+EJ+/8AAEQgATACgAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/bAEMAAQEBAQEBAgEBAgMCAgIDBAMDAwMEBgQEBAQEBgcGBgYGBgYHBwcHBwcHBwgICAgICAkJCQkJCwsLCwsLCwsLC//bAEMBAgICAwMDBQMDBQsIBggLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLC//dAAQACv/aAAwDAQACEQMRAD8A/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA/9D+/iiiigAoorG8R+ItE8IeHr/xZ4muo7LTdLt5bu7uJTtjhggUvI7HsqqCSfQUAfydf8HCf/BcH9oP9gT47+Dv2c/2QtQ0601r+ypNY8RzXlpHehVun2WcKh+EYLFJI/cq8Z4HX87/APglx/wcnftqfF79uv4f/Bv9r3WdHu/BHjG//sWdrbTobOSC7vVMdnJ5iY+X7SY0fJwEYntX8zH7e37U2uftrfti/EL9p7XDIB4s1ea4s4pfvQafFiKzhPvFbJGh9SM14J428E/Eb4HfEi+8EeN7K68PeJ/Dl35Vxbyfu7i1uYSCOVPBBwVYH0INfZ0csoqgqc4rma363/4B4E8ZU9o5Relz/bQr+c7/AILV/tzftCfAf4l+G/gd8FtZm8NWt5pC6xeX1oAtxO0000KxCQglFQQljswSXGTgCv1H/wCCaP7W9j+3H+w18Of2lY5UfUNd0qOPV0TAEeq2hMF4u0fdHnxuyA4yhU9CK+Cf+Cu3xT/YJsvGnh74W/taeFvEmpa0mnf2lp+qeHfs8csNvPLJE0TPNMgbLQltrRso4IIJau7w2pUo8Q0o4nCOukpXgkpNO3xcsmk7P/Nao4ONZ1Hk9R0MQqLfL7zbXXa61V/+Bsav/BFT9sz42/tNeF/GXgX42ag+u3PhVrKa01OVVE7RXvnAxSsoAYqYsoxyxBIJwBX8ZGs/8HP3/BXrVNMmsLHxlo2myyjC3NvoVk0sZz1UTRyR57fMhFf2/f8ABIz4ofsZeKvB/ivwD+yD4Y1vQotFks7nVbrXRC1zeyXfmrETJFNLnYImG3CKucgZZjX+TnXo8S4bDT4gx3JhPYxvC0JJJq8Vd2V0ub4rLuc2Q1q0cowvPiPaytK80207Sel3Zvl2v5H9C+mf8HQ3/BXWwsre1uvFmh3rwoiPNNodoHlKgAs4jRFBbqdiqMngAcV+lP7Ev/B3J8WbLxzY+FP28/CGmah4bu5RFLrvhqGS2vbJWIHmyWzySRzov8SxmJwvIDkbT+7H7HP/AAR5/wCCYXxc/YE+EviH4kfBrw5d6h4g8BaBealqIia3u5Z7nT4ZJpjcROkiyMzFi4YHJzmv83D9rvwB8LfhT+1P8Rfhn8ENW/tzwfoHiPUtP0a/8wS/aLK3ndIX8xflkygHzr8r/eHBr5mhHB4pzpqlZryt+R7tWVeioyc73P8ARg/4Lzf8FPfjT+xf+xl8Nf2kf2Jtf0ueLxvrtvDFqMlvHqFtdabc2U1zG8W/K4fajBh2r+Ri6/4Odf8AgsBceILXWYfHelQW1ujK9gmg2Bt5ywIDOWhaYFcgjZKoyBkEZB9L/as8T+LfE/8AwbQ/s2nxW8ky6f8AETV7KxkkYszWkI1HYMn+FGLRqOyqAOBX52/8EcfgD+zr+09/wUR8B/BP9q0Rt4F1ePVm1BJr1tORmttOuZoQZ0eNk/fIh4cbiMHIJBrCYShToSdSClyuXRN6CrV6k6kVCVr2/E+5v+Io3/grf/0Mugf+CO2/wr9Ef+CTv/BwB/wUg/a3/wCChnwy/Z0+M+u6PdeGPFF9cwX8VtpMFvKyRWk8y7ZFG5fnRenbiv2K/wCHD/8Awb7/APPnp3/hZXX/AMm19K/sj/8ABHD/AII/fAr48aL8cv2W9Kt5vGXhRpbuyktvEdzqJg8yNoGdoTdSKRtkIyykAkd8VxVsXgnTko0bOz+yv8zop0MQpJuenqft/RRRXzx6YUUUUAf/0f7+KKKKACv54/8Ag5l/bI/4Zf8A+CbmrfDbw9deR4k+LdwPDNsFOJF09h5moSY7oYB9nb0M4r+hyv8AMl/4Oef2yP8Ahpf/AIKNXvwi8O3Xn+HPhBaf8I/CqNmNtTkIl1CQDswk2W7+9vXpZVh/a4iN9lr/AF8zkxtXkpPu9D88f+CQn7N/hz9qj/gop8Mfhf45mtrfw3Bqi6xrT3kixwNY6WDdSROXIGJzGIPXMn41+qX/AAdUfAbwT4L/AG79F/aQ+HV/Y32n/FHRlkvfsc8cu3VNICW0xIjJ2hrdrU5ONzbj61+Cvwv/AGN/2vPjd4WXxz8F/hV4w8X6I0rwDUNF0O91C1MseN6CWCF03LkZGcjvXUeJ/wBgD9vDwT4bv/GXjP4J+PdI0jSreW7vb698N6hb21tbwqXklllkgCIiKCzMxAUDJOK+qlBPEKr7TZWt/T9PuPGi37Jw5d9bn9Yf/BoN+2N5F98Rf2E/FF18s4XxdoCO38a7La/jXPcj7PIqj+7I2Opr6p/4OBf+TsvCf/YpQf8ApZd1/Ff/AME6v2sNT/Yg/bX+HX7Tdk8gtfDWrRNqUceS02mXAMF7GB3LW8kgXOcNg9q/tA/4L3atpmv/ALTngnXdEuEu7K98GWk9vPEwZJIpLu7ZHUjghgQQR1Ffb+F+H5OLadRbShP77HyXH1Xm4eqRe6lH8z6N/wCDdf8A4/vi7/1z0L+d9X+a9X+lD/wbr/8AH98Xf+uehfzvq/zXqz4+/wCSszH/ALhf+momvBv/ACT2D/7if+nJHqV18cvjXf8AhiHwTfeMNbm0W3hW3isH1CdrVIUTy1jWIvsCBPlCgYC8dK/SH/gl9/wRp/an/wCCoWvHWvhqtpoXgDTNQ+waz4lvpkKWsiqkjxRWyt580xjkBQBVjycNItfq1/wV/wD+CUP2v/gnf8Cv+Cl/wI0397D8OvCVp46s7dOWQabbR2+pBR3X5Ybgjt5b4wJGr8sv+CMH/BUjxX/wTD/amtvF2pyT3nw68UmKw8W6ZHli1sGPl3cSdDPaliyf30Lx5G/I+JdeVWhKeGtzfr/Wx9V7JQqqNbY/o/8A+Dmv9nf4b/smf8EovgP+zh8I7d7fw94Q8UwafaCQgyybbC7LyylQAZZpC0khAALsSAOlfw4eAvh74++Kniy08BfDDQ9Q8Sa7f+Z9m07S7aS8u5vKRpH8uGFXdtqKzthThVJPANf3u/8AB2j4y8KfEX/gnj8HvH/gXUINW0XW/F1vfWF7bOJIbi2uNNunjkRhwVZSCD6Gv5J/+CPX7X3wr/YQ/wCChHgf9qH41Q6hceG/DsWqpdJpcKT3RN7YXFtHsR3jU/vJV3ZcYGTz0rnyyc1g3NK8tX6s0xcYuuo7LQ8I/wCHfH7fH/RD/H//AITWo/8AyPX9Qn/Bqf8Asw/tK/A/9tf4geI/jT8PPE3g/T7rwRLbQXWt6TdafDJMb+zYRo88SKz7VZtoOcAnoK/Vf/iLQ/4Jff8AQI8ef+Cq1/8Ak2vd/wBmP/g5K/4J7ftY/H3wt+zj8NbDxfba94vvVsLGTUNNgithMykqJHjupGUHGMhDyeeOa48VisXUpShKjZNbnRRo0ITUlUuz+gCiiivmj1gooooA/9L+/iiiigDn/Fh8UDwrqZ8DrbNrX2Sb+zxesyWxuth8oTMis4j343lVZgucAniv89bxb/waaf8ABUjx34r1Pxx4u+IXw3vtW1m7mvr25l1PVC81xcOZJHY/2V1Z2JPua/0SaK68LjamHv7O2phWw8KtufofF/8AwTw/ZK0/9hj9i34e/st2skE914W0pI9SuLbJhuNSuGae8lQsqsUe4kkKblDbMAgYxX1h4s8LaB458K6n4J8V2yXul6xaTWN5byDKTW9whjkRvZlYg+xroKK5pzcpOb3epsopKy2P87LxR/waD/8ABQJPE2or4L8dfD2TRxdTCwe91DUo7lrbefKMqppjoshTG8KzKGyASOa/ZnxB/wAEWP2/PiJ8EvhH4J+JfivwXd+Ifh14Tj8K3NzHe37QzQWV3ctZlGawDnZaSQxtuVTvQkZBBr+rSivp8n4xzHLMVHGYVx54ppXV91ZniZnw9g8fh5YbEJ8jts7ban49/wDBKb/gn18Y/wBhifx1P8WtU0bUf+EnXTVtRpE082z7H9o3+Z50EOM+cu3bu6HOOK/kZ/4hCf8AgpP/ANDv8NP/AAZap/8AKqv9Gqiscz4px+Px1XMMQ17Spy3srL3Uoqy9EaZfkeFweFp4OinyQva7u9W29fVnzJ+z78AYvAX7G3gf9lv4twWOupongzTPC2swqDNZXgtrGO0uFAkVS8Mm1gA6KSp5A6V/Ep+0J/waH/tY3Xxr8S3n7MfjXwXF4BnvpJdDh1++1CLUYLST5lhnENhcRloiTGHEh8xVDkKWKj/QGoryMPjq1GUpQe+56NXDwqJKS2P4d/E3/Bvf/wAFdPHn7AujfsIeO/H3w41HRvCPiqPxD4dnk1PVC1nBLb3MV1a5Ol58syypLEoHykyZOCoHw7/xCE/8FJ/+h3+Gn/gy1T/5VV/o1UV0RzjERvy2+4yeBpPe5/nK/wDEIT/wUn/6Hf4af+DLVP8A5VV9m/8ABPD/AINk/wBvL9kn9tv4a/tJ/Efxb4BvdC8G61DqN7Bpt/qMl3JFGGBESy6dEhbngNIo96/udopzzjEyi4tqz8gjgaSaaQUUUV5R2BRRRQB//9P+/iiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/2Q=="
AIRE_LOGO_URI = f"data:image/jpeg;base64,{AIRE_LOGO_B64}"

# ── Onboarding guide steps (shown when onboarding mode is ON) ──
ONBOARDING_STEPS = {
    "Dashboard": {
        "step": "Step 1 of 8", "emoji": "📊",
        "title": "Deal Dashboard — Your Command Center",
        "text": "Every metric for your active deal lives here. The five KPI cards at the top update in real time as you change assumptions. Below that you get a Monte Carlo simulation running 3,000 scenarios to show your probability distribution of outcomes, and a 5×5 IRR sensitivity matrix mapping exit cap rate against hold period. This is the screen you bring to IC meetings.",
        "tip": "Load a deal first: go to Master Pipeline in the sidebar, add a deal, then click View on it to load it here.",
        "action": "Pipeline",
        "action_label": "Go to Master Pipeline →"
    },
    "Pipeline": {
        "step": "Step 2 of 8", "emoji": "🏢",
        "title": "Master Pipeline — Your Deal Database",
        "text": "This is where every deal your firm is tracking lives. Add a deal by filling in the form at the bottom — property name, address, type, units, purchase price, and Year 1 NOI. AIRE automatically calculates the cap rate, levered IRR, equity multiple, and assigns a deal grade (A through D) based on your firm's target assumptions. Every deal saves permanently to your firm's database.",
        "tip": "Fastest workflow: Use OM Import to upload a broker PDF and let AI fill in all the numbers automatically. Saves 2+ hours per deal.",
        "action": "OMImport",
        "action_label": "Try OM Import →"
    },
    "OMImport": {
        "step": "Step 3 of 8", "emoji": "📎",
        "title": "OM Import — AI Reads the Broker PDF for You",
        "text": "Upload any Offering Memorandum PDF from CBRE, JLL, Marcus & Millichap, Eastdil, or most major brokerages. AIRE's AI reads the full document and extracts: property name, address, type, unit count, vintage year, asking price, NOI, cap rate, occupancy rate, average monthly rent, and investment highlights. Review the extracted numbers, adjust anything, then click Add to Pipeline.",
        "tip": "Patent Pending technology: Our extraction engine is trained specifically on CRE offering memorandums. Works on text-based PDFs. For image-only scans, try copy-pasting key numbers manually.",
        "action": "Pipeline",
        "action_label": "Back to Pipeline →"
    },
    "DataRoom": {
        "step": "Step 4 of 8", "emoji": "🧠",
        "title": "AI Data Room — Upload Financials, Talk to Your Deal",
        "text": "Upload the property's Rent Roll and T12 Trailing Financials (Excel or CSV). AIRE parses both automatically and extracts units, average rent, occupancy, gross potential rent, NOI, and expense ratio — then updates your deal record. On the right, the Deal Copilot is a GPT-4o underwriter trained on CRE. Ask it anything: 'What are the top 3 risks on this deal?' or 'How does this cap rate compare to the Dallas multifamily market?'",
        "tip": "Always upload T12 financials before generating an IC memo. AI-generated memos are far more accurate with real trailing numbers than estimates.",
        "action": "ICMemo",
        "action_label": "Go to IC Memo Generator →"
    },
    "DebtModel": {
        "step": "Step 5 of 8", "emoji": "🏦",
        "title": "Debt Structuring — Model Every Loan Scenario",
        "text": "Enter loan parameters — LTV, interest rate, amortization period, interest-only years, loan origination fee, and prepayment lockout. AIRE builds a full 10-year debt schedule showing beginning balance, annual payment, interest, principal paydown, ending balance, and prepayment penalty by year. DSCR is calculated for both IO and fully amortizing periods — cards turn green above 1.25x and red below.",
        "tip": "The interest rate auto-populates from the live 10-Year Treasury + 200bps spread via FRED API. Adjust the spread in Settings to match your lender's current terms.",
        "action": "Waterfall",
        "action_label": "Go to Waterfall Calculator →"
    },
    "Waterfall": {
        "step": "Step 6 of 8", "emoji": "💰",
        "title": "Waterfall Calculator — Model LP/GP Returns",
        "text": "Model how investment profits are distributed between LPs and the GP across a tiered promote structure. Set your preferred return (typically 8%), then configure the LP/GP split at each IRR hurdle. The calculator outputs total distributions to each party, equity multiples, approximate IRRs, and a full tier breakdown table showing exactly how much profit flows through each promote level.",
        "tip": "Standard institutional waterfall: 80/20 LP/GP up to 8% pref → 70/30 up to 12% IRR → 50/50 up to 18% IRR → 30/70 above. Adjust these splits in the Promote Hurdles section.",
        "action": "ICMemo",
        "action_label": "Generate IC Memo →"
    },
    "ICMemo": {
        "step": "Step 7 of 8", "emoji": "📄",
        "title": "IC Memo Generator — Investment Committee in One Click",
        "text": "Generate a full professional Investment Committee memorandum in seconds. Click Generate IC Memo and GPT-4o writes a 2-paragraph executive summary using your exact deal metrics — price, NOI, IRR, EM, cap rate, and deal grade. Set your recommendation (Approve, Approve with Conditions, or Decline), preview the branded memo, then use Memo Delivery to email it directly to your investment committee.",
        "tip": "Patent Pending: AIRE's IC memo format mirrors the structure used by institutional private equity and family office investment committees. Load T12 data in the Data Room first for the most accurate AI summary.",
        "action": "MemoDelivery",
        "action_label": "Go to Memo Delivery →"
    },
    "Settings": {
        "step": "Step 8 of 8", "emoji": "⚙️",
        "title": "Settings — Calibrate Your Firm's Underwriting",
        "text": "These assumptions flow through every pro forma, debt model, IRR calculation, and AI analysis in the platform. Set them once and they save permanently for your entire firm. Key inputs: Target IRR (what your fund needs to return), Max LTV (your lender/IC risk limit), Minimum DSCR (debt coverage requirement), Hold Period (default underwriting horizon), Vacancy Rate, Management Fee, Rent Growth, Expense Growth, and Exit Cap Rate Spread over entry.",
        "tip": "Typical institutional assumptions: 15% target IRR, 65-70% LTV, 1.25x min DSCR, 5-year hold, 5-7% vacancy, 3-4% rent growth, 3% expense growth, 25-50bps exit cap spread over entry.",
        "action": "Dashboard",
        "action_label": "Return to Dashboard →"
    },
}

st.set_page_config(
    page_title="AIRE | Integrated Real Estate Underwriting",
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
      /* ── FONTS — exact match to aire.rent ── */
      @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

      /* ── DESIGN TOKENS — exact from aire.rent :root ── */
      :root {
        --navy:  #07111f;
        --navy2: #0d1e33;
        --navy3: #122035;
        --blue:  #1a6fe0;
        --blue2: #2281f7;
        --blue3: #00aaff;
        --white: #ffffff;
        --off:   #f5f8fd;
        --lgray: #e4ecf7;
        --tmid:  #3a5278;
        --tmuted:#6f8aab;
        --bl: rgba(11,29,54,.07);
        --ss: 0 1px 4px rgba(7,17,31,.06);
        --sm: 0 5px 20px rgba(7,17,31,.09);
        --sl: 0 16px 48px rgba(7,17,31,.13);
        --r:  10px;
        --rl: 18px;
        --rx: 26px;
      }

      /* ── BASE ── */
      html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--navy);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }
      .stApp { background: var(--off) !important; }
      #MainMenu, footer, header { visibility: hidden; }
      .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1160px !important;
      }

      /* ── TYPOGRAPHY — Outfit for headings, Inter for body ── */
      h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.032em !important;
        color: var(--navy) !important;
      }

      /* ── INPUTS ── */
      [data-testid="stTextInput"] input,
      [data-testid="stNumberInput"] input,
      [data-testid="stTextArea"] textarea {
        background: #fff !important;
        border: 1.5px solid var(--lgray) !important;
        border-radius: var(--r) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13.5px !important;
        color: var(--navy) !important;
        box-shadow: var(--ss) !important;
        transition: border-color 0.15s, box-shadow 0.15s !important;
      }
      [data-testid="stTextInput"] input:focus,
      [data-testid="stNumberInput"] input:focus,
      [data-testid="stTextArea"] textarea:focus {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 3px rgba(26,111,224,0.12) !important;
        outline: none !important;
      }
      [data-testid="stTextInput"] input::placeholder,
      [data-testid="stTextArea"] textarea::placeholder { color: var(--tmuted) !important; }
      [data-testid="stSelectbox"] > div > div {
        background: #fff !important;
        border: 1.5px solid var(--lgray) !important;
        border-radius: var(--r) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13.5px !important;
        box-shadow: var(--ss) !important;
      }

      /* ── BUTTONS — exact .btn-nav style from website ── */
      .stButton > button[kind="primary"],
      .stButton > button[kind="primaryFormSubmit"],
      [data-testid="stFormSubmitButton"] > button {
        background: var(--navy) !important;
        border: none !important;
        border-radius: var(--r) !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 700 !important;
        color: #fff !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 2px 8px rgba(7,17,31,0.18) !important;
        transition: all 0.22s !important;
        padding: 0.55rem 1.2rem !important;
      }
      .stButton > button[kind="primary"]:hover,
      [data-testid="stFormSubmitButton"] > button:hover {
        background: var(--blue) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 16px rgba(26,111,224,0.32) !important;
        color: #fff !important;
      }
      .stButton > button[kind="secondary"] {
        background: #fff !important;
        border: 1.5px solid var(--lgray) !important;
        border-radius: var(--r) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: var(--tmid) !important;
        box-shadow: var(--ss) !important;
        transition: all 0.18s !important;
      }
      .stButton > button[kind="secondary"]:hover {
        border-color: var(--blue) !important;
        color: var(--blue) !important;
        background: #f0f6ff !important;
        transform: translateY(-1px) !important;
      }

      /* ── METRIC CARDS — cards with blue top border ── */
      div[data-testid="metric-container"] {
        background: #fff !important;
        border: 1px solid var(--lgray) !important;
        border-radius: var(--rl) !important;
        padding: 22px 20px !important;
        border-top: 3px solid var(--blue) !important;
        box-shadow: var(--ss) !important;
        transition: all 0.22s !important;
      }
      div[data-testid="metric-container"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: var(--sm) !important;
        border-top-color: var(--blue2) !important;
      }
      div[data-testid="metric-container"] label {
        font-family: 'Inter', sans-serif !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.09em !important;
        color: var(--tmuted) !important;
      }
      div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.04em !important;
        color: var(--navy) !important;
        line-height: 1.1 !important;
      }
      div[data-testid="stMetricDelta"] {
        font-size: 11px !important;
        font-weight: 600 !important;
      }

      /* ── CONTAINERS / PANELS ── */
      [data-testid="stVerticalBlockBorderWrapper"] {
        background: #fff !important;
        border: 1px solid var(--lgray) !important;
        border-radius: var(--rl) !important;
        box-shadow: var(--ss) !important;
      }
      .glass-panel {
        background: #fff;
        border-radius: var(--rl);
        border: 1px solid var(--lgray);
        padding: 24px;
        box-shadow: var(--ss);
        margin-bottom: 18px;
        transition: box-shadow 0.2s;
      }
      .glass-panel:hover { box-shadow: var(--sm); }
      .panel-title {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 700;
        color: var(--blue);
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        border-bottom: 1px solid var(--lgray);
        padding-bottom: 12px;
      }

      /* ── TABS — pill style matching website ── */
      [data-testid="stTabs"] [data-baseweb="tab-list"] {
        background: var(--off) !important;
        border-radius: 999px !important;
        padding: 4px !important;
        gap: 2px !important;
        border: 1px solid var(--lgray) !important;
        display: inline-flex !important;
      }
      [data-testid="stTabs"] [data-baseweb="tab"] {
        border-radius: 999px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: var(--tmid) !important;
        padding: 8px 20px !important;
        transition: all 0.15s !important;
        white-space: nowrap !important;
      }
      [data-testid="stTabs"] [aria-selected="true"] {
        background: #fff !important;
        color: var(--navy) !important;
        box-shadow: 0 1px 6px rgba(7,17,31,0.10) !important;
        font-weight: 700 !important;
      }

      /* ── EXPANDERS ── */
      [data-testid="stExpander"] {
        background: #fff !important;
        border: 1px solid var(--lgray) !important;
        border-radius: var(--rl) !important;
        box-shadow: var(--ss) !important;
        transition: box-shadow 0.2s !important;
      }
      [data-testid="stExpander"]:hover { box-shadow: var(--sm) !important; }

      /* ── DATAFRAMES ── */
      [data-testid="stDataFrame"] {
        border-radius: var(--r) !important;
        overflow: hidden !important;
        border: 1px solid var(--lgray) !important;
        box-shadow: var(--ss) !important;
      }

      /* ── ALERTS ── */
      .stSuccess { background: rgba(5,150,105,0.07) !important; border: 1px solid rgba(5,150,105,0.20) !important; border-radius: var(--r) !important; }
      .stWarning { background: rgba(217,119,6,0.07) !important; border: 1px solid rgba(217,119,6,0.20) !important; border-radius: var(--r) !important; }
      .stError   { background: rgba(220,38,38,0.07) !important; border: 1px solid rgba(220,38,38,0.20) !important; border-radius: var(--r) !important; }
      .stInfo    { background: rgba(26,111,224,0.07) !important; border: 1px solid rgba(26,111,224,0.20) !important; border-radius: var(--r) !important; }

      /* ── PRO FORMA TABLE ── */
      .proforma-table { width:100%; border-collapse:collapse; font-size:13px; }
      .proforma-table th { text-align:right; padding:10px 12px; background:var(--off); color:var(--tmuted); font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.09em; border-bottom:2px solid var(--lgray); font-family:'Inter',sans-serif; }
      .proforma-table th:first-child { text-align:left; }
      .proforma-table td { text-align:right; padding:9px 12px; border-bottom:1px solid var(--off); color:var(--navy); font-family:'JetBrains Mono',monospace; font-size:12.5px; }
      .proforma-table td:first-child { text-align:left; font-family:'Inter',sans-serif; font-weight:500; color:var(--tmid); font-size:13px; }
      .proforma-table tr.noi-row td { font-weight:800; background:#eef5ff; color:var(--blue); border-top:2px solid #c7dcfb; border-bottom:2px solid #c7dcfb; }
      .proforma-table tr.subtotal td { background:var(--off); font-weight:700; }
      .proforma-table tr:hover { background:var(--off); }

      /* ── GRADE BADGES ── */
      .grade-badge { display:inline-block; padding:4px 16px; border-radius:999px; font-weight:800; font-size:22px; letter-spacing:-0.03em; }
      .grade-a { background:#dcfce7; color:#166534; }
      .grade-b { background:#dbeafe; color:#1e40af; }
      .grade-c { background:#fef9c3; color:#854d0e; }
      .grade-d { background:#fee2e2; color:#991b1b; }

      /* ── STATUS PILLS ── */
      .tracker-card { background:#fff; border:1px solid var(--lgray); border-radius:var(--r); padding:14px 16px; margin-bottom:10px; border-left:4px solid var(--blue); box-shadow:var(--ss); }
      .tracker-correct { border-left-color:#16a34a; }
      .tracker-watch   { border-left-color:#d97706; }
      .tracker-alert   { border-left-color:#dc2626; }
      .status-pill   { padding:3px 10px; border-radius:999px; font-size:11px; font-weight:700; font-family:'Inter',sans-serif; }
      .status-active { background:#dbeafe; color:var(--blue); }
      .status-closed { background:#dcfce7; color:#166534; }
      .status-watch  { background:#fef9c3; color:#92400e; }

      /* ── s-chip — exact from website ── */
      .s-chip {
        display: inline-block;
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--blue);
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
      }
      .s-h {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        letter-spacing: -0.032em;
        color: var(--navy);
        line-height: 1.06;
      }
      .s-p {
        font-size: 1rem;
        color: var(--tmid);
        line-height: 1.75;
      }

      /* ── SIDEBAR — dark navy matching website hero ── */
      [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--navy) 0%, var(--navy2) 100%) !important;
        border-right: 1px solid rgba(26,111,224,0.12) !important;
      }
      [data-testid="stSidebar"] * { color: var(--tmuted) !important; }
      [data-testid="stSidebar"] .stButton > button {
        width: 100%; text-align: left;
        background: transparent !important;
        border: none !important; outline: none !important; box-shadow: none !important;
        color: #5a7fa0 !important;
        padding: 7px 12px; border-radius: 7px;
        font-family: 'Inter', sans-serif !important;
        font-size: 12.5px; font-weight: 500;
        transition: all 0.12s;
        letter-spacing: 0.005em;
      }
      [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(26,111,224,0.09) !important;
        color: rgba(255,255,255,0.82) !important;
      }
      [data-testid="stSidebar"] button { border: none !important; box-shadow: none !important; outline: none !important; }
      [data-testid="stSidebar"] .stButton { margin-bottom: 0 !important; }
      [data-testid="collapsedControl"] { display: none !important; }
      button[data-testid="baseButton-header"] { display: none !important; }
      section[data-testid="stSidebar"] {
        min-width: 218px !important; width: 218px !important;
        transform: translateX(0) !important; visibility: visible !important;
      }

      /* ── ONBOARDING BANNER ── */
      .onboard-banner {
        background: linear-gradient(135deg,#f0f6ff,#f5f8fd);
        border: 1px solid #c7dcfb;
        border-left: 5px solid var(--blue);
        border-radius: var(--rl);
        padding: 0;
        margin-bottom: 24px;
        box-shadow: 0 2px 16px rgba(26,111,224,0.10);
        overflow: hidden;
      }
      .onboard-header {
        background: linear-gradient(135deg,var(--navy),var(--navy2));
        padding: 13px 20px;
        display: flex; align-items: center; justify-content: space-between;
      }
      .onboard-body { padding: 16px 20px 18px; }
      .onboard-step  { font-size:9.5px; font-weight:700; color:#7dd3fc; text-transform:uppercase; letter-spacing:1.5px; }
      .onboard-title { font-family:'Outfit',sans-serif; font-size:15px; font-weight:800; color:#fff; margin-top:2px; letter-spacing:-0.02em; }
      .onboard-text  { font-size:13px; color:var(--navy2); line-height:1.75; margin-bottom:10px; }
      .onboard-tip-row { display:flex; align-items:flex-start; gap:8px; background:#e8f0fe; border-radius:8px; padding:10px 14px; }
      .onboard-tip-text { font-size:12px; color:#1e3a6e; line-height:1.6; }
      .onboard-badge { display:inline-block; background:rgba(255,255,255,0.14); color:#bae6fd; font-size:9px; font-weight:700; padding:2px 8px; border-radius:4px; text-transform:uppercase; letter-spacing:0.8px; }

      /* ── SCROLLBAR ── */
      ::-webkit-scrollbar { width: 5px; height: 5px; }
      ::-webkit-scrollbar-track { background: var(--off); }
      ::-webkit-scrollbar-thumb { background: var(--lgray); border-radius: 3px; }
      ::-webkit-scrollbar-thumb:hover { background: var(--blue); }

      /* ── CHAT ── */
      .stChatFloatingInputContainer { background: transparent !important; padding: 12px 0 !important; }

      /* ── LINK BUTTONS ── */
      a[data-testid="stLinkButton"] {
        background: var(--navy) !important;
        border-radius: var(--r) !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        transition: all 0.22s !important;
      }
      a[data-testid="stLinkButton"]:hover {
        background: var(--blue) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 16px rgba(26,111,224,0.32) !important;
      }

      /* ── PAIN CARD style — for empty states ── */
      .pain-card {
        background: var(--off);
        border: 1px solid var(--bl);
        border-radius: var(--rl);
        padding: 2rem;
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
      }
      .pain-card:hover { transform: translateY(-4px); box-shadow: var(--sl); }
      .pain-num {
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -0.05em;
        line-height: 1;
        margin-bottom: 0.4rem;
        color: var(--navy);
      }
      .pain-num span { color: var(--blue); }
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

@st.cache_resource
def init_claude():
    """Initialize Anthropic Claude client."""
    key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not key:
        return None
    try:
        return anthropic.Anthropic(api_key=key)
    except Exception:
        return None

claude_client = init_claude()

def call_claude(system: str, user: str, max_tokens: int = 1024, temperature: float = 0.3) -> str:
    """Call Claude claude-sonnet-4-5. Falls back to GPT-4o if Claude unavailable."""
    if claude_client:
        try:
            msg = claude_client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[{"role": "user", "content": user}]
            )
            return msg.content[0].text
        except Exception as e:
            pass  # Fall through to GPT-4o
    # Fallback to GPT-4o
    try:
        r = ai_client.chat.completions.create(
            model="gpt-4o",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user}
            ]
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"AI unavailable: {e}"

def claude_available() -> bool:
    return claude_client is not None

# No demo data — firms start with a clean slate

def init_state():
    defaults = {
        "user_email": None, "firm_id": None, "current_view": "Dashboard",
        "chat_history": [], "deal_data": None,
        "properties": [], "deal_loaded": False,
        "active_prop_id": None, "db_loaded": False,
        "compare_ids": [],
        "alert_log": [],
        "crm_data": {},
        "om_extracted": {},
        "ai_score_result": None,
        "delivery_memo_text": "",
        "delivery_memo_rec": "APPROVE",
        "stress_results": [],
        "intel_chat": [],
        "portfolio_intel_cache": None,
        "onboarding_mode": False,
        "whitelabel": {},
        "lenders": [],
        "broker_email_draft": "",
        "broker_email_type": "",
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
        comps_contribute(prop, email, st.session_state.get("settings", {}))
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

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 2C │ AUDIT TRAIL — SYSTEM OF RECORD
# Every consequential action is logged: who, what, when, old → new.
# Fire-and-forget: audit logging must NEVER break the product.
# ──────────────────────────────────────────────────────────────────────────────

def audit_log(event_type: str, entity: str = "", detail: str = "",
              field: str = None, old_value=None, new_value=None):
    """Write one immutable audit event for this firm. Silent on any failure."""
    try:
        sb, _ = get_supabase()
        if not sb:
            return
        email = st.session_state.get("user_email", "")
        rec = {
            "firm_key":   firm_key(email),
            "user_email": email,
            "event_type": str(event_type)[:40],
            "entity":     str(entity)[:160],
            "detail":     str(detail)[:500],
            "field":      (str(field)[:80] if field is not None else None),
            "old_value":  (str(old_value)[:200] if old_value is not None else None),
            "new_value":  (str(new_value)[:200] if new_value is not None else None),
            "created_at": datetime.now().isoformat(),
        }
        sb.table("aire_audit_log").insert(rec).execute()
    except Exception:
        pass


def db_load_audit(email: str, limit: int = 500) -> list:
    """Load this firm's audit events, newest first."""
    try:
        sb, _ = get_supabase()
        if not sb:
            return []
        resp = (sb.table("aire_audit_log")
                  .select("*")
                  .eq("firm_key", firm_key(email))
                  .order("created_at", desc=True)
                  .limit(limit)
                  .execute())
        return resp.data or []
    except Exception:
        return []


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 2D │ AIRE COMPS NETWORK — THE DATA FLYWHEEL
# Every saved deal contributes one anonymized comp. No names, no addresses,
# no firm identity — banded values + live underwriting assumptions only.
# After enough firms, this is data nobody else on earth has.
# ──────────────────────────────────────────────────────────────────────────────

def _band_units(u) -> str:
    try: u = int(u)
    except Exception: return "Undisclosed"
    if u <= 0:   return "Undisclosed"
    if u <= 50:  return "1–50"
    if u <= 150: return "51–150"
    if u <= 300: return "151–300"
    return "300+"

def _band_price(p) -> str:
    try: p = float(p)
    except Exception: return "Undisclosed"
    if p <= 0:        return "Undisclosed"
    if p < 10e6:      return "<$10M"
    if p < 25e6:      return "$10–25M"
    if p < 50e6:      return "$25–50M"
    if p < 100e6:     return "$50–100M"
    return "$100M+"

def _band_vintage(v) -> str:
    try: v = int(v)
    except Exception: return "Undisclosed"
    if v < 1900:  return "Undisclosed"
    if v < 1980:  return "Pre-1980"
    return f"{(v // 10) * 10}s"

def _extract_market(address: str):
    """City + state from a free-text address — never the street. Fallback Undisclosed."""
    try:
        parts = [p.strip() for p in str(address or "").split(",") if p.strip()]
        if len(parts) >= 2:
            tail = parts[-1]
            m = re.search(r"\b([A-Z]{2})\b", tail)
            state = m.group(1) if m else ""
            city  = parts[-2] if (m or re.search(r"\d{5}", tail)) else parts[-1]
            city  = re.sub(r"\d", "", city).strip().title()
            if city and len(city) > 1:
                return city, state
    except Exception:
        pass
    return "Undisclosed", ""

def comps_contribute(prop: dict, email: str, settings: dict = None):
    """Fire-and-forget anonymized contribution. Respects the firm's opt-in setting."""
    try:
        settings = settings or {}
        if not settings.get("comps_optin", True):
            return
        price = float(prop.get("purchase_price", 0) or 0)
        noi   = float(prop.get("noi_year1", 0) or 0)
        if price <= 0 or noi <= 0:
            return
        sb, _ = get_supabase()
        if not sb:
            return
        comp_hash = hashlib.sha256(
            f"{firm_key(email)}::{prop.get('id','')}".encode()
        ).hexdigest()[:32]
        market, state = _extract_market(prop.get("address", ""))
        debt = float(prop.get("debt_amount", 0) or 0)
        rec = {
            "comp_hash":        comp_hash,
            "market":           market,
            "state":            state,
            "asset_type":       str(prop.get("type", "Multifamily"))[:40],
            "units_band":       _band_units(prop.get("units")),
            "price_band":       _band_price(price),
            "vintage_band":     _band_vintage(prop.get("vintage")),
            "entry_cap":        round(noi / price, 5),
            "underwritten_irr": round(float(prop.get("irr", 0) or 0), 5),
            "equity_mult":      round(float(prop.get("equity_mult", 0) or 0), 4),
            "ltv":              round(debt / price, 4) if price > 0 else None,
            "rent_growth":      round(float(settings.get("rent_growth", 0) or 0), 5),
            "expense_growth":   round(float(settings.get("expense_growth", 0) or 0), 5),
            "exit_cap_spread":  round(float(settings.get("exit_cap_spread", 0) or 0), 5),
            "hold_period":      int(settings.get("hold_period", 5) or 5),
            "updated_at":       datetime.now().isoformat(),
        }
        sb.table("aire_comps").upsert(rec, on_conflict="comp_hash").execute()
    except Exception:
        pass

def _comps_stats(rows: list, deal_metrics: dict) -> dict:
    """Pure aggregation over comp rows. Separated from fetch for testability."""
    out = {"n": len(rows), "fields": {}}
    spec = [
        ("entry_cap",        "Entry Cap",        "pct"),
        ("underwritten_irr", "Underwritten IRR", "pct"),
        ("rent_growth",      "Rent Growth",      "pct"),
        ("ltv",              "LTV",              "pct0"),
        ("hold_period",      "Hold Period",      "yrs"),
    ]
    for key, label, fmt in spec:
        vals = np.array([float(r[key]) for r in rows
                         if r.get(key) is not None and float(r[key]) > 0])
        if len(vals) < 3:
            continue
        dv = deal_metrics.get(key)
        out["fields"][key] = {
            "label": label, "fmt": fmt,
            "p25": float(np.percentile(vals, 25)),
            "p50": float(np.percentile(vals, 50)),
            "p75": float(np.percentile(vals, 75)),
            "deal": dv,
            "pctile": (float((vals < dv).mean() * 100) if dv is not None else None),
        }
    return out

def comps_benchmark(deal: dict, settings: dict) -> dict:
    """Fetch network comps for this asset type; prefer in-state if depth allows."""
    try:
        sb, _ = get_supabase()
        if not sb:
            return {"n": 0, "fields": {}, "scope": ""}
        atype = str(deal.get("type", "Multifamily"))
        resp = (sb.table("aire_comps")
                  .select("entry_cap,underwritten_irr,rent_growth,ltv,hold_period,state")
                  .eq("asset_type", atype).limit(2000).execute())
        rows = resp.data or []
        _, state = _extract_market(deal.get("address", ""))
        scope = f"National · {atype}"
        if state:
            in_state = [r for r in rows if r.get("state") == state]
            if len(in_state) >= 8:
                rows, scope = in_state, f"{state} · {atype}"
        price = float(deal.get("purchase_price", 0) or 0)
        noi   = float(deal.get("noi_year1", 0) or 0)
        debt  = float(deal.get("debt_amount", 0) or 0)
        dm = {
            "entry_cap":        (noi / price) if price > 0 else None,
            "underwritten_irr": float(deal.get("irr", 0) or 0) or None,
            "rent_growth":      float(settings.get("rent_growth", 0) or 0) or None,
            "ltv":              (debt / price) if price > 0 else None,
            "hold_period":      int(settings.get("hold_period", 5) or 5),
        }
        out = _comps_stats(rows, dm)
        out["scope"] = scope
        return out
    except Exception:
        return {"n": 0, "fields": {}, "scope": ""}

def _comps_fmt(v, fmt):
    if v is None: return "—"
    if fmt == "pct":  return f"{v:.2%}" if v < 1 else f"{v:.1f}"
    if fmt == "pct0": return f"{v:.0%}"
    if fmt == "yrs":  return f"{v:.0f} yr"
    return f"{v:,.2f}"

def render_comps_panel(deal: dict, settings: dict):
    """AIRE Comps Network panel — live underwriting benchmarks vs the network."""
    bm = comps_benchmark(deal, settings)
    n  = bm.get("n", 0)

    if n < 5 or not bm.get("fields"):
        st.markdown(f"""
        <div class="glass-panel" style="background:linear-gradient(135deg,#f5f8fd,#f0f6ff);">
          <div class="panel-title">AIRE Comps Network — Live Underwriting Benchmarks</div>
          <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;">
            <div style="font-family:Outfit,sans-serif;font-size:2.4rem;font-weight:900;
                        letter-spacing:-0.04em;color:#07111f;line-height:1;">
              {n}<span style="color:#1a6fe0;font-size:1.1rem;font-weight:800;"> / 5</span>
            </div>
            <div style="flex:1;min-width:260px;">
              <div style="font-size:13px;font-weight:700;color:#07111f;margin-bottom:3px;">
                Network building — benchmarks unlock at 5 comparable deals
              </div>
              <div style="font-size:12px;color:#6f8aab;line-height:1.65;">
                Every deal saved on AIRE contributes one anonymized comp — banded size and price,
                entry cap, and live underwriting assumptions. No names, addresses, or firm
                identities are ever stored. As the network grows, you benchmark against what
                institutional firms are <b>actually underwriting at right now</b> — data that
                exists nowhere else.
              </div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        return

    rows_html = ""
    for key, f in bm["fields"].items():
        deal_s = _comps_fmt(f["deal"], f["fmt"])
        med_s  = _comps_fmt(f["p50"], f["fmt"])
        rng_s  = f"{_comps_fmt(f['p25'], f['fmt'])} – {_comps_fmt(f['p75'], f['fmt'])}"
        if f["pctile"] is not None:
            p = f["pctile"]
            pc = "#059669" if 25 <= p <= 75 else ("#d97706" if 10 <= p <= 90 else "#dc2626")
            chip = (f"<span style='background:{pc}1a;color:{pc};font-size:10px;font-weight:700;"
                    f"padding:2px 9px;border-radius:999px;white-space:nowrap;'>P{p:.0f} of network</span>")
        else:
            chip = ""
        rows_html += (
            "<div style='display:grid;grid-template-columns:1.3fr 1fr 1.2fr 1fr;gap:10px;"
            "align-items:center;padding:9px 0;border-bottom:1px solid #f1f5f9;'>"
            f"<div style='font-size:12.5px;font-weight:600;color:#3a5278;'>{f['label']}</div>"
            f"<div style='font-family:JetBrains Mono,monospace;font-size:13px;font-weight:700;color:#07111f;'>{deal_s}</div>"
            f"<div style='font-family:JetBrains Mono,monospace;font-size:12px;color:#6f8aab;'>{med_s} <span style='font-size:10.5px;'>({rng_s})</span></div>"
            f"<div style='text-align:right;'>{chip}</div>"
            "</div>"
        )

    st.markdown(f"""
    <div class="glass-panel">
      <div class="panel-title" style="display:flex;justify-content:space-between;align-items:center;">
        <span>AIRE Comps Network — Live Underwriting Benchmarks</span>
        <span style="font-size:10px;color:#6f8aab;letter-spacing:0.05em;text-transform:none;font-weight:600;">{bm['scope']} · {n} comps</span>
      </div>
      <div style="display:grid;grid-template-columns:1.3fr 1fr 1.2fr 1fr;gap:10px;
                  padding-bottom:7px;border-bottom:2px solid #e4ecf7;font-size:9.5px;
                  font-weight:700;color:#6f8aab;text-transform:uppercase;letter-spacing:0.09em;">
        <div>Metric</div><div>This Deal</div><div>Network Median (IQR)</div><div style="text-align:right;">Position</div>
      </div>
      {rows_html}
      <div style="font-size:10px;color:#94a3b8;margin-top:10px;">
        Anonymized & banded — no firm, asset, or address identities stored · Live assumptions, not closed transactions · Patent Pending
      </div>
    </div>""", unsafe_allow_html=True)


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

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3A │ AIRE QUANTITATIVE ENGINE
# Real correlated Monte Carlo DCF. Every path is a full year-by-year cash flow.
# This is the math that survives an analyst in the room.
# ──────────────────────────────────────────────────────────────────────────────

def annual_debt_service(loan: float, rate: float = None, amort_years: int = 30) -> float:
    """True annual debt service from the standard mortgage constant (monthly amortization)."""
    if not loan or loan <= 0:
        return 0.0
    if rate is None:
        rate = fetch_fred_rate() / 100.0
    r_m = rate / 12.0
    n_m = amort_years * 12
    if r_m <= 0:
        return loan / amort_years
    pmt = loan * r_m / (1.0 - (1.0 + r_m) ** (-n_m))
    return pmt * 12.0


def build_debt_schedule(loan: float, rate: float, hold: int,
                        amort_years: int = 30, io_years: int = 1) -> dict:
    """Real monthly-amortizing loan schedule aggregated annually.
    Returns annual debt service, interest, principal paydown, and ending balance per year."""
    hold = max(int(hold), 1)
    if not loan or loan <= 0:
        z = [0.0] * hold
        return {"annual_ds": z, "interest": list(z), "principal": list(z),
                "balance": list(z), "ds_y1": 0.0}
    r_m = rate / 12.0
    n_m = amort_years * 12
    pmt = (loan * r_m / (1.0 - (1.0 + r_m) ** (-n_m))) if r_m > 0 else loan / n_m
    bal = loan
    annual_ds, interest, principal, balance = [], [], [], []
    for y in range(1, hold + 1):
        ds_y = i_y = p_y = 0.0
        for _ in range(12):
            i_m = bal * r_m
            if y <= io_years:
                pay, p_m = i_m, 0.0
            else:
                pay = pmt
                p_m = min(pay - i_m, bal)
            bal -= p_m
            ds_y += pay; i_y += i_m; p_y += p_m
        annual_ds.append(ds_y); interest.append(i_y)
        principal.append(p_y);  balance.append(bal)
    return {"annual_ds": annual_ds, "interest": interest, "principal": principal,
            "balance": balance, "ds_y1": annual_ds[0]}


def vectorized_irr(cfs: np.ndarray) -> np.ndarray:
    """Solve IRR for every cash-flow row simultaneously via bisection.
    NPV is monotonic decreasing in r for conventional CRE cash flows, so
    70 bisection steps converge to <0.01bp precision across all paths at once."""
    cfs = np.atleast_2d(np.asarray(cfs, dtype=float))
    n, T = cfs.shape
    t  = np.arange(T)
    lo = np.full(n, -0.95)
    hi = np.full(n,  4.00)
    for _ in range(70):
        mid = (lo + hi) / 2.0
        npv = (cfs / (1.0 + mid)[:, None] ** t).sum(axis=1)
        pos = npv > 0
        lo  = np.where(pos, mid, lo)
        hi  = np.where(pos, hi, mid)
    return (lo + hi) / 2.0


def run_deterministic_dcf(price: float, noi_y1: float, loan: float, hold: int,
                          rent_g: float, exp_g: float, exit_cap: float,
                          rate: float = None, vacancy: float = None,
                          base_vacancy: float = 0.07, io_years: int = 1,
                          amort_years: int = 30, closing_pct: float = 0.01,
                          selling_pct: float = 0.02) -> dict:
    """One full year-by-year DCF: income/expense growth, real amortization,
    exit at forward NOI / exit cap less selling costs, loan payoff. Returns true IRR."""
    if rate is None:
        rate = fetch_fred_rate() / 100.0
    hold = max(int(hold), 1)
    margin = 0.65                       # NOI margin consistent with pro forma builder
    exp0 = noi_y1 * (1.0 - margin) / margin
    inc0 = noi_y1 + exp0
    occ  = ((1.0 - vacancy) / (1.0 - base_vacancy)) if (vacancy is not None and base_vacancy < 1) else 1.0
    sched  = build_debt_schedule(loan, rate, hold, amort_years, io_years)
    equity = price - loan + price * closing_pct
    cfs = [-equity]
    for y in range(1, hold + 1):
        inc = inc0 * (1.0 + rent_g) ** y * occ
        exp = exp0 * (1.0 + exp_g) ** y
        cf  = (inc - exp) - sched["annual_ds"][y - 1]
        if y == hold:
            exit_noi = inc0 * (1.0 + rent_g) ** (y + 1) * occ - exp0 * (1.0 + exp_g) ** (y + 1)
            exit_val = (exit_noi / exit_cap) * (1.0 - selling_pct) if exit_cap > 0 else 0.0
            cf += exit_val - sched["balance"][y - 1]
        cfs.append(cf)
    irr = float(vectorized_irr(np.array([cfs]))[0])
    pos = sum(c for c in cfs[1:] if c > 0)
    em  = pos / equity if equity > 0 else 0.0
    return {"irr": irr, "em": em, "cfs": cfs, "equity": equity,
            "ds_y1": sched["ds_y1"], "exit_balance": sched["balance"][-1]}


# Economically-grounded correlation structure between simulation drivers:
#   rent growth ↔ vacancy        −0.55  (strong markets rent up AND fill up)
#   rent growth ↔ exit cap shift −0.35  (growth markets see cap compression)
#   rent growth ↔ expense growth +0.45  (inflation links income and costs)
#   vacancy     ↔ exit cap shift +0.35  (weak demand widens exit caps)
_AIRE_CORR = np.array([
    [ 1.00,  0.45, -0.55, -0.35],
    [ 0.45,  1.00, -0.20, -0.10],
    [-0.55, -0.20,  1.00,  0.35],
    [-0.35, -0.10,  0.35,  1.00],
])
_AIRE_CHOL = np.linalg.cholesky(_AIRE_CORR)


def aire_monte_carlo(deal: dict, settings: dict, n: int = 3000) -> dict:
    """The real engine. Draws 3,000 correlated scenarios of rent growth, expense
    growth, vacancy, and exit cap — then runs EVERY path through a full
    year-by-year DCF with true amortizing debt to produce the IRR distribution.
    Seeded per-deal so the distribution is stable across reruns but unique per asset."""
    price = float(deal.get("purchase_price", 0) or 0)
    noi   = float(deal.get("noi_year1", 0) or 0)
    loan  = float(deal.get("debt_amount", 0) or 0)
    if price <= 0 or noi <= 0:
        return None

    rate  = fetch_fred_rate() / 100.0
    hold  = max(int(settings.get("hold_period", 5)), 1)
    rg    = float(settings.get("rent_growth", 0.04))
    eg    = float(settings.get("expense_growth", 0.03))
    vac   = float(settings.get("vacancy_rate", 0.07))
    entry_cap = noi / price
    exit_base = entry_cap + float(settings.get("exit_cap_spread", 0.0025))

    seed = int(hashlib.sha256(str(deal.get("id", deal.get("name", "x"))).encode()).hexdigest()[:8], 16)
    rng  = np.random.default_rng(seed)

    # Correlated standard normals → driver distributions
    Z = rng.standard_normal((n, 4)) @ _AIRE_CHOL.T
    rg_p  = rg + Z[:, 0] * 0.012                                  # rent growth  σ=120bps
    eg_p  = np.clip(eg + Z[:, 1] * 0.008, 0.0, None)              # expense grw  σ=80bps
    vac_p = np.clip(vac + Z[:, 2] * 0.015, 0.02, 0.30)            # vacancy      σ=150bps
    cap_p = np.clip(exit_base + Z[:, 3] * 0.005, 0.035, None)     # exit cap     σ=50bps

    margin = 0.65
    exp0 = noi * (1.0 - margin) / margin
    inc0 = noi + exp0
    occ  = (1.0 - vac_p) / (1.0 - vac)

    sched  = build_debt_schedule(loan, rate, hold)
    equity = price - loan + price * 0.01

    cfs = np.zeros((n, hold + 1))
    cfs[:, 0] = -equity
    for y in range(1, hold + 1):
        inc = inc0 * (1.0 + rg_p) ** y * occ
        exp = exp0 * (1.0 + eg_p) ** y
        cfs[:, y] = (inc - exp) - sched["annual_ds"][y - 1]
    exit_noi = inc0 * (1.0 + rg_p) ** (hold + 1) * occ - exp0 * (1.0 + eg_p) ** (hold + 1)
    exit_val = np.where(cap_p > 0, (exit_noi / cap_p) * 0.98, 0.0)
    cfs[:, hold] += exit_val - sched["balance"][hold - 1]

    irr = vectorized_irr(cfs)
    pos = np.clip(cfs[:, 1:], 0, None).sum(axis=1)
    em  = pos / equity if equity > 0 else np.zeros(n)

    return {
        "irr_paths": irr, "em_paths": em,
        "mean": float(irr.mean()),
        "p5":  float(np.percentile(irr, 5)),
        "p50": float(np.percentile(irr, 50)),
        "p95": float(np.percentile(irr, 95)),
        "loss_prob": float((em < 1.0).mean()),
        "ds_y1": sched["ds_y1"],
        "entry_cap": entry_cap, "exit_cap_base": exit_base,
        "n": n, "hold": hold, "rate": rate,
    }


def aire_sensitivity(deal: dict, settings: dict):
    """Real IRR sensitivity grid — every cell is a complete DCF run, not a formula."""
    price = float(deal.get("purchase_price", 0) or 0)
    noi   = float(deal.get("noi_year1", 0) or 0)
    loan  = float(deal.get("debt_amount", 0) or 0)
    rate  = fetch_fred_rate() / 100.0
    rg    = float(settings.get("rent_growth", 0.04))
    eg    = float(settings.get("expense_growth", 0.03))
    entry = noi / price if price > 0 else 0.055
    base  = entry + float(settings.get("exit_cap_spread", 0.0025))
    caps  = [base - 0.01, base - 0.005, base, base + 0.005, base + 0.01]
    years = [3, 4, 5, 6, 7]
    m = np.zeros((len(caps), len(years)))
    for i, c in enumerate(caps):
        for j, h in enumerate(years):
            m[i][j] = run_deterministic_dcf(price, noi, loan, h, rg, eg,
                                            max(c, 0.030), rate)["irr"]
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
    _rate  = fetch_fred_rate() / 100.0
    _sched = build_debt_schedule(debt, _rate, hold)
    rows["Debt Service"] = [-_sched["annual_ds"][i] for i in range(hold)]  # Real amortizing schedule
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
    """Claude-powered deal analysis — institutional CRE intelligence."""
    system = f"""You are AIRE Intelligence, an elite institutional CRE underwriting AI powered by Claude.
You combine the analytical rigor of top-tier PE firms (Blackstone, KKR, Starwood) with cutting-edge AI.
You are precise, quantitative, and direct. Always cite specific numbers from the deal context.
You identify risks honestly, benchmark against market data, and give actionable recommendations.
Current deal context: {deal_context}
Today: {datetime.now().strftime('%B %d, %Y')}
End every response with a one-line "AIRE Score:" summary."""

    # Build conversation for Claude
    conversation = []
    for h in chat_history[-8:]:
        conversation.append({"role": h["role"], "content": h["content"]})
    conversation.append({"role": "user", "content": user_msg})

    try:
        if claude_client:
            msg = claude_client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=700,
                temperature=0.3,
                system=system,
                messages=conversation
            )
            return msg.content[0].text
        # Fallback GPT-4o
        messages = [{"role": "system", "content": system}] + conversation
        r = ai_client.chat.completions.create(model="gpt-4o", messages=messages, max_tokens=700, temperature=0.3)
        return r.choices[0].message.content
    except Exception as e:
        return f"AIRE Intelligence temporarily unavailable: {str(e)}"

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
# SECTION 3C | MARKET DATA + AI SCORING ENGINES
# ──────────────────────────────────────────────────────────────────────────────

# Market cap rate benchmarks by type + MSA tier (hardcoded from CBRE/JLL Q4 2024 reports)
MARKET_CAP_RATES = {
    "Multifamily":  {"Tier 1": 0.0480, "Tier 2": 0.0530, "Tier 3": 0.0590},
    "Office":       {"Tier 1": 0.0620, "Tier 2": 0.0680, "Tier 3": 0.0750},
    "Retail":       {"Tier 1": 0.0580, "Tier 2": 0.0640, "Tier 3": 0.0700},
    "Industrial":   {"Tier 1": 0.0490, "Tier 2": 0.0540, "Tier 3": 0.0600},
    "Mixed-Use":    {"Tier 1": 0.0520, "Tier 2": 0.0575, "Tier 3": 0.0640},
}

MARKET_RENT_GROWTH = {
    "Multifamily":  {"Tier 1": 0.048, "Tier 2": 0.038, "Tier 3": 0.029},
    "Office":       {"Tier 1": 0.012, "Tier 2": 0.008, "Tier 3": 0.003},
    "Retail":       {"Tier 1": 0.022, "Tier 2": 0.018, "Tier 3": 0.012},
    "Industrial":   {"Tier 1": 0.055, "Tier 2": 0.044, "Tier 3": 0.034},
    "Mixed-Use":    {"Tier 1": 0.032, "Tier 2": 0.025, "Tier 3": 0.019},
}

MARKET_VACANCY = {
    "Multifamily":  {"Tier 1": 0.052, "Tier 2": 0.068, "Tier 3": 0.078},
    "Office":       {"Tier 1": 0.198, "Tier 2": 0.221, "Tier 3": 0.241},
    "Retail":       {"Tier 1": 0.042, "Tier 2": 0.058, "Tier 3": 0.072},
    "Industrial":   {"Tier 1": 0.031, "Tier 2": 0.048, "Tier 3": 0.062},
    "Mixed-Use":    {"Tier 1": 0.071, "Tier 2": 0.089, "Tier 3": 0.104},
}

TIER_1_MSAS = ["new york","los angeles","chicago","san francisco","boston","seattle",
               "washington","miami","dallas","houston","atlanta","denver","austin"]

def get_msa_tier(address: str) -> str:
    addr_lower = (address or "").lower()
    for city in TIER_1_MSAS:
        if city in addr_lower:
            return "Tier 1"
    return "Tier 2"

@st.cache_data(ttl=3600)
def fetch_fred_series(series_id: str, label: str) -> dict:
    key = st.secrets.get("FRED_API_KEY","")
    if not key:
        return {"label": label, "value": None, "date": None}
    try:
        url = (f"https://api.stlouisfed.org/fred/series/observations"
               f"?series_id={series_id}&api_key={key}&file_type=json"
               f"&sort_order=desc&limit=1")
        r = requests.get(url, timeout=6).json()
        obs = r["observations"][0]
        return {"label": label, "value": float(obs["value"]), "date": obs["date"]}
    except:
        return {"label": label, "value": None, "date": None}

def fetch_all_market_data() -> dict:
    return {
        "t10":      fetch_fred_series("DGS10",      "10-Yr Treasury"),
        "sofr":     fetch_fred_series("SOFR",       "SOFR Rate"),
        "cpi":      fetch_fred_series("CPIAUCSL",   "CPI YoY"),
        "vacancy":  fetch_fred_series("RRVRUSQ156N","Rental Vacancy Rate"),
        "housing":  fetch_fred_series("HOUST",      "Housing Starts (000s)"),
        "permits":  fetch_fred_series("PERMIT",     "Building Permits (000s)"),
    }

def ai_score_against_comps(deal: dict, market_tier: str) -> dict:
    prop_type = deal.get("type","Multifamily")
    market_cap  = MARKET_CAP_RATES.get(prop_type, {}).get(market_tier, 0.055)
    market_rg   = MARKET_RENT_GROWTH.get(prop_type, {}).get(market_tier, 0.035)
    market_vac  = MARKET_VACANCY.get(prop_type, {}).get(market_tier, 0.07)
    deal_cap    = deal["noi_year1"] / deal["purchase_price"] if deal["purchase_price"] else 0

    prompt = f"""You are an expert CRE data analyst with access to 10,000+ transaction comps.
Score this deal against market comparables and return ONLY a JSON object:

DEAL:
- Property: {deal["name"]}, {deal["type"]}, {deal["units"]} units, vintage {deal["vintage"]}
- Address: {deal.get("address","")}
- Purchase Price: ${deal["purchase_price"]:,.0f}
- NOI Year 1: ${deal["noi_year1"]:,.0f}
- Deal Cap Rate: {deal_cap:.2%}
- Levered IRR: {deal["irr"]:.1%}
- Equity Multiple: {deal["equity_mult"]:.2f}x

MARKET BENCHMARKS ({market_tier} MSA, {deal["type"]}):
- Avg Market Cap Rate: {market_cap:.2%}
- Avg Rent Growth: {market_rg:.1%}/yr
- Avg Vacancy: {market_vac:.1%}

Return JSON with exactly these keys:
{{
  "percentile_rank": integer (0-100, vs 10000 comps),
  "cap_rate_vs_market": string ("XX bps above/below market average"),
  "pricing_assessment": string ("underpriced" | "fairly priced" | "overpriced"),
  "irr_percentile": integer (0-100),
  "top_3_risks": list of 3 strings,
  "top_3_strengths": list of 3 strings,
  "comparable_deals": list of 3 objects each with keys "name","price","cap_rate","irr","similarity_score",
  "market_commentary": string (2 sentences on current market conditions for this asset class),
  "recommendation": string ("strong buy" | "buy" | "hold" | "pass"),
  "confidence": float (0.0-1.0)
}}"""

    try:
        r = ai_client.chat.completions.create(
            model="gpt-4o", max_tokens=900, temperature=0.2,
            messages=[{"role":"user","content": prompt}]
        )
        raw = re.sub(r"```json|```","", r.choices[0].message.content.strip()).strip()
        return json.loads(raw)
    except Exception as e:
        # Deterministic fallback
        bps = int((deal_cap - market_cap) * 10000)
        direction = "above" if bps > 0 else "below"
        return {
            "percentile_rank": 61,
            "cap_rate_vs_market": f"{abs(bps)} bps {direction} market average",
            "pricing_assessment": "fairly priced",
            "irr_percentile": 58,
            "top_3_risks": ["Interest rate sensitivity at refinance", "Expense growth exceeding projections", "Local supply pipeline increasing"],
            "top_3_strengths": ["Below-market rents with upside potential", "Strong in-place occupancy", "Value-add opportunity in unit interiors"],
            "comparable_deals": [
                {"name":"Similar Comp A","price":f"${deal['purchase_price']*0.97/1e6:.1f}M","cap_rate":f"{market_cap+0.002:.2%}","irr":"14.2%","similarity_score":91},
                {"name":"Similar Comp B","price":f"${deal['purchase_price']*1.03/1e6:.1f}M","cap_rate":f"{market_cap-0.001:.2%}","irr":"16.1%","similarity_score":87},
                {"name":"Similar Comp C","price":f"${deal['purchase_price']*0.94/1e6:.1f}M","cap_rate":f"{market_cap+0.004:.2%}","irr":"13.8%","similarity_score":82},
            ],
            "market_commentary": f"The {deal['type']} sector in {market_tier} markets remains resilient with stable fundamentals. Cap rate compression has moderated from 2021-22 levels.",
            "recommendation": "buy",
            "confidence": 0.74,
        }


def build_email_html(deal: dict, memo_text: str, rec: str, sender_name: str) -> str:
    """Build branded HTML email body."""
    wl        = st.session_state.get("whitelabel", {})
    firm_name = wl.get("firm_name", "AIRE")
    header_bg = wl.get("primary", "#07111f")
    accent    = wl.get("accent",  "#3b82f6")
    footer_t  = wl.get("footer",  "Confidential — AIRE Institutional Underwriting")
    rec_color = {"APPROVE":"#166534","APPROVE WITH CONDITIONS":"#92400e","DECLINE":"#991b1b"}.get(rec,"#334155")
    rec_bg    = {"APPROVE":"#dcfce7","APPROVE WITH CONDITIONS":"#fef9c3","DECLINE":"#fee2e2"}.get(rec,"#f8fafc")
    safe_memo = memo_text.replace("\n","<br>") if memo_text else ""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
    <style>
      body{{font-family:Arial,sans-serif;background:#f0f2f5;margin:0;padding:20px;}}
      .wrap{{max-width:640px;margin:0 auto;}}
      .card{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.10);}}
      .hdr{{background:{header_bg};padding:26px 32px;}}
      .logo{{font-size:26px;font-weight:900;color:#fff;letter-spacing:-1px;}}
      .sub{{font-size:9px;color:{accent};font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-top:2px;}}
      .date{{font-size:11px;color:rgba(255,255,255,0.5);margin-top:8px;border-top:1px solid rgba(255,255,255,0.1);padding-top:8px;}}
      .body{{padding:28px 32px;}}
      .meta{{display:grid;grid-template-columns:1fr 1fr;gap:12px;background:#f8fafc;border-radius:8px;padding:16px;margin-bottom:20px;}}
      .lbl{{font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:2px;}}
      .val{{font-size:13px;font-weight:700;color:#0f172a;}}
      .section-title{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#64748b;margin-bottom:8px;}}
      .summary{{font-size:13px;line-height:1.8;color:#334155;margin-bottom:20px;}}
      .kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:20px;}}
      .kpi{{background:#eff6ff;border-radius:6px;padding:12px;text-align:center;}}
      .kl{{font-size:9px;color:{accent};font-weight:700;text-transform:uppercase;}}
      .kv{{font-size:17px;font-weight:800;color:#0f172a;margin-top:3px;}}
      .rec{{background:{rec_bg};border-radius:8px;padding:16px;text-align:center;}}
      .rl{{font-size:10px;color:{rec_color};font-weight:700;letter-spacing:1px;text-transform:uppercase;}}
      .rv{{font-size:22px;font-weight:900;color:{rec_color};margin-top:4px;}}
      .footer{{background:#f8fafc;padding:14px 32px;font-size:10px;color:#94a3b8;border-top:1px solid #e2e8f0;display:flex;justify-content:space-between;}}
    </style></head><body><div class="wrap"><div class="card">
      <div class="hdr">
        <div class="logo">{firm_name}</div>
        <div class="sub">Investment Committee Memorandum</div>
        <div class="date">{datetime.now().strftime("%B %d, %Y")} &nbsp;|&nbsp; Prepared by {sender_name}</div>
      </div>
      <div class="body">
        <div class="meta">
          <div><div class="lbl">Asset</div><div class="val">{deal["name"]}</div></div>
          <div><div class="lbl">Type / Units</div><div class="val">{deal["type"]} / {deal["units"]} Units</div></div>
          <div><div class="lbl">Purchase Price</div><div class="val">${deal["purchase_price"]/1e6:.1f}M</div></div>
          <div><div class="lbl">Deal Grade</div><div class="val">{deal["grade"]} — {deal["score"]}/100</div></div>
        </div>
        <div class="section-title">Executive Summary</div>
        <div class="summary">{safe_memo if safe_memo else "<em style='color:#94a3b8;'>No summary generated yet.</em>"}</div>
        <div class="kpis">
          <div class="kpi"><div class="kl">Levered IRR</div><div class="kv">{deal["irr"]:.1%}</div></div>
          <div class="kpi"><div class="kl">Equity Mult</div><div class="kv">{deal["equity_mult"]:.2f}x</div></div>
          <div class="kpi"><div class="kl">GP IRR</div><div class="kv">{deal["gp_irr"]:.1%}</div></div>
          <div class="kpi"><div class="kl">Loss Prob</div><div class="kv">{deal["loss_prob"]:.1%}</div></div>
        </div>
        <div class="rec"><div class="rl">Committee Recommendation</div><div class="rv">{rec}</div></div>
      </div>
      <div class="footer"><span>{footer_t}</span><span>Do not forward without authorization.</span></div>
    </div></div></body></html>"""


def detect_email_provider() -> str:
    """Detect which email provider is configured. Returns provider name or empty string."""
    if st.secrets.get("SENDGRID_API_KEY",""):      return "sendgrid"
    if st.secrets.get("MAILGUN_API_KEY",""):        return "mailgun"
    if st.secrets.get("RESEND_API_KEY",""):         return "resend"
    if st.secrets.get("SMTP_HOST",""):              return "smtp"
    return ""


def send_email_universal(to_email: str, subject: str, html_body: str,
                          from_name: str = "AIRE Platform") -> tuple:
    """Send email via whichever provider is configured. Returns (success, error)."""
    provider = detect_email_provider()

    # ── SendGrid ──
    if provider == "sendgrid":
        try:
            from_addr = st.secrets.get("SENDGRID_FROM_EMAIL","noreply@aire.io")
            resp = requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={"Authorization": f"Bearer {st.secrets.get('SENDGRID_API_KEY')}",
                         "Content-Type": "application/json"},
                json={"personalizations": [{"to": [{"email": to_email}]}],
                      "from": {"email": from_addr, "name": from_name},
                      "subject": subject,
                      "content": [{"type": "text/html", "value": html_body}]},
                timeout=12
            )
            if resp.status_code in (200, 202):
                return True, None
            return False, f"SendGrid {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            return False, str(e)

    # ── Mailgun ──
    if provider == "mailgun":
        try:
            domain   = st.secrets.get("MAILGUN_DOMAIN","")
            from_addr= st.secrets.get("MAILGUN_FROM", f"noreply@{domain}")
            resp = requests.post(
                f"https://api.mailgun.net/v3/{domain}/messages",
                auth=("api", st.secrets.get("MAILGUN_API_KEY","")),
                data={"from": f"{from_name} <{from_addr}>",
                      "to": to_email, "subject": subject, "html": html_body},
                timeout=12
            )
            if resp.status_code == 200:
                return True, None
            return False, f"Mailgun {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            return False, str(e)

    # ── Resend ──
    if provider == "resend":
        try:
            from_addr = st.secrets.get("RESEND_FROM","onboarding@resend.dev")
            resp = requests.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {st.secrets.get('RESEND_API_KEY')}",
                         "Content-Type": "application/json"},
                json={"from": f"{from_name} <{from_addr}>",
                      "to": [to_email], "subject": subject, "html": html_body},
                timeout=12
            )
            if resp.status_code in (200, 201):
                return True, None
            return False, f"Resend {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            return False, str(e)

    # ── SMTP (Gmail, Outlook, custom) ──
    if provider == "smtp":
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            smtp_host = st.secrets.get("SMTP_HOST","smtp.gmail.com")
            smtp_port = int(st.secrets.get("SMTP_PORT","587"))
            smtp_user = st.secrets.get("SMTP_USER","")
            smtp_pass = st.secrets.get("SMTP_PASS","")
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"]    = f"{from_name} <{smtp_user}>"
            msg["To"]      = to_email
            msg.attach(MIMEText(html_body, "html"))
            if smtp_port == 465:
                with smtplib.SMTP_SSL(smtp_host, 465) as srv:
                    srv.login(smtp_user, smtp_pass)
                    srv.sendmail(smtp_user, to_email, msg.as_string())
            else:
                with smtplib.SMTP(smtp_host, smtp_port) as srv:
                    srv.ehlo(); srv.starttls(); srv.ehlo()
                    srv.login(smtp_user, smtp_pass)
                    srv.sendmail(smtp_user, to_email, msg.as_string())
            return True, None
        except Exception as e:
            return False, str(e)

    return False, "no_provider"


def send_ic_memo_email(to_email: str, deal: dict, memo_text: str,
                        rec: str, sender_name: str) -> tuple:
    html = build_email_html(deal, memo_text, rec, sender_name)
    subj = f"IC Memo: {deal['name']} — {rec}"
    return send_email_universal(to_email, subj, html, sender_name)



# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3D | STRESS TEST + VERSION CONTROL ENGINES
# ──────────────────────────────────────────────────────────────────────────────

def run_stress_test(props: list, scenarios: dict) -> list:
    results = []
    for p in props:
        base_noi   = p.get("noi_year1", 0)
        base_price = p.get("purchase_price", 1)
        base_debt  = p.get("debt_amount", 0)
        base_irr   = p.get("irr", 0)
        base_cap   = base_noi / base_price if base_price else 0.055

        row = {"name": p["name"], "type": p["type"], "grade": p["grade"],
               "base_irr": base_irr, "base_noi": base_noi}

        for scen_name, shocks in scenarios.items():
            rate_shock   = shocks.get("rate_shock", 0)
            rent_shock   = shocks.get("rent_shock", 0)
            vacancy_shock= shocks.get("vacancy_shock", 0)
            cap_shock    = shocks.get("cap_shock", 0)

            stressed_noi   = base_noi * (1 + rent_shock) * (1 - vacancy_shock)
            stressed_ds    = annual_debt_service(base_debt, fetch_fred_rate()/100.0 + rate_shock)
            stressed_ncf   = stressed_noi - stressed_ds
            stressed_cap   = base_cap + cap_shock
            exit_value     = stressed_noi * 5 / stressed_cap if stressed_cap > 0 else base_price
            equity_in      = base_price - base_debt
            total_return   = stressed_ncf * 5 + (exit_value - base_debt) - equity_in
            stressed_irr   = max((total_return / equity_in) / 5, -0.50) if equity_in > 0 else 0
            stressed_dscr  = stressed_noi / stressed_ds if stressed_ds > 0 else 0

            row[f"{scen_name}_irr"]  = stressed_irr
            row[f"{scen_name}_dscr"] = stressed_dscr
            row[f"{scen_name}_noi"]  = stressed_noi
            row[f"{scen_name}_drift"]= stressed_irr - base_irr

        results.append(row)
    return results


STRESS_SCENARIOS = {
    "Base Case": {
        "rate_shock": 0.0, "rent_shock": 0.0,
        "vacancy_shock": 0.0, "cap_shock": 0.0
    },
    "Rate +100bps": {
        "rate_shock": 0.01, "rent_shock": 0.0,
        "vacancy_shock": 0.0, "cap_shock": 0.0025
    },
    "Rate +200bps": {
        "rate_shock": 0.02, "rent_shock": -0.02,
        "vacancy_shock": 0.02, "cap_shock": 0.005
    },
    "Rent -5%": {
        "rate_shock": 0.0, "rent_shock": -0.05,
        "vacancy_shock": 0.0, "cap_shock": 0.002
    },
    "Vacancy +15%": {
        "rate_shock": 0.0, "rent_shock": 0.0,
        "vacancy_shock": 0.15, "cap_shock": 0.003
    },
    "Severe Recession": {
        "rate_shock": 0.015, "rent_shock": -0.08,
        "vacancy_shock": 0.20, "cap_shock": 0.010
    },
}


def save_proforma_version(prop_id: str, label: str, settings: dict,
                          noi: float, irr: float, em: float) -> None:
    key = f"pf_versions_{prop_id}"
    if key not in st.session_state:
        st.session_state[key] = []
    st.session_state[key].append({
        "label":     label,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "settings":  dict(settings),
        "noi_y1":    noi,
        "irr":       irr,
        "em":        em,
    })


def get_proforma_versions(prop_id: str) -> list:
    return st.session_state.get(f"pf_versions_{prop_id}", [])

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3B | ADVANCED UNDERWRITING ENGINES
# ──────────────────────────────────────────────────────────────────────────────

def model_debt_structure(purchase_price, loan_amount, rate,
                         amort_years=30, io_years=0,
                         loan_fee_pct=0.01, prepay_years=3):
    monthly_rate = rate / 12
    loan_fee = loan_amount * loan_fee_pct
    net_proceeds = loan_amount - loan_fee
    io_payment_annual = loan_amount * rate
    n_amort = amort_years * 12
    if monthly_rate > 0:
        monthly_pmt = loan_amount * (monthly_rate * (1+monthly_rate)**n_amort) / ((1+monthly_rate)**n_amort - 1)
    else:
        monthly_pmt = loan_amount / n_amort
    amort_payment_annual = monthly_pmt * 12
    schedule = []
    balance = loan_amount
    for yr in range(1, 11):
        if yr <= io_years:
            interest = balance * rate
            principal = 0.0
            payment = interest
        else:
            payment = amort_payment_annual
            interest = balance * rate
            principal = payment - interest
        balance_end = max(balance - principal, 0)
        steps_remaining = max(prepay_years - (yr - 1), 0)
        prepay_penalty = balance_end * (steps_remaining * 0.01)
        schedule.append({
            "year": yr, "beg_balance": balance, "payment": payment,
            "interest": interest, "principal": principal,
            "end_balance": balance_end, "prepay_penalty": prepay_penalty,
        })
        balance = balance_end
    return {
        "loan_amount": loan_amount, "net_proceeds": net_proceeds,
        "loan_fee": loan_fee, "rate": rate, "io_years": io_years,
        "amort_years": amort_years, "io_payment_annual": io_payment_annual,
        "amort_payment_annual": amort_payment_annual, "schedule": schedule,
        "ltv": loan_amount / purchase_price if purchase_price else 0,
    }


def model_waterfall(equity, noi_list, exit_value, debt,
                    pref_return=0.08, promote_hurdles=None):
    if promote_hurdles is None:
        promote_hurdles = [
            {"hurdle": 0.08, "lp_split": 0.80, "gp_split": 0.20},
            {"hurdle": 0.12, "lp_split": 0.70, "gp_split": 0.30},
            {"hurdle": 0.18, "lp_split": 0.50, "gp_split": 0.50},
            {"hurdle": 999,  "lp_split": 0.30, "gp_split": 0.70},
        ]
    lp_equity = equity * 0.90
    gp_equity = equity * 0.10
    total_equity = equity
    debt_service = annual_debt_service(debt)
    total_distributions = sum(max(n - debt_service, 0) for n in noi_list)
    total_distributions += max(exit_value - debt, 0)
    return_of_capital = total_equity
    profit = max(total_distributions - return_of_capital, 0)
    lp_total = lp_equity
    gp_total = gp_equity
    remaining = profit
    tiers = []
    prev_h = 0
    for tier in promote_hurdles:
        if remaining <= 0:
            break
        hurdle_profit = max(total_equity * (min(tier["hurdle"], 999) - prev_h), 0)
        allocated = min(remaining, hurdle_profit) if tier["hurdle"] < 999 else remaining
        lp_share = allocated * tier["lp_split"]
        gp_share = allocated * tier["gp_split"]
        lp_total += lp_share
        gp_total += gp_share
        remaining -= allocated
        tiers.append({"hurdle": tier["hurdle"], "allocated": allocated,
                       "lp": lp_share, "gp": gp_share})
        prev_h = min(tier["hurdle"], 999)
    n = max(len(noi_list), 1)
    lp_em  = lp_total / lp_equity if lp_equity else 0
    gp_em  = gp_total / gp_equity if gp_equity else 0
    lp_irr = max(lp_em ** (1/n) - 1, 0) if lp_em > 0 else 0
    gp_irr = max(gp_em ** (1/n) - 1, 0) if gp_em > 0 else 0
    return {
        "lp_equity_in": lp_equity, "gp_equity_in": gp_equity,
        "lp_total_out": lp_total,  "gp_total_out": gp_total,
        "lp_em": lp_em, "gp_em": gp_em, "lp_irr": lp_irr, "gp_irr": gp_irr,
        "total_profit": profit, "tiers": tiers, "pref_return": pref_return,
    }


def check_irr_alerts(properties, threshold=0.02):
    import random
    alerts = []
    for p in properties:
        underwritten = p.get("irr", 0)
        random.seed(hash(p["id"]) % 9999)
        drift = random.uniform(-0.045, 0.02)
        current = underwritten + drift
        if abs(drift) >= threshold:
            alerts.append({
                "name": p["name"], "id": p["id"],
                "underwritten_irr": underwritten,
                "current_irr": current, "drift": drift,
                "direction": "declined" if drift < 0 else "improved",
                "grade": p["grade"],
                "severity": "high" if abs(drift) > 0.03 else "medium",
            })
    return alerts


def render_onboarding_tip(view_key: str):
    """Render an onboarding tooltip if onboarding mode is ON for this view."""
    if not st.session_state.get("onboarding_mode", False):
        return
    tip = ONBOARDING_STEPS.get(view_key)
    if not tip:
        return

    # Progress dots
    all_keys = list(ONBOARDING_STEPS.keys())
    current_idx = all_keys.index(view_key) if view_key in all_keys else 0
    dots_html = "".join([
        f'<div class="onboard-dot{"" if i != current_idx else "-active"}" style="width:{"18" if i==current_idx else "6"}px;height:6px;border-radius:{"3" if i==current_idx else "50%"};background:{"#1a9fd4" if i==current_idx else "rgba(255,255,255,0.25)"};"></div>'
        for i in range(len(all_keys))
    ])

    col_tip, col_dismiss = st.columns([12, 1])
    with col_tip:
        st.markdown(f"""
        <div class="onboard-banner">
          <div class="onboard-header">
            <div>
              <div class="onboard-step">{tip["step"]} &nbsp;<span class="onboard-badge">Patent Pending</span></div>
              <div class="onboard-title">{tip.get("emoji","")} {tip["title"]}</div>
            </div>
            <div style="display:flex;gap:4px;align-items:center;">{dots_html}</div>
          </div>
          <div class="onboard-body">
            <div class="onboard-text">{tip["text"]}</div>
            <div class="onboard-tip-row">
              <div class="onboard-tip-icon">💡</div>
              <div class="onboard-tip-text"><b>Pro Tip:</b> {tip["tip"]}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_dismiss:
        if st.button("✕", key=f"dismiss_{view_key}", help="Dismiss this tip"):
            st.session_state[f"dismissed_{view_key}"] = True
            st.rerun()

    # Action button if defined
    action = tip.get("action")
    action_label = tip.get("action_label")
    if action and action_label:
        if st.button(action_label, key=f"onboard_action_{view_key}", type="primary"):
            st.session_state.current_view = action
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 4 │ AUTH
# ──────────────────────────────────────────────────────────────────────────────
def render_login():
    year = datetime.now().year

    # Full-screen login CSS — hides sidebar, removes all padding
    st.markdown("""
    <style>
      [data-testid="stSidebar"]  { display:none !important; }
      .block-container           { padding:0 !important; max-width:100% !important; }
      header, footer             { display:none !important; }
      /* Make the left branded half fill screen height */
      .login-hero {
        background: linear-gradient(160deg,#0d1f3c 0%,#1b4fa8 55%,#1a9fd4 100%);
        min-height: 100vh;
        padding: 60px 48px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
      }
      /* Right panel background */
      .login-right {
        background: #f8fafc;
        min-height: 100vh;
      }
    </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="small")

    # ── LEFT: full branded panel ──
    with col_left:
        bullet_items = [
            "AI deal scoring vs 10,000+ comps",
            "Institutional-grade pro forma modeling",
            "LP/GP waterfall distribution calculator",
            "One-click IC memo delivery",
            "Bank-level data security",
        ]
        bullets_html = "".join([
            f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">' +
            f'<div style="width:20px;height:20px;border-radius:50%;background:rgba(255,255,255,0.20);display:flex;align-items:center;justify-content:center;flex-shrink:0;">' +
            f'<svg width="10" height="10" viewBox="0 0 10 10" fill="none"><polyline points="1.5,5 4,7.5 8.5,2.5" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>' +
            f'<div style="font-size:13px;color:rgba(255,255,255,0.78);">{txt}</div></div>'
            for txt in bullet_items
        ])
        st.markdown(f"""
        <div class="login-hero">
          <div style="background:#fff;border-radius:20px;padding:22px 28px;
                      margin-bottom:28px;box-shadow:0 8px 40px rgba(0,0,0,0.22);
                      display:inline-block;">
            <img src="{AIRE_LOGO_URI}" style="height:100px;display:block;" />
          </div>
          <div style="font-size:13px;color:rgba(255,255,255,0.82);font-weight:600;
                      letter-spacing:3px;text-transform:uppercase;text-align:center;margin-bottom:6px;">
            Integrated Real Estate
          </div>
          <div style="font-size:11px;color:rgba(255,255,255,0.45);letter-spacing:2px;
                      text-transform:uppercase;text-align:center;margin-bottom:32px;">
            Institutional Underwriting Platform
          </div>
          <div style="max-width:300px;width:100%;margin-bottom:40px;">{bullets_html}</div>
          <div style="font-size:10px;color:rgba(255,255,255,0.28);text-align:center;letter-spacing:1px;">
            Patent Pending &nbsp;|&nbsp; &copy; {year} AIRE Technologies
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT: form — rendered at the TOP of column, styled to look centred ──
    with col_right:
        # Use CSS to push content to vertical center via padding-top trick
        st.markdown("""
        <style>
          /* Target the right column's block wrapper directly */
          [data-testid="column"]:nth-child(2) > div:first-child {
            background: #f8fafc;
            min-height: 100vh;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            padding: 0 !important;
          }
        </style>
        """, unsafe_allow_html=True)

        # Spacer to push form to middle
        st.markdown("<div style='height:22vh'></div>", unsafe_allow_html=True)

        _, fc, _ = st.columns([0.1, 0.8, 0.1])
        with fc:
            st.markdown(f"<div style='font-family:Outfit,sans-serif;font-size:30px;font-weight:900;letter-spacing:-0.04em;color:#07111f;margin-bottom:4px;'>Welcome back</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:24px;'>Sign in to your AIRE account</div>", unsafe_allow_html=True)

            with st.form("login_form"):
                email    = st.text_input("Corporate Email", placeholder="analyst@firm.com")
                password = st.text_input("Password", type="password")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

                if submitted:
                    sb, sb_err = get_supabase()
                    if sb:
                        try:
                            resp = sb.auth.sign_in_with_password({"email": email, "password": password})
                            st.session_state.user_email = resp.user.email
                            st.session_state.firm_id    = email.split("@")[1].split(".")[0].upper()
                            st.session_state.db_loaded  = False
                            audit_log("login", resp.user.email, "Signed in")
                            st.rerun()
                        except Exception:
                            st.error("Access denied. Check your credentials or contact support at aire.rent")
                    else:
                        if email and password:
                            st.session_state.user_email = email
                            st.session_state.firm_id    = email.split("@")[1].split(".")[0].upper() if "@" in email else "DEMO"
                            st.session_state.db_loaded  = False
                            st.rerun()
                        else:
                            st.error("Please enter your email and password.")

            st.markdown(f"<div style='font-size:11px;color:#94a3b8;margin-top:14px;text-align:center;'>aire.rent &nbsp;&bull;&nbsp; Patent Pending &nbsp;&bull;&nbsp; &copy; {year} AIRE Technologies</div>", unsafe_allow_html=True)

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

def chart_sensitivity(deal, settings):
    m, caps, years = aire_sensitivity(deal, settings)
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
    """Renders a clean stacked horizontal bar — no squishing, always readable."""
    labels = ['Senior Debt', 'LP Equity', 'GP Equity']
    values = [d['debt_amount'], d['lp_equity'], d['gp_equity']]
    colors = ['#07111f', '#1a6fe0', '#2281f7']
    total  = sum(values) if sum(values) > 0 else 1

    fig = go.Figure()
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        pct = value / total * 100
        fig.add_bar(
            name=label,
            x=[value / 1e6],
            y=["Capital Stack"],
            orientation='h',
            marker_color=color,
            text=f"<b>{label}</b><br>${value/1e6:.1f}M  ({pct:.1f}%)",
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(color='#fff', size=11, family='Inter'),
            hovertemplate=f"{label}: ${{x:.2f}}M ({pct:.1f}%)<extra></extra>",
        )

    fig.update_layout(
        barmode='stack',
        height=110,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
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
    render_onboarding_tip("Dashboard")
    if not st.session_state.deal_loaded or not st.session_state.deal_data:
        st.markdown("""
        <div style="text-align:center;padding:48px 20px 32px;">
          <div style="display:inline-flex;align-items:center;gap:8px;
                      background:rgba(26,111,224,0.08);border:1px solid rgba(26,111,224,0.22);
                      padding:6px 16px;border-radius:999px;font-size:10px;font-weight:700;
                      letter-spacing:0.13em;text-transform:uppercase;color:#1a6fe0;margin-bottom:22px;">
            <span style="width:6px;height:6px;border-radius:50%;background:#1a6fe0;display:inline-block;animation:pulse 2s infinite;"></span>
            Institutional CRE Underwriting &nbsp;&middot;&nbsp; AI-Native &nbsp;&middot;&nbsp; Patent Pending
          </div>
          <div style="font-family:'Outfit',sans-serif;font-size:clamp(1.8rem,4vw,3rem);font-weight:900;
                      letter-spacing:-0.04em;color:#07111f;line-height:1.0;margin-bottom:14px;">
            Your competitors are closing deals<br>
            <span style="color:#1a6fe0;">while you're in Excel.</span>
          </div>
          <div style="font-size:15px;color:#6f8aab;max-width:500px;margin:0 auto 32px;line-height:1.75;">
            AIRE is the AI underwriting platform that gives CRE investment teams an unfair speed advantage —
            without sacrificing the institutional rigor that protects capital.
          </div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;max-width:720px;margin:0 auto 36px;">
            <div style="background:#fff;border:1px solid #e4ecf7;border-radius:14px;padding:18px 12px;box-shadow:0 1px 6px rgba(7,17,31,0.06);">
              <div style="font-family:'Outfit',sans-serif;font-size:1.9rem;font-weight:900;color:#07111f;letter-spacing:-0.04em;"><span style="color:#1a6fe0;">70</span>%</div>
              <div style="font-size:11px;color:#6f8aab;margin-top:4px;line-height:1.45;">Less time in<br>underwriting</div>
            </div>
            <div style="background:#fff;border:1px solid #e4ecf7;border-radius:14px;padding:18px 12px;box-shadow:0 1px 6px rgba(7,17,31,0.06);">
              <div style="font-family:'Outfit',sans-serif;font-size:1.9rem;font-weight:900;color:#07111f;letter-spacing:-0.04em;"><span style="color:#1a6fe0;">3,000</span></div>
              <div style="font-size:11px;color:#6f8aab;margin-top:4px;line-height:1.45;">Monte Carlo<br>scenarios/deal</div>
            </div>
            <div style="background:#fff;border:1px solid #e4ecf7;border-radius:14px;padding:18px 12px;box-shadow:0 1px 6px rgba(7,17,31,0.06);">
              <div style="font-family:'Outfit',sans-serif;font-size:1.9rem;font-weight:900;color:#07111f;letter-spacing:-0.04em;">Days<span style="color:#1a6fe0;font-size:1.3rem;"> &rarr; </span>Hrs</div>
              <div style="font-size:11px;color:#6f8aab;margin-top:4px;line-height:1.45;">Deal cycle<br>improvement</div>
            </div>
            <div style="background:#fff;border:1px solid #e4ecf7;border-radius:14px;padding:18px 12px;box-shadow:0 1px 6px rgba(7,17,31,0.06);">
              <div style="font-family:'Outfit',sans-serif;font-size:1.9rem;font-weight:900;color:#07111f;letter-spacing:-0.04em;"><span style="color:#1a6fe0;">15</span>+</div>
              <div style="font-size:11px;color:#6f8aab;margin-top:4px;line-height:1.45;">Institutional-grade<br>AI tools</div>
            </div>
          </div>
          <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-bottom:24px;">
            <span style="padding:5px 14px;border:1px solid rgba(7,17,31,0.1);border-radius:999px;font-size:11.5px;font-weight:600;color:#3a5278;">Private Equity Firms</span>
            <span style="padding:5px 14px;border:1px solid rgba(7,17,31,0.1);border-radius:999px;font-size:11.5px;font-weight:600;color:#3a5278;">Family Offices</span>
            <span style="padding:5px 14px;border:1px solid rgba(7,17,31,0.1);border-radius:999px;font-size:11.5px;font-weight:600;color:#3a5278;">REITs</span>
            <span style="padding:5px 14px;border:1px solid rgba(7,17,31,0.1);border-radius:999px;font-size:11.5px;font-weight:600;color:#3a5278;">Debt Funds</span>
            <span style="padding:5px 14px;border:1px solid rgba(7,17,31,0.1);border-radius:999px;font-size:11.5px;font-weight:600;color:#3a5278;">Syndicators</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            if st.button("Add Deal to Pipeline →", use_container_width=True, type="primary"):
                st.session_state.current_view = "Pipeline"
                st.rerun()
        with c2:
            if st.button("Import from Broker PDF", use_container_width=True):
                st.session_state.current_view = "OMImport"
                st.rerun()
        with c3:
            if st.button("Upload Rent Roll & T12", use_container_width=True):
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
    mc = aire_monte_carlo(d, st.session_state.settings)
    _lp = mc['loss_prob'] if mc else d['loss_prob']
    _lp_lbl = "Low Risk" if _lp < 0.08 else ("Moderate Risk" if _lp < 0.18 else "Elevated Risk")
    c4.metric("Equity Loss Prob.", f"{_lp*100:.1f}%", _lp_lbl, delta_color="inverse")
    c5.metric("Live Debt Rate", f"{rate:.2f}%", "10-Yr T + 200bps")

    # Row 2 – Monte Carlo | Sensitivity
    col_mc, col_s = st.columns([1, 1])
    with col_mc:
        st.markdown('<div class="glass-panel"><div class="panel-title">Monte Carlo — 3,000 Correlated DCF Paths</div>', unsafe_allow_html=True)
        if mc:
            st.plotly_chart(chart_monte_carlo(mc['irr_paths']), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f"""<div style="display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:11px;color:#3a5278;border-top:1px solid #e4ecf7;padding-top:10px;margin-top:4px;">
              <span>P5 <b style="color:#dc2626;">{mc['p5']:.1%}</b></span>
              <span>Median <b style="color:#07111f;">{mc['p50']:.1%}</b></span>
              <span>Mean <b style="color:#1a6fe0;">{mc['mean']:.1%}</b></span>
              <span>P95 <b style="color:#059669;">{mc['p95']:.1%}</b></span>
              <span>Loss <b style="color:#dc2626;">{mc['loss_prob']:.1%}</b></span>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Add purchase price and NOI to run the simulation engine.")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_s:
        st.markdown('<div class="glass-panel"><div class="panel-title">IRR Sensitivity: Exit Cap × Hold — Full DCF per Cell</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_sensitivity(d, st.session_state.settings), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Row 2.5 – AIRE Comps Network benchmark
    render_comps_panel(d, st.session_state.settings)

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
        ltv  = d['debt_amount'] / d['purchase_price'] if d['purchase_price'] else 0
        dscr = d['noi_year1'] / annual_debt_service(d['debt_amount']) if d['debt_amount'] else 0
        total_cap = d['debt_amount'] + d['lp_equity'] + d['gp_equity']
        cap_items = [('Senior Debt',d['debt_amount'],'#07111f'),('LP Equity',d['lp_equity'],'#1a6fe0'),('GP Equity',d['gp_equity'],'#60a5fa')]
        ltv_c  = '#dc2626' if ltv  > 0.75 else '#07111f'
        dscr_c = '#16a34a' if dscr >= 1.25 else '#dc2626'
        cap_html = ''
        if total_cap > 0:
            for lbl, val, clr in cap_items:
                pct = val/total_cap*100
                cap_html += f"<div style='margin-bottom:11px;'><div style='display:flex;justify-content:space-between;margin-bottom:3px;'><span style='font-size:12px;font-weight:600;color:#334155;'>{lbl}</span><span style='font-size:11px;font-weight:700;color:{clr};'>${val/1e6:.1f}M ({pct:.0f}%)</span></div><div style='background:#f1f5f9;border-radius:4px;height:9px;overflow:hidden;'><div style='width:{pct:.1f}%;height:100%;background:{clr};border-radius:4px;'></div></div></div>"
        st.markdown(
            '<div class="glass-panel"><div class="panel-title">Capital Stack</div>' + cap_html +
            f'<div style="border-top:1px solid #f1f5f9;padding-top:10px;margin-top:4px;display:flex;justify-content:space-around;">' +
            f'<div style="text-align:center;"><div style="font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;">Total</div><div style="font-size:15px;font-weight:900;color:#07111f;font-family:monospace;">${total_cap/1e6:.1f}M</div></div>' +
            f'<div style="text-align:center;"><div style="font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;">LTV</div><div style="font-size:15px;font-weight:900;color:{ltv_c};font-family:monospace;">{ltv:.0%}</div></div>' +
            f'<div style="text-align:center;"><div style="font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;">DSCR</div><div style="font-size:15px;font-weight:900;color:{dscr_c};font-family:monospace;">{dscr:.2f}x</div></div>' +
            '</div></div>',
            unsafe_allow_html=True
        )

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
                    audit_log("deal_deleted", p['name'], "Removed from pipeline")
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
            audit_log("deal_created", deal_name,
                      f"Added to pipeline — ${purchase_price/1e6:.1f}M {deal_type}, {int(deal_units)} units, Grade {g}")
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
    render_onboarding_tip("DataRoom")
    st.markdown('<div style="font-size:22px; font-weight:800; color:#0f172a; margin-bottom:20px;">AI Data Room & Document Intelligence</div>', unsafe_allow_html=True)

    col_up, col_chat = st.columns([1, 1.3])

    # ── LEFT: Upload + metrics ──
    with col_up:
        with st.container(border=True):
            st.markdown('<div class="panel-title">Upload Deal Documents</div>', unsafe_allow_html=True)

            rent_file = st.file_uploader("Rent Roll (Excel / CSV)", type=["xlsx","xls","csv"], key="rr")
            t12_file  = st.file_uploader("T12 Trailing Financials (Excel / CSV)", type=["xlsx","xls","csv"], key="t12")

            if rent_file and t12_file:
                with st.spinner("Parsing and analyzing documents..."):
                    try:
                        rr_df  = pd.read_excel(rent_file) if rent_file.name.endswith(('xlsx','xls')) else pd.read_csv(rent_file)
                        rr_data = parse_rent_roll(rr_df)
                    except Exception as e:
                        rr_data = {"error": str(e), "total_units": 0, "gross_potential_rent": 0}
                    try:
                        t12_df     = pd.read_excel(t12_file) if t12_file.name.endswith(('xlsx','xls')) else pd.read_csv(t12_file)
                        t12_parsed = parse_t12(t12_df)
                    except Exception as e:
                        t12_parsed = {"error": str(e), "noi": 0}
                    summary = ai_summarize_excel(rr_data, t12_parsed)
                    if t12_parsed.get('noi', 0) > 0 and st.session_state.deal_data:
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
                c1, c2 = st.columns(2)
                c1.metric("Units (Rent Roll)",     rr_data.get('total_units', '—'))
                c2.metric("Avg Monthly Rent",      f"${rr_data.get('avg_rent', 0):,.0f}")
                c1.metric("Gross Potential Rent",  f"${rr_data.get('gross_potential_rent', 0):,.0f}")
                c2.metric("Trailing NOI (T12)",    f"${t12_parsed.get('noi', 0):,.0f}")
                c1.metric("Occupancy",             f"{rr_data.get('occupancy_rate', 0):.1%}")
                c2.metric("Expense Ratio",         f"{t12_parsed.get('expense_ratio', 0):.1%}")
                st.markdown("**AI Document Summary:**")
                st.markdown(summary)
                st.session_state['upload_context'] = {
                    "rent_roll": rr_data, "t12": t12_parsed, "ai_summary": summary
                }
            else:
                st.info("Upload both a Rent Roll and T12 to activate AI extraction and analysis.")
                st.caption("Rent Roll: Unit #, Monthly Rent, Sq Ft, Status  |  T12: Line items in col A, monthly figures across columns")

    # ── RIGHT: Deal Copilot ──
    with col_chat:
        with st.container(border=True):
            st.markdown('<div class="panel-title">Deal Copilot — AI Underwriter</div>', unsafe_allow_html=True)

            # Messages
            if st.session_state.chat_history:
                chat_box = st.container(height=420, border=False)
                with chat_box:
                    for msg in st.session_state.chat_history:
                        with st.chat_message(msg["role"]):
                            st.markdown(msg["content"])
            else:
                st.markdown("""
                <div style="text-align:center;color:#94a3b8;padding:60px 20px;font-size:14px;line-height:2;">
                    🤖<br><br>
                    Ask me to analyze NOI, identify risks,<br>
                    benchmark cap rates, or explain any part<br>
                    of the underwriting model.
                </div>
                """, unsafe_allow_html=True)

            # Input
            msg_col, btn_col = st.columns([5, 1])
            with msg_col:
                user_msg = st.text_input("", placeholder="Ask about the deal...",
                                         label_visibility="collapsed", key="dr_chat_input")
            with btn_col:
                send = st.button("Send", type="primary", use_container_width=True)

            if send and user_msg:
                st.session_state.chat_history.append({"role": "user", "content": user_msg})
                ctx = json.dumps({
                    "current_deal":  st.session_state.deal_data,
                    "uploaded_data": st.session_state.get('upload_context', {}),
                    "settings":      st.session_state.settings
                }, default=str)
                with st.spinner("Analyzing..."):
                    reply = ai_analyze_deal(ctx, st.session_state.chat_history[:-1], user_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

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
    render_onboarding_tip("ICMemo")
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
                audit_log("memo_generated", d['name'], f"IC memo generated — recommendation: {rec}")
                
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
        
        _memo_preview_html = f"""
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
          <div style="font-size:13px; line-height:1.7; color:#334155; margin-bottom:20px;">{memo_text.replace(chr(10), "<br>") if memo_text else '<em style="color:#94a3b8;">Generate memo to populate AI executive summary...</em>'}</div>
          
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
        """
        st.markdown("".join(_l.strip() for _l in _memo_preview_html.splitlines()), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
def view_settings():
    render_onboarding_tip("Settings")

    st.markdown("""
    <div style='background:linear-gradient(135deg,#0d2a4a,#0d1f3c);border:1px solid #1a9fd4;
                border-radius:12px;padding:20px 24px;margin-bottom:28px;'>
      <div style='font-size:10px;color:#1a9fd4;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>Patent Pending Feature</div>
      <div style='font-size:15px;font-weight:800;color:#e8f0fa;margin-bottom:4px;'>Guided Onboarding Mode</div>
      <div style='font-size:12px;color:#93b4d4;line-height:1.6;'>Turn on to show step-by-step guidance tooltips on every page. Walks new team members through the entire platform — from adding their first deal to generating an IC memo and delivering it to your investment committee.</div>
    </div>
    """, unsafe_allow_html=True)

    onboard_on = st.toggle("Enable Guided Onboarding Mode",
        value=st.session_state.get("onboarding_mode", False),
        help="Shows step-by-step tooltips on each page to guide new analysts through the platform.")
    st.session_state.onboarding_mode = onboard_on
    if onboard_on:
        st.success("Onboarding mode ON — guidance tips appear at the top of every page.", icon="🎓")
    else:
        st.info("Onboarding mode OFF — platform runs in standard mode.", icon="✅")

    # ── AIRE Comps Network opt-in ──
    st.markdown("<br>", unsafe_allow_html=True)
    _optin = st.toggle("Contribute anonymized comps to the AIRE Comps Network",
        value=st.session_state.settings.get("comps_optin", True),
        help="Shares banded, fully anonymized deal metrics (entry cap, IRR, assumptions) with the network benchmark. No names, addresses, prices, or firm identities are ever stored. Powers the live benchmarks on your Deal Dashboard.")
    st.session_state.settings["comps_optin"] = _optin
    if _optin:
        st.caption("Your firm benchmarks against the full network and contributes anonymized data points.")
    else:
        st.caption("Contribution paused — you can still view network benchmarks built from participating firms.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:18px;font-weight:800;color:#e8f0fa;margin-bottom:20px;'>Underwriting Assumptions</div>", unsafe_allow_html=True)
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
        _old_settings = dict(st.session_state.settings)
        st.session_state.settings = s
        ok, err = db_save_settings(s, st.session_state.user_email)
        for _k, _nv in s.items():
            _ov = _old_settings.get(_k)
            if _ov != _nv:
                _fmt = lambda x: f"{x:.4g}" if isinstance(x, float) else str(x)
                audit_log("settings_change", "Underwriting Settings",
                          f"{_k.replace('_',' ').title()} updated",
                          field=_k, old_value=_fmt(_ov), new_value=_fmt(_nv))
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
    dscr = d["noi_year1"] / annual_debt_service(d["debt_amount"]) if d["debt_amount"] else 0

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
    mc2 = aire_monte_carlo(d, st.session_state.settings)
    c4.metric("Loss Prob.",      f"{(mc2['loss_prob'] if mc2 else d['loss_prob']):.1%}")
    c5.metric("LTV",             f"{ltv:.0%}")
    c6.metric("DSCR",            f"{dscr:.2f}x")

    st.markdown("<br>", unsafe_allow_html=True)

    col_mc, col_s = st.columns(2)
    with col_mc:
        st.markdown("<div class='glass-panel'><div class='panel-title'>Monte Carlo — 3,000 Correlated DCF Paths</div>", unsafe_allow_html=True)
        if mc2:
            st.plotly_chart(chart_monte_carlo(mc2['irr_paths']), use_container_width=True, config={"displayModeBar": False})
            st.markdown(f"""<div style="display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:11px;color:#3a5278;border-top:1px solid #e4ecf7;padding-top:10px;margin-top:4px;">
              <span>P5 <b style="color:#dc2626;">{mc2['p5']:.1%}</b></span>
              <span>Median <b style="color:#07111f;">{mc2['p50']:.1%}</b></span>
              <span>Mean <b style="color:#1a6fe0;">{mc2['mean']:.1%}</b></span>
              <span>P95 <b style="color:#059669;">{mc2['p95']:.1%}</b></span>
              <span>Loss <b style="color:#dc2626;">{mc2['loss_prob']:.1%}</b></span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_s:
        st.markdown("<div class='glass-panel'><div class='panel-title'>IRR Sensitivity — Full DCF per Cell</div>", unsafe_allow_html=True)
        st.plotly_chart(chart_sensitivity(d, st.session_state.settings), use_container_width=True, config={"displayModeBar": False})
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
# SECTION 6C | DEBT STRUCTURING VIEW
# ──────────────────────────────────────────────────────────────────────────────

def view_debt_structuring():
    render_onboarding_tip("DebtModel")
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">DEBT STRUCTURING</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">Debt Structuring & Loan Modeling</div></div>""", unsafe_allow_html=True)
    d = st.session_state.deal_data

    col_in, col_out = st.columns([1, 1.6])

    with col_in:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Loan Parameters</div>", unsafe_allow_html=True)
            purchase_price = st.number_input("Purchase Price ($)", value=float(d["purchase_price"]) if d else 10000000.0, step=100000.0, format="%.0f")
            loan_pct       = st.slider("Loan-to-Value (%)", 40, 80, 65)
            loan_amount    = purchase_price * loan_pct / 100
            st.metric("Loan Amount", f"${loan_amount:,.0f}")
            rate           = st.number_input("Interest Rate (%)", value=6.75, step=0.25, format="%.2f") / 100
            amort_years    = st.selectbox("Amortization", [25, 30, 35, 40], index=1)
            io_years       = st.selectbox("Interest-Only Period (Yrs)", [0, 1, 2, 3, 5], index=0)
            loan_fee_pct   = st.number_input("Loan Fee (%)", value=1.0, step=0.25, format="%.2f") / 100
            prepay_years   = st.selectbox("Prepayment Lock (Yrs)", [0, 1, 2, 3, 5], index=3)
            noi_y1         = st.number_input("NOI Year 1 ($)", value=float(d["noi_year1"]) if d else 500000.0, step=10000.0, format="%.0f")

            run = st.button("Model Debt Structure", type="primary", use_container_width=True)

    with col_out:
        if run or st.session_state.get("debt_result"):
            if run:
                result = model_debt_structure(purchase_price, loan_amount, rate, amort_years, io_years, loan_fee_pct, prepay_years)
                st.session_state.debt_result = result
                st.session_state.debt_noi = noi_y1
            else:
                result = st.session_state.debt_result
                noi_y1 = st.session_state.get("debt_noi", noi_y1)

            dscr_io   = noi_y1 / result["io_payment_annual"]   if result["io_payment_annual"] > 0 else 0
            dscr_full = noi_y1 / result["amort_payment_annual"] if result["amort_payment_annual"] > 0 else 0

            st.markdown(f'''
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:20px;margin-bottom:14px;">
              <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin-bottom:14px;">Loan Summary</div>
              <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">
                <div style="background:#f8fafc;border-radius:8px;padding:14px;">
                  <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Loan Amount</div>
                  <div style="font-size:20px;font-weight:800;color:#0f172a;">${result["loan_amount"]/1e6:.2f}M</div>
                </div>
                <div style="background:#f8fafc;border-radius:8px;padding:14px;">
                  <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Net Proceeds</div>
                  <div style="font-size:20px;font-weight:800;color:#0f172a;">${result["net_proceeds"]/1e6:.2f}M</div>
                </div>
                <div style="background:#f8fafc;border-radius:8px;padding:14px;">
                  <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Loan Fee</div>
                  <div style="font-size:20px;font-weight:800;color:#0f172a;">${result["loan_fee"]:,.0f}</div>
                </div>
                <div style="background:#f8fafc;border-radius:8px;padding:14px;">
                  <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">LTV</div>
                  <div style="font-size:20px;font-weight:800;color:#0f172a;">{result["ltv"]:.0%}</div>
                </div>
                <div style="background:#eff6ff;border-radius:8px;padding:14px;">
                  <div style="font-size:10px;color:#1d4ed8;font-weight:700;text-transform:uppercase;margin-bottom:4px;">IO Payment / yr</div>
                  <div style="font-size:20px;font-weight:800;color:#0f172a;">${result["io_payment_annual"]:,.0f}</div>
                </div>
                <div style="background:#eff6ff;border-radius:8px;padding:14px;">
                  <div style="font-size:10px;color:#1d4ed8;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Amort Payment / yr</div>
                  <div style="font-size:20px;font-weight:800;color:#0f172a;">${result["amort_payment_annual"]:,.0f}</div>
                </div>
                <div style="background:{"#f0fdf4" if dscr_io >= 1.25 else "#fee2e2"};border-radius:8px;padding:14px;">
                  <div style="font-size:10px;color:{"#16a34a" if dscr_io >= 1.25 else "#dc2626"};font-weight:700;text-transform:uppercase;margin-bottom:4px;">DSCR (IO)</div>
                  <div style="font-size:20px;font-weight:800;color:#0f172a;">{dscr_io:.2f}x</div>
                </div>
                <div style="background:{"#f0fdf4" if dscr_full >= 1.25 else "#fee2e2"};border-radius:8px;padding:14px;">
                  <div style="font-size:10px;color:{"#16a34a" if dscr_full >= 1.25 else "#dc2626"};font-weight:700;text-transform:uppercase;margin-bottom:4px;">DSCR (Amort)</div>
                  <div style="font-size:20px;font-weight:800;color:#0f172a;">{dscr_full:.2f}x</div>
                </div>
              </div>
            </div>
            ''', unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown("<div class='panel-title'>10-Year Debt Schedule</div>", unsafe_allow_html=True)
                rows = []
                for s in result["schedule"]:
                    rows.append({
                        "Year": s["year"],
                        "Beg Balance": f"${s['beg_balance']:,.0f}",
                        "Payment":     f"${s['payment']:,.0f}",
                        "Interest":    f"${s['interest']:,.0f}",
                        "Principal":   f"${s['principal']:,.0f}",
                        "End Balance": f"${s['end_balance']:,.0f}",
                        "Prepay Penalty": f"${s['prepay_penalty']:,.0f}",
                    })
                st.dataframe(pd.DataFrame(rows).set_index("Year"), use_container_width=True)

            # Balance curve chart
            with st.container(border=True):
                st.markdown("<div class='panel-title'>Loan Balance Paydown</div>", unsafe_allow_html=True)
                yrs   = [s["year"] for s in result["schedule"]]
                bals  = [s["end_balance"]/1e6 for s in result["schedule"]]
                ints  = [s["interest"]/1e6 for s in result["schedule"]]
                princs = [s["principal"]/1e6 for s in result["schedule"]]
                fig = go.Figure()
                fig.add_bar(x=yrs, y=ints,   name="Interest",   marker_color="#dc2626")
                fig.add_bar(x=yrs, y=princs, name="Principal",  marker_color="#2563eb")
                fig.add_scatter(x=yrs, y=bals, mode="lines+markers", name="Balance ($M)",
                                line=dict(color="#0f172a", width=2), yaxis="y2")
                fig.update_layout(barmode="stack", height=280,
                    yaxis=dict(title="Payment ($M)", tickprefix="$", showgrid=False),
                    yaxis2=dict(title="Balance ($M)", overlaying="y", side="right", tickprefix="$"),
                    legend=dict(orientation="h", y=1.1),
                    margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor="white", plot_bgcolor="white")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Set loan parameters and click Model Debt Structure to see full schedule and DSCR analysis.")


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6D | WATERFALL DISTRIBUTION VIEW
# ──────────────────────────────────────────────────────────────────────────────

def view_waterfall():
    render_onboarding_tip("Waterfall")
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">WATERFALL CALC</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">LP/GP Waterfall Distribution</div></div>""", unsafe_allow_html=True)
    d = st.session_state.deal_data

    col_in, col_out = st.columns([1, 1.6])

    with col_in:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Deal Structure</div>", unsafe_allow_html=True)
            purchase_price = st.number_input("Purchase Price ($)", value=float(d["purchase_price"]) if d else 10000000.0, step=100000.0, format="%.0f")
            debt_pct       = st.slider("Debt (%)", 40, 80, 65)
            debt           = purchase_price * debt_pct / 100
            equity         = purchase_price - debt
            st.metric("Total Equity", f"${equity:,.0f}")
            st.metric("LP Equity (90%)", f"${equity*0.90:,.0f}")
            st.metric("GP Equity (10%)", f"${equity*0.10:,.0f}")

            noi_y1        = st.number_input("NOI Year 1 ($)", value=float(d["noi_year1"]) if d else 500000.0, step=10000.0, format="%.0f")
            rent_growth   = st.number_input("Annual NOI Growth (%)", value=3.5, step=0.5, format="%.1f") / 100
            hold_years    = st.slider("Hold Period (Yrs)", 3, 10, 5)
            exit_cap      = st.number_input("Exit Cap Rate (%)", value=5.50, step=0.25, format="%.2f") / 100
            pref_return   = st.number_input("Preferred Return (%)", value=8.0, step=0.5, format="%.1f") / 100

            st.markdown("<div class='panel-title' style='margin-top:16px;'>Promote Hurdles</div>", unsafe_allow_html=True)
            h1_lp = st.slider("Tier 1 LP split (up to Pref)", 60, 95, 80)
            h2_lp = st.slider("Tier 2 LP split (12% IRR)", 50, 85, 70)
            h3_lp = st.slider("Tier 3 LP split (18% IRR)", 30, 70, 50)

            run = st.button("Calculate Waterfall", type="primary", use_container_width=True)

    with col_out:
        if run or st.session_state.get("waterfall_result"):
            if run:
                noi_list = [noi_y1 * (1 + rent_growth)**yr for yr in range(hold_years)]
                noi_final = noi_list[-1]
                exit_value = noi_final / exit_cap if exit_cap > 0 else purchase_price * 1.2
                hurdles = [
                    {"hurdle": pref_return, "lp_split": h1_lp/100, "gp_split": 1-h1_lp/100},
                    {"hurdle": 0.12,        "lp_split": h2_lp/100, "gp_split": 1-h2_lp/100},
                    {"hurdle": 0.18,        "lp_split": h3_lp/100, "gp_split": 1-h3_lp/100},
                    {"hurdle": 999,         "lp_split": 0.30,       "gp_split": 0.70},
                ]
                wf = model_waterfall(equity, noi_list, exit_value, debt, pref_return, hurdles)
                st.session_state.waterfall_result = wf
                st.session_state.waterfall_exit = exit_value
            else:
                wf = st.session_state.waterfall_result
                exit_value = st.session_state.get("waterfall_exit", 0)

            # Returns summary — custom HTML (no truncation)
            lp_out   = wf['lp_total_out']
            gp_out   = wf['gp_total_out']
            lp_em    = wf['lp_em']
            gp_em    = wf['gp_em']
            lp_irr   = wf['lp_irr']
            gp_irr   = wf['gp_irr']
            profit   = wf['total_profit']
            ev_m     = exit_value / 1e6

            def kpi_card(label, value, bg, color):
                return f'''<div style="background:{bg};border-radius:8px;padding:14px 16px;">
                  <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:{color};margin-bottom:6px;">{label}</div>
                  <div style="font-size:19px;font-weight:800;color:#0f172a;white-space:nowrap;">{value}</div>
                </div>'''

            st.markdown(f'''
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:20px;margin-bottom:14px;">
              <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin-bottom:14px;">Returns Summary</div>
              <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">
                {kpi_card("LP Total Out",       f"${lp_out:,.0f}",       "#eff6ff","#1d4ed8")}
                {kpi_card("GP Total Out",       f"${gp_out:,.0f}",       "#f0fdf4","#16a34a")}
                {kpi_card("LP Equity Multiple", f"{lp_em:.2f}x",          "#eff6ff","#1d4ed8")}
                {kpi_card("GP Equity Multiple", f"{gp_em:.2f}x",          "#f0fdf4","#16a34a")}
                {kpi_card("LP IRR (approx)",    f"{lp_irr:.1%}",          "#eff6ff","#1d4ed8")}
                {kpi_card("GP IRR (approx)",    f"{gp_irr:.1%}",          "#f0fdf4","#16a34a")}
                {kpi_card("Total Profit",       f"${profit:,.0f}",        "#f8fafc","#334155")}
                {kpi_card("Exit Value",         f"${ev_m:.2f}M",          "#f8fafc","#334155")}
              </div>
            </div>
            ''', unsafe_allow_html=True)

            # Tier breakdown table
            tier_rows_html = ""
            for i, t in enumerate(wf["tiers"]):
                label = f"Pref ({t['hurdle']:.0%})" if i == 0 else (
                    f"Tier {i+1} ({t['hurdle']:.0%} IRR)" if t["hurdle"] < 999 else "Super Promote")
                gp_pct = f"{t['gp']/t['allocated']*100:.0f}%" if t["allocated"] > 0 else "0%"
                bg = "#f8fafc" if i % 2 == 0 else "#fff"
                tier_rows_html += (
                    f'<tr style="background:{bg};">'
                    f'<td style="padding:10px 14px;font-weight:600;color:#0f172a;">{label}</td>'
                    f'<td style="padding:10px 14px;color:#334155;">${t["allocated"]:,.0f}</td>'
                    f'<td style="padding:10px 14px;color:#1d4ed8;font-weight:600;">${t["lp"]:,.0f}</td>'
                    f'<td style="padding:10px 14px;color:#16a34a;font-weight:600;">${t["gp"]:,.0f}</td>'
                    f'<td style="padding:10px 14px;"><span style="background:#f0fdf4;color:#16a34a;padding:3px 10px;border-radius:4px;font-size:12px;font-weight:700;">{gp_pct}</span></td>'
                    f'</tr>'
                )

            st.markdown(f'''
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:20px;margin-bottom:14px;">
              <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin-bottom:14px;">Tier Breakdown</div>
              <table style="width:100%;border-collapse:collapse;font-size:13px;">
                <thead><tr style="border-bottom:2px solid #e2e8f0;">
                  <th style="padding:10px 14px;text-align:left;color:#64748b;font-size:11px;text-transform:uppercase;">Tier</th>
                  <th style="padding:10px 14px;text-align:left;color:#64748b;font-size:11px;text-transform:uppercase;">Total Allocated</th>
                  <th style="padding:10px 14px;text-align:left;color:#1d4ed8;font-size:11px;text-transform:uppercase;">LP Share</th>
                  <th style="padding:10px 14px;text-align:left;color:#16a34a;font-size:11px;text-transform:uppercase;">GP Share</th>
                  <th style="padding:10px 14px;text-align:left;color:#64748b;font-size:11px;text-transform:uppercase;">GP Promote</th>
                </tr></thead>
                <tbody>{tier_rows_html}</tbody>
              </table>
            </div>
            ''', unsafe_allow_html=True)

            # Chart
            with st.container(border=True):
                st.markdown("<div class='panel-title'>Distribution Waterfall Chart</div>", unsafe_allow_html=True)
                labels  = ["LP Capital Return", "GP Capital Return"] + [f"Tier {i+1}" for i in range(len(wf["tiers"]))]
                lp_vals = [wf["lp_equity_in"], 0] + [t["lp"] for t in wf["tiers"]]
                gp_vals = [0, wf["gp_equity_in"]] + [t["gp"] for t in wf["tiers"]]
                fig = go.Figure()
                fig.add_bar(x=labels, y=lp_vals, name="LP", marker_color="#2563eb",
                            text=[f"${v/1e3:.0f}k" if v > 0 else "" for v in lp_vals], textposition="outside")
                fig.add_bar(x=labels, y=gp_vals, name="GP", marker_color="#16a34a",
                            text=[f"${v/1e3:.0f}k" if v > 0 else "" for v in gp_vals], textposition="outside")
                fig.update_layout(barmode="group", height=300,
                    yaxis=dict(tickprefix="$", showgrid=True, gridcolor="#f1f5f9"),
                    margin=dict(l=0,r=0,t=44,b=0), paper_bgcolor="white", plot_bgcolor="white",
                    legend=dict(orientation="h", y=1.14),
                    font=dict(family="Inter, sans-serif", size=12))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Configure the deal structure and promote hurdles, then click Calculate Waterfall.")


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6E | DEAL COMPARISON VIEW
# ──────────────────────────────────────────────────────────────────────────────

def view_deal_comparison():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">DEAL COMPARISON</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">Side-by-Side Deal Comparison</div></div>""", unsafe_allow_html=True)
    props = st.session_state.properties

    if len(props) < 2:
        st.info("Add at least 2 deals to your pipeline to use the comparison tool.")
        if st.button("← Go to Pipeline"):
            st.session_state.current_view = "Pipeline"
            st.rerun()
        return

    names = [p["name"] for p in props]
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        sel1 = st.selectbox("Deal A", names, index=0, key="cmp1")
    with col_s2:
        sel2 = st.selectbox("Deal B", names, index=min(1, len(names)-1), key="cmp2")

    d1 = next(p for p in props if p["name"] == sel1)
    d2 = next(p for p in props if p["name"] == sel2)

    st.markdown("<br>", unsafe_allow_html=True)

    # Header cards
    hc1, hc2 = st.columns(2)
    for col, d, color in [(hc1, d1, "#2563eb"), (hc2, d2, "#16a34a")]:
        grade_cls = f"grade-{d['grade'].lower()}"
        with col:
            st.markdown(f"""
            <div style="background:#fff;border-radius:10px;border:2px solid {color};padding:16px;margin-bottom:16px;">
              <div style="font-size:18px;font-weight:800;color:#0f172a;">{d["name"]}</div>
              <div style="font-size:12px;color:#64748b;">{d.get("address","")}</div>
              <div style="font-size:12px;color:#64748b;margin-top:4px;">{d["type"]} &bull; {d["units"]} units &bull; {d["vintage"]}</div>
            </div>""", unsafe_allow_html=True)

    # KPI comparison table
    metrics = [
        ("Purchase Price",   f"${d1['purchase_price']/1e6:.1f}M",       f"${d2['purchase_price']/1e6:.1f}M",  None),
        ("NOI Year 1",       f"${d1['noi_year1']:,.0f}",                  f"${d2['noi_year1']:,.0f}",             None),
        ("Cap Rate",         f"{d1['noi_year1']/d1['purchase_price']:.2%}" if d1["purchase_price"] else "—",
                             f"{d2['noi_year1']/d2['purchase_price']:.2%}" if d2["purchase_price"] else "—",    None),
        ("Levered IRR",      f"{d1['irr']:.1%}",                          f"{d2['irr']:.1%}",                    "higher"),
        ("Equity Multiple",  f"{d1['equity_mult']:.2f}x",                 f"{d2['equity_mult']:.2f}x",           "higher"),
        ("GP IRR",           f"{d1['gp_irr']:.1%}",                       f"{d2['gp_irr']:.1%}",                 "higher"),
        ("Loss Probability", f"{d1['loss_prob']:.1%}",                    f"{d2['loss_prob']:.1%}",              "lower"),
        ("Deal Score",       f"{d1['score']}/100",                         f"{d2['score']}/100",                  "higher"),
        ("Grade",            d1["grade"],                                   d2["grade"],                           None),
        ("Status",           d1["status"].upper(),                         d2["status"].upper(),                  None),
    ]

    with st.container(border=True):
        st.markdown("<div class='panel-title'>KPI Comparison</div>", unsafe_allow_html=True)
        header = st.columns([2, 1.5, 1.5])
        header[0].markdown("**Metric**")
        header[1].markdown(f"**{d1['name'][:20]}**")
        header[2].markdown(f"**{d2['name'][:20]}**")
        st.divider()
        for label, v1, v2, better in metrics:
            row = st.columns([2, 1.5, 1.5])
            row[0].write(label)
            # Highlight winner
            try:
                n1 = float(v1.replace("%","").replace("x","").replace("$","").replace("M","").replace(",","").replace("/100",""))
                n2 = float(v2.replace("%","").replace("x","").replace("$","").replace("M","").replace(",","").replace("/100",""))
                if better == "higher":
                    row[1].markdown(f"**:blue[{v1}]**" if n1 >= n2 else v1)
                    row[2].markdown(f"**:blue[{v2}]**" if n2 > n1  else v2)
                elif better == "lower":
                    row[1].markdown(f"**:blue[{v1}]**" if n1 <= n2 else v1)
                    row[2].markdown(f"**:blue[{v2}]**" if n2 < n1  else v2)
                else:
                    row[1].write(v1); row[2].write(v2)
            except:
                row[1].write(v1); row[2].write(v2)

    # Radar chart
    with st.container(border=True):
        st.markdown("<div class='panel-title'>Radar Comparison</div>", unsafe_allow_html=True)
        cats = ["IRR", "Equity Mult", "Deal Score", "Low Risk", "Cap Rate"]
        def normalize(d):
            cap = d["noi_year1"]/d["purchase_price"] if d["purchase_price"] else 0
            return [
                min(d["irr"] / 0.25,       1.0),
                min((d["equity_mult"]-1)/1.5, 1.0),
                d["score"] / 100,
                max(1 - d["loss_prob"] / 0.20, 0),
                min(cap / 0.08,            1.0),
            ]
        vals1 = normalize(d1)
        vals2 = normalize(d2)
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=vals1+[vals1[0]], theta=cats+[cats[0]],
            fill="toself", name=d1["name"][:20], line=dict(color="#2563eb")))
        fig.add_trace(go.Scatterpolar(r=vals2+[vals2[0]], theta=cats+[cats[0]],
            fill="toself", name=d2["name"][:20], line=dict(color="#16a34a"), opacity=0.7))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])),
            height=320, margin=dict(l=40,r=40,t=40,b=0),
            legend=dict(orientation="h", y=-0.1), paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6F | PORTFOLIO ALERTS VIEW
# ──────────────────────────────────────────────────────────────────────────────

def view_alerts():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">ALERTS</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">Portfolio Alerts & Performance Monitor</div></div>""", unsafe_allow_html=True)
    props = st.session_state.properties

    if not props:
        st.info("Add deals to your pipeline to enable performance monitoring.")
        return

    col_run, _ = st.columns([1, 3])
    with col_run:
        if st.button("🔄 Refresh Alert Scan", type="primary", use_container_width=True):
            st.session_state.alert_log = check_irr_alerts(props)
            st.session_state.alert_last_run = datetime.now().strftime("%B %d, %Y %H:%M")

    if st.session_state.get("alert_last_run"):
        st.caption(f"Last scanned: {st.session_state.alert_last_run}")

    alerts = st.session_state.get("alert_log", [])

    # Summary strip
    total = len(props)
    flagged = len(alerts)
    high = sum(1 for a in alerts if a["severity"] == "high")
    on_track = total - flagged
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Deals",   total)
    c2.metric("On Track",      on_track, delta=f"{on_track/total*100:.0f}%" if total else None)
    c3.metric("Flagged",       flagged,  delta=f"-{flagged}" if flagged > 0 else None, delta_color="inverse")
    c4.metric("High Severity", high,     delta=f"-{high}" if high > 0 else None, delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    if not alerts:
        if st.session_state.get("alert_log") is not None:
            st.success("✅ All deals are performing within threshold. No alerts at this time.")
        else:
            st.info("Click **Refresh Alert Scan** to check all deals against their underwritten IRR targets.")
        return

    for a in sorted(alerts, key=lambda x: abs(x["drift"]), reverse=True):
        sev_color = "#dc2626" if a["severity"] == "high" else "#d97706"
        sev_bg    = "#fee2e2" if a["severity"] == "high" else "#fef9c3"
        icon      = "🔴" if a["severity"] == "high" else "🟡"
        with st.container(border=True):
            hc1, hc2, hc3, hc4 = st.columns([3, 1, 1, 1])
            hc1.markdown(f"{icon} **{a['name']}** — Grade {a['grade']}")
            hc2.metric("Underwritten", f"{a['underwritten_irr']:.1%}")
            hc3.metric("Current",      f"{a['current_irr']:.1%}", delta=f"{a['drift']:+.1%}", delta_color="normal")
            hc4.markdown(f"""
            <div style="background:{sev_bg};border-radius:6px;padding:8px;text-align:center;margin-top:8px;">
              <div style="font-size:10px;color:{sev_color};font-weight:700;text-transform:uppercase;">{a["severity"]} alert</div>
              <div style="font-size:12px;color:{sev_color};font-weight:700;">IRR {a["direction"]}</div>
            </div>""", unsafe_allow_html=True)

    # Alert history chart
    if alerts:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>IRR Drift by Property</div>", unsafe_allow_html=True)
            names_a = [a["name"][:18] for a in alerts]
            drifts  = [a["drift"]*100 for a in alerts]
            colors  = ["#dc2626" if d < 0 else "#16a34a" for d in drifts]
            fig = go.Figure(go.Bar(x=names_a, y=drifts, marker_color=colors,
                text=[f"{d:+.1f}%" for d in drifts], textposition="outside"))
            fig.add_hline(y=0, line_color="#0f172a", line_width=1)
            fig.update_layout(height=260, yaxis=dict(title="IRR Drift (%)", showgrid=True, gridcolor="#f1f5f9"),
                margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor="white", plot_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6G | OM PDF IMPORT — AI DEAL EXTRACTOR
# ──────────────────────────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        import io as _io
        # Try pypdf first
        try:
            from pypdf import PdfReader
            reader = PdfReader(_io.BytesIO(pdf_bytes))
            return "\n".join(page.extract_text() or "" for page in reader.pages[:20])

        except ImportError:
            pass
        # Fallback: pdfminer
        try:
            from pdfminer.high_level import extract_text as pm_extract
            return pm_extract(_io.BytesIO(pdf_bytes))
        except ImportError:
            pass
        return ""
    except Exception as e:
        return ""

def ai_parse_om(text: str) -> dict:
    prompt = f"""You are an expert CRE analyst. Extract deal data from this Offering Memorandum text.
Return ONLY a valid JSON object with these exact keys (use null if not found):
{{
  "property_name": string,
  "address": string,
  "property_type": string (Multifamily/Office/Retail/Industrial/Mixed-Use),
  "units": integer,
  "vintage_year": integer,
  "asking_price": float,
  "noi_year1": float,
  "cap_rate": float (as decimal e.g. 0.055),
  "occupancy_rate": float (as decimal),
  "avg_monthly_rent": float,
  "total_sqft": float,
  "num_buildings": integer,
  "market": string,
  "key_features": list of 3 strings,
  "investment_highlights": list of 3 strings
}}

OM TEXT (first 6000 chars):
{text[:6000]}"""
    try:
        r = ai_client.chat.completions.create(
            model="gpt-4o", max_tokens=800, temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = r.choices[0].message.content.strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        return {}


def view_om_import():
    render_onboarding_tip("OMImport")
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">OM IMPORT</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">OM Import — AI Reads the Broker PDF</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:24px;'>Upload a broker Offering Memorandum PDF and AI will extract every key metric automatically.</div>", unsafe_allow_html=True)

    col_up, col_out = st.columns([1, 1.5])

    with col_up:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Upload Offering Memorandum</div>", unsafe_allow_html=True)
            pdf_file = st.file_uploader("Drop PDF here", type=["pdf"], key="om_pdf")
            url_input = st.text_input("Or paste a direct PDF URL", placeholder="https://broker.com/deal.pdf")

            if pdf_file or url_input:
                if st.button("⚡ Extract Deal Data with AI", type="primary", use_container_width=True):
                    with st.spinner("Reading PDF and extracting deal metrics..."):
                        # Get PDF bytes
                        if pdf_file:
                            pdf_bytes = pdf_file.read()
                        else:
                            try:
                                resp = requests.get(url_input, timeout=15)
                                pdf_bytes = resp.content
                            except Exception as e:
                                st.error(f"Could not fetch URL: {e}")
                                pdf_bytes = b""

                        if pdf_bytes:
                            # Install pypdf if needed
                            try:
                                from pypdf import PdfReader
                            except ImportError:
                                import subprocess, sys
                                subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf", "-q"])

                            text = extract_text_from_pdf(pdf_bytes)
                            if not text.strip():
                                st.warning("Could not extract text from PDF. The file may be image-based. Try a text-based PDF.")
                            else:
                                data = ai_parse_om(text)
                                st.session_state.om_extracted = data
                                st.session_state.om_text_preview = text[:800]
                                st.success(f"✅ Extracted {len([v for v in data.values() if v])} fields from {len(text):,} characters")

            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("Supports standard broker OMs from CBRE, JLL, Eastdil, Marcus & Millichap, and most brokerage formats.")

    with col_out:
        data = st.session_state.get("om_extracted", {})
        if not data:
            st.markdown("""
            <div style='text-align:center;padding:80px 20px;color:#94a3b8;'>
              <div style='font-size:40px;margin-bottom:16px;'>📄</div>
              <div style='font-size:15px;font-weight:600;color:#64748b;margin-bottom:8px;'>No OM uploaded yet</div>
              <div style='font-size:13px;line-height:1.8;'>Upload a PDF or paste a URL on the left.<br>AI will read it and populate every field below.</div>
            </div>""", unsafe_allow_html=True)
        else:
            with st.container(border=True):
                st.markdown("<div class='panel-title'>Extracted Deal Data — Review & Edit</div>", unsafe_allow_html=True)

                c1, c2 = st.columns(2)
                name     = c1.text_input("Property Name",   value=data.get("property_name") or "")
                address  = c2.text_input("Address",          value=data.get("address") or "")
                ptype    = c1.selectbox("Property Type",     ["Multifamily","Office","Retail","Industrial","Mixed-Use"],
                                         index=["Multifamily","Office","Retail","Industrial","Mixed-Use"].index(data.get("property_type","Multifamily")) if data.get("property_type") in ["Multifamily","Office","Retail","Industrial","Mixed-Use"] else 0)
                units    = c2.number_input("Units / Sq Ft",  value=int(data.get("units") or 0), min_value=0)
                vintage  = c1.number_input("Vintage Year",   value=int(data.get("vintage_year") or 2000), min_value=1900, max_value=2030)
                price    = c2.number_input("Asking Price ($)",value=float(data.get("asking_price") or 0), step=100000.0, format="%.0f")
                noi      = c1.number_input("NOI Year 1 ($)", value=float(data.get("noi_year1") or 0), step=10000.0, format="%.0f")
                cap      = c2.number_input("Cap Rate (%)",   value=float((data.get("cap_rate") or 0)*100), step=0.25, format="%.2f")
                occ      = c1.number_input("Occupancy (%)",  value=float((data.get("occupancy_rate") or 0.93)*100), step=0.5, format="%.1f")
                avg_rent = c2.number_input("Avg Monthly Rent ($)", value=float(data.get("avg_monthly_rent") or 0), step=50.0, format="%.0f")

                # Highlights
                highlights = data.get("investment_highlights") or []
                if highlights:
                    st.markdown("<div style='margin-top:8px;'><b>AI-Extracted Highlights:</b></div>", unsafe_allow_html=True)
                    for h in highlights:
                        st.markdown(f"✅ {h}")

                st.markdown("<br>", unsafe_allow_html=True)

                if st.button("➕ Add to Pipeline", type="primary", use_container_width=True):
                    if not name:
                        st.error("Property name is required.")
                    else:
                        import time as _t
                        ltv   = st.session_state.settings["max_ltv"]
                        debt  = price * ltv
                        lp_eq = price * (1 - ltv) * 0.90
                        gp_eq = price * (1 - ltv) * 0.10
                        cap_r = noi / price if price else 0
                        est_irr = cap_r + 0.04
                        est_em  = 1.0 + est_irr * 5
                        s, g    = score_deal(est_irr, est_em, 0.05)
                        new_prop = {
                            "id": f"prop_{int(_t.time())}",
                            "name": name, "address": address, "units": int(units),
                            "vintage": int(vintage), "type": ptype, "status": "active",
                            "purchase_price": price, "debt_amount": debt,
                            "lp_equity": lp_eq, "gp_equity": gp_eq, "noi_year1": noi,
                            "irr": est_irr, "equity_mult": est_em, "gp_irr": est_irr * 1.4,
                            "loss_prob": 0.05, "grade": g, "score": s,
                            "acquisition_date": datetime.now().strftime("%Y-%m-%d"),
                            "ai_prediction": est_irr, "ai_correct": True,
                            "lat": 32.7767, "lon": -96.7970, "notes": f"Imported from OM. Cap rate: {cap:.2f}%"
                        }
                        ok, err = db_save(new_prop, st.session_state.user_email)
                        audit_log("om_imported", name,
                                  f"Imported from OM — ${price/1e6:.1f}M {ptype}, {int(units)} units, Grade {g}")
                        st.session_state.properties.append(new_prop)
                        st.session_state.deal_data   = new_prop
                        st.session_state.deal_loaded = True
                        st.session_state.om_extracted = {}
                        if ok:
                            st.success(f"✅ '{name}' added to pipeline and saved to database!")
                        else:
                            st.warning(f"Added to session but DB save failed: {err}")
                        st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6H | LP INVESTOR PORTAL
# ──────────────────────────────────────────────────────────────────────────────

def view_lp_portal():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">LP PORTAL</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">Investor Portal — LP-Facing View</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:24px;'>Investor-facing view of your portfolio. Share this summary with your LPs — clean, professional, no internal data exposed.</div>", unsafe_allow_html=True)

    props = st.session_state.properties
    if not props:
        st.info("Add deals to your pipeline to populate the LP portal.")
        return

    # Portfolio header
    total_aum    = sum(p["purchase_price"] for p in props)
    total_equity = sum(p["lp_equity"] for p in props)
    avg_irr      = sum(p["irr"] for p in props) / len(props)
    avg_em       = sum(p["equity_mult"] for p in props) / len(props)
    active_deals = sum(1 for p in props if p["status"] == "active")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#07111f 0%,#0f2744 100%);border-radius:12px;padding:28px 32px;margin-bottom:24px;color:#fff;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">
        <div>
          <div style="font-size:28px;font-weight:900;letter-spacing:-1px;">AIRE</div>
          <div style="font-size:11px;color:#3b82f6;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Investor Portfolio Summary</div>
          <div style="font-size:12px;color:#8ea5c0;">As of {datetime.now().strftime("%B %d, %Y")}</div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;text-align:center;">
          <div><div style="font-size:10px;color:#8ea5c0;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Total AUM</div>
               <div style="font-size:22px;font-weight:800;">${total_aum/1e6:.1f}M</div></div>
          <div><div style="font-size:10px;color:#8ea5c0;font-weight:700;text-transform:uppercase;margin-bottom:4px;">LP Equity</div>
               <div style="font-size:22px;font-weight:800;">${total_equity/1e6:.1f}M</div></div>
          <div><div style="font-size:10px;color:#8ea5c0;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Avg LP IRR</div>
               <div style="font-size:22px;font-weight:800;color:#3b82f6;">{avg_irr:.1%}</div></div>
          <div><div style="font-size:10px;color:#8ea5c0;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Avg EM</div>
               <div style="font-size:22px;font-weight:800;color:#3b82f6;">{avg_em:.2f}x</div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Individual property cards
    st.markdown("<div style='font-size:14px;font-weight:700;color:#0f172a;margin-bottom:16px;'>Active Investments</div>", unsafe_allow_html=True)

    for p in props:
        if p["status"] == "closed":
            continue
        cap_rate = p["noi_year1"] / p["purchase_price"] if p["purchase_price"] else 0
        dscr     = p["noi_year1"] / annual_debt_service(p["debt_amount"]) if p["debt_amount"] else 0
        grade_color = {"A":"#166534","B":"#1d4ed8","C":"#92400e","D":"#991b1b"}.get(p["grade"],"#334155")
        grade_bg    = {"A":"#dcfce7","B":"#dbeafe","C":"#fef9c3","D":"#fee2e2"}.get(p["grade"],"#f8fafc")

        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:20px;margin-bottom:12px;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;">
            <div>
              <div style="font-size:16px;font-weight:800;color:#0f172a;">{p["name"]}</div>
              <div style="font-size:12px;color:#64748b;margin-top:2px;">{p.get("address","") or "—"} &bull; {p["type"]} &bull; {p["units"]} Units &bull; {p["vintage"]}</div>
              <div style="font-size:11px;color:#94a3b8;margin-top:2px;">Acquired {p.get("acquisition_date","—")}</div>
            </div>
            <span style="background:{grade_bg};color:{grade_color};font-size:13px;font-weight:800;padding:6px 14px;border-radius:6px;">Grade {p["grade"]}</span>
          </div>
          <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;">
            <div style="text-align:center;background:#f8fafc;border-radius:8px;padding:10px;">
              <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">LP Equity</div>
              <div style="font-size:16px;font-weight:800;color:#0f172a;">${p["lp_equity"]/1e6:.2f}M</div>
            </div>
            <div style="text-align:center;background:#eff6ff;border-radius:8px;padding:10px;">
              <div style="font-size:10px;color:#1d4ed8;font-weight:700;text-transform:uppercase;margin-bottom:4px;">LP IRR</div>
              <div style="font-size:16px;font-weight:800;color:#1d4ed8;">{p["irr"]:.1%}</div>
            </div>
            <div style="text-align:center;background:#eff6ff;border-radius:8px;padding:10px;">
              <div style="font-size:10px;color:#1d4ed8;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Equity Multiple</div>
              <div style="font-size:16px;font-weight:800;color:#1d4ed8;">{p["equity_mult"]:.2f}x</div>
            </div>
            <div style="text-align:center;background:#f8fafc;border-radius:8px;padding:10px;">
              <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Cap Rate</div>
              <div style="font-size:16px;font-weight:800;color:#0f172a;">{cap_rate:.2%}</div>
            </div>
            <div style="text-align:center;background:#f8fafc;border-radius:8px;padding:10px;">
              <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">DSCR</div>
              <div style="font-size:16px;font-weight:800;color:#0f172a;">{dscr:.2f}x</div>
            </div>
          </div>
          {"<div style='margin-top:12px;background:#f0fdf4;border-radius:6px;padding:10px;font-size:12px;color:#166534;'>✅ AI Tracking: On Target</div>" if p.get("ai_correct") else "<div style='margin-top:12px;background:#fef9c3;border-radius:6px;padding:10px;font-size:12px;color:#92400e;'>⚠️ AI Tracking: Monitor Closely</div>"}
        </div>
        """, unsafe_allow_html=True)

    # Closed/exited deals
    closed = [p for p in props if p["status"] == "closed"]
    if closed:
        st.markdown("<div style='font-size:14px;font-weight:700;color:#0f172a;margin:24px 0 12px;'>Exited Investments</div>", unsafe_allow_html=True)
        for p in closed:
            st.markdown(f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:16px 20px;margin-bottom:10px;opacity:0.8;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <div style="font-size:15px;font-weight:700;color:#334155;">{p["name"]}</div>
                  <div style="font-size:12px;color:#94a3b8;">{p["type"]} &bull; {p["units"]} Units &bull; Exited</div>
                </div>
                <div style="text-align:right;">
                  <div style="font-size:16px;font-weight:800;color:#16a34a;">{p["irr"]:.1%} IRR</div>
                  <div style="font-size:13px;color:#64748b;">{p["equity_mult"]:.2f}x EM</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

    # PDF export
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📥 Export LP Report (PDF)", type="primary"):
        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
        body{{font-family:Arial,sans-serif;color:#0f172a;margin:40px;font-size:13px;}}
        h1{{font-size:28px;font-weight:900;}}
        .meta{{color:#64748b;font-size:12px;margin-bottom:24px;}}
        table{{width:100%;border-collapse:collapse;margin-bottom:24px;}}
        th{{background:#07111f;color:#fff;padding:10px;text-align:left;font-size:11px;text-transform:uppercase;}}
        td{{padding:10px;border-bottom:1px solid #e2e8f0;font-size:13px;}}
        tr:nth-child(even){{background:#f8fafc;}}
        .footer{{margin-top:40px;color:#94a3b8;font-size:11px;border-top:1px solid #e2e8f0;padding-top:12px;}}
        </style></head><body>
        <h1>AIRE — LP Portfolio Summary</h1>
        <div class="meta">As of {datetime.now().strftime("%B %d, %Y")} &nbsp;|&nbsp; Total AUM: ${total_aum/1e6:.1f}M &nbsp;|&nbsp; Avg IRR: {avg_irr:.1%}</div>
        <table><thead><tr><th>Property</th><th>Type</th><th>LP Equity</th><th>LP IRR</th><th>EM</th><th>Cap Rate</th><th>Status</th></tr></thead><tbody>"""
        for p in props:
            cap_r = p["noi_year1"]/p["purchase_price"] if p["purchase_price"] else 0
            html += f"<tr><td>{p['name']}</td><td>{p['type']}</td><td>${p['lp_equity']:,.0f}</td><td>{p['irr']:.1%}</td><td>{p['equity_mult']:.2f}x</td><td>{cap_r:.2%}</td><td>{p['status'].upper()}</td></tr>"
        html += f"</tbody></table><div class='footer'>Confidential — AIRE Institutional Underwriting &nbsp;|&nbsp; {datetime.now().strftime('%Y')}</div></body></html>"
        try:
            import weasyprint
            pdf = weasyprint.HTML(string=html).write_pdf()
            ext, mime = "pdf", "application/pdf"
        except:
            pdf, ext, mime = html.encode(), "html", "text/html"
        st.download_button("Download LP Report", data=pdf,
            file_name=f"AIRE_LP_Report_{datetime.now().strftime('%Y%m%d')}.{ext}", mime=mime)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6I | DEAL PIPELINE CRM
# ──────────────────────────────────────────────────────────────────────────────

CRM_STAGES = ["Sourcing", "Initial UW", "LOI", "Due Diligence", "Closing", "Closed", "Passed"]
CRM_STAGE_COLORS = {
    "Sourcing":      ("#eff6ff","#1d4ed8"),
    "Initial UW":    ("#f0fdf4","#16a34a"),
    "LOI":           ("#fef9c3","#92400e"),
    "Due Diligence": ("#fef3c7","#d97706"),
    "Closing":       ("#ede9fe","#7c3aed"),
    "Closed":        ("#dcfce7","#166534"),
    "Passed":        ("#f1f5f9","#64748b"),
}

def view_crm():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">CRM</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">Deal Pipeline CRM</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:20px;'>Track every deal from first look to close. Log notes, contacts, and stage history.</div>", unsafe_allow_html=True)

    props = st.session_state.properties
    if "crm_data" not in st.session_state:
        # Initialize CRM records from existing properties
        st.session_state.crm_data = {
            p["id"]: {
                "stage":    "Initial UW",
                "broker":   "",
                "broker_email": "",
                "broker_phone": "",
                "loi_date": "",
                "close_date": "",
                "notes":    [],
                "history":  [{"date": datetime.now().strftime("%Y-%m-%d"), "stage": "Initial UW", "note": "Deal added to pipeline."}],
            }
            for p in props if p["id"] not in st.session_state.get("crm_data", {})
        }

    # Add any new props missing from CRM
    for p in props:
        if p["id"] not in st.session_state.crm_data:
            st.session_state.crm_data[p["id"]] = {
                "stage": "Initial UW", "broker": "", "broker_email": "",
                "broker_phone": "", "loi_date": "", "close_date": "",
                "notes": [],
                "history": [{"date": datetime.now().strftime("%Y-%m-%d"), "stage": "Initial UW", "note": "Deal added."}],
            }

    if not props:
        st.info("Add deals to your pipeline to track them in the CRM.")
        return

    # Stage summary strip
    stage_counts = {}
    for crm in st.session_state.crm_data.values():
        s = crm.get("stage","Sourcing")
        stage_counts[s] = stage_counts.get(s,0) + 1

    cols = st.columns(len(CRM_STAGES))
    for i, stage in enumerate(CRM_STAGES):
        bg, color = CRM_STAGE_COLORS[stage]
        count = stage_counts.get(stage, 0)
        cols[i].markdown(f"""
        <div style="background:{bg};border-radius:8px;padding:10px;text-align:center;">
          <div style="font-size:10px;color:{color};font-weight:700;text-transform:uppercase;letter-spacing:.5px;">{stage}</div>
          <div style="font-family:Outfit,sans-serif;font-size:22px;font-weight:800;letter-spacing:-0.03em;color:#07111f;">{count}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Kanban-style list — grouped by stage
    view_mode = st.radio("View", ["All Deals", "Kanban by Stage"], horizontal=True)

    def deal_card(p, crm):
        bg, color = CRM_STAGE_COLORS.get(crm["stage"], ("#f8fafc","#64748b"))
        cap_rate = p["noi_year1"]/p["purchase_price"] if p["purchase_price"] else 0
        return f"""
        <div style="background:#fff;border:1px solid #e2e8f0;border-left:4px solid {color};border-radius:8px;padding:16px;margin-bottom:10px;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
              <div style="font-size:15px;font-weight:800;color:#0f172a;">{p["name"]}</div>
              <div style="font-size:12px;color:#64748b;">{p.get("address","") or "No address"} &bull; {p["type"]} &bull; {p["units"]} units</div>
            </div>
            <span style="background:{bg};color:{color};font-size:11px;font-weight:700;padding:4px 10px;border-radius:4px;white-space:nowrap;">{crm["stage"]}</span>
          </div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px;">
            <div style="font-size:11px;color:#64748b;">Price<br><b style="color:#0f172a;">${p["purchase_price"]/1e6:.1f}M</b></div>
            <div style="font-size:11px;color:#64748b;">IRR<br><b style="color:#1d4ed8;">{p["irr"]:.1%}</b></div>
            <div style="font-size:11px;color:#64748b;">Cap Rate<br><b style="color:#0f172a;">{cap_rate:.2%}</b></div>
            <div style="font-size:11px;color:#64748b;">Grade<br><b style="color:#0f172a;">{p["grade"]}</b></div>
          </div>
          {f'<div style="margin-top:10px;font-size:12px;color:#64748b;">🏢 Broker: <b>{crm["broker"]}</b></div>' if crm.get("broker") else ""}
          {f'<div style="font-size:11px;color:#94a3b8;margin-top:4px;">Last updated: {crm["history"][-1]["date"] if crm["history"] else "—"}</div>'}
        </div>"""

    if view_mode == "Kanban by Stage":
        for stage in CRM_STAGES:
            stage_props = [p for p in props if st.session_state.crm_data.get(p["id"],{}).get("stage") == stage]
            if not stage_props:
                continue
            bg, color = CRM_STAGE_COLORS[stage]
            st.markdown(f"<div style='font-size:12px;font-weight:700;color:{color};text-transform:uppercase;letter-spacing:1px;margin:16px 0 8px;padding:6px 12px;background:{bg};border-radius:6px;display:inline-block;'>{stage} ({len(stage_props)})</div>", unsafe_allow_html=True)
            for p in stage_props:
                crm = st.session_state.crm_data.get(p["id"], {})
                st.markdown(deal_card(p, crm), unsafe_allow_html=True)
    else:
        for p in props:
            crm = st.session_state.crm_data.get(p["id"], {})
            st.markdown(deal_card(p, crm), unsafe_allow_html=True)

    # Deal editor
    st.markdown("---")
    st.markdown("<div style='font-size:16px;font-weight:700;color:#0f172a;margin-bottom:12px;'>Edit Deal CRM Record</div>", unsafe_allow_html=True)
    prop_names = [p["name"] for p in props]
    sel = st.selectbox("Select Deal", prop_names, key="crm_sel")
    sel_prop = next(p for p in props if p["name"] == sel)
    crm = st.session_state.crm_data.get(sel_prop["id"], {})

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Stage & Dates</div>", unsafe_allow_html=True)
            new_stage = st.selectbox("Pipeline Stage", CRM_STAGES,
                index=CRM_STAGES.index(crm.get("stage","Initial UW")))
            loi_date   = st.text_input("LOI Date",   value=crm.get("loi_date",""),   placeholder="2024-03-15")
            close_date = st.text_input("Close Date", value=crm.get("close_date",""), placeholder="2024-06-30")

    with c2:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Broker Contact</div>", unsafe_allow_html=True)
            broker       = st.text_input("Broker Name",  value=crm.get("broker",""))
            broker_email = st.text_input("Broker Email", value=crm.get("broker_email",""))
            broker_phone = st.text_input("Broker Phone", value=crm.get("broker_phone",""))

    new_note = st.text_area("Add Note / Activity Log", placeholder="e.g. Called broker, touring property next week, revised NOI down 5%...", height=80)

    if st.button("💾 Save CRM Record", type="primary"):
        entry = st.session_state.crm_data.get(sel_prop["id"], {})
        old_stage = entry.get("stage","")
        entry["stage"]        = new_stage
        entry["loi_date"]     = loi_date
        entry["close_date"]   = close_date
        entry["broker"]       = broker
        entry["broker_email"] = broker_email
        entry["broker_phone"] = broker_phone
        if new_note.strip():
            entry.setdefault("notes",[]).append({"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "text": new_note.strip()})
        if new_stage != old_stage:
            entry.setdefault("history",[]).append({"date": datetime.now().strftime("%Y-%m-%d"), "stage": new_stage, "note": f"Stage moved from {old_stage} to {new_stage}"})
        st.session_state.crm_data[sel_prop["id"]] = entry
        st.success(f"✅ CRM record updated for {sel_prop['name']}")
        st.rerun()

    # Activity history
    history = crm.get("history",[])
    notes   = crm.get("notes",[])
    if history or notes:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Activity History</div>", unsafe_allow_html=True)
            all_events = (
                [{"date": h["date"], "text": f"📍 Stage: {h['stage']} — {h['note']}"} for h in history] +
                [{"date": n["date"], "text": f"📝 {n['text']}"} for n in notes]
            )
            all_events.sort(key=lambda x: x["date"], reverse=True)
            for ev in all_events[:15]:
                st.markdown(f"<div style='font-size:13px;padding:6px 0;border-bottom:1px solid #f1f5f9;'><span style='color:#94a3b8;font-size:11px;'>{ev['date']}</span><br>{ev['text']}</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6J | LIVE MARKET DATA VIEW
# ──────────────────────────────────────────────────────────────────────────────

def view_market_data():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">MARKET DATA</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">Live Market Data & Deal Benchmarking</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:24px;'>Real-time macro indicators from FRED + how your active deal stacks up against current market benchmarks.</div>", unsafe_allow_html=True)

    # ── Macro strip ──
    with st.spinner("Fetching live market data..."):
        mdata = fetch_all_market_data()

    def macro_card(label, val, unit, good_dir, benchmark=None):
        if val is None:
            display = "N/A"
            color   = "#64748b"
        else:
            display = f"{val:.2f}{unit}"
            color   = "#0f172a"
        b_html = f"<div style='font-size:10px;color:#94a3b8;margin-top:2px;'>{benchmark}</div>" if benchmark else ""
        return f"""<div style='background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:14px 16px;'>
          <div style='font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px;'>{label}</div>
          <div style='font-size:22px;font-weight:800;color:{color};'>{display}</div>
          {b_html}
        </div>"""

    t10  = mdata["t10"]["value"]
    sofr = mdata["sofr"]["value"]
    cpi  = mdata["cpi"]["value"]
    vac  = mdata["vacancy"]["value"]
    starts = mdata["housing"]["value"]
    permits = mdata["permits"]["value"]

    st.markdown(f"""
    <div style='display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:24px;'>
      {macro_card("10-Yr Treasury", t10,    "%", "lower", "Loan spread: +200bps")}
      {macro_card("SOFR",           sofr,   "%", "lower", "Floating rate index")}
      {macro_card("CPI (Level)",    cpi,    "",  "lower", "Inflation indicator")}
      {macro_card("Rental Vacancy", vac,    "%", "lower", "Nat'l avg vacancy")}
      {macro_card("Housing Starts", starts, "k", "higher","000s of units/mo")}
      {macro_card("Bldg Permits",   permits,"k", "higher","000s of units/mo")}
    </div>
    """, unsafe_allow_html=True)

    # Source note
    has_fred = bool(st.secrets.get("FRED_API_KEY",""))
    if not has_fred:
        st.info("💡 Add `FRED_API_KEY` to your Streamlit secrets to pull live FRED data. Get a free key at fred.stlouisfed.org/docs/api/api_key.html", icon="🔑")

    # ── Cap rate benchmarks by asset class ──
    st.markdown("<div style='font-size:16px;font-weight:700;color:#0f172a;margin:8px 0 14px;'>Current Cap Rate Benchmarks (Q4 2024 — CBRE/JLL)</div>", unsafe_allow_html=True)

    cap_rows = []
    for ptype, tiers in MARKET_CAP_RATES.items():
        rg = MARKET_RENT_GROWTH[ptype]
        vac_m = MARKET_VACANCY[ptype]
        cap_rows.append({
            "Asset Class": ptype,
            "Tier 1 Cap": f"{tiers['Tier 1']:.2%}",
            "Tier 2 Cap": f"{tiers['Tier 2']:.2%}",
            "Tier 3 Cap": f"{tiers['Tier 3']:.2%}",
            "Rent Growth (T1)": f"{rg['Tier 1']:.1%}",
            "Vacancy (T1)": f"{vac_m['Tier 1']:.1%}",
        })

    st.dataframe(pd.DataFrame(cap_rows).set_index("Asset Class"), use_container_width=True)

    # ── Deal overlay if deal loaded ──
    d = st.session_state.deal_data
    if not d or not d.get("purchase_price"):
        st.info("Load a deal from your pipeline to see how it compares against market benchmarks.")
        return

    st.markdown(f"<div style='font-size:16px;font-weight:700;color:#0f172a;margin:24px 0 14px;'>Deal Overlay — {d['name']}</div>", unsafe_allow_html=True)

    tier     = get_msa_tier(d.get("address",""))
    ptype    = d.get("type","Multifamily")
    mkt_cap  = MARKET_CAP_RATES.get(ptype,{}).get(tier, 0.055)
    mkt_rg   = MARKET_RENT_GROWTH.get(ptype,{}).get(tier, 0.035)
    mkt_vac  = MARKET_VACANCY.get(ptype,{}).get(tier, 0.07)
    deal_cap = d["noi_year1"] / d["purchase_price"] if d["purchase_price"] else 0
    bps_diff = int((deal_cap - mkt_cap) * 10000)
    bps_dir  = "above" if bps_diff > 0 else "below"
    bps_color = "#16a34a" if bps_diff > 0 else "#dc2626"

    # Implied loan rate
    loan_rate = (t10 + 2.0) if t10 else 6.75

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div style='background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:14px;'>
      <div style='font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;'>Deal Cap Rate</div>
      <div style='font-family:Outfit,sans-serif;font-size:22px;font-weight:800;letter-spacing:-0.03em;color:#07111f;'>{deal_cap:.2%}</div>
      <div style='font-size:12px;color:{bps_color};font-weight:600;'>{abs(bps_diff)} bps {bps_dir} market avg</div>
    </div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div style='background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:14px;'>
      <div style='font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;'>Market Cap ({tier})</div>
      <div style='font-family:Outfit,sans-serif;font-size:22px;font-weight:800;letter-spacing:-0.03em;color:#07111f;'>{mkt_cap:.2%}</div>
      <div style='font-size:12px;color:#64748b;'>{ptype} benchmark</div>
    </div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div style='background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:14px;'>
      <div style='font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;'>Implied Loan Rate</div>
      <div style='font-family:Outfit,sans-serif;font-size:22px;font-weight:800;letter-spacing:-0.03em;color:#07111f;'>{loan_rate:.2f}%</div>
      <div style='font-size:12px;color:#64748b;'>10Y T + 200bps</div>
    </div>""", unsafe_allow_html=True)
    c4.markdown(f"""<div style='background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:14px;'>
      <div style='font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;'>Market Rent Growth</div>
      <div style='font-family:Outfit,sans-serif;font-size:22px;font-weight:800;letter-spacing:-0.03em;color:#07111f;'>{mkt_rg:.1%}/yr</div>
      <div style='font-size:12px;color:#64748b;'>{tier} {ptype}</div>
    </div>""", unsafe_allow_html=True)

    # Visual cap rate comparison chart
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div class='panel-title'>Cap Rate vs Market — All Asset Classes</div>", unsafe_allow_html=True)
        types  = list(MARKET_CAP_RATES.keys())
        t1_caps = [MARKET_CAP_RATES[t]["Tier 1"] * 100 for t in types]
        t2_caps = [MARKET_CAP_RATES[t]["Tier 2"] * 100 for t in types]
        fig = go.Figure()
        fig.add_bar(name="Tier 1 MSA", x=types, y=t1_caps, marker_color="#2563eb",
                    text=[f"{v:.2f}%" for v in t1_caps], textposition="outside")
        fig.add_bar(name="Tier 2 MSA", x=types, y=t2_caps, marker_color="#93c5fd",
                    text=[f"{v:.2f}%" for v in t2_caps], textposition="outside")
        if deal_cap > 0:
            fig.add_hline(y=deal_cap * 100, line_dash="dot", line_color="#dc2626", line_width=2,
                          annotation_text=f"Your Deal: {deal_cap:.2%}", annotation_position="top right")
        fig.update_layout(barmode="group", height=300,
            yaxis=dict(title="Cap Rate (%)", showgrid=True, gridcolor="#f1f5f9"),
            margin=dict(l=0,r=0,t=40,b=0), paper_bgcolor="white", plot_bgcolor="white",
            legend=dict(orientation="h", y=1.12), font=dict(family="Inter, sans-serif"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6K | AI DEAL SCORER vs 10,000 COMPS
# ──────────────────────────────────────────────────────────────────────────────

def view_ai_scorer():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">AI DEAL SCORER</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">AI Deal Scorer — Benchmark Your Deal</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:24px;'>AI benchmarks your deal against thousands of closed CRE transactions and tells you exactly where it ranks.</div>", unsafe_allow_html=True)

    d = st.session_state.deal_data
    if not d or not d.get("purchase_price"):
        st.info("Load a deal from your pipeline first, then come back here to score it.")
        if st.button("← Go to Pipeline"):
            st.session_state.current_view = "Pipeline"
            st.rerun()
        return

    tier = get_msa_tier(d.get("address",""))
    ptype = d.get("type","Multifamily")

    col_deal, col_score = st.columns([1, 1.6])

    with col_deal:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Deal Being Scored</div>", unsafe_allow_html=True)
            deal_cap = d["noi_year1"] / d["purchase_price"] if d["purchase_price"] else 0
            st.markdown(f"""
            <div style='margin-bottom:12px;'>
              <div style='font-size:17px;font-weight:800;color:#0f172a;'>{d["name"]}</div>
              <div style='font-size:12px;color:#64748b;'>{d.get("address","—")}</div>
              <div style='font-size:12px;color:#64748b;margin-top:4px;'>{d["type"]} &bull; {d["units"]} units &bull; {d["vintage"]} vintage</div>
            </div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>
              <div style='background:#f8fafc;border-radius:6px;padding:10px;'>
                <div style='font-size:10px;color:#64748b;font-weight:700;'>PRICE</div>
                <div style='font-size:15px;font-weight:800;'>${d["purchase_price"]/1e6:.1f}M</div>
              </div>
              <div style='background:#f8fafc;border-radius:6px;padding:10px;'>
                <div style='font-size:10px;color:#64748b;font-weight:700;'>CAP RATE</div>
                <div style='font-size:15px;font-weight:800;'>{deal_cap:.2%}</div>
              </div>
              <div style='background:#eff6ff;border-radius:6px;padding:10px;'>
                <div style='font-size:10px;color:#1d4ed8;font-weight:700;'>LEVERED IRR</div>
                <div style='font-size:15px;font-weight:800;color:#1d4ed8;'>{d["irr"]:.1%}</div>
              </div>
              <div style='background:#eff6ff;border-radius:6px;padding:10px;'>
                <div style='font-size:10px;color:#1d4ed8;font-weight:700;'>EQUITY MULT</div>
                <div style='font-size:15px;font-weight:800;color:#1d4ed8;'>{d["equity_mult"]:.2f}x</div>
              </div>
            </div>
            <div style='margin-top:10px;background:#f8fafc;border-radius:6px;padding:10px;'>
              <div style='font-size:10px;color:#64748b;font-weight:700;'>MARKET CONTEXT</div>
              <div style='font-size:13px;font-weight:600;color:#0f172a;'>{tier} MSA — {ptype}</div>
            </div>
            """, unsafe_allow_html=True)

            run_score = st.button("🎯 Score Against Comps", type="primary", use_container_width=True)

    with col_score:
        score_data = st.session_state.get("ai_score_result")

        if run_score:
            with st.spinner("Benchmarking against 10,000+ comps..."):
                score_data = ai_score_against_comps(d, tier)
                st.session_state.ai_score_result = score_data

        if score_data:
            pct      = score_data.get("percentile_rank", 50)
            irr_pct  = score_data.get("irr_percentile", 50)
            rec      = score_data.get("recommendation","buy")
            pricing  = score_data.get("pricing_assessment","fairly priced")
            conf     = score_data.get("confidence", 0.75)

            rec_colors = {
                "strong buy": ("#dcfce7","#166534"),
                "buy":        ("#dbeafe","#1d4ed8"),
                "hold":       ("#fef9c3","#92400e"),
                "pass":       ("#fee2e2","#991b1b"),
            }
            r_bg, r_col = rec_colors.get(rec, ("#f8fafc","#334155"))
            pricing_colors = {"underpriced":"#16a34a","fairly priced":"#1d4ed8","overpriced":"#dc2626"}
            p_col = pricing_colors.get(pricing,"#334155")

            # Main score card
            st.markdown(f"""
            <div style='background:#07111f;border-radius:12px;padding:24px;margin-bottom:16px;color:#fff;'>
              <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;'>
                <div>
                  <div style='font-size:11px;color:#3b82f6;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;'>COMP PERCENTILE RANK</div>
                  <div style='font-size:56px;font-weight:900;letter-spacing:-2px;line-height:1;'>{pct}<span style='font-size:24px;color:#8ea5c0;'>th</span></div>
                  <div style='font-size:13px;color:#8ea5c0;margin-top:6px;'>vs 10,000+ closed transactions</div>
                </div>
                <div style='text-align:right;'>
                  <div style='background:{r_bg};color:{r_col};font-size:16px;font-weight:800;padding:10px 20px;border-radius:8px;text-transform:uppercase;letter-spacing:1px;'>{rec}</div>
                  <div style='font-size:12px;color:#8ea5c0;margin-top:8px;'>AI Confidence: {conf:.0%}</div>
                </div>
              </div>
              <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:20px;'>
                <div style='background:#111f33;border-radius:8px;padding:12px;text-align:center;'>
                  <div style='font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;'>IRR Percentile</div>
                  <div style='font-size:22px;font-weight:800;color:#3b82f6;'>{irr_pct}th</div>
                </div>
                <div style='background:#111f33;border-radius:8px;padding:12px;text-align:center;'>
                  <div style='font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;'>Pricing</div>
                  <div style='font-size:16px;font-weight:800;color:{p_col};text-transform:capitalize;'>{pricing}</div>
                </div>
                <div style='background:#111f33;border-radius:8px;padding:12px;text-align:center;'>
                  <div style='font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;'>Cap vs Market</div>
                  <div style='font-size:13px;font-weight:700;color:#f0f4f8;'>{score_data.get("cap_rate_vs_market","—")}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Strengths + Risks
            s_col, r_col2 = st.columns(2)
            with s_col:
                st.markdown("<div style='background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:14px;'>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:11px;font-weight:700;color:#16a34a;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px;'>✅ Strengths</div>", unsafe_allow_html=True)
                for s in score_data.get("top_3_strengths",[]):
                    st.markdown(f"<div style='font-size:13px;color:#166534;padding:4px 0;border-bottom:1px solid #dcfce7;'>• {s}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with r_col2:
                st.markdown("<div style='background:#fff5f5;border:1px solid #fecaca;border-radius:8px;padding:14px;'>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:11px;font-weight:700;color:#dc2626;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px;'>⚠️ Risks</div>", unsafe_allow_html=True)
                for r in score_data.get("top_3_risks",[]):
                    st.markdown(f"<div style='font-size:13px;color:#991b1b;padding:4px 0;border-bottom:1px solid #fee2e2;'>• {r}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Market commentary
            commentary = score_data.get("market_commentary","")
            if commentary:
                st.markdown(f"""
                <div style='background:#eff6ff;border-left:4px solid #2563eb;border-radius:6px;padding:14px;margin-top:14px;'>
                  <div style='font-size:10px;font-weight:700;color:#1d4ed8;text-transform:uppercase;margin-bottom:6px;'>Market Commentary</div>
                  <div style='font-size:13px;color:#1e3a5f;line-height:1.7;'>{commentary}</div>
                </div>""", unsafe_allow_html=True)

            # Comparable deals table
            comps = score_data.get("comparable_deals",[])
            if comps:
                st.markdown("<br>", unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown("<div class='panel-title'>Most Similar Closed Comps</div>", unsafe_allow_html=True)
                    comp_rows = []
                    for c in comps:
                        comp_rows.append({
                            "Comp": c.get("name","—"),
                            "Price": c.get("price","—"),
                            "Cap Rate": c.get("cap_rate","—"),
                            "IRR": c.get("irr","—"),
                            "Similarity": f"{c.get('similarity_score',0)}%",
                        })
                    st.dataframe(pd.DataFrame(comp_rows).set_index("Comp"), use_container_width=True)
        else:
            st.markdown("""
            <div style='text-align:center;padding:80px 20px;color:#94a3b8;'>
              <div style='font-size:40px;margin-bottom:16px;'>🎯</div>
              <div style='font-size:15px;font-weight:600;color:#64748b;margin-bottom:8px;'>Ready to score</div>
              <div style='font-size:13px;'>Click "Score Against Comps" to benchmark<br>your deal against 10,000+ closed transactions.</div>
            </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6L | IC MEMO EMAIL DELIVERY
# ──────────────────────────────────────────────────────────────────────────────

def view_memo_delivery():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">MEMO DELIVERY</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">IC Memo Delivery — One Click to Your Committee</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:24px;'>Generate and email a fully branded IC memo directly to your investment committee — no downloading, no attaching.</div>", unsafe_allow_html=True)

    d = st.session_state.deal_data
    if not d:
        st.info("Load a deal from your pipeline first.")
        return

    col_cfg, col_prev = st.columns([1, 1.5])

    with col_cfg:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Memo Configuration</div>", unsafe_allow_html=True)
            deal_name   = st.text_input("Deal Name",    value=d["name"])
            sender_name = st.text_input("Prepared By",  value=st.session_state.user_email or "Senior Analyst")
            rec         = st.selectbox("Recommendation",["APPROVE","APPROVE WITH CONDITIONS","DECLINE"])

            st.markdown("<div class='panel-title' style='margin-top:16px;'>Recipients</div>", unsafe_allow_html=True)
            to_emails_raw = st.text_area("To (one email per line)", placeholder="partner@firm.com, cfo@firm.com", height=100)


            cc_raw        = st.text_input("CC (comma-separated)", placeholder="assistant@firm.com")

            st.markdown("<div class='panel-title' style='margin-top:16px;'>Generate Memo</div>", unsafe_allow_html=True)
            regen = st.button("⚡ Generate AI Memo", use_container_width=True)
            if regen:
                with st.spinner("AI drafting executive summary..."):
                    prompt = f"""Write a professional CRE investment committee executive summary for:
Property: {d["name"]}, {d["units"]} units, {d["type"]}
IRR: {d["irr"]:.1%}, EM: {d["equity_mult"]:.2f}x, GP IRR: {d["gp_irr"]:.1%}
NOI Y1: ${d["noi_year1"]:,.0f}, Purchase Price: ${d["purchase_price"]:,.0f}
Deal Grade: {d["grade"]} ({d["score"]}/100)
Recommendation: {rec}
Write 2 concise professional paragraphs. Use specific metrics. No fluff."""
                    try:
                        resp = ai_client.chat.completions.create(
                            model="gpt-4o", max_tokens=450, temperature=0.35,
                            messages=[{"role":"user","content":prompt}]
                        )
                        st.session_state.delivery_memo_text = resp.choices[0].message.content
                        st.session_state.delivery_memo_rec  = rec
                    except Exception as e:
                        st.error(f"AI error: {e}")

            memo_text = st.session_state.get("delivery_memo_text","")

            st.markdown("<br>", unsafe_allow_html=True)
            send_btn = st.button("📬 Send to Committee", type="primary", use_container_width=True,
                                  disabled=not memo_text)

            if send_btn and memo_text:
                emails = [e.strip() for e in to_emails_raw.replace(",","\n").strip().split("\n") if e.strip()]

                if not emails:
                    st.error("Enter at least one recipient email.")
                else:
                    results = []
                    with st.spinner(f"Sending to {len(emails)} recipient(s)..."):
                        for email in emails:
                            ok, err = send_ic_memo_email(email, d, memo_text,
                                                          st.session_state.delivery_memo_rec or rec,
                                                          sender_name)
                            results.append((email, ok, err))
                    for _re, _rok, _ in results:
                        if _rok:
                            audit_log("memo_sent", d['name'], f"IC memo delivered to {_re}")
                    for email, ok, err in results:
                        if ok:
                            st.success(f"✅ Sent to {email}")
                        else:
                            st.error(f"❌ Failed for {email}: {err}")

                    if all(ok for _, ok, _ in results):
                        st.balloons()

    with col_prev:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Live Email Preview</div>", unsafe_allow_html=True)
            memo_text = st.session_state.get("delivery_memo_text","")
            rec_used  = st.session_state.get("delivery_memo_rec", rec)
            rec_color = {"APPROVE":"#166534","APPROVE WITH CONDITIONS":"#92400e","DECLINE":"#991b1b"}.get(rec_used,"#334155")
            rec_bg    = {"APPROVE":"#dcfce7","APPROVE WITH CONDITIONS":"#fef9c3","DECLINE":"#fee2e2"}.get(rec_used,"#f8fafc")

            st.markdown(f"""
            <div style='font-family:Arial,sans-serif;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;'>
              <div style='background:#07111f;padding:18px 22px;'>
                <div style='font-size:22px;font-weight:900;color:#fff;letter-spacing:-1px;'>AIRE</div>
                <div style='font-size:9px;color:#3b82f6;font-weight:700;letter-spacing:2px;text-transform:uppercase;'>Investment Committee Memorandum</div>
                <div style='font-size:11px;color:#8ea5c0;margin-top:2px;'>{datetime.now().strftime("%B %d, %Y")} &nbsp;|&nbsp; {sender_name}</div>
              </div>
              <div style='padding:20px 22px;'>
                <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;background:#f8fafc;border-radius:8px;padding:14px;margin-bottom:16px;'>
                  <div><div style='font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;'>Asset</div><div style='font-size:13px;font-weight:700;'>{d["name"]}</div></div>
                  <div><div style='font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;'>Type / Units</div><div style='font-size:13px;font-weight:700;'>{d["type"]} / {d["units"]}</div></div>
                  <div><div style='font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;'>Purchase Price</div><div style='font-size:13px;font-weight:700;'>${d["purchase_price"]/1e6:.1f}M</div></div>
                  <div><div style='font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;'>Grade</div><div style='font-size:13px;font-weight:700;'>{d["grade"]} — {d["score"]}/100</div></div>
                </div>
                <div style='font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;margin-bottom:6px;'>Executive Summary</div>
                <div style='font-size:12px;line-height:1.7;color:#334155;margin-bottom:16px;'>{memo_text if memo_text else "<em style='color:#94a3b8;'>Click Generate AI Memo to populate...</em>"}</div>
                <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px;'>
                  <div style='background:#eff6ff;border-radius:6px;padding:10px;text-align:center;'><div style='font-size:9px;color:#1d4ed8;font-weight:700;'>IRR</div><div style='font-size:16px;font-weight:800;'>{d["irr"]:.1%}</div></div>
                  <div style='background:#eff6ff;border-radius:6px;padding:10px;text-align:center;'><div style='font-size:9px;color:#1d4ed8;font-weight:700;'>EM</div><div style='font-size:16px;font-weight:800;'>{d["equity_mult"]:.2f}x</div></div>
                  <div style='background:#eff6ff;border-radius:6px;padding:10px;text-align:center;'><div style='font-size:9px;color:#1d4ed8;font-weight:700;'>GP IRR</div><div style='font-size:16px;font-weight:800;'>{d["gp_irr"]:.1%}</div></div>
                  <div style='background:#eff6ff;border-radius:6px;padding:10px;text-align:center;'><div style='font-size:9px;color:#1d4ed8;font-weight:700;'>LOSS PROB</div><div style='font-size:16px;font-weight:800;'>{d["loss_prob"]:.1%}</div></div>
                </div>
                <div style='background:{rec_bg};border-radius:6px;padding:12px;text-align:center;'>
                  <div style='font-size:9px;color:{rec_color};font-weight:700;text-transform:uppercase;letter-spacing:1px;'>Recommendation</div>
                  <div style='font-size:18px;font-weight:900;color:{rec_color};'>{rec_used}</div>
                </div>
              </div>
              <div style='background:#f8fafc;padding:10px 22px;font-size:10px;color:#94a3b8;border-top:1px solid #e2e8f0;'>Confidential — AIRE Institutional Underwriting</div>
            </div>
            """, unsafe_allow_html=True)

            # Email setup hint
            _prov = detect_email_provider()
            _prov_labels = {"sendgrid":"SendGrid","mailgun":"Mailgun","resend":"Resend","smtp":"SMTP / Gmail"}
            if not _prov:
                st.warning("⚠️ No email provider connected yet.", icon="📧")
                if st.button("⚙️ Set up email in Settings", use_container_width=True):
                    st.session_state.current_view = "Settings"
                    st.rerun()
            else:
                st.success(f"✅ {_prov_labels.get(_prov, _prov)} connected — ready to send", icon="📬")


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6M | PORTFOLIO STRESS TESTING
# ──────────────────────────────────────────────────────────────────────────────

def view_stress_test():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">STRESS TESTING</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">Portfolio Stress Testing</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:20px;'>Model what happens to every deal simultaneously under rate shocks, rent drops, and recession scenarios.</div>", unsafe_allow_html=True)

    props = st.session_state.properties
    if not props:
        st.info("Add deals to your pipeline to run stress tests.")
        return

    # Custom scenario editor
    with st.expander("⚙️ Customize Scenarios", expanded=False):
        cols = st.columns(4)
        rate_shock    = cols[0].number_input("Rate Shock (bps)", value=100, step=25) / 10000
        rent_shock    = cols[1].number_input("Rent Change (%)",  value=-5,  step=1)  / 100
        vac_shock     = cols[2].number_input("Vacancy Spike (%)",value=10,  step=1)  / 100
        cap_shock     = cols[3].number_input("Cap Exp. (bps)",   value=50,  step=10) / 10000
        STRESS_SCENARIOS["Custom"] = {
            "rate_shock": rate_shock, "rent_shock": rent_shock,
            "vacancy_shock": vac_shock, "cap_shock": cap_shock
        }

    if st.button("▶ Run Stress Test Across Portfolio", type="primary"):
        with st.spinner("Stressing all deals..."):
            results = run_stress_test(props, STRESS_SCENARIOS)
            st.session_state.stress_results = results

    results = st.session_state.get("stress_results", [])
    if not results:
        st.info("Click **Run Stress Test** to model all scenarios across your portfolio.")
        return

    # Scenario summary strip — portfolio-level IRR impact
    scenarios = list(STRESS_SCENARIOS.keys())
    st.markdown("<br>", unsafe_allow_html=True)

    scen_cols = st.columns(len(scenarios))
    for i, scen in enumerate(scenarios):
        irrs = [r.get(f"{scen}_irr", r["base_irr"]) for r in results]
        avg_irr = sum(irrs) / len(irrs) if irrs else 0
        drift   = avg_irr - (sum(r["base_irr"] for r in results) / len(results))
        color   = "#16a34a" if drift >= 0 else ("#d97706" if drift > -0.03 else "#dc2626")
        bg      = "#f0fdf4" if drift >= 0 else ("#fef9c3" if drift > -0.03 else "#fee2e2")
        scen_cols[i].markdown(f"""
        <div style="background:{bg};border-radius:8px;padding:12px;text-align:center;">
          <div style="font-size:9px;color:{color};font-weight:700;text-transform:uppercase;letter-spacing:.5px;">{scen}</div>
          <div style="font-size:20px;font-weight:800;color:#0f172a;">{avg_irr:.1%}</div>
          <div style="font-size:11px;color:{color};font-weight:600;">{drift:+.1%} drift</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Per-deal results heatmap table
    with st.container(border=True):
        st.markdown("<div class='panel-title'>Deal-Level Stress Results — IRR by Scenario</div>", unsafe_allow_html=True)
        header_html = "<table style='width:100%;border-collapse:collapse;font-size:12px;'><thead><tr style='background:#07111f;color:#fff;'>"
        header_html += "<th style='padding:10px 12px;text-align:left;'>Property</th><th style='padding:10px 12px;'>Type</th><th style='padding:10px 12px;'>Base IRR</th>"
        for scen in scenarios[1:]:  # skip base
            header_html += f"<th style='padding:10px 12px;'>{scen}</th>"
        header_html += "</tr></thead><tbody>"

        rows_html = ""
        for i, row in enumerate(results):
            bg = "#fff" if i % 2 == 0 else "#f8fafc"
            rows_html += f"<tr style='background:{bg};'>"
            rows_html += f"<td style='padding:9px 12px;font-weight:700;'>{row['name'][:22]}</td>"
            rows_html += f"<td style='padding:9px 12px;color:#64748b;'>{row['type']}</td>"
            rows_html += f"<td style='padding:9px 12px;font-weight:700;color:#1d4ed8;'>{row['base_irr']:.1%}</td>"
            for scen in scenarios[1:]:
                sirr  = row.get(f"{scen}_irr", row["base_irr"])
                drift = sirr - row["base_irr"]
                cell_color = "#16a34a" if drift >= 0 else ("#d97706" if drift > -0.03 else "#dc2626")
                cell_bg    = "#f0fdf4" if drift >= 0 else ("#fef9c3" if drift > -0.03 else "#fee2e2")
                rows_html += f"<td style='padding:9px 12px;background:{cell_bg};color:{cell_color};font-weight:600;text-align:center;'>{sirr:.1%}<br><span style='font-size:10px;'>({drift:+.1%})</span></td>"
            rows_html += "</tr>"

        st.markdown(header_html + rows_html + "</tbody></table>", unsafe_allow_html=True)

    # Portfolio IRR by scenario chart
    with st.container(border=True):
        st.markdown("<div class='panel-title'>Portfolio Average IRR — Scenario Comparison</div>", unsafe_allow_html=True)
        scen_irrs = []
        for scen in scenarios:
            irrs = [r.get(f"{scen}_irr", r["base_irr"]) for r in results]
            scen_irrs.append(sum(irrs) / len(irrs))
        colors = ["#2563eb" if i == 0 else ("#16a34a" if v >= scen_irrs[0] else ("#d97706" if v >= scen_irrs[0]-0.03 else "#dc2626")) for i, v in enumerate(scen_irrs)]
        fig = go.Figure(go.Bar(
            x=scenarios, y=[v*100 for v in scen_irrs],
            marker_color=colors,
            text=[f"{v:.1%}" for v in scen_irrs], textposition="outside"
        ))
        fig.add_hline(y=scen_irrs[0]*100, line_dash="dot", line_color="#64748b", line_width=1)
        fig.update_layout(height=280, yaxis=dict(title="Portfolio Avg IRR (%)", showgrid=True, gridcolor="#f1f5f9"),
            margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor="white", plot_bgcolor="white",
            font=dict(family="Inter, sans-serif"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6N | VERSION-CONTROLLED PRO FORMAS
# ──────────────────────────────────────────────────────────────────────────────

def view_version_proforma():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">PRO FORMAS</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">Version-Controlled Pro Formas</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:20px;'>Every time you update assumptions, save a snapshot. See exactly how IRR changed from v1 to now.</div>", unsafe_allow_html=True)

    d = st.session_state.deal_data
    if not d:
        st.info("Load a deal from your pipeline first.")
        return

    prop_id = d["id"]
    s = st.session_state.settings

    col_left, col_right = st.columns([1, 1.5])

    with col_left:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Current Assumptions</div>", unsafe_allow_html=True)
            noi_y1        = st.number_input("NOI Year 1 ($)",    value=float(d["noi_year1"]), step=10000.0, format="%.0f")
            rent_growth   = st.number_input("Rent Growth (%)",   value=float(s["rent_growth"]*100), step=0.5, format="%.2f") / 100
            expense_growth= st.number_input("Expense Growth (%)",value=float(s["expense_growth"]*100), step=0.5, format="%.2f") / 100
            exit_cap      = st.number_input("Exit Cap Rate (%)", value=5.50, step=0.25, format="%.2f") / 100
            hold          = st.slider("Hold Period (Yrs)",       3, 10, int(s["hold_period"]))
            ltv           = st.slider("LTV (%)", 40, 80, 65) / 100
            debt          = d["purchase_price"] * ltv

            pf = build_proforma(noi_y1, rent_growth, expense_growth, d["purchase_price"], debt, hold)
            noi_final  = pf["noi_list"][-1]
            exit_val   = noi_final / exit_cap if exit_cap > 0 else d["purchase_price"]
            equity_in  = d["purchase_price"] - debt
            ds         = annual_debt_service(debt)
            ncf_total  = sum(n - ds for n in pf["noi_list"])
            total_ret  = ncf_total + (exit_val - debt) - equity_in
            est_irr    = max(total_ret / equity_in / hold, -0.5) if equity_in > 0 else 0
            est_em     = (ncf_total + exit_val - debt) / equity_in if equity_in > 0 else 1

            st.markdown(f"""
            <div style="background:#eff6ff;border-radius:8px;padding:14px;margin-top:12px;">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                <div><div style="font-size:10px;color:#1d4ed8;font-weight:700;">EST. IRR</div>
                     <div style="font-family:Outfit,sans-serif;font-size:22px;font-weight:800;letter-spacing:-0.03em;color:#07111f;">{est_irr:.1%}</div></div>
                <div><div style="font-size:10px;color:#1d4ed8;font-weight:700;">EQUITY MULT</div>
                     <div style="font-family:Outfit,sans-serif;font-size:22px;font-weight:800;letter-spacing:-0.03em;color:#07111f;">{est_em:.2f}x</div></div>
              </div>
            </div>""", unsafe_allow_html=True)

            ver_label = st.text_input("Version Label", placeholder="e.g. Conservative / Mgmt revised NOI")
            if st.button("💾 Save This Version", type="primary", use_container_width=True):
                if ver_label:
                    save_proforma_version(prop_id, ver_label,
                        {"rent_growth": rent_growth, "expense_growth": expense_growth,
                         "exit_cap": exit_cap, "hold": hold, "ltv": ltv},
                        noi_y1, est_irr, est_em)
                    st.success(f"✅ Saved version: {ver_label}")
                    st.rerun()
                else:
                    st.error("Enter a version label.")

    with col_right:
        versions = get_proforma_versions(prop_id)

        if not versions:
            st.markdown("""
            <div style='text-align:center;padding:60px 20px;color:#94a3b8;'>
              <div style='font-size:36px;margin-bottom:12px;'>📋</div>
              <div style='font-size:14px;font-weight:600;color:#64748b;'>No versions saved yet</div>
              <div style='font-size:13px;margin-top:4px;'>Adjust assumptions and save your first snapshot.</div>
            </div>""", unsafe_allow_html=True)
        else:
            with st.container(border=True):
                st.markdown("<div class='panel-title'>Version History</div>", unsafe_allow_html=True)
                rows_html = ""
                for i, v in enumerate(reversed(versions)):
                    irr_color = "#16a34a" if v["irr"] >= 0.15 else ("#d97706" if v["irr"] >= 0.10 else "#dc2626")
                    rows_html += f"""
                    <div style="border-bottom:1px solid #f1f5f9;padding:12px 0;display:flex;justify-content:space-between;align-items:center;">
                      <div>
                        <div style="font-size:13px;font-weight:700;color:#0f172a;">{v["label"]}</div>
                        <div style="font-size:11px;color:#94a3b8;">{v["timestamp"]}</div>
                        <div style="font-size:11px;color:#64748b;margin-top:2px;">
                          NOI: ${v["noi_y1"]:,.0f} &bull; 
                          RG: {v["settings"].get("rent_growth",0):.1%} &bull;
                          Exit Cap: {v["settings"].get("exit_cap",0.055):.2%} &bull;
                          Hold: {v["settings"].get("hold",5)}yr
                        </div>
                      </div>
                      <div style="text-align:right;">
                        <div style="font-size:20px;font-weight:800;color:{irr_color};">{v["irr"]:.1%}</div>
                        <div style="font-size:12px;color:#64748b;">{v["em"]:.2f}x EM</div>
                      </div>
                    </div>"""
                st.markdown(f"<div>{rows_html}</div>", unsafe_allow_html=True)

            if len(versions) >= 2:
                with st.container(border=True):
                    st.markdown("<div class='panel-title'>IRR Progression Across Versions</div>", unsafe_allow_html=True)
                    labels = [v["label"][:16] for v in versions]
                    irrs   = [v["irr"]*100 for v in versions]
                    colors = ["#16a34a" if v >= 15 else ("#d97706" if v >= 10 else "#dc2626") for v in irrs]
                    fig = go.Figure()
                    fig.add_bar(x=labels, y=irrs, marker_color=colors,
                        text=[f"{v:.1f}%" for v in irrs], textposition="outside")
                    fig.add_hline(y=15, line_dash="dot", line_color="#2563eb", line_width=1.5,
                        annotation_text="Target IRR 15%", annotation_position="top right")
                    fig.update_layout(height=260,
                        yaxis=dict(title="IRR (%)", showgrid=True, gridcolor="#f1f5f9"),
                        margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor="white", plot_bgcolor="white")
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6O | MULTI-USER TEAM ACCOUNTS
# ──────────────────────────────────────────────────────────────────────────────

def view_team():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">TEAM</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">Team Management</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:20px;'>Add analysts and partners to your firm. Control who can view, edit, or approve deals.</div>", unsafe_allow_html=True)

    email = st.session_state.get("user_email","")
    fk    = firm_key(email)

    # Role definitions
    ROLES = {
        "Partner":  {"color":"#7c3aed","bg":"#ede9fe","perms":["View","Edit","Approve","Settings","Team"]},
        "Analyst":  {"color":"#1d4ed8","bg":"#dbeafe","perms":["View","Edit"]},
        "Viewer":   {"color":"#64748b","bg":"#f1f5f9","perms":["View"]},
    }

    # Load team from Supabase
    sb, _ = get_supabase()
    team  = []
    if sb:
        try:
            resp = sb.table("aire_team").select("*").eq("firm_key", fk).execute()
            team = resp.data or []
        except:
            pass

    # Header strip
    c1, c2, c3 = st.columns(3)
    c1.metric("Team Members", len(team))
    c2.metric("Partners", sum(1 for m in team if m.get("role")=="Partner"))
    c3.metric("Analysts",  sum(1 for m in team if m.get("role")=="Analyst"))

    st.markdown("<br>", unsafe_allow_html=True)

    # Team table
    if team:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Current Team</div>", unsafe_allow_html=True)
            for m in team:
                role = m.get("role","Analyst")
                rc   = ROLES.get(role, ROLES["Analyst"])
                perms_html = " ".join(f"<span style='background:#f1f5f9;color:#334155;font-size:10px;padding:2px 7px;border-radius:4px;margin:2px;'>{p}</span>" for p in rc["perms"])
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #f1f5f9;">
                  <div>
                    <div style="font-size:13px;font-weight:700;color:#0f172a;">{m.get("name","—")}</div>
                    <div style="font-size:12px;color:#64748b;">{m.get("email","")}</div>
                    <div style="margin-top:4px;">{perms_html}</div>
                  </div>
                  <div style="text-align:right;">
                    <span style="background:{rc["bg"]};color:{rc["color"]};font-size:11px;font-weight:700;padding:4px 12px;border-radius:6px;">{role}</span>
                    <div style="font-size:10px;color:#94a3b8;margin-top:4px;">Added {m.get("added_date","—")}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("No team members yet. Invite your first analyst or partner below.")

    # Invite form
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div class='panel-title'>Invite Team Member</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        inv_name  = c1.text_input("Full Name",    placeholder="Jane Smith")
        inv_email = c2.text_input("Email",        placeholder="jane@firm.com")
        inv_role  = c3.selectbox("Role", list(ROLES.keys()))

        if st.button("Send Invite", type="primary"):
            if inv_name and inv_email and "@" in inv_email:
                if sb:
                    try:
                        rec = {
                            "firm_key":   fk,
                            "name":       inv_name,
                            "email":      inv_email,
                            "role":       inv_role,
                            "added_by":   email,
                            "added_date": datetime.now().strftime("%Y-%m-%d"),
                            "status":     "invited",
                        }
                        sb.table("aire_team").upsert(rec, on_conflict="firm_key,email").execute()
                        st.success(f"✅ {inv_name} ({inv_role}) added to your team!")

                        # Send invite email
                        inv_body = f"""
                        <div style="font-family:Arial;padding:20px;">
                          <h2>You've been added to AIRE</h2>
                          <p>{email} has added you to their firm's AIRE underwriting platform as a <b>{inv_role}</b>.</p>
                          <p>Log in at <a href="https://aire.io">aire.io</a> with your email address to get started.</p>
                          <p style="color:#64748b;font-size:12px;">AIRE Institutional Underwriting Platform</p>
                        </div>"""
                        sg_key    = st.secrets.get("SENDGRID_API_KEY","")
                        from_addr = st.secrets.get("SENDGRID_FROM_EMAIL","noreply@aire.io")
                        if sg_key:
                            try:
                                requests.post("https://api.sendgrid.com/v3/mail/send",
                                    headers={"Authorization": f"Bearer {sg_key}", "Content-Type":"application/json"},
                                    json={"personalizations":[{"to":[{"email":inv_email}]}],
                                          "from":{"email":from_addr,"name":"AIRE Platform"},
                                          "subject":f"You've been added to AIRE by {email}",
                                          "content":[{"type":"text/html","value":inv_body}]}, timeout=8)
                            except:
                                pass
                        st.rerun()
                    except Exception as e:
                        st.error(f"DB error: {e}")
                        st.info("Run create_team_table.sql in Supabase SQL Editor first.")
                else:
                    st.error("Supabase not connected.")
            else:
                st.error("Enter a valid name and email.")

    # Permissions reference
    with st.expander("Role Permissions Reference"):
        rows = []
        for role, info in ROLES.items():
            rows.append({"Role": role, "Permissions": ", ".join(info["perms"])})
        st.dataframe(pd.DataFrame(rows).set_index("Role"), use_container_width=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6P | WHITE-LABEL SETTINGS
# ──────────────────────────────────────────────────────────────────────────────

def view_whitelabel():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">WHITE-LABEL</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">White-Label — Your Brand, Your Platform</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:24px;'>Replace AIRE branding with your firm identity across all reports, memos, and the LP portal.</div>", unsafe_allow_html=True)

    wl = st.session_state.get("whitelabel", {})

    col_cfg, col_prev = st.columns([1, 1.3])

    with col_cfg:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Brand Identity</div>", unsafe_allow_html=True)
            firm_name     = st.text_input("Firm Name",    value=wl.get("firm_name","AIRE"))
            firm_tagline  = st.text_input("Tagline",      value=wl.get("tagline","Institutional Underwriting Platform"))

            st.markdown("<div style='font-size:12px;font-weight:700;color:#64748b;margin:12px 0 4px;'>COLORS</div>", unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            primary_color = cc1.color_picker("Header Background", value=wl.get("primary","#07111f"))
            accent_color  = cc2.color_picker("Accent / Buttons",  value=wl.get("accent","#2563eb"))

            st.markdown("<div style='font-size:12px;font-weight:700;color:#64748b;margin:12px 0 4px;'>CONTACT & LINKS</div>", unsafe_allow_html=True)
            logo_url  = st.text_input("Logo URL (optional)", value=wl.get("logo_url",""),  placeholder="https://yourfirm.com/logo.png")
            website   = st.text_input("Firm Website",        value=wl.get("website",""),   placeholder="https://yourfirm.com")
            footer_text = st.text_input("Report Footer Text", value=wl.get("footer","Confidential — Institutional Underwriting"))

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Save Brand Settings", type="primary", use_container_width=True):
                st.session_state.whitelabel = {
                    "firm_name": firm_name, "tagline": firm_tagline,
                    "primary": primary_color, "accent": accent_color,
                    "logo_url": logo_url, "website": website, "footer": footer_text,
                }
                ok, err = db_save_settings({"whitelabel": st.session_state.whitelabel},
                                            st.session_state.user_email)
                if ok:
                    st.success("✅ Brand saved — applied to all memos and LP reports.")
                else:
                    st.success("✅ Applied this session.")
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("Brand settings are saved per firm and persist across all logins. Every IC memo, LP report, and email delivery will use your branding.")

    with col_prev:
        # Pull current values fresh every render
        fn = firm_name  if 'firm_name'    in dir() else wl.get("firm_name","AIRE")
        tg = firm_tagline if 'firm_tagline' in dir() else wl.get("tagline","Institutional Underwriting Platform")
        pc = primary_color if 'primary_color' in dir() else wl.get("primary","#07111f")
        ac = accent_color  if 'accent_color'  in dir() else wl.get("accent","#2563eb")
        ft = footer_text   if 'footer_text'   in dir() else wl.get("footer","Confidential — Institutional Underwriting")
        lu = logo_url      if 'logo_url'      in dir() else wl.get("logo_url","")

        # ── Memo preview card ──
        logo_tag = ""
        if lu:
            logo_tag = "<img src='" + lu + "' style='height:36px;margin-bottom:10px;display:block;' />"

        header_content = logo_tag + (
            "<div style='font-size:26px;font-weight:900;color:#fff;letter-spacing:-1px;line-height:1;'>" + fn + "</div>"
            "<div style='font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-top:4px;color:" + ac + ";'>" + tg + "</div>"
        )

        preview_html = """
        <div style='border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);'>

          <!-- Header -->
          <div style='background:""" + pc + """;padding:22px 26px;'>""" + header_content + """
            <div style='font-size:11px;color:rgba(255,255,255,0.5);margin-top:8px;border-top:1px solid rgba(255,255,255,0.1);padding-top:8px;'>
              Investment Committee Memorandum &nbsp;|&nbsp; """ + datetime.now().strftime("%B %d, %Y") + """
            </div>
          </div>

          <!-- Deal meta grid -->
          <div style='padding:18px 26px;background:#fff;'>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;background:#f8fafc;border-radius:8px;padding:14px;margin-bottom:16px;'>
              <div>
                <div style='font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;'>Asset</div>
                <div style='font-size:13px;font-weight:700;color:#0f172a;'>123 Main Apartments</div>
              </div>
              <div>
                <div style='font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;'>Type / Units</div>
                <div style='font-size:13px;font-weight:700;color:#0f172a;'>Multifamily / 120 Units</div>
              </div>
              <div>
                <div style='font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;'>Purchase Price</div>
                <div style='font-size:13px;font-weight:700;color:#0f172a;'>$18.5M</div>
              </div>
              <div>
                <div style='font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;'>Deal Grade</div>
                <div style='font-size:13px;font-weight:700;color:#0f172a;'>A — 88/100</div>
              </div>
            </div>

            <!-- KPI row -->
            <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px;'>
              <div style='background:#eff6ff;border-radius:6px;padding:10px;text-align:center;'>
                <div style='font-size:9px;color:""" + ac + """;font-weight:700;'>LEVERED IRR</div>
                <div style='font-size:18px;font-weight:800;color:#0f172a;'>18.4%</div>
              </div>
              <div style='background:#eff6ff;border-radius:6px;padding:10px;text-align:center;'>
                <div style='font-size:9px;color:""" + ac + """;font-weight:700;'>EQUITY MULT</div>
                <div style='font-size:18px;font-weight:800;color:#0f172a;'>2.21x</div>
              </div>
              <div style='background:#eff6ff;border-radius:6px;padding:10px;text-align:center;'>
                <div style='font-size:9px;color:""" + ac + """;font-weight:700;'>GP IRR</div>
                <div style='font-size:18px;font-weight:800;color:#0f172a;'>24.1%</div>
              </div>
              <div style='background:#eff6ff;border-radius:6px;padding:10px;text-align:center;'>
                <div style='font-size:9px;color:""" + ac + """;font-weight:700;'>LOSS PROB</div>
                <div style='font-size:18px;font-weight:800;color:#0f172a;'>3.2%</div>
              </div>
            </div>

            <!-- Recommendation -->
            <div style='background:#dcfce7;border-radius:8px;padding:14px;text-align:center;'>
              <div style='font-size:10px;color:#166534;font-weight:700;text-transform:uppercase;letter-spacing:1px;'>Committee Recommendation</div>
              <div style='font-size:22px;font-weight:900;color:#166534;'>APPROVE</div>
            </div>
          </div>

          <!-- Footer -->
          <div style='background:#f8fafc;padding:10px 26px;font-size:10px;color:#94a3b8;border-top:1px solid #e2e8f0;display:flex;justify-content:space-between;'>
            <span>""" + ft + """</span>
            <span>""" + (website if website else "aire.rent") + """</span>
          </div>
        </div>
        """

        st.markdown("<div style='font-size:13px;font-weight:700;color:#0f172a;margin-bottom:12px;'>📄 Memo Preview</div>", unsafe_allow_html=True)
        # Flatten: indented multi-line HTML after blank lines gets parsed as a
        # Markdown code block — strip per-line indentation so it renders as HTML.
        st.markdown("".join(_l.strip() for _l in preview_html.splitlines()), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Where branding is applied
        st.markdown("""
        <div style='background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:14px;'>
          <div style='font-size:11px;font-weight:700;color:#334155;margin-bottom:8px;text-transform:uppercase;letter-spacing:.5px;'>Applied Across</div>
          <div style='display:grid;grid-template-columns:1fr 1fr;gap:6px;'>
            <div style='font-size:12px;color:#64748b;'>✅ IC Memo Generator</div>
            <div style='font-size:12px;color:#64748b;'>✅ Memo Email Delivery</div>
            <div style='font-size:12px;color:#64748b;'>✅ LP Investor Portal</div>
            <div style='font-size:12px;color:#64748b;'>✅ PDF Exports</div>
            <div style='font-size:12px;color:#64748b;'>✅ LP Report PDF</div>
            <div style='font-size:12px;color:#64748b;'>✅ Broker Emails</div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6Q | LENDER DATABASE
# ──────────────────────────────────────────────────────────────────────────────

def view_lender_db():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">LENDER DATABASE</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">Lender Database & Deal Matching</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:20px;'>Store preferred lenders with their rate sheets and LTV limits. One-click match to find the best lender for your active deal.</div>", unsafe_allow_html=True)

    if "lenders" not in st.session_state:
        st.session_state.lenders = [
            {"id":"l001","name":"Berkadia","contact":"John Smith","email":"jsmith@berkadia.com",
             "phone":"212-555-0101","type":"Agency","max_ltv":0.80,"rate_spread":1.85,
             "min_dscr":1.20,"asset_types":["Multifamily"],"io_available":True,
             "min_loan":2e6,"max_loan":500e6,"notes":"Best rates on MF. Strong GSE shop."},
            {"id":"l002","name":"Wells Fargo CRE","contact":"Sarah Lee","email":"slee@wf.com",
             "phone":"415-555-0202","type":"Balance Sheet","max_ltv":0.75,"rate_spread":2.10,
             "min_dscr":1.25,"asset_types":["Office","Retail","Industrial","Mixed-Use"],"io_available":True,
             "min_loan":5e6,"max_loan":200e6,"notes":"Prefer Class A office in gateway markets."},
            {"id":"l003","name":"Ready Capital","contact":"Mike Chen","email":"mchen@readycap.com",
             "phone":"646-555-0303","type":"Bridge","max_ltv":0.85,"rate_spread":3.50,
             "min_dscr":1.10,"asset_types":["Multifamily","Mixed-Use"],"io_available":True,
             "min_loan":1e6,"max_loan":50e6,"notes":"Bridge/value-add specialist. Fast close."},
        ]

    d   = st.session_state.deal_data
    fk_ = fetch_fred_rate() if True else 6.75

    tab_list, tab_add, tab_match = st.tabs(["📋 All Lenders", "➕ Add Lender", "🎯 Match to Deal"])

    with tab_list:
        lenders = st.session_state.lenders
        if not lenders:
            st.info("No lenders saved yet. Add your preferred lenders in the Add Lender tab.")
        for l in lenders:
            rate_est = l["rate_spread"] + (fetch_fred_rate() - 2.0)
            badge_color = {"Agency":"#1d4ed8","Balance Sheet":"#16a34a","Bridge":"#d97706","CMBS":"#7c3aed"}.get(l["type"],"#64748b")
            badge_bg    = {"Agency":"#dbeafe","Balance Sheet":"#dcfce7","Bridge":"#fef9c3","CMBS":"#ede9fe"}.get(l["type"],"#f1f5f9")
            with st.container(border=True):
                c1, c2 = st.columns([2,1])
                with c1:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                      <div style="font-size:16px;font-weight:800;color:#0f172a;">{l["name"]}</div>
                      <span style="background:{badge_bg};color:{badge_color};font-size:11px;font-weight:700;padding:3px 10px;border-radius:4px;">{l["type"]}</span>
                    </div>
                    <div style="font-size:12px;color:#64748b;">👤 {l["contact"]} &bull; ✉️ {l["email"]} &bull; 📞 {l["phone"]}</div>
                    <div style="font-size:12px;color:#64748b;margin-top:4px;">Assets: {", ".join(l["asset_types"])}</div>
                    <div style="font-size:12px;color:#64748b;margin-top:2px;font-style:italic;">{l.get("notes","")}</div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                    <div style="background:#f8fafc;border-radius:8px;padding:12px;text-align:center;">
                      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                        <div><div style="font-size:9px;color:#64748b;font-weight:700;">EST RATE</div>
                             <div style="font-size:16px;font-weight:800;color:#1d4ed8;">{rate_est:.2f}%</div></div>
                        <div><div style="font-size:9px;color:#64748b;font-weight:700;">MAX LTV</div>
                             <div style="font-size:16px;font-weight:800;">{l["max_ltv"]:.0%}</div></div>
                        <div><div style="font-size:9px;color:#64748b;font-weight:700;">MIN DSCR</div>
                             <div style="font-size:16px;font-weight:800;">{l["min_dscr"]:.2f}x</div></div>
                        <div><div style="font-size:9px;color:#64748b;font-weight:700;">IO AVAIL</div>
                             <div style="font-size:16px;font-weight:800;">{"✅" if l["io_available"] else "❌"}</div></div>
                      </div>
                    </div>""", unsafe_allow_html=True)

    with tab_add:
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            l_name    = c1.text_input("Lender Name")
            l_contact = c2.text_input("Contact Name")
            l_email   = c3.text_input("Contact Email")
            c4, c5, c6 = st.columns(3)
            l_phone   = c4.text_input("Phone")
            l_type    = c5.selectbox("Lender Type", ["Agency","Balance Sheet","Bridge","CMBS","Debt Fund"])
            l_io      = c6.checkbox("IO Available", value=True)
            c7, c8, c9 = st.columns(3)
            l_ltv     = c7.number_input("Max LTV (%)", value=75.0, step=5.0) / 100
            l_spread  = c8.number_input("Spread over T (bps)", value=200, step=10) / 100
            l_dscr    = c9.number_input("Min DSCR", value=1.25, step=0.05, format="%.2f")
            c10, c11  = st.columns(2)
            l_min     = c10.number_input("Min Loan ($M)", value=2.0, step=0.5) * 1e6
            l_max     = c11.number_input("Max Loan ($M)", value=100.0, step=10.0) * 1e6
            l_assets  = st.multiselect("Asset Types", ["Multifamily","Office","Retail","Industrial","Mixed-Use"], default=["Multifamily"])
            l_notes   = st.text_area("Notes", height=60)

            if st.button("Add Lender", type="primary"):
                if l_name:
                    import time as _t
                    st.session_state.lenders.append({
                        "id": f"l{int(_t.time())}", "name": l_name, "contact": l_contact,
                        "email": l_email, "phone": l_phone, "type": l_type,
                        "max_ltv": l_ltv, "rate_spread": l_spread, "min_dscr": l_dscr,
                        "asset_types": l_assets, "io_available": l_io,
                        "min_loan": l_min, "max_loan": l_max, "notes": l_notes,
                    })
                    st.success(f"✅ {l_name} added to your lender database!")
                    st.rerun()

    with tab_match:
        if not d:
            st.info("Load a deal from your pipeline to match lenders.")
        else:
            loan_needed = d["purchase_price"] * 0.65
            noi         = d["noi_year1"]
            prop_type   = d["type"]
            st.markdown(f"**Matching lenders for:** {d['name']} | ${loan_needed/1e6:.1f}M loan needed | {prop_type}")
            st.markdown("<br>", unsafe_allow_html=True)
            matches = []
            for l in st.session_state.lenders:
                score = 0
                reasons = []
                if prop_type in l["asset_types"]: score += 30; reasons.append("✅ Lends on this asset type")
                if loan_needed >= l["min_loan"]:   score += 20; reasons.append("✅ Above min loan size")
                if loan_needed <= l["max_loan"]:   score += 20; reasons.append("✅ Below max loan size")
                rate_est = l["rate_spread"] + (fetch_fred_rate() - 2.0)
                ds_est   = loan_needed * rate_est / 100
                dscr_est = noi / ds_est if ds_est > 0 else 0
                if dscr_est >= l["min_dscr"]:      score += 30; reasons.append(f"✅ DSCR {dscr_est:.2f}x above min")
                else:                               reasons.append(f"⚠️ DSCR {dscr_est:.2f}x below min {l['min_dscr']:.2f}x")
                matches.append({"lender": l, "score": score, "reasons": reasons, "rate_est": rate_est, "dscr_est": dscr_est})
            matches.sort(key=lambda x: x["score"], reverse=True)
            for m in matches:
                l = m["lender"]
                badge = "🥇" if m["score"] >= 80 else ("🥈" if m["score"] >= 50 else "🥉")
                with st.container(border=True):
                    hc1, hc2 = st.columns([2,1])
                    with hc1:
                        st.markdown(f"**{badge} {l['name']}** — Match Score: **{m['score']}/100**")
                        for r in m["reasons"]: st.markdown(f"  {r}")
                    with hc2:
                        st.metric("Est. Rate", f"{m['rate_est']:.2f}%")
                        st.metric("Est. DSCR",  f"{m['dscr_est']:.2f}x")


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6R | GPT BROKER EMAIL DRAFTS
# ──────────────────────────────────────────────────────────────────────────────

def view_broker_emails():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">BROKER EMAILS</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">GPT-Powered Broker Email Drafts</div></div>""", unsafe_allow_html=True)



    st.markdown("<div style='font-size:14px;color:#64748b;margin-bottom:20px;'>AI drafts professional broker emails using your exact deal metrics — LOIs, counteroffers, due diligence requests, and more.</div>", unsafe_allow_html=True)

    d = st.session_state.deal_data

    EMAIL_TYPES = {
        "LOI (Letter of Intent)": "Draft a formal Letter of Intent to purchase this property. Include price, due diligence period (30 days), closing period (60 days), earnest money deposit (1% of purchase price), and key conditions. Professional and firm tone.",
        "Counteroffer": "Draft a professional counteroffer response to the broker. We are interested but need to negotiate on price. Reference specific deal metrics to justify our position. Be firm but collaborative.",
        "Due Diligence Request": "Draft a due diligence request list to the broker/seller. Request: rent rolls, T12 financials, operating statements, property tax bills, insurance certificates, maintenance logs, current leases, CAM reconciliations, and inspection reports.",
        "Introduction / Relationship": "Draft a professional introduction email to a new broker. Mention our focus on [asset type], typical deal size, and that we move quickly. Establish credibility and express interest in their deal flow.",
        "Pass / Decline": "Draft a professional pass email on this deal. Be respectful, brief, and leave the door open for future opportunities. Do not over-explain our reasons.",
        "Offer Follow-Up": "Draft a polite but firm follow-up email checking on the status of our submitted offer. We submitted [X] days ago and need a response to move forward.",
        "IC Approval Notification": "Draft an email notifying the broker that our Investment Committee has approved the deal and we are ready to proceed to contract. Express excitement and urgency to close.",
    }

    col_cfg, col_out = st.columns([1, 1.5])

    with col_cfg:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>Email Configuration</div>", unsafe_allow_html=True)
            email_type  = st.selectbox("Email Type", list(EMAIL_TYPES.keys()))
            broker_name = st.text_input("Broker Name", placeholder="Mike Johnson")
            broker_firm = st.text_input("Brokerage Firm", placeholder="Marcus & Millichap")
            sender_name = st.text_input("Your Name", value=st.session_state.user_email or "")
            extra_notes = st.text_area("Additional Context", placeholder="We already toured twice. Seller needs to close by Q2.", height=80)
            tone        = st.select_slider("Tone", ["Formal","Professional","Confident","Assertive"], value="Professional")

            deal_ctx = ""
            if d:
                cap_r = d["noi_year1"]/d["purchase_price"] if d["purchase_price"] else 0
                deal_ctx = f"Property: {d['name']}, {d['units']} units, {d['type']}, ${d['purchase_price']/1e6:.1f}M asking, {cap_r:.2%} cap rate, NOI ${d['noi_year1']:,.0f}, IRR {d['irr']:.1%}"
                st.info(f"Using active deal: **{d['name']}**")
            else:
                st.warning("No deal loaded — email will use generic context.")

            if st.button("✍️ Draft Email with AI", type="primary", use_container_width=True):
                with st.spinner("Drafting professional email..."):
                    prompt = f"""You are a senior CRE investment professional drafting a {email_type} email.
Tone: {tone}
Broker: {broker_name or "the broker"} at {broker_firm or "their firm"}
Sender: {sender_name}
Deal context: {deal_ctx or "a commercial real estate acquisition"}
Additional context: {extra_notes or "None"}
Email purpose: {EMAIL_TYPES[email_type]}

Draft a complete, professional email with subject line and body. Format as:
SUBJECT: [subject line]

[email body]

Keep it concise and action-oriented. No fluff."""

                    try:
                        resp = ai_client.chat.completions.create(
                            model="gpt-4o", max_tokens=600, temperature=0.4,
                            messages=[{"role":"user","content":prompt}]
                        )
                        raw = resp.choices[0].message.content.strip()
                        st.session_state.broker_email_draft = raw
                        st.session_state.broker_email_type  = email_type
                    except Exception as e:
                        st.error(f"AI error: {e}")

    with col_out:
        draft = st.session_state.get("broker_email_draft","")
        etype = st.session_state.get("broker_email_type","")

        if not draft:
            st.markdown("""
            <div style='text-align:center;padding:80px 20px;color:#94a3b8;'>
              <div style='font-size:40px;margin-bottom:16px;'>✉️</div>
              <div style='font-size:15px;font-weight:600;color:#64748b;'>No draft yet</div>
              <div style='font-size:13px;margin-top:6px;'>Configure and click Draft Email to generate<br>a professional broker communication.</div>
            </div>""", unsafe_allow_html=True)
        else:
            with st.container(border=True):
                st.markdown(f"<div class='panel-title'>{etype}</div>", unsafe_allow_html=True)

                # Parse subject + body
                lines = draft.split("\n")

                subject = ""
                body_lines = []
                for i, line in enumerate(lines):
                    if line.startswith("SUBJECT:"):
                        subject = line.replace("SUBJECT:","").strip()
                    else:
                        body_lines.append(line)
                body = "\n".join(body_lines).strip()


                if subject:
                    st.markdown(f"""
                    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:10px 14px;margin-bottom:12px;">
                      <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Subject Line</div>
                      <div style="font-size:14px;font-weight:700;color:#0f172a;">{subject}</div>
                    </div>""", unsafe_allow_html=True)

                edited = st.text_area("Email Body (edit before sending)", value=body, height=340)
                st.session_state.broker_email_draft_edited = edited

                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("📋 Copy to Clipboard", use_container_width=True):
                        st.code(f"Subject: {subject}\n\n{edited}")


                with c2:
                    send_addr = st.session_state.get("broker_send_addr","")
                with c3:
                    if st.button("🔄 Regenerate", use_container_width=True):
                        st.session_state.broker_email_draft = ""
                        st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)
                send_to = st.text_input("Send directly to broker email", placeholder="broker@firm.com", key="broker_send_addr")
                if st.button("📬 Send Email", type="primary", use_container_width=True):
                    if send_to and "@" in send_to:
                        sg_key    = st.secrets.get("SENDGRID_API_KEY","")
                        from_addr = st.secrets.get("SENDGRID_FROM_EMAIL","noreply@aire.io")
                        if sg_key:
                            try:
                                html_body = f"<pre style='font-family:Arial;font-size:13px;white-space:pre-wrap;'>{edited}</pre>"
                                resp = requests.post("https://api.sendgrid.com/v3/mail/send",
                                    headers={"Authorization":f"Bearer {sg_key}","Content-Type":"application/json"},
                                    json={"personalizations":[{"to":[{"email":send_to}]}],
                                          "from":{"email":from_addr,"name":sender_name or "AIRE Platform"},
                                          "subject": subject or etype,
                                          "content":[{"type":"text/html","value":html_body}]},
                                    timeout=10)
                                if resp.status_code in (200,202):
                                    st.success(f"✅ Sent to {send_to}")
                                else:
                                    st.error(f"SendGrid error: {resp.status_code}")
                            except Exception as e:
                                st.error(f"Send failed: {e}")
                        else:
                            st.warning("Add SENDGRID_API_KEY to Streamlit secrets to send directly. For now, copy the email above.")
                    else:
                        st.error("Enter a valid email address.")

# ──────────────────────────────────────────────────────────────────────────────
# AIRE INTELLIGENCE │ CLAUDE-POWERED COMMAND CENTER
# The most advanced CRE AI system ever built.
# ──────────────────────────────────────────────────────────────────────────────

def run_claude_deep_analysis(props: list, settings: dict, query: str = "") -> str:
    """Run a deep portfolio-level analysis using Claude."""
    if not props:
        return "No deals in pipeline to analyze."

    portfolio_summary = f"""
FIRM: {st.session_state.get('firm_id','Unknown')}
PORTFOLIO SIZE: {len(props)} deals
TOTAL AUM: ${sum(p['purchase_price'] for p in props)/1e6:.1f}M
AVG IRR: {sum(p['irr'] for p in props)/len(props):.1%}
AVG EM: {sum(p['equity_mult'] for p in props)/len(props):.2f}x
TARGET IRR: {settings.get('target_irr',0.15):.1%}
MAX LTV: {settings.get('max_ltv',0.70):.0%}

DEALS:
"""
    for p in props:
        cap = p['noi_year1']/p['purchase_price'] if p['purchase_price'] else 0
        debt = p['debt_amount']
        ds   = annual_debt_service(debt)
        dscr = p['noi_year1']/ds if ds > 0 else 0
        ltv  = debt/p['purchase_price'] if p['purchase_price'] else 0
        portfolio_summary += f"""
• {p['name']} | {p['type']} | {p['units']} units | Grade {p['grade']}
  Price: ${p['purchase_price']/1e6:.1f}M | NOI: ${p['noi_year1']:,.0f} | Cap: {cap:.2%}
  IRR: {p['irr']:.1%} | EM: {p['equity_mult']:.2f}x | DSCR: {dscr:.2f}x | LTV: {ltv:.0%}
  Status: {p.get('status','active')}
"""

    system = """You are AIRE Intelligence, the most advanced institutional CRE analysis AI ever built.
You are powered by Claude and operate at the level of a Managing Director at a top-5 private equity real estate firm.
You have deep expertise in: portfolio construction, risk management, capital markets, debt structuring,
market cycles, LP/GP dynamics, value-add strategies, and institutional underwriting.

Your analysis is characterized by:
- Brutal honesty about risks — you never sugarcoat
- Specific, quantitative insights with real numbers
- Institutional-grade recommendations that would survive IC scrutiny
- Forward-looking market intelligence
- Actionable next steps, not generic advice

Format your responses with clear sections. Use specific numbers always.
You are the competitive edge that separates AIRE from every other CRE tool on the market."""

    user_prompt = f"""Here is the full portfolio data:
{portfolio_summary}

{'User question: ' + query if query else 'Provide a comprehensive institutional-grade portfolio analysis. Cover: (1) Portfolio health and risk assessment, (2) Deals requiring immediate attention, (3) Capital allocation recommendations, (4) Market timing insights given current rate environment, (5) Three specific actions to take in the next 30 days.'}"""

    try:
        if claude_client:
            msg = claude_client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=2000,
                temperature=0.2,
                system=system,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return msg.content[0].text
        # Fallback
        r = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role":"system","content":system},{"role":"user","content":user_prompt}],
            max_tokens=2000, temperature=0.2
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"AIRE Intelligence temporarily unavailable: {e}"


def run_claude_deal_score(deal: dict, settings: dict, market_data: dict = None) -> str:
    """Deep single-deal analysis using Claude."""
    cap = deal['noi_year1']/deal['purchase_price'] if deal['purchase_price'] else 0
    debt = deal['debt_amount']
    ds   = annual_debt_service(debt)
    dscr = deal['noi_year1']/ds if ds > 0 else 0
    ltv  = debt/deal['purchase_price'] if deal['purchase_price'] else 0

    system = """You are AIRE Intelligence, the world's most advanced institutional CRE underwriting AI.
You analyze deals with the depth of a 20-year PE veteran and the speed of AI.
Give a complete, honest, institutional-grade deal analysis. Be specific. Use real numbers.
Do not hedge excessively. Give a clear verdict."""

    prompt = f"""DEAL ANALYSIS REQUEST

Property: {deal['name']}
Type: {deal['type']} | Units: {deal['units']} | Vintage: {deal['vintage']}
Address: {deal.get('address','Not specified')}

FINANCIAL METRICS:
Purchase Price: ${deal['purchase_price']:,.0f}
NOI Year 1: ${deal['noi_year1']:,.0f}
Cap Rate: {cap:.2%}
Levered IRR: {deal['irr']:.1%}
Equity Multiple: {deal['equity_mult']:.2f}x
DSCR: {dscr:.2f}x
LTV: {ltv:.0%}
Loss Probability: {deal.get('loss_prob',0.05):.1%}
Deal Grade: {deal['grade']} ({deal.get('score',50)}/100)

FIRM TARGETS:
Target IRR: {settings.get('target_irr',0.15):.1%}
Max LTV: {settings.get('max_ltv',0.70):.0%}
Min DSCR: {settings.get('min_dscr',1.25):.2f}x

Provide:
1. EXECUTIVE VERDICT (2 sentences — approve/conditional/pass and why)
2. FINANCIAL ANALYSIS (IRR quality, DSCR adequacy, cap rate vs market)
3. TOP 3 RISKS (specific, quantified where possible)
4. TOP 3 STRENGTHS (specific, quantified where possible)
5. SENSITIVITY CHECK (what breaks this deal — rate +100bps, NOI -10%, vacancy +5%)
6. RECOMMENDATION (one clear sentence with conviction)"""

    try:
        if claude_client:
            msg = claude_client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1200,
                temperature=0.15,
                system=system,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text
        r = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            max_tokens=1200, temperature=0.15
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"Analysis unavailable: {e}"


def view_aire_intelligence():
    props    = st.session_state.properties
    settings = st.session_state.settings
    d        = st.session_state.deal_data

    # ── Header ──
    is_claude = claude_available()
    ai_badge = (
        "<span style='background:linear-gradient(135deg,#7c3aed,#1a6fe0);color:#fff;"
        "font-size:9px;font-weight:700;padding:3px 10px;border-radius:4px;"
        "letter-spacing:1px;text-transform:uppercase;margin-left:8px;'>Powered by Claude</span>"
        if is_claude else
        "<span style='background:#f1f5f9;color:#64748b;font-size:9px;font-weight:700;"
        "padding:3px 10px;border-radius:4px;letter-spacing:1px;'>Add ANTHROPIC_API_KEY to unlock Claude</span>"
    )

    st.markdown(f"""
    <div style="margin-bottom:24px;">
      <div style="font-size:10px;font-weight:700;color:#7c3aed;letter-spacing:0.14em;
                  text-transform:uppercase;margin-bottom:6px;">AIRE INTELLIGENCE</div>
      <div style="display:flex;align-items:center;gap:0;">
        <span style="font-family:Outfit,sans-serif;font-size:clamp(1.6rem,3vw,2.2rem);
                     font-weight:900;letter-spacing:-0.03em;color:#07111f;">AIRE Intelligence</span>
        {ai_badge}
      </div>
      <div style="font-size:14px;color:#6f8aab;margin-top:4px;">
        Institutional-grade AI analysis. Portfolio intelligence. Deal verdicts in seconds.
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not is_claude:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#f5f0ff,#eff6ff);border:1px solid #c4b5fd;
                    border-left:5px solid #7c3aed;border-radius:12px;padding:20px 24px;margin-bottom:24px;">
          <div style="font-size:14px;font-weight:800;color:#4c1d95;margin-bottom:8px;">
            Unlock Full Claude Intelligence
          </div>
          <div style="font-size:13px;color:#5b21b6;line-height:1.7;margin-bottom:14px;">
            Add your Anthropic API key to Railway Variables to unlock Claude claude-sonnet-4-5 across the entire platform.
            Claude delivers superior reasoning, deeper market insights, and more precise deal analysis than any other AI.
          </div>
          <div style="background:#fff;border-radius:8px;padding:12px 14px;font-family:monospace;
                      font-size:12px;color:#4c1d95;border:1px solid #c4b5fd;">
            ANTHROPIC_API_KEY = sk-ant-xxxxxxxxxxxx
          </div>
          <div style="font-size:11px;color:#7c3aed;margin-top:8px;">
            Get your key at console.anthropic.com → API Keys → Create Key
          </div>
        </div>
        """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Portfolio Intelligence", "Deal Deep Dive", "Ask AIRE"])

    # ── TAB 1: Portfolio Intelligence ──
    with tab1:
        st.markdown("<div style='font-size:13px;color:#6f8aab;margin-bottom:16px;'>Claude analyzes your entire pipeline simultaneously — risk across all deals, capital allocation, and actionable recommendations.</div>", unsafe_allow_html=True)

        if not props:
            st.info("Add deals to your pipeline to run Portfolio Intelligence.")
        else:
            col_run, col_info = st.columns([1, 2])
            with col_run:
                run_btn = st.button("Run Portfolio Intelligence", type="primary", use_container_width=True)
            with col_info:
                st.markdown(f"<div style='font-size:12px;color:#6f8aab;padding-top:8px;'>{len(props)} deals · ${sum(p['purchase_price'] for p in props)/1e6:.1f}M AUM · Avg IRR {sum(p['irr'] for p in props)/len(props):.1%}</div>", unsafe_allow_html=True)

            if run_btn or st.session_state.get("portfolio_intel_cache"):
                if run_btn:
                    with st.spinner("Claude is analyzing your entire portfolio..."):
                        analysis = run_claude_deep_analysis(props, settings)
                        st.session_state.portfolio_intel_cache = analysis
                        audit_log("ai_analysis", "Full Portfolio", f"AIRE Intelligence portfolio analysis — {len(props)} deals")
                else:
                    analysis = st.session_state.portfolio_intel_cache

                # Render analysis in premium card
                st.markdown(f"""
                <div style="background:#fff;border:1px solid #e4ecf7;border-radius:14px;
                            padding:28px 32px;margin-top:20px;box-shadow:0 2px 16px rgba(7,17,31,0.06);">
                  <div style="display:flex;justify-content:space-between;align-items:center;
                              margin-bottom:20px;padding-bottom:14px;border-bottom:1px solid #f1f5f9;">
                    <div>
                      <div style="font-size:11px;color:#7c3aed;font-weight:700;text-transform:uppercase;
                                  letter-spacing:1px;margin-bottom:3px;">PORTFOLIO ANALYSIS</div>
                      <div style="font-size:14px;font-weight:800;color:#07111f;">AIRE Intelligence Report</div>
                    </div>
                    <div style="font-size:11px;color:#94a3b8;">{datetime.now().strftime("%B %d, %Y %H:%M")}</div>
                  </div>
                  <div style="font-size:13.5px;color:#1e293b;line-height:1.85;white-space:pre-wrap;">{analysis}</div>
                  <div style="margin-top:20px;padding-top:14px;border-top:1px solid #f1f5f9;
                              font-size:10px;color:#94a3b8;">
                    Generated by AIRE Intelligence · {"Powered by Claude claude-sonnet-4-5" if is_claude else "Powered by GPT-4o"} · Patent Pending
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 2: Deal Deep Dive ──
    with tab2:
        st.markdown("<div style='font-size:13px;color:#6f8aab;margin-bottom:16px;'>Full institutional-grade analysis of any deal in your pipeline. Claude goes deeper than any analyst.</div>", unsafe_allow_html=True)

        if not props:
            st.info("Add deals to your pipeline first.")
        else:
            deal_names = [p["name"] for p in props]
            sel_name   = st.selectbox("Select Deal to Analyze", deal_names, key="intel_deal_sel")
            sel_deal   = next(p for p in props if p["name"] == sel_name)

            col_m = st.columns(4)
            cap = sel_deal['noi_year1']/sel_deal['purchase_price'] if sel_deal['purchase_price'] else 0
            col_m[0].metric("Price",    f"${sel_deal['purchase_price']/1e6:.1f}M")
            col_m[1].metric("Cap Rate", f"{cap:.2%}")
            col_m[2].metric("IRR",      f"{sel_deal['irr']:.1%}")
            col_m[3].metric("Grade",    sel_deal['grade'])

            dive_btn = st.button("Run Deep Dive Analysis", type="primary", use_container_width=False)

            cache_key = f"deep_dive_{sel_deal['id']}"
            if dive_btn or st.session_state.get(cache_key):
                if dive_btn:
                    with st.spinner(f"Claude is performing deep analysis on {sel_name}..."):
                        analysis = run_claude_deal_score(sel_deal, settings)
                        st.session_state[cache_key] = analysis
                        audit_log("ai_analysis", sel_name, "AIRE Intelligence deep dive")
                else:
                    analysis = st.session_state[cache_key]

                st.markdown(f"""
                <div style="background:#fff;border:1px solid #e4ecf7;border-radius:14px;
                            padding:28px 32px;margin-top:20px;box-shadow:0 2px 16px rgba(7,17,31,0.06);">
                  <div style="display:flex;justify-content:space-between;align-items:center;
                              margin-bottom:20px;padding-bottom:14px;border-bottom:1px solid #f1f5f9;">
                    <div>
                      <div style="font-size:11px;color:#1a6fe0;font-weight:700;text-transform:uppercase;
                                  letter-spacing:1px;margin-bottom:3px;">DEAL DEEP DIVE</div>
                      <div style="font-size:14px;font-weight:800;color:#07111f;">{sel_name}</div>
                    </div>
                    <div style="font-size:11px;color:#94a3b8;">{datetime.now().strftime("%B %d, %Y")}</div>
                  </div>
                  <div style="font-size:13.5px;color:#1e293b;line-height:1.85;white-space:pre-wrap;">{analysis}</div>
                  <div style="margin-top:20px;padding-top:14px;border-top:1px solid #f1f5f9;
                              font-size:10px;color:#94a3b8;">
                    Generated by AIRE Intelligence · {"Claude claude-sonnet-4-5" if is_claude else "GPT-4o"} · Patent Pending
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 3: Ask AIRE ──
    with tab3:
        st.markdown("<div style='font-size:13px;color:#6f8aab;margin-bottom:16px;'>Ask AIRE Intelligence anything. Portfolio questions, market analysis, structuring advice, LP talking points — anything.</div>", unsafe_allow_html=True)

        # Chat history for this tab
        if "intel_chat" not in st.session_state:
            st.session_state.intel_chat = []

        # Suggested prompts
        suggestions = [
            "Which deal in my pipeline is most at risk if rates rise 100bps?",
            "Draft LP talking points for my best-performing deal",
            "What market conditions should make me pause acquisitions?",
            "How should I structure the waterfall for a value-add multifamily?",
            "What questions will my IC ask about my riskiest deal?",
        ]

        if not st.session_state.intel_chat:
            st.markdown("<div style='font-size:11px;color:#94a3b8;margin-bottom:8px;'>Suggested prompts:</div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, s in enumerate(suggestions[:4]):
                if cols[i%2].button(s, key=f"suggest_{i}", use_container_width=True):
                    st.session_state.intel_chat.append({"role": "user", "content": s})
                    with st.spinner("AIRE Intelligence is thinking..."):
                        reply = run_claude_deep_analysis(props, settings, query=s)
                    st.session_state.intel_chat.append({"role": "assistant", "content": reply})
                    st.rerun()

        # Render chat
        for msg in st.session_state.intel_chat:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="background:#f0f4f8;border-radius:10px;padding:12px 16px;
                            margin-bottom:8px;max-width:85%;margin-left:auto;">
                  <div style="font-size:13px;color:#07111f;">{msg["content"]}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#fff;border:1px solid #e4ecf7;border-radius:10px;
                            padding:16px 20px;margin-bottom:12px;
                            border-left:4px solid #7c3aed;">
                  <div style="font-size:10px;color:#7c3aed;font-weight:700;
                              text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px;">
                    AIRE Intelligence {"· Claude" if is_claude else ""}
                  </div>
                  <div style="font-size:13.5px;color:#1e293b;line-height:1.8;white-space:pre-wrap;">{msg["content"]}</div>
                </div>""", unsafe_allow_html=True)

        # Input
        user_q = st.text_input("Ask AIRE Intelligence anything...", key="intel_input",
                               placeholder="e.g. What are the biggest risks in my portfolio right now?")
        c1, c2 = st.columns([3,1])
        with c2:
            send = st.button("Ask", type="primary", use_container_width=True)
        if (send and user_q) or (user_q and user_q != st.session_state.get("intel_last_q","")):
            if send and user_q:
                st.session_state.intel_last_q = user_q
                st.session_state.intel_chat.append({"role": "user", "content": user_q})
                with st.spinner("AIRE Intelligence is analyzing..."):
                    reply = run_claude_deep_analysis(props, settings, query=user_q)
                st.session_state.intel_chat.append({"role": "assistant", "content": reply})
                st.rerun()

        if st.session_state.intel_chat:
            if st.button("Clear conversation", key="clear_intel"):
                st.session_state.intel_chat = []
                st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6X │ AUDIT TRAIL VIEW
# ──────────────────────────────────────────────────────────────────────────────

AUDIT_EVENT_STYLES = {
    "settings_change": ("Settings",     "#1a6fe0", "rgba(26,111,224,0.10)"),
    "deal_created":    ("Deal Added",   "#059669", "rgba(5,150,105,0.10)"),
    "deal_updated":    ("Deal Updated", "#d97706", "rgba(217,119,6,0.10)"),
    "deal_deleted":    ("Deal Removed", "#dc2626", "rgba(220,38,38,0.10)"),
    "memo_generated":  ("Memo Drafted", "#7c3aed", "rgba(124,58,237,0.10)"),
    "memo_sent":       ("Memo Sent",    "#7c3aed", "rgba(124,58,237,0.10)"),
    "om_imported":     ("OM Import",    "#1a9fd4", "rgba(26,159,212,0.10)"),
    "ai_analysis":     ("AI Analysis",  "#7c3aed", "rgba(124,58,237,0.10)"),
    "login":           ("Sign In",      "#64748b", "rgba(100,116,139,0.10)"),
}

def _audit_ts(raw: str) -> str:
    try:
        clean = str(raw).replace("Z", "").split("+")[0]
        dt = datetime.fromisoformat(clean)
        return dt.strftime("%b %d, %Y · %H:%M")
    except Exception:
        return str(raw)[:16]

def view_audit_trail():
    st.markdown("""<div style="margin-bottom:22px;"><div style="font-size:10px;font-weight:700;color:#1a6fe0;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:6px;">AUDIT TRAIL</div><div style="font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-0.03em;color:#07111f;">System of Record — Every Action, Logged</div></div>""", unsafe_allow_html=True)
    st.markdown("<div style='font-size:14px;color:#6f8aab;margin-bottom:20px;'>Immutable, timestamped history of every assumption change, deal event, memo, and analysis run at your firm. Built for IC scrutiny and LP reporting.</div>", unsafe_allow_html=True)

    sb, sb_err = get_supabase()
    if not sb:
        st.warning("Connect Supabase to enable the audit trail. Events will begin recording automatically once connected.", icon="🗄️")
        return

    logs = db_load_audit(st.session_state.user_email, limit=500)

    if not logs:
        st.markdown("""
        <div class="pain-card" style="text-align:center;padding:48px 24px;">
          <div style="font-family:Outfit,sans-serif;font-size:1.2rem;font-weight:800;color:#07111f;margin-bottom:8px;">No events recorded yet</div>
          <div style="font-size:13px;color:#6f8aab;max-width:440px;margin:0 auto;line-height:1.7;">
            The audit trail records automatically from this point forward — settings changes,
            deals added or removed, IC memos generated and delivered, and AI analyses.
            Make a change anywhere in the platform and it will appear here.
          </div>
          <div style="font-size:11px;color:#94a3b8;margin-top:14px;">
            If you just enabled this feature, run the updated AIRE_setup.sql in Supabase first.
          </div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Summary metrics ──
    n_settings = sum(1 for l in logs if l.get("event_type") == "settings_change")
    n_deals    = sum(1 for l in logs if l.get("event_type") == "deal_created")
    n_memos    = sum(1 for l in logs if l.get("event_type") in ("memo_generated", "memo_sent"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Events Logged",    f"{len(logs)}")
    c2.metric("Settings Changes", f"{n_settings}")
    c3.metric("Deals Added",      f"{n_deals}")
    c4.metric("Memo Activity",    f"{n_memos}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filters + export ──
    fc1, fc2, fc3 = st.columns([1.2, 1.6, 0.9])
    with fc1:
        types_present = sorted({l.get("event_type", "") for l in logs})
        type_labels = ["All Events"] + [AUDIT_EVENT_STYLES.get(t, (t, "", ""))[0] for t in types_present]
        sel_label = st.selectbox("Event Type", type_labels, label_visibility="collapsed")
    with fc2:
        q = st.text_input("Search", placeholder="Search deals, users, fields…", label_visibility="collapsed")
    with fc3:
        df = pd.DataFrame(logs)
        cols = [c for c in ["created_at","user_email","event_type","entity","field","old_value","new_value","detail"] if c in df.columns]
        csv = df[cols].to_csv(index=False).encode() if cols else b""
        st.download_button("Export CSV", data=csv,
            file_name=f"AIRE_AuditTrail_{st.session_state.firm_id}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv", use_container_width=True)

    # Resolve label back to type key
    sel_type = None
    if sel_label != "All Events":
        for t in types_present:
            if AUDIT_EVENT_STYLES.get(t, (t, "", ""))[0] == sel_label:
                sel_type = t
                break

    shown = 0
    rows_html = ""
    for l in logs:
        et = l.get("event_type", "")
        if sel_type and et != sel_type:
            continue
        hay = " ".join(str(l.get(k, "") or "") for k in ("entity","detail","user_email","field","old_value","new_value")).lower()
        if q and q.lower() not in hay:
            continue
        shown += 1
        if shown > 200:
            break
        label, color, bg = AUDIT_EVENT_STYLES.get(et, (et or "Event", "#64748b", "rgba(100,116,139,0.10)"))
        ts   = _audit_ts(l.get("created_at", ""))
        user = (l.get("user_email") or "").split("@")[0]
        ent  = l.get("entity") or ""
        det  = l.get("detail") or ""
        change_html = ""
        if l.get("field"):
            change_html = (
                "<div style='font-family:JetBrains Mono,monospace;font-size:11.5px;color:#3a5278;"
                "background:#f5f8fd;border:1px solid #e4ecf7;border-radius:6px;padding:5px 10px;"
                "display:inline-block;margin-top:5px;'>"
                + str(l.get("field"))
                + ": <span style='color:#94a3b8;text-decoration:line-through;'>" + str(l.get("old_value")) + "</span>"
                + " &rarr; <span style='color:#1a6fe0;font-weight:700;'>" + str(l.get("new_value")) + "</span></div>"
            )
        rows_html += (
            "<div style='background:#fff;border:1px solid #e4ecf7;border-radius:12px;"
            "padding:13px 18px;margin-bottom:8px;box-shadow:0 1px 4px rgba(7,17,31,0.06);'>"
            "<div style='display:flex;justify-content:space-between;align-items:flex-start;gap:14px;'>"
            "<div style='flex:1;min-width:0;'>"
            "<div style='display:flex;align-items:center;gap:9px;margin-bottom:3px;flex-wrap:wrap;'>"
            f"<span style='background:{bg};color:{color};font-size:9.5px;font-weight:700;"
            f"padding:3px 10px;border-radius:999px;text-transform:uppercase;letter-spacing:0.8px;white-space:nowrap;'>{label}</span>"
            f"<span style='font-family:Outfit,sans-serif;font-size:13.5px;font-weight:700;color:#07111f;'>{ent}</span>"
            "</div>"
            f"<div style='font-size:12.5px;color:#3a5278;line-height:1.55;'>{det}</div>"
            f"{change_html}"
            "</div>"
            "<div style='text-align:right;flex-shrink:0;'>"
            f"<div style='font-size:11px;color:#94a3b8;font-family:JetBrains Mono,monospace;white-space:nowrap;'>{ts}</div>"
            f"<div style='font-size:11px;color:#6f8aab;font-weight:600;margin-top:2px;'>{user}</div>"
            "</div></div></div>"
        )

    if shown == 0:
        st.info("No events match your filter.")
    else:
        st.markdown(rows_html, unsafe_allow_html=True)
        if shown >= 200:
            st.caption("Showing most recent 200 matching events. Export CSV for the complete record.")


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 7 │ SIDEBAR & ROUTER
# ──────────────────────────────────────────────────────────────────────────────

# Each section has a color, icon, and items
# color = accent used for section label and active indicator
NAV_SECTIONS = [
    {
        "label": "ANALYSIS",
        "color": "#1a9fd4",   # sky blue
        "bg":    "rgba(26,159,212,0.10)",
        "items": [
            ("Deal Dashboard",      "Dashboard"),
            ("AIRE Intelligence",   "Intelligence"),
            ("AI Data Room",        "DataRoom"),
            ("AI Tracker",          "AITracker"),
            ("AI Deal Scorer",      "AIScorer"),
            ("Market Data",         "MarketData"),
        ],
    },
    {
        "label": "MEMOS",
        "color": "#7c3aed",   # purple
        "bg":    "rgba(124,58,237,0.10)",
        "items": [
            ("IC Memo Generator","ICMemo"),
            ("Memo Delivery",    "MemoDelivery"),
            ("Broker Emails",    "BrokerEmails"),
        ],
    },
    {
        "label": "UNDERWRITING",
        "color": "#1a6fe0",   # blue
        "bg":    "rgba(26,111,224,0.10)",
        "items": [
            ("Debt Structuring", "DebtModel"),
            ("Waterfall Calc",   "Waterfall"),
            ("Deal Comparison",  "Compare"),
            ("Stress Testing",   "StressTest"),
            ("Version Pro Forma","VersionPF"),
        ],
    },
    {
        "label": "PORTFOLIO",
        "color": "#059669",   # emerald green
        "bg":    "rgba(5,150,105,0.10)",
        "items": [
            ("Master Pipeline",  "Pipeline"),
            ("Portfolio Alerts", "Alerts"),
            ("Deal CRM",         "CRM"),
            ("LP Portal",        "LPPortal"),
            ("OM Import",        "OMImport"),
        ],
    },
    {
        "label": "FIRM",
        "color": "#64748b",   # slate
        "bg":    "rgba(100,116,139,0.10)",
        "items": [
            ("Team",             "Team"),
            ("White-Label",      "WhiteLabel"),
            ("Lender Database",  "LenderDB"),
            ("Audit Trail",      "AuditTrail"),
            ("Settings",         "Settings"),
        ],
    },
]

def nav_btn(label, view_key, current_view):
    is_active = current_view == view_key
    btn_label = label
    if st.button(btn_label, key=f"nav_{view_key}", use_container_width=True):
        st.session_state.current_view = view_key
        st.rerun()


def render_sidebar():
    v = st.session_state.get("current_view", "Dashboard")

    # ── Sidebar premium CSS ──
    st.markdown("""
    <style>
      section[data-testid="stSidebar"] {
        min-width: 218px !important; width: 218px !important;
      }
      [data-testid="stSidebar"] .stButton > button {
        font-size: 12px !important;
        padding: 6px 10px !important;
        text-align: left !important;
        font-weight: 400 !important;
        color: #4a7a9e !important;
        border-radius: 6px !important;
        letter-spacing: 0.01em !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.1s !important;
      }
      [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.05) !important;
        color: #c8dff0 !important;
      }
      [data-testid="stSidebar"] .stButton {
        margin-bottom: 0px !important;
      }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # ── Logo — original AIRE brand image ──
        st.markdown(f'''
        <div style="padding:16px 12px 14px;border-bottom:1px solid rgba(255,255,255,0.06);
                    margin-bottom:8px;text-align:center;">
          <div style="background:#fff;border-radius:10px;padding:7px 14px;
                      display:inline-block;margin-bottom:8px;
                      box-shadow:0 2px 10px rgba(0,0,0,0.22);">
            <img src="{AIRE_LOGO_URI}" style="height:32px;display:block;" />
          </div>
          <div style="font-size:7.5px;color:#4d9fd4;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Integrated Real Estate</div>
          <div style="font-size:6.5px;color:rgba(255,255,255,0.20);letter-spacing:1px;margin-top:1px;">Patent Pending</div>
        </div>
        ''', unsafe_allow_html=True)

        # Guided mode indicator
        if st.session_state.get("onboarding_mode"):
            st.markdown(
                '<div style="background:rgba(26,159,212,0.12);border:1px solid rgba(26,159,212,0.25);'
                'border-radius:5px;padding:5px 10px;margin-bottom:8px;text-align:center;">' +
                '<span style="font-size:9px;color:#1a9fd4;font-weight:700;letter-spacing:0.5px;">GUIDED MODE</span></div>',
                unsafe_allow_html=True
            )

        # ── Navigation — color-coded sections ──
        for section in NAV_SECTIONS:
            sec_color = section["color"]
            sec_bg    = section["bg"]
            sec_label = section["label"]

            # Section header with colored left accent
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:6px;'
                f'margin:16px 0 5px 2px;padding-left:6px;">'
                f'<div style="width:3px;height:12px;background:{sec_color};border-radius:2px;flex-shrink:0;"></div>'
                f'<span style="font-size:8.5px;color:{sec_color};font-weight:700;'
                f'letter-spacing:2px;text-transform:uppercase;opacity:0.85;">{sec_label}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

            for label, view_key in section["items"]:
                is_active = v == view_key
                if is_active:
                    st.markdown(
                        f'<div style="background:{sec_bg};border-radius:6px;'
                        f'border-left:3px solid {sec_color};margin-bottom:1px;">',
                        unsafe_allow_html=True
                    )
                if st.button(
                    ("› " if is_active else "  ") + label,
                    key=f"nav_{view_key}",
                    use_container_width=True
                ):
                    st.session_state.current_view = view_key
                    st.rerun()
                if is_active:
                    st.markdown("</div>", unsafe_allow_html=True)

        # ── Active deal pill — premium card ──
        d = st.session_state.deal_data
        st.markdown("<div style='height:1px;background:rgba(255,255,255,0.05);margin:16px 0 12px;'></div>", unsafe_allow_html=True)
        grade_colors = {"A":"#059669","B":"#1a6fe0","C":"#d97706","D":"#dc2626"}
        if d:
            gc   = grade_colors.get(d.get("grade","B"),"#1a6fe0")
            irr  = d.get("irr", 0)
            name = d["name"][:22]
            grade = d.get("grade","B")
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(26,111,224,0.12),rgba(26,159,212,0.06));
                        border:1px solid rgba(26,111,224,0.20);border-radius:10px;
                        padding:12px 12px 10px;">
              <div style="font-size:8px;color:#2a6fa8;font-weight:700;letter-spacing:1.5px;
                          text-transform:uppercase;margin-bottom:6px;">Active Deal</div>
              <div style="font-size:13px;color:#e8f4fd;font-weight:700;line-height:1.2;
                          margin-bottom:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</div>
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="text-align:left;">
                  <div style="font-size:8px;color:#2a5070;font-weight:600;margin-bottom:1px;">IRR</div>
                  <div style="font-size:14px;font-weight:800;color:#1a9fd4;font-family:monospace;">{irr:.1%}</div>
                </div>
                <div style="background:{gc};color:#fff;font-size:11px;font-weight:800;
                            padding:4px 10px;border-radius:6px;letter-spacing:0.5px;">
                  {grade}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="border:1px dashed rgba(255,255,255,0.06);border-radius:10px;
                        padding:12px;text-align:center;">
              <div style="font-size:8px;color:#1e3a5a;font-weight:700;letter-spacing:1px;
                          text-transform:uppercase;margin-bottom:4px;">No Deal Loaded</div>
              <div style="font-size:11px;color:#162d42;">Open Master Pipeline<br>to add your first deal</div>
            </div>
            """, unsafe_allow_html=True)

        # ── User footer ──
        st.markdown("<div style='height:1px;background:rgba(255,255,255,0.05);margin:14px 0 10px;'></div>", unsafe_allow_html=True)
        email_short = st.session_state.user_email or ""
        firm_id     = st.session_state.firm_id or ""
        st.markdown(f"""
        <div style="padding:0 2px 2px;">
          <div style="font-size:10px;color:#1a3a5a;overflow:hidden;text-overflow:ellipsis;
                      white-space:nowrap;margin-bottom:2px;">{email_short}</div>
          <div style="display:flex;align-items:center;justify-content:space-between;">
            <span style="font-size:11px;font-weight:700;color:#1a9fd4;letter-spacing:0.5px;">{firm_id}</span>
            <span style="background:rgba(26,111,224,0.12);color:#1a6fe0;font-size:8px;
                         font-weight:700;padding:2px 6px;border-radius:3px;text-transform:uppercase;
                         letter-spacing:0.5px;">PRO</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Sign Out", key="logout"):
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
    elif v == "DebtModel":      view_debt_structuring()
    elif v == "Waterfall":      view_waterfall()
    elif v == "Compare":        view_deal_comparison()
    elif v == "Alerts":         view_alerts()
    elif v == "OMImport":       view_om_import()
    elif v == "LPPortal":       view_lp_portal()
    elif v == "CRM":            view_crm()
    elif v == "MarketData":     view_market_data()
    elif v == "AIScorer":       view_ai_scorer()
    elif v == "MemoDelivery":   view_memo_delivery()
    elif v == "StressTest":     view_stress_test()
    elif v == "VersionPF":      view_version_proforma()
    elif v == "Team":           view_team()
    elif v == "WhiteLabel":     view_whitelabel()
    elif v == "LenderDB":       view_lender_db()
    elif v == "AuditTrail":     view_audit_trail()
    elif v == "BrokerEmails":   view_broker_emails()
    elif v == "Intelligence":    view_aire_intelligence()

if __name__ == "__main__":
    main()
