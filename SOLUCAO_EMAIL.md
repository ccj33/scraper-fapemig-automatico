# 🚨 SOLUÇÃO RÁPIDA: Emails Não Estão Funcionando

## ❌ **PROBLEMA IDENTIFICADO**

Baseado no erro que você mostrou:
```
❌ Erro ao enviar email: invalid literal for int() with base 10: ''
```

**O problema é que algumas variáveis de ambiente estão vazias no GitHub Actions!**

## 🔍 **DIAGNÓSTICO AUTOMÁTICO**

Execute este comando no seu repositório para identificar exatamente o que está faltando:

```bash
python diagnostico_email.py
```

## 🚨 **VARIÁVEIS QUE ESTÃO FALTANDO**

Baseado no erro, estas variáveis estão vazias:
- ❌ `SMTP_SERVER` - Vazio
- ❌ `EMAIL_DESTINO` - Vazio
- ⚠️ `SMTP_PORT` - Provavelmente vazio também

## 🔧 **SOLUÇÃO IMEDIATA**

### **1️⃣ Configure os GitHub Secrets (OBRIGATÓRIO)**

1. Vá para seu repositório no GitHub
2. Clique em `Settings` (Configurações)
3. Clique em `Secrets and variables` → `Actions`
4. Clique em `New repository secret`
5. Adicione **TODOS** estes secrets:

| **Secret Name** | **Value** | **Status** |
|-----------------|-----------|------------|
| `SMTP_SERVER` | `smtp.gmail.com` | ❌ **FALTANDO** |
| `SMTP_PORT` | `587` | ❌ **FALTANDO** |
| `EMAIL_USER` | `ccjota51@gmail.com` | ✅ Configurado |
| `EMAIL_PASS` | `[16 CARACTERES]` | ✅ Configurado |
| `EMAIL_FROM` | `ccjota51@gmail.com` | ✅ Configurado |
| `EMAIL_DESTINO` | `ccjota51@gmail.com` | ❌ **FALTANDO** |

### **2️⃣ Gerar Senha de Aplicativo Gmail**

Se `EMAIL_PASS` também estiver vazio:

1. Acesse: [myaccount.google.com](https://myaccount.google.com)
2. Vá para: `Segurança` → `Verificação em duas etapas`
3. Clique em: `Senhas de app`
4. Selecione: `Email` + `Windows Computer`
5. Clique em: `Gerar`
6. **COPIE** a senha de 16 caracteres
7. Cole no secret `EMAIL_PASS`

## 🧪 **TESTE LOCAL ANTES**

Antes de executar no GitHub Actions, teste localmente:

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export EMAIL_USER="ccjota51@gmail.com"
export EMAIL_PASS="sua_senha_de_app"
export EMAIL_FROM="ccjota51@gmail.com"
export EMAIL_DESTINO="ccjota51@gmail.com"

# 3. Executar diagnóstico
python diagnostico_email.py

# 4. Se tudo OK, testar envio
python enviar_email_resultados.py
```

## ✅ **VERIFICAÇÃO FINAL**

Após configurar todos os secrets, execute novamente o workflow. Você deve ver:

```
🔍 VALIDANDO CONFIGURAÇÃO DE EMAIL:
========================================
✅ SMTP_SERVER: smtp.gmail.com
✅ SMTP_PORT: 587
✅ EMAIL_USER: ********
✅ EMAIL_PASS: ****************
✅ EMAIL_FROM: ccjota51@gmail.com
✅ EMAIL_DESTINO: ccjota51@gmail.com

✅ Todas as variáveis estão configuradas corretamente!
```

## 🎯 **RESUMO DO QUE FAZER**

1. **Configure TODOS os 6 GitHub Secrets** listados acima
2. **Execute o diagnóstico local** para confirmar
3. **Execute o workflow** no GitHub Actions
4. **Verifique se o email foi enviado**

## 🆘 **AINDA NÃO FUNCIONA?**

Se após configurar todos os secrets ainda não funcionar:

1. Execute: `python diagnostico_email.py`
2. Verifique os logs do GitHub Actions
3. Confirme se a senha de aplicativo foi gerada corretamente
4. Verifique se a verificação em duas etapas está ativada

---

**🎯 Meta: Receber emails automáticos diários com os resultados dos scrapers!**
