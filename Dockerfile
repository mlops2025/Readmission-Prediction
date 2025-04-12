FROM node:18-bullseye

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

COPY src/backend ./backend
COPY src/backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/frontend ./frontend
RUN cd frontend && npm install && npm run build

RUN npm install -g serve

EXPOSE 8080
ENV PORT=8080

CMD ["sh", "-c", "serve -s frontend/dist -l 3000 & uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]


