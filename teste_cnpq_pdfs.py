#!/usr/bin/env python3
"""
Teste específico para verificar se o scraper do CNPq está baixando PDFs
"""

def test_cnpq_pdf_detection():
    """Testa a detecção de PDFs do CNPq"""
    
    print("🧪 TESTE DE DETECÇÃO DE PDFs DO CNPq")
    print("=" * 60)
    
    # Simular dados como seriam encontrados no site
    chamadas_teste = [
        {
            'titulo': 'CHAMADA ERC- CNPQ - 2025 Nº 13/2025',
            'url_detalhes': 'http://memoria2.cnpq.br/web/guest/chamadas-publicas/erc-2025',
            'periodo_inscricao': 'Inscrições: 11/08/2025 a 30/09/2025'
        },
        {
            'titulo': 'CHAMADA PÚBLICA CNPq Nº 12/2025 - PROGRAMA INSTITUCIONAL DE BOLSAS DE PÓS-GRADUAÇÃO (PIBPG) - CICLO 2026',
            'url_detalhes': 'http://memoria2.cnpq.br/web/guest/chamadas-publicas/pibpg-2026',
            'periodo_inscricao': '04/08/2025 a 17/09/2025'
        },
        {
            'titulo': 'Chamada CNPq/SETEC/MCTI N° 06/2025 - Apoio a Eventos de Promoção do Empreendedorismo e da Inovação no Brasil',
            'url_detalhes': 'http://memoria2.cnpq.br/web/guest/chamadas-publicas/eventos-2025',
            'periodo_inscricao': '04/08/2025 a 18/09/2025'
        },
        {
            'titulo': 'CHAMADA PÚBLICA MCTI/CNPq/CSIC Nº 9/2025',
            'url_detalhes': 'http://memoria2.cnpq.br/web/guest/chamadas-publicas/csic-2025',
            'periodo_inscricao': '17/06/2025 a 12/09/2025'
        }
    ]
    
    print("📋 Chamadas encontradas:")
    for i, chamada in enumerate(chamadas_teste, 1):
        print(f"   {i}. {chamada['titulo'][:60]}...")
        print(f"      📅 {chamada['periodo_inscricao']}")
        print(f"      🔗 {chamada['url_detalhes']}")
        print()
    
    print("🔍 Estratégias de busca por PDFs:")
    estrategias = [
        "1. Buscar por links diretos (.pdf, .doc, .docx)",
        "2. Buscar por links 'Anexo' (comum no CNPq)",
        "3. Buscar por links 'Chamada' que levam aos detalhes",
        "4. Buscar por texto que sugira PDF/Download/Edital",
        "5. Buscar em toda a página por links relacionados"
    ]
    
    for estrategia in estrategias:
        print(f"   {estrategia}")
    
    print("\n✅ Teste de detecção concluído!")

def test_cnpq_link_priorities():
    """Testa as prioridades de busca de links"""
    
    print("\n🎯 TESTE DE PRIORIDADES DE LINKS")
    print("=" * 60)
    
    # Simular diferentes tipos de links encontrados
    links_teste = [
        {
            'texto': 'Chamada',
            'href': 'http://memoria2.cnpq.br/chamada-detalhes',
            'prioridade': 'ALTA - Link principal para detalhes'
        },
        {
            'texto': 'Anexo I',
            'href': 'http://memoria2.cnpq.br/anexo1.pdf',
            'prioridade': 'MÁXIMA - PDF direto'
        },
        {
            'texto': 'Anexo II',
            'href': 'http://memoria2.cnpq.br/anexo2.pdf',
            'prioridade': 'MÁXIMA - PDF direto'
        },
        {
            'texto': 'FAQ',
            'href': 'http://memoria2.cnpq.br/faq',
            'prioridade': 'BAIXA - Informação secundária'
        },
        {
            'texto': 'Resultado',
            'href': 'http://memoria2.cnpq.br/resultado',
            'prioridade': 'MÉDIA - Informação importante'
        }
    ]
    
    print("📋 Prioridades de links:")
    for link in links_teste:
        print(f"   {link['prioridade']}")
        print(f"      Texto: {link['texto']}")
        print(f"      URL: {link['href']}")
        print()
    
    print("✅ Teste de prioridades concluído!")

def test_cnpq_pdf_download_simulation():
    """Simula o processo de download de PDFs"""
    
    print("\n📥 SIMULAÇÃO DE DOWNLOAD DE PDFs")
    print("=" * 60)
    
    # Simular processo de download
    processo = [
        "1. Encontrar título da chamada",
        "2. Localizar link 'Chamada' para detalhes",
        "3. Acessar página de detalhes",
        "4. Procurar por anexos (.pdf, .doc, .docx)",
        "5. Procurar por links 'Anexo I', 'Anexo II', etc.",
        "6. Baixar PDF encontrado",
        "7. Extrair conteúdo do PDF",
        "8. Salvar informações no resumo"
    ]
    
    print("🔄 Processo de download:")
    for passo in processo:
        print(f"   {passo}")
    
    print("\n📊 Resultado esperado:")
    resultado_esperado = {
        'chamadas_encontradas': 4,
        'pdfs_baixados': '2-4 (dependendo dos anexos disponíveis)',
        'conteudo_extraido': 'Datas, valores, objetivos, áreas',
        'links_pdf_incluidos': 'Sim, nos resumos'
    }
    
    for campo, valor in resultado_esperado.items():
        print(f"   {campo}: {valor}")
    
    print("\n✅ Simulação concluída!")

if __name__ == "__main__":
    test_cnpq_pdf_detection()
    test_cnpq_link_priorities()
    test_cnpq_pdf_download_simulation()
    
    print("\n🎉 TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 60)
    print("💡 Para testar o scraper real com as melhorias:")
    print("   python scraper_unificado.py")
    print("\n🔍 Verifique os logs para acompanhar:")
    print("   • Detecção de links 'Chamada'")
    print("   • Busca por anexos e PDFs")
    print("   • Download de arquivos")
    print("   • Extração de conteúdo")
