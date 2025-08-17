# 🔐 CONFIGURAÇÃO DE SECRETS PARA ENVIO DE EMAIL

## 📧 Secrets Necessárias no GitHub

Para que o sistema de envio de email funcione, você precisa configurar as seguintes **secrets** no seu repositório GitHub:

### 1. 🔑 Acesse as Secrets do Repositório
- Vá para seu repositório no GitHub
- Clique em **Settings** (Configurações)
- No menu lateral, clique em **Secrets and variables** → **Actions**
- Clique em **New repository secret**

### 2. 📋 Secrets Obrigatórias

#### **SMTP_SERVER**
- **Nome:** `SMTP_SERVER`
- **Valor:** Servidor SMTP do seu provedor de email
- **Exemplos:**
  - Gmail: `smtp.gmail.com`
  - Outlook: `smtp-mail.outlook.com`
  - Yahoo: `smtp.mail.yahoo.com`

#### **SMTP_PORT**
- **Nome:** `SMTP_PORT`
- **Valor:** Porta SMTP (geralmente 587 para TLS ou 465 para SSL)
- **Exemplos:**
  - Gmail: `587`
  - Outlook: `587`
  - Yahoo: `587`

#### **SMTP_USERNAME**
- **Nome:** `SMTP_USERNAME`
- **Valor:** Seu endereço de email completo
- **Exemplo:** `seuemail@gmail.com`

#### **SMTP_PASSWORD**
- **Nome:** `SMTP_PASSWORD`
- **Valor:** Sua senha de email OU senha de aplicativo
- **⚠️ IMPORTANTE:** Para Gmail, use uma **senha de aplicativo**

#### **EMAIL_FROM**
- **Nome:** `EMAIL_FROM`
- **Valor:** Endereço de email que aparecerá como remetente
- **Exemplo:** `clevioferreira@gmail.com`

### 3. 🚀 Configuração para Gmail (Recomendado)

#### **Passo 1: Ativar Autenticação de 2 Fatores**
1. Acesse sua conta Google
2. Vá em **Segurança**
3. Ative **Verificação em duas etapas**

#### **Passo 2: Gerar Senha de Aplicativo**
1. Ainda em **Segurança**
2. Clique em **Senhas de app**
3. Selecione **Email** e **Windows Computer**
4. Copie a senha gerada (16 caracteres)

#### **Passo 3: Configurar Secrets**
```
SMTP_SERVER: smtp.gmail.com
SMTP_PORT: 587
SMTP_USERNAME: clevioferreira@gmail.com
SMTP_PASSWORD: [SENHA_DE_16_CARACTERES]
EMAIL_FROM: clevioferreira@gmail.com
```

### 4. 📧 Configuração para Outlook/Hotmail

```
SMTP_SERVER: smtp-mail.outlook.com
SMTP_PORT: 587
SMTP_USERNAME: seuemail@outlook.com
SMTP_PASSWORD: [SUA_SENHA_NORMAL]
EMAIL_FROM: seuemail@outlook.com
```

### 5. 🔍 Verificar Configuração

Após configurar as secrets:

1. **Execute o workflow manualmente:**
   - Vá para a aba **Actions**
   - Clique em **🚀 Scraper Automatizado com Email**
   - Clique em **Run workflow**

2. **Verifique os logs:**
   - Se houver erro de autenticação, verifique as credenciais
   - Se houver erro de servidor, verifique o SMTP_SERVER e SMTP_PORT

### 6. 🎯 Estrutura Final das Secrets

```
Repository Secrets:
├── SMTP_SERVER: smtp.gmail.com
├── SMTP_PORT: 587
├── SMTP_USERNAME: clevioferreira@gmail.com
├── SMTP_PASSWORD: [SENHA_DE_APLICATIVO]
└── EMAIL_FROM: clevioferreira@gmail.com
```

### 7. 🚨 Solução de Problemas

#### **Erro: "Authentication failed"**
- Verifique se a senha está correta
- Para Gmail, use senha de aplicativo, não a senha normal

#### **Erro: "Connection refused"**
- Verifique SMTP_SERVER e SMTP_PORT
- Teste se o servidor está acessível

#### **Erro: "Sender not allowed"**
- Verifique se EMAIL_FROM é igual ao SMTP_USERNAME
- Para Gmail, ambos devem ser o mesmo email

### 8. ✅ Teste de Configuração

Após configurar tudo:

1. Execute o workflow manualmente
2. Verifique se o email foi recebido em `clevioferreira@gmail.com`
3. O email deve conter o relatório completo das oportunidades

---

**🎉 Com essas configurações, você receberá emails diários com todas as oportunidades de pesquisa!**
