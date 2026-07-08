# Development Guide - Password Manager

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Node.js 22+
- pnpm or npm
- Docker (optional, for containerized development)

### Backend Development

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py
```

Server runs on `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs` (Swagger UI)

### Frontend Development

```bash
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

Frontend runs on `http://localhost:3000`

## 📁 Project Structure

### Backend (`backend/`)

```
backend/
├── main.py              # FastAPI application and endpoints
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic request/response schemas
├── auth.py              # Authentication and JWT handling
├── database.py          # Database configuration
├── security.py          # Encryption utilities
├── requirements.txt     # Python dependencies
└── Dockerfile           # Container configuration
```

### Frontend (`frontend/`)

```
frontend/
├── src/
│   ├── pages/           # Page components (Login, Dashboard)
│   ├── components/      # Reusable UI components
│   ├── contexts/        # React contexts (Auth, Theme)
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utility functions
│   ├── App.tsx          # Main app component
│   ├── main.tsx         # Entry point
│   └── index.css        # Global styles
├── package.json         # Dependencies
├── vite.config.ts       # Vite configuration
└── tsconfig.json        # TypeScript configuration
```

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Create new account |
| POST | `/api/login` | Login user |
| POST | `/api/change-password` | Change master password |

### Vault

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/vault` | Get all passwords |
| POST | `/api/vault` | Create password |
| PUT | `/api/vault/{id}` | Update password |
| DELETE | `/api/vault/{id}` | Delete password |

### Folders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/folders` | Get all folders |
| POST | `/api/folders` | Create folder |
| DELETE | `/api/folders/{id}` | Delete folder |

### Utilities

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generate-password` | Generate random password |
| GET | `/api/backup` | Export vault as JSON |
| POST | `/api/health` | Health check |

## 🔐 Authentication Flow

1. **Register**: User creates account with username and master password
2. **Hash**: Master password is hashed with Argon2id
3. **Login**: User provides credentials
4. **Verify**: Password verified against hash
5. **Token**: JWT token issued with 24-hour expiration
6. **Protected Routes**: All vault endpoints require valid JWT token

## 💾 Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    encryption_salt VARCHAR,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Vault Items Table

```sql
CREATE TABLE vault_items (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    folder_id INTEGER FOREIGN KEY,
    title VARCHAR NOT NULL,
    username_encrypted VARCHAR NOT NULL,
    password_encrypted VARCHAR NOT NULL,
    url_encrypted VARCHAR,
    notes_encrypted VARCHAR,
    favorite BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

### Folders Table

```sql
CREATE TABLE folders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    name VARCHAR NOT NULL
);
```

## 🔒 Security Implementation

### Password Hashing

- **Algorithm**: Argon2id (OWASP recommended)
- **Library**: `passlib`
- **Configuration**: Default parameters (memory=65540, time=3, parallelism=4)

### Data Encryption

- **Algorithm**: AES-256
- **Library**: `cryptography.fernet`
- **Key Derivation**: PBKDF2 with SHA256

### JWT Tokens

- **Algorithm**: HS256
- **Expiration**: 24 hours
- **Refresh**: Not implemented (user must login again)

## 🧪 Testing

### Manual Testing

```bash
# Test registration
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Test login
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Test protected endpoint (replace TOKEN with actual token)
curl http://localhost:8000/api/vault \
  -H "Authorization: Bearer TOKEN"
```

### Frontend Testing

```bash
# Run type checking
pnpm check

# Build for production
pnpm build

# Preview production build
pnpm preview
```

## 🚀 Building for Production

### Backend

```bash
# Build Docker image
docker build -t password-manager-backend:latest backend/

# Run container
docker run -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DATABASE_URL="sqlite:///./data/vault.db" \
  -v $(pwd)/data:/app/data \
  password-manager-backend:latest
```

### Frontend

```bash
# Build production bundle
pnpm build

# The dist/ folder contains production files
```

### Docker Compose

```bash
# Build all containers
docker-compose build

# Start in production mode
docker-compose up -d
```

## 📝 Code Style

### Python

- Follow PEP 8
- Use type hints
- Docstrings for functions
- Max line length: 100 characters

### TypeScript/React

- Use ESLint and Prettier
- Type all props and state
- Use functional components with hooks
- Component names in PascalCase
- File names in kebab-case

## 🔄 Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/my-feature

# Create pull request
```

## 📚 Dependencies

### Backend

| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | ^0.100 | Web framework |
| SQLAlchemy | ^2.0 | ORM |
| Passlib | ^1.7 | Password hashing |
| python-jose | ^3.3 | JWT handling |
| cryptography | ^41.0 | Encryption |

### Frontend

| Package | Version | Purpose |
|---------|---------|---------|
| React | ^19 | UI framework |
| TypeScript | ^5.6 | Type safety |
| Tailwind CSS | ^4.1 | Styling |
| shadcn/ui | latest | Component library |
| Wouter | ^3.3 | Routing |

## 🐛 Debugging

### Backend

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Frontend

```typescript
// Use browser DevTools
console.log("Debug message");

// Check network requests in Network tab
// Check console for errors
```

## 🔄 Deployment

### Local Network

1. Get server IP: `hostname -I`
2. Access from other computer: `http://SERVER_IP:3000`

### Remote Access (with reverse proxy)

1. Set up Nginx reverse proxy
2. Configure SSL certificate
3. Point domain to server
4. Access via `https://your-domain.com`

### CasaOS

1. Place files in CasaOS app directory
2. Use `app.json` configuration
3. Install through CasaOS UI

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [OWASP Security Guidelines](https://owasp.org/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Wait for review and merge

---

Happy coding! 🚀
