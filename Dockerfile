# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables
# PYTHONUNBUFFERED ensures logs are printed immediately to Deplexo's console
ENV PYTHONUNBUFFERED=1
# Set the working directory inside the container
WORKDIR /app

# 1. Copy only requirements first (this leverages Docker caching to speed up builds)
COPY requirements.txt .

# 2. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of your application code (main.py, assets, etc.)
COPY . .

# Expose the port Deplexo expects (we set this to 3000 earlier)
EXPOSE 3000

# Command to run your NiceGUI app
CMD ["python", "main.py"]