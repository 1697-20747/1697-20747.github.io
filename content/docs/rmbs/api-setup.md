# RMBS API Server - Setup & Deployment Guide

Complete guide to deploy and manage the RMBS API server.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r rmbs_api_requirements.txt
```

### 2. Set Environment Variables

```bash
export RMBS_MASTER_KEY="your_secure_master_key_here"
export FLASK_ENV="production"
```

### 3. Run Server (Development)

```bash
python rmbs_api_server.py
```

Server will start on `http://localhost:5000`

### 4. Run Server (Production)

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 rmbs_api_server:app
```

---

## API Key Management

### Create API Key

Admin creates key for a client:

```bash
curl -X POST http://localhost:5000/api/v1/admin/keys/create \
  -H "X-Master-Key: your_secure_master_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Investment Bank XYZ",
    "permissions": ["read_reports", "read_dashboards"],
    "expires_days": 365
  }'
```

**Response**:
```json
{
  "api_key": "H8x_BQaY1K2_pL3_zM9_nO7_vP5...",
  "key_hash": "abc123def456...",
  "client_name": "Investment Bank XYZ",
  "expires": "2027-05-17T...",
  "permissions": ["read_reports", "read_dashboards"]
}
```

**⚠️ IMPORTANT**: The `api_key` is only shown once on creation. Save it securely!

### List All API Keys

```bash
curl -H "X-Master-Key: your_secure_master_key_here" \
  http://localhost:5000/api/v1/admin/keys/list
```

### Revoke API Key

```bash
curl -X POST http://localhost:5000/api/v1/admin/keys/revoke \
  -H "X-Master-Key: your_secure_master_key_here" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "key_to_revoke"}'
```

---

## Client Usage

### Python Client

```python
from rmbs_api_client import RMBSAPIClient

# Initialize
client = RMBSAPIClient(
    base_url='http://localhost:5000',
    api_key='H8x_BQaY1K2_pL3_zM9_nO7_vP5...',
    verify_ssl=False  # Set to True for production
)

# Health check
status = client.health_check()
print(f"API Status: {status['status']}")

# Get key info
key_info = client.get_key_info()
print(f"Client: {key_info['client_name']}")
print(f"Permissions: {key_info['permissions']}")
print(f"Expires: {key_info['expires']}")

# List reports
reports = client.list_reports()
print(f"Available reports: {reports['count']}")

# Get summary
summary = client.get_reports_summary()
print(f"Total reports: {summary['total_reports']}")
print(f"Size: {summary['total_size_mb']} MB")

# Download report
client.download_report(
    year=2026,
    month=5,
    format='csv',
    output_file='investor_report.csv'
)

# List dashboards
dashboards = client.list_dashboards()
print(f"Available dashboards: {dashboards['count']}")

# Download dashboard
client.download_dashboard(
    year=2026,
    month=5,
    dashboard_type='pool',
    output_file='dashboard.html'
)

# View dashboard HTML
html = client.view_dashboard(
    year=2026,
    month=5,
    dashboard_type='summary'
)
print(html[:500])  # First 500 chars
```

### cURL Examples

```bash
# 1. Health check
curl http://localhost:5000/api/v1/health

# 2. Get key info
curl -H "X-API-Key: YOUR_KEY" \
  http://localhost:5000/api/v1/auth/key-info

# 3. List reports
curl -H "X-API-Key: YOUR_KEY" \
  http://localhost:5000/api/v1/reports/list | jq

# 4. Get report summary
curl -H "X-API-Key: YOUR_KEY" \
  http://localhost:5000/api/v1/reports/summary | jq

# 5. Download report
curl -H "X-API-Key: YOUR_KEY" \
  http://localhost:5000/api/v1/reports/download/2026-05/investor_report_202605.csv \
  -o report.csv

# 6. List dashboards
curl -H "X-API-Key: YOUR_KEY" \
  http://localhost:5000/api/v1/dashboards/list | jq

# 7. Download dashboard
curl -H "X-API-Key: YOUR_KEY" \
  http://localhost:5000/api/v1/dashboards/download/2026-05/dashboard_pool_202605.html \
  -o dashboard.html

# 8. View dashboard (not download)
curl -H "X-API-Key: YOUR_KEY" \
  http://localhost:5000/api/v1/view/dashboard/2026-05/dashboard_pool_202605.html \
  > dashboard.html
```

---

## Deployment Options

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY rmbs_api_requirements.txt .
RUN pip install --no-cache-dir -r rmbs_api_requirements.txt

# Copy application
COPY rmbs_api_server.py .

# Set environment
ENV FLASK_ENV=production
ENV RMBS_MASTER_KEY=change-me-in-production

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--access-logfile", "-", "rmbs_api_server:app"]
```

Build and run:

```bash
# Build image
docker build -t rmbs-api:1.0.0 .

# Run container
docker run -d \
  --name rmbs-api \
  -p 5000:5000 \
  -e RMBS_MASTER_KEY="your_secure_key" \
  -v /path/to/logs:/app/logs \
  rmbs-api:1.0.0
```

### Kubernetes Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rmbs-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rmbs-api
  template:
    metadata:
      labels:
        app: rmbs-api
    spec:
      containers:
      - name: rmbs-api
        image: rmbs-api:1.0.0
        ports:
        - containerPort: 5000
        env:
        - name: RMBS_MASTER_KEY
          valueFrom:
            secretKeyRef:
              name: rmbs-secrets
              key: master-key
        - name: FLASK_ENV
          value: "production"
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
        volumeMounts:
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: logs
        persistentVolumeClaim:
          claimName: rmbs-logs-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: rmbs-api-service
spec:
  selector:
    app: rmbs-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

Deploy:

```bash
# Create secret
kubectl create secret generic rmbs-secrets --from-literal=master-key="your_secure_key"

# Deploy
kubectl apply -f k8s-deployment.yaml

# Check status
kubectl get pods
kubectl logs rmbs-api-xxxxx
```

---

## Production Configuration

### HTTPS/SSL

Enable SSL with reverse proxy (nginx):

```nginx
server {
    listen 443 ssl http2;
    server_name api.rmbs.example.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name api.rmbs.example.com;
    return 301 https://$server_name$request_uri;
}
```

### Logging

Enable detailed logging:

```python
# In rmbs_api_server.py
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('rmbs_api.log', maxBytes=10*1024*1024, backupCount=10)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
```

### Monitoring

Check API health:

```bash
curl http://localhost:5000/api/v1/health | jq
```

Monitor logs:

```bash
tail -f rmbs_api.log | grep -E "ERROR|WARNING"
```

---

## Security Checklist

- [ ] Change `RMBS_MASTER_KEY` from default
- [ ] Enable HTTPS/SSL
- [ ] Use strong, unique API keys
- [ ] Rotate keys periodically (set expiration dates)
- [ ] Enable rate limiting
- [ ] Enable audit logging
- [ ] Monitor access patterns
- [ ] Restrict network access (firewall)
- [ ] Run as unprivileged user
- [ ] Keep dependencies updated

---

## Troubleshooting

### Server won't start

```bash
# Check if port 5000 is in use
lsof -i :5000

# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list | grep Flask
```

### API key not working

```bash
# Verify key exists
curl -H "X-Master-Key: MASTER_KEY" \
  http://localhost:5000/api/v1/admin/keys/list | jq

# Check if key is active and not expired
```

### Reports/dashboards not found

```bash
# Verify files exist
ls -la logs/*/investor_report_*.csv
ls -la logs/*/dashboard_*.html

# Check permissions
stat logs/2026-05_*/
```

### High memory usage

```bash
# Reduce workers
gunicorn --bind 0.0.0.0:5000 --workers 2 rmbs_api_server:app

# Check for memory leaks
ps aux | grep gunicorn
```

---

## API Documentation

Full API documentation is available at:

- Markdown: `API_DOCUMENTATION.md`
- HTML: `/api/v1/docs` (browse at http://localhost:5000/api/v1/docs)

---

## Support

For issues or questions:
1. Check logs: `tail -f rmbs_api.log`
2. Review documentation: `API_DOCUMENTATION.md`
3. Test with curl: See examples above
4. Contact: api-support@rmbs.example.com

