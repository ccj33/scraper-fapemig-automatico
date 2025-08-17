# Sistema de Scraping com Extração de PDFs 🚀

Este sistema avançado combina web scraping tradicional com **extração inteligente de dados de PDFs**, permitindo obter informações muito mais completas e precisas dos editais e chamadas.

## ✨ Funcionalidades Principais

### 🔍 **Scraping Tradicional**
- Coleta de editais da **UFMG**
- Oportunidades da **FAPEMIG** 
- Chamadas do **CNPq**

### 📄 **Extração de PDFs (NOVO!)**
- **Download automático** de PDFs dos links coletados
- **Extração de texto** usando PyMuPDF e PyPDF2
- **Análise inteligente** do conteúdo
- **Complementação automática** de dados faltantes

### 📊 **Relatórios Enriquecidos**
- Dados originais + informações dos PDFs
- Estatísticas de extração
- Análise de conteúdo
- Detecção de idioma

## 🛠️ Instalação

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Verificar Bibliotecas
O sistema usa:
- `PyMuPDF` (fitz) - Extração robusta de PDFs
- `PyPDF2` - Fallback para PDFs simples
- `requests` - Download de arquivos
- `selenium` - Scraping web

## 🚀 Como Usar

### Opção 1: Sistema Completo
```python
from scraper_com_pdf import ScraperComPDF

scraper = ScraperComPDF()
resultado = scraper.executar_scraping_completo()

if resultado:
    print(f"✅ {resultado['dados_enriquecidos']['pdf_metadata']['total_pdfs_processados']} PDFs extraídos!")
```

### Opção 2: Apenas Extração de PDFs
```python
# Para dados já coletados
dados_existentes = {...}  # Seus dados de scraping
scraper = ScraperComPDF()
dados_enriquecidos = scraper.executar_apenas_pdfs(dados_existentes)
```

### Opção 3: Componentes Individuais
```python
# Extrator de PDFs
from extrator_pdf import ExtratorPDF
extrator = ExtratorPDF()
dados_pdf = extrator.extrair_de_url("https://exemplo.com/edital.pdf")

# Integrador
from integrador_pdf import IntegradorPDF
integrador = IntegradorPDF()
dados_enriquecidos = integrador.processar_editais_com_pdfs(dados_scraping)
```

## 📄 O que é Extraído dos PDFs

### 🔍 **Metadados Básicos**
- Número de páginas
- Tamanho do arquivo
- Metadados do documento

### 💰 **Informações Financeiras**
- Valores de bolsas/recursos
- Limites de investimento
- Custos elegíveis

### ⏰ **Prazos e Datas**
- Períodos de inscrição
- Datas de submissão
- Cronogramas

### 🎯 **Objetivos e Descrições**
- Objetivos dos editais
- Áreas temáticas
- Linhas de pesquisa

### 🌍 **Análise de Conteúdo**
- Detecção de idioma
- Estatísticas de texto
- Padrões encontrados

## 📊 Exemplo de Saída

```json
{
  "ufmg": [
    {
      "titulo": "Edital PROEX 2025",
      "valor": "R$ 5.000,00",
      "pdf_extraido": true,
      "pdf_paginas": 15,
      "pdf_valor_encontrado": "R$ 5.000,00",
      "pdf_prazo_encontrado": "30/09/2025",
      "pdf_objetivo_encontrado": "Apoiar eventos acadêmicos",
      "pdf_idioma": "português",
      "valor_fonte": "PDF extraído"
    }
  ],
  "pdf_metadata": {
    "total_pdfs_processados": 1,
    "data_processamento": "2025-01-16T10:30:00"
  }
}
```

## 🔧 Configurações

### Diretório de Downloads
```python
extrator = ExtratorPDF(diretorio_downloads="meus_pdfs")
```

### Timeouts e Delays
```python
# No extrator_pdf.py
response = requests.get(url, headers=headers, timeout=30)  # 30s timeout
time.sleep(2)  # 2s delay entre PDFs
```

## 📈 Benefícios

### ✅ **Dados Mais Completos**
- Informações que não estão nas páginas web
- Detalhes específicos dos editais
- Metadados dos documentos

### ✅ **Precisão Aumentada**
- Dados extraídos diretamente dos PDFs
- Menos dependência de parsing de HTML
- Informações sempre atualizadas

### ✅ **Automação Inteligente**
- Complementação automática de campos
- Detecção de padrões
- Análise de conteúdo

## 🚨 Limitações e Considerações

### ⚠️ **Tamanho dos PDFs**
- PDFs muito grandes podem ser lentos
- Alguns PDFs podem ter proteções
- Arquivos corrompidos podem falhar

### ⚠️ **Qualidade do Texto**
- PDFs escaneados podem ter OCR ruim
- Layouts complexos podem confundir
- Idiomas não suportados

### ⚠️ **Rate Limiting**
- Respeitar limites dos servidores
- Delays entre downloads
- Headers apropriados

## 🧪 Testes

### Teste Básico
```bash
python extrator_pdf.py
```

### Teste de Integração
```bash
python integrador_pdf.py
```

### Teste Completo
```bash
python scraper_com_pdf.py
```

## 📁 Estrutura de Arquivos

```
meu-scraper/
├── extrator_pdf.py          # Extração de PDFs
├── integrador_pdf.py        # Integração com scraping
├── scraper_com_pdf.py       # Sistema completo
├── gerador_resumo_melhorado.py  # Relatórios enriquecidos
├── scraper_unificado.py     # Scraping original
├── requirements.txt          # Dependências
└── downloads_pdf/           # PDFs baixados (criado automaticamente)
```

## 🔄 Fluxo de Trabalho

1. **Scraping** → Coleta links e dados básicos
2. **Detecção** → Identifica URLs de PDFs
3. **Download** → Baixa PDFs automaticamente
4. **Extração** → Extrai texto e analisa conteúdo
5. **Integração** → Combina dados originais + PDFs
6. **Relatório** → Gera relatórios enriquecidos
7. **Limpeza** → Remove arquivos temporários

## 🆘 Solução de Problemas

### Erro: "PyMuPDF não encontrado"
```bash
pip install PyMuPDF
```

### Erro: "Falha ao baixar PDF"
- Verificar se a URL é acessível
- Verificar permissões de rede
- Aumentar timeout se necessário

### Erro: "Falha na extração"
- PDF pode estar protegido
- Arquivo pode estar corrompido
- Tentar com PyPDF2 como fallback

## 🚀 Próximos Passos

- [ ] Suporte a mais formatos (DOC, DOCX)
- [ ] OCR para PDFs escaneados
- [ ] Análise de tabelas em PDFs
- [ ] Machine Learning para extração
- [ ] Interface web para visualização

## 📞 Suporte

Para dúvidas ou problemas:
- Verificar logs em `scraper_com_pdf.log`
- Testar componentes individualmente
- Verificar dependências instaladas

---

**🎯 Resultado Final**: Sistema que não só coleta links, mas **extrai e analisa o conteúdo real dos documentos**, fornecendo dados muito mais ricos e úteis para análise de oportunidades!
