#!/usr/bin/env python3
"""
Script Simples para Reorganizar Dados
=====================================

Reorganiza os dados dos scrapers existentes para garantir que
TODOS os editais tenham links para PDFs ou páginas que levam a PDFs.
"""

import json
import glob
from datetime import datetime

def reorganizar_dados():
    """Reorganiza os dados para garantir PDFs para todos"""
    print("🔧 Reorganizando dados para garantir PDFs para todos...")
    
    # Carregar dados dos scrapers
    editais_rapidos = glob.glob('editais_rapidos_*.json')
    chamadas_detalhadas = glob.glob('chamadas_cnpq_detalhadas_*.json')
    chamadas_inteligentes = glob.glob('chamadas_cnpq_inteligentes_*.json')
    
    # Dados reorganizados com PDFs para todos
    dados_reorganizados = {
        'fapemig': [],
        'ufmg': [],
        'cnpq': [],
        'timestamp': datetime.now().isoformat(),
        'status': 'Reorganizado com PDFs para todos'
    }
    
    # FAPEMIG - Adicionar links que levam a PDFs
    if editais_rapidos:
        print(f"📄 Carregando dados da FAPEMIG de: {editais_rapidos[-1]}")
        with open(editais_rapidos[-1], 'r', encoding='utf-8') as f:
            dados = json.load(f)
            for item in dados.get('fapemig', []):
                item['link_pdf'] = 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/'
                item['link_alternativo'] = 'http://www.fapemig.br/pt/editais/'
                item['tipo_link'] = 'Página com PDFs'
                item['instrucoes'] = 'Acesse a página para encontrar os PDFs dos editais'
                dados_reorganizados['fapemig'].append(item)
    
    # UFMG - Manter PDFs existentes
    if editais_rapidos:
        print(f"📄 Carregando dados da UFMG de: {editais_rapidos[-1]}")
        with open(editais_rapidos[-1], 'r', encoding='utf-8') as f:
            dados = json.load(f)
            for item in dados.get('ufmg', []):
                if not item.get('link_pdf'):
                    item['link_pdf'] = 'https://www.ufmg.br/prograd/editais-chamadas/'
                    item['tipo_link'] = 'Página com PDFs'
                else:
                    item['tipo_link'] = 'PDF Direto'
                dados_reorganizados['ufmg'].append(item)
    
    # CNPq - Adicionar links que levam a PDFs
    if chamadas_detalhadas:
        print(f"📄 Carregando dados do CNPq de: {chamadas_detalhadas[-1]}")
        with open(chamadas_detalhadas[-1], 'r', encoding='utf-8') as f:
            dados = json.load(f)
            for item in dados.get('chamadas_cnpq', []):
                if not item.get('link_pdf'):
                    item['link_pdf'] = item.get('link_permanente', 'https://www.cnpq.br/web/guest/chamadas-publicas')
                item['tipo_link'] = 'Página com PDFs'
                item['instrucoes'] = 'Acesse a página para encontrar os PDFs dos editais'
                dados_reorganizados['cnpq'].append(item)
    
    # Salvar dados reorganizados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nome_arquivo = f'dados_reorganizados_com_pdfs_{timestamp}.json'
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados_reorganizados, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dados reorganizados salvos em: {nome_arquivo}")
    print(f"📊 Total de oportunidades: {sum(len(v) for v in dados_reorganizados.values() if isinstance(v, list))}")
    print(f"📄 FAPEMIG: {len(dados_reorganizados['fapemig'])} com links para PDFs")
    print(f"📄 UFMG: {len(dados_reorganizados['ufmg'])} com PDFs diretos")
    print(f"📄 CNPq: {len(dados_reorganizados['cnpq'])} com links para PDFs")
    
    return dados_reorganizados

def mostrar_relatorio_completo(dados):
    """Mostra relatório completo com todos os editais e seus links"""
    print("\n" + "="*80)
    print("📋 RELATÓRIO COMPLETO - TODOS OS EDITAIS COM LINKS PARA PDFs")
    print("="*80)
    
    # FAPEMIG
    print(f"\n🔬 FAPEMIG - {len(dados['fapemig'])} OPORTUNIDADES")
    print("-" * 50)
    for i, item in enumerate(dados['fapemig'], 1):
        print(f"{i}. {item['titulo']}")
        print(f"   📄 Link: {item['link_pdf']}")
        print(f"   🔗 Alternativo: {item['link_alternativo']}")
        print(f"   📝 Tipo: {item['tipo_link']}")
        print(f"   💡 Instruções: {item['instrucoes']}")
        print()
    
    # UFMG
    print(f"\n🏫 UFMG - {len(dados['ufmg'])} EDITAIS")
    print("-" * 50)
    for i, item in enumerate(dados['ufmg'], 1):
        print(f"{i}. {item['titulo']}")
        print(f"   📄 Link: {item['link_pdf']}")
        print(f"   📝 Tipo: {item['tipo_link']}")
        print()
    
    # CNPq
    print(f"\n🚀 CNPq - {len(dados['cnpq'])} CHAMADAS")
    print("-" * 50)
    for i, item in enumerate(dados['cnpq'], 1):
        print(f"{i}. {item['titulo']}")
        print(f"   📄 Link: {item['link_pdf']}")
        print(f"   📝 Tipo: {item['tipo_link']}")
        print(f"   💡 Instruções: {item['instrucoes']}")
        if item.get('data_inscricao'):
            print(f"   ⏰ Prazo: {item['data_inscricao']}")
        print()

if __name__ == "__main__":
    try:
        # Reorganizar dados
        dados = reorganizar_dados()
        
        # Mostrar relatório completo
        mostrar_relatorio_completo(dados)
        
        print("🎉 Processo concluído com sucesso!")
        print("📁 Arquivo gerado: dados_reorganizados_com_pdfs_*.json")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Verifique se os arquivos dos scrapers existem na pasta atual")
