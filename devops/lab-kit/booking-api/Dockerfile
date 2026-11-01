# syntax=docker/dockerfile:1
FROM node:22-bookworm-slim AS deps
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev --no-audit --no-fund

FROM gcr.io/distroless/nodejs22-debian12:nonroot
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY package.json server.js healthcheck.js ./
ENV NODE_ENV=production PORT=8080
EXPOSE 8080
USER nonroot
CMD ["server.js"]
