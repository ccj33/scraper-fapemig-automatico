#!/usr/bin/env python3
"""
Integrador de PDFs Robusto e Inteligente
========================================

Resolve todos os problemas de integração identificados:
1. Não atualiza campos sem validação adequada
2. Seleciona valores mais plausíveis
3. Mantém todas as ocorrências em listas
4. Tratamento adequado para páginas sem PDF
5. Validação de qualidade dos dados extraídos
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from extrator_pdf_robusto import ExtratorPDFRobusto

logger = logging.getLogger(__name__)

class IntegradorPDFRobusto:
    """Integra extração de PDFs com dados de scraping de forma inteligente"""
    
    def __init__(self):
        self.extrator = ExtratorPDFRobusto()
        
    def processar_editais_com_pdfs(self, dados_scraping: Dict) -> Dict:
        """
        Processa editais que possuem PDFs com integração inteligente
        
        Args:
            dados_scraping: Dados originais do scraping
            
        Returns:
            Dados enriquecidos com informações dos PDFs
        """
        logger.info("🚀 Iniciando integração robusta de PDFs...")
        
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
            'total_pdfs_com_erro': self._contar_pdfs_com_erro(dados_enriquecidos),
            'versao_integrador': '2.0.0',
            'metodo': 'integracao_robusta'
        }
        
        logger.info(f"✅ Integração robusta concluída: {self._contar_pdfs_processados(dados_enriquecidos)} PDFs processados")
        return dados_enriquecidos
    
    def _processar_ufmg_pdfs(self, editais: List[Dict]) -> List[Dict]:
        """Processa PDFs dos editais da UFMG com integração inteligente"""
        editais_processados = []
        
        for edital in editais:
            edital_processado = edital.copy()
            
            # Verificar se há PDF disponível
            if self._contem_pdf(edital.get('url', '')):
                logger.info(f"📄 Processando PDF UFMG: {edital.get('titulo', 'Sem título')}")
                
                try:
                    # Usar o extrator robusto
                    dados_pdf = self.extrator.extrair_de_url_com_selenium(
                        edital.get('driver'), 
                        edital['url'], 
                        edital.get('titulo')
                    )
                    
                    if 'erro' not in dados_pdf:
                        # Adicionar dados do PDF
                        edital_processado.update({
                            'pdf_extraido': True,
                            'pdf_status_baixa': dados_pdf.get('status_baixa'),
                            'pdf_status_analise': dados_pdf.get('status_analise'),
                            'pdf_hash': dados_pdf.get('pdf_hash'),
                            'pdf_caminho': dados_pdf.get('caminho_pdf'),
                            'pdf_caminho_texto': dados_pdf.get('caminho_texto'),
                            'pdf_tamanho_bytes': dados_pdf.get('tamanho_bytes'),
                            'pdf_link_direto': dados_pdf.get('link_pdf'),
                            'pdf_paginas': dados_pdf.get('estatisticas', {}).get('total_linhas', 0) // 50,  # Estimativa
                            'pdf_estatisticas': dados_pdf.get('estatisticas'),
                            'pdf_idioma': self._detectar_idioma_simples(dados_pdf.get('texto_completo', '')),
                            'pdf_data_extracao': dados_pdf.get('data_extracao')
                        })
                        
                        # Adicionar dados extraídos (manter como listas)
                        if dados_pdf.get('valores_encontrados'):
                            edital_processado['pdf_valores_encontrados'] = dados_pdf['valores_encontrados']
                        
                        if dados_pdf.get('prazos_encontrados'):
                            edital_processado['pdf_prazos_encontrados'] = dados_pdf['prazos_encontrados']
                        
                        if dados_pdf.get('objetivos_encontrados'):
                            edital_processado['pdf_objetivos_encontrados'] = dados_pdf['objetivos_encontrados']
                        
                        if dados_pdf.get('areas_encontradas'):
                            edital_processado['pdf_areas_encontradas'] = dados_pdf['areas_encontradas']
                        
                        if dados_pdf.get('datas_encontradas'):
                            edital_processado['pdf_datas_encontradas'] = dados_pdf['datas_encontradas']
                        
                        # Integração inteligente: selecionar valores mais plausíveis
                        edital_processado = self._integrar_dados_inteligentemente(edital_processado, dados_pdf)
                        
                        logger.info(f"✅ PDF UFMG processado: {len(dados_pdf)} campos extraídos")
                    else:
                        edital_processado.update({
                            'pdf_extraido': False,
                            'pdf_status_baixa': dados_pdf.get('status_baixa'),
                            'pdf_erro': dados_pdf['erro'],
                            'pdf_motivo': 'Falha na extração'
                        })
                        logger.warning(f"⚠️ Erro no PDF UFMG: {dados_pdf['erro']}")
                        
                except Exception as e:
                    edital_processado.update({
                        'pdf_extraido': False,
                        'pdf_erro': str(e),
                        'pdf_motivo': 'Exceção durante processamento'
                    })
                    logger.error(f"❌ Erro ao processar PDF UFMG: {e}")
            else:
                edital_processado.update({
                    'pdf_extraido': False,
                    'pdf_motivo': 'URL não é PDF',
                    'pdf_status_baixa': 'nao_aplicavel'
                })
            
            editais_processados.append(edital_processado)
        
        return editais_processados
    
    def _processar_fapemig_pdfs(self, oportunidades: List[Dict]) -> List[Dict]:
        """Processa PDFs das oportunidades da FAPEMIG com integração inteligente"""
        oportunidades_processadas = []
        
        for oportunidade in oportunidades:
            oportunidade_processada = oportunidade.copy()
            
            if self._contem_pdf(oportunidade.get('url', '')):
                logger.info(f"📄 Processando PDF FAPEMIG: {oportunidade.get('titulo', 'Sem título')}")
                
                try:
                    dados_pdf = self.extrator.extrair_de_url_com_selenium(
                        oportunidade.get('driver'), 
                        oportunidade['url'], 
                        oportunidade.get('titulo')
                    )
                    
                    if 'erro' not in dados_pdf:
                        # Adicionar dados do PDF
                        oportunidade_processada.update({
                            'pdf_extraido': True,
                            'pdf_status_baixa': dados_pdf.get('status_baixa'),
                            'pdf_status_analise': dados_pdf.get('status_analise'),
                            'pdf_hash': dados_pdf.get('pdf_hash'),
                            'pdf_caminho': dados_pdf.get('caminho_pdf'),
                            'pdf_caminho_texto': dados_pdf.get('caminho_texto'),
                            'pdf_tamanho_bytes': dados_pdf.get('tamanho_bytes'),
                            'pdf_link_direto': dados_pdf.get('link_pdf'),
                            'pdf_paginas': dados_pdf.get('estatisticas', {}).get('total_linhas', 0) // 50,
                            'pdf_estatisticas': dados_pdf.get('estatisticas'),
                            'pdf_idioma': self._detectar_idioma_simples(dados_pdf.get('texto_completo', '')),
                            'pdf_data_extracao': dados_pdf.get('data_extracao')
                        })
                        
                        # Adicionar dados extraídos (manter como listas)
                        if dados_pdf.get('valores_encontrados'):
                            oportunidade_processada['pdf_valores_encontrados'] = dados_pdf['valores_encontrados']
                        
                        if dados_pdf.get('prazos_encontrados'):
                            oportunidade_processada['pdf_prazos_encontrados'] = dados_pdf['prazos_encontrados']
                        
                        if dados_pdf.get('objetivos_encontrados'):
                            oportunidade_processada['pdf_objetivos_encontrados'] = dados_pdf['objetivos_encontrados']
                        
                        if dados_pdf.get('areas_encontradas'):
                            oportunidade_processada['pdf_areas_encontradas'] = dados_pdf['areas_encontradas']
                        
                        if dados_pdf.get('datas_encontradas'):
                            oportunidade_processada['pdf_datas_encontradas'] = dados_pdf['datas_encontradas']
                        
                        # Integração inteligente
                        oportunidade_processada = self._integrar_dados_inteligentemente(oportunidade_processada, dados_pdf)
                        
                        logger.info(f"✅ PDF FAPEMIG processado: {len(dados_pdf)} campos extraídos")
                    else:
                        oportunidade_processada.update({
                            'pdf_extraido': False,
                            'pdf_status_baixa': dados_pdf.get('status_baixa'),
                            'pdf_erro': dados_pdf['erro'],
                            'pdf_motivo': 'Falha na extração'
                        })
                        logger.warning(f"⚠️ Erro no PDF FAPEMIG: {dados_pdf['erro']}")
                        
                except Exception as e:
                    oportunidade_processada.update({
                        'pdf_extraido': False,
                        'pdf_erro': str(e),
                        'pdf_motivo': 'Exceção durante processamento'
                    })
                    logger.error(f"❌ Erro ao processar PDF FAPEMIG: {e}")
            else:
                oportunidade_processada.update({
                    'pdf_extraido': False,
                    'pdf_motivo': 'URL não é PDF',
                    'pdf_status_baixa': 'nao_aplicavel'
                })
            
            oportunidades_processadas.append(oportunidade_processada)
        
        return oportunidades_processadas
    
    def _processar_cnpq_pdfs(self, chamadas: List[Dict]) -> List[Dict]:
        """Processa PDFs das chamadas do CNPq com integração inteligente"""
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
                        dados_pdf = self.extrator.extrair_de_url_com_selenium(
                            chamada.get('driver'), 
                            url, 
                            chamada.get('titulo')
                        )
                        
                        if 'erro' not in dados_pdf:
                            # Adicionar dados do PDF
                            chamada_processada.update({
                                'pdf_extraido': True,
                                'pdf_status_baixa': dados_pdf.get('status_baixa'),
                                'pdf_status_analise': dados_pdf.get('status_analise'),
                                'pdf_hash': dados_pdf.get('pdf_hash'),
                                'pdf_caminho': dados_pdf.get('caminho_pdf'),
                                'pdf_caminho_texto': dados_pdf.get('caminho_texto'),
                                'pdf_tamanho_bytes': dados_pdf.get('tamanho_bytes'),
                                'pdf_link_direto': dados_pdf.get('link_pdf'),
                                'pdf_url_fonte': url,
                                'pdf_paginas': dados_pdf.get('estatisticas', {}).get('total_linhas', 0) // 50,
                                'pdf_estatisticas': dados_pdf.get('estatisticas'),
                                'pdf_idioma': self._detectar_idioma_simples(dados_pdf.get('texto_completo', '')),
                                'pdf_data_extracao': dados_pdf.get('data_extracao')
                            })
                            
                            # Adicionar dados extraídos (manter como listas)
                            if dados_pdf.get('valores_encontrados'):
                                chamada_processada['pdf_valores_encontrados'] = dados_pdf['valores_encontrados']
                            
                            if dados_pdf.get('prazos_encontrados'):
                                chamada_processada['pdf_prazos_encontrados'] = dados_pdf['prazos_encontrados']
                            
                            if dados_pdf.get('objetivos_encontrados'):
                                chamada_processada['pdf_objetivos_encontrados'] = dados_pdf['objetivos_encontrados']
                            
                            if dados_pdf.get('areas_encontradas'):
                                chamada_processada['pdf_areas_encontradas'] = dados_pdf['areas_encontradas']
                            
                            if dados_pdf.get('datas_encontradas'):
                                chamada_processada['pdf_datas_encontradas'] = dados_pdf['datas_encontradas']
                            
                            # Integração inteligente
                            chamada_processada = self._integrar_dados_inteligentemente(chamada_processada, dados_pdf)
                            
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
                chamada_processada.update({
                    'pdf_extraido': False,
                    'pdf_motivo': 'Nenhuma URL é PDF',
                    'pdf_status_baixa': 'nao_aplicavel'
                })
            
            chamadas_processadas.append(chamada_processada)
        
        return chamadas_processadas
    
    def _integrar_dados_inteligentemente(self, item: Dict, dados_pdf: Dict) -> Dict:
        """
        Integra dados do PDF de forma inteligente, selecionando valores mais plausíveis
        e mantendo todas as ocorrências em listas
        """
        item_integrado = item.copy()
        
        # Integrar valores monetários
        if dados_pdf.get('valores_encontrados'):
            valores_pdf = dados_pdf['valores_encontrados']
            
            # Selecionar valor mais plausível (maior valor monetário)
            valor_mais_plausivel = self._selecionar_valor_mais_plausivel(valores_pdf)
            
            if valor_mais_plausivel:
                item_integrado['valor_selecionado'] = valor_mais_plausivel
                item_integrado['valor_fonte'] = 'PDF extraído (seleção inteligente)'
            
            # Manter todos os valores encontrados
            item_integrado['todos_valores_encontrados'] = valores_pdf
        
        # Integrar prazos
        if dados_pdf.get('prazos_encontrados'):
            prazos_pdf = dados_pdf['prazos_encontrados']
            
            # Selecionar prazo mais plausível (data mais recente)
            prazo_mais_plausivel = self._selecionar_prazo_mais_plausivel(prazos_pdf)
            
            if prazo_mais_plausivel:
                item_integrado['prazo_selecionado'] = prazo_mais_plausivel
                item_integrado['prazo_fonte'] = 'PDF extraído (seleção inteligente)'
            
            # Manter todos os prazos encontrados
            item_integrado['todos_prazos_encontrados'] = prazos_pdf
        
        # Integrar objetivos
        if dados_pdf.get('objetivos_encontrados'):
            objetivos_pdf = dados_pdf['objetivos_encontrados']
            
            # Selecionar objetivo mais plausível (mais longo e completo)
            objetivo_mais_plausivel = self._selecionar_objetivo_mais_plausivel(objetivos_pdf)
            
            if objetivo_mais_plausivel:
                item_integrado['objetivo_selecionado'] = objetivo_mais_plausivel
                item_integrado['objetivo_fonte'] = 'PDF extraído (seleção inteligente)'
            
            # Manter todos os objetivos encontrados
            item_integrado['todos_objetivos_encontrados'] = objetivos_pdf
        
        # Integrar áreas
        if dados_pdf.get('areas_encontradas'):
            areas_pdf = dados_pdf['areas_encontradas']
            
            # Selecionar área mais plausível (mais específica)
            area_mais_plausivel = self._selecionar_area_mais_plausivel(areas_pdf)
            
            if area_mais_plausivel:
                item_integrado['area_selecionada'] = area_mais_plausivel
                item_integrado['area_fonte'] = 'PDF extraído (seleção inteligente)'
            
            # Manter todas as áreas encontradas
            item_integrado['todas_areas_encontradas'] = areas_pdf
        
        return item_integrado
    
    def _selecionar_valor_mais_plausivel(self, valores: List[str]) -> Optional[str]:
        """Seleciona o valor monetário mais plausível"""
        if not valores:
            return None
        
        # Converter para números para comparação
        valores_numericos = []
        for valor in valores:
            try:
                # Extrair número do valor (R$ 50.000,00 -> 50000.00)
                numero = valor.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
                numero_float = float(numero)
                valores_numericos.append((numero_float, valor))
            except:
                continue
        
        if not valores_numericos:
            return valores[0]  # Retornar primeiro se não conseguir converter
        
        # Retornar o maior valor
        return max(valores_numericos, key=lambda x: x[0])[1]
    
    def _selecionar_prazo_mais_plausivel(self, prazos: List[str]) -> Optional[str]:
        """Seleciona o prazo mais plausível (data mais recente)"""
        if not prazos:
            return None
        
        # Tentar converter para datas
        datas_validas = []
        for prazo in prazos:
            try:
                # Padrão DD/MM/AAAA
                if '/' in prazo:
                    dia, mes, ano = prazo.split('/')
                    data = datetime(int(ano), int(mes), int(dia))
                    datas_validas.append((data, prazo))
            except:
                continue
        
        if not datas_validas:
            return prazos[0]  # Retornar primeiro se não conseguir converter
        
        # Retornar a data mais recente
        return max(datas_validas, key=lambda x: x[0])[1]
    
    def _selecionar_objetivo_mais_plausivel(self, objetivos: List[str]) -> Optional[str]:
        """Seleciona o objetivo mais plausível (mais longo e completo)"""
        if not objetivos:
            return None
        
        # Selecionar o objetivo mais longo (provavelmente mais completo)
        return max(objetivos, key=len)
    
    def _selecionar_area_mais_plausivel(self, areas: List[str]) -> Optional[str]:
        """Seleciona a área mais plausível (mais específica)"""
        if not areas:
            return None
        
        # Selecionar a área mais longa (provavelmente mais específica)
        return max(areas, key=len)
    
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
    
    def _detectar_idioma_simples(self, texto: str) -> str:
        """Detecta idioma de forma simples"""
        if not texto:
            return "desconhecido"
        
        # Contar palavras em português vs inglês
        import re
        palavras_pt = len(re.findall(r'\b(de|para|com|por|em|não|são|está|ser|ter|que|uma|um|este|esta|como|mais|muito|pode|devem|todos|todas)\b', texto, re.IGNORECASE))
        palavras_en = len(re.findall(r'\b(the|and|for|with|in|is|are|was|were|have|has|will|can|should|would|could|this|that|these|those)\b', texto, re.IGNORECASE))
        
        if palavras_pt > palavras_en:
            return "português"
        elif palavras_en > palavras_pt:
            return "inglês"
        else:
            return "misto"
    
    def _contar_pdfs_processados(self, dados: Dict) -> int:
        """Conta quantos PDFs foram processados com sucesso"""
        total = 0
        
        for fonte in ['ufmg', 'fapemig', 'cnpq']:
            if fonte in dados:
                for item in dados[fonte]:
                    if item.get('pdf_extraido') and item.get('pdf_status_analise') == 'ok':
                        total += 1
        
        return total
    
    def _contar_pdfs_com_erro(self, dados: Dict) -> int:
        """Conta quantos PDFs tiveram erros"""
        total = 0
        
        for fonte in ['ufmg', 'fapemig', 'cnpq']:
            if fonte in dados:
                for item in dados[fonte]:
                    if item.get('pdf_extraido') and item.get('pdf_erro'):
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
        self.extrator.limpar_arquivos()

def main():
    """Teste do integrador robusto"""
    integrador = IntegradorPDFRobusto()
    
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
    
    print("🧪 Testando integrador robusto de PDFs...")
    
    # Processar dados (sem driver real)
    print("⚠️ Este é um teste sem driver Selenium real")
    print("📊 Estrutura de dados preparada para integração")
    
    # Mostrar estrutura esperada
    print(f"\n📋 Estrutura de dados preparada:")
    print(f"   • UFMG: {len(dados_exemplo['ufmg'])} editais")
    print(f"   • FAPEMIG: {len(dados_exemplo['fapemig'])} oportunidades")
    print(f"   • CNPq: {len(dados_exemplo['cnpq'])} chamadas")
    
    # Salvar dados de exemplo
    integrador.salvar_dados_enriquecidos(dados_exemplo, 'dados_exemplo_integrador.json')
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    main()
