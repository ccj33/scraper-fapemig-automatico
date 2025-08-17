# ✅ CHECKLIST - CONFIGURAÇÃO DE SECRETS GITHUB

## 🎯 **OBJETIVO: Configurar envio de emails automáticos**

### **📋 PASSO A PASSO COMPLETO**

#### **🔑 PASSO 1: Acessar GitHub**
- [ ] Abrir: `https://github.com/[seu-usuario]/meu-scraper`
- [ ] Clicar em **Settings** (aba de configurações)
- [ ] No menu lateral, clicar em **Secrets and variables**
- [ ] Clicar em **Actions**

#### **📧 PASSO 2: Configurar Secrets**
- [ ] **SMTP_SERVER**
  - [ ] Clicar em **New repository secret**
  - [ ] Name: `SMTP_SERVER`
  - [ ] Value: `smtp.gmail.com`
  - [ ] Clicar em **Add secret**

- [ ] **SMTP_PORT**
  - [ ] Clicar em **New repository secret**
  - [ ] Name: `SMTP_PORT`
  - [ ] Value: `587`
  - [ ] Clicar em **Add secret**

- [ ] **SMTP_USERNAME**
  - [ ] Clicar em **New repository secret**
  - [ ] Name: `SMTP_USERNAME`
  - [ ] Value: `ccjota51@gmail.com`
  - [ ] Clicar em **Add secret**

- [ ] **SMTP_PASSWORD**
  - [ ] Clicar em **New repository secret**
  - [ ] Name: `SMTP_PASSWORD`
  - [ ] Value: `[SENHA_DE_16_CARACTERES]` ← Gerar no Gmail
  - [ ] Clicar em **Add secret**

- [ ] **EMAIL_FROM**
  - [ ] Clicar em **New repository secret**
  - [ ] Name: `EMAIL_FROM`
  - [ ] Value: `ccjota51@gmail.com`
  - [ ] Clicar em **Add secret**

#### **🔐 PASSO 3: Gerar Senha de Aplicativo Gmail**
- [ ] Acessar: `https://myaccount.google.com/`
- [ ] Fazer login com `clevioferreira@gmail.com`
- [ ] Clicar em **Segurança**
- [ ] Ativar **Verificação em duas etapas** (se não estiver)
- [ ] Clicar em **Senhas de app**
- [ ] Selecionar **Email** + **Windows Computer**
- [ ] Clicar em **Gerar**
- [ ] **COPIAR senha de 16 caracteres**
- [ ] Voltar ao GitHub e colar na secret `SMTP_PASSWORD`

#### **🧪 PASSO 4: Testar Configuração**
- [ ] Voltar para aba **Actions** no GitHub
- [ ] Clicar em **🚀 Scraper Automatizado com Email**
- [ ] Clicar em **Run workflow**
- [ ] Aguardar execução
- [ ] Verificar se email foi recebido em `clevioferreira@gmail.com`

## 🎉 **RESULTADO ESPERADO**

Após configurar tudo:
- ✅ Workflow executa sem erros
- ✅ Email é enviado automaticamente
- ✅ Relatório completo das oportunidades
- ✅ Sistema funciona 3x por dia (8h, 12h, 18h UTC)

## 🚨 **PROBLEMAS COMUNS**

- **Erro "Server address must be specified"** → Secret `SMTP_SERVER` não configurada
- **Erro "Authentication failed"** → Secret `SMTP_PASSWORD` incorreta
- **Erro "Connection refused"** → Secret `SMTP_PORT` incorreta

## 📞 **SUPORTE**

Se tiver dúvidas:
1. Verificar se todas as 5 secrets estão configuradas
2. Confirmar se a senha de aplicativo tem 16 caracteres
3. Testar com workflow manual primeiro

---

**🎯 META: Configurar 5 secrets para receber emails automáticos diários!**
