# 🚀 Guia de Instalação e Uso - Scraper de Editais

## 📋 Pré-requisitos

### Sistema Operacional
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, CentOS 7+)

### Software Necessário
- ✅ **Python 3.7+** (recomendado: Python 3.9+)
- ✅ **Google Chrome** (versão mais recente)
- ✅ **Git** (para clonar o repositório)

### Hardware Recomendado
- 💻 **RAM**: Mínimo 4GB, recomendado 8GB+
- 💾 **Espaço**: Mínimo 1GB livre
- 🌐 **Internet**: Conexão estável

## 🔧 Instalação

### 1. Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd meu-scraper
```

### 2. Criar Ambiente Virtual (Recomendado)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Verificar Instalação
```bash
python teste_scraper.py
```

## 🎯 Uso Básico

### Execução Simples
```bash
python scraper_editais_atualizado.py
```

### Execução em Modo Headless
1. Editar `config_scraper.py`
2. Alterar `MODO_HEADLESS = True`
3. Executar normalmente

### Execução por Fonte Específica
```python
from scraper_editais_atualizado import ScraperEditaisAtualizado

scraper = ScraperEditaisAtualizado()
scraper.configurar_navegador()

# Apenas UFMG
scraper.extrair_ufmg()

# Apenas FAPEMIG
scraper.extrair_fapemig()

# Apenas CNPq
scraper.extrair_cnpq()

scraper.driver.quit()
```

## ⚙️ Configurações

### Arquivo de Configuração
Edite `config_scraper.py` para personalizar:

```python
# Modo de execução
MODO_HEADLESS = False  # True para executar sem abrir navegador
MODO_DEBUG = True      # True para logs detalhados

# Timeouts
IMPLICIT_WAIT = 10     # Segundos
EXPLICIT_WAIT = 15     # Segundos
SLEEP_ENTRE_PAGINAS = 3 # Segundos

# URLs das fontes
UFMG_CONFIG = {
    "url": "https://www.ufmg.br/prograd/editais-chamadas/",
    "palavras_chave": ["edital", "chamada", "seleção", "concurso"]
}
```

### Verificar Configurações
```bash
python config_scraper.py
```

## 📊 Saídas e Resultados

### Console
- Progresso em tempo real
- Contadores por fonte
- Resumo final
- Exemplos encontrados

### Arquivo JSON
- Salvo automaticamente
- Nome: `editais_extraidos_YYYYMMDD_HHMMSS.json`
- Estrutura organizada por fonte

### Estrutura dos Dados
```json
{
  "ufmg": [
    {
      "titulo": "Edital de Seleção para Pós-Graduação",
      "descricao": "Descrição detalhada...",
      "link_pdf": "https://exemplo.com/edital.pdf",
      "data_limite": "15/12/2024",
      "fonte": "UFMG",
      "data_coleta": "2024-01-15T10:30:00"
    }
  ],
  "fapemig": [...],
  "cnpq": [...],
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🔍 Exemplos de Uso

### Exemplo 1: Execução Completa
```bash
python scraper_editais_atualizado.py
```

### Exemplo 2: Uso Programático
```python
from scraper_editais_atualizado import ScraperEditaisAtualizado

scraper = ScraperEditaisAtualizado()
resultados = scraper.executar_extracao()

if resultados:
    print(f"UFMG: {len(resultados['ufmg'])} editais")
    print(f"FAPEMIG: {len(resultados['fapemig'])} oportunidades")
    print(f"CNPq: {len(resultados['cnpq'])} chamadas")
```

### Exemplo 3: Filtros Personalizados
```python
# Filtrar apenas editais com PDF
editais_com_pdf = []
for fonte, resultados in scraper.resultados.items():
    for resultado in resultados:
        if resultado.get('link_pdf'):
            editais_com_pdf.append(resultado)

print(f"Editais com PDF: {len(editais_com_pdf)}")
```

### Exemplo 4: Busca por Palavras-chave
```python
# Buscar editais relacionados a tecnologia
palavras_chave = ['tecnologia', 'computação', 'ciência']
editais_tecnologia = []

for fonte, resultados in scraper.resultados.items():
    for resultado in resultados:
        titulo_desc = f"{resultado['titulo']} {resultado['descricao']}".lower()
        if any(palavra in titulo_desc for palavra in palavras_chave):
            editais_tecnologia.append(resultado)
```

## 🚨 Solução de Problemas

### Erro: "Chrome não encontrado"
```bash
# Verificar se o Chrome está instalado
# Baixar e instalar: https://www.google.com/chrome/
```

### Erro: "ChromeDriver não encontrado"
```bash
# O chromedriver-autoinstaller deve resolver automaticamente
# Se persistir, instalar manualmente:
pip install --upgrade chromedriver-autoinstaller
```

### Erro: "Elemento não encontrado"
- Verificar se os seletores ainda são válidos
- Inspecionar o HTML das páginas
- Atualizar seletores em `config_scraper.py`

### Erro: "Timeout"
- Aumentar `EXPLICIT_WAIT` em `config_scraper.py`
- Verificar conexão com internet
- Verificar se os sites estão funcionando

### Poucos Resultados
- Verificar se os sites mudaram de estrutura
- Ajustar palavras-chave em `config_scraper.py`
- Verificar se há bloqueios anti-bot

## 🔄 Manutenção

### Atualizar Seletores
1. Inspecionar HTML das páginas
2. Identificar novos seletores CSS/XPath
3. Atualizar `config_scraper.py`
4. Testar com pequenas amostras

### Adicionar Novas Fontes
1. Criar nova configuração em `config_scraper.py`
2. Adicionar método de extração em `scraper_editais_atualizado.py`
3. Atualizar método principal
4. Testar e validar

### Monitorar Mudanças
- Verificar regularmente se os sites funcionam
- Acompanhar mudanças na estrutura HTML
- Atualizar seletores conforme necessário

## 📈 Monitoramento e Logs

### Logs Úteis
- ✅ Sucessos com contadores
- ⚠️ Avisos para itens com problemas
- ❌ Erros críticos
- 🔍 Progresso de cada fonte

### Métricas
- Total de itens por fonte
- Taxa de sucesso na extração
- Tempo total de execução
- Arquivos salvos com sucesso

## 🎯 Casos de Uso

### Pesquisadores
- Monitorar oportunidades de bolsas
- Acompanhar editais de pesquisa
- Identificar prazos importantes

### Estudantes
- Buscar programas de pós-graduação
- Encontrar bolsas de estudo
- Acompanhar concursos

### Instituições
- Monitorar concorrência
- Acompanhar tendências do setor
- Identificar oportunidades de parceria

## 🤝 Contribuições

### Como Contribuir
1. Testar em diferentes ambientes
2. Reportar problemas encontrados
3. Sugerir melhorias nos seletores
4. Adicionar novas fontes de dados

### Reportar Bugs
- Descrever o problema detalhadamente
- Incluir logs de erro
- Especificar ambiente (OS, Python, Chrome)
- Anexar screenshots se relevante

### Sugerir Melhorias
- Explicar a funcionalidade desejada
- Descrever benefícios
- Fornecer exemplos de uso
- Considerar impacto na performance

## 📚 Recursos Adicionais

### Documentação
- `README_SCRAPER_ATUALIZADO.md` - Documentação técnica
- `config_scraper.py` - Configurações centralizadas
- `exemplo_uso.py` - Exemplos práticos

### Testes
- `teste_scraper.py` - Validação da instalação
- Executar antes de usar em produção

### Suporte
- Verificar logs detalhados
- Consultar configurações
- Testar com exemplos básicos

---

## 🎉 Pronto para Usar!

Agora você tem um scraper robusto e configurável para extrair editais e oportunidades de pesquisa. 

**Próximos passos:**
1. ✅ Instalar dependências
2. ✅ Testar instalação
3. ✅ Configurar conforme necessário
4. ✅ Executar primeira extração
5. ✅ Analisar resultados
6. ✅ Personalizar filtros

**Comandos principais:**
```bash
# Testar instalação
python teste_scraper.py

# Ver configurações
python config_scraper.py

# Executar scraper
python scraper_editais_atualizado.py

# Ver exemplos
python exemplo_uso.py
```

**Boa sorte com suas extrações! 🚀**
