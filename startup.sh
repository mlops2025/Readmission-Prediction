#!/bin/bash

set -e  # Exit on any error

echo "[INFO] Updating system and installing Docker..."
apt-get update -y
apt-get install -y apt-transport-https ca-certificates curl software-properties-common git

# Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-get update -y
apt-get install -y docker-ce

# Install Docker Compose
DOCKER_COMPOSE_VERSION=1.29.2
curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo "[INFO] Cloning project repository..."
cd /home
git clone https://github.com/mlops2025/Readmission-Prediction.git
cd Readmission-Prediction 

echo "[INFO] Creating .env from metadata..."
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

echo "[INFO] Starting Airflow with Docker Compose..."
docker-compose up -d
