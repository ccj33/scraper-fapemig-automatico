#!/usr/bin/env python3
"""
Gerador de Resumos Completos e Inteligentes
===========================================

Resolve todos os problemas de truncamento identificados:
1. Extrai primeiro parágrafo completo com pelo menos 12 palavras
2. Mostra texto completo se houver menos de 18 palavras
3. Só adiciona "..." se houver mais de 18 palavras
4. Preserva informações completas dos PDFs
5. Inclui campos link_pdf e pdf_hash
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

class GeradorResumoCompleto:
    """Gera resumos completos e inteligentes dos dados de scraping"""
    
    def __init__(self, dados_scraping: Dict):
        self.dados = dados_scraping
        self.timestamp = datetime.now()
        
    def gerar_resumo_completo(self) -> str:
        """Gera resumo completo e inteligente"""
        
        resumo = f"""
🚀 RELATÓRIO COMPLETO DE OPORTUNIDADES
=======================================
📅 Gerado em: {self.timestamp.strftime('%d/%m/%Y às %H:%M:%S')}
🎯 Total de Oportunidades: {self.dados.get('total_editais', 0)}

{'='*60}

📚 UFMG - EDITAIS E CHAMADAS
{'='*60}
{self._formatar_ufmg_completo()}

{'='*60}

🔬 FAPEMIG - OPORTUNIDADES
{'='*60}
{self._formatar_fapemig_completo()}

{'='*60}

📖 CNPq - CHAMADAS PÚBLICAS
{'='*60}
{self._formatar_cnpq_completo()}

{'='*60}

📄 ANÁLISE DETALHADA DE PDFs EXTRAÍDOS
{'='*60}
{self._formatar_analise_pdfs_completa()}

{'='*60}

📊 RESUMO EXECUTIVO INTELIGENTE
{'='*60}
{self._gerar_resumo_executivo_inteligente()}

{'='*60}

🤖 Sistema automatizado via GitHub Actions
📧 Enviado automaticamente para: {self._get_email_destino()}
⏰ Próxima execução: {self._get_proxima_execucao()}
        """
        
        return resumo
    
    def _extrair_primeiro_paragrafo_completo(self, texto: str, min_palavras: int = 12) -> str:
        """
        Extrai o primeiro parágrafo completo com pelo menos min_palavras
        
        Args:
            texto: Texto para extrair parágrafo
            min_palavras: Número mínimo de palavras para considerar completo
            
        Returns:
            Primeiro parágrafo completo ou texto truncado inteligentemente
        """
        if not texto:
            return ""
        
        # Dividir em parágrafos
        paragrafos = [p.strip() for p in texto.split('\n') if p.strip()]
        
        # Procurar primeiro parágrafo com pelo menos min_palavras
        for paragrafo in paragrafos:
            palavras = paragrafo.split()
            if len(palavras) >= min_palavras:
                return paragrafo
        
        # Se não encontrou parágrafo longo, retornar o primeiro não vazio
        for paragrafo in paragrafos:
            if paragrafo:
                return paragrafo
        
        return texto[:200] if len(texto) > 200 else texto
    
    def _formatar_texto_inteligente(self, texto: str, max_palavras: int = 18) -> str:
        """
        Formata texto de forma inteligente:
        - Se menos de max_palavras: mostra completo
        - Se mais de max_palavras: mostra início + "..."
        
        Args:
            texto: Texto para formatar
            max_palavras: Limite de palavras para truncamento
            
        Returns:
            Texto formatado
        """
        if not texto:
            return ""
        
        palavras = texto.split()
        
        if len(palavras) <= max_palavras:
            # Mostrar texto completo
            return texto
        else:
            # Mostrar início + "..."
            inicio = ' '.join(palavras[:max_palavras])
            return f"{inicio}..."
    
    def _formatar_ufmg_completo(self) -> str:
        """Formata dados da UFMG de forma completa e inteligente"""
        ufmg_data = self.dados.get('ufmg', [])
        
        if not ufmg_data:
            return "❌ Nenhum edital encontrado"
            
        formatted = f"📋 Total de Editais: {len(ufmg_data)}\n\n"
        
        for i, edital in enumerate(ufmg_data, 1):
            formatted += f"🔸 EDITAL #{i}\n"
            formatted += f"   📝 Título: {edital.get('titulo', 'Sem título')}\n"
            
            if 'data' in edital and edital['data'] != "Data não encontrada":
                formatted += f"   📅 Data: {edital['data']}\n"
                
            # Valor selecionado (se disponível)
            if edital.get('valor_selecionado'):
                formatted += f"   💰 Valor Selecionado: {edital['valor_selecionado']}"
                if edital.get('valor_fonte'):
                    formatted += f" ({edital['valor_fonte']})"
                formatted += "\n"
            elif 'valor' in edital and edital['valor'] != "Valor não informado":
                formatted += f"   💰 Valor: {edital['valor']}\n"
            
            # Prazo selecionado (se disponível)
            if edital.get('prazo_selecionado'):
                formatted += f"   ⏰ Prazo Selecionado: {edital['prazo_selecionado']}"
                if edital.get('prazo_fonte'):
                    formatted += f" ({edital['prazo_fonte']})"
                formatted += "\n"
            elif 'prazo' in edital and edital['prazo'] != "Prazo não informado":
                formatted += f"   ⏰ Prazo: {edital['prazo']}\n"
            
            # Objetivo selecionado (se disponível)
            if edital.get('objetivo_selecionado'):
                objetivo = edital['objetivo_selecionado']
                formatted += f"   🎯 Objetivo Selecionado: {self._formatar_texto_inteligente(objetivo)}"
                if edital.get('objetivo_fonte'):
                    formatted += f" ({edital['objetivo_fonte']})"
                formatted += "\n"
            elif 'objetivo' in edital and edital['objetivo'] != "Objetivo não informado":
                objetivo = edital['objetivo']
                formatted += f"   🎯 Objetivo: {self._formatar_texto_inteligente(objetivo)}\n"
            
            # Área selecionada (se disponível)
            if edital.get('area_selecionada'):
                area = edital['area_selecionada']
                formatted += f"   🔬 Área Selecionada: {self._formatar_texto_inteligente(area)}"
                if edital.get('area_fonte'):
                    formatted += f" ({edital['area_fonte']})"
                formatted += "\n"
            
            formatted += f"   🔗 Link: {edital.get('url', 'Não disponível')}\n"
            
            # Informações completas do PDF
            if edital.get('pdf_extraido'):
                formatted += f"   📄 PDF: ✅ Extraído\n"
                formatted += f"      🔗 Link Direto: {edital.get('pdf_link_direto', 'N/A')}\n"
                formatted += f"      🆔 Hash: {edital.get('pdf_hash', 'N/A')[:16]}...\n"
                formatted += f"      📊 Status: {edital.get('pdf_status_baixa', 'N/A')} / {edital.get('pdf_status_analise', 'N/A')}\n"
                formatted += f"      💾 Tamanho: {edital.get('pdf_tamanho_bytes', 0):,} bytes\n"
                formatted += f"      🌐 Idioma: {edital.get('pdf_idioma', 'N/A')}\n"
                
                # Valores encontrados no PDF (todos)
                if edital.get('todos_valores_encontrados'):
                    valores = edital['todos_valores_encontrados']
                    formatted += f"      💰 Todos os Valores: {', '.join(valores[:3])}"
                    if len(valores) > 3:
                        formatted += f" ... e mais {len(valores) - 3}"
                    formatted += "\n"
                
                # Prazos encontrados no PDF (todos)
                if edital.get('todos_prazos_encontrados'):
                    prazos = edital['todos_prazos_encontrados']
                    formatted += f"      ⏰ Todos os Prazos: {', '.join(prazos[:3])}"
                    if len(prazos) > 3:
                        formatted += f" ... e mais {len(prazos) - 3}"
                    formatted += "\n"
                
                # Objetivos encontrados no PDF (todos)
                if edital.get('todos_objetivos_encontrados'):
                    objetivos = edital['todos_objetivos_encontrados']
                    formatted += f"      🎯 Todos os Objetivos:\n"
                    for j, objetivo in enumerate(objetivos[:3], 1):
                        objetivo_formatado = self._formatar_texto_inteligente(objetivo)
                        formatted += f"         {j}. {objetivo_formatado}\n"
                    if len(objetivos) > 3:
                        formatted += f"         ... e mais {len(objetivos) - 3} objetivos\n"
                
                # Áreas encontradas no PDF (todas)
                if edital.get('todas_areas_encontradas'):
                    areas = edital['todas_areas_encontradas']
                    formatted += f"      🔬 Todas as Áreas:\n"
                    for j, area in enumerate(areas[:3], 1):
                        area_formatada = self._formatar_texto_inteligente(area)
                        formatted += f"         {j}. {area_formatada}\n"
                    if len(areas) > 3:
                        formatted += f"         ... e mais {len(areas) - 3} áreas\n"
                
                # Datas encontradas no PDF
                if edital.get('pdf_datas_encontradas'):
                    datas = edital['pdf_datas_encontradas']
                    formatted += f"      📅 Datas no PDF: {', '.join(datas[:5])}"
                    if len(datas) > 5:
                        formatted += f" ... e mais {len(datas) - 5}"
                    formatted += "\n"
                
            elif edital.get('pdf_erro'):
                formatted += f"   📄 PDF: ❌ Erro - {edital['pdf_erro']}\n"
                formatted += f"      📋 Motivo: {edital.get('pdf_motivo', 'N/A')}\n"
            else:
                formatted += f"   📄 PDF: ⚠️ {edital.get('pdf_motivo', 'Não processado')}\n"
                
            formatted += "\n"
            
        return formatted
    
    def _formatar_fapemig_completo(self) -> str:
        """Formata dados da FAPEMIG de forma completa e inteligente"""
        fapemig_data = self.dados.get('fapemig', [])
        
        if not fapemig_data:
            return "❌ Nenhuma oportunidade encontrada"
            
        formatted = f"📋 Total de Oportunidades: {len(fapemig_data)}\n\n"
        
        for i, oportunidade in enumerate(fapemig_data, 1):
            formatted += f"🔸 OPORTUNIDADE #{i}\n"
            formatted += f"   📝 Título: {oportunidade.get('titulo', 'Sem título')}\n"
            
            # Valor selecionado (se disponível)
            if oportunidade.get('valor_selecionado'):
                formatted += f"   💰 Valor Selecionado: {oportunidade['valor_selecionado']}"
                if oportunidade.get('valor_fonte'):
                    formatted += f" ({oportunidade['valor_fonte']})"
                formatted += "\n"
            elif 'valor' in oportunidade and oportunidade['valor'] != "Valor não informado":
                formatted += f"   💰 Valor: {oportunidade['valor']}\n"
            
            # Prazo selecionado (se disponível)
            if oportunidade.get('prazo_selecionado'):
                formatted += f"   ⏰ Prazo Selecionado: {oportunidade['prazo_selecionado']}"
                if oportunidade.get('prazo_fonte'):
                    formatted += f" ({oportunidade['prazo_fonte']})"
                formatted += "\n"
            elif 'prazo' in oportunidade and oportunidade['prazo'] != "Prazo não informado":
                formatted += f"   ⏰ Prazo: {oportunidade['prazo']}\n"
            
            if 'url' in oportunidade:
                formatted += f"   🔗 Link: {oportunidade['url']}\n"
            
            # Informações completas do PDF
            if oportunidade.get('pdf_extraido'):
                formatted += f"   📄 PDF: ✅ Extraído\n"
                formatted += f"      🔗 Link Direto: {oportunidade.get('pdf_link_direto', 'N/A')}\n"
                formatted += f"      🆔 Hash: {oportunidade.get('pdf_hash', 'N/A')[:16]}...\n"
                formatted += f"      📊 Status: {oportunidade.get('pdf_status_baixa', 'N/A')} / {oportunidade.get('pdf_status_analise', 'N/A')}\n"
                formatted += f"      💾 Tamanho: {oportunidade.get('pdf_tamanho_bytes', 0):,} bytes\n"
                formatted += f"      🌐 Idioma: {oportunidade.get('pdf_idioma', 'N/A')}\n"
                
                # Valores encontrados no PDF (todos)
                if oportunidade.get('todos_valores_encontrados'):
                    valores = oportunidade['todos_valores_encontrados']
                    formatted += f"      💰 Todos os Valores: {', '.join(valores[:3])}"
                    if len(valores) > 3:
                        formatted += f" ... e mais {len(valores) - 3}"
                    formatted += "\n"
                
                # Prazos encontrados no PDF (todos)
                if oportunidade.get('todos_prazos_encontrados'):
                    prazos = oportunidade['todos_prazos_encontrados']
                    formatted += f"      ⏰ Todos os Prazos: {', '.join(prazos[:3])}"
                    if len(prazos) > 3:
                        formatted += f" ... e mais {len(prazos) - 3}"
                    formatted += "\n"
                
                # Objetivos encontrados no PDF (todos)
                if oportunidade.get('todos_objetivos_encontrados'):
                    objetivos = oportunidade['todos_objetivos_encontrados']
                    formatted += f"      🎯 Todos os Objetivos:\n"
                    for j, objetivo in enumerate(objetivos[:3], 1):
                        objetivo_formatado = self._formatar_texto_inteligente(objetivo)
                        formatted += f"         {j}. {objetivo_formatado}\n"
                    if len(objetivos) > 3:
                        formatted += f"         ... e mais {len(objetivos) - 3} objetivos\n"
                
                # Áreas encontradas no PDF (todas)
                if oportunidade.get('todas_areas_encontradas'):
                    areas = oportunidade['todas_areas_encontradas']
                    formatted += f"      🔬 Todas as Áreas:\n"
                    for j, area in enumerate(areas[:3], 1):
                        area_formatada = self._formatar_texto_inteligente(area)
                        formatted += f"         {j}. {area_formatada}\n"
                    if len(areas) > 3:
                        formatted += f"         ... e mais {len(areas) - 3} áreas\n"
                
                # Datas encontradas no PDF
                if oportunidade.get('pdf_datas_encontradas'):
                    datas = oportunidade['pdf_datas_encontradas']
                    formatted += f"      📅 Datas no PDF: {', '.join(datas[:5])}"
                    if len(datas) > 5:
                        formatted += f" ... e mais {len(datas) - 5}"
                    formatted += "\n"
                
            elif oportunidade.get('pdf_erro'):
                formatted += f"   📄 PDF: ❌ Erro - {oportunidade['pdf_erro']}\n"
                formatted += f"      📋 Motivo: {oportunidade.get('pdf_motivo', 'N/A')}\n"
            else:
                formatted += f"   📄 PDF: ⚠️ {oportunidade.get('pdf_motivo', 'Não processado')}\n"
                
            formatted += "\n"
            
        return formatted
    
    def _formatar_cnpq_completo(self) -> str:
        """Formata dados do CNPq de forma completa e inteligente"""
        cnpq_data = self.dados.get('cnpq', [])
        
        if not cnpq_data:
            return "❌ Nenhuma chamada encontrada"
            
        formatted = f"📋 Total de Chamadas: {len(cnpq_data)}\n\n"
        
        for i, chamada in enumerate(cnpq_data, 1):
            formatted += f"🔸 CHAMADA #{i}\n"
            formatted += f"   📝 Título: {chamada.get('titulo', 'Sem título')}\n"
            
            # Período selecionado (se disponível)
            if chamada.get('prazo_selecionado'):
                formatted += f"   📅 Prazo Selecionado: {chamada['prazo_selecionado']}"
                if chamada.get('prazo_fonte'):
                    formatted += f" ({chamada['prazo_fonte']})"
                formatted += "\n"
            elif 'periodo_inscricao' in chamada and chamada['periodo_inscricao'] != "Período não encontrado":
                formatted += f"   📅 Período: {chamada['periodo_inscricao']}\n"
            
            # Valor selecionado (se disponível)
            if chamada.get('valor_selecionado'):
                formatted += f"   💰 Valor Selecionado: {chamada['valor_selecionado']}"
                if chamada.get('valor_fonte'):
                    formatted += f" ({chamada['valor_fonte']})"
                formatted += "\n"
            elif 'valor' in chamada and chamada['valor'] != "Valor não informado":
                formatted += f"   💰 Valor: {chamada['valor']}\n"
            
            # Objetivo selecionado (se disponível)
            if chamada.get('objetivo_selecionado'):
                objetivo = chamada['objetivo_selecionado']
                formatted += f"   🎯 Objetivo Selecionado: {self._formatar_texto_inteligente(objetivo)}"
                if chamada.get('objetivo_fonte'):
                    formatted += f" ({chamada['objetivo_fonte']})"
                formatted += "\n"
            elif 'descricao' in chamada and chamada['descricao'] != "Descrição não informada":
                descricao = chamada['descricao']
                formatted += f"   📖 Descrição: {self._formatar_texto_inteligente(descricao)}\n"
            
            # Área selecionada (se disponível)
            if chamada.get('area_selecionada'):
                area = chamada['area_selecionada']
                formatted += f"   🔬 Área Selecionada: {self._formatar_texto_inteligente(area)}"
                if chamada.get('area_fonte'):
                    formatted += f" ({chamada['area_fonte']})"
                formatted += "\n"
            
            if 'url_detalhes' in chamada:
                formatted += f"   🔗 Detalhes: {chamada['url_detalhes']}\n"
            
            # Informações completas do PDF
            if chamada.get('pdf_extraido'):
                formatted += f"   📄 PDF: ✅ Extraído\n"
                formatted += f"      🔗 Link Direto: {chamada.get('pdf_link_direto', 'N/A')}\n"
                formatted += f"      🆔 Hash: {chamada.get('pdf_hash', 'N/A')[:16]}...\n"
                formatted += f"      📊 Status: {chamada.get('pdf_status_baixa', 'N/A')} / {chamada.get('pdf_status_analise', 'N/A')}\n"
                formatted += f"      💾 Tamanho: {chamada.get('pdf_tamanho_bytes', 0):,} bytes\n"
                formatted += f"      🌐 Idioma: {chamada.get('pdf_idioma', 'N/A')}\n"
                
                # Valores encontrados no PDF (todos)
                if chamada.get('todos_valores_encontrados'):
                    valores = chamada['todos_valores_encontrados']
                    formatted += f"      💰 Todos os Valores: {', '.join(valores[:3])}"
                    if len(valores) > 3:
                        formatted += f" ... e mais {len(valores) - 3}"
                    formatted += "\n"
                
                # Prazos encontrados no PDF (todos)
                if chamada.get('todos_prazos_encontrados'):
                    prazos = chamada['todos_prazos_encontrados']
                    formatted += f"      ⏰ Todos os Prazos: {', '.join(prazos[:3])}"
                    if len(prazos) > 3:
                        formatted += f" ... e mais {len(prazos) - 3}"
                    formatted += "\n"
                
                # Objetivos encontrados no PDF (todos)
                if chamada.get('todos_objetivos_encontrados'):
                    objetivos = chamada['todos_objetivos_encontrados']
                    formatted += f"      🎯 Todos os Objetivos:\n"
                    for j, objetivo in enumerate(objetivos[:3], 1):
                        objetivo_formatado = self._formatar_texto_inteligente(objetivo)
                        formatted += f"         {j}. {objetivo_formatado}\n"
                    if len(objetivos) > 3:
                        formatted += f"         ... e mais {len(objetivos) - 3} objetivos\n"
                
                # Áreas encontradas no PDF (todas)
                if chamada.get('todas_areas_encontradas'):
                    areas = chamada['todas_areas_encontradas']
                    formatted += f"      🔬 Todas as Áreas:\n"
                    for j, area in enumerate(areas[:3], 1):
                        area_formatada = self._formatar_texto_inteligente(area)
                        formatted += f"         {j}. {area_formatada}\n"
                    if len(areas) > 3:
                        formatted += f"         ... e mais {len(areas) - 3} áreas\n"
                
                # Datas encontradas no PDF
                if chamada.get('pdf_datas_encontradas'):
                    datas = chamada['pdf_datas_encontradas']
                    formatted += f"      📅 Datas no PDF: {', '.join(datas[:5])}"
                    if len(datas) > 5:
                        formatted += f" ... e mais {len(datas) - 5}"
                    formatted += "\n"
                
            elif chamada.get('pdf_erro'):
                formatted += f"   📄 PDF: ❌ Erro - {chamada['pdf_erro']}\n"
                formatted += f"      📋 Motivo: {chamada.get('pdf_motivo', 'N/A')}\n"
            else:
                formatted += f"   📄 PDF: ⚠️ {chamada.get('pdf_motivo', 'Não processado')}\n"
                
            formatted += "\n"
            
        return formatted
    
    def _formatar_analise_pdfs_completa(self) -> str:
        """Formata análise completa dos PDFs extraídos"""
        pdf_metadata = self.dados.get('pdf_metadata', {})
        
        if not pdf_metadata:
            return "❌ Nenhum PDF foi processado"
        
        total_pdfs = pdf_metadata.get('total_pdfs_processados', 0)
        total_erros = pdf_metadata.get('total_pdfs_com_erro', 0)
        data_processamento = pdf_metadata.get('data_processamento', 'N/A')
        versao = pdf_metadata.get('versao_integrador', 'N/A')
        metodo = pdf_metadata.get('metodo', 'N/A')
        
        if total_pdfs == 0:
            return "⚠️ Nenhum PDF foi extraído com sucesso"
        
        # Contar PDFs por fonte
        ufmg_pdfs = sum(1 for item in self.dados.get('ufmg', []) if item.get('pdf_extraido'))
        fapemig_pdfs = sum(1 for item in self.dados.get('fapemig', []) if item.get('pdf_extraido'))
        cnpq_pdfs = sum(1 for item in self.dados.get('cnpq', []) if item.get('pdf_extraido'))
        
        # Estatísticas dos PDFs
        total_paginas = 0
        total_caracteres = 0
        idiomas = {'português': 0, 'inglês': 0, 'misto': 0, 'desconhecido': 0}
        
        for fonte in ['ufmg', 'fapemig', 'cnpq']:
            for item in self.dados.get(fonte, []):
                if item.get('pdf_extraido'):
                    if item.get('pdf_estatisticas'):
                        total_paginas += item.get('pdf_estatisticas', {}).get('total_linhas', 0) // 50
                        total_caracteres += item.get('pdf_estatisticas', {}).get('total_caracteres', 0)
                    if item.get('pdf_idioma'):
                        idiomas[item.get('pdf_idioma')] = idiomas.get(item.get('pdf_idioma'), 0) + 1
        
        formatted = f"""
📊 ESTATÍSTICAS COMPLETAS DOS PDFs EXTRAÍDOS:
   • Total de PDFs processados: {total_pdfs}
   • Total de PDFs com erro: {total_erros}
   • Taxa de sucesso: {((total_pdfs - total_erros) / total_pdfs * 100):.1f}%
   • Data de processamento: {data_processamento}
   • Versão do integrador: {versao}
   • Método utilizado: {metodo}

📄 DISTRIBUIÇÃO POR FONTE:
   • UFMG: {ufmg_pdfs} PDFs
   • FAPEMIG: {fapemig_pdfs} PDFs  
   • CNPq: {cnpq_pdfs} PDFs

📊 ANÁLISE DO CONTEÚDO:
   • Total de páginas estimado: {total_paginas}
   • Total de caracteres: {total_caracteres:,}
   • Idiomas detectados: {', '.join([f'{k}: {v}' for k, v in idiomas.items() if v > 0])}

🎯 BENEFÍCIOS DA EXTRAÇÃO ROBUSTA:
   • ✅ Captura de links diretos via Selenium
   • ✅ Download robusto com httpx e redirecionamentos
   • ✅ Cálculo de hash SHA256 para deduplicação
   • ✅ Validação de conteúdo e tipo
   • ✅ Fallbacks para OCR e múltiplos métodos
   • ✅ Normalização adequada de dados
   • ✅ Seleção inteligente de valores mais plausíveis
   • ✅ Preservação de todas as ocorrências encontradas
   • ✅ Campos link_pdf e pdf_hash incluídos
        """
        
        return formatted
    
    def _gerar_resumo_executivo_inteligente(self) -> str:
        """Gera resumo executivo inteligente dos dados"""
        total = self.dados.get('total_editais', 0)
        ufmg_count = len(self.dados.get('ufmg', []))
        fapemig_count = len(self.dados.get('fapemig', []))
        cnpq_count = len(self.dados.get('cnpq', []))
        
        # Contar PDFs extraídos
        total_pdfs = 0
        total_pdfs_com_erro = 0
        for fonte in ['ufmg', 'fapemig', 'cnpq']:
            for item in self.dados.get(fonte, []):
                if item.get('pdf_extraido'):
                    total_pdfs += 1
                if item.get('pdf_erro'):
                    total_pdfs_com_erro += 1
        
        # Contar campos enriquecidos
        campos_enriquecidos = 0
        for fonte in ['ufmg', 'fapemig', 'cnpq']:
            for item in self.dados.get(fonte, []):
                if any(item.get(f) for f in ['valor_selecionado', 'prazo_selecionado', 'objetivo_selecionado', 'area_selecionada']):
                    campos_enriquecidos += 1
        
        resumo = f"""
📈 ESTATÍSTICAS GERAIS:
   • Total de Oportunidades: {total}
   • UFMG: {ufmg_count} editais
   • FAPEMIG: {fapemig_count} oportunidades  
   • CNPq: {cnpq_count} chamadas
   • PDFs extraídos: {total_pdfs}
   • PDFs com erro: {total_pdfs_com_erro}
   • Campos enriquecidos: {campos_enriquecidos}

🎯 PRÓXIMOS PASSOS RECOMENDADOS:
   • Verificar prazos de inscrição (selecionados automaticamente)
   • Analisar valores e recursos disponíveis (mais plausíveis identificados)
   • Identificar oportunidades mais relevantes
   • Preparar documentação necessária
   • Acessar PDFs originais via links diretos fornecidos

💡 DICAS IMPORTANTES:
   • Sempre verifique os links originais fornecidos
   • Confirme datas e prazos selecionados automaticamente
   • Prepare documentos com antecedência
   • Entre em contato em caso de dúvidas
   • PDFs extraídos fornecem informações complementares completas
   • Hash SHA256 permite verificar integridade dos documentos

🚀 NOVIDADES DO SISTEMA ROBUSTO:
   • ✅ Captura automática de links diretos de PDFs
   • ✅ Download robusto com múltiplos fallbacks
   • ✅ Extração de texto com OCR quando necessário
   • ✅ Seleção inteligente de valores mais plausíveis
   • ✅ Preservação de todas as informações encontradas
   • ✅ Normalização adequada de dados
   • ✅ Cálculo de hash para deduplicação
   • ✅ Tratamento robusto de erros
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
    """Teste do gerador de resumos completo"""
    # Dados de exemplo com PDFs extraídos robustamente
    dados_exemplo = {
        'ufmg': [
            {
                'titulo': 'Edital PROEX nº 08/2025 – Programa de Apoio Integrado a Eventos',
                'data': '15/08/2025',
                'valor': 'Valor não informado',
                'url': 'https://exemplo.com/edital1.pdf',
                'pdf_extraido': True,
                'pdf_hash': 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6',
                'pdf_link_direto': 'https://exemplo.com/edital1_direto.pdf',
                'pdf_status_baixa': 'ok',
                'pdf_status_analise': 'ok',
                'pdf_tamanho_bytes': 1500000,
                'pdf_idioma': 'português',
                'valor_selecionado': 'R$ 5.000,00',
                'valor_fonte': 'PDF extraído (seleção inteligente)',
                'prazo_selecionado': '30/09/2025',
                'prazo_fonte': 'PDF extraído (seleção inteligente)',
                'objetivo_selecionado': 'Apoiar eventos acadêmicos e científicos de excelência que contribuam para o desenvolvimento da pesquisa e inovação no país',
                'objetivo_fonte': 'PDF extraído (seleção inteligente)',
                'todos_valores_encontrados': ['R$ 5.000,00', 'R$ 3.000,00', 'R$ 2.000,00'],
                'todos_prazos_encontrados': ['30/09/2025', '15/10/2025'],
                'todos_objetivos_encontrados': [
                    'Apoiar eventos acadêmicos e científicos de excelência que contribuam para o desenvolvimento da pesquisa e inovação no país',
                    'Fomentar a participação de estudantes em eventos científicos',
                    'Promover a divulgação científica'
                ],
                'pdf_estatisticas': {
                    'total_caracteres': 25000,
                    'total_palavras': 5000,
                    'total_linhas': 500
                }
            }
        ],
        'fapemig': [
            {
                'titulo': 'CHAMADA FAPEMIG 011/2025 - DEEP TECH - INSERÇÃO NO MERCADO E INOVAÇÃO',
                'valor': 'Valor não informado',
                'url': 'https://exemplo.com/chamada1.pdf',
                'pdf_extraido': True,
                'pdf_hash': 'b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7',
                'pdf_link_direto': 'https://exemplo.com/chamada1_direto.pdf',
                'pdf_status_baixa': 'ok',
                'pdf_status_analise': 'ok',
                'pdf_tamanho_bytes': 2000000,
                'pdf_idioma': 'português',
                'valor_selecionado': 'R$ 50.000,00',
                'valor_fonte': 'PDF extraído (seleção inteligente)',
                'prazo_selecionado': '15/10/2025',
                'prazo_fonte': 'PDF extraído (seleção inteligente)',
                'todos_valores_encontrados': ['R$ 50.000,00', 'R$ 25.000,00'],
                'todos_prazos_encontrados': ['15/10/2025', '30/10/2025'],
                'pdf_estatisticas': {
                    'total_caracteres': 30000,
                    'total_palavras': 6000,
                    'total_linhas': 600
                }
            }
        ],
        'cnpq': [
            {
                'titulo': 'CHAMADA ERC- CNPQ - 2025 Nº 13/2025',
                'periodo_inscricao': 'Período não encontrado',
                'url_detalhes': 'https://exemplo.com/cnpq1.pdf',
                'pdf_extraido': True,
                'pdf_hash': 'c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8',
                'pdf_link_direto': 'https://exemplo.com/cnpq1_direto.pdf',
                'pdf_status_baixa': 'ok',
                'pdf_status_analise': 'ok',
                'pdf_tamanho_bytes': 1800000,
                'pdf_idioma': 'português',
                'prazo_selecionado': '30/09/2025',
                'prazo_fonte': 'PDF extraído (seleção inteligente)',
                'todos_prazos_encontrados': ['30/09/2025', '15/10/2025'],
                'pdf_estatisticas': {
                    'total_caracteres': 28000,
                    'total_palavras': 5600,
                    'total_linhas': 560
                }
            }
        ],
        'total_editais': 3,
        'pdf_metadata': {
            'data_processamento': '2025-01-16T10:30:00',
            'total_pdfs_processados': 3,
            'total_pdfs_com_erro': 0,
            'versao_integrador': '2.0.0',
            'metodo': 'integracao_robusta'
        }
    }
    
    gerador = GeradorResumoCompleto(dados_exemplo)
    resumo = gerador.gerar_resumo_completo()
    
    print(resumo)

if __name__ == "__main__":
    main()
