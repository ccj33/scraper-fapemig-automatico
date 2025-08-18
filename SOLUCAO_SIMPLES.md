# 🎯 SOLUÇÃO SUPER SIMPLES: Apenas 2 Variáveis!

## ✅ **AGORA É MUITO MAIS FÁCIL!**

**Só precisa de 2 GitHub Secrets:**

| **Secret** | **Valor** |
|------------|-----------|
| `EMAIL_USER` | `ccjota51@gmail.com` |
| `EMAIL_PASS` | `[16 CARACTERES]` |

## 🔧 **CONFIGURAÇÃO EM 2 MINUTOS:**

1. **Vá para**: `Settings` → `Secrets and variables` → `Actions`
2. **Clique em**: `New repository secret`
3. **Adicione apenas estes 2**:

### **Secret 1: EMAIL_USER**
- **Name**: `EMAIL_USER`
- **Value**: `ccjota51@gmail.com`

### **Secret 2: EMAIL_PASS**
- **Name**: `EMAIL_PASS`
- **Value**: `[SENHA_DE_16_CARACTERES]`

## 🔑 **GERAR SENHA DE APLICATIVO:**

1. Acesse: [myaccount.google.com](https://myaccount.google.com)
2. Vá para: `Segurança` → `Verificação em duas etapas`
3. Clique em: `Senhas de app`
4. Selecione: `Email` + `Windows Computer`
5. Clique em: `Gerar`
6. **COPIE** a senha de 16 caracteres
7. Cole no secret `EMAIL_PASS`

## 🚀 **PRONTO!**

Agora execute o workflow e você receberá emails automaticamente!

## 🧪 **TESTE LOCAL:**

```bash
# Configurar apenas 2 variáveis
export EMAIL_USER="ccjota51@gmail.com"
export EMAIL_PASS="sua_senha_de_app"

# Testar
python enviar_email_simples.py
```

---

**🎯 Meta: Receber emails com apenas 2 configurações!**
