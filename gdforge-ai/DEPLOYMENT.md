# Deployment Guide

## Local Development

### Předpoklady
- Python 3.10+
- Node.js 18+
- OpenAI nebo Anthropic API klíč

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/gdforge-ai.git
cd gdforge-ai

# 2. Run setup script
bash setup.sh

# 3. Configure API keys
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# 4. Start backend (Terminal 1)
cd backend
source venv/bin/activate
python run.py

# 5. Start frontend (Terminal 2)
cd frontend
npm run dev
```

Backend: http://localhost:8000
Frontend: http://localhost:5173

## Docker Deployment

### Single Command

```bash
docker-compose up
```

### Manual Build & Run

```bash
# Backend
docker build -t gdforge-backend ./backend
docker run -p 8000:8000 gdforge-backend

# Frontend
docker build -t gdforge-frontend ./frontend
docker run -p 5173:5173 gdforge-frontend
```

## Production Deployment

### 1. Environment Setup

Create `.env` s production settings:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
DEBUG=false
CORS_ORIGINS=["https://yourdomain.com"]
```

### 2. Backend Production

```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# Or using systemd (Linux)
sudo cp gdforge-ai.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gdforge-ai
sudo systemctl start gdforge-ai
```

systemd service file (`gdforge-ai.service`):
```ini
[Unit]
Description=GDForge AI Backend
After=network.target

[Service]
Type=notify
User=gdforge
WorkingDirectory=/opt/gdforge-ai/backend
Environment="PATH=/opt/gdforge-ai/backend/venv/bin"
ExecStart=/opt/gdforge-ai/backend/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Frontend Production

```bash
# Build
npm run build

# Serve static files
# Using Node.js
npx serve dist

# Using Nginx
sudo cp nginx.conf /etc/nginx/sites-available/gdforge
sudo ln -s /etc/nginx/sites-available/gdforge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

nginx config (`nginx.conf`):
```nginx
upstream gdforge_backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    root /var/www/gdforge-ai;

    # Frontend
    location / {
        try_files $uri /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://gdforge_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

### 4. SSL/TLS Certificate

Using Let's Encrypt:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

### 5. Database (Future)

Pro persistence (v0.2.0+):

```bash
# PostgreSQL
docker run -d \
  --name gdforge-db \
  -e POSTGRES_PASSWORD=securepass \
  -p 5432:5432 \
  postgres:15

# Update connection string in .env
DATABASE_URL=postgresql://user:password@localhost:5432/gdforge
```

## Cloud Deployment

### Heroku

```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create gdforge-ai

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-...

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

Procfile:
```
web: cd backend && gunicorn -w 4 app.main:app
```

### AWS Deployment

Using EC2 + RDS + S3:

```bash
# 1. EC2 Instance
# - Ubuntu 22.04 LTS
# - Security group: allow 80, 443, 22

# 2. Connect & setup
ssh -i key.pem ec2-user@instance-ip
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nodejs npm nginx

# 3. Clone & setup
git clone https://github.com/yourusername/gdforge-ai.git
cd gdforge-ai
bash setup.sh

# 4. Configure Nginx & SSL
# (See nginx config above)

# 5. Setup systemd service
# (See service file above)

# 6. Start services
sudo systemctl start gdforge-ai
sudo systemctl start nginx
```

### Google Cloud Run

```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT_ID/gdforge-ai

# Deploy
gcloud run deploy gdforge-ai \
  --image gcr.io/PROJECT_ID/gdforge-ai \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-...
```

### Docker Hub Registry

```bash
# Build
docker build -t yourusername/gdforge-ai-backend ./backend
docker build -t yourusername/gdforge-ai-frontend ./frontend

# Push
docker login
docker push yourusername/gdforge-ai-backend
docker push yourusername/gdforge-ai-frontend

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

docker-compose.prod.yml:
```yaml
version: '3.8'

services:
  backend:
    image: yourusername/gdforge-ai-backend:latest
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEBUG=false
    restart: unless-stopped

  frontend:
    image: yourusername/gdforge-ai-frontend:latest
    ports:
      - "5173:5173"
    restart: unless-stopped
```

## Monitoring & Logging

### Application Logging

Backend logs s Python logging:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Application started")
logger.error("Error occurred", exc_info=True)
```

### System Monitoring

Using supervisor:

```ini
[program:gdforge-backend]
command=/opt/gdforge-ai/backend/venv/bin/python run.py
directory=/opt/gdforge-ai/backend
user=gdforge
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/gdforge/backend.log
```

### Metrics

Future (0.3.0):
- Prometheus metrics
- Grafana dashboards
- Alert configuration

## Backup & Recovery

### Database Backup (Future)

```bash
# PostgreSQL backup
pg_dump gdforge > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql gdforge < backup_20240101_120000.sql
```

### Code Backup

```bash
# Git ensures version control
git remote add backup https://github.com/backup/gdforge-ai.git
git push backup main
```

## Security Checklist

- [ ] API keys v environment variables (ne v kódu)
- [ ] HTTPS/SSL certificate nainstalován
- [ ] Rate limiting enabled
- [ ] CORS nakonfigurován správně
- [ ] SQL injection protection (ORM)
- [ ] XSS protection (React escaping)
- [ ] CSRF tokens (budoucí feature)
- [ ] Regular security updates
- [ ] Firewall rules
- [ ] Backup strategy

## Troubleshooting

**Backend nedostupný:**
```bash
# Check if running
curl http://localhost:8000/api/health

# Check logs
docker logs gdforge-backend
```

**API Key error:**
```bash
# Verify .env
cat backend/.env | grep API_KEY

# Test API
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test"}'
```

**Frontend build error:**
```bash
cd frontend
rm -rf node_modules dist
npm install
npm run build
```

## Performance Tuning

1. **Backend:**
   - Vylaďte počet Gunicorn workers: `4 * CPU_COUNT`
   - Cache LLM responses
   - Connection pooling

2. **Frontend:**
   - Code splitting
   - Lazy loading
   - Image optimization

3. **Database:**
   - Index frequently queried fields
   - Connection pooling

## Support

- Issues: https://github.com/CowleyCZE/RangersAPP/issues
- Discussions: https://github.com/CowleyCZE/RangersAPP/discussions

---

Last updated: 2024-12-11
