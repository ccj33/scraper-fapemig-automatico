#!/usr/bin/env python3
"""
Teste Simples de Extração de PDFs
=================================

Demonstra como usar o sistema de extração de PDFs
"""

from extrator_pdf import ExtratorPDF
import json

def teste_extracao_basica():
    """Teste básico de extração de PDFs"""
    print("🧪 TESTE BÁSICO DE EXTRAÇÃO DE PDFs")
    print("=" * 50)
    
    extrator = ExtratorPDF()
    
    # URLs de exemplo (substitua por URLs reais)
    urls_teste = [
        "https://www.ufmg.br/prograd/wp-content/uploads/2024/01/edital_exemplo.pdf",
        "https://www.fapemig.br/wp-content/uploads/2024/01/chamada_exemplo.pdf"
    ]
    
    print(f"🔍 Testando {len(urls_teste)} URLs...")
    
    for i, url in enumerate(urls_teste, 1):
        print(f"\n📄 Teste {i}: {url}")
        
        try:
            resultado = extrator.extrair_de_url(url)
            
            if 'erro' not in resultado:
                print(f"   ✅ Sucesso!")
                print(f"   📊 Páginas: {resultado.get('num_paginas', 'N/A')}")
                print(f"   💾 Tamanho: {resultado.get('tamanho_bytes', 'N/A'):,} bytes")
                print(f"   💰 Valor encontrado: {resultado.get('valor', 'N/A')}")
                print(f"   ⏰ Prazo encontrado: {resultado.get('prazo', 'N/A')}")
                print(f"   🎯 Objetivo: {resultado.get('objetivo', 'N/A')[:50]}...")
                print(f"   🌍 Idioma: {resultado.get('idioma_detectado', 'N/A')}")
                
                if resultado.get('estatisticas'):
                    stats = resultado['estatisticas']
                    print(f"   📈 Estatísticas: {stats.get('total_caracteres', 0):,} chars, {stats.get('total_palavras', 0)} palavras")
            else:
                print(f"   ❌ Erro: {resultado['erro']}")
                
        except Exception as e:
            print(f"   💥 Exceção: {e}")
    
    # Limpar arquivos de teste
    extrator.limpar_arquivos_locais()
    print(f"\n🗑️ Arquivos temporários limpos")

def teste_analise_conteudo():
    """Teste de análise de conteúdo"""
    print("\n🔍 TESTE DE ANÁLISE DE CONTEÚDO")
    print("=" * 50)
    
    # Texto de exemplo (simula conteúdo extraído de PDF)
    texto_exemplo = """
    EDITAL PROEX Nº 08/2025
    
    OBJETIVO: Apoiar eventos acadêmicos e científicos da UFMG
    
    VALOR: R$ 5.000,00 por projeto
    
    PRAZO: Inscrições até 30/09/2025
    
    ÁREA TEMÁTICA: Ciências Humanas e Sociais
    
    Este edital visa fomentar a realização de eventos que contribuam
    para o desenvolvimento acadêmico e científico da instituição.
    """
    
    extrator = ExtratorPDF()
    analise = extrator._analisar_conteudo(texto_exemplo)
    
    print("📝 Texto analisado:")
    print(f"   {texto_exemplo[:100]}...")
    
    print("\n🔍 Resultados da análise:")
    for campo, valor in analise.items():
        if campo != 'estatisticas':
            print(f"   • {campo}: {valor}")
    
    if 'estatisticas' in analise:
        stats = analise['estatisticas']
        print(f"   • Estatísticas: {stats['total_caracteres']} chars, {stats['total_palavras']} palavras")

def teste_deteccao_pdf():
    """Teste de detecção de URLs de PDF"""
    print("\n🔍 TESTE DE DETECÇÃO DE PDFs")
    print("=" * 50)
    
    extrator = ExtratorPDF()
    
    urls_teste = [
        "https://exemplo.com/edital.pdf",
        "https://exemplo.com/documento.PDF",
        "https://exemplo.com/arquivo?tipo=pdf",
        "https://exemplo.com/edital.doc",
        "https://exemplo.com/pagina.html",
        "https://exemplo.com/",
        ""
    ]
    
    for url in urls_teste:
        eh_pdf = extrator._eh_pdf(url)
        status = "✅ É PDF" if eh_pdf else "❌ Não é PDF"
        print(f"   {url or '(vazio)':<40} → {status}")

def main():
    """Função principal"""
    print("🚀 SISTEMA DE EXTRAÇÃO DE PDFs - TESTES")
    print("=" * 60)
    
    try:
        # Teste 1: Detecção de PDFs
        teste_deteccao_pdf()
        
        # Teste 2: Análise de conteúdo
        teste_analise_conteudo()
        
        # Teste 3: Extração básica (com URLs reais)
        print("\n" + "=" * 60)
        print("⚠️  ATENÇÃO: Para testar extração real, edite as URLs no código!")
        print("   URLs atuais são apenas exemplos e não existem.")
        
        # teste_extracao_basica()  # Descomente para testar com URLs reais
        
        print("\n✅ Todos os testes concluídos!")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        print("💡 Verifique se todas as dependências estão instaladas:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
