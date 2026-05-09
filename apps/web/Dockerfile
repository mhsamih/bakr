FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY apps/web/package*.json ./apps/web/

# Install dependencies
RUN npm install --workspace=@cmms/web

# Copy source code
COPY . .

# Build the application
RUN npm run build:web

# Production image
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY apps/web/package*.json ./apps/web/

# Install production dependencies only
RUN npm install --workspace=@cmms/web --omit=dev

# Copy built application
COPY --from=builder /app/apps/web/.next ./apps/web/.next
COPY --from=builder /app/apps/web/public ./apps/web/public

EXPOSE 3000

CMD ["npm", "run", "start", "--workspace=@cmms/web"]
