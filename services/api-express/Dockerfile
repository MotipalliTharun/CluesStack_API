# --- Build stage ---
FROM node:20-slim AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci
COPY tsconfig.json ./tsconfig.json
COPY src ./src
RUN npm run build

# --- Runtime stage ---
FROM node:20-slim
WORKDIR /app
ENV NODE_ENV=production
# Render injects PORT at runtime; default to 4000 locally
ENV PORT=4000
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev
COPY --from=build /app/dist ./dist
EXPOSE 4000
CMD ["bash","-lc","node dist/index.js"]
