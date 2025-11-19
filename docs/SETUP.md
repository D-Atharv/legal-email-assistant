# Setup and Deployment Guide

## Table of Contents

1. [Development Setup](#development-setup)
2. [Environment Configuration](#environment-configuration)
3. [Running Locally](#running-locally)
4. [Production Deployment](#production-deployment)
5. [Docker Deployment](#docker-deployment)
6. [CI/CD Setup](#cicd-setup)
7. [Troubleshooting](#troubleshooting)

---

## Development Setup

### Prerequisites

Before starting, ensure you have the following installed:

- **Node.js** 20.x or higher ([Download](https://nodejs.org/))
- **Python** 3.11 or higher ([Download](https://www.python.org/))
- **npm** or **yarn** package manager
- **Git** for version control
- **Google Gemini API Key** ([Get API Key](https://makersuite.google.com/app/apikey))

### System Requirements

- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: At least 2GB free space
- **Internet**: Stable connection for API calls

---

## Environment Configuration

### Backend Environment Variables

Create a `.env` file in the `server/` directory:

```env
# === LLM Provider (Required) ===
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# === CORS Configuration ===
FRONTEND_ORIGIN=http://localhost:3000

# === Audit Logging ===
AUDIT_LOG_DIR=static/audit_logs

# === Application Settings (Optional) ===
APP_NAME=Legal Email Assistant - Backend
LOG_LEVEL=INFO
```

**Important Notes:**

- `GEMINI_API_KEY` is **required** - get it from Google AI Studio
- `FRONTEND_ORIGIN` must match your frontend URL exactly
- `AUDIT_LOG_DIR` will be created automatically if it doesn't exist

### Frontend Environment Variables

Create a `.env.local` file in the `client/` directory:

```env
# Backend API URL
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

**Important Notes:**

- Use `NEXT_PUBLIC_` prefix for client-side variables
- Update this URL for production deployment

---

## Running Locally

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/legal-email-assistant.git
cd legal-email-assistant
```

### Step 2: Backend Setup

#### On Windows (PowerShell)

```powershell
# Navigate to server directory
cd server

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
# (Copy from section above)

# Run the server
uvicorn main:app --reload --port 8000
```

#### On Linux/macOS

```bash
# Navigate to server directory
cd server

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# (Copy from section above)

# Run the server
uvicorn main:app --reload --port 8000
```

**Verify Backend is Running:**

Open http://localhost:8000/docs to see the Swagger UI.

### Step 3: Frontend Setup

#### Open a New Terminal

```bash
# Navigate to client directory
cd client

# Install dependencies
npm install

# Create .env.local file
# (Copy from section above)

# Run development server
npm run dev
```

**Verify Frontend is Running:**

Open http://localhost:3000 to see the application.

### Step 4: Test the Application

1. Navigate to http://localhost:3000/assistant
2. Paste a sample email in Step 1
3. Click "Analyze Email"
4. Review the JSON output
5. Provide contract clauses
6. Generate a draft reply

---

## Production Deployment

### Backend Deployment (FastAPI)

#### Option 1: Traditional Server (VPS/EC2)

**1. Prepare the Server**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Nginx (optional, for reverse proxy)
sudo apt install nginx -y
```

**2. Deploy the Application**

```bash
# Clone repository
git clone https://github.com/your-username/legal-email-assistant.git
cd legal-email-assistant/server

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create production .env file
nano .env
```

**Production `.env` Example:**

```env
GEMINI_API_KEY=your_production_api_key
GEMINI_MODEL=gemini-2.5-flash
FRONTEND_ORIGIN=https://your-frontend-domain.com
AUDIT_LOG_DIR=/var/log/legal-assistant/audit_logs
LOG_LEVEL=WARNING
```

**3. Run with Production Server**

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**4. Create Systemd Service (Linux)**

Create `/etc/systemd/system/legal-assistant.service`:

```ini
[Unit]
Description=Legal Email Assistant API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/legal-email-assistant/server
Environment="PATH=/path/to/legal-email-assistant/server/venv/bin"
ExecStart=/path/to/legal-email-assistant/server/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and Start Service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable legal-assistant
sudo systemctl start legal-assistant
sudo systemctl status legal-assistant
```

**5. Configure Nginx Reverse Proxy**

Create `/etc/nginx/sites-available/legal-assistant`:

```nginx
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable Site:**

```bash
sudo ln -s /etc/nginx/sites-available/legal-assistant /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**6. Setup SSL with Let's Encrypt**

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.your-domain.com
```

#### Option 2: Render.com

**1. Create `render.yaml` in project root:**

```yaml
services:
  - type: web
    name: legal-assistant-api
    env: python
    region: oregon
    buildCommand: "cd server && pip install -r requirements.txt"
    startCommand: "cd server && uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: GEMINI_MODEL
        value: gemini-2.5-flash
      - key: FRONTEND_ORIGIN
        value: https://your-frontend-domain.vercel.app
      - key: PYTHON_VERSION
        value: 3.11.0
```

**2. Deploy:**

- Connect GitHub repository
- Add environment variables in Render dashboard
- Deploy automatically

#### Option 3: Railway

**1. Install Railway CLI:**

```bash
npm install -g @railway/cli
```

**2. Deploy:**

```bash
cd server
railway login
railway init
railway up
```

**3. Set Environment Variables:**

```bash
railway variables set GEMINI_API_KEY=your_key
railway variables set FRONTEND_ORIGIN=https://your-frontend.com
```

### Frontend Deployment (Next.js)

#### Option 1: Vercel (Recommended)

**1. Install Vercel CLI:**

```bash
npm install -g vercel
```

**2. Deploy:**

```bash
cd client
vercel login
vercel
```

**3. Set Environment Variables:**

In Vercel Dashboard:

- Go to Project Settings → Environment Variables
- Add: `NEXT_PUBLIC_BACKEND_URL` = `https://your-backend-api.com`

**4. Production Deployment:**

```bash
vercel --prod
```

#### Option 2: Netlify

**1. Build the Application:**

```bash
cd client
npm run build
```

**2. Deploy:**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify login
netlify deploy --prod
```

**3. Configure Build Settings:**

In `netlify.toml`:

```toml
[build]
  command = "cd client && npm run build"
  publish = "client/.next"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

#### Option 3: Traditional Server

**1. Build the Application:**

```bash
cd client
npm run build
```

**2. Run Production Server:**

```bash
npm start
```

**3. Use PM2 for Process Management:**

```bash
npm install -g pm2
pm2 start npm --name "legal-assistant-frontend" -- start
pm2 save
pm2 startup
```

**4. Configure Nginx:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## Docker Deployment

### Backend Dockerfile

Create `server/Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create audit log directory
RUN mkdir -p static/audit_logs

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

Create `client/Dockerfile`:

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

# Copy built application
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# Expose port
EXPOSE 3000

# Run application
CMD ["node", "server.js"]
```

### Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: "3.8"

services:
  backend:
    build:
      context: ./server
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - GEMINI_MODEL=gemini-2.5-flash
      - FRONTEND_ORIGIN=http://localhost:3000
    volumes:
      - ./server/static/audit_logs:/app/static/audit_logs
    restart: unless-stopped

  frontend:
    build:
      context: ./client
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
    depends_on:
      - backend
    restart: unless-stopped
```

### Running with Docker Compose

```bash
# Create .env file with GEMINI_API_KEY
echo "GEMINI_API_KEY=your_api_key" > .env

# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## CI/CD Setup

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST \
            -H "Authorization: Bearer $RENDER_API_KEY" \
            https://api.render.com/v1/services/${{ secrets.RENDER_SERVICE_ID }}/deploys

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: "--prod"
```

### GitLab CI/CD

Create `.gitlab-ci.yml`:

```yaml
stages:
  - build
  - test
  - deploy

build-backend:
  stage: build
  image: python:3.11
  script:
    - cd server
    - pip install -r requirements.txt
    - python -m pytest

build-frontend:
  stage: build
  image: node:20
  script:
    - cd client
    - npm ci
    - npm run build

deploy-production:
  stage: deploy
  only:
    - main
  script:
    - echo "Deploying to production..."
    # Add your deployment commands here
```

---

## Troubleshooting

### Common Issues

#### 1. Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Frontend Can't Connect to Backend

**Error:** `Network request failed` or CORS error

**Solution:**

- Verify backend is running: http://localhost:8000/docs
- Check `FRONTEND_ORIGIN` in backend `.env` matches frontend URL exactly
- Check `NEXT_PUBLIC_BACKEND_URL` in frontend `.env.local`

#### 3. Gemini API Errors

**Error:** `401 Unauthorized`

**Solution:**

- Verify `GEMINI_API_KEY` in `.env` is correct
- Check API key hasn't expired
- Ensure API key has proper permissions

**Error:** `429 Too Many Requests`

**Solution:**

- You've hit the API rate limit
- Wait and retry
- Consider implementing request throttling

#### 4. Port Already in Use

**Error:** `Address already in use`

**Solution:**

On Windows:

```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <process_id> /F
```

On Linux/Mac:

```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

#### 5. Build Errors

**Error:** TypeScript or ESLint errors

**Solution:**

```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

### Getting Help

If you encounter issues:

1. Check the logs:

   - Backend: Terminal where uvicorn is running
   - Frontend: Browser console (F12)
   - Audit logs: `server/static/audit_logs/`

2. Enable debug logging:

   ```env
   LOG_LEVEL=DEBUG
   ```

3. Test API endpoints directly:

   - Visit http://localhost:8000/docs
   - Use the interactive Swagger UI

4. Check system requirements are met

5. Consult the documentation in `docs/` folder

---

## Production Checklist

Before deploying to production:

- [ ] Update environment variables for production
- [ ] Set `LOG_LEVEL=WARNING` or `ERROR`
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting
- [ ] Configure backup for audit logs
- [ ] Test all endpoints with production data
- [ ] Set up proper error tracking (e.g., Sentry)
- [ ] Review and minimize API key permissions
- [ ] Configure rate limiting
- [ ] Set up health check endpoints
- [ ] Document runbook for common issues
- [ ] Configure automatic restarts on failure

---

**Last Updated:** November 19, 2025
