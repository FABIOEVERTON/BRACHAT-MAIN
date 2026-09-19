# EZRA web — Next.js standalone (E0-S09, substitui o stub da FASE 0)
# Multi-stage: deps → build → runtime standalone (menor imagem, healthcheck node fetch).

FROM node:22-alpine AS deps
WORKDIR /repo
COPY package.json package-lock.json turbo.json tsconfig.json ./
COPY apps/web/package.json apps/web/package.json
COPY packages/types/package.json packages/api-contracts/package.json packages/crypto/package.json packages/ui/package.json packages/types/src apps/web/.placeholder 2>/dev/null || true
RUN npm install --workspace @ezra/web --omit=dev 2>/dev/null || npm install

FROM node:22-alpine AS builder
WORKDIR /repo
COPY . .
RUN npm install && npm run build --workspace @ezra/web

FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /repo/apps/web/.next/standalone ./
COPY --from=builder /repo/apps/web/.next/static ./apps/web/.next/static
COPY --from=builder /repo/apps/web/public ./apps/web/public
EXPOSE 3000
# healthcheck: alpine sem curl — usa node fetch
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:3000/api/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
CMD ["node", "apps/web/server.js"]