FROM node:22.12.0-bookworm-slim

# backend/pyproject.toml supports Python >=3.11,<3.13. Debian bookworm supplies
# Python 3.11; uv manages the project virtual environment and locked packages.
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Use the pinned uv release already used by the project workflow.
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

WORKDIR /app

# Install Node dependencies from committed lockfiles before copying the rest
# of the application so source changes do not invalidate them.
COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package-lock.json ./frontend/
RUN npm ci && npm ci --prefix frontend

# uv installs this project (not only third-party packages), so app/ must exist
# before sync. The remaining backend files are copied with the full source
# tree below.
COPY backend/pyproject.toml backend/uv.lock ./backend/
COPY backend/app ./backend/app
RUN cd backend && uv sync --frozen

# .dockerignore keeps .env, virtual environments, node_modules, and uploads
# out of the image. Runtime credentials are supplied only through Compose.
COPY . .

EXPOSE 3000 5001

HEALTHCHECK --interval=30s --timeout=5s --start-period=45s --retries=3 \
    CMD python3 -c "import urllib.request; response = urllib.request.urlopen('http://127.0.0.1:5001/health', timeout=3); assert response.status == 200"

# The root dev command starts Vite (port 3000) and Flask (port 5001). Compose
# publishes only Vite; its /api proxy reaches Flask over the container loopback.
CMD ["npm", "run", "dev"]
