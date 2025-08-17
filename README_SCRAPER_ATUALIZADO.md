# Scraper Atualizado para Editais e Chamadas

## 📋 Descrição

Script Selenium robusto e atualizado para extrair informações completas de editais e oportunidades de pesquisa dos seguintes sites:

- **🏛️ UFMG** - Universidade Federal de Minas Gerais
- **🔬 FAPEMIG** - Fundação de Amparo à Pesquisa de Minas Gerais  
- **📚 CNPq** - Conselho Nacional de Desenvolvimento Científico e Tecnológico

## ✨ Funcionalidades

### O que é extraído:
- **Título** da chamada/edital
- **Breve descrição** da oportunidade
- **Link para PDF** (quando disponível)
- **Data limite** de submissão
- **Fonte** da informação
- **Timestamp** de coleta

### Características técnicas:
- ✅ **Seletores robustos** adaptados para cada site
- ✅ **Múltiplas estratégias** de extração (fallback)
- ✅ **Tratamento de erros** abrangente
- ✅ **Aguardar carregamento** das páginas
- ✅ **Salvamento automático** em JSON
- ✅ **Relatório detalhado** da extração
- ✅ **Configuração otimizada** do Chrome

## 🚀 Como usar

### 1. Instalação das dependências
```bash
pip install -r requirements.txt
```

### 2. Execução do script
```bash
python scraper_editais_atualizado.py
```

### 3. Modo headless (opcional)
Para executar sem abrir o navegador, descomente a linha:
```python
options.add_argument('--headless')
```

## 📊 Saída

### Console:
- Progresso em tempo real da extração
- Contadores de itens encontrados por fonte
- Resumo final com estatísticas
- Exemplos dos itens encontrados

### Arquivo JSON:
- Salvo automaticamente com timestamp
- Formato: `editais_extraidos_YYYYMMDD_HHMMSS.json`
- Estrutura organizada por fonte
- Dados completos para análise posterior

## 🔧 Configurações

### Timeouts e aguardas:
- **Implicit wait**: 10 segundos
- **Explicit wait**: 15 segundos  
- **Sleep entre páginas**: 3-4 segundos

### Opções do Chrome:
- Janela 1920x1080
- User-Agent personalizado
- Anti-detecção de automação
- Otimizações de performance

## 📁 Estrutura dos dados

```json
{
  "ufmg": [
    {
      "titulo": "Edital de Seleção para Programa de Pós-Graduação",
      "descricao": "Descrição detalhada da oportunidade...",
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

## 🎯 Estratégias de extração

### UFMG:
- Busca por links com texto contendo "edital", "chamada", "seleção"
- Filtra apenas links que terminam em .pdf
- Extrai datas usando regex patterns

### FAPEMIG:
- Busca por títulos h5 com palavras-chave
- Estratégia alternativa para outros elementos
- Busca por descrições em elementos próximos
- Identifica links para PDFs e páginas de detalhes

### CNPq:
- Busca por títulos h4 com palavras-chave
- Navega pela estrutura DOM para encontrar descrições
- Busca por PDFs em elementos anexos
- Estratégia alternativa para outros seletores

## ⚠️ Tratamento de erros

- **TimeoutException**: Aguarda elementos carregarem
- **NoSuchElementException**: Continua para próximo item
- **ElementClickInterceptedException**: Tenta estratégias alternativas
- **Erros genéricos**: Log detalhado para debugging

## 🔄 Manutenção

### Seletores que podem precisar de atualização:
- **FAPEMIG**: Estrutura de páginas pode mudar
- **CNPq**: Layout pode ser atualizado
- **UFMG**: Relativamente estável

### Como adaptar:
1. Inspecionar o HTML da página
2. Identificar novos seletores CSS/XPath
3. Atualizar os métodos correspondentes
4. Testar com pequenas amostras

## 📈 Monitoramento

### Logs úteis:
- ✅ Sucessos com contadores
- ⚠️ Avisos para itens com problemas
- ❌ Erros críticos que impedem extração
- 🔍 Progresso de cada fonte

### Métricas:
- Total de itens por fonte
- Taxa de sucesso na extração
- Tempo total de execução
- Arquivos salvos com sucesso

## 🚨 Solução de problemas

### Navegador não abre:
- Verificar instalação do Chrome
- Atualizar chromedriver-autoinstaller
- Verificar permissões do sistema

### Poucos resultados:
- Verificar conectividade com os sites
- Aumentar timeouts se necessário
- Verificar se os seletores ainda são válidos

### Erros de extração:
- Verificar logs detalhados no console
- Testar sites manualmente no navegador
- Adaptar seletores conforme necessário

## 📝 Exemplo de uso

```python
from scraper_editais_atualizado import ScraperEditaisAtualizado

# Criar instância
scraper = ScraperEditaisAtualizado()

# Executar extração completa
sucesso = scraper.executar_extracao()

# Acessar resultados
if sucesso:
    print(f"UFMG: {len(scraper.resultados['ufmg'])} editais")
    print(f"FAPEMIG: {len(scraper.resultados['fapemig'])} oportunidades")
    print(f"CNPq: {len(scraper.resultados['cnpq'])} chamadas")
```

## 🤝 Contribuições

Para melhorar o scraper:
1. Teste em diferentes ambientes
2. Reporte problemas encontrados
3. Sugira melhorias nos seletores
4. Adicione novas fontes de dados

## 📄 Licença

Este projeto é de uso livre para fins educacionais e de pesquisa.

---

**Última atualização**: Janeiro 2024  
**Versão**: 2.0  
**Compatibilidade**: Python 3.7+, Selenium 4.15+
