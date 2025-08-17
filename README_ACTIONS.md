# 🚀 GitHub Actions - Como Verificar e Executar

## 🔍 Por que o Action não foi executado?

### 1. **Verificar Status dos Workflows**
- Vá para a aba **Actions** no seu repositório GitHub
- Verifique se há workflows listados
- Clique em cada workflow para ver o histórico de execuções

### 2. **Problemas Comuns**

#### **❌ Cron não executou:**
- **Causa:** GitHub Actions pode ter atrasos ou não executar cron exatamente no horário
- **Solução:** Use múltiplos horários ou execute manualmente

#### **❌ Workflow não aparece:**
- **Causa:** Arquivo `.yml` não está na pasta correta
- **Solução:** Verifique se está em `.github/workflows/`

#### **❌ Erro de sintaxe:**
- **Causa:** YAML mal formatado
- **Solução:** Use um validador YAML online

### 3. 🧪 Teste os Workflows

#### **Workflow de Teste Simples:**
```yaml
name: 🧪 Teste Simples
on:
  schedule:
    - cron: '*/5 * * * *'  # A cada 5 minutos
  workflow_dispatch:         # Manual
  push:                      # No push
```

#### **Workflow Principal:**
```yaml
name: 🚀 Scraper Automatizado com Email
on:
  schedule:
    - cron: '0 8 * * *'   # 8h UTC
    - cron: '0 12 * * *'  # 12h UTC (9h BRT)
    - cron: '0 18 * * *'  # 18h UTC (15h BRT)
  workflow_dispatch:        # Manual
  push:                     # No push
```

## 🚀 Como Executar Manualmente

### **1. Via GitHub Interface:**
1. Vá para **Actions** → **🚀 Scraper Automatizado com Email**
2. Clique em **Run workflow**
3. Selecione a branch (main/master)
4. Clique em **Run workflow**

### **2. Via Push no Repositório:**
```bash
git add .
git commit -m "🚀 Trigger workflow execution"
git push origin main
```

### **3. Verificar Logs:**
- Clique no workflow em execução
- Clique em cada step para ver os logs
- Verifique se há erros

## ⏰ Horários de Execução

### **Cron Schedule (UTC):**
- **08:00 UTC** = 05:00 BRT (Brasília)
- **12:00 UTC** = 09:00 BRT (Brasília) 
- **18:00 UTC** = 15:00 BRT (Brasília)

### **Execuções Automáticas:**
- ✅ **Diárias** nos horários acima
- ✅ **No push** para qualquer branch
- ✅ **Manual** via workflow_dispatch

## 🔧 Solução de Problemas

### **Workflow não executa:**
1. Verifique se está na pasta `.github/workflows/`
2. Verifique sintaxe YAML
3. Execute manualmente primeiro
4. Verifique logs de erro

### **Erro de dependências:**
1. Verifique se os arquivos Python existem
2. Verifique se as dependências estão corretas
3. Teste localmente primeiro

### **Erro de email:**
1. Configure as secrets corretamente
2. Teste com o script `teste_email.py`
3. Verifique logs do step de email

## 📋 Checklist de Verificação

- [ ] Arquivo `.yml` está em `.github/workflows/`
- [ ] Sintaxe YAML está correta
- [ ] Workflow aparece na aba Actions
- [ ] Execução manual funciona
- [ ] Logs não mostram erros
- [ ] Secrets configuradas (para email)
- [ ] Dependências instaladas corretamente

## 🎯 Próximos Passos

1. **Execute o workflow de teste** primeiro
2. **Verifique os logs** para identificar problemas
3. **Execute o workflow principal** manualmente
4. **Configure as secrets** para envio de email
5. **Teste o envio de email** localmente

---

**💡 Dica:** Sempre execute manualmente primeiro para verificar se está funcionando!
