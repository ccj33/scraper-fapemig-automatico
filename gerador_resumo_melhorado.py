#!/usr/bin/env python3
"""
Gerador de Resumos Melhorados para Scraping
===========================================

Transforma dados brutos em resumos legíveis e organizados
Inclui informações extraídas de PDFs
"""

from datetime import datetime, timedelta
from typing import List, Dict

class GeradorResumoMelhorado:
    """Gera resumos legíveis e organizados dos dados de scraping"""
    
    def __init__(self, dados_scraping: Dict):
        self.dados = dados_scraping
        self.timestamp = datetime.now()
        
    def gerar_resumo_completo(self) -> str:
        """Gera resumo completo e legível"""
        
        resumo = f"""
🚀 RELATÓRIO COMPLETO DE OPORTUNIDADES
=======================================
📅 Gerado em: {self.timestamp.strftime('%d/%m/%Y às %H:%M:%S')}
🎯 Total de Oportunidades: {self.dados.get('total_editais', 0)}

{'='*60}

📚 UFMG - EDITAIS E CHAMADAS
{'='*60}
{self._formatar_ufmg()}

{'='*60}

🔬 FAPEMIG - OPORTUNIDADES
{'='*60}
{self._formatar_fapemig()}

{'='*60}

📖 CNPq - CHAMADAS PÚBLICAS
{'='*60}
{self._formatar_cnpq()}

{'='*60}

📄 ANÁLISE DE PDFs EXTRAÍDOS
{'='*60}
{self._formatar_analise_pdfs()}

{'='*60}

📊 RESUMO EXECUTIVO
{'='*60}
{self._gerar_resumo_executivo()}

{'='*60}

🤖 Sistema automatizado via GitHub Actions
📧 Enviado automaticamente para: {self._get_email_destino()}
⏰ Próxima execução: {self._get_proxima_execucao()}
        """
        
        return resumo
        
    def _formatar_ufmg(self) -> str:
        """Formata dados da UFMG de forma legível"""
        ufmg_data = self.dados.get('ufmg', [])
        
        if not ufmg_data:
            return "❌ Nenhum edital encontrado"
            
        formatted = f"📋 Total de Editais: {len(ufmg_data)}\n\n"
        
        for i, edital in enumerate(ufmg_data, 1):
            formatted += f"🔸 EDITAL #{i}\n"
            formatted += f"   📝 Título: {edital.get('titulo', 'Sem título')}\n"
            
            if 'data' in edital and edital['data'] != "Data não encontrada":
                formatted += f"   📅 Data: {edital['data']}\n"
                
            if 'valor' in edital and edital['valor'] != "Valor não informado":
                formatted += f"   💰 Valor: {edital['valor']}"
                if edital.get('valor_fonte') == 'PDF extraído':
                    formatted += " (📄 Extraído do PDF)"
                formatted += "\n"
                
            if 'prazo' in edital and edital['prazo'] != "Prazo não informado":
                formatted += f"   ⏰ Prazo: {edital['prazo']}"
                if edital.get('prazo_fonte') == 'PDF extraído':
                    formatted += " (📄 Extraído do PDF)"
                formatted += "\n"
                
            if 'objetivo' in edital and edital['objetivo'] != "Objetivo não informado":
                formatted += f"   🎯 Objetivo: {edital['objetivo'][:100]}..."
                if edital.get('objetivo_fonte') == 'PDF extraído':
                    formatted += " (📄 Extraído do PDF)"
                formatted += "\n"
                
            formatted += f"   🔗 Link: {edital.get('url', 'Não disponível')}\n"
            
            # Informações do PDF se disponível
            if edital.get('pdf_extraido'):
                formatted += f"   📄 PDF: ✅ Extraído ({edital.get('pdf_paginas', 'N/A')} páginas)\n"
                if edital.get('pdf_valor_encontrado'):
                    formatted += f"      💰 Valor no PDF: {edital['pdf_valor_encontrado']}\n"
                if edital.get('pdf_prazo_encontrado'):
                    formatted += f"      ⏰ Prazo no PDF: {edital['pdf_prazo_encontrado']}\n"
                if edital.get('pdf_objetivo_encontrado'):
                    formatted += f"      🎯 Objetivo no PDF: {edital['pdf_objetivo_encontrado'][:80]}...\n"
            elif edital.get('pdf_erro'):
                formatted += f"   📄 PDF: ❌ Erro - {edital['pdf_erro']}\n"
            else:
                formatted += f"   📄 PDF: ⚠️ Não processado\n"
                
            formatted += "\n"
            
        return formatted
        
    def _formatar_fapemig(self) -> str:
        """Formata dados da FAPEMIG de forma legível"""
        fapemig_data = self.dados.get('fapemig', [])
        
        if not fapemig_data:
            return "❌ Nenhuma oportunidade encontrada"
            
        formatted = f"📋 Total de Oportunidades: {len(fapemig_data)}\n\n"
        
        for i, oportunidade in enumerate(fapemig_data, 1):
            formatted += f"🔸 OPORTUNIDADE #{i}\n"
            formatted += f"   📝 Título: {oportunidade.get('titulo', 'Sem título')}\n"
            
            if 'valor' in oportunidade and oportunidade['valor'] != "Valor não informado":
                formatted += f"   💰 Valor: {oportunidade['valor']}"
                if oportunidade.get('valor_fonte') == 'PDF extraído':
                    formatted += " (📄 Extraído do PDF)"
                formatted += "\n"
                
            if 'prazo' in oportunidade and oportunidade['prazo'] != "Prazo não informado":
                formatted += f"   ⏰ Prazo: {oportunidade['prazo']}"
                if oportunidade.get('prazo_fonte') == 'PDF extraído':
                    formatted += " (📄 Extraído do PDF)"
                formatted += "\n"
                
            if 'url' in oportunidade:
                formatted += f"   🔗 Link: {oportunidade['url']}\n"
            
            # Informações do PDF se disponível
            if oportunidade.get('pdf_extraido'):
                formatted += f"   📄 PDF: ✅ Extraído ({oportunidade.get('pdf_paginas', 'N/A')} páginas)\n"
                if oportunidade.get('pdf_valor_encontrado'):
                    formatted += f"      💰 Valor no PDF: {oportunidade['pdf_valor_encontrado']}\n"
                if oportunidade.get('pdf_prazo_encontrado'):
                    formatted += f"      ⏰ Prazo no PDF: {oportunidade['pdf_prazo_encontrado']}\n"
                if oportunidade.get('pdf_objetivo_encontrado'):
                    formatted += f"      🎯 Objetivo no PDF: {oportunidade['pdf_objetivo_encontrado'][:80]}...\n"
            elif oportunidade.get('pdf_erro'):
                formatted += f"   📄 PDF: ❌ Erro - {oportunidade['pdf_erro']}\n"
            else:
                formatted += f"   📄 PDF: ⚠️ Não processado\n"
                
            formatted += "\n"
            
        return formatted
        
    def _formatar_cnpq(self) -> str:
        """Formata dados do CNPq de forma legível"""
        cnpq_data = self.dados.get('cnpq', [])
        
        if not cnpq_data:
            return "❌ Nenhuma chamada encontrada"
            
        formatted = f"📋 Total de Chamadas: {len(cnpq_data)}\n\n"
        
        for i, chamada in enumerate(cnpq_data, 1):
            formatted += f"🔸 CHAMADA #{i}\n"
            formatted += f"   📝 Título: {chamada.get('titulo', 'Sem título')}\n"
            
            if 'periodo_inscricao' in chamada and chamada['periodo_inscricao'] != "Período não encontrado":
                formatted += f"   📅 Período: {chamada['periodo_inscricao']}"
                if chamada.get('periodo_fonte') == 'PDF extraído':
                    formatted += " (📄 Extraído do PDF)"
                formatted += "\n"
                
            if 'valor' in chamada and chamada['valor'] != "Valor não informado":
                formatted += f"   💰 Valor: {chamada['valor']}"
                if chamada.get('valor_fonte') == 'PDF extraído':
                    formatted += " (📄 Extraído do PDF)"
                formatted += "\n"
                
            if 'descricao' in chamada and chamada['descricao'] != "Descrição não informada":
                formatted += f"   📖 Descrição: {chamada['descricao'][:100]}..."
                if chamada.get('descricao_fonte') == 'PDF extraído':
                    formatted += " (📄 Extraído do PDF)"
                formatted += "\n"
                
            if 'url_detalhes' in chamada:
                formatted += f"   🔗 Detalhes: {chamada['url_detalhes']}\n"
            
            # Informações do PDF se disponível
            if chamada.get('pdf_extraido'):
                formatted += f"   📄 PDF: ✅ Extraído ({chamada.get('pdf_paginas', 'N/A')} páginas)\n"
                if chamada.get('pdf_valor_encontrado'):
                    formatted += f"      💰 Valor no PDF: {chamada['pdf_valor_encontrado']}\n"
                if chamada.get('pdf_prazo_encontrado'):
                    formatted += f"      ⏰ Prazo no PDF: {chamada['pdf_prazo_encontrado']}\n"
                if chamada.get('pdf_objetivo_encontrado'):
                    formatted += f"      🎯 Objetivo no PDF: {chamada['pdf_objetivo_encontrado'][:80]}...\n"
            elif chamada.get('pdf_erro'):
                formatted += f"   📄 PDF: ❌ Erro - {chamada['pdf_erro']}\n"
            else:
                formatted += f"   📄 PDF: ⚠️ Não processado\n"
                
            formatted += "\n"
            
        return formatted
    
    def _formatar_analise_pdfs(self) -> str:
        """Formata análise dos PDFs extraídos"""
        pdf_metadata = self.dados.get('pdf_metadata', {})
        
        if not pdf_metadata:
            return "❌ Nenhum PDF foi processado"
        
        total_pdfs = pdf_metadata.get('total_pdfs_processados', 0)
        data_processamento = pdf_metadata.get('data_processamento', 'N/A')
        
        if total_pdfs == 0:
            return "⚠️ Nenhum PDF foi extraído com sucesso"
        
        # Contar PDFs por fonte
        ufmg_pdfs = sum(1 for item in self.dados.get('ufmg', []) if item.get('pdf_extraido'))
        fapemig_pdfs = sum(1 for item in self.dados.get('fapemig', []) if item.get('pdf_extraido'))
        cnpq_pdfs = sum(1 for item in self.dados.get('cnpq', []) if item.get('pdf_extraido'))
        
        # Estatísticas dos PDFs
        total_paginas = 0
        total_caracteres = 0
        idiomas = {'português': 0, 'inglês': 0}
        
        for fonte in ['ufmg', 'fapemig', 'cnpq']:
            for item in self.dados.get(fonte, []):
                if item.get('pdf_extraido'):
                    total_paginas += item.get('pdf_paginas', 0)
                    if item.get('pdf_estatisticas'):
                        total_caracteres += item.get('pdf_estatisticas', {}).get('total_caracteres', 0)
                    if item.get('pdf_idioma'):
                        idiomas[item.get('pdf_idioma')] = idiomas.get(item.get('pdf_idioma'), 0) + 1
        
        formatted = f"""
📊 ESTATÍSTICAS DOS PDFs EXTRAÍDOS:
   • Total de PDFs processados: {total_pdfs}
   • Data de processamento: {data_processamento}
   • UFMG: {ufmg_pdfs} PDFs
   • FAPEMIG: {fapemig_pdfs} PDFs  
   • CNPq: {cnpq_pdfs} PDFs

📄 ANÁLISE DO CONTEÚDO:
   • Total de páginas: {total_paginas}
   • Total de caracteres: {total_caracteres:,}
   • Idiomas detectados: {', '.join([f'{k}: {v}' for k, v in idiomas.items() if v > 0])}

🎯 BENEFÍCIOS DA EXTRAÇÃO:
   • Dados mais completos e precisos
   • Informações extraídas diretamente dos documentos
   • Complementação automática de campos vazios
   • Análise de conteúdo dos editais
        """
        
        return formatted
        
    def _gerar_resumo_executivo(self) -> str:
        """Gera resumo executivo dos dados"""
        total = self.dados.get('total_editais', 0)
        ufmg_count = len(self.dados.get('ufmg', []))
        fapemig_count = len(self.dados.get('fapemig', []))
        cnpq_count = len(self.dados.get('cnpq', []))
        
        # Contar PDFs extraídos
        total_pdfs = 0
        for fonte in ['ufmg', 'fapemig', 'cnpq']:
            for item in self.dados.get(fonte, []):
                if item.get('pdf_extraido'):
                    total_pdfs += 1
        
        resumo = f"""
📈 ESTATÍSTICAS GERAIS:
   • Total de Oportunidades: {total}
   • UFMG: {ufmg_count} editais
   • FAPEMIG: {fapemig_count} oportunidades  
   • CNPq: {cnpq_count} chamadas
   • PDFs extraídos: {total_pdfs}

🎯 PRÓXIMOS PASSOS RECOMENDADOS:
   • Verificar prazos de inscrição
   • Analisar valores e recursos disponíveis
   • Identificar oportunidades mais relevantes
   • Preparar documentação necessária

💡 DICAS IMPORTANTES:
   • Sempre verifique os links originais
   • Confirme datas e prazos nos sites oficiais
   • Prepare documentos com antecedência
   • Entre em contato em caso de dúvidas
   • PDFs extraídos fornecem informações complementares

🚀 NOVIDADES DO SISTEMA:
   • ✅ Extração automática de PDFs
   • ✅ Análise de conteúdo dos documentos
   • ✅ Complementação automática de dados
   • ✅ Detecção de idioma dos documentos
        """
        
        return resumo
        
    def _get_email_destino(self) -> str:
        """Retorna email de destino"""
        return "clevioferreira@gmail.com"
        
    def _get_proxima_execucao(self) -> str:
        """Calcula próxima execução (amanhã às 05:00 BRT)"""
        amanha = self.timestamp + timedelta(days=1)
        return amanha.strftime('%d/%m/%Y às 05:00 BRT')

def main():
    """Teste do gerador de resumos"""
    # Dados de exemplo com PDFs extraídos
    dados_exemplo = {
        'ufmg': [
            {
                'titulo': 'Edital PROEX nº 08/2025 – Programa de Apoio Integrado a Eventos',
                'data': '15/08/2025',
                'valor': 'R$ 5.000,00',
                'url': 'https://exemplo.com/edital1.pdf',
                'pdf_extraido': True,
                'pdf_paginas': 15,
                'pdf_valor_encontrado': 'R$ 5.000,00',
                'pdf_prazo_encontrado': '30/09/2025',
                'pdf_objetivo_encontrado': 'Apoiar eventos acadêmicos e científicos',
                'pdf_idioma': 'português'
            }
        ],
        'fapemig': [
            {
                'titulo': 'CHAMADA FAPEMIG 011/2025 - DEEP TECH - INSERÇÃO NO MERCADO E INOVAÇÃO',
                'valor': 'R$ 50.000,00',
                'url': 'https://exemplo.com/chamada1.pdf',
                'pdf_extraido': True,
                'pdf_paginas': 25,
                'pdf_valor_encontrado': 'R$ 50.000,00',
                'pdf_prazo_encontrado': '15/10/2025',
                'pdf_idioma': 'português'
            }
        ],
        'cnpq': [
            {
                'titulo': 'CHAMADA ERC- CNPQ - 2025 Nº 13/2025',
                'periodo_inscricao': '01/09/2025 a 30/09/2025',
                'url_detalhes': 'https://exemplo.com/cnpq1.pdf',
                'pdf_extraido': True,
                'pdf_paginas': 20,
                'pdf_idioma': 'português'
            }
        ],
        'total_editais': 3,
        'pdf_metadata': {
            'data_processamento': '2025-01-16T10:30:00',
            'total_pdfs_processados': 3,
            'versao_integrador': '1.0.0'
        }
    }
    
    gerador = GeradorResumoMelhorado(dados_exemplo)
    resumo = gerador.gerar_resumo_completo()
    
    print(resumo)

if __name__ == "__main__":
    main()
