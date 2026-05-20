FROM python:3.11-slim

WORKDIR /app


# Only install curl — skip build-essential entirely
# Most Python packages have pre-built wheels so we don't need gcc
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    streamlit \
    plotly \
    pydeck \
    requests \
    openai \
    supabase \
    openpyxl \
    xlrd \
    pypdf \
    numpy \
    pandas

# Copy app files
COPY . .

# Create streamlit config
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
