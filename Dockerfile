# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL files
COPY . .

# Create memory directory
RUN mkdir -p memory_data

# Expose port
EXPOSE 8080

# Set environment
ENV PORT=8080
ENV PYTHONPATH=/app

# Start the web server IMMEDIATELY
CMD ["python", "server.py"]