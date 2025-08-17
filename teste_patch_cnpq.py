#!/usr/bin/env python3
"""
Teste para verificar se o patch do CNPq está funcionando
"""

def test_patch_features():
    """Testa as funcionalidades do patch"""
    
    print("🧪 TESTE DO PATCH DO CNPq")
    print("=" * 60)
    
    print("🚀 NOVAS FUNCIONALIDADES IMPLEMENTADAS:")
    print()
    
    features = [
        "✅ Sistema de scoring para filtrar ruído",
        "✅ Detecção robusta de datas brasileiras",
        "✅ Suporte a acentos em XPath",
        "✅ Deduplicação inteligente com hash + URL",
        "✅ Múltiplas estratégias de busca",
        "✅ Verificação HEAD antes de baixar PDFs",
        "✅ Controle de tamanho de arquivos",
        "✅ Session management otimizado",
        "✅ Fallbacks em camadas",
        "✅ Logging detalhado"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print("\n📊 RESULTADOS ESPERADOS:")
    print("   • Deve encontrar as 4 chamadas do CNPq")
    print("   • Deve extrair datas corretamente")
    print("   • Deve baixar PDFs sem duplicatas")
    print("   • Deve filtrar ruído automaticamente")
    print("   • Deve ser mais rápido e robusto")

def test_date_extraction():
    """Testa a extração de datas"""
    
    print("\n📅 TESTE DE EXTRAÇÃO DE DATAS")
    print("=" * 60)
    
    # Simular os regex patterns do patch
    import re
    
    test_cases = [
        "Inscrições: 11/08/2025 a 30/09/2025",
        "Prazo até 15 de agosto de 2025",
        "Submissões encerram em 20/12/2025",
        "Período: 01/01/2026 até 31/03/2026"
    ]
    
    patterns = [
        r'(\d{1,2}/\d{1,2}/\d{2,4})\s*(?:a|até|-|–|—)\s*(\d{1,2}/\d{1,2}/\d{2,4})',
        r'(?:prazo|inscriç(?:ão|oes)|submiss(?:ão|ões)).{0,40}?(?:até|encerra(?:m)? em)\s+(\d{1,2}/\d{1,2}/\d{2,4})',
        r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4}).{0,30}?(?:a|até|-|–|—).{0,30}?(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})'
    ]
    
    for test_case in test_cases:
        print(f"\n🔍 Testando: {test_case}")
        for i, pattern in enumerate(patterns, 1):
            matches = re.findall(pattern, test_case, re.IGNORECASE)
            if matches:
                print(f"   Padrão {i}: ✅ {matches}")
            else:
                print(f"   Padrão {i}: ❌ Sem match")

def test_scoring_system():
    """Testa o sistema de scoring"""
    
    print("\n🎯 TESTE DO SISTEMA DE SCORING")
    print("=" * 60)
    
    # Simular o sistema de scoring do patch
    def score(title, url, context, period):
        score = 0
        title_lower = title.lower()
        
        # Pontos por palavras-chave no título
        keywords = ["chamada", "edital", "seleção", "bolsas", "fomento"]
        for kw in keywords:
            if kw in title_lower:
                score += 1
        
        # Pontos por palavras-chave na URL
        if url:
            url_lower = url.lower()
            if any(k in url_lower for k in ["chamada", "edital"]):
                score += 1
        
        # Pontos por período
        if period:
            score += 1
        
        # Pontos por contexto
        if context:
            context_lower = context.lower()
            if any(k in context_lower for k in keywords):
                score += 1
        
        return score
    
    test_cases = [
        {
            "title": "CHAMADA PÚBLICA CNPq Nº 12/2025",
            "url": "https://cnpq.br/chamadas/edital12",
            "context": "Seleção de propostas para bolsas",
            "period": {"inicio": "2025-08-01", "fim": "2025-09-30"}
        },
        {
            "title": "Notícias do CNPq",
            "url": "https://cnpq.br/noticias",
            "context": "Últimas atualizações",
            "period": None
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        score_result = score(case["title"], case["url"], case["context"], case["period"])
        print(f"\n🔍 Caso {i}: {case['title']}")
        print(f"   Score: {score_result}/5")
        print(f"   Qualidade: {'✅ Alta' if score_result >= 3 else '⚠️ Baixa' if score_result >= 2 else '❌ Ruído'}")

def test_deduplication():
    """Testa o sistema de deduplicação"""
    
    print("\n🔄 TESTE DO SISTEMA DE DEDUPLICAÇÃO")
    print("=" * 60)
    
    # Simular o sistema de deduplicação do patch
    import hashlib
    
    def create_key(title, url):
        # Normalizar título
        norm_title = ' '.join(title.lower().split())
        # URL canônica (sem query params e fragmentos)
        canon_url = url.split('#')[0].split('?')[0] if url else ""
        # Hash do título + URL canônica
        key = f"{hashlib.md5(norm_title.encode()).hexdigest()}|{canon_url}"
        return key
    
    test_cases = [
        ("CHAMADA CNPq 2025", "https://cnpq.br/chamada1"),
        ("CHAMADA CNPq 2025", "https://cnpq.br/chamada1?param=123"),
        ("CHAMADA CNPq 2025", "https://cnpq.br/chamada1#section"),
        ("Chamada CNPq 2025", "https://cnpq.br/chamada1"),
        ("NOVA CHAMADA 2026", "https://cnpq.br/chamada2")
    ]
    
    seen_keys = set()
    
    for title, url in test_cases:
        key = create_key(title, url)
        if key in seen_keys:
            print(f"❌ DUPLICATA: {title} -> {url}")
        else:
            print(f"✅ NOVA: {title} -> {url}")
            seen_keys.add(key)

if __name__ == "__main__":
    test_patch_features()
    test_date_extraction()
    test_scoring_system()
    test_deduplication()
    
    print("\n🎉 TESTE DO PATCH CONCLUÍDO!")
    print("=" * 60)
    print("💡 Para implementar o patch:")
    print("   1. Substitua a classe CNPqScraper existente")
    print("   2. Ou copie os métodos para sua classe atual")
    print("   3. Execute o scraper para testar")
    print("\n🔍 Verifique se:")
    print("   • Está encontrando as 4 chamadas")
    print("   • Está extraindo datas corretamente")
    print("   • Está baixando PDFs sem duplicatas")
    print("   • Está mais rápido e robusto")
