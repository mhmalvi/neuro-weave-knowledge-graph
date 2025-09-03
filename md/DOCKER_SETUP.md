# 🐳 NeuroWeave Knowledge Graph - Docker Setup Guide

## 🚀 Quick Start

### **Prerequisites**
- Docker Desktop installed and running
- OpenAI API Key (required)
- GitHub Token (optional, improves rate limits)

### **1. Setup Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your keys:
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here  # Optional
```

### **2. Build and Run (Method 1 - Simple)**
```bash
# Build the Docker image
docker-build.bat

# Run the container
docker-run.bat
```

### **3. Docker Compose (Method 2 - Recommended)**
```bash
# Start complete stack
docker-compose-up.bat
```

### **4. Access Your App**
Open your browser: **http://localhost:8501**

---

## 🔧 Docker Commands

### **Basic Operations**
```bash
# Build image
docker build -t neuroweave-knowledge-graph:latest .

# Run container
docker run -d --name neuroweave-app --env-file .env -p 8501:8501 neuroweave-knowledge-graph:latest

# Stop container
docker stop neuroweave-app

# Remove container
docker rm neuroweave-app

# View logs
docker logs neuroweave-app -f
```

### **Docker Compose Operations**
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild and start
docker-compose up -d --build
```

---

## 📊 Container Features

### **Image Details**
- **Base Image**: python:3.11-slim
- **Size**: ~800MB (optimized)
- **User**: Non-root (neuroweave)
- **Port**: 8501
- **Health Check**: Included

### **Volumes**
- **visualizations**: Persistent storage for generated graphs
- **temp_repos**: Temporary GitHub repository clones

### **Environment Variables**
- `OPENAI_API_KEY`: Required for LLM processing
- `GITHUB_TOKEN`: Optional for GitHub API access
- `STREAMLIT_SERVER_PORT`: Default 8501
- `STREAMLIT_SERVER_ADDRESS`: Default 0.0.0.0

---

## 🔍 Troubleshooting

### **Common Issues**

**1. Container won't start**
```bash
# Check logs
docker logs neuroweave-app

# Common causes:
# - Missing OPENAI_API_KEY in .env
# - Port 8501 already in use
# - Docker Desktop not running
```

**2. Can't access app**
```bash
# Check if container is running
docker ps

# Check port mapping
docker port neuroweave-app

# Verify health status
docker exec neuroweave-app curl -f http://localhost:8501/_stcore/health
```

**3. GitHub cloning fails**
```bash
# Check if git is available in container
docker exec neuroweave-app git --version

# Check GitHub connectivity
docker exec neuroweave-app curl -s https://github.com
```

**4. Memory issues**
```bash
# Check container resource usage
docker stats neuroweave-app

# Increase Docker Desktop memory limit if needed (Settings > Resources)
```

---

## 🚀 Production Deployment

### **With NGINX Reverse Proxy**
```bash
# Start with production profile
docker-compose --profile production up -d

# Includes NGINX for:
# - Custom domain mapping
# - SSL/HTTPS support
# - Load balancing (future)
```

### **Environment Configuration**
```bash
# Production .env settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### **Security Considerations**
- Container runs as non-root user
- Minimal base image (python:slim)
- Health checks included
- No sensitive data in image
- Environment variables for secrets

---

## 📈 Monitoring

### **Health Checks**
```bash
# Manual health check
curl http://localhost:8501/_stcore/health

# Docker health status
docker inspect --format='{{.State.Health.Status}}' neuroweave-app
```

### **Resource Monitoring**
```bash
# Real-time stats
docker stats neuroweave-app

# Container resource limits
docker inspect neuroweave-app | grep -i memory
```

### **Log Management**
```bash
# View recent logs
docker logs neuroweave-app --tail 50

# Follow logs in real-time
docker logs neuroweave-app -f

# Export logs
docker logs neuroweave-app > neuroweave.log
```

---

## 🔄 Updates and Maintenance

### **Updating the Application**
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### **Cleanup**
```bash
# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Complete cleanup (careful!)
docker system prune -a
```

### **Backup**
```bash
# Backup persistent volumes
docker run --rm -v neuroweave-visualizations:/data -v $(pwd):/backup alpine tar czf /backup/visualizations-backup.tar.gz /data

# Restore from backup
docker run --rm -v neuroweave-visualizations:/data -v $(pwd):/backup alpine tar xzf /backup/visualizations-backup.tar.gz -C /
```

---

## 🎯 Advanced Usage

### **Custom Configuration**
```bash
# Run with custom Streamlit config
docker run -d --name neuroweave-app \
  --env-file .env \
  -p 8501:8501 \
  -v $(pwd)/streamlit-config.toml:/app/.streamlit/config.toml \
  neuroweave-knowledge-graph:latest
```

### **Development Mode**
```bash
# Mount source code for development
docker run -d --name neuroweave-dev \
  --env-file .env \
  -p 8501:8501 \
  -v $(pwd):/app \
  neuroweave-knowledge-graph:latest
```

### **Multi-Stage Deployment**
```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Staging
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

This setup provides a complete Docker containerization solution for the NeuroWeave Knowledge Graph application, making it easy to deploy, scale, and maintain in any environment!