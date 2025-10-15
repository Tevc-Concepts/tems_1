# TEMS Production Security Configuration Guide

This guide provides step-by-step instructions for configuring the security enhancements identified in the security audit.

---

## 1. Configure Security Headers (nginx)

### Location
Edit your nginx site configuration, typically:
- `/etc/nginx/sites-available/tems.local`
- `/etc/nginx/conf.d/tems.conf`

### Configuration
Add these headers to the `server` block:

```nginx
server {
    listen 443 ssl http2;
    server_name tems.local;
    
    # SSL Configuration (see section 2)
    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;
    
    # Security Headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Content Security Policy
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' wss:; frame-ancestors 'self';" always;
    
    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Existing proxy configuration...
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name tems.local;
    return 301 https://$server_name$request_uri;
}
```

### Apply Changes
```bash
# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

---

## 2. Enable HTTPS with SSL Certificate

### Option A: Let's Encrypt (Recommended for Production)

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d tems.local

# Auto-renewal (certbot sets this up automatically)
sudo certbot renew --dry-run
```

### Option B: Self-Signed Certificate (Development Only)

```bash
# Generate self-signed certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/tems.key \
  -out /etc/ssl/certs/tems.crt \
  -subj "/CN=tems.local"

# Update nginx config with paths
ssl_certificate /etc/ssl/certs/tems.crt;
ssl_certificate_key /etc/ssl/private/tems.key;
```

---

## 3. Configure Frappe Production Mode

### Edit Site Configuration
```bash
cd /workspace/development/frappe-bench
bench --site tems.local set-config developer_mode 0
bench --site tems.local set-config allow_error_traceback 0
```

### Or Edit Manually
Edit `sites/tems.local/site_config.json`:

```json
{
  "db_name": "...",
  "db_password": "...",
  "developer_mode": 0,
  "allow_error_traceback": 0,
  "disable_error_mail": 0,
  "server_script_enabled": 0,
  "deny_multiple_sessions": 1
}
```

### Common Site Config
Edit `sites/common_site_config.json`:

```json
{
  "developer_mode": 0,
  "allow_error_traceback": 0,
  "enable_frappe_logger": 1,
  "log_queries": 0,
  "background_workers": 1,
  "shallow_clone": true,
  "redis_cache": "redis://127.0.0.1:13000",
  "redis_queue": "redis://127.0.0.1:11000"
}
```

### Restart Services
```bash
bench restart
```

---

## 4. Configure Rate Limiting

### Method A: Frappe Built-in Rate Limiting

Edit `sites/common_site_config.json`:

```json
{
  "rate_limit": {
    "limit": 100,
    "window": 60
  },
  "rate_limit_whitelist": [
    "127.0.0.1",
    "::1"
  ]
}
```

This limits requests to 100 per 60 seconds per user.

### Method B: nginx Rate Limiting

Add to nginx configuration:

```nginx
# Define rate limit zone (outside server block)
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;

server {
    # ... existing config ...
    
    # Apply rate limiting to API endpoints
    location ~ ^/api/ {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://127.0.0.1:8000;
    }
    
    # Stricter limit for login endpoint
    location /api/method/login {
        limit_req zone=login_limit burst=5 nodelay;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### Restart nginx
```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 5. Configure Fail2Ban (Brute Force Protection)

### Install Fail2Ban
```bash
sudo apt-get install fail2ban
```

### Create Frappe Filter
Create `/etc/fail2ban/filter.d/frappe.conf`:

```ini
[Definition]
failregex = ^.*Login failed for.*<HOST>.*$
            ^.*Authentication failed.*<HOST>.*$
ignoreregex =
```

### Create Jail Configuration
Create `/etc/fail2ban/jail.d/frappe.conf`:

```ini
[frappe]
enabled = true
port = http,https
filter = frappe
logpath = /workspace/development/frappe-bench/logs/*.log
maxretry = 5
findtime = 600
bantime = 3600
```

### Restart Fail2Ban
```bash
sudo systemctl restart fail2ban
sudo fail2ban-client status frappe
```

---

## 6. Database Security

### Secure MariaDB/MySQL

```bash
# Run security script
sudo mysql_secure_installation
```

Answer prompts:
- Set root password: YES
- Remove anonymous users: YES
- Disallow root login remotely: YES
- Remove test database: YES
- Reload privilege tables: YES

### Restrict Database User Permissions

```sql
-- Connect to MySQL
mysql -u root -p

-- Check current permissions
SHOW GRANTS FOR 'erpnext_user'@'localhost';

-- Revoke unnecessary permissions
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'erpnext_user'@'localhost';

-- Grant only necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, 
      LOCK TABLES, EXECUTE, CREATE ROUTINE, ALTER ROUTINE
ON erpnext_db.* TO 'erpnext_user'@'localhost';

FLUSH PRIVILEGES;
```

---

## 7. Firewall Configuration (UFW)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
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

---

## 8. Session Security

### Configure Secure Sessions

Edit `sites/common_site_config.json`:

```json
{
  "session_expiry": "06:00:00",
  "session_expiry_mobile": "168:00:00",
  "deny_multiple_sessions": 1,
  "cookie_secure": 1,
  "cookie_httponly": 1,
  "cookie_samesite": "Lax"
}
```

### Restart Bench
```bash
bench restart
```

---

## 9. Backup Security

### Configure Encrypted Backups

```bash
# Install encryption tools
sudo apt-get install gnupg

# Generate GPG key for backups
gpg --gen-key

# Configure bench backup with encryption
bench --site tems.local backup --with-files --compress --encrypt

# Set up automated backups
crontab -e
```

Add to crontab:
```bash
# Daily encrypted backup at 2 AM
0 2 * * * cd /workspace/development/frappe-bench && bench --site tems.local backup --with-files --compress --encrypt
```

### Offsite Backup

```bash
# Install rclone for cloud storage
curl https://rclone.org/install.sh | sudo bash

# Configure rclone (follow interactive setup)
rclone config

# Add to backup script
0 3 * * * rclone copy /workspace/development/frappe-bench/sites/tems.local/private/backups/ remote:tems-backups/
```

---

## 10. Logging and Monitoring

### Enable Comprehensive Logging

Edit `sites/common_site_config.json`:

```json
{
  "enable_frappe_logger": 1,
  "file_watcher_port": 6787,
  "developer_mode": 0,
  "log_queries": 0,
  "logging": 2
}
```

### Set Up Log Rotation

Create `/etc/logrotate.d/frappe`:

```
/workspace/development/frappe-bench/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 frappe frappe
    sharedscripts
    postrotate
        systemctl reload supervisor > /dev/null 2>&1 || true
    endscript
}
```

### Monitor Security Events

Install and configure monitoring tools:

```bash
# Install logwatch for daily reports
sudo apt-get install logwatch

# Configure daily security reports
sudo logwatch --detail high --mailto admin@tems.local --service all --range today
```

---

## 11. Two-Factor Authentication (2FA)

### Enable 2FA in Frappe

```bash
# Enable 2FA for all users
bench --site tems.local execute frappe.utils.setup.enable_2fa
```

### Configure 2FA Settings

Navigate to:
1. User Settings → Security Settings
2. Enable "Two Factor Authentication"
3. Choose method: OTP App (recommended) or SMS

### Enforce 2FA for Roles

```python
# In hooks.py or custom script
doc_events = {
    "User": {
        "validate": "tems.utils.enforce_2fa"
    }
}

# In tems/utils.py
import frappe

def enforce_2fa(doc, method):
    """Enforce 2FA for privileged roles"""
    privileged_roles = ["Fleet Manager", "Operations Manager", "Safety Manager", "System Manager"]
    
    user_roles = frappe.get_roles(doc.name)
    if any(role in privileged_roles for role in user_roles):
        if not doc.two_factor_authentication:
            frappe.throw("Two-factor authentication is required for your role")
```

---

## 12. Security Monitoring Checklist

### Daily Tasks
- [ ] Review login attempts (failed and successful)
- [ ] Check error logs for unusual patterns
- [ ] Monitor database query performance
- [ ] Verify backup completion

### Weekly Tasks
- [ ] Review user access logs
- [ ] Check for suspicious API activity
- [ ] Verify SSL certificate validity
- [ ] Review firewall logs
- [ ] Check fail2ban status

### Monthly Tasks
- [ ] Update system packages: `sudo apt-get update && sudo apt-get upgrade`
- [ ] Update Frappe/ERPNext: `bench update`
- [ ] Review user permissions
- [ ] Audit active sessions
- [ ] Test backup restoration
- [ ] Review security headers with SSL Labs

---

## 13. Security Incident Response Plan

### If Security Breach Suspected

1. **Immediate Actions:**
   ```bash
   # Disable site
   bench --site tems.local set-maintenance-mode on
   
   # Block suspicious IPs at firewall
   sudo ufw deny from <suspicious-ip>
   
   # Force all users to logout
   bench --site tems.local clear-cache
   ```

2. **Investigation:**
   ```bash
   # Check access logs
   grep "suspicious-pattern" /workspace/development/frappe-bench/logs/*.log
   
   # Check currently logged-in users
   bench --site tems.local console
   >>> frappe.get_all("Sessions", fields=["user", "lastupdate"])
   ```

3. **Recovery:**
   ```bash
   # Restore from backup if needed
   bench --site tems.local restore <backup-file>
   
   # Force password reset for all users
   bench --site tems.local reset-password --all
   ```

4. **Post-Incident:**
   - Document incident
   - Review and update security measures
   - Notify affected users
   - Report to authorities if required

---

## 14. Verification Script

After applying configurations, run this verification script:

```bash
#!/bin/bash
echo "TEMS Security Configuration Verification"
echo "========================================"

# Check HTTPS
echo -n "1. HTTPS enabled: "
curl -sI https://tems.local | grep -q "HTTP/2 200" && echo "✓" || echo "✗"

# Check security headers
echo -n "2. X-Content-Type-Options: "
curl -sI https://tems.local | grep -q "X-Content-Type-Options" && echo "✓" || echo "✗"

echo -n "3. X-Frame-Options: "
curl -sI https://tems.local | grep -q "X-Frame-Options" && echo "✓" || echo "✗"

echo -n "4. Content-Security-Policy: "
curl -sI https://tems.local | grep -q "Content-Security-Policy" && echo "✓" || echo "✗"

echo -n "5. Strict-Transport-Security: "
curl -sI https://tems.local | grep -q "Strict-Transport-Security" && echo "✓" || echo "✗"

# Check Frappe config
echo -n "6. Developer mode disabled: "
bench --site tems.local get-config developer_mode | grep -q "0" && echo "✓" || echo "✗"

# Check firewall
echo -n "7. UFW enabled: "
sudo ufw status | grep -q "active" && echo "✓" || echo "✗"

# Check fail2ban
echo -n "8. Fail2ban running: "
systemctl is-active fail2ban | grep -q "active" && echo "✓" || echo "✗"

echo ""
echo "Configuration verification complete!"
```

---

## Quick Reference: Production Deployment Commands

```bash
# 1. Set production mode
bench --site tems.local set-config developer_mode 0
bench --site tems.local set-config allow_error_traceback 0

# 2. Enable SSL (Let's Encrypt)
sudo certbot --nginx -d tems.local

# 3. Restart services
bench restart
sudo systemctl reload nginx

# 4. Enable firewall
sudo ufw enable
sudo ufw allow 22,80,443/tcp

# 5. Verify deployment
curl -I https://tems.local
```

---

**For questions or support, contact the TEMS security team.**
