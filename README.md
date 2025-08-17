# 🚀 Scraper Simples - Editais e Chamadas

Sistema automatizado para monitorar editais e chamadas da **FAPEMIG** e **CNPq** usando GitHub Actions, executando diariamente e coletando links de PDFs.

## ✨ Funcionalidades

- 🤖 **Execução Automática**: Roda todo dia às 05:00 (horário de Brasília)
- 🕷️ **Scraping Simples**: Coleta apenas links de PDFs e páginas de detalhes
- 📁 **Artefatos**: Salva dados extraídos como arquivos JSON para download
- 🔄 **Execução Manual**: Pode ser executado manualmente quando necessário
- 🎯 **Foco nos Links**: Não baixa PDFs, apenas coleta os links

## 🎯 Sites Monitorados

### **FAPEMIG** (Fundação de Amparo à Pesquisa de Minas Gerais)
- **URL**: http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/
- **Foco**: Editais e chamadas de pesquisa em Minas Gerais

### **CNPq** (Conselho Nacional de Desenvolvimento Científico e Tecnológico)
- **URL**: https://www.gov.br/cnpq/pt-br/acesso-a-informacao/acoes-e-programas/programas/chamadas-publicas
- **Foco**: Chamadas públicas nacionais de pesquisa

## 🛠️ Configuração

### 1. **Preparar o Repositório**

```bash
# Clone este repositório ou crie um novo
git init
git add .
git commit -m "🚀 Inicializar scraper simples de editais"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

### 2. **Dependências**

O sistema usa apenas:
- **Selenium**: Para navegação web
- **ChromeDriver**: Gerenciado automaticamente

## 🚀 Como Funciona

### **Execução Automática**
- ⏰ **Agendamento**: Todo dia às 05:00 (horário de Brasília)
- 🖥️ **Ambiente**: Ubuntu Linux limpo e atualizado
- 🐍 **Python**: Versão 3.10 com dependências mínimas
- 🌐 **Navegador**: Chrome em modo headless (sem interface)

### **Processo de Scraping**
1. **Inicialização**: Configura ambiente e navegador
2. **FAPEMIG**: Acessa site e coleta links de editais/chamadas
3. **CNPq**: Acessa site e coleta links de chamadas públicas
4. **Processamento**: Organiza dados encontrados
5. **Artefatos**: Salva dados para download posterior

### **Estratégia de Extração**
- 🔍 **Links diretos**: Busca por links que terminem em `.pdf`
- 📋 **Páginas de detalhes**: Coleta links para páginas com informações
- 🎯 **Filtros inteligentes**: Identifica editais, chamadas e oportunidades

## 📊 Monitoramento

### **Verificar Execuções**
1. Vá para a aba **Actions** do seu repositório
2. Clique no workflow **🚀 Scraper Simples - Editais e Chamadas**
3. Veja o histórico de execuções e logs

### **Execução Manual**
1. Na aba **Actions**, clique no workflow
2. Clique em **Run workflow**
3. Selecione a branch e clique em **Run workflow**

### **Download de Artefatos**
1. Após cada execução, clique na execução
2. Role para baixo até **Artifacts**
3. Baixe `oportunidades-scraper-[número]` para ver os dados extraídos

## 📁 Estrutura dos Arquivos

```
meu-scraper/
├── scraper_simples.py        # Script principal do scraper
├── requirements.txt           # Dependências Python (mínimas)
├── .github/
│   └── workflows/
│       └── scraper.yml       # Configuração do GitHub Actions
└── README.md                  # Este arquivo
```

## 📋 Formato dos Dados

### **Arquivo JSON de Saída**
```json
{
  "fapemig": [
    {
      "titulo": "Nome da Oportunidade",
      "link_pdf": "http://exemplo.com/edital.pdf",
      "fonte": "FAPEMIG",
      "data_coleta": "2024-01-01T10:00:00"
    }
  ],
  "cnpq": [
    {
      "titulo": "Chamada Pública",
      "link_detalhes": "http://exemplo.com/chamada",
      "fonte": "CNPq",
      "data_coleta": "2024-01-01T10:00:00"
    }
  ],
  "timestamp": "2024-01-01T10:00:00"
}
```

## 🔧 Personalização

### **Adicionar Novos Sites**
Edite `scraper_simples.py` e adicione novos métodos de extração seguindo o padrão existente.

### **Alterar Horário de Execução**
Edite `.github/workflows/scraper.yml`:
```yaml
schedule:
  - cron: "0 8 * * *"   # Formato: minuto hora dia mês dia_semana
```

## 🚨 Limitações

- **Não baixa PDFs**: Apenas coleta links
- **Dependência do Selenium**: Requer Chrome/Chromium
- **Sites podem mudar**: Estrutura dos sites pode alterar

## 📝 Licença

Este projeto é de uso livre para fins educacionais e de pesquisa.
