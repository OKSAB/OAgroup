# OA Group — Deployment Guide

## Local laptop testing (current setup)

### 1. Add domain to /etc/hosts  (one-time, needs sudo)
This makes your laptop resolve `oalamoudi.com` to itself instead of the internet.

```bash
sudo nano /etc/hosts
```
Add this line at the bottom:
```
127.0.0.1   oalamoudi.com www.oalamoudi.com
```
Save: Ctrl+O, Enter, Ctrl+X.

### 2. Start the stack
```bash
cd /Users/School/Desktop/Omarwebsite/OAgroup
bash deploy/start.sh
```
Open **https://oalamoudi.com** in your browser.  
Your browser will show a certificate warning — click **Advanced → Proceed** (the self-signed cert is only for local testing).

### 3. Stop the stack
```bash
bash deploy/stop.sh
```

### 4. Re-deploy after code changes
```bash
bash deploy/stop.sh
venv/bin/python manage.py collectstatic --noinput   # only if CSS/JS changed
bash deploy/start.sh
```

---

## Email setup (if not done yet)
Edit `.env` and replace `your-app-password-here` with a Gmail App Password:
```
EMAIL_HOST_PASSWORD=xxxxxxxxxxxxxxxxxxxx
```
Generate one at: myaccount.google.com → Security → 2-Step Verification → App passwords

---

## Moving to a real VPS (Sahara.com / any Linux server)

### Step 1 — DNS at sahara.com
Log in to sahara.com → DNS Manager for `oalamoudi.com` and add:

| Type | Name | Value         | TTL  |
|------|------|---------------|------|
| A    | @    | YOUR_VPS_IP   | 3600 |
| A    | www  | YOUR_VPS_IP   | 3600 |

### Step 2 — Server setup (Ubuntu 22.04)
```bash
sudo apt update && sudo apt install -y python3.11 python3.11-venv python3-pip nginx certbot python3-certbot-nginx git

git clone <your-repo> /home/ubuntu/OAgroup
cd /home/ubuntu/OAgroup
python3.11 -m venv venv
venv/bin/pip install -r requirements.txt
cp .env.example .env   # then edit with production values
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput
```

### Step 3 — Update paths in nginx.conf
Replace `/Users/School/Desktop/Omarwebsite/OAgroup` with `/home/ubuntu/OAgroup` in `deploy/nginx.conf`, then:
```bash
sudo ln -s /home/ubuntu/OAgroup/deploy/nginx.conf /etc/nginx/sites-enabled/oalamoudi.conf
sudo nginx -t && sudo systemctl reload nginx
```

### Step 4 — Real SSL with Let's Encrypt (replaces self-signed)
```bash
sudo certbot --nginx -d oalamoudi.com -d www.oalamoudi.com
```
Certbot automatically edits your nginx.conf with the real cert paths and sets up auto-renewal.

### Step 5 — Run Gunicorn as a systemd service
```bash
sudo nano /etc/systemd/system/oagroup.service
```
```ini
[Unit]
Description=OA Group Gunicorn
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/OAgroup
ExecStart=/home/ubuntu/OAgroup/venv/bin/gunicorn oagroup.wsgi:application --config deploy/gunicorn.conf.py
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable --now oagroup
sudo systemctl status oagroup
```

Done — `https://oalamoudi.com` is live with a real trusted SSL certificate.
