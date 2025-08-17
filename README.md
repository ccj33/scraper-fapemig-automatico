# 🚀 Scraper FAPEMIG Automatizado - GitHub Actions

Sistema automatizado para monitorar editais e chamadas da FAPEMIG usando GitHub Actions, executando diariamente e enviando notificações por email.

## ✨ Funcionalidades

- 🤖 **Execução Automática**: Roda todo dia às 05:00 (horário de Brasília)
- 🕷️ **Scraping Headless**: Funciona sem interface gráfica no GitHub
- 📧 **Notificações por Email**: Envia resumo das oportunidades encontradas
- 📁 **Artefatos**: Salva dados extraídos como arquivos para download
- 🔄 **Execução Manual**: Pode ser executado manualmente quando necessário

## 🛠️ Configuração

### 1. **Preparar o Repositório**

```bash
# Clone este repositório ou crie um novo
git init
git add .
git commit -m "🚀 Inicializar scraper FAPEMIG automatizado"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

### 2. **Configurar Secrets no GitHub**

No seu repositório GitHub, vá em:
**Settings → Secrets and variables → Actions → New repository secret**

#### **EMAIL_USER**
- **Nome**: `EMAIL_USER`
- **Valor**: Seu email Gmail (ex: `seuemail@gmail.com`)

#### **EMAIL_PASS**
- **Nome**: `EMAIL_PASS`
- **Valor**: Senha de app do Gmail (NÃO sua senha normal!)

### 3. **Como Gerar Senha de App do Gmail**

1. Ative a **Verificação em duas etapas** na sua conta Google
2. Vá em **Gerenciar sua Conta Google → Segurança**
3. Em **Como você faz login no Google**, clique em **Senhas de app**
4. Selecione **Email** e clique em **Gerar**
5. Use essa senha gerada no campo `EMAIL_PASS`

## 🚀 Como Funciona

### **Execução Automática**
- ⏰ **Agendamento**: Todo dia às 05:00 (horário de Brasília)
- 🖥️ **Ambiente**: Ubuntu Linux limpo e atualizado
- 🐍 **Python**: Versão 3.10 com todas as dependências
- 🌐 **Navegador**: Chrome em modo headless (sem interface)

### **Processo de Scraping**
1. **Inicialização**: Configura ambiente e dependências
2. **Navegação**: Acessa https://fapemig.br/chamadas/
3. **Extração**: Busca por chamadas, editais e oportunidades
4. **Processamento**: Organiza dados encontrados
5. **Notificação**: Envia email com resumo
6. **Artefatos**: Salva dados para download posterior

### **Estratégias de Extração**
- 🔍 **Links específicos**: Busca por elementos com "chamada" ou "edital"
- 📋 **Elementos gerais**: Procura por cards, itens e classes comuns
- 📄 **Texto completo**: Extrai conteúdo da página para análise

## 📊 Monitoramento

### **Verificar Execuções**
1. Vá para a aba **Actions** do seu repositório
2. Clique no workflow **🚀 Scraper FAPEMIG Automático**
3. Veja o histórico de execuções e logs

### **Execução Manual**
1. Na aba **Actions**, clique no workflow
2. Clique em **Run workflow**
3. Selecione a branch e clique em **Run workflow**

### **Download de Artefatos**
1. Após cada execução, clique na execução
2. Role para baixo até **Artifacts**
3. Baixe `dados-scraper-[número]` para ver os dados extraídos

## 📁 Estrutura dos Arquivos

```
meu-scraper/
├── scraper.py              # Script principal do scraper
├── requirements.txt         # Dependências Python
├── .github/
│   └── workflows/
│       └── scraper.yml     # Configuração do GitHub Actions
└── README.md               # Este arquivo
```

## 🔧 Personalização

### **Alterar Horário de Execução**
Edite `.github/workflows/scraper.yml`:
```yaml
schedule:
  - cron: "0 8 * * *"   # 08:00 UTC = 05:00 BRT
```

### **Modificar URL de Scraping**
Edite `scraper.py`:
```python
url_fapemig = "https://fapemig.br/chamadas/"
```

### **Ajustar Estratégias de Extração**
Modifique as funções de busca em `scraper.py` para adaptar ao site específico.

## 🚨 Troubleshooting

### **Erro: "Chrome não inicia"**
- ✅ Normal no GitHub Actions - o modo headless funciona sem problemas
- ⚠️ Se testar localmente, pode precisar do Chrome instalado

### **Erro: "Email não enviado"**
- ✅ Verifique se os secrets `EMAIL_USER` e `EMAIL_PASS` estão configurados
- ✅ Confirme se a verificação em duas etapas está ativada no Gmail
- ✅ Use senha de app, não senha normal da conta

### **Nenhuma chamada encontrada**
- 🔍 Verifique se a URL ainda está válida
- 🔍 O site pode ter mudado sua estrutura
- 🔍 Ajuste as estratégias de extração no código

### **Execução muito lenta**
- ⏱️ Normal na primeira execução (download de dependências)
- ⏱️ Execuções subsequentes são mais rápidas
- ⏱️ O GitHub Actions tem limites de tempo (6 horas por job)

## 📈 Logs e Debug

### **Ver Logs Completos**
1. Vá para **Actions → [Execução específica]**
2. Clique em **🚀 Executar scraper**
3. Veja todos os logs de execução

### **Arquivos de Debug**
- `chamadas_encontradas.json`: Dados extraídos em formato estruturado
- `pagina_fapemig.txt`: Texto completo da página para análise

## 🔒 Segurança

- 🔐 **Secrets**: Credenciais ficam protegidas no GitHub
- 🌐 **HTTPS**: Todas as conexões são seguras
- 🚫 **Sem exposição**: Dados sensíveis não aparecem nos logs
- 📧 **Email próprio**: Notificações vão apenas para você

## 🎯 Próximos Passos

1. ✅ **Configure os secrets** no GitHub
2. ✅ **Faça push** do código
3. ✅ **Verifique a primeira execução** automática
4. ✅ **Teste execução manual** se necessário
5. ✅ **Monitore** as execuções diárias
6. ✅ **Ajuste** estratégias de extração conforme necessário

## 📞 Suporte

- 📖 **Documentação**: Este README
- 🐛 **Issues**: Use a aba Issues do GitHub para reportar problemas
- 🔄 **Updates**: Mantenha o repositório atualizado

---

**🎉 Seu scraper FAPEMIG está pronto para rodar automaticamente no GitHub!**

**⏰ Execução**: Todo dia às 05:00 (BRT)  
**📧 Notificações**: Automáticas por email  
**🤖 Automação**: Totalmente hands-free  
**📊 Dados**: Salvos como artefatos para download
