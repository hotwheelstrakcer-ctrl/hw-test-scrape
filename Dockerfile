FROM python:3.9-slim

# Set up app directory
WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
