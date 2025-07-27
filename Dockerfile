# Use official Python slim image
FROM --platform=linux/amd64 python:3.10-slim

# Set workdir
WORKDIR /app

# Install system dependencies for PyMuPDF
RUN apt-get update && apt-get install -y libmupdf-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
COPY main.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy English model (offline trick: pack it in image)
RUN python -m spacy download en_core_web_sm

# Entrypoint
CMD ["python", "main.py"]
