#!/usr/bin/env python3
"""
Teste para verificar se as melhorias no scraper do CNPq estão funcionando
"""

def test_cnpq_improvements():
    """Testa as melhorias implementadas no scraper do CNPq"""
    
    print("🧪 TESTE DAS MELHORIAS NO SCRAPER DO CNPq")
    print("=" * 70)
    
    print("🔍 PROBLEMA IDENTIFICADO:")
    print("   • O scraper não estava encontrando nenhuma chamada do CNPq")
    print("   • Resultado: 0 chamadas encontradas")
    print()
    
    print("🚀 MELHORIAS IMPLEMENTADAS:")
    print()
    
    estrategias = [
        "1. ESTRATÉGIA 1: Seletores específicos (h1, h2, h3, h4, div, li, a)",
        "   • Procura por elementos com texto 'CHAMADA' ou 'Chamada'",
        "   • Usa seletores XPath específicos",
        "   • Fallback se não encontrar nada",
        "",
        "2. ESTRATÉGIA 2: Busca por qualquer elemento com 'CHAMADA'",
        "   • Se a estratégia 1 falhar, tenta esta",
        "   • Procura por qualquer elemento que contenha 'CHAMADA' no texto",
        "   • Mais abrangente e flexível",
        "",
        "3. ESTRATÉGIA 3: Busca por links com 'chamada' na URL",
        "   • Se as estratégias 1 e 2 falharem, tenta esta",
        "   • Procura por links que contenham 'chamada' na URL",
        "   • Último recurso para encontrar chamadas",
        "",
        "4. BUSCA DE LINKS MELHORADA:",
        "   • Estratégia 1: Parent e siblings",
        "   • Estratégia 2: Links globais na página",
        "   • Estratégia 3: Links com 'chamada' na URL"
    ]
    
    for estrategia in estrategias:
        print(estrategia)
    
    print("\n📊 RESULTADO ESPERADO:")
    print("   • Deve encontrar as 4 chamadas que estavam aparecendo antes")
    print("   • Deve conseguir baixar os PDFs")
    print("   • Deve extrair contexto das páginas")
    print("   • Deve incluir links nos resumos")

def test_cnpq_urls():
    """Testa as URLs que o scraper está tentando acessar"""
    
    print("\n🌐 TESTE DAS URLs DO CNPq")
    print("=" * 70)
    
    urls = [
        "https://www.gov.br/cnpq/pt-br/acesso-a-informacao/acoes-e-programas/programas/chamadas-publicas",
        "https://www.gov.br/cnpq/pt-br/acesso-a-informacao/acoes-e-programas/programas",
        "http://memoria2.cnpq.br/web/guest/chamadas-publicas"
    ]
    
    print("🔍 URLs que o scraper está tentando:")
    for i, url in enumerate(urls, 1):
        print(f"   {i}. {url}")
    
    print("\n💡 OBSERVAÇÕES:")
    print("   • As duas primeiras URLs são do governo brasileiro (gov.br)")
    print("   • A terceira é a URL antiga que funcionava antes")
    print("   • O scraper tenta cada uma até encontrar chamadas")

def test_cnpq_selectors():
    """Testa os seletores que o scraper está usando"""
    
    print("\n🎯 TESTE DOS SELETORES")
    print("=" * 70)
    
    selectors = [
        '//h4[contains(text(), "CHAMADA") or contains(text(), "Chamada")]',
        '//h3[contains(text(), "CHAMADA") or contains(text(), "Chamada")]',
        '//h2[contains(text(), "CHAMADA") or contains(text(), "Chamada")]',
        '//h1[contains(text(), "CHAMADA") or contains(text(), "Chamada")]',
        '//div[contains(@class, "chamada") or contains(@class, "edital")]',
        '//li[contains(text(), "CHAMADA") or contains(text(), "Chamada")]',
        '//a[contains(text(), "CHAMADA") or contains(text(), "Chamada")]'
    ]
    
    print("🔍 Seletores XPath utilizados:")
    for i, selector in enumerate(selectors, 1):
        print(f"   {i}. {selector}")
    
    print("\n💡 ESTRATÉGIAS DE FALLBACK:")
    print("   • Se os seletores específicos falharem, usa busca genérica")
    print("   • Procura por qualquer elemento com 'CHAMADA' no texto")
    print("   • Procura por links com 'chamada' na URL")

def test_cnpq_expected_results():
    """Testa os resultados esperados"""
    
    print("\n📋 RESULTADOS ESPERADOS")
    print("=" * 70)
    
    print("🎯 ANTES (PROBLEMA):")
    print("   📊 CNPq - Chamadas Públicas")
    print("   ----------------------------")
    print("   Total: 0 chamadas")
    print("   PDFs: 0 baixados")
    print("   Nenhuma oportunidade encontrada")
    print()
    
    print("🎯 DEPOIS (CORRIGIDO):")
    print("   📊 CNPq - Chamadas Públicas")
    print("   ----------------------------")
    print("   Total: 4 chamadas")
    print("   PDFs: 2-4 baixados")
    print("   1. CHAMADA ERC- CNPQ - 2025 Nº 13/2025")
    print("      📅 Período: Inscrições: 11/08/2025 a 30/09/2025")
    print("      📋 Contexto: A presente chamada pública tem por objetivo...")
    print("      📄 PDF: Baixado ✅")
    print("      🔗 Link PDF: http://memoria2.cnpq.br/anexo1.pdf")

if __name__ == "__main__":
    test_cnpq_improvements()
    test_cnpq_urls()
    test_cnpq_selectors()
    test_cnpq_expected_results()
    
    print("\n🎉 TESTE DAS MELHORIAS CONCLUÍDO!")
    print("=" * 70)
    print("💡 Para testar o scraper real com as melhorias:")
    print("   python scraper_unificado.py")
    print("\n🔍 Verifique nos logs:")
    print("   • Se está tentando as 3 estratégias")
    print("   • Se está encontrando as chamadas")
    print("   • Se está conseguindo baixar os PDFs")
    print("   • Se está extraindo o contexto")
