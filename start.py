import os
import pathlib

# Write secrets.toml from Railway environment variables
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

secrets_path = secrets_dir / "secrets.toml"
secrets_path.write_text("\n".join(lines))
print(f"✅ Wrote {len(lines)} secrets to secrets.toml")

# Railway injects $PORT — default to 8501 if not set
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
