import json
import re
from pathlib import Path

def extrair_periodo_do_texto(texto):
    """Tenta extrair período de inscrição/prazo do texto usando regex"""
    if not texto:
        return ""
    
    # Padrões para datas brasileiras
    padroes = [
        r'(\d{1,2}/\d{1,2}/\d{2,4})\s*(?:a|até|-)\s*(\d{1,2}/\d{1,2}/\d{2,4})',  # 01/08/2025 a 30/09/2025
        r'(\d{1,2}/\d{1,2}/\d{2,4})',  # Data única
        r'prazo.*?(\d{1,2}/\d{1,2}/\d{2,4})',  # "prazo até 30/09/2025"
        r'inscrições.*?(\d{1,2}/\d{1,2}/\d{2,4})',  # "inscrições até 30/09/2025"
    ]
    
    for padrao in padroes:
        match = re.search(padrao, texto, re.I)
        if match:
            if len(match.groups()) == 2:
                return f"{match.group(1)} a {match.group(2)}"
            else:
                return match.group(1)
    
    return ""

def formatar_chamada_fapemig(chamada):
    """Formata uma chamada do FAPEMIG"""
    nome = chamada.get('titulo', 'Sem título')
    periodo = chamada.get('data_limite', '')
    link = chamada.get('link_pdf', '')
    
    # Se não tem período, tenta extrair do título
    if not periodo:
        periodo = extrair_periodo_do_texto(nome)
    
    return {
        'nome': nome,
        'periodo': periodo,
        'link': link,
        'fonte': 'FAPEMIG'
    }

def main():
    """Mostra apenas as chamadas do FAPEMIG"""
    print("🔍 CHAMADAS FAPEMIG")
    print("=" * 60)
    
    # Procura por arquivos com dados do FAPEMIG
    arquivos_fapemig = [
        'fapemig_completo_20250817_202009.json',
        'fapemig_dados_reais_20250817_203807.json',
        'fapemig_ultra_melhorado_20250817_202737.json',
        'dados_reorganizados_com_pdfs_20250817_201259.json'
    ]
    
    todas_chamadas_fapemig = []
    
    for arquivo in arquivos_fapemig:
        if Path(arquivo).exists():
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                if 'fapemig' in dados and dados['fapemig']:
                    for chamada in dados['fapemig']:
                        todas_chamadas_fapemig.append(formatar_chamada_fapemig(chamada))
                    print(f"✅ {arquivo}: {len(dados['fapemig'])} chamadas")
                else:
                    print(f"❌ {arquivo}: Sem dados FAPEMIG")
                    
            except Exception as e:
                print(f"❌ Erro ao ler {arquivo}: {e}")
        else:
            print(f"⚠️  {arquivo}: Arquivo não encontrado")
    
    print("\n" + "=" * 60)
    print("🎯 CHAMADAS FAPEMIG FORMATADAS:")
    print("=" * 60)
    
    # Remove duplicatas
    chamadas_unicas = []
    nomes_vistos = set()
    
    for chamada in todas_chamadas_fapemig:
        nome_limpo = re.sub(r'\s+', ' ', chamada['nome'].strip())
        if nome_limpo not in nomes_vistos:
            nomes_vistos.add(nome_limpo)
            chamadas_unicas.append(chamada)
    
    if not chamadas_unicas:
        print("❌ Nenhuma chamada FAPEMIG encontrada!")
        return
    
    print(f"📊 Total: {len(chamadas_unicas)} chamadas únicas\n")
    
    for i, chamada in enumerate(chamadas_unicas, 1):
        print(f"{i}. {chamada['nome']}")
        
        if chamada['periodo']:
            print(f"   📅 {chamada['periodo']}")
        else:
            print(f"   📅 Período não especificado")
        
        if chamada['link']:
            print(f"   🔗 {chamada['link']}")
        else:
            print(f"   🔗 Link não disponível")
        
        print()

if __name__ == "__main__":
    main()
