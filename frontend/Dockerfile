# Этап сборки
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .
RUN npm run build
RUN npm install -g serve
RUN npm run build

EXPOSE 3000

CMD ["serve", "-s", "build"]