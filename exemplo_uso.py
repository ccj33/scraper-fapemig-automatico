#!/usr/bin/env python3
"""
Exemplos de Uso do Scraper de Editais Atualizado
=================================================

Este arquivo demonstra diferentes formas de usar o scraper:
1. Execução completa automática
2. Execução por fonte específica
3. Uso programático personalizado
4. Configurações customizadas
"""

import json
from datetime import datetime
from scraper_editais_atualizado import ScraperEditaisAtualizado
from config_scraper import *

def exemplo_execucao_completa():
    """Exemplo 1: Execução completa automática"""
    print("🚀 EXEMPLO 1: Execução Completa Automática")
    print("=" * 50)
    
    scraper = ScraperEditaisAtualizado()
    sucesso = scraper.executar_extracao()
    
    if sucesso:
        print("✅ Execução completa bem-sucedida!")
        return scraper.resultados
    else:
        print("❌ Execução completa falhou!")
        return None

def exemplo_por_fonte():
    """Exemplo 2: Executar apenas uma fonte específica"""
    print("\n🚀 EXEMPLO 2: Execução por Fonte Específica")
    print("=" * 50)
    
    scraper = ScraperEditaisAtualizado()
    
    if not scraper.configurar_navegador():
        print("❌ Falha ao configurar navegador")
        return None
    
    try:
        # Escolher fonte (ufmg, fapemig, cnpq)
        fonte = "ufmg"  # Pode ser alterado
        
        print(f"🔍 Extraindo apenas da fonte: {fonte.upper()}")
        
        if fonte == "ufmg":
            scraper.extrair_ufmg()
        elif fonte == "fapemig":
            scraper.extrair_fapemig()
        elif fonte == "cnpq":
            scraper.extrair_cnpq()
        else:
            print(f"❌ Fonte '{fonte}' não reconhecida")
            return None
        
        # Mostrar resultados
        resultados = scraper.resultados[fonte]
        print(f"\n📊 Resultados da {fonte.upper()}: {len(resultados)} itens")
        
        for i, resultado in enumerate(resultados[:3]):  # Mostrar apenas 3
            print(f"\n{i+1}. {resultado['titulo']}")
            if resultado.get('link_pdf'):
                print(f"   PDF: {resultado['link_pdf']}")
            if resultado.get('data_limite'):
                print(f"   Data: {resultado['data_limite']}")
        
        return scraper.resultados
        
    finally:
        scraper.driver.quit()

def exemplo_uso_programatico():
    """Exemplo 3: Uso programático personalizado"""
    print("\n🚀 EXEMPLO 3: Uso Programático Personalizado")
    print("=" * 50)
    
    scraper = ScraperEditaisAtualizado()
    
    if not scraper.configurar_navegador():
        print("❌ Falha ao configurar navegador")
        return None
    
    try:
        resultados_personalizados = {
            'ufmg': [],
            'fapemig': [],
            'cnpq': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Extrair UFMG com filtros personalizados
        print("🔍 Extraindo UFMG com filtros personalizados...")
        scraper.extrair_ufmg()
        
        # Filtrar apenas editais com PDF
        for resultado in scraper.resultados['ufmg']:
            if resultado.get('link_pdf'):
                resultados_personalizados['ufmg'].append(resultado)
        
        print(f"✅ UFMG: {len(resultados_personalizados['ufmg'])} editais com PDF")
        
        # Extrair FAPEMIG
        print("🔍 Extraindo FAPEMIG...")
        scraper.extrair_fapemig()
        resultados_personalizados['fapemig'] = scraper.resultados['fapemig']
        
        # Extrair CNPq
        print("🔍 Extraindo CNPq...")
        scraper.extrair_cnpq()
        resultados_personalizados['cnpq'] = scraper.resultados['cnpq']
        
        # Salvar resultados personalizados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"resultados_personalizados_{timestamp}.json"
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(resultados_personalizados, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Resultados personalizados salvos em: {nome_arquivo}")
        
        # Mostrar estatísticas
        total_ufmg = len(resultados_personalizados['ufmg'])
        total_fapemig = len(resultados_personalizados['fapemig'])
        total_cnpq = len(resultados_personalizados['cnpq'])
        total_geral = total_ufmg + total_fapemig + total_cnpq
        
        print(f"\n📊 ESTATÍSTICAS PERSONALIZADAS:")
        print(f"   UFMG (com PDF): {total_ufmg}")
        print(f"   FAPEMIG: {total_fapemig}")
        print(f"   CNPq: {total_cnpq}")
        print(f"   TOTAL: {total_geral}")
        
        return resultados_personalizados
        
    finally:
        scraper.driver.quit()

def exemplo_configuracoes_customizadas():
    """Exemplo 4: Configurações customizadas"""
    print("\n🚀 EXEMPLO 4: Configurações Customizadas")
    print("=" * 50)
    
    # Mostrar configurações atuais
    print("🔧 Configurações atuais:")
    print(f"   Modo Headless: {MODO_HEADLESS}")
    print(f"   Implicit Wait: {IMPLICIT_WAIT}s")
    print(f"   Explicit Wait: {EXPLICIT_WAIT}s")
    
    # Mostrar configurações por fonte
    print("\n📊 Configurações por fonte:")
    for fonte in ["ufmg", "fapemig", "cnpq"]:
        config = obter_config_fonte(fonte)
        print(f"\n   {fonte.upper()}:")
        print(f"     URL: {config.get('url', 'Não configurada')}")
        print(f"     Palavras-chave: {', '.join(config.get('palavras_chave', []))}")
        print(f"     Padrões de data: {len(config.get('padroes_data', []))}")
    
    # Mostrar configurações de extração
    print(f"\n🔍 Configurações de extração:")
    print(f"   Tamanho mínimo descrição: {EXTRACAO_CONFIG['tamanho_minimo_descricao']}")
    print(f"   Tamanho mínimo título: {EXTRACAO_CONFIG['tamanho_minimo_titulo']}")
    print(f"   Máximo exemplos resumo: {EXTRACAO_CONFIG['maximo_exemplos_resumo']}")
    
    # Mostrar configurações de arquivo
    print(f"\n📁 Configurações de arquivo:")
    print(f"   Formato timestamp: {ARQUIVO_CONFIG['formato_timestamp']}")
    print(f"   Prefixo: {ARQUIVO_CONFIG['prefixo_arquivo']}")
    print(f"   Encoding: {ARQUIVO_CONFIG['encoding']}")
    
    return True

def exemplo_filtros_avancados():
    """Exemplo 5: Filtros avançados nos resultados"""
    print("\n🚀 EXEMPLO 5: Filtros Avançados")
    print("=" * 50)
    
    # Simular resultados para demonstração
    resultados_exemplo = {
        'ufmg': [
            {
                'titulo': 'Edital de Seleção para Pós-Graduação 2024',
                'descricao': 'Programa de mestrado em Ciência da Computação',
                'link_pdf': 'https://exemplo.com/edital1.pdf',
                'data_limite': '15/03/2024',
                'fonte': 'UFMG'
            },
            {
                'titulo': 'Chamada para Bolsas de Iniciação Científica',
                'descricao': 'Bolsas PIBIC para alunos de graduação',
                'link_pdf': 'https://exemplo.com/edital2.pdf',
                'data_limite': '30/04/2024',
                'fonte': 'UFMG'
            }
        ],
        'fapemig': [
            {
                'titulo': 'CHAMADA FAPEMIG 01/2024',
                'descricao': 'Apoio a projetos de pesquisa em tecnologia',
                'link_pdf': '',
                'data_limite': '20/02/2024',
                'fonte': 'FAPEMIG'
            }
        ]
    }
    
    print("📋 Aplicando filtros avançados...")
    
    # Filtro 1: Apenas editais com PDF
    editais_com_pdf = []
    for fonte, resultados in resultados_exemplo.items():
        for resultado in resultados:
            if resultado.get('link_pdf'):
                editais_com_pdf.append(resultado)
    
    print(f"✅ Editais com PDF: {len(editais_com_pdf)}")
    
    # Filtro 2: Apenas editais com data limite próxima (exemplo: até março)
    editais_marco = []
    for fonte, resultados in resultados_exemplo.items():
        for resultado in resultados:
            if resultado.get('data_limite'):
                data = resultado['data_limite']
                if '/03/' in data or '/04/' in data:  # Simplificado para exemplo
                    editais_marco.append(resultado)
    
    print(f"✅ Editais até abril: {len(editais_marco)}")
    
    # Filtro 3: Buscar por palavras-chave específicas
    editais_tecnologia = []
    palavras_chave = ['tecnologia', 'computação', 'ciência']
    
    for fonte, resultados in resultados_exemplo.items():
        for resultado in resultados:
            titulo_desc = f"{resultado['titulo']} {resultado['descricao']}".lower()
            if any(palavra in titulo_desc for palavra in palavras_chave):
                editais_tecnologia.append(resultado)
    
    print(f"✅ Editais relacionados a tecnologia: {len(editais_tecnologia)}")
    
    # Mostrar resultados filtrados
    print(f"\n📊 RESULTADOS DOS FILTROS:")
    print(f"   Com PDF: {len(editais_com_pdf)}")
    print(f"   Até abril: {len(editais_marco)}")
    print(f"   Tecnologia: {len(editais_tecnologia)}")
    
    return {
        'com_pdf': editais_com_pdf,
        'ate_abril': editais_marco,
        'tecnologia': editais_tecnologia
    }

def main():
    """Função principal que executa todos os exemplos"""
    print("🎯 EXEMPLOS DE USO DO SCRAPER DE EDITAIS")
    print("=" * 60)
    
    exemplos = [
        ("Configurações", exemplo_configuracoes_customizadas),
        ("Filtros Avançados", exemplo_filtros_avancados),
        # Descomente os exemplos abaixo para executar (podem demorar)
        # ("Execução Completa", exemplo_execucao_completa),
        # ("Por Fonte", exemplo_por_fonte),
        # ("Programático", exemplo_uso_programatico),
    ]
    
    for nome_exemplo, funcao_exemplo in exemplos:
        print(f"\n{'='*20} {nome_exemplo} {'='*20}")
        try:
            resultado = funcao_exemplo()
            if resultado:
                print(f"✅ Exemplo '{nome_exemplo}' executado com sucesso!")
            else:
                print(f"⚠️ Exemplo '{nome_exemplo}' executado, mas sem resultados")
        except Exception as e:
            print(f"❌ Erro no exemplo '{nome_exemplo}': {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Todos os exemplos foram executados!")
    print("\n💡 Para executar o scraper completo:")
    print("   python scraper_editais_atualizado.py")
    print("\n💡 Para ver as configurações:")
    print("   python config_scraper.py")

if __name__ == "__main__":
    main()
