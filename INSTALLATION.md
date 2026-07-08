# Installation Guide - Password Manager for CasaOS

## 📋 Prerequisites

- Docker and Docker Compose installed
- 500MB free disk space
- Modern web browser
- CasaOS (optional, for app store installation)

## 🚀 Quick Start (Docker Compose)

### Step 1: Clone or Download

```bash
git clone https://github.com/seu-usuario/password-manager.git
cd password-manager
```

### Step 2: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and change SECRET_KEY to a random string
nano .env
```

**Important**: Change `SECRET_KEY` to a random, strong string. Example:
```bash
SECRET_KEY=your-random-string-here-change-this
```

### Step 3: Start Services

```bash
# Build and start containers
docker-compose up -d

# Check status
docker-compose ps
```

### Step 4: Access the Application

Open your browser and go to:
```
http://localhost:3000
```

Or access from another computer:
```
http://YOUR_SERVER_IP:3000
```

## 🐳 Docker Compose Details

The `docker-compose.yml` file includes:

- **Backend**: FastAPI running on port 8000
- **Frontend**: Node.js server running on port 3000
- **Database**: SQLite stored in `./data/vault.db`
- **Network**: Internal bridge network for secure communication
- **Volumes**: Persistent data storage

### Check Logs

```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# All logs
docker-compose logs -f
```

### Stop Services

```bash
docker-compose down
```

### Restart Services

```bash
docker-compose restart
```

## 🔧 Manual Installation (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install
# or
npm install

# Development server
pnpm dev
# or
npm run dev
```

Frontend will run on `http://localhost:3000`

## 🐳 CasaOS Installation

### Method 1: App Store (If Available)

1. Open CasaOS
2. Go to App Store
3. Search for "Password Manager"
4. Click Install
5. Wait for installation to complete
6. Access at `http://your-casaos-ip:3000`

### Method 2: Manual CasaOS Install

1. SSH into your CasaOS server
2. Clone the repository
3. Run `docker-compose up -d`
4. Add the app to CasaOS using the `app.json` configuration

## 📁 Directory Structure After Installation

```
password-manager/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── database.py
│   ├── security.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── dist/                    # Built files
│   ├── package.json
│   ├── Dockerfile
│   └── .dockerignore
├── data/                        # SQLite database (created on first run)
│   └── vault.db
├── backups/                     # Backup files (created when running backup.sh)
├── docker-compose.yml
├── .env                         # Your configuration
├── .env.example                 # Example configuration
├── app.json                     # CasaOS configuration
├── backup.sh                    # Backup script
├── README.md                    # Main documentation
└── INSTALLATION.md              # This file
```

## 🔐 First Time Setup

### Create Your Account

1. Open `http://localhost:3000`
2. Click "Create Account"
3. Enter a username (e.g., `admin`)
4. Enter a strong master password
5. Click "Create Account"

**Important**: Remember your master password. It cannot be recovered.

### Add Your First Password

1. Click "Add Password"
2. Fill in the details:
   - **Service Name**: e.g., "Gmail"
   - **Username/Email**: your email
   - **Password**: your password
   - **URL**: https://gmail.com (optional)
   - **Notes**: Any notes (optional)
3. Click "Add Password"

## 🔄 Backup and Restore

### Create Backup

```bash
./backup.sh
```

Backups are saved in `./backups/` directory.

### Manual Backup

```bash
# Stop containers
docker-compose down

# Copy database
cp data/vault.db backups/vault_backup_manual.db

# Restart
docker-compose up -d
```

### Restore Backup

```bash
# Stop containers
docker-compose down

# Restore database
cp backups/vault_backup_YYYYMMDD_HHMMSS.db data/vault.db

# Restart
docker-compose up -d
```

## 🌐 Access from Outside Your Network

### Option 1: Reverse Proxy with Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Option 2: VPN

Use a VPN to securely access your home network.

### Option 3: Port Forwarding

⚠️ **Not Recommended** - Use HTTPS if you expose to the internet.

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Change ports in .env
BACKEND_PORT=8001
FRONTEND_PORT=3001

# Restart
docker-compose down
docker-compose up -d
```

### Database Corrupted

```bash
# Remove database
rm data/vault.db

# Restart (will create new database)
docker-compose restart backend
```

### Containers Won't Start

```bash
# Check logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Forgot Master Password

Unfortunately, there's no recovery mechanism. You'll need to:

1. Backup encrypted data
2. Delete database: `rm data/vault.db`
3. Restart: `docker-compose restart backend`
4. Create new account
5. Manually restore data if possible

## 🔐 Security Recommendations

1. **Change SECRET_KEY**: Use a strong random string in `.env`
2. **Use HTTPS**: Set up a reverse proxy with SSL certificates
3. **Regular Backups**: Run `./backup.sh` regularly
4. **Strong Master Password**: Use 16+ characters with mixed case, numbers, symbols
5. **Keep Updated**: Check for security updates regularly
6. **Firewall**: Restrict access to the application port

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 1 core | 2+ cores |
| RAM | 512MB | 1GB+ |
| Storage | 500MB | 2GB+ |
| Network | 100Mbps | 1Gbps |

## ✅ Verification

After installation, verify everything is working:

```bash
# Check containers running
docker-compose ps

# Test backend health
curl http://localhost:8000/api/health

# Test frontend
curl http://localhost:3000
```

## 📞 Support

For issues or questions:

1. Check the main README.md
2. Review troubleshooting section above
3. Check Docker logs: `docker-compose logs`
4. Open an issue on GitHub

## 🎉 You're Ready!

Your password manager is now installed and ready to use. Start adding your passwords securely!

---

**Remember**: Your passwords are encrypted and stored locally on your server. No data leaves your network.
