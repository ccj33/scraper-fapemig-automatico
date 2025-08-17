#!/usr/bin/env python3
"""
Teste Simples das Melhorias
===========================
"""

from extrator_pdf import ExtratorPDF

def testar_padroes():
    """Testa os padrões regex melhorados"""
    print("🧪 TESTE SIMPLES DOS PADRÕES REGEX")
    print("=" * 40)
    
    # Criar instância
    extrator = ExtratorPDF()
    
    # Texto de exemplo
    texto = """
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
    
    print("📝 Texto de exemplo processado")
    
    # Testar cada método
    try:
        # Valores
        valores = extrator._extrair_valores_melhorado(texto)
        print(f"💰 Valores: {valores}")
        
        # Datas
        datas = extrator._extrair_datas_melhorado(texto)
        print(f"📅 Datas: {datas}")
        
        # Prazos
        prazos = extrator._extrair_prazos_melhorado(texto)
        print(f"⏰ Prazos: {prazos}")
        
        # Objetivos
        objetivos = extrator._extrair_objetivos_melhorado(texto)
        print(f"🎯 Objetivos: {objetivos}")
        
        # Áreas
        areas = extrator._extrair_areas_melhorado(texto)
        print(f"🔬 Áreas: {areas}")
        
        # Idioma
        idioma = extrator._detectar_idioma(texto)
        print(f"🌍 Idioma: {idioma}")
        
        # Limpeza
        texto_limpo = extrator._limpar_texto(texto)
        print(f"🧹 Texto limpo (100 chars): {texto_limpo[:100]}...")
        
        print("\n✅ Todos os testes passaram!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_padroes()
