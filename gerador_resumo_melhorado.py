#!/usr/bin/env python3
"""
Gerador de Resumos Melhorados para Scraping
===========================================

Transforma dados brutos em resumos legíveis e organizados
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
                formatted += f"   💰 Valor: {edital['valor']}\n"
                
            if 'prazo' in edital and edital['prazo'] != "Prazo não informado":
                formatted += f"   ⏰ Prazo: {edital['prazo']}\n"
                
            if 'objetivo' in edital and edital['objetivo'] != "Objetivo não informado":
                formatted += f"   🎯 Objetivo: {edital['objetivo'][:100]}...\n"
                
            formatted += f"   🔗 Link: {edital.get('url', 'Não disponível')}\n"
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
                formatted += f"   💰 Valor: {oportunidade['valor']}\n"
                
            if 'prazo' in oportunidade and oportunidade['prazo'] != "Prazo não informado":
                formatted += f"   ⏰ Prazo: {oportunidade['prazo']}\n"
                
            if 'url' in oportunidade:
                formatted += f"   🔗 Link: {oportunidade['url']}\n"
                
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
                formatted += f"   📅 Período: {chamada['periodo_inscricao']}\n"
                
            if 'valor' in chamada and chamada['valor'] != "Valor não informado":
                formatted += f"   💰 Valor: {chamada['valor']}\n"
                
            if 'descricao' in chamada and chamada['descricao'] != "Descrição não informada":
                formatted += f"   📖 Descrição: {chamada['descricao'][:100]}...\n"
                
            if 'url_detalhes' in chamada:
                formatted += f"   🔗 Detalhes: {chamada['url_detalhes']}\n"
                
            formatted += "\n"
            
        return formatted
        
    def _gerar_resumo_executivo(self) -> str:
        """Gera resumo executivo dos dados"""
        total = self.dados.get('total_editais', 0)
        ufmg_count = len(self.dados.get('ufmg', []))
        fapemig_count = len(self.dados.get('fapemig', []))
        cnpq_count = len(self.dados.get('cnpq', []))
        
        resumo = f"""
📈 ESTATÍSTICAS GERAIS:
   • Total de Oportunidades: {total}
   • UFMG: {ufmg_count} editais
   • FAPEMIG: {ufmg_count} oportunidades  
   • CNPq: {cnpq_count} chamadas

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
        """
        
        return resumo
        
    def _get_email_destino(self) -> str:
        """Retorna email de destino"""
        return "ccjota51@gmail.com"
        
    def _get_proxima_execucao(self) -> str:
        """Calcula próxima execução (amanhã às 05:00 BRT)"""
        amanha = self.timestamp + timedelta(days=1)
        return amanha.strftime('%d/%m/%Y às 05:00 BRT')

def main():
    """Teste do gerador de resumos"""
    # Dados de exemplo
    dados_exemplo = {
        'ufmg': [
            {
                'titulo': 'Edital PROEX nº 08/2025 – Programa de Apoio Integrado a Eventos',
                'data': '15/08/2025',
                'valor': 'R$ 5.000,00',
                'url': 'https://exemplo.com/edital1.pdf'
            }
        ],
        'fapemig': [
            {
                'titulo': 'CHAMADA FAPEMIG 011/2025 - DEEP TECH - INSERÇÃO NO MERCADO E INOVAÇÃO',
                'valor': 'R$ 50.000,00',
                'url': 'https://exemplo.com/chamada1'
            }
        ],
        'cnpq': [
            {
                'titulo': 'CHAMADA ERC- CNPQ - 2025 Nº 13/2025',
                'periodo_inscricao': '01/09/2025 a 30/09/2025',
                'url_detalhes': 'https://exemplo.com/cnpq1'
            }
        ],
        'total_editais': 3
    }
    
    gerador = GeradorResumoMelhorado(dados_exemplo)
    resumo = gerador.gerar_resumo_completo()
    
    print(resumo)

if __name__ == "__main__":
    main()
