# Infrastructure Issue Reporter - Deployment Guide

This guide provides detailed instructions for deploying the Infrastructure Issue Reporter application in various environments.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Windows Deployment](#windows-deployment)
3. [Linux Deployment](#linux-deployment)
4. [macOS Deployment](#macos-deployment)
5. [Network Configuration](#network-configuration)
6. [Production Deployment](#production-deployment)
7. [Backup and Maintenance](#backup-and-maintenance)
8. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **CPU**: 1 GHz processor
- **RAM**: 2 GB RAM
- **Storage**: 1 GB free disk space
- **Network**: Local network access (for LAN deployment)
- **Operating System**: Windows 10+, Ubuntu 18.04+, macOS 10.14+

### Recommended Requirements
- **CPU**: 2 GHz dual-core processor
- **RAM**: 4 GB RAM
- **Storage**: 5 GB free disk space (for photos and database growth)
- **Network**: Gigabit Ethernet for optimal performance

### Software Dependencies
- Python 3.8 or higher
- pip (Python package installer)
- Web browser (Chrome, Firefox, Safari, Edge)

## Windows Deployment

### Step 1: Install Python

1. **Download Python**:
   - Visit https://www.python.org/downloads/
   - Download Python 3.8 or higher for Windows
   - **Important**: Check "Add Python to PATH" during installation

2. **Verify Installation**:
   ```cmd
   python --version
   pip --version
   ```

### Step 2: Set Up the Application

1. **Extract the Application**:
   - Extract the infrastructure-reporter folder to `C:\infrastructure-reporter`

2. **Open Command Prompt as Administrator**:
   ```cmd
   cd C:\infrastructure-reporter
   ```

3. **Create Virtual Environment**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install Dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

5. **Create Demo Data**:
   ```cmd
   python create_demo_data.py
   ```

6. **Start the Application**:
   ```cmd
   python src\main.py
   ```

### Step 3: Create Windows Service (Optional)

For automatic startup, create a Windows service:

1. **Install NSSM** (Non-Sucking Service Manager):
   - Download from https://nssm.cc/download
   - Extract to `C:\nssm`

2. **Create Service**:
   ```cmd
   C:\nssm\nssm.exe install InfrastructureReporter
   ```

3. **Configure Service**:
   - Path: `C:\infrastructure-reporter\venv\Scripts\python.exe`
   - Arguments: `C:\infrastructure-reporter\src\main.py`
   - Startup directory: `C:\infrastructure-reporter`

### Step 4: Windows Firewall Configuration

1. **Open Windows Defender Firewall**
2. **Click "Advanced settings"**
3. **Create Inbound Rule**:
   - Rule Type: Port
   - Protocol: TCP
   - Port: 5001
   - Action: Allow the connection
   - Profile: All profiles
   - Name: Infrastructure Reporter

## Linux Deployment

### Step 1: Install Dependencies

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```

#### CentOS/RHEL:
```bash
sudo yum install python3 python3-pip git
# or for newer versions:
sudo dnf install python3 python3-pip git
```

### Step 2: Set Up the Application

1. **Extract and Navigate**:
   ```bash
   cd /opt
   sudo mkdir infrastructure-reporter
   sudo chown $USER:$USER infrastructure-reporter
   cd infrastructure-reporter
   # Extract files here
   ```

2. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Demo Data**:
   ```bash
   python create_demo_data.py
   ```

5. **Test the Application**:
   ```bash
   python src/main.py
   ```

### Step 3: Create Systemd Service

1. **Create Service File**:
   ```bash
   sudo nano /etc/systemd/system/infrastructure-reporter.service
   ```

2. **Add Service Configuration**:
   ```ini
   [Unit]
   Description=Infrastructure Issue Reporter
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/infrastructure-reporter
   Environment=PATH=/opt/infrastructure-reporter/venv/bin
   ExecStart=/opt/infrastructure-reporter/venv/bin/python src/main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and Start Service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable infrastructure-reporter
   sudo systemctl start infrastructure-reporter
   sudo systemctl status infrastructure-reporter
   ```

### Step 4: Configure Firewall

#### UFW (Ubuntu):
```bash
sudo ufw allow 5001
sudo ufw reload
```

#### Firewalld (CentOS/RHEL):
```bash
sudo firewall-cmd --permanent --add-port=5001/tcp
sudo firewall-cmd --reload
```

## macOS Deployment

### Step 1: Install Prerequisites

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**:
   ```bash
   brew install python
   ```

### Step 2: Set Up Application

1. **Navigate to Application Directory**:
   ```bash
   cd /Applications
   mkdir infrastructure-reporter
   cd infrastructure-reporter
   # Extract files here
   ```

2. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Demo Data**:
   ```bash
   python create_demo_data.py
   ```

5. **Start Application**:
   ```bash
   python src/main.py
   ```

### Step 3: Create Launch Agent (Optional)

1. **Create Plist File**:
   ```bash
   nano ~/Library/LaunchAgents/com.infrastructure.reporter.plist
   ```

2. **Add Configuration**:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.infrastructure.reporter</string>
       <key>ProgramArguments</key>
       <array>
           <string>/Applications/infrastructure-reporter/venv/bin/python</string>
           <string>/Applications/infrastructure-reporter/src/main.py</string>
       </array>
       <key>WorkingDirectory</key>
       <string>/Applications/infrastructure-reporter</string>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
   </dict>
   </plist>
   ```

3. **Load Launch Agent**:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.infrastructure.reporter.plist
   ```

## Network Configuration

### Local Network Access

1. **Find Your IP Address**:
   ```bash
   # Windows
   ipconfig
   
   # Linux/macOS
   ifconfig
   # or
   ip addr show
   ```

2. **Update Flask Configuration**:
   Edit `src/main.py` and change:
   ```python
   app.run(host='0.0.0.0', port=5001, debug=False)
   ```

3. **Access from Other Devices**:
   - Use your IP address: `http://192.168.1.100:5001`
   - Replace `192.168.1.100` with your actual IP address

### Port Configuration

To use a different port, update `src/main.py`:
```python
app.run(host='0.0.0.0', port=8080, debug=False)  # Use port 8080
```

## Production Deployment

### Using Gunicorn (Recommended for Linux)

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn Configuration**:
   ```bash
   nano gunicorn.conf.py
   ```

   ```python
   bind = "0.0.0.0:5001"
   workers = 4
   worker_class = "sync"
   worker_connections = 1000
   max_requests = 1000
   max_requests_jitter = 100
   timeout = 30
   keepalive = 2
   preload_app = True
   ```

3. **Start with Gunicorn**:
   ```bash
   gunicorn -c gunicorn.conf.py src.main:app
   ```

### Using Nginx Reverse Proxy

1. **Install Nginx**:
   ```bash
   # Ubuntu/Debian
   sudo apt install nginx
   
   # CentOS/RHEL
   sudo yum install nginx
   ```

2. **Create Nginx Configuration**:
   ```bash
   sudo nano /etc/nginx/sites-available/infrastructure-reporter
   ```

   ```nginx
   server {
       listen 80;
       server_name your-server-ip;

       location / {
           proxy_pass http://127.0.0.1:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static {
           alias /opt/infrastructure-reporter/src/static;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   ```

3. **Enable Site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/infrastructure-reporter /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Backup and Maintenance

### Database Backup

1. **Create Backup Script**:
   ```bash
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   BACKUP_DIR="/opt/backups/infrastructure-reporter"
   mkdir -p $BACKUP_DIR
   
   # Backup database
   cp /opt/infrastructure-reporter/src/database/app.db $BACKUP_DIR/app_$DATE.db
   
   # Backup uploads
   tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /opt/infrastructure-reporter/src/static/uploads/
   
   # Keep only last 30 days of backups
   find $BACKUP_DIR -name "*.db" -mtime +30 -delete
   find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
   ```

2. **Schedule with Cron**:
   ```bash
   crontab -e
   # Add line for daily backup at 2 AM:
   0 2 * * * /opt/infrastructure-reporter/backup.sh
   ```

### Log Rotation

1. **Create Logrotate Configuration**:
   ```bash
   sudo nano /etc/logrotate.d/infrastructure-reporter
   ```

   ```
   /var/log/infrastructure-reporter/*.log {
       daily
       missingok
       rotate 52
       compress
       delaycompress
       notifempty
       create 644 www-data www-data
   }
   ```

### Updates and Maintenance

1. **Update Dependencies**:
   ```bash
   source venv/bin/activate
   pip install --upgrade -r requirements.txt
   ```

2. **Monitor Disk Space**:
   ```bash
   df -h
   du -sh /opt/infrastructure-reporter/src/static/uploads/
   ```

3. **Monitor Application**:
   ```bash
   # Check service status
   sudo systemctl status infrastructure-reporter
   
   # View logs
   sudo journalctl -u infrastructure-reporter -f
   ```

## Troubleshooting

### Common Issues

1. **Application Won't Start**:
   ```bash
   # Check Python version
   python --version
   
   # Check if port is in use
   netstat -tulpn | grep :5001
   
   # Check permissions
   ls -la src/database/
   ls -la src/static/uploads/
   ```

2. **Database Errors**:
   ```bash
   # Reset database
   rm src/database/app.db
   python create_demo_data.py
   ```

3. **Permission Issues**:
   ```bash
   # Fix permissions
   sudo chown -R www-data:www-data /opt/infrastructure-reporter
   sudo chmod -R 755 /opt/infrastructure-reporter
   sudo chmod -R 777 /opt/infrastructure-reporter/src/static/uploads
   ```

4. **Network Access Issues**:
   - Check firewall settings
   - Verify IP address configuration
   - Test with `curl http://localhost:5001`

### Performance Optimization

1. **Database Optimization**:
   - Regular VACUUM operations for SQLite
   - Monitor database size growth
   - Consider PostgreSQL for large deployments

2. **File Storage**:
   - Implement image compression
   - Set up automatic cleanup of old files
   - Monitor disk usage

3. **Network Performance**:
   - Use CDN for static assets in large deployments
   - Implement caching strategies
   - Optimize image sizes

### Security Hardening

1. **Change Default Credentials**:
   ```python
   # In Python shell
   from src.models.user import User
   from src.main import app
   
   with app.app_context():
       admin = User.query.filter_by(username='admin').first()
       admin.set_password('new_secure_password')
       db.session.commit()
   ```

2. **SSL/HTTPS Setup**:
   - Obtain SSL certificate
   - Configure Nginx with SSL
   - Redirect HTTP to HTTPS

3. **Regular Updates**:
   - Keep Python and dependencies updated
   - Monitor security advisories
   - Regular security audits

---

This deployment guide covers the most common scenarios for deploying the Infrastructure Issue Reporter. For specific requirements or advanced configurations, consult the main README.md file or modify the deployment according to your organization's needs.

