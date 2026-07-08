# Setup com Virtual Environment - Solução para Python 3.12+

## 🚨 Erro: `externally-managed-environment`

Se você receber:
```
error: externally-managed-environment
× This environment is externally managed
```

**Causa:** Python 3.12+ protege o ambiente do sistema

**Solução:** Use Virtual Environment

---

## ✅ Passo a Passo

### 1. Clonar Repositório

```bash
git clone https://github.com/Lucca-png/Password-Manager-For-CasaOS.git
cd Password-Manager-For-CasaOS
```

### 2. Criar Virtual Environment

```bash
python3 -m venv venv
```

### 3. Ativar Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

Você verá `(venv)` no início do terminal:
```
(venv) usuario@pc:~/Password-Manager-For-CasaOS$
```

### 4. Atualizar pip

```bash
pip install --upgrade pip
```

### 5. Instalar Dependências Backend

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 6. Inicializar Banco de Dados

```bash
cd backend
python3 init_db.py
```

Saída esperada:
```
Database path: /home/usuario/Password-Manager-For-CasaOS/data/vault.db
✅ Database initialized successfully!
```

### 7. Iniciar Backend

```bash
python3 main.py
```

Saída esperada:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Acesse:** http://localhost:8000/docs

### 8. Iniciar Frontend (novo terminal)

```bash
# Novo terminal
cd Password-Manager-For-CasaOS

# Ativar venv
source venv/bin/activate

# Instalar dependências
cd frontend
npm install

# Iniciar
npm run dev
```

**Acesse:** http://localhost:5173

---

## 🧪 Testar API

```bash
# Registrar
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","password":"Teste123!"}'

# Login
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","password":"Teste123!"}'
```

---

## 💡 Dicas

### Desativar venv
```bash
deactivate
```

### Reativar venv
```bash
source venv/bin/activate
```

### Limpar venv
```bash
rm -rf venv
```

---

**Pronto! 🎉**
