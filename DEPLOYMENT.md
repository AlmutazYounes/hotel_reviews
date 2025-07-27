# 🚀 Deployment Guide

This guide will help you deploy the Hotel Reviews ABSA application to production.

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Git
- Web server (Nginx/Apache) - for production
- SSL certificate - for HTTPS

## 🏗️ Local Development Setup

### Quick Start

```bash
# Clone the repository
git clone https://github.com/AlmutazYounes/hotel_reviews.git
cd hotel_reviews

# Run automated installation
chmod +x install.sh
./install.sh

# Start the application
cd flask_app
python app.py
```

### Manual Setup

```bash
# Clone the repository
git clone https://github.com/AlmutazYounes/hotel_reviews.git
cd hotel_reviews

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model (if not already trained)
python train_model.py

# Start the application
cd flask_app
python app.py
```

## 🌐 Production Deployment

### Using Gunicorn (Recommended)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn configuration**
   ```bash
   # Create gunicorn.conf.py
   bind = "0.0.0.0:5002"
   workers = 4
   worker_class = "sync"
   worker_connections = 1000
   timeout = 30
   keepalive = 2
   max_requests = 1000
   max_requests_jitter = 100
   ```

3. **Start with Gunicorn**
   ```bash
   cd flask_app
   gunicorn -c gunicorn.conf.py app:app
   ```

### Using Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 5002
   
   CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "4", "flask_app.app:app"]
   ```

2. **Build and run**
   ```bash
   docker build -t hotel-reviews-absa .
   docker run -p 5002:5002 hotel-reviews-absa
   ```

### Using Nginx as Reverse Proxy

1. **Install Nginx**
   ```bash
   sudo apt-get install nginx  # Ubuntu/Debian
   sudo yum install nginx      # CentOS/RHEL
   ```

2. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5002;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable and start Nginx**
   ```bash
   sudo systemctl enable nginx
   sudo systemctl start nginx
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
FLASK_ENV=production
FLASK_DEBUG=False
MODEL_PATH=/path/to/hotel_reviews_model
LOG_LEVEL=INFO
```

### Model Configuration

The model can be configured in `train_model.py`:

```python
aspect_model = NERModel("bert", "bert-base-multilingual-cased",
                        labels=["B-A", "I-A", "O"],
                        args={
                            "train_batch_size": 5,
                            "num_train_epochs": 2,
                            "learning_rate": 0.0001,
                            "gradient_accumulation_steps": 5,
                            "output_dir": "hotel_reviews_model"
                        })
```

## 📊 Monitoring

### Logging

Configure logging in `flask_app/app.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/hotel_reviews.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Hotel Reviews ABSA startup')
```

### Health Check

Add a health check endpoint:

```python
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "model_loaded": os.path.exists(model_path),
        "timestamp": datetime.now().isoformat()
    })
```

## 🔒 Security

### HTTPS Setup

1. **Obtain SSL Certificate**
   ```bash
   # Using Let's Encrypt
   sudo certbot --nginx -d your-domain.com
   ```

2. **Update Nginx Configuration**
   ```nginx
   server {
       listen 443 ssl;
       server_name your-domain.com;
       
       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
       
       location / {
           proxy_pass http://127.0.0.1:5002;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

### Rate Limiting

Add rate limiting to prevent abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/analyze_sentence', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_sentence():
    # ... existing code
```

## 📈 Performance Optimization

### Model Caching

Implement model caching to avoid reloading:

```python
from functools import lru_cache

@lru_cache(maxsize=1)
def get_model():
    return NERModel("bert", model_path, use_cuda=False, ...)
```

### Response Caching

Add response caching for repeated requests:

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/analyze_sentence', methods=['POST'])
@cache.memoize(timeout=300)  # Cache for 5 minutes
def analyze_sentence():
    # ... existing code
```

## 🧪 Testing

### Run Tests

```bash
# Test the model
python test_app.py

# Test the web interface
cd flask_app
python app.py
# Then visit http://localhost:5002
```

### Load Testing

Use Apache Bench for load testing:

```bash
# Test single sentence endpoint
ab -n 100 -c 10 -p test_data.json -T application/json http://localhost:5002/analyze_sentence

# Test file upload endpoint
ab -n 50 -c 5 -p test_file.csv -T multipart/form-data http://localhost:5002/predict
```

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin master

# Update dependencies
pip install -r requirements.txt

# Restart the application
sudo systemctl restart hotel-reviews-absa
```

### Backup Strategy

```bash
# Backup model files
tar -czf hotel_reviews_model_backup_$(date +%Y%m%d).tar.gz hotel_reviews_model/

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/
```

## 📞 Support

For deployment issues:

1. Check the logs: `tail -f logs/hotel_reviews.log`
2. Verify model files exist: `ls -la hotel_reviews_model/`
3. Test the model: `python test_app.py`
4. Check system resources: `htop`, `df -h`

## 🎯 Production Checklist

- [ ] Model trained and tested
- [ ] Web server configured (Nginx/Apache)
- [ ] SSL certificate installed
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Rate limiting enabled
- [ ] Error handling tested
- [ ] Performance optimized
- [ ] Security measures in place

---

**🚀 Your Hotel Reviews ABSA application is now ready for production!** 