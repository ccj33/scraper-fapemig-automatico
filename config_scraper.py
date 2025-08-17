#!/usr/bin/env python3
"""
Configurações do Scraper de Editais
===================================

Arquivo de configuração centralizada para personalizar o comportamento
do scraper sem modificar o código principal.
"""

# ============================================================================
# CONFIGURAÇÕES GERAIS
# ============================================================================

# Modo de execução
MODO_HEADLESS = False  # True para executar sem abrir navegador
MODO_DEBUG = True      # True para logs detalhados

# Timeouts e aguardas (em segundos)
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
SLEEP_ENTRE_PAGINAS = 3
SLEEP_FAPEMIG = 4
SLEEP_CNPQ = 4

# Configurações do Chrome
CHROME_WINDOW_SIZE = "1920,1080"
CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# ============================================================================
# CONFIGURAÇÕES UFMG
# ============================================================================

UFMG_CONFIG = {
    "url": "https://www.ufmg.br/prograd/editais-chamadas/",
    "palavras_chave": ["edital", "chamada", "seleção", "concurso"],
    "extensoes_pdf": [".pdf"],
    "padroes_data": [
        r'\d{2}/\d{2}/\d{4}',
        r'até \d{2}/\d{2}/\d{4}',
        r'até dia \d{2}/\d{2}/\d{4}',
        r'prazo: \d{2}/\d{2}/\d{4}',
        r'encerra em \d{2}/\d{2}/\d{4}'
    ]
}

# ============================================================================
# CONFIGURAÇÕES FAPEMIG
# ============================================================================

FAPEMIG_CONFIG = {
    "url": "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/?hl=pt-BR",
    "palavras_chave": ["CHAMADA", "PORTARIA", "CREDENCIAMENTO", "EDITAL", "OPORTUNIDADE"],
    "seletores_primarios": ["h5"],
    "seletores_alternativos": ["h3", "h4", ".chamada", ".oportunidade"],
    "padroes_data": [
        r'\d{2}/\d{2}/\d{4}',
        r'\d{2} de \w+ de \d{4}',
        r'até \d{2}/\d{2}/\d{4}',
        r'prazo: \d{2}/\d{2}/\d{4}'
    ],
    "palavras_link_detalhes": ["detalhes", "ver", "abrir", "chamada"]
}

# ============================================================================
# CONFIGURAÇÕES CNPQ
# ============================================================================

CNPQ_CONFIG = {
    "url": "http://memoria2.cnpq.br/web/guest/chamadas-publicas",
    "palavras_chave": ["CHAMADA", "EDITAL", "OPORTUNIDADE", "PROGRAMA", "BOLSA"],
    "seletores_primarios": ["h4"],
    "seletores_alternativos": ["h3", "h5", ".chamada", ".oportunidade", ".edital"],
    "padroes_data": [
        r'\d{2}/\d{2}/\d{4}',
        r'\d{2} de \w+ de \d{4}',
        r'até \d{2}/\d{2}/\d{4}',
        r'prazo: \d{2}/\d{2}/\d{4}',
        r'inscrição: \d{2}/\d{2}/\d{4}'
    ]
}

# ============================================================================
# CONFIGURAÇÕES DE EXTRAÇÃO
# ============================================================================

EXTRACAO_CONFIG = {
    "tamanho_minimo_descricao": 20,
    "tamanho_minimo_titulo": 10,
    "maximo_exemplos_resumo": 2,
    "truncar_descricao_em": 100
}

# ============================================================================
# CONFIGURAÇÕES DE ARQUIVO
# ============================================================================

ARQUIVO_CONFIG = {
    "formato_timestamp": "%Y%m%d_%H%M%S",
    "prefixo_arquivo": "editais_extraidos_",
    "extensao": ".json",
    "encoding": "utf-8",
    "indentacao_json": 2
}

# ============================================================================
# CONFIGURAÇÕES DE LOG
# ============================================================================

LOG_CONFIG = {
    "mostrar_progresso": True,
    "mostrar_erros_detalhados": True,
    "mostrar_resumo": True,
    "mostrar_exemplos": True,
    "simbolos_emoji": True  # True para usar emojis, False para texto simples
}

# ============================================================================
# CONFIGURAÇÕES DE FILTROS
# ============================================================================

FILTROS_CONFIG = {
    "filtrar_duplicatas": True,
    "filtrar_titulos_vazios": True,
    "filtrar_links_invalidos": True,
    "validar_urls": True
}

# ============================================================================
# CONFIGURAÇÕES DE RETRY
# ============================================================================

RETRY_CONFIG = {
    "max_tentativas": 3,
    "delay_entre_tentativas": 2,
    "retry_em_timeout": True,
    "retry_em_elemento_nao_encontrado": False
}

# ============================================================================
# FUNÇÕES DE CONFIGURAÇÃO
# ============================================================================

def obter_config_fonte(fonte):
    """Retorna a configuração para uma fonte específica"""
    configs = {
        "ufmg": UFMG_CONFIG,
        "fapemig": FAPEMIG_CONFIG,
        "cnpq": CNPQ_CONFIG
    }
    return configs.get(fonte.lower(), {})

def obter_palavras_chave(fonte):
    """Retorna as palavras-chave para uma fonte específica"""
    config = obter_config_fonte(fonte)
    return config.get("palavras_chave", [])

def obter_url_fonte(fonte):
    """Retorna a URL para uma fonte específica"""
    config = obter_config_fonte(fonte)
    return config.get("url", "")

def obter_padroes_data(fonte):
    """Retorna os padrões de data para uma fonte específica"""
    config = obter_config_fonte(fonte)
    return config.get("padroes_data", [])

def obter_seletores(fonte):
    """Retorna os seletores para uma fonte específica"""
    config = obter_config_fonte(fonte)
    return {
        "primarios": config.get("seletores_primarios", []),
        "alternativos": config.get("seletores_alternativos", [])
    }

# ============================================================================
# VALIDAÇÃO DE CONFIGURAÇÕES
# ============================================================================

def validar_configuracoes():
    """Valida se todas as configurações estão corretas"""
    erros = []
    
    # Validar URLs
    for fonte in ["ufmg", "fapemig", "cnpq"]:
        url = obter_url_fonte(fonte)
        if not url:
            erros.append(f"URL não configurada para {fonte.upper()}")
        elif not url.startswith(('http://', 'https://')):
            erros.append(f"URL inválida para {fonte.upper()}: {url}")
    
    # Validar timeouts
    if IMPLICIT_WAIT <= 0 or EXPLICIT_WAIT <= 0:
        erros.append("Timeouts devem ser maiores que zero")
    
    # Validar configurações de arquivo
    if not ARQUIVO_CONFIG["formato_timestamp"]:
        erros.append("Formato de timestamp não configurado")
    
    return erros

def mostrar_configuracoes():
    """Mostra as configurações atuais"""
    print("🔧 CONFIGURAÇÕES ATUAIS DO SCRAPER")
    print("=" * 50)
    
    print(f"Modo Headless: {'✅ Ativado' if MODO_HEADLESS else '❌ Desativado'}")
    print(f"Modo Debug: {'✅ Ativado' if MODO_DEBUG else '❌ Desativado'}")
    print(f"Implicit Wait: {IMPLICIT_WAIT}s")
    print(f"Explicit Wait: {EXPLICIT_WAIT}s")
    print(f"Sleep entre páginas: {SLEEP_ENTRE_PAGINAS}s")
    
    print("\n📊 CONFIGURAÇÕES POR FONTE:")
    for fonte in ["ufmg", "fapemig", "cnpq"]:
        config = obter_config_fonte(fonte)
        print(f"\n{fonte.upper()}:")
        print(f"  URL: {config.get('url', 'Não configurada')}")
        print(f"  Palavras-chave: {', '.join(config.get('palavras_chave', []))}")
        print(f"  Padrões de data: {len(config.get('padroes_data', []))} padrões")
    
    # Validar configurações
    erros = validar_configuracoes()
    if erros:
        print(f"\n⚠️ PROBLEMAS ENCONTRADOS:")
        for erro in erros:
            print(f"  - {erro}")
    else:
        print(f"\n✅ Todas as configurações estão válidas!")

if __name__ == "__main__":
    mostrar_configuracoes()
