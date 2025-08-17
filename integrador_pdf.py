#!/usr/bin/env python3
"""
Integrador de PDFs com Sistema de Scraping
==========================================

Integra a extração de PDFs com o sistema de scraping existente
"""

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from extrator_pdf import ExtratorPDF

logger = logging.getLogger(__name__)

class IntegradorPDF:
    """Integra extração de PDFs com dados de scraping"""
    
    def __init__(self):
        self.extrator = ExtratorPDF()
        
    def processar_editais_com_pdfs(self, dados_scraping: Dict) -> Dict:
        """
        Processa editais que possuem PDFs e extrai dados adicionais
        
        Args:
            dados_scraping: Dados originais do scraping
            
        Returns:
            Dados enriquecidos com informações dos PDFs
        """
        logger.info("🚀 Iniciando integração de PDFs...")
        
        dados_enriquecidos = dados_scraping.copy()
        
        # Processar UFMG
        if 'ufmg' in dados_enriquecidos:
            dados_enriquecidos['ufmg'] = self._processar_ufmg_pdfs(dados_enriquecidos['ufmg'])
        
        # Processar FAPEMIG
        if 'fapemig' in dados_enriquecidos:
            dados_enriquecidos['fapemig'] = self._processar_fapemig_pdfs(dados_enriquecidos['fapemig'])
        
        # Processar CNPq
        if 'cnpq' in dados_enriquecidos:
            dados_enriquecidos['cnpq'] = self._processar_cnpq_pdfs(dados_enriquecidos['cnpq'])
        
        # Adicionar metadados de processamento
        dados_enriquecidos['pdf_metadata'] = {
            'data_processamento': datetime.now().isoformat(),
            'total_pdfs_processados': self._contar_pdfs_processados(dados_enriquecidos),
            'versao_integrador': '1.0.0'
        }
        
        logger.info(f"✅ Integração concluída: {self._contar_pdfs_processados(dados_enriquecidos)} PDFs processados")
        return dados_enriquecidos
    
    def _processar_ufmg_pdfs(self, editais: List[Dict]) -> List[Dict]:
        """Processa PDFs dos editais da UFMG"""
        editais_processados = []
        
        for edital in editais:
            edital_processado = edital.copy()
            
            if self._contem_pdf(edital.get('url', '')):
                logger.info(f"📄 Processando PDF UFMG: {edital.get('titulo', 'Sem título')}")
                
                try:
                    dados_pdf = self.extrator.extrair_de_url(edital['url'])
                    
                    if 'erro' not in dados_pdf:
                        edital_processado.update({
                            'pdf_extraido': True,
                            'pdf_paginas': dados_pdf.get('num_paginas'),
                            'pdf_tamanho': dados_pdf.get('tamanho_bytes'),
                            'pdf_valores_encontrados': dados_pdf.get('valores_encontrados'),
                            'pdf_prazos_encontrados': dados_pdf.get('prazos_encontrados'),
                            'pdf_objetivos_encontrados': dados_pdf.get('objetivos_encontrados'),
                            'pdf_areas_encontradas': dados_pdf.get('areas_encontradas'),
                            'pdf_datas_encontradas': dados_pdf.get('datas_encontradas'),
                            'pdf_estatisticas': dados_pdf.get('estatisticas'),
                            'pdf_idioma': dados_pdf.get('idioma_detectado'),
                            'pdf_arquivo_local': dados_pdf.get('arquivo_local'),
                            'pdf_resumo_conteudo': dados_pdf.get('resumo_conteudo')
                        })
                        
                        # Enriquecer dados existentes se não estiverem disponíveis
                        if not edital_processado.get('valor') or edital_processado['valor'] == "Valor não informado":
                            if dados_pdf.get('valores_encontrados') and len(dados_pdf['valores_encontrados']) > 0:
                                edital_processado['valor'] = dados_pdf['valores_encontrados'][0]
                                edital_processado['valor_fonte'] = 'PDF extraído'
                        
                        if not edital_processado.get('prazo') or edital_processado['prazo'] == "Prazo não informado":
                            if dados_pdf.get('prazos_encontrados') and len(dados_pdf['prazos_encontrados']) > 0:
                                edital_processado['prazo'] = dados_pdf['prazos_encontrados'][0]
                                edital_processado['prazo_fonte'] = 'PDF extraído'
                        
                        if not edital_processado.get('objetivo') or edital_processado['objetivo'] == "Objetivo não informado":
                            if dados_pdf.get('objetivos_encontrados') and len(dados_pdf['objetivos_encontrados']) > 0:
                                edital_processado['objetivo'] = dados_pdf['objetivos_encontrados'][0]
                                edital_processado['objetivo_fonte'] = 'PDF extraído'
                        
                        logger.info(f"✅ PDF UFMG processado: {len(dados_pdf)} campos extraídos")
                    else:
                        edital_processado['pdf_erro'] = dados_pdf['erro']
                        logger.warning(f"⚠️ Erro no PDF UFMG: {dados_pdf['erro']}")
                        
                except Exception as e:
                    edital_processado['pdf_erro'] = str(e)
                    logger.error(f"❌ Erro ao processar PDF UFMG: {e}")
            else:
                edital_processado['pdf_extraido'] = False
                edital_processado['pdf_motivo'] = 'URL não é PDF'
            
            editais_processados.append(edital_processado)
        
        return editais_processados
    
    def _processar_fapemig_pdfs(self, oportunidades: List[Dict]) -> List[Dict]:
        """Processa PDFs das oportunidades da FAPEMIG"""
        oportunidades_processadas = []
        
        for oportunidade in oportunidades:
            oportunidade_processada = oportunidade.copy()
            
            if self._contem_pdf(oportunidade.get('url', '')):
                logger.info(f"📄 Processando PDF FAPEMIG: {oportunidade.get('titulo', 'Sem título')}")
                
                try:
                    dados_pdf = self.extrator.extrair_de_url(oportunidade['url'])
                    
                    if 'erro' not in dados_pdf:
                        oportunidade_processada.update({
                            'pdf_extraido': True,
                            'pdf_paginas': dados_pdf.get('num_paginas'),
                            'pdf_tamanho': dados_pdf.get('tamanho_bytes'),
                            'pdf_valores_encontrados': dados_pdf.get('valores_encontrados'),
                            'pdf_prazos_encontrados': dados_pdf.get('prazos_encontrados'),
                            'pdf_objetivos_encontrados': dados_pdf.get('objetivos_encontrados'),
                            'pdf_areas_encontradas': dados_pdf.get('areas_encontradas'),
                            'pdf_datas_encontradas': dados_pdf.get('datas_encontradas'),
                            'pdf_estatisticas': dados_pdf.get('estatisticas'),
                            'pdf_idioma': dados_pdf.get('idioma_detectado'),
                            'pdf_arquivo_local': dados_pdf.get('arquivo_local'),
                            'pdf_resumo_conteudo': dados_pdf.get('resumo_conteudo')
                        })
                        
                        # Enriquecer dados existentes
                        if not oportunidade_processada.get('valor') or oportunidade_processada['valor'] == "Valor não informado":
                            if dados_pdf.get('valores_encontrados') and len(dados_pdf['valores_encontrados']) > 0:
                                oportunidade_processada['valor'] = dados_pdf['valores_encontrados'][0]
                                oportunidade_processada['valor_fonte'] = 'PDF extraído'
                        
                        if not oportunidade_processada.get('prazo') or oportunidade_processada['prazo'] == "Prazo não informado":
                            if dados_pdf.get('prazos_encontrados') and len(dados_pdf['prazos_encontrados']) > 0:
                                oportunidade_processada['prazo'] = dados_pdf['prazos_encontrados'][0]
                                oportunidade_processada['prazo_fonte'] = 'PDF extraído'
                        
                        logger.info(f"✅ PDF FAPEMIG processado: {len(dados_pdf)} campos extraídos")
                    else:
                        oportunidade_processada['pdf_erro'] = dados_pdf['erro']
                        logger.warning(f"⚠️ Erro no PDF FAPEMIG: {dados_pdf['erro']}")
                        
                except Exception as e:
                    oportunidade_processada['pdf_erro'] = str(e)
                    logger.error(f"❌ Erro ao processar PDF FAPEMIG: {e}")
            else:
                oportunidade_processada['pdf_extraido'] = False
                oportunidade_processada['pdf_motivo'] = 'URL não é PDF'
            
            oportunidades_processadas.append(oportunidade_processada)
        
        return oportunidades_processadas
    
    def _processar_cnpq_pdfs(self, chamadas: List[Dict]) -> List[Dict]:
        """Processa PDFs das chamadas do CNPq"""
        chamadas_processadas = []
        
        for chamada in chamadas:
            chamada_processada = chamada.copy()
            
            # CNPq pode ter URLs de detalhes que são PDFs
            urls_para_verificar = [
                chamada.get('url_detalhes', ''),
                chamada.get('url', '')
            ]
            
            pdf_encontrado = False
            for url in urls_para_verificar:
                if url and self._contem_pdf(url):
                    logger.info(f"📄 Processando PDF CNPq: {chamada.get('titulo', 'Sem título')}")
                    
                    try:
                        dados_pdf = self.extrator.extrair_de_url(url)
                        
                        if 'erro' not in dados_pdf:
                            chamada_processada.update({
                                'pdf_extraido': True,
                                'pdf_url_fonte': url,
                                'pdf_paginas': dados_pdf.get('num_paginas'),
                                'pdf_tamanho': dados_pdf.get('tamanho_bytes'),
                                'pdf_valores_encontrados': dados_pdf.get('valores_encontrados'),
                                'pdf_prazos_encontrados': dados_pdf.get('prazos_encontrados'),
                                'pdf_objetivos_encontrados': dados_pdf.get('objetivos_encontrados'),
                                'pdf_areas_encontradas': dados_pdf.get('areas_encontradas'),
                                'pdf_datas_encontradas': dados_pdf.get('datas_encontradas'),
                                'pdf_estatisticas': dados_pdf.get('estatisticas'),
                                'pdf_idioma': dados_pdf.get('idioma_detectado'),
                                'pdf_arquivo_local': dados_pdf.get('arquivo_local'),
                                'pdf_resumo_conteudo': dados_pdf.get('resumo_conteudo')
                            })
                            
                            # Enriquecer dados existentes
                            if not chamada_processada.get('valor') or chamada_processada['valor'] == "Valor não informado":
                                if dados_pdf.get('valores_encontrados') and len(dados_pdf['valores_encontrados']) > 0:
                                    chamada_processada['valor'] = dados_pdf['valores_encontrados'][0]
                                    chamada_processada['valor_fonte'] = 'PDF extraído'
                            
                            if not chamada_processada.get('periodo_inscricao') or chamada_processada['periodo_inscricao'] == "Período não encontrado":
                                if dados_pdf.get('prazos_encontrados') and len(dados_pdf['prazos_encontrados']) > 0:
                                    chamada_processada['periodo_inscricao'] = dados_pdf['prazos_encontrados'][0]
                                    chamada_processada['periodo_fonte'] = 'PDF extraído'
                            
                            if not chamada_processada.get('descricao') or chamada_processada['descricao'] == "Descrição não informada":
                                if dados_pdf.get('objetivos_encontrados') and len(dados_pdf['objetivos_encontrados']) > 0:
                                    chamada_processada['descricao'] = dados_pdf['objetivos_encontrados'][0]
                                    chamada_processada['descricao_fonte'] = 'PDF extraído'
                            
                            logger.info(f"✅ PDF CNPq processado: {len(dados_pdf)} campos extraídos")
                            pdf_encontrado = True
                            break
                        else:
                            chamada_processada['pdf_erro'] = dados_pdf['erro']
                            logger.warning(f"⚠️ Erro no PDF CNPq: {dados_pdf['erro']}")
                            
                    except Exception as e:
                        chamada_processada['pdf_erro'] = str(e)
                        logger.error(f"❌ Erro ao processar PDF CNPq: {e}")
            
            if not pdf_encontrado:
                chamada_processada['pdf_extraido'] = False
                chamada_processada['pdf_motivo'] = 'Nenhuma URL é PDF'
            
            chamadas_processadas.append(chamada_processada)
        
        return chamadas_processadas
    
    def _contem_pdf(self, url: str) -> bool:
        """Verifica se a URL contém um PDF"""
        if not url:
            return False
        
        # Verificações básicas
        url_lower = url.lower()
        if '.pdf' in url_lower or 'pdf' in url_lower:
            return True
        
        # Verificar se é um link direto para PDF
        if any(ext in url_lower for ext in ['.pdf', 'application/pdf']):
            return True
        
        return False
    
    def _contar_pdfs_processados(self, dados: Dict) -> int:
        """Conta quantos PDFs foram processados com sucesso"""
        total = 0
        
        for fonte in ['ufmg', 'fapemig', 'cnpq']:
            if fonte in dados:
                for item in dados[fonte]:
                    if item.get('pdf_extraido') and 'erro' not in item:
                        total += 1
        
        return total
    
    def salvar_dados_enriquecidos(self, dados: Dict, caminho_arquivo: str):
        """Salva dados enriquecidos em arquivo JSON"""
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Dados enriquecidos salvos: {caminho_arquivo}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar dados: {e}")
    
    def limpar_arquivos_pdf(self):
        """Limpa arquivos PDF baixados"""
        self.extrator.limpar_arquivos_locais()

def main():
    """Teste do integrador de PDFs"""
    integrador = IntegradorPDF()
    
    # Dados de exemplo
    dados_exemplo = {
        'ufmg': [
            {
                'titulo': 'Edital PROEX nº 08/2025',
                'url': 'https://exemplo.com/edital1.pdf',
                'valor': 'Valor não informado'
            }
        ],
        'fapemig': [
            {
                'titulo': 'CHAMADA FAPEMIG 011/2025',
                'url': 'https://exemplo.com/chamada1.pdf',
                'prazo': 'Prazo não informado'
            }
        ],
        'cnpq': [
            {
                'titulo': 'CHAMADA ERC-CNPq 2025',
                'url_detalhes': 'https://exemplo.com/cnpq1.pdf'
            }
        ],
        'total_editais': 3
    }
    
    print("🧪 Testando integrador de PDFs...")
    
    # Processar dados
    dados_enriquecidos = integrador.processar_editais_com_pdfs(dados_exemplo)
    
    # Mostrar resultados
    print(f"\n📊 Total de PDFs processados: {dados_enriquecidos['pdf_metadata']['total_pdfs_processados']}")
    
    for fonte in ['ufmg', 'fapemig', 'cnpq']:
        if fonte in dados_enriquecidos:
            print(f"\n🔍 {fonte.upper()}:")
            for item in dados_enriquecidos[fonte]:
                print(f"  • {item['titulo']}")
                print(f"    PDF extraído: {item.get('pdf_extraido', False)}")
                if item.get('pdf_extraido'):
                    print(f"    Páginas: {item.get('pdf_paginas', 'N/A')}")
                    print(f"    Valor: {item.get('valor', 'N/A')}")
                    print(f"    Prazo: {item.get('prazo', 'N/A')}")
    
    # Salvar dados
    integrador.salvar_dados_enriquecidos(dados_enriquecidos, 'dados_enriquecidos_pdf.json')
    
    # Limpar arquivos
    integrador.limpar_arquivos_pdf()

if __name__ == "__main__":
    main()
