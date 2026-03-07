# AIRE — Institutional Underwriting Platform

## Stack
- **Frontend/App**: Streamlit (deployed via Streamlit Cloud)
- **AI Engine**: OpenAI GPT-4o
- **Market Data**: FRED API (Federal Reserve)
- **Database/Auth**: Supabase (Postgres + Row-Level Security)
- **Maps**: PyDeck (Mapbox)

---

## Streamlit Secrets Setup
Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY  = "sk-..."
SUPABASE_URL    = "https://xxxx.supabase.co"
SUPABASE_KEY    = "eyJ..."        # anon/public key
FRED_API_KEY    = "your_fred_key" # free at fred.stlouisfed.org
```

---

## Supabase Setup
1. Create project at supabase.com
2. Run `supabase_schema.sql` in the SQL Editor
3. Enable Email Auth under Authentication > Providers
4. Add firm users manually: Authentication > Users > Invite User
5. Each user email domain maps to a firm automatically

## Adding a Paying Customer
1. Create user in Supabase Auth with their corporate email
2. Insert row in `firms` table: `INSERT INTO firms (name, domain) VALUES ('Firm Name', 'firmname.com');`
3. Done — they can log in immediately

---

## FRED API Key
Free at: https://fred.stlouisfed.org/docs/api/api_key.html
Used for: Live 10-Year Treasury rate → calculates real-time debt pricing

---

## Deploy to Streamlit Cloud
1. Push to GitHub
2. Go to share.streamlit.io → New App → connect repo
3. Add secrets in Streamlit Cloud dashboard (Settings > Secrets)
4. Deploy

---

## Features
- ✅ Secure multi-firm login (Supabase Auth + Row-Level Security)
- ✅ AI Deal Copilot (GPT-4o RAG chat)
- ✅ Excel/CSV Rent Roll + T12 parsing with NOI extraction
- ✅ Dynamic pro forma (reacts to uploaded data)
- ✅ Monte Carlo simulation (3,000 scenarios)
- ✅ IRR sensitivity heatmap (exit cap × hold period)
- ✅ AI deal grading + investment scoring (0–100)
- ✅ AI property tracker with self-correcting predictions
- ✅ Live debt pricing via FRED API
- ✅ IC Memo generator (AI executive summary)
- ✅ Master pipeline with AUM tracking
- ✅ 3D asset map (PyDeck)
- ✅ Pro forma Excel export
