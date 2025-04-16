#!/bin/bash
set -e  # Exit on any error

echo "[INFO] Updating system and installing prerequisites..."
apt-get update -y
apt-get install -y apt-transport-https ca-certificates curl software-properties-common git unzip

echo "[INFO] Installing Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-get update -y
apt-get install -y docker-ce

echo "[INFO] Installing Docker Compose..."
DOCKER_COMPOSE_VERSION=1.29.2
curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo "[INFO] Verifying network..."
ping -c 3 github.com || echo "⚠️ Warning: GitHub not reachable at first try."

echo "[INFO] Cloning project repository..."
cd /home

# Add retry logic in case of temporary failure
for attempt in {1..3}; do
  git clone https://github.com/mlops2025/Readmission-Prediction.git && break
  echo "⚠️ Clone attempt $attempt failed, retrying in 5s..."
  sleep 5
done

cd Readmission-Prediction || { echo "❌ Failed to cd into repo directory"; exit 1; }

echo "[INFO] Creating .env file from GCP instance metadata..."
cat <<EOF > .env
SMTP_USER=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/SMTP_USER" -H "Metadata-Flavor: Google")
SMTP_PASSWORD=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/SMTP_PASSWORD" -H "Metadata-Flavor: Google")
DB_HOST=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/DB_HOST" -H "Metadata-Flavor: Google")
DB_NAME=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/DB_NAME" -H "Metadata-Flavor: Google")
DB_PASS=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/DB_PASS" -H "Metadata-Flavor: Google")
DB_USER=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/DB_USER" -H "Metadata-Flavor: Google")
GCP_BUCKET_NAME=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/GCP_BUCKET_NAME" -H "Metadata-Flavor: Google")
GCP_PROJECT_ID=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/GCP_PROJECT_ID" -H "Metadata-Flavor: Google")
EOF

echo "[INFO] Ensuring required directories exist..."
mkdir -p dags logs plugins config data data/processed
chown -R "${USER}":"${USER}" dags logs plugins config data

echo "[INFO] Starting Airflow with Docker Compose..."
docker-compose up -d

echo "[✅ DONE] Airflow stack launched. Check container logs if needed."
