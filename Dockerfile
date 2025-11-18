# Docker support for Playwright CrewAI Agents
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY requirements.txt package.json package-lock.json ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies
RUN npm ci

# Install Playwright browsers
RUN npx playwright install --with-deps chromium

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs test_plan tests

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HEADLESS=true

# Expose port for Streamlit (if used)
EXPOSE 8501

# Default command
CMD ["python", "src/test_ai_assistant/main.py"]
