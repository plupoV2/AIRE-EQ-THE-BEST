FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install ALL dependencies upfront so app starts instantly
COPY requirements.txt .
RUN pip install --no-cache-dir streamlit plotly pydeck requests openai \
    supabase openpyxl xlrd pypdf numpy pandas

# Run requirements.txt too in case there are extras
RUN pip install --no-cache-dir -r requirements.txt || true

COPY . .

# Create streamlit config to disable the browser open and set port
RUN mkdir -p /app/.streamlit && cat > /app/.streamlit/config.toml << 'TOML'
[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
TOML

EXPOSE 8501

ENTRYPOINT ["python", "start.py"]
