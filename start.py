import os
import pathlib

# Write secrets from Railway env vars into .streamlit/secrets.toml
secrets_dir = pathlib.Path("/app/.streamlit")
secrets_dir.mkdir(exist_ok=True)

KEYS = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "OPENAI_API_KEY",
    "SENDGRID_API_KEY",
    "SENDGRID_FROM_EMAIL",
    "FRED_API_KEY",
]

lines = []
for key in KEYS:
    val = os.environ.get(key, "")
    if val:
        lines.append(f'{key} = "{val}"')

(secrets_dir / "secrets.toml").write_text("\n".join(lines))
print(f"✅ Wrote {len(lines)} secrets")

port = os.environ.get("PORT", "8501")
print(f"✅ Starting on port {port}")

os.execvp("streamlit", [
    "streamlit", "run", "app-2.py",
    f"--server.port={port}",
    "--server.address=0.0.0.0",
    "--server.headless=true",
    "--server.enableCORS=false",
    "--server.enableXsrfProtection=false",
    "--server.enableWebsocketCompression=false",
])
