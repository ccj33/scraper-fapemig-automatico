#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de Relatório FAPEMIG
Cria relatórios bonitos para apresentações e emails
"""

import json
import re
from datetime import datetime

def gerar_relatorio_texto(chamadas):
    """
    Gera relatório em formato de texto para emails
    """
    relatorio = []
    relatorio.append("🎯 RELATÓRIO DE CHAMADAS FAPEMIG")
    relatorio.append("=" * 60)
    relatorio.append(f"📅 Data do relatório: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    relatorio.append(f"📊 Total de chamadas: {len(chamadas)}")
    relatorio.append("")
    
    for i, chamada in enumerate(chamadas, 1):
        relatorio.append(f"{i}. {chamada['titulo']}")
        
        if chamada.get('numero'):
            relatorio.append(f"   🔢 Número: {chamada['numero']}")
        
        if chamada.get('prazo_final'):
            relatorio.append(f"   ⏰ Prazo: {chamada['prazo_final']}")
        
        if chamada.get('link_pdf'):
            relatorio.append(f"   🔗 Link: {chamada['link_pdf']}")
        
        if chamada.get('descricao'):
            relatorio.append(f"   📝 {chamada['descricao']}")
        
        relatorio.append("")
    
    relatorio.append("📋 Fonte: FAPEMIG - Fundação de Amparo à Pesquisa do Estado de Minas Gerais")
    relatorio.append("🌐 Site: http://www.fapemig.br/")
    
    return "\n".join(relatorio)

def gerar_relatorio_html(chamadas):
    """
    Gera relatório em formato HTML para apresentações
    """
    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório FAPEMIG - {datetime.now().strftime('%d/%m/%Y')}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
            margin-top: 10px;
        }}
        .stats {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            border-bottom: 1px solid #e9ecef;
        }}
        .stats .stat-item {{
            display: inline-block;
            margin: 0 20px;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .stats .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        .stats .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .content {{
            padding: 30px;
        }}
        .chamada {{
            background: #f8f9fa;
            margin: 20px 0;
            padding: 25px;
            border-radius: 10px;
            border-left: 5px solid #3498db;
            transition: transform 0.2s;
        }}
        .chamada:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        .chamada h3 {{
            margin: 0 0 15px 0;
            color: #2c3e50;
            font-size: 1.3em;
        }}
        .chamada .meta {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }}
        .meta-item {{
            background: white;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }}
        .meta-item .label {{
            font-weight: bold;
            color: #666;
            font-size: 0.8em;
            text-transform: uppercase;
        }}
        .meta-item .value {{
            color: #2c3e50;
            margin-top: 5px;
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
        .urgent {{
            border-left-color: #e74c3c !important;
        }}
        .urgent .meta-item {{
            border-color: #e74c3c;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Relatório FAPEMIG</h1>
            <div class="subtitle">Chamadas e Oportunidades de Pesquisa</div>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{len(chamadas)}</div>
                <div class="stat-label">Chamadas Ativas</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{datetime.now().strftime('%d/%m')}</div>
                <div class="stat-label">Data do Relatório</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{sum(1 for c in chamadas if '2025' in c.get('numero', ''))}</div>
                <div class="stat-label">Chamadas 2025</div>
            </div>
        </div>
        
        <div class="content">
"""
    
    for i, chamada in enumerate(chamadas, 1):
        # Verifica se é urgente (prazo próximo)
        is_urgent = "urgent" if "2024" in chamada.get('numero', '') else ""
        
        html += f"""
            <div class="chamada {is_urgent}">
                <h3>{i}. {chamada['titulo']}</h3>
                <div class="meta">
"""
        
        if chamada.get('numero'):
            html += f"""
                    <div class="meta-item">
                        <div class="label">Número</div>
                        <div class="value">🔢 {chamada['numero']}</div>
                    </div>
"""
        
        if chamada.get('prazo_final'):
            html += f"""
                    <div class="meta-item">
                        <div class="label">Prazo Final</div>
                        <div class="value">⏰ {chamada['prazo_final']}</div>
                    </div>
"""
        
        if chamada.get('link_pdf'):
            html += f"""
                    <div class="meta-item">
                        <div class="label">Link</div>
                        <div class="value">🔗 <a href="{chamada['link_pdf']}" target="_blank">Acessar</a></div>
                    </div>
"""
        
        if chamada.get('descricao'):
            html += f"""
                    <div class="meta-item" style="grid-column: 1 / -1;">
                        <div class="label">Descrição</div>
                        <div class="value">📝 {chamada['descricao']}</div>
                    </div>
"""
        
        html += """
                </div>
            </div>
"""
    
    html += """
        </div>
        
        <div class="footer">
            📋 Fonte: FAPEMIG - Fundação de Amparo à Pesquisa do Estado de Minas Gerais<br>
            🌐 Site: <a href="http://www.fapemig.br/" target="_blank" style="color: #3498db;">http://www.fapemig.br/</a><br>
            📅 Relatório gerado em: """ + datetime.now().strftime('%d/%m/%Y às %H:%M') + """
        </div>
    </div>
</body>
</html>
"""
    
    return html

def gerar_relatorio_markdown(chamadas):
    """
    Gera relatório em formato Markdown para documentação
    """
    relatorio = []
    relatorio.append("# 🎯 Relatório de Chamadas FAPEMIG")
    relatorio.append("")
    relatorio.append(f"**Data do relatório:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}  ")
    relatorio.append(f"**Total de chamadas:** {len(chamadas)}  ")
    relatorio.append("")
    
    for i, chamada in enumerate(chamadas, 1):
        relatorio.append(f"## {i}. {chamada['titulo']}")
        relatorio.append("")
        
        if chamada.get('numero'):
            relatorio.append(f"**Número:** {chamada['numero']}  ")
        
        if chamada.get('prazo_final'):
            relatorio.append(f"**Prazo Final:** {chamada['prazo_final']}  ")
        
        if chamada.get('link_pdf'):
            relatorio.append(f"**Link:** [{chamada['link_pdf']}]({chamada['link_pdf']})  ")
        
        if chamada.get('descricao'):
            relatorio.append(f"**Descrição:** {chamada['descricao']}  ")
        
        relatorio.append("")
        relatorio.append("---")
        relatorio.append("")
    
    relatorio.append("---")
    relatorio.append("**Fonte:** FAPEMIG - Fundação de Amparo à Pesquisa do Estado de Minas Gerais  ")
    relatorio.append("**Site:** http://www.fapemig.br/")
    
    return "\n".join(relatorio)

def main():
    """
    Função principal
    """
    print("🚀 Gerador de Relatórios FAPEMIG")
    print("=" * 50)
    
    # Dados das chamadas (simulados)
    chamadas = [
        {
            "titulo": "CHAMADA FAPEMIG 011/2025 - DEEP TECH - INSERÇÃO NO MERCADO E TRAÇÃO COMERCIAL",
            "numero": "011/2025",
            "descricao": "Chamada para projetos de Deep Tech com foco em inserção no mercado",
            "data_inclusao": "15/08/2025",
            "prazo_final": "30/10/2025",
            "link_pdf": "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/",
            "fonte": "FAPEMIG",
            "data_coleta": datetime.now().isoformat()
        },
        {
            "titulo": "CHAMADA 016/2024 - PARTICIPAÇÃO COLETIVA EM EVENTOS TÉCNICOS NO PAÍS - 3ª ENTRADA",
            "numero": "016/2024",
            "descricao": "Apoio para participação em eventos técnicos nacionais",
            "data_inclusao": "10/08/2024",
            "prazo_final": "25/09/2024",
            "link_pdf": "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/",
            "fonte": "FAPEMIG",
            "data_coleta": datetime.now().isoformat()
        },
        {
            "titulo": "CHAMADA 005/2025 - ORGANIZAÇÃO DE EVENTOS DE CARÁTER TÉCNICO CIENTÍFICO - 2ª ENTRADA",
            "numero": "005/2025",
            "descricao": "Apoio para organização de eventos técnico-científicos",
            "data_inclusao": "05/08/2025",
            "prazo_final": "20/10/2025",
            "link_pdf": "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/",
            "fonte": "FAPEMIG",
            "data_coleta": datetime.now().isoformat()
        }
    ]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Gera relatório em texto
    relatorio_texto = gerar_relatorio_texto(chamadas)
    with open(f"relatorio_fapemig_texto_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(relatorio_texto)
    print(f"✅ Relatório em texto salvo: relatorio_fapemig_texto_{timestamp}.txt")
    
    # Gera relatório em HTML
    relatorio_html = gerar_relatorio_html(chamadas)
    with open(f"relatorio_fapemig_html_{timestamp}.html", 'w', encoding='utf-8') as f:
        f.write(relatorio_html)
    print(f"✅ Relatório em HTML salvo: relatorio_fapemig_html_{timestamp}.html")
    
    # Gera relatório em Markdown
    relatorio_md = gerar_relatorio_markdown(chamadas)
    with open(f"relatorio_fapemig_md_{timestamp}.md", 'w', encoding='utf-8') as f:
        f.write(relatorio_md)
    print(f"✅ Relatório em Markdown salvo: relatorio_fapemig_md_{timestamp}.md")
    
    print(f"\n🎉 Relatórios gerados com sucesso!")
    print("📁 Arquivos criados:")
    print("   • .txt - Para emails e cópia/cola")
    print("   • .html - Para apresentações e web")
    print("   • .md - Para documentação e GitHub")

if __name__ == "__main__":
    main()
