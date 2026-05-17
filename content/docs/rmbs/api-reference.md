# RMBS API Documentation

Complete REST API for secure access to RMBS reports and dashboards.

## Overview

The RMBS API provides secure, authenticated access to:
- RMBS Investor Reports (CSV & Parquet)
- Interactive Dashboards (HTML)
- Report metadata and summaries

### Key Features

✅ **Authentication**: Secure API key-based authentication  
✅ **Authorization**: Fine-grained permissions (read_reports, read_dashboards)  
✅ **Rate Limiting**: Protect against abuse  
✅ **Audit Logging**: Track all access  
✅ **RESTful**: Standard HTTP methods and status codes  
✅ **Documentation**: Self-documenting API with OpenAPI support  

---

## Getting Started

### 1. Obtain API Key

Contact RMBS administrator to request an API key:

```bash
# Admin creates key for client
curl -X POST https://api.rmbs.example.com/api/v1/admin/keys/create \
  -H "X-Master-Key: MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Investment Bank XYZ",
    "permissions": ["read_reports", "read_dashboards"],
    "expires_days": 365
  }'

# Response:
{
  "api_key": "your_secret_key_here",
  "key_hash": "abc123...",
  "client_name": "Investment Bank XYZ",
  "expires": "2025-05-17T...",
  "permissions": ["read_reports", "read_dashboards"]
}
```

**IMPORTANT**: Save the `api_key` immediately - it's only shown once!

### 2. Make Your First Request

```bash
curl -H "X-API-Key: your_api_key_here" \
  https://api.rmbs.example.com/api/v1/health
```

---

## Authentication

### Headers

All endpoints require the API key in the request header:

```
X-API-Key: YOUR_API_KEY
```

### Example

```bash
curl -H "X-API-Key: eyJ0eXAiOiJKV1QiLCJhbGc..." \
  https://api.rmbs.example.com/api/v1/reports/list
```

---

## Endpoints

### Health Check

**Endpoint**: `GET /api/v1/health`  
**Auth**: Not required  
**Description**: Check API server status

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-17T12:34:56.789Z",
  "service": "RMBS API Server",
  "version": "1.0.0"
}
```

### Get API Key Info

**Endpoint**: `GET /api/v1/auth/key-info`  
**Auth**: Required  
**Permissions**: None  
**Description**: Get information about current API key

**Response**:
```json
{
  "client_name": "Investment Bank XYZ",
  "created": "2025-05-17T08:00:00Z",
  "expires": "2026-05-17T08:00:00Z",
  "permissions": ["read_reports", "read_dashboards"],
  "usage_count": 342,
  "last_used": "2026-05-17T12:30:00Z"
}
```

---

## Reports API

### List Reports

**Endpoint**: `GET /api/v1/reports/list`  
**Auth**: Required  
**Permissions**: `read_reports`  
**Rate Limit**: 30 per minute  
**Description**: List all available reports

**Response**:
```json
{
  "count": 48,
  "reports": [
    {
      "filename": "investor_report_202605.csv",
      "format": "csv",
      "month": 5,
      "year": 2026,
      "size_bytes": 596,
      "generated": "2026-05-17T08:15:00Z",
      "path": "2026-05_20260517_080204",
      "download_url": "/api/v1/reports/download/2026-05/investor_report_202605.csv"
    },
    {
      "filename": "investor_report_202605.parquet",
      "format": "parquet",
      "month": 5,
      "year": 2026,
      "size_bytes": 12288,
      "generated": "2026-05-17T08:15:00Z",
      "path": "2026-05_20260517_080204",
      "download_url": "/api/v1/reports/download/2026-05/investor_report_202605.parquet"
    }
  ]
}
```

### Get Reports Summary

**Endpoint**: `GET /api/v1/reports/summary`  
**Auth**: Required  
**Permissions**: `read_reports`  
**Rate Limit**: 20 per minute  
**Description**: Get aggregate statistics

**Response**:
```json
{
  "total_reports": 96,
  "total_size_bytes": 614400,
  "total_size_mb": 0.59,
  "months_available": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
  "years_available": [2024, 2025, 2026],
  "earliest_report": "2024-01",
  "latest_report": "2026-05"
}
```

### Download Report

**Endpoint**: `GET /api/v1/reports/download/{year}-{month:02d}/{filename}`  
**Auth**: Required  
**Permissions**: `read_reports`  
**Rate Limit**: 10 per minute  
**Description**: Download report file

**Parameters**:
- `year`: Year (e.g., 2026)
- `month`: Month zero-padded (e.g., 05)
- `filename`: Exact filename (e.g., investor_report_202605.csv)

**Example**:
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
  https://api.rmbs.example.com/api/v1/reports/download/2026-05/investor_report_202605.csv \
  -o investor_report.csv
```

**Response**: File content (binary)

---

## Dashboards API

### List Dashboards

**Endpoint**: `GET /api/v1/dashboards/list`  
**Auth**: Required  
**Permissions**: `read_dashboards`  
**Rate Limit**: 30 per minute  
**Description**: List all available dashboards

**Response**:
```json
{
  "count": 36,
  "dashboards": [
    {
      "filename": "dashboard_pool_202605.html",
      "type": "pool",
      "month": 5,
      "year": 2026,
      "size_bytes": 8500,
      "generated": "2026-05-17T08:15:00Z",
      "path": "2026-05_20260517_080204",
      "download_url": "/api/v1/dashboards/download/2026-05/dashboard_pool_202605.html"
    },
    {
      "filename": "dashboard_tranches_202605.html",
      "type": "tranches",
      "month": 5,
      "year": 2026,
      "size_bytes": 9700,
      "generated": "2026-05-17T08:15:00Z",
      "path": "2026-05_20260517_080204",
      "download_url": "/api/v1/dashboards/download/2026-05/dashboard_tranches_202605.html"
    }
  ]
}
```

### Download Dashboard

**Endpoint**: `GET /api/v1/dashboards/download/{year}-{month:02d}/{filename}`  
**Auth**: Required  
**Permissions**: `read_dashboards`  
**Rate Limit**: 10 per minute  
**Description**: Download dashboard HTML file

**Example**:
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
  https://api.rmbs.example.com/api/v1/dashboards/download/2026-05/dashboard_pool_202605.html \
  -o dashboard.html
```

### View Dashboard

**Endpoint**: `GET /api/v1/view/dashboard/{year}-{month:02d}/{filename}`  
**Auth**: Required  
**Permissions**: `read_dashboards`  
**Rate Limit**: 20 per minute  
**Description**: Get dashboard HTML (not as download)

**Example**:
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
  https://api.rmbs.example.com/api/v1/view/dashboard/2026-05/dashboard_pool_202605.html
```

**Response**: HTML content

---

## Admin Endpoints

### Create API Key

**Endpoint**: `POST /api/v1/admin/keys/create`  
**Auth**: Master key required  
**Rate Limit**: 5 per hour  
**Description**: Create new API key for client

**Headers**:
```
X-Master-Key: your_master_key
Content-Type: application/json
```

**Body**:
```json
{
  "client_name": "Investment Bank XYZ",
  "permissions": ["read_reports", "read_dashboards"],
  "expires_days": 365
}
```

**Response**:
```json
{
  "api_key": "new_secret_key",
  "key_hash": "abc123...",
  "client_name": "Investment Bank XYZ",
  "expires": "2027-05-17T...",
  "permissions": ["read_reports", "read_dashboards"]
}
```

### List API Keys

**Endpoint**: `GET /api/v1/admin/keys/list`  
**Auth**: Master key required  
**Rate Limit**: 10 per hour  
**Description**: List all API keys and their usage

**Headers**:
```
X-Master-Key: your_master_key
```

**Response**:
```json
{
  "total_keys": 5,
  "keys": [
    {
      "key_hash": "abc123...",
      "client_name": "Investment Bank XYZ",
      "created": "2025-05-17T08:00:00Z",
      "expires": "2026-05-17T08:00:00Z",
      "active": true,
      "usage_count": 342,
      "last_used": "2026-05-17T12:30:00Z",
      "permissions": ["read_reports", "read_dashboards"]
    }
  ]
}
```

### Revoke API Key

**Endpoint**: `POST /api/v1/admin/keys/revoke`  
**Auth**: Master key required  
**Rate Limit**: 5 per hour  
**Description**: Revoke an API key

**Headers**:
```
X-Master-Key: your_master_key
Content-Type: application/json
```

**Body**:
```json
{
  "api_key": "key_to_revoke"
}
```

**Response**:
```json
{
  "message": "Key revoked successfully"
}
```

---

## Rate Limits

| Endpoint Type | Limit |
|---|---|
| Health check | Unlimited |
| List endpoints | 30 per minute |
| Download endpoints | 10 per minute |
| View endpoints | 20 per minute |
| Admin endpoints | 5 per hour |
| General | 200 per day, 50 per hour |

When limit exceeded, server returns `429 Too Many Requests`.

---

## Error Handling

### Error Response Format

```json
{
  "error": "Error type",
  "message": "Human-readable error message"
}
```

### Status Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (missing/invalid API key) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not found |
| 429 | Rate limit exceeded |
| 500 | Server error |

### Example Error Response

```json
{
  "error": "Authentication failed",
  "message": "API key has expired"
}
```

---

## Client Libraries

### Python

```python
from rmbs_api_client import RMBSAPIClient

client = RMBSAPIClient(
    base_url='https://api.rmbs.example.com',
    api_key='your_api_key_here'
)

# List reports
reports = client.list_reports()
print(f"Available reports: {reports['count']}")

# Download report
client.download_report(2026, 5, format='csv', output_file='report.csv')

# Download dashboard
client.download_dashboard(2026, 5, dashboard_type='pool', output_file='dashboard.html')
```

### cURL

```bash
# List reports
curl -H "X-API-Key: YOUR_API_KEY" \
  https://api.rmbs.example.com/api/v1/reports/list | jq

# Download report
curl -H "X-API-Key: YOUR_API_KEY" \
  https://api.rmbs.example.com/api/v1/reports/download/2026-05/investor_report_202605.csv \
  -o report.csv

# View dashboard
curl -H "X-API-Key: YOUR_API_KEY" \
  https://api.rmbs.example.com/api/v1/view/dashboard/2026-05/dashboard_pool_202605.html \
  > dashboard.html
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const client = axios.create({
  baseURL: 'https://api.rmbs.example.com',
  headers: {
    'X-API-Key': 'your_api_key_here'
  }
});

// List reports
client.get('/api/v1/reports/list')
  .then(res => console.log(`Available: ${res.data.count} reports`))
  .catch(err => console.error(err));

// Download report
client.get('/api/v1/reports/download/2026-05/investor_report_202605.csv', {
  responseType: 'arraybuffer'
})
  .then(res => {
    const fs = require('fs');
    fs.writeFileSync('report.csv', res.data);
  });
```

---

## Security Best Practices

1. **Secure Storage**: Store API keys securely (use environment variables, vaults)
2. **HTTPS Only**: Always use HTTPS (API server enforces this)
3. **Key Rotation**: Rotate keys periodically (set expiration dates)
4. **Monitoring**: Monitor API usage for anomalies
5. **Revocation**: Revoke compromised keys immediately
6. **Least Privilege**: Only grant necessary permissions
7. **Audit Logs**: Review access logs regularly

---

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY rmbs_api_requirements.txt .
RUN pip install -r rmbs_api_requirements.txt

COPY rmbs_api_server.py .

ENV RMBS_MASTER_KEY=change-me-in-production
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "rmbs_api_server:app"]
```

### Production Server

```bash
# Install dependencies
pip install -r rmbs_api_requirements.txt

# Set environment
export RMBS_MASTER_KEY="your_secure_master_key"

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 --access-logfile - rmbs_api_server:app

# Or use with Supervisor
# See supervisor config template below
```

### Supervisor Config

```ini
[program:rmbs-api]
command=/usr/bin/python3 /app/rmbs_api_server.py
autostart=true
autorestart=true
stderr_logfile=/var/log/rmbs-api.err.log
stdout_logfile=/var/log/rmbs-api.out.log
environment=RMBS_MASTER_KEY=your_key
```

---

## Troubleshooting

### Invalid API Key

```json
{
  "error": "Authentication failed",
  "message": "Invalid API key"
}
```

**Solution**: Check that X-API-Key header is correct

### Key Expired

```json
{
  "error": "Authentication failed",
  "message": "API key has expired"
}
```

**Solution**: Request admin to create new key or extend expiration

### Permission Denied

```json
{
  "error": "Permission denied",
  "message": "This API key does not have ['read_dashboards'] permission"
}
```

**Solution**: Request admin to grant required permissions

### Rate Limit Exceeded

```json
{
  "error": "Rate limit exceeded",
  "message": "..."
}
```

**Solution**: Wait before making more requests or contact admin for limit increase

---

## Support

For API issues or questions:
- Contact: api-support@rmbs.example.com
- Documentation: https://api.rmbs.example.com/api/v1/docs
- Status: https://status.rmbs.example.com

