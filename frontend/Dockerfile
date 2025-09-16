FROM node:20-alpine

WORKDIR /app

# Install deps first (better caching)
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN if [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then npm i -g pnpm && pnpm i --frozen-lockfile; \
    elif [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
    else npm i; fi

COPY . .

ENV PORT=3000 HOST=0.0.0.0
EXPOSE 3000
CMD ["npm", "run", "dev"]


