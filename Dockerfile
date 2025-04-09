# Use an official base image with both Node and Python
FROM node:18-bullseye

# Install Python and pip (already included in the base image, but just in case)
RUN apt-get update && apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /app

# Copy backend files
COPY src/backend ./backend
# Install Python dependencies
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy frontend files
COPY src/frontend ./frontend
# Install frontend dependencies
RUN cd frontend && npm install

# Copy service account credentials (if needed)
COPY config/key.json ./backend/service-account.json

# Set environment variable for the backend
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/backend/service-account.json

# Expose frontend and backend ports
EXPOSE 3000 8000

# Use a shell script to run both frontend and backend
CMD ["sh", "-c", "cd /app/frontend && npm run dev & cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]

