FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY templates/ templates/
COPY static/ static/

# Expose port (default 8000)
EXPOSE 8000

# Set environment variables
ENV PORT=8000

# Run the application
CMD ["python", "main.py"]
