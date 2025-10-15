# TEMS Production Deployment Checklist

**Quick Reference Guide for Production Deployment**

---

## Pre-Deployment (1-2 hours)

### Server Preparation
- [ ] Server provisioned (Ubuntu 22.04, 8GB RAM, 4 CPU cores, 50GB storage)
- [ ] SSH access configured
- [ ] Domain name configured (DNS A record)
- [ ] SSL certificate ready (or Let's Encrypt prepared)
- [ ] Team notified of deployment window
- [ ] Downtime window scheduled (if applicable)

### Access & Credentials
- [ ] Root/sudo access verified
- [ ] Git repository access confirmed
- [ ] Database credentials prepared
- [ ] Email service configured
- [ ] Admin passwords documented (stored securely)

---

## Installation (2-3 hours)

### System Setup
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Create frappe user
sudo adduser frappe --disabled-password --gecos "Frappe User"
sudo usermod -aG sudo frappe
sudo su - frappe
```

- [ ] System packages updated
- [ ] Frappe user created

### Frappe Bench Installation
```bash
# Install bench
sudo pip3 install frappe-bench

# Initialize bench
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
```

- [ ] Bench installed
- [ ] Frappe initialized

### Install Apps
```bash
# Install apps
bench get-app erpnext --branch version-15
bench get-app hrms --branch version-15
bench get-app drive https://github.com/frappe/drive
bench get-app tems https://github.com/Gabcelltd/tems.git
```

- [ ] ERPNext installed
- [ ] HRMS installed
- [ ] Drive installed
- [ ] TEMS installed

### Create Site
```bash
# Create site
bench new-site tems.yourdomain.com

# Install apps
bench --site tems.yourdomain.com install-app erpnext
bench --site tems.yourdomain.com install-app hrms
bench --site tems.yourdomain.com install-app drive
bench --site tems.yourdomain.com install-app tems

# Migrate
bench --site tems.yourdomain.com migrate
```

- [ ] Site created
- [ ] Apps installed on site
- [ ] Migrations completed

---

## Security Configuration (1-2 hours)

### Application Security
```bash
# Disable developer mode
bench --site tems.yourdomain.com set-config developer_mode 0
bench --site tems.yourdomain.com set-config allow_error_traceback 0
bench --site tems.yourdomain.com set-config deny_multiple_sessions 1
```

- [ ] Developer mode disabled
- [ ] Error traceback disabled
- [ ] Multiple sessions denied

### Firewall (UFW)
```bash
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 127.0.0.1 to any port 3306
sudo ufw allow from 127.0.0.1 to any port 11000
sudo ufw allow from 127.0.0.1 to any port 13000
sudo ufw status verbose
```

- [ ] Firewall enabled
- [ ] SSH allowed (port 22)
- [ ] HTTP/HTTPS allowed (ports 80, 443)
- [ ] Database restricted to localhost
- [ ] Redis restricted to localhost

### Fail2Ban
```bash
sudo apt-get install -y fail2ban
# Configure filters (see DEPLOYMENT_GUIDE.md)
sudo systemctl restart fail2ban
```

- [ ] Fail2ban installed
- [ ] Frappe filter configured
- [ ] Service running

### Database Security
```bash
sudo mysql_secure_installation
# Answer YES to all prompts
```

- [ ] MariaDB secured
- [ ] Root password set
- [ ] Anonymous users removed
- [ ] Remote root login disabled

---

## Web Server & SSL (1 hour)

### nginx Configuration
```bash
# Generate config
bench setup nginx

# Add security headers (see DEPLOYMENT_GUIDE.md)
sudo nano /etc/nginx/sites-available/frappe-bench.conf

# Enable site
sudo ln -s /etc/nginx/sites-available/frappe-bench.conf /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

- [ ] nginx configured
- [ ] Security headers added
- [ ] Site enabled
- [ ] Default site removed
- [ ] Configuration tested

### SSL/HTTPS (Let's Encrypt)
```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d tems.yourdomain.com
sudo certbot renew --dry-run
```

- [ ] Certbot installed
- [ ] SSL certificate obtained
- [ ] HTTPS configured
- [ ] HTTP redirect enabled
- [ ] Auto-renewal tested

---

## Production Deployment (30 minutes)

### Build & Deploy
```bash
cd ~/frappe-bench

# Build assets
bench build

# Setup production
bench setup production frappe

# Enable scheduler
bench --site tems.yourdomain.com enable-scheduler
```

- [ ] Assets built
- [ ] Production configured
- [ ] Supervisor configured
- [ ] Scheduler enabled

### Start Services
```bash
# Start all services
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all

# Verify status
sudo supervisorctl status
```

- [ ] Services started
- [ ] All processes running
- [ ] No FATAL errors

---

## Backup Configuration (30 minutes)

### Automated Backups
```bash
# Create backup script (see DEPLOYMENT_GUIDE.md)
nano ~/frappe-bench/backup-tems.sh
chmod +x ~/frappe-bench/backup-tems.sh

# Schedule backups
crontab -e
# Add: 0 2 * * * /home/frappe/frappe-bench/backup-tems.sh
```

- [ ] Backup script created
- [ ] Backup script tested
- [ ] Daily backups scheduled
- [ ] Backup directory configured
- [ ] Offsite backups configured (optional)

---

## Verification (30 minutes)

### Service Verification
```bash
# Check services
sudo supervisorctl status
# All should be RUNNING

# Check web access
curl -I http://localhost:8000
# Should return: 200 OK

# Check HTTPS
curl -I https://tems.yourdomain.com
# Should return: HTTP/2 200

# Run system check
bench --site tems.yourdomain.com doctor
```

- [ ] All supervisor processes RUNNING
- [ ] Web server responding (200 OK)
- [ ] HTTPS working
- [ ] System check passed

### PWA Verification
```bash
curl -I https://tems.yourdomain.com/assets/tems/frontend/operations-pwa/dist/index.html
curl -I https://tems.yourdomain.com/assets/tems/frontend/safety-pwa/dist/index.html
curl -I https://tems.yourdomain.com/assets/tems/frontend/fleet-pwa/dist/index.html
curl -I https://tems.yourdomain.com/assets/tems/frontend/driver-pwa/dist/index.html
# All should return: HTTP/2 200
```

- [ ] Operations PWA accessible
- [ ] Safety PWA accessible
- [ ] Fleet PWA accessible
- [ ] Driver PWA accessible

### Security Verification
```bash
# Test security headers
curl -I https://tems.yourdomain.com | grep -E 'X-Content-Type-Options|X-Frame-Options|Strict-Transport-Security'

# Check firewall
sudo ufw status verbose

# Check fail2ban
sudo fail2ban-client status frappe
```

- [ ] Security headers present
- [ ] Firewall active
- [ ] Fail2ban active
- [ ] SSL/TLS working (A+ rating on SSL Labs recommended)

### Functional Testing
- [ ] Login as Administrator works
- [ ] Create test user works
- [ ] Navigate to each PWA works
- [ ] API endpoints responding
- [ ] Scheduled jobs running

---

## Post-Deployment (1 hour)

### Monitoring Setup
```bash
# Install monitoring tools
sudo apt-get install -y htop logwatch

# Create monitoring script (see DEPLOYMENT_GUIDE.md)
nano ~/monitor-tems.sh
chmod +x ~/monitor-tems.sh

# Schedule monitoring
crontab -e
# Add health checks and reports
```

- [ ] Monitoring tools installed
- [ ] Health check script created
- [ ] Health checks scheduled
- [ ] Daily reports configured

### Documentation
- [ ] Deployment notes documented
- [ ] Credentials documented (secure storage)
- [ ] Team notified of completion
- [ ] Admin training scheduled
- [ ] Support contacts documented

### Performance Baseline
```bash
# Run performance test
cd ~/frappe-bench/apps/tems
/home/frappe/frappe-bench/env/bin/python test_performance_analysis.py
```

- [ ] Performance baseline recorded
- [ ] Results compared with testing environment
- [ ] Any issues documented

---

## Go-Live Checklist

### Final Verification
- [ ] All services running without errors
- [ ] SSL certificate valid and auto-renewal working
- [ ] Backups tested and scheduled
- [ ] Monitoring active
- [ ] Security headers verified
- [ ] Firewall configured
- [ ] All PWAs accessible and functional
- [ ] API endpoints tested
- [ ] Admin user can login
- [ ] Test users created for UAT

### Communication
- [ ] Team notified of go-live
- [ ] Users notified (if applicable)
- [ ] Support team briefed
- [ ] Escalation procedures documented

### Rollback Plan
- [ ] Rollback procedure documented
- [ ] Backup verified and accessible
- [ ] Emergency contacts documented
- [ ] Downtime procedure prepared

---

## Troubleshooting Quick Reference

### Services Not Starting
```bash
sudo tail -f /var/log/supervisor/supervisord.log
cd ~/frappe-bench && tail -f logs/web.error.log
sudo supervisorctl restart all
```

### Database Issues
```bash
sudo systemctl status mariadb
sudo systemctl restart mariadb
bench --site tems.yourdomain.com console
```

### nginx 502 Error
```bash
sudo supervisorctl status
sudo netstat -tlnp | grep 8000
sudo supervisorctl restart frappe-bench-web:*
```

### SSL Issues
```bash
sudo certbot certificates
sudo certbot renew
```

### Performance Issues
```bash
htop
bench --site tems.yourdomain.com clear-cache
bench build
bench restart
```

---

## Emergency Contacts

| Role | Name | Contact | Availability |
|------|------|---------|--------------|
| System Admin | _________ | _________ | 24/7 |
| Database Admin | _________ | _________ | Business hours |
| TEMS Developer | _________ | _________ | Business hours |
| Support Lead | _________ | _________ | Business hours |

---

## Sign-Off

### Deployment Completed By
- **Name:** _____________________
- **Date:** _____________________
- **Time:** _____________________
- **Signature:** _____________________

### Deployment Verified By
- **Name:** _____________________
- **Date:** _____________________
- **Time:** _____________________
- **Signature:** _____________________

---

**Document Version:** 1.0  
**Last Updated:** October 15, 2025  
**Total Estimated Time:** 7-10 hours

**Quick Links:**
- Full Deployment Guide: `DEPLOYMENT_GUIDE.md`
- Security Setup: `PRODUCTION_SECURITY_SETUP.md`
- Security Audit: `SECURITY_AUDIT_REPORT.md`
- Performance Report: `PERFORMANCE_AUDIT_REPORT.md`
