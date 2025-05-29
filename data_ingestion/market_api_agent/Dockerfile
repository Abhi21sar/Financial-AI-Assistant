# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code
COPY . .

# Expose port
EXPOSE 8001

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]