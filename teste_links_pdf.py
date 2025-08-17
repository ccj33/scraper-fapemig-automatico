#!/usr/bin/env python3
"""
Teste para verificar se os links dos PDFs estão sendo incluídos corretamente
"""

def test_pdf_url_structure():
    """Testa a estrutura dos dados com URLs de PDF"""
    
    # Simular dados como seriam retornados pelo scraper modificado
    dados_teste = {
        'ufmg': [
            {
                'titulo': 'Edital PROEX nº 08/2025 – Programa de Apoio Integrado a Eventos – PAIE',
                'url': 'https://ufmg.br/edital1',
                'data': '06/08/2025',
                'fonte': 'UFMG',
                'pdf_baixado': 'pdfs_baixados/edital1.pdf',
                'pdf_url': 'https://ufmg.br/edital1.pdf',
                'pdf_info': {
                    'datas_encontradas': ['12 de setembro de 2025', '20 de agosto de 2025'],
                    'valores_encontrados': ['15.000,00', '5.000,00']
                }
            }
        ],
        'fapemig': [
            {
                'titulo': 'Chamada FAPEMIG 2025',
                'url': 'https://fapemig.br/chamada1',
                'fonte': 'FAPEMIG',
                'pdf_baixado': 'pdfs_baixados/chamada1.pdf',
                'pdf_url': 'https://fapemig.br/chamada1.pdf',
                'pdf_info': {
                    'valores_encontrados': ['50.000,00']
                }
            }
        ],
        'cnpq': [
            {
                'titulo': 'Chamada CNPq 2025',
                'url_detalhes': 'https://cnpq.br/chamada1',
                'fonte': 'CNPq',
                'pdf_baixado': 'pdfs_baixados/cnpq1.pdf',
                'pdf_url': 'https://cnpq.br/chamada1.pdf',
                'pdf_info': {
                    'objetivo': 'Fomentar pesquisas inovadoras'
                }
            }
        ],
        'total_editais': 3
    }
    
    print("🧪 TESTE DE ESTRUTURA DE DADOS COM LINKS DE PDF")
    print("=" * 60)
    
    # Verificar UFMG
    print("\n📚 UFMG:")
    for edital in dados_teste['ufmg']:
        print(f"   Título: {edital['titulo']}")
        print(f"   URL: {edital['url']}")
        print(f"   PDF Baixado: {edital['pdf_baixado']}")
        print(f"   PDF URL: {edital['pdf_url']}")
        print(f"   PDF Info: {edital['pdf_info']}")
        print()
    
    # Verificar FAPEMIG
    print("🔬 FAPEMIG:")
    for oportunidade in dados_teste['fapemig']:
        print(f"   Título: {oportunidade['titulo']}")
        print(f"   URL: {oportunidade['url']}")
        print(f"   PDF Baixado: {oportunidade['pdf_baixado']}")
        print(f"   PDF URL: {oportunidade['pdf_url']}")
        print(f"   PDF Info: {oportunidade['pdf_info']}")
        print()
    
    # Verificar CNPq
    print("📖 CNPq:")
    for chamada in dados_teste['cnpq']:
        print(f"   Título: {chamada['titulo']}")
        print(f"   URL Detalhes: {chamada['url_detalhes']}")
        print(f"   PDF Baixado: {chamada['pdf_baixado']}")
        print(f"   PDF URL: {chamada['pdf_url']}")
        print(f"   PDF Info: {chamada['pdf_info']}")
        print()
    
    print("✅ Teste concluído! Verifique se todos os campos pdf_url estão presentes.")

def test_pdf_url_formatting():
    """Testa a formatação dos links de PDF no resumo"""
    
    print("\n📝 TESTE DE FORMATAÇÃO DOS LINKS DE PDF")
    print("=" * 60)
    
    # Simular formatação como seria feita pelo scraper
    def format_edital_with_pdf_link(edital):
        formatted = f"🔸 {edital['titulo']}\n"
        formatted += f"   📅 Data: {edital.get('data', 'N/A')}\n"
        
        if edital.get('pdf_baixado'):
            formatted += f"   📄 PDF: Baixado ✅\n"
            # Adicionar link do PDF se disponível
            if edital.get('pdf_url'):
                formatted += f"   🔗 Link PDF: {edital['pdf_url']}\n"
            elif edital.get('url') and edital['url'].lower().endswith('.pdf'):
                formatted += f"   🔗 Link PDF: {edital['url']}\n"
        elif edital.get('url') and edital['url'].lower().endswith('.pdf'):
            formatted += f"   📄 PDF: Disponível (não baixado)\n"
            formatted += f"   🔗 Link PDF: {edital['url']}\n"
        
        formatted += "\n"
        return formatted
    
    # Testar formatação
    edital_teste = {
        'titulo': 'Edital PROEX nº 08/2025 – Programa de Apoio Integrado a Eventos – PAIE',
        'url': 'https://ufmg.br/edital1',
        'data': '06/08/2025',
        'pdf_baixado': 'pdfs_baixados/edital1.pdf',
        'pdf_url': 'https://ufmg.br/edital1.pdf'
    }
    
    resultado_formatado = format_edital_with_pdf_link(edital_teste)
    print("Formatação do edital:")
    print(resultado_formatado)
    
    print("✅ Teste de formatação concluído!")

if __name__ == "__main__":
    test_pdf_url_structure()
    test_pdf_url_formatting()
