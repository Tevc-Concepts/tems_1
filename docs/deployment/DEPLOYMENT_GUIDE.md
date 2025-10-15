# TEMS Platform Deployment Guide

**Version:** 1.0  
**Date:** October 15, 2025  
**Target Environment:** Production Server (Ubuntu/Debian Linux)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Pre-Deployment Checklist](#pre-deployment-checklist)
4. [Installation Steps](#installation-steps)
5. [Database Configuration](#database-configuration)
6. [Security Configuration](#security-configuration)
7. [Web Server Setup (nginx)](#web-server-setup-nginx)
8. [SSL/HTTPS Configuration](#sslhttps-configuration)
9. [Application Deployment](#application-deployment)
10. [Service Management](#service-management)
11. [Monitoring & Logging](#monitoring--logging)
12. [Backup Configuration](#backup-configuration)
13. [Post-Deployment Verification](#post-deployment-verification)
14. [Troubleshooting](#troubleshooting)
15. [Rollback Procedures](#rollback-procedures)

---

## Prerequisites

### Required Knowledge
- Linux system administration
- Command line interface (CLI) proficiency
- Basic understanding of web servers (nginx)
- Familiarity with Python applications
- Database management concepts

### Access Requirements
- Root/sudo access to production server
- Domain name configured and pointing to server
- SSH access to server
- Git repository access (GitHub)

### Tools Required
- Terminal/SSH client
- Text editor (nano, vim, or VS Code)
- Git client

---

## System Requirements

### Minimum Server Specifications

| Component | Requirement |
|-----------|-------------|
| **OS** | Ubuntu 20.04+ / Debian 11+ |
| **CPU** | 4 cores |
| **RAM** | 8 GB |
| **Storage** | 50 GB SSD |
| **Network** | 100 Mbps |

### Recommended Server Specifications

| Component | Requirement |
|-----------|-------------|
| **OS** | Ubuntu 22.04 LTS |
| **CPU** | 8 cores |
| **RAM** | 16 GB |
| **Storage** | 100 GB SSD |
| **Network** | 1 Gbps |

### Software Dependencies

- **Python:** 3.10 or 3.11
- **Node.js:** 18.x or 20.x
- **MariaDB/MySQL:** 10.6+
- **Redis:** 6.0+
- **nginx:** 1.18+
- **wkhtmltopdf:** 0.12.6 (with patched qt)

---

## Pre-Deployment Checklist

### ✅ Before You Begin

- [ ] Server provisioned and accessible via SSH
- [ ] Domain name configured (DNS A record pointing to server IP)
- [ ] SSL certificate ready (or Let's Encrypt will be configured)
- [ ] Database credentials prepared
- [ ] Email service configured (for notifications)
- [ ] Backup storage prepared
- [ ] Git repository access verified
- [ ] All team members notified of deployment window
- [ ] Downtime window scheduled (if replacing existing system)

### ✅ Documentation Ready

- [ ] This deployment guide
- [ ] `PRODUCTION_SECURITY_SETUP.md` (security hardening)
- [ ] `SECURITY_AUDIT_REPORT.md` (security assessment)
- [ ] `PERFORMANCE_AUDIT_REPORT.md` (performance baseline)
- [ ] ERPNext site credentials
- [ ] Admin user credentials

---

## Installation Steps

### Step 1: Prepare the Server

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install basic utilities
sudo apt-get install -y git curl wget nano htop
```

### Step 2: Install Frappe/ERPNext Bench

#### Option A: Production Install Script (Recommended)

```bash
# Install Frappe Bench using production installer
sudo apt-get install -y python3-minimal python3-pip
sudo pip3 install frappe-bench

# Create frappe user
sudo adduser frappe --disabled-password --gecos "Frappe User"
sudo usermod -aG sudo frappe

# Switch to frappe user
sudo su - frappe

# Initialize bench
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
```

#### Option B: Manual Installation

See Frappe documentation: https://frappeframework.com/docs/user/en/installation

### Step 3: Install ERPNext and Dependencies

```bash
# Install ERPNext
bench get-app erpnext --branch version-15

# Install HRMS
bench get-app hrms --branch version-15

# Install Frappe Drive
bench get-app drive https://github.com/frappe/drive

# Install Frappe Insights (optional)
bench get-app insights https://github.com/frappe/insights
```

### Step 4: Install TEMS Custom App

```bash
# Clone TEMS repository
bench get-app tems https://github.com/Gabcelltd/tems.git

# Or if using local development version
cd apps
git clone https://github.com/Gabcelltd/tems.git
cd ..
```

### Step 5: Create Production Site

```bash
# Create new site (replace with your domain)
bench new-site tems.yourdomain.com

# When prompted, enter:
# - MariaDB root password
# - Administrator password (save this securely!)

# Install apps on the site
bench --site tems.yourdomain.com install-app erpnext
bench --site tems.yourdomain.com install-app hrms
bench --site tems.yourdomain.com install-app drive
bench --site tems.yourdomain.com install-app tems

# Run migrations
bench --site tems.yourdomain.com migrate
```

---

## Database Configuration

### Step 1: Secure MariaDB Installation

```bash
# Run security script
sudo mysql_secure_installation
```

Answer the prompts:
- Set root password: **YES**
- Remove anonymous users: **YES**
- Disallow root login remotely: **YES**
- Remove test database: **YES**
- Reload privilege tables: **YES**

### Step 2: Optimize Database Settings

Edit MariaDB configuration:

```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Add under `[mysqld]` section:

```ini
[mysqld]
# Performance tuning
max_connections = 200
innodb_buffer_pool_size = 2G
innodb_log_file_size = 512M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT

# Character set
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Barracuda file format
innodb_file_format = Barracuda
innodb_file_per_table = 1
innodb_large_prefix = 1
```

Restart MariaDB:

```bash
sudo systemctl restart mariadb
```

### Step 3: Database Backup Configuration

```bash
# Create backup directory
mkdir -p ~/frappe-bench/sites/tems.yourdomain.com/private/backups

# Configure automated backups (see Backup Configuration section)
```

---

## Security Configuration

### Step 1: Disable Developer Mode

```bash
cd ~/frappe-bench

# Disable developer mode
bench --site tems.yourdomain.com set-config developer_mode 0
bench --site tems.yourdomain.com set-config allow_error_traceback 0

# Enable production settings
bench --site tems.yourdomain.com set-config deny_multiple_sessions 1
bench --site tems.yourdomain.com set-config disable_error_mail 0
```

### Step 2: Configure Session Security

Edit site configuration:

```bash
nano sites/tems.yourdomain.com/site_config.json
```

Add these security settings:

```json
{
  "developer_mode": 0,
  "allow_error_traceback": 0,
  "deny_multiple_sessions": 1,
  "session_expiry": "06:00:00",
  "session_expiry_mobile": "168:00:00",
  "cookie_secure": 1,
  "cookie_httponly": 1,
  "cookie_samesite": "Lax"
}
```

### Step 3: Configure Firewall (UFW)

```bash
# Enable firewall
sudo ufw enable

# Allow SSH (IMPORTANT: do this first!)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow only local connections to database
sudo ufw allow from 127.0.0.1 to any port 3306

# Allow only local connections to Redis
sudo ufw allow from 127.0.0.1 to any port 11000
sudo ufw allow from 127.0.0.1 to any port 13000

# Check status
sudo ufw status verbose
```

### Step 4: Configure Fail2Ban (Brute Force Protection)

```bash
# Install fail2ban
sudo apt-get install -y fail2ban

# Create Frappe filter
sudo nano /etc/fail2ban/filter.d/frappe.conf
```

Add:

```ini
[Definition]
failregex = ^.*Login failed for.*<HOST>.*$
            ^.*Authentication failed.*<HOST>.*$
ignoreregex =
```

Create jail configuration:

```bash
sudo nano /etc/fail2ban/jail.d/frappe.conf
```

Add:

```ini
[frappe]
enabled = true
port = http,https
filter = frappe
logpath = /home/frappe/frappe-bench/logs/*.log
maxretry = 5
findtime = 600
bantime = 3600
```

Restart fail2ban:

```bash
sudo systemctl restart fail2ban
sudo fail2ban-client status frappe
```

---

## Web Server Setup (nginx)

### Step 1: Install nginx

```bash
sudo apt-get install -y nginx
```

### Step 2: Generate nginx Configuration

```bash
cd ~/frappe-bench

# Generate production nginx config
bench setup nginx

# This creates: /etc/nginx/sites-available/frappe-bench.conf
```

### Step 3: Customize nginx Configuration

Edit the generated configuration:

```bash
sudo nano /etc/nginx/sites-available/frappe-bench.conf
```

Add security headers in the server block:

```nginx
# Security Headers
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Content Security Policy
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' wss:; frame-ancestors 'self';" always;
```

### Step 4: Enable nginx Configuration

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/frappe-bench.conf /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# If OK, reload nginx
sudo systemctl reload nginx
```

### Step 5: Configure Rate Limiting (Optional)

Add to nginx configuration before server blocks:

```nginx
# Rate limiting zones
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;

server {
    # ... existing config ...
    
    # Apply rate limiting to API endpoints
    location ~ ^/api/ {
        limit_req zone=api_limit burst=20 nodelay;
        # ... existing proxy config ...
    }
    
    # Stricter limit for login endpoint
    location /api/method/login {
        limit_req zone=login_limit burst=5 nodelay;
        # ... existing proxy config ...
    }
}
```

---

## SSL/HTTPS Configuration

### Option A: Let's Encrypt (Recommended for Production)

```bash
# Install certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Obtain certificate (replace with your domain)
sudo certbot --nginx -d tems.yourdomain.com

# Follow prompts:
# - Enter email address
# - Agree to terms
# - Choose whether to redirect HTTP to HTTPS (recommended: YES)

# Test auto-renewal
sudo certbot renew --dry-run

# Certificates auto-renew via systemd timer
sudo systemctl status certbot.timer
```

### Option B: Custom SSL Certificate

If you have your own SSL certificate:

```bash
# Copy certificate files to server
sudo mkdir -p /etc/ssl/tems
sudo cp your-certificate.crt /etc/ssl/tems/cert.crt
sudo cp your-private-key.key /etc/ssl/tems/key.key
sudo cp your-ca-bundle.crt /etc/ssl/tems/ca-bundle.crt

# Set permissions
sudo chmod 600 /etc/ssl/tems/key.key
sudo chmod 644 /etc/ssl/tems/cert.crt
sudo chmod 644 /etc/ssl/tems/ca-bundle.crt
```

Edit nginx configuration:

```nginx
server {
    listen 443 ssl http2;
    server_name tems.yourdomain.com;
    
    ssl_certificate /etc/ssl/tems/cert.crt;
    ssl_certificate_key /etc/ssl/tems/key.key;
    ssl_trusted_certificate /etc/ssl/tems/ca-bundle.crt;
    
    # SSL optimization
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # ... rest of config ...
}
```

### Step 3: Force HTTPS Redirect

Ensure nginx redirects HTTP to HTTPS:

```nginx
server {
    listen 80;
    server_name tems.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Application Deployment

### Step 1: Build Frontend Assets

```bash
cd ~/frappe-bench

# Build all assets
bench build

# This compiles:
# - PWA applications (Operations, Safety, Fleet, Driver)
# - CSS/JS assets
# - Static files
```

### Step 2: Setup Production Mode

```bash
# Setup production configuration
bench setup production frappe

# This configures:
# - Supervisor for process management
# - nginx for web server
# - systemd services
```

### Step 3: Configure Supervisor

Check supervisor configuration:

```bash
sudo nano /etc/supervisor/conf.d/frappe-bench.conf
```

Ensure processes are configured:

```ini
[group:frappe-bench-web]
programs=frappe-bench-frappe-web,frappe-bench-node-socketio

[group:frappe-bench-workers]
programs=frappe-bench-frappe-schedule,frappe-bench-frappe-default-worker,frappe-bench-frappe-short-worker,frappe-bench-frappe-long-worker

[program:frappe-bench-frappe-web]
command=/home/frappe/frappe-bench/env/bin/gunicorn -b 127.0.0.1:8000 -w 4 --max-requests 5000 --max-requests-jitter 500 -t 120 frappe.app:application --preload
# ... rest of config ...
```

Reload supervisor:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

### Step 4: Enable Scheduled Jobs

```bash
# Enable scheduler
bench --site tems.yourdomain.com enable-scheduler

# Verify scheduler is running
bench --site tems.yourdomain.com doctor
```

---

## Service Management

### Starting Services

```bash
# Start all services
sudo supervisorctl start all

# Or individually
sudo supervisorctl start frappe-bench-web:*
sudo supervisorctl start frappe-bench-workers:*
```

### Stopping Services

```bash
# Stop all services
sudo supervisorctl stop all

# Or individually
sudo supervisorctl stop frappe-bench-web:*
sudo supervisorctl stop frappe-bench-workers:*
```

### Restarting Services

```bash
# Restart all
sudo supervisorctl restart all

# Or use bench command
cd ~/frappe-bench
bench restart
```

### Checking Service Status

```bash
# Check all services
sudo supervisorctl status

# Check specific service
sudo supervisorctl status frappe-bench-frappe-web
```

### Viewing Logs

```bash
# Supervisor logs
sudo tail -f /var/log/supervisor/supervisord.log

# Frappe logs
cd ~/frappe-bench
tail -f logs/web.log
tail -f logs/worker.log
tail -f logs/scheduler.log

# nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## Monitoring & Logging

### Step 1: Configure Log Rotation

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/frappe
```

Add:

```
/home/frappe/frappe-bench/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 frappe frappe
    sharedscripts
    postrotate
        sudo supervisorctl restart frappe-bench-web:* > /dev/null 2>&1 || true
    endscript
}
```

### Step 2: Install Monitoring Tools

```bash
# Install htop for process monitoring
sudo apt-get install -y htop

# Install logwatch for log analysis
sudo apt-get install -y logwatch

# Configure daily reports
sudo logwatch --detail high --mailto admin@yourdomain.com --service all --range today
```

### Step 3: Setup System Monitoring

Create monitoring script:

```bash
nano ~/monitor-tems.sh
```

Add:

```bash
#!/bin/bash
echo "=== TEMS System Status ==="
echo "Date: $(date)"
echo ""
echo "=== Supervisor Status ==="
sudo supervisorctl status
echo ""
echo "=== Disk Usage ==="
df -h | grep -E '^/dev/'
echo ""
echo "=== Memory Usage ==="
free -h
echo ""
echo "=== CPU Load ==="
uptime
echo ""
echo "=== Database Status ==="
sudo systemctl status mariadb | grep Active
echo ""
echo "=== nginx Status ==="
sudo systemctl status nginx | grep Active
```

Make executable:

```bash
chmod +x ~/monitor-tems.sh
```

### Step 4: Setup Automated Health Checks

Add to crontab:

```bash
crontab -e
```

Add:

```bash
# Health check every 5 minutes
*/5 * * * * curl -f http://localhost:8000/api/method/ping > /dev/null 2>&1 || echo "TEMS is down!" | mail -s "TEMS Alert" admin@yourdomain.com

# Daily monitoring report
0 8 * * * ~/monitor-tems.sh | mail -s "TEMS Daily Report" admin@yourdomain.com
```

---

## Backup Configuration

### Step 1: Configure Automated Backups

```bash
# Create backup script
nano ~/frappe-bench/backup-tems.sh
```

Add:

```bash
#!/bin/bash
# TEMS Backup Script

SITE="tems.yourdomain.com"
BENCH_PATH="/home/frappe/frappe-bench"
BACKUP_DIR="/home/frappe/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Navigate to bench
cd $BENCH_PATH

# Backup database and files
bench --site $SITE backup --with-files

# Copy to backup directory
cp sites/$SITE/private/backups/* $BACKUP_DIR/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*-files.tar" -mtime +7 -delete

# Log backup
echo "$DATE - Backup completed" >> $BACKUP_DIR/backup.log
```

Make executable:

```bash
chmod +x ~/frappe-bench/backup-tems.sh
```

### Step 2: Schedule Automated Backups

```bash
crontab -e
```

Add:

```bash
# Daily backup at 2 AM
0 2 * * * /home/frappe/frappe-bench/backup-tems.sh

# Weekly full backup (Sundays at 3 AM)
0 3 * * 0 /home/frappe/frappe-bench/backup-tems.sh
```

### Step 3: Configure Offsite Backups (Recommended)

Install rclone:

```bash
curl https://rclone.org/install.sh | sudo bash
```

Configure rclone for your cloud storage:

```bash
rclone config
```

Update backup script to sync to cloud:

```bash
# Add to end of backup-tems.sh
rclone sync $BACKUP_DIR remote:tems-backups/
```

---

## Post-Deployment Verification

### Step 1: Verify Services are Running

```bash
# Check supervisor processes
sudo supervisorctl status

# Expected output: All processes should be RUNNING
# frappe-bench-frappe-web          RUNNING
# frappe-bench-node-socketio       RUNNING
# frappe-bench-frappe-schedule     RUNNING
# frappe-bench-frappe-default-worker RUNNING
# frappe-bench-frappe-short-worker RUNNING
# frappe-bench-frappe-long-worker  RUNNING
```

### Step 2: Verify Database Connection

```bash
cd ~/frappe-bench
bench --site tems.yourdomain.com console
```

In console:

```python
frappe.db.sql("SELECT 1")
# Should return: ((1,),)
exit()
```

### Step 3: Verify Web Access

```bash
# Test HTTP response
curl -I http://localhost:8000

# Test HTTPS (replace with your domain)
curl -I https://tems.yourdomain.com

# Expected: HTTP/1.1 200 OK or HTTP/2 200
```

### Step 4: Verify PWA Accessibility

Test each PWA:

```bash
# Operations PWA
curl -I https://tems.yourdomain.com/assets/tems/frontend/operations-pwa/dist/index.html

# Safety PWA
curl -I https://tems.yourdomain.com/assets/tems/frontend/safety-pwa/dist/index.html

# Fleet PWA
curl -I https://tems.yourdomain.com/assets/tems/frontend/fleet-pwa/dist/index.html

# Driver PWA
curl -I https://tems.yourdomain.com/assets/tems/frontend/driver-pwa/dist/index.html

# All should return: HTTP/2 200
```

### Step 5: Verify API Endpoints

```bash
# Test API (requires authentication)
curl -X POST https://tems.yourdomain.com/api/method/login \
  -H "Content-Type: application/json" \
  -d '{"usr":"administrator","pwd":"your-password"}'

# Should return: Success message with session info
```

### Step 6: Run System Health Check

```bash
cd ~/frappe-bench
bench --site tems.yourdomain.com doctor

# Check output for any issues
```

### Step 7: Verify Security Configuration

```bash
# Test security headers
curl -I https://tems.yourdomain.com | grep -E 'X-Content-Type-Options|X-Frame-Options|Content-Security-Policy|Strict-Transport-Security'

# Expected: All security headers should be present
```

### Step 8: Test Backup System

```bash
# Run manual backup
~/frappe-bench/backup-tems.sh

# Verify backup files created
ls -lh ~/backups/

# Should show recent .sql.gz and .tar files
```

### Step 9: Verify Scheduled Jobs

```bash
# Check scheduler status
bench --site tems.yourdomain.com ready-for-migration
bench --site tems.yourdomain.com scheduler status

# Expected: Scheduler should be active
```

### Step 10: Performance Smoke Test

```bash
# Measure page load time
time curl -s https://tems.yourdomain.com > /dev/null

# Should complete in < 1 second
```

---

## Troubleshooting

### Issue: Services Won't Start

**Symptoms:**
- `supervisorctl status` shows FATAL or STOPPED
- Application inaccessible

**Solutions:**

```bash
# Check logs
sudo tail -f /var/log/supervisor/supervisord.log

# Check individual service logs
cd ~/frappe-bench
tail -f logs/web.error.log
tail -f logs/worker.error.log

# Restart services
sudo supervisorctl restart all

# If still failing, check bench
bench doctor
```

### Issue: Database Connection Error

**Symptoms:**
- "Database connection failed" errors
- Can't access application

**Solutions:**

```bash
# Check MariaDB status
sudo systemctl status mariadb

# Restart MariaDB
sudo systemctl restart mariadb

# Check database credentials
nano ~/frappe-bench/sites/tems.yourdomain.com/site_config.json

# Test database connection
mysql -u root -p
```

### Issue: nginx 502 Bad Gateway

**Symptoms:**
- nginx shows 502 error
- Application not responding

**Solutions:**

```bash
# Check if gunicorn is running
sudo supervisorctl status frappe-bench-frappe-web

# Check port 8000 is listening
sudo netstat -tlnp | grep 8000

# Check nginx error log
sudo tail -f /var/log/nginx/error.log

# Restart web workers
sudo supervisorctl restart frappe-bench-web:*
```

### Issue: SSL Certificate Error

**Symptoms:**
- Browser shows "Not Secure"
- Certificate warnings

**Solutions:**

```bash
# Check certificate expiry
sudo certbot certificates

# Renew certificate
sudo certbot renew

# If using Let's Encrypt and renewal fails
sudo certbot --nginx -d tems.yourdomain.com --force-renewal
```

### Issue: Slow Performance

**Symptoms:**
- Pages load slowly
- High CPU/memory usage

**Solutions:**

```bash
# Check system resources
htop

# Check database queries
cd ~/frappe-bench
bench --site tems.yourdomain.com mariadb
# Run: SHOW PROCESSLIST;

# Clear cache
bench --site tems.yourdomain.com clear-cache

# Rebuild assets
bench build

# Restart services
bench restart
```

### Issue: Scheduler Not Running

**Symptoms:**
- Scheduled tasks not executing
- Background jobs not processing

**Solutions:**

```bash
# Check scheduler status
bench --site tems.yourdomain.com enable-scheduler

# Check worker status
sudo supervisorctl status | grep worker

# Restart scheduler
sudo supervisorctl restart frappe-bench-frappe-schedule
```

### Issue: File Upload Errors

**Symptoms:**
- Can't upload files
- "Permission denied" errors

**Solutions:**

```bash
# Check file permissions
ls -la ~/frappe-bench/sites/tems.yourdomain.com/

# Fix permissions
cd ~/frappe-bench
bench setup sudoers
sudo chown -R frappe:frappe sites/

# Check disk space
df -h
```

---

## Rollback Procedures

### Quick Rollback (Application Issue)

If deployment causes application issues:

```bash
cd ~/frappe-bench

# Stop services
bench --site tems.yourdomain.com set-maintenance-mode on

# Restore from last backup
bench --site tems.yourdomain.com restore /path/to/backup.sql.gz

# Restart services
bench restart
bench --site tems.yourdomain.com set-maintenance-mode off
```

### Full Rollback (Database Restore)

If database corruption or data loss:

```bash
# Enable maintenance mode
bench --site tems.yourdomain.com set-maintenance-mode on

# Restore database
bench --site tems.yourdomain.com restore /path/to/backup-YYYY-MM-DD.sql.gz

# Restore files (if needed)
cd sites/tems.yourdomain.com
tar -xvf /path/to/backup-YYYY-MM-DD-files.tar

# Clear cache and rebuild
bench --site tems.yourdomain.com clear-cache
bench build

# Restart services
bench restart

# Disable maintenance mode
bench --site tems.yourdomain.com set-maintenance-mode off
```

### Code Rollback (Git)

If TEMS app code has issues:

```bash
cd ~/frappe-bench/apps/tems

# Check git log
git log --oneline

# Rollback to previous commit
git reset --hard <previous-commit-hash>

# Rebuild assets
cd ~/frappe-bench
bench build

# Restart
bench restart
```

---

## Appendix

### A. Useful Commands Reference

```bash
# Bench commands
bench start                    # Start development server
bench restart                  # Restart production services
bench migrate                  # Run database migrations
bench build                    # Build frontend assets
bench clear-cache              # Clear application cache

# Site commands
bench --site SITE migrate      # Migrate specific site
bench --site SITE console      # Open Python console
bench --site SITE mariadb      # Open MySQL console
bench --site SITE backup       # Create backup

# Service management
sudo supervisorctl status      # Check all services
sudo supervisorctl restart all # Restart all services
sudo supervisorctl tail -f PROCESS # Follow log

# nginx
sudo nginx -t                  # Test configuration
sudo systemctl reload nginx    # Reload configuration
sudo systemctl restart nginx   # Restart nginx

# Database
sudo systemctl status mariadb  # Check database status
sudo systemctl restart mariadb # Restart database
```

### B. Configuration File Locations

| File | Location |
|------|----------|
| Site Config | `~/frappe-bench/sites/SITE/site_config.json` |
| Common Site Config | `~/frappe-bench/sites/common_site_config.json` |
| nginx Config | `/etc/nginx/sites-available/frappe-bench.conf` |
| Supervisor Config | `/etc/supervisor/conf.d/frappe-bench.conf` |
| SSL Certificates | `/etc/letsencrypt/live/DOMAIN/` |
| Logs | `~/frappe-bench/logs/` |
| Backups | `~/frappe-bench/sites/SITE/private/backups/` |

### C. Support Resources

- **Frappe Documentation:** https://frappeframework.com/docs
- **ERPNext Documentation:** https://docs.erpnext.com
- **Frappe Forum:** https://discuss.frappe.io
- **TEMS Repository:** https://github.com/Gabcelltd/tems
- **Security Guide:** `PRODUCTION_SECURITY_SETUP.md`
- **Performance Report:** `PERFORMANCE_AUDIT_REPORT.md`

---

**Document Version:** 1.0  
**Last Updated:** October 15, 2025  
**Maintained By:** TEMS Development Team  
**Next Review:** Post-deployment feedback
