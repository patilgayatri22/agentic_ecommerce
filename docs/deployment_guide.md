# Deployment Guide

## Local Deployment

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Steps

1. **Clone and Setup**
```bash
git clone https://github.com/yourusername/agentic-ecommerce.git
cd agentic-ecommerce
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Run Application**
```bash
streamlit run app/streamlit_app.py
```

## Cloud Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**
```bash
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your repository
   - Set main file path: `app/streamlit_app.py`
   - Add secrets in Settings → Secrets:
```toml
HUGGINGFACE_API_TOKEN = "your_token"
ICECAT_TOKEN = "your_token"
RAPIDAPI_KEY = "your_token"
```

3. **Deploy** - Click "Deploy"

### Heroku Deployment

1. **Create Procfile**
```
web: streamlit run app/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Create runtime.txt**
```
python-3.11.0
```

3. **Deploy**
```bash
heroku create your-app-name
heroku config:set HUGGINGFACE_API_TOKEN=your_token
heroku config:set ICECAT_TOKEN=your_token
heroku config:set RAPIDAPI_KEY=your_token
git push heroku main
```

### Google Cloud Run

1. **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD streamlit run app/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Deploy**
```bash
gcloud run deploy agentic-ecommerce \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars HUGGINGFACE_API_TOKEN=$HUGGINGFACE_API_TOKEN
```

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Choose Ubuntu 22.04 LTS
   - t2.medium or larger recommended
   - Configure security group to allow port 8501

2. **SSH and Setup**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install python3.11 python3-pip python3-venv -y

# Clone repository
git clone https://github.com/yourusername/agentic-ecommerce.git
cd agentic-ecommerce

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
nano .env
# Add your API keys

# Run with screen (keeps running after logout)
screen -S streamlit
streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0
# Press Ctrl+A then D to detach
```

3. **Setup systemd service (optional)**
```bash
sudo nano /etc/systemd/system/agentic-ecommerce.service
```

```ini
[Unit]
Description=Agentic E-Commerce Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/agentic-ecommerce
Environment="PATH=/home/ubuntu/agentic-ecommerce/venv/bin"
EnvironmentFile=/home/ubuntu/agentic-ecommerce/.env
ExecStart=/home/ubuntu/agentic-ecommerce/venv/bin/streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable agentic-ecommerce
sudo systemctl start agentic-ecommerce
```

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t agentic-ecommerce .

# Run container
docker run -p 8501:8501 \
  -e HUGGINGFACE_API_TOKEN=your_token \
  -e ICECAT_TOKEN=your_token \
  -e RAPIDAPI_KEY=your_token \
  agentic-ecommerce
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - HUGGINGFACE_API_TOKEN=${HUGGINGFACE_API_TOKEN}
      - ICECAT_TOKEN=${ICECAT_TOKEN}
      - RAPIDAPI_KEY=${RAPIDAPI_KEY}
    env_file:
      - .env
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

## Production Considerations

### Performance
- Use caching aggressively
- Consider Redis for distributed caching
- Implement rate limiting for API calls
- Use connection pooling for HTTP clients

### Security
- Never commit `.env` file
- Use secrets management (AWS Secrets Manager, Google Secret Manager)
- Implement authentication if needed
- Use HTTPS in production
- Validate all user inputs

### Monitoring
- Set up error tracking (Sentry)
- Monitor API usage and costs
- Track response times
- Set up alerts for failures

### Scaling
- Use load balancer for multiple instances
- Consider async workers for heavy tasks
- Cache frequently accessed data
- Implement circuit breakers for external APIs

## Troubleshooting

### Common Issues

**Port already in use**
```bash
# Find process using port 8501
lsof -i :8501
# Kill the process
kill -9 <PID>
```

**API timeouts**
- Increase timeout settings in `src/config.py`
- Check API rate limits
- Verify network connectivity

**Memory issues**
- Reduce cache size in config
- Limit concurrent requests
- Use streaming for large datasets

**Environment variables not loading**
- Verify `.env` file exists
- Check file permissions
- Ensure python-dotenv is installed
