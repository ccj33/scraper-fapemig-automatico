#!/usr/bin/env python3
"""
Teste para verificar se a extração de contexto das páginas web está funcionando
"""

def test_context_extraction():
    """Testa a extração de contexto das páginas web"""
    
    print("🧪 TESTE DE EXTRAÇÃO DE CONTEXTO DAS PÁGINAS WEB")
    print("=" * 70)
    
    # Simular dados como seriam retornados pelo scraper melhorado
    dados_teste = {
        'ufmg': [
            {
                'titulo': 'Edital PROEX nº 08/2025 – Programa de Apoio Integrado a Eventos – PAIE',
                'url': 'https://ufmg.br/edital1',
                'data': '06/08/2025',
                'fonte': 'UFMG',
                'contexto': 'Este edital tem por objetivo apoiar financeiramente eventos científicos, tecnológicos e culturais promovidos pela comunidade acadêmica da UFMG. As propostas devem contemplar atividades que contribuam para o desenvolvimento científico e tecnológico da instituição e da sociedade.',
                'pdf_baixado': 'pdfs_baixados/edital1.pdf',
                'pdf_url': 'https://ufmg.br/edital1.pdf'
            }
        ],
        'fapemig': [
            {
                'titulo': 'Chamada Pública FAPEMIG 2025 - Apoio a Projetos de Pesquisa',
                'url': 'https://fapemig.br/chamada1',
                'fonte': 'FAPEMIG',
                'contexto': 'A presente chamada pública tem por objetivo selecionar propostas para apoio financeiro a projetos de pesquisa que visem contribuir significativamente para o desenvolvimento científico e tecnológico de Minas Gerais.',
                'pdf_baixado': 'pdfs_baixados/chamada1.pdf',
                'pdf_url': 'https://fapemig.br/chamada1.pdf'
            }
        ],
        'cnpq': [
            {
                'titulo': 'CHAMADA ERC- CNPQ - 2025 Nº 13/2025',
                'url_detalhes': 'http://memoria2.cnpq.br/chamada1',
                'periodo_inscricao': 'Inscrições: 11/08/2025 a 30/09/2025',
                'fonte': 'CNPq',
                'contexto': 'A presente chamada pública tem por objetivo selecionar propostas para apoio financeiro a projetos que visem contribuir significativamente para o desenvolvimento científico e tecnológico do país. As propostas devem observar as condições específicas estabelecidas na parte II - Regulamento.',
                'pdf_baixado': 'pdfs_baixados/chamada_cnpq1.pdf',
                'pdf_url': 'http://memoria2.cnpq.br/anexo1.pdf'
            }
        ]
    }
    
    print("📋 Dados de teste com contexto extraído:")
    print()
    
    for fonte, editais in dados_teste.items():
        print(f"🔍 {fonte.upper()}:")
        for i, edital in enumerate(editais, 1):
            print(f"   {i}. {edital['titulo'][:60]}...")
            if edital.get('contexto'):
                contexto = edital['contexto']
                if len(contexto) > 80:
                    print(f"      📋 Contexto: {contexto[:80]}...")
                else:
                    print(f"      📋 Contexto: {contexto}")
            print()
    
    print("✅ Teste de estrutura de dados concluído!")

def test_context_formatting():
    """Testa a formatação do contexto no resumo"""
    
    print("\n📝 TESTE DE FORMATAÇÃO DO CONTEXTO NO RESUMO")
    print("=" * 70)
    
    # Simular função de formatação
    def format_editais_with_context(editais):
        if not editais:
            return "Nenhuma oportunidade encontrada"
            
        formatted = ""
        for i, edital in enumerate(editais, 1):
            titulo = edital.get('titulo', 'Sem título')
            formatted += f"{i}. {titulo[:60]}...\n"
            
            # Contexto extraído da página web (prioridade alta)
            if edital.get('contexto'):
                contexto = edital['contexto']
                if len(contexto) > 120:
                    formatted += f"   📋 Contexto: {contexto[:120]}... (📄 Texto completo disponível)\n"
                else:
                    formatted += f"   📋 Contexto: {contexto}\n"
            
            # Outras informações
            if edital.get('data'):
                formatted += f"   📅 Data: {edital['data']}\n"
            if edital.get('periodo_inscricao'):
                formatted += f"   📅 Período: {edital['periodo_inscricao']}\n"
            if edital.get('pdf_url'):
                formatted += f"   🔗 Link PDF: {edital['pdf_url']}\n"
            formatted += "\n"
            
        return formatted
    
    # Dados de teste
    editais_teste = [
        {
            'titulo': 'CHAMADA ERC- CNPQ - 2025 Nº 13/2025',
            'contexto': 'A presente chamada pública tem por objetivo selecionar propostas para apoio financeiro a projetos que visem contribuir significativamente para o desenvolvimento científico e tecnológico do país. As propostas devem observar as condições específicas estabelecidas na parte II - Regulamento, anexo a esta chamada pública, que determina os requisitos relativos ao proponente, cronograma, recursos financeiros a serem aplicados nas propostas aprovadas, origem dos recursos, itens financiáveis, prazo para execução dos projetos, critérios de elegibilidade, critérios e parâmetros objetivos de julgamento e demais informações necessárias.',
            'periodo_inscricao': 'Inscrições: 11/08/2025 a 30/09/2025',
            'pdf_url': 'http://memoria2.cnpq.br/anexo1.pdf'
        }
    ]
    
    print("📋 Resumo formatado com contexto:")
    print("-" * 40)
    resultado = format_editais_with_context(editais_teste)
    print(resultado)
    
    print("✅ Teste de formatação concluído!")

def test_context_priorities():
    """Testa as prioridades de extração de contexto"""
    
    print("\n🎯 TESTE DE PRIORIDADES DE EXTRAÇÃO DE CONTEXTO")
    print("=" * 70)
    
    estrategias = [
        "1. 📋 Contexto da página web (PRIORIDADE MÁXIMA)",
        "   • Extraído diretamente do site",
        "   • Incluído no resumo antes das informações do PDF",
        "   • Limite de 120 caracteres no resumo",
        "",
        "2. 📖 Conteúdo do PDF (PRIORIDADE ALTA)",
        "   • Datas, valores, objetivos extraídos",
        "   • Complementa o contexto da página",
        "   • Incluído após o contexto",
        "",
        "3. 🔗 Links e URLs (PRIORIDADE MÉDIA)",
        "   • Links para PDFs e páginas de detalhes",
        "   • Incluídos no final de cada item"
    ]
    
    for estrategia in estrategias:
        print(estrategia)
    
    print("\n✅ Teste de prioridades concluído!")

if __name__ == "__main__":
    test_context_extraction()
    test_context_formatting()
    test_context_priorities()
    
    print("\n🎉 TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 70)
    print("💡 Para testar o scraper real com extração de contexto:")
    print("   python scraper_unificado.py")
    print("\n🔍 Verifique se o contexto está sendo extraído:")
    print("   • Procure por '📋 Contexto:' nos resumos")
    print("   • Verifique se o texto é relevante e descritivo")
    print("   • Confirme se está sendo truncado corretamente (>120 chars)")
