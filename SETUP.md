# Setup do Gerenciador de Senhas - Guia Completo

## ⚠️ Importante: Sem Docker?

Se você receber erro de permissão do Docker (`PermissionError: [Errno 13] Permission denied`), siga este guia para rodar sem Docker.

## 🚀 Instalação Rápida (Sem Docker)

### 1. Instalar Dependências

```bash
# Python 3.9+
python3 --version

# Instalar dependências do backend
cd backend
sudo pip install -r requirements.txt

# Instalar dependências do frontend
cd ../frontend
npm install  # ou pnpm install
```

### 2. Inicializar Banco de Dados

```bash
cd backend
python3 init_db.py
```

Você verá:
```
Database path: /home/ubuntu/password-manager/data/vault.db
Database URL: sqlite:////home/ubuntu/password-manager/data/vault.db
✅ Database initialized successfully!
```

### 3. Iniciar Backend

```bash
cd backend
python3 main.py
```

O backend estará disponível em: **http://localhost:8000**

Documentação interativa: **http://localhost:8000/docs**

### 4. Iniciar Frontend (em outro terminal)

```bash
cd frontend
npm run dev  # ou pnpm dev
```

O frontend estará disponível em: **http://localhost:5173** (ou outra porta)

## 📝 Testando a API

### Registrar Novo Usuário

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "password": "SenhaForte123!"
  }'
```

### Fazer Login

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "password": "SenhaForte123!"
  }'
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## 🐳 Usando Docker (Se Disponível)

Se Docker estiver funcionando:

```bash
docker-compose up -d
```

Isso iniciará:
- Backend (porta 8000)
- Frontend (porta 3000)
- Banco de dados (SQLite)

## 📁 Estrutura de Arquivos

```
password-manager/
├── backend/
│   ├── main.py           # API FastAPI
│   ├── models.py         # Modelos SQLAlchemy
│   ├── database.py       # Configuração do banco
│   ├── auth.py           # Autenticação JWT
│   ├── init_db.py        # Inicializar banco
│   └── requirements.txt   # Dependências Python
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── data/
│   └── vault.db          # Banco SQLite (criado automaticamente)
└── docker-compose.yml    # Configuração Docker
```

## 🔧 Solução de Problemas

### Erro: `PermissionError: [Errno 13] Permission denied`

**Solução:** Use o método sem Docker acima.

### Erro: `ModuleNotFoundError: No module named 'fastapi'`

**Solução:**
```bash
cd backend
sudo pip install -r requirements.txt
```

### Erro: `unable to open database file`

**Solução:**
```bash
mkdir -p data
cd backend
python3 init_db.py
```

### Porta 8000 já em uso

**Solução:**
```bash
# Encontrar processo na porta 8000
lsof -i :8000

# Matar processo
kill -9 <PID>

# Ou usar outra porta
PORT=8001 python3 main.py
```

## 🔐 Segurança

- Altere `SECRET_KEY` em `.env` para produção
- Use HTTPS em produção
- Configure CORS corretamente
- Faça backup regular do `data/vault.db`

## 📚 Documentação

- [README.md](README.md) - Visão geral do projeto
- [INSTALLATION.md](INSTALLATION.md) - Guia de instalação detalhado
- [DEVELOPMENT.md](DEVELOPMENT.md) - Guia para desenvolvedores
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Resumo técnico

## 🆘 Precisa de Ajuda?

1. Verifique se Python 3.9+ está instalado
2. Verifique se as dependências foram instaladas
3. Verifique se o banco de dados foi inicializado
4. Verifique os logs em `/tmp/backend.log`

---

**Pronto para usar! Seguro. Privado. Seu.** 🔐
