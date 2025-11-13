# Base image
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy repo
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (if using UI later)
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
