# Instalação no CasaOS

Guia completo para instalar o Password Manager como app nativo no CasaOS.

## 📋 Pré-requisitos

- CasaOS instalado e funcionando
- Docker e Docker Compose
- Acesso SSH ao servidor (opcional)

## 🚀 Método 1: Instalação via CasaOS Store (Recomendado)

### 1. Adicionar Repositório Customizado

1. Abra o CasaOS no navegador (http://seu-ip:80)
2. Vá para **App Store**
3. Clique em **Settings** (engrenagem)
4. Selecione **App Sources**
5. Clique em **Add Source**
6. Cole a URL:
   ```
   https://github.com/Lucca-png/Password-Manager-For-CasaOS
   ```
7. Clique em **Add**

### 2. Instalar o App

1. Volte para **App Store**
2. Procure por **Password Manager**
3. Clique em **Install**
4. Aguarde a instalação (pode levar alguns minutos)

### 3. Acessar

- Após instalação, o app aparecerá na dashboard
- Clique no ícone para acessar o Password Manager
- URL: `http://seu-ip:3000`

---

## 🐳 Método 2: Instalação Manual via Docker Compose

### 1. Clonar Repositório

```bash
cd /opt/casaos/apps
git clone https://github.com/Lucca-png/Password-Manager-For-CasaOS password-manager
cd password-manager
```

### 2. Configurar Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
nano .env
```

Altere:
```env
SECRET_KEY=sua-chave-secreta-aqui-mude-isso
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

### 3. Criar Diretório de Dados

```bash
sudo mkdir -p /data/password-manager
sudo chown -R 1000:1000 /data/password-manager
```

### 4. Iniciar Containers

```bash
docker-compose up -d
```

### 5. Verificar Status

```bash
docker-compose ps
```

Você deve ver:
```
NAME                    STATUS
password-manager-backend    Up
password-manager-frontend   Up
```

### 6. Acessar

- Frontend: http://seu-ip:3000
- Backend API: http://seu-ip:8000
- Documentação: http://seu-ip:8000/docs

---

## 🔧 Método 3: Instalação via CasaOS CLI

Se o CasaOS CLI estiver disponível:

```bash
# Adicionar app
casaos-cli app add https://github.com/Lucca-png/Password-Manager-For-CasaOS/app.json

# Instalar
casaos-cli app install password-manager

# Iniciar
casaos-cli app start password-manager
```

---

## 📝 Primeiro Acesso

### 1. Criar Conta

1. Acesse http://seu-ip:3000
2. Clique em **Create Account**
3. Escolha um **username** e **master password** forte
4. Clique em **Create Account**

### 2. Fazer Login

1. Digite seu **username** e **master password**
2. Clique em **Sign In**

### 3. Adicionar Primeira Senha

1. Clique em **+ Gerar Senha** (ou **+ Add Password**)
2. Preencha os dados:
   - **Title**: Nome do serviço (ex: Gmail)
   - **Username**: Seu usuário
   - **Password**: Sua senha
   - **URL**: Link do serviço (opcional)
3. Clique em **Save**

---

## 🔐 Configuração de Segurança

### Alterar SECRET_KEY em Produção

**IMPORTANTE:** Mude a `SECRET_KEY` antes de usar em produção!

```bash
# Gerar nova chave segura
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Editar .env
nano .env

# Alterar:
SECRET_KEY=sua-nova-chave-aqui

# Reiniciar containers
docker-compose restart
```

### Backup de Dados

```bash
# Backup do banco de dados
sudo cp /data/password-manager/vault.db /data/password-manager/vault.db.backup

# Ou usar script de backup
bash backup.sh
```

### Restaurar de Backup

```bash
# Parar containers
docker-compose down

# Restaurar banco
sudo cp /data/password-manager/vault.db.backup /data/password-manager/vault.db

# Iniciar containers
docker-compose up -d
```

---

## 🆘 Troubleshooting

### Erro: "Cannot connect to Docker daemon"

```bash
# Verificar se Docker está rodando
sudo systemctl status docker

# Iniciar Docker
sudo systemctl start docker
```

### Erro: "Port already in use"

```bash
# Encontrar processo na porta
sudo lsof -i :3000

# Matar processo
sudo kill -9 <PID>

# Ou usar outra porta no .env
FRONTEND_PORT=3001
```

### Erro: "Permission denied"

```bash
# Dar permissão ao usuário
sudo usermod -aG docker $USER
newgrp docker
```

### Banco de dados corrompido

```bash
# Remover banco antigo
sudo rm /data/password-manager/vault.db

# Reiniciar containers (vai criar novo banco)
docker-compose restart
```

---

## 📊 Monitorar Logs

```bash
# Ver logs do backend
docker-compose logs -f backend

# Ver logs do frontend
docker-compose logs -f frontend

# Ver todos os logs
docker-compose logs -f
```

---

## 🔄 Atualizar App

```bash
# Parar containers
docker-compose down

# Atualizar código
git pull origin main

# Reconstruir imagens
docker-compose build --no-cache

# Iniciar novamente
docker-compose up -d
```

---

## 📱 Acessar de Fora da Rede

### Via Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Via Cloudflare Tunnel

```bash
# Instalar Cloudflare Tunnel
curl -L --output cloudflared.tgz https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.tgz
tar -xzf cloudflared.tgz

# Conectar
./cloudflared tunnel --url http://localhost:3000
```

---

## 📚 Documentação Adicional

- [README.md](README.md) - Visão geral do projeto
- [SETUP_VENV.md](SETUP_VENV.md) - Setup com Virtual Environment
- [DEVELOPMENT.md](DEVELOPMENT.md) - Guia para desenvolvedores

---

## 💡 Dicas

- **Backup regular**: Configure backup automático do banco de dados
- **Senhas fortes**: Use o gerador de senhas integrado
- **Atualizações**: Verifique atualizações regularmente
- **Logs**: Monitore logs para detectar problemas

---

**Pronto para usar! Seguro. Privado. Seu.** 🔐

Dúvidas? Abra uma issue no GitHub!
