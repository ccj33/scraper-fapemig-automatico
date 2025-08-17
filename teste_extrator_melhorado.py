#!/usr/bin/env python3
"""
Teste do Extrator de PDFs Melhorado
====================================

Script para testar as melhorias no extrator de PDFs
"""

import os
import sys
from extrator_pdf import ExtratorPDF

def testar_extrator_melhorado():
    """Testa o extrator de PDFs melhorado"""
    print("🧪 TESTE DO EXTRATOR DE PDFs MELHORADO")
    print("=" * 50)
    
    # Criar instância do extrator
    extrator = ExtratorPDF()
    
    # URL de teste (substitua por uma URL real de PDF)
    url_teste = "https://www.ufmg.br/prograd/wp-content/uploads/2024/01/edital_exemplo.pdf"
    
    print(f"🔍 Testando extração de: {url_teste}")
    print("⚠️  Nota: Esta é uma URL de exemplo. Para teste real, use uma URL válida de PDF.")
    
    try:
        # Tentar extrair dados
        resultado = extrator.extrair_de_url(url_teste)
        
        if 'erro' not in resultado:
            print("\n✅ EXTRACTION BEM-SUCEDIDA!")
            print(f"📄 Páginas: {resultado.get('num_paginas', 'N/A')}")
            print(f"📊 Tamanho: {resultado.get('tamanho_bytes', 'N/A')} bytes")
            print(f"🔗 URL origem: {resultado.get('url_origem', 'N/A')}")
            print(f"💾 Arquivo local: {resultado.get('arquivo_local', 'N/A')}")
            
            # Estatísticas do texto
            if 'estatisticas' in resultado:
                stats = resultado['estatisticas']
                print(f"\n📊 ESTATÍSTICAS DO TEXTO:")
                print(f"   • Total de caracteres: {stats.get('total_caracteres', 'N/A')}")
                print(f"   • Total de palavras: {stats.get('total_palavras', 'N/A')}")
                print(f"   • Total de linhas: {stats.get('total_linhas', 'N/A')}")
                print(f"   • Caracteres limpos: {stats.get('caracteres_limpos', 'N/A')}")
            
            # Valores encontrados
            if 'valores_encontrados' in resultado and resultado['valores_encontrados']:
                print(f"\n💰 VALORES ENCONTRADOS:")
                for i, valor in enumerate(resultado['valores_encontrados'][:5], 1):
                    print(f"   {i}. {valor}")
            
            # Datas encontradas
            if 'datas_encontradas' in resultado and resultado['datas_encontradas']:
                print(f"\n📅 DATAS ENCONTRADAS:")
                for i, data in enumerate(resultado['datas_encontradas'][:5], 1):
                    print(f"   {i}. {data}")
            
            # Prazos encontrados
            if 'prazos_encontrados' in resultado and resultado['prazos_encontrados']:
                print(f"\n⏰ PRAZOS ENCONTRADOS:")
                for i, prazo in enumerate(resultado['prazos_encontrados'][:5], 1):
                    print(f"   {i}. {prazo}")
            
            # Objetivos encontrados
            if 'objetivos_encontrados' in resultado and resultado['objetivos_encontrados']:
                print(f"\n🎯 OBJETIVOS ENCONTRADOS:")
                for i, objetivo in enumerate(resultado['objetivos_encontrados'][:3], 1):
                    print(f"   {i}. {objetivo[:100]}...")
            
            # Áreas encontradas
            if 'areas_encontradas' in resultado and resultado['areas_encontradas']:
                print(f"\n🔬 ÁREAS ENCONTRADAS:")
                for i, area in enumerate(resultado['areas_encontradas'][:3], 1):
                    print(f"   {i}. {area[:100]}...")
            
            # Idioma detectado
            if 'idioma_detectado' in resultado:
                print(f"\n🌍 IDIOMA DETECTADO: {resultado['idioma_detectado']}")
            
            # Resumo do conteúdo
            if 'resumo_conteudo' in resultado:
                print(f"\n📖 RESUMO DO CONTEÚDO (primeiras linhas):")
                print(resultado['resumo_conteudo'][:300] + "..." if len(resultado['resumo_conteudo']) > 300 else resultado['resumo_conteudo'])
            
        else:
            print(f"\n❌ ERRO NA EXTRAÇÃO: {resultado['erro']}")
            
    except Exception as e:
        print(f"\n💥 EXCEÇÃO DURANTE O TESTE: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Limpar arquivos de teste
        print(f"\n🧹 Limpando arquivos de teste...")
        extrator.limpar_arquivos_locais()

def testar_padroes_regex():
    """Testa os padrões regex melhorados"""
    print("\n🔍 TESTE DOS PADRÕES REGEX MELHORADOS")
    print("=" * 50)
    
    # Texto de exemplo
    texto_exemplo = """
    Edital PROEX nº 08/2025 – Programa de Apoio Integrado a Eventos
    
    Objetivo: Apoiar eventos acadêmicos e científicos de excelência que contribuam para o desenvolvimento 
    das áreas do conhecimento e áreas temáticas da extensão, no período de 01/01/2025 a 31/12/2025.
    
    Valor: R$ 15.000,00 por evento
    Valor máximo: R$ 5.000,00 para eventos menores
    
    Prazo: Inscrições até 30/09/2025
    Data limite: 15/10/2025
    
    Área: Ciências Humanas, Ciências Sociais Aplicadas e Linguística
    Tema: Eventos acadêmicos e científicos
    
    Datas importantes:
    - 21 de setembro de 2025: Início das inscrições
    - 06 de novembro de 2025: Fim das inscrições
    - 04 de julho de 2024: Data de referência
    """
    
    print("📝 TEXTO DE EXEMPLO:")
    print(texto_exemplo)
    
    # Criar instância do extrator para testar os métodos
    extrator = ExtratorPDF()
    
    # Testar extração de valores
    valores = extrator._extrair_valores_melhorado(texto_exemplo)
    print(f"\n💰 VALORES EXTRAÍDOS: {valores}")
    
    # Testar extração de datas
    datas = extrator._extrair_datas_melhorado(texto_exemplo)
    print(f"📅 DATAS EXTRAÍDAS: {datas}")
    
    # Testar extração de prazos
    prazos = extrator._extrair_prazos_melhorado(texto_exemplo)
    print(f"⏰ PRAZOS EXTRAÍDOS: {prazos}")
    
    # Testar extração de objetivos
    objetivos = extrator._extrair_objetivos_melhorado(texto_exemplo)
    print(f"🎯 OBJETIVOS EXTRAÍDOS: {objetivos}")
    
    # Testar extração de áreas
    areas = extrator._extrair_areas_melhorado(texto_exemplo)
    print(f"🔬 ÁREAS EXTRAÍDAS: {areas}")
    
    # Testar detecção de idioma
    idioma = extrator._detectar_idioma(texto_exemplo)
    print(f"🌍 IDIOMA DETECTADO: {idioma}")
    
    # Testar limpeza de texto
    texto_limpo = extrator._limpar_texto(texto_exemplo)
    print(f"\n🧹 TEXTO LIMPO (primeiros 200 caracteres):")
    print(texto_limpo[:200] + "..." if len(texto_limpo) > 200 else texto_limpo)

def main():
    """Função principal"""
    print("🚀 INICIANDO TESTES DO EXTRATOR MELHORADO")
    print("=" * 60)
    
    # Teste 1: Padrões regex
    testar_padroes_regex()
    
    print("\n" + "=" * 60)
    
    # Teste 2: Extração completa (requer URL válida)
    testar_extrator_melhorado()
    
    print("\n✅ TESTES CONCLUÍDOS!")
    print("💡 Para testar com PDFs reais, atualize a URL no script.")

if __name__ == "__main__":
    main()
