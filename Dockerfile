# Frontend build stage
FROM node:16-alpine AS frontend-build
WORKDIR /app
COPY react-frontend/package*.json ./
RUN npm ci
COPY react-frontend/ ./
RUN npm run build

# Backend build stage
FROM python:3.9-alpine AS backend-build
WORKDIR /app
COPY requirements.txt ./
RUN apk --no-cache add build-base
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py ./

# MongoDB stage
FROM mongo:5.0.5
VOLUME /data/db

# Production stage
FROM python:3.9-alpine
WORKDIR /app
ENV MONGO_URI=mongodb://mongodb:27017/emertondb
ENV PYTHONUNBUFFERED=1
COPY --from=backend-build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=backend-build /app/main.py .
COPY --from=frontend-build /app/build/ /app/static/
COPY --from=frontend-build /app/public/ /app/templates/
EXPOSE 8000
CMD ["python", "main.py"]
