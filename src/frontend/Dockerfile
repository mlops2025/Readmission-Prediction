# Stage 1: Build the React app
FROM node:20-alpine as builder

# Set working directory
WORKDIR /app

# Install dependencies and build
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve the app with a lightweight web server
FROM nginx:alpine

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Remove default nginx config and optionally copy your own
RUN rm /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/conf.d

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
