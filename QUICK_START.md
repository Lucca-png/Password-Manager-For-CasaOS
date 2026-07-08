# 🚀 Quick Start - 5 Minutes to Secure Passwords

## TL;DR

```bash
# 1. Extract and navigate
unzip password-manager-complete.zip
cd password-manager

# 2. Configure
cp .env.example .env
# Edit .env and change SECRET_KEY to something random

# 3. Start
docker-compose up -d

# 4. Access
# Open browser: http://localhost:3000

# 5. Create account and start adding passwords!
```

## 📱 First Steps

### 1. Create Your Account

1. Open `http://localhost:3000`
2. Click "Create Account"
3. Enter username: `admin` (or your preferred username)
4. Enter master password: **Use a strong password!** (16+ characters recommended)
5. Click "Create Account"

**⚠️ Important**: You cannot recover your master password. Make it strong and remember it!

### 2. Add Your First Password

1. Click "Add Password"
2. Fill in:
   - **Service Name**: Gmail
   - **Username/Email**: your@email.com
   - **Password**: your-password
   - **URL**: https://gmail.com (optional)
3. Click "Add Password"

### 3. Manage Your Passwords

- **View**: Click the eye icon to show/hide password
- **Copy**: Click copy icon to copy to clipboard
- **Delete**: Click trash icon to delete
- **Favorite**: Click star icon to mark as favorite
- **Search**: Use search bar to find passwords

## 🔧 Configuration

### Change Ports

Edit `.env`:
```env
BACKEND_PORT=8001
FRONTEND_PORT=3001
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

### Change Secret Key

Edit `.env`:
```env
SECRET_KEY=your-random-secret-key-here
```

**Generate random key**:
```bash
openssl rand -hex 32
```

## 🆘 Common Issues

### Can't access on http://localhost:3000

**Solution**: Check if containers are running
```bash
docker-compose ps
```

If not running:
```bash
docker-compose up -d
```

### Port already in use

**Solution**: Change ports in `.env` (see Configuration above)

### Forgot master password

**Solution**: Unfortunately, there's no recovery. You must:
1. Delete database: `rm data/vault.db`
2. Restart: `docker-compose restart backend`
3. Create new account

## 📊 Check Status

```bash
# See running containers
docker-compose ps

# View logs
docker-compose logs -f

# Test backend
curl http://localhost:8000/api/health

# Test frontend
curl http://localhost:3000
```

## 💾 Backup Your Passwords

```bash
# Create backup
./backup.sh

# Backups saved in ./backups/
```

## 🔐 Security Checklist

- ✅ Changed SECRET_KEY in .env
- ✅ Created strong master password (16+ characters)
- ✅ Saved backup of database
- ✅ Only accessible on local network (for now)

## 📖 Next Steps

- Read [README.md](README.md) for full documentation
- Read [INSTALLATION.md](INSTALLATION.md) for advanced setup
- Read [DEVELOPMENT.md](DEVELOPMENT.md) if you want to contribute

## 🎉 You're Done!

Your password manager is now running securely on your local network!

---

**Need help?** Check the troubleshooting section in [INSTALLATION.md](INSTALLATION.md)
