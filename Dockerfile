FROM python:3.9-slim

# Set working directory early to leverage caching
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install requirements in a single RUN command
RUN pip install -U pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the service account key file into the container
COPY ./monterrey-344322-ddc5260c31aa.json /app/service-account-file.json

# Set environment variable for Google Cloud SDK
ENV GOOGLE_APPLICATION_CREDENTIALS="./monterrey-344322-ddc5260c31aa.json"
# Expose ports
EXPOSE 8080
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Entry point
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
