# 1. Base image
FROM python:3.10-slim

# 2. Working directory
WORKDIR /app

# 3. System dependencies
# build-essential is added to compile any missing wheels
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends -o Acquire::Retries=5 \
    ghostscript \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Upgrade pip tooling
RUN python -m pip install --upgrade pip setuptools wheel

# 5. Install CPU-only PyTorch (Heavy file, installed first to cache it)
RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu \
    --timeout 1000 \
    --retries 5

# 6. Copy & install remaining dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir \
    -r requirements.txt \
    --timeout 1000 \
    --retries 5

# 7. Copy application code
COPY . .

# 8. Expose port (Documentation only, Render ignores this but good for local)
EXPOSE 8000

# 9. Run app
# Using ${PORT} ensures Render can assign its own port dynamically
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]