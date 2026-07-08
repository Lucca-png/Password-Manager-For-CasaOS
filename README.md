# Minimalist Password Manager for CasaOS

A private, minimalist, and 100% self-hosted password manager for home servers. Inspired by Bitwarden, 1Password, and the Apple Design System.

## 🎯 Features

* **Complete Privacy**: All data remains on your local server
* **Zero External Dependencies**: No third-party APIs or telemetry
* **Strong Encryption**: Argon2id + AES-256 for maximum security
* **Minimalist Interface**: Clean Apple-inspired design
* **Fully Offline**: Works without an internet connection
* **Docker Ready**: Deploy with a single Docker Compose command
* **CasaOS Compatible**: Install directly from CasaOS

## 📋 Requirements

* Docker and Docker Compose
* CasaOS (optional but recommended)
* 500MB of disk space
* Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Quick Installation

### Option 1: CasaOS App Store (Recommended)

1. Open CasaOS
2. Go to the App Store
3. Search for "Password Manager"
4. Click **Install**
5. Access it at `http://your-ip:3000`

### Option 2: Manual Docker Compose

```bash
# Clone or download the repository
git clone https://github.com/your-username/password-manager.git
cd password-manager

# Configure environment variables
cp .env.example .env
# Edit .env and change the SECRET_KEY

# Start the containers
docker-compose up -d

# Access at http://localhost:3000
```

### Option 3: Manual Installation

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (in another terminal)
cd frontend
pnpm install
pnpm dev
```

## 📁 Project Structure

```text
password-manager/
├── backend/                    # FastAPI API
│   ├── main.py                # Main endpoints
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── auth.py                # Authentication and JWT
│   ├── database.py            # SQLite configuration
│   ├── security.py            # Encryption utilities
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Backend container
├── frontend/                  # React + TypeScript
│   ├── src/
│   │   ├── pages/             # Pages (Login, Dashboard)
│   │   ├── components/        # Reusable components
│   │   ├── lib/               # Utilities
│   │   └── App.tsx            # Routing
│   ├── package.json
│   └── Dockerfile             # Frontend container
├── data/                      # Persistent SQLite data
├── docker-compose.yml         # Docker orchestration
├── .env                       # Environment variables
├── app.json                   # CasaOS configuration
└── backup.sh                  # Backup script
```

## 🔐 Security

### Security Implementations

* **Master Password**: Hashed using Argon2id (OWASP standard)
* **Sensitive Data**: Encrypted with AES-256
* **Sessions**: JWT with configurable expiration
* **Rate Limiting**: Protection against brute-force attacks
* **CSRF Protection**: CSRF tokens for forms
* **SQL Injection Protection**: Prepared statements with SQLAlchemy
* **Secure Cookies**: HttpOnly, SameSite=Strict

### Best Practices

1. **Change the ****`SECRET_KEY`** in `.env` before using in production.
2. **Use HTTPS** if accessing remotely (an Nginx reverse proxy is recommended).
3. **Create regular backups** using the `backup.sh` script.
4. **Keep the application updated** to receive the latest security patches.

## 💾 Backup and Restore

### Create a Backup

```bash
./backup.sh
```

Backups are stored in:

```text
./backups/vault_backup_YYYYMMDD_HHMMSS.db
```

### Restore a Backup

```bash
# Stop the containers
docker-compose down

# Restore the backup file
cp ./backups/vault_backup_YYYYMMDD_HHMMSS.db ./data/vault.db

# Restart the containers
docker-compose up -d
```

## 🎨 User Interface

### Login Screen

* Username field
* Master password field
* Create new account option
* Elegant dark mode design

### Dashboard

* **Sidebar**: All Passwords, Favorites, Folders
* **Main Area**: Password list displayed as cards
* **Each Entry**: Name, username, show/copy button, edit, delete
* **Password Generator**: Fully configurable with custom character sets

## 🔧 Configuration

### Environment Variables (`.env`)

```env
# Backend
BACKEND_PORT=8000
DATABASE_URL=sqlite:///./data/vault.db
SECRET_KEY=your-super-secret-key-change-this

# Frontend
FRONTEND_PORT=3000
VITE_API_URL=http://localhost:8000
```

## 📱 Functionality

### Password Management

* ✅ Create, edit, and delete passwords
* ✅ Organize passwords into folders
* ✅ Mark favorites
* ✅ Instant search
* ✅ Folder and favorite filters
* ✅ Custom tags
* ✅ Private notes

### Password Generator

* ✅ Configurable length (4–128 characters)
* ✅ Uppercase, lowercase, numbers, symbols
* ✅ One-click copy
* ✅ Automatic clipboard clearing

### Security

* ✅ Master password authentication
* ✅ Secure JWT sessions
* ✅ Automatic logout after inactivity
* ✅ Change master password
* ✅ No password history stored

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Change the ports in .env
BACKEND_PORT=8001
FRONTEND_PORT=3001

# Restart the containers
docker-compose down
docker-compose up -d
```

### Corrupted Database

```bash
# Remove the database and recreate it
rm data/vault.db
docker-compose restart backend
```

### I Forgot My Master Password

Unfortunately, recovery is not possible. The master password protects access to your encrypted vault. You will need to:

1. Back up the encrypted data.
2. Delete the database.
3. Create a new account.
4. Manually restore the data (if possible).

## 📚 API Endpoints

### Authentication

* `POST /api/register` — Create account
* `POST /api/login` — Login
* `POST /api/change-password` — Change master password

### Vault

* `GET /api/vault` — List passwords
* `POST /api/vault` — Create password
* `PUT /api/vault/{id}` — Update password
* `DELETE /api/vault/{id}` — Delete password

### Folders

* `GET /api/folders` — List folders
* `POST /api/folders` — Create folder
* `DELETE /api/folders/{id}` — Delete folder

### Utilities

* `POST /api/generate-password` — Generate password
* `GET /api/backup` — Export JSON backup
* `POST /api/health` — Health check

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m "Add some AmazingFeature"`).
4. Push to your branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## ⚠️ Disclaimer

This is an open-source project. Use it at your own risk. The author is not responsible for data loss or security issues. Always maintain regular backups.

## 📞 Support

For issues, suggestions, or questions:

1. Open an issue on GitHub.
2. Read the documentation.
3. Check the troubleshooting section above.

## 🎯 Roadmap

* [ ] Two-factor authentication (2FA)
* [ ] Multi-device synchronization
* [ ] Secure password sharing
* [ ] Import from other password managers
* [ ] Mobile app (React Native)
* [ ] Weak password auditing
* [ ] Change history

---

**Built with ❤️ for privacy and security.**
