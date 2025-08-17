#!/usr/bin/env python3
"""
Scraper Robusto e Unificado para Editais e Chamadas
==================================================

Sistema completo que resolve todos os problemas críticos identificados:
1. Captura de links diretos via Selenium
2. Download robusto com httpx e redirecionamentos
3. Extração robusta de PDFs com múltiplos fallbacks
4. Integração inteligente de dados
5. Geração de resumos completos sem truncamento
6. Cálculo de hash SHA256 para deduplicação
7. Campos link_pdf e pdf_hash incluídos
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import chromedriver_autoinstaller
import logging
from typing import List, Dict, Optional, Tuple
import random

# Importar módulos robustos
from extrator_pdf_robusto import ExtratorPDFRobusto
from integrador_pdf_robusto import IntegradorPDFRobusto
from gerador_resumo_completo import GeradorResumoCompleto

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_robusto.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BaseScraperRobusto:
    """Classe base robusta para todos os scrapers"""
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.extrator_pdf = ExtratorPDFRobusto()
        
    def safe_find_element(self, by: By, value: str) -> Optional[webdriver.remote.webelement.WebElement]:
        """Encontra elemento de forma segura"""
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            return None
            
    def safe_find_elements(self, by: By, value: str) -> List[webdriver.remote.webelement.WebElement]:
        """Encontra elementos de forma segura"""
        try:
            return self.driver.find_elements(by, value)
        except NoSuchElementException:
            return []
            
    def safe_get_text(self, element) -> str:
        """Extrai texto de forma segura"""
        try:
            return element.text.strip()
        except:
            return ""
            
    def safe_get_attribute(self, element, attribute: str) -> str:
        """Extrai atributo de forma segura"""
        try:
            return element.get_attribute(attribute) or ""
        except:
            return ""
            
    def random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Delay aleatório para não sobrecarregar os sites"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def extrair_pdf_robusto(self, url: str, titulo: str) -> Dict:
        """Extrai PDF de forma robusta usando o extrator melhorado"""
        try:
            # Adicionar driver ao item para o extrator usar
            item_temp = {'driver': self.driver, 'url': url, 'titulo': titulo}
            
            # Usar o extrator robusto
            resultado = self.extrator_pdf.extrair_de_url_com_selenium(
                self.driver, url, titulo
            )
            
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro na extração robusta de PDF: {e}")
            return {
                'status_baixa': 'erro_critico',
                'erro': str(e),
                'url_origem': url,
                'data_extracao': datetime.now().isoformat()
            }

class UFMGScraperRobusto(BaseScraperRobusto):
    """Scraper robusto para UFMG - Editais e Chamadas"""
    
    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
        self.base_url = "https://www.ufmg.br/prograd/editais-chamadas/"
        
    def extract_editais(self) -> List[Dict]:
        """Extrai editais da UFMG com funcionalidades robustas"""
        logger.info("🚀 Iniciando extração robusta UFMG...")
        
        try:
            self.driver.get(self.base_url)
            self.random_delay(2, 4)
            
            editais = []
            page = 1
            
            while True:
                logger.info(f"📄 Processando página {page}...")
                
                # Extrair editais da página atual
                page_editais = self._extract_page_editais()
                editais.extend(page_editais)
                
                # Tentar ir para próxima página
                if not self._go_to_next_page():
                    break
                    
                page += 1
                self.random_delay(2, 4)
                
                # Limite de páginas para não sobrecarregar
                if page > 10:
                    logger.warning("⚠️ Limite de 10 páginas atingido")
                    break
                    
            logger.info(f"✅ UFMG: {len(editais)} editais extraídos")
            return editais
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair UFMG: {e}")
            return []
            
    def _extract_page_editais(self) -> List[Dict]:
        """Extrai editais de uma página específica com funcionalidades robustas"""
        editais = []
        
        try:
            # Procurar por links de editais (mais abrangente)
            edital_links = self.safe_find_elements(By.CSS_SELECTOR, 'a[href*="Edital"], a[href*="edital"], a[href*=".pdf"], a[href*=".doc"]')
            
            for link in edital_links:
                try:
                    titulo = self.safe_get_text(link)
                    href = self.safe_get_attribute(link, "href")
                    
                    if titulo and href and "edital" in titulo.lower():
                        # Procurar data próxima ao link
                        data = self._extract_date_near_link(link)
                        
                        # Extrair PDF de forma robusta se for um link de PDF
                        pdf_info = {}
                        if self._eh_url_pdf(href):
                            logger.info(f"📄 Extraindo PDF robusto: {titulo}")
                            pdf_info = self.extrair_pdf_robusto(href, titulo)
                        
                        edital = {
                            'titulo': titulo,
                            'url': href,
                            'data': data,
                            'fonte': 'UFMG',
                            'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'driver': self.driver  # Para o extrator usar
                        }
                        
                        # Adicionar informações do PDF se disponível
                        if pdf_info and 'erro' not in pdf_info:
                            edital.update({
                                'pdf_extraido': True,
                                'pdf_info': pdf_info
                            })
                        else:
                            edital.update({
                                'pdf_extraido': False,
                                'pdf_erro': pdf_info.get('erro', 'Falha na extração')
                            })
                        
                        editais.append(edital)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar link UFMG: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Erro ao extrair página UFMG: {e}")
            
        return editais
    
    def _eh_url_pdf(self, url: str) -> bool:
        """Verifica se a URL é um PDF"""
        if not url:
            return False
        
        url_lower = url.lower()
        return '.pdf' in url_lower or 'pdf' in url_lower
        
    def _extract_date_near_link(self, link_element) -> str:
        """Extrai data próxima ao link do edital"""
        try:
            # Procurar por texto com data próximo ao link
            parent = link_element.find_element(By.XPATH, "./..")
            parent_text = self.safe_get_text(parent)
            
            # Procurar padrões de data
            import re
            date_patterns = [
                r'\d{2}/\d{2}/\d{4}',
                r'\d{2}-\d{2}-\d{4}',
                r'\d{2}\.\d{2}\.\d{4}'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, parent_text)
                if match:
                    return match.group()
                    
        except:
            pass
            
        return "Data não encontrada"
        
    def _go_to_next_page(self) -> bool:
        """Tenta ir para a próxima página"""
        try:
            # Procurar por links de próxima página
            next_links = self.safe_find_elements(By.XPATH, '//a[contains(text(), "Próxima") or contains(text(), "»")]')
            
            for link in next_links:
                if link.is_enabled() and link.is_displayed():
                    link.click()
                    return True
                    
        except:
            pass
            
        return False

class FAPEMIGScraperRobusto(BaseScraperRobusto):
    """Scraper robusto para FAPEMIG - Oportunidades"""
    
    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
        self.base_url = "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/"
        
    def extract_chamadas(self) -> List[Dict]:
        """Extrai chamadas da FAPEMIG com funcionalidades robustas"""
        logger.info("🚀 Iniciando extração robusta FAPEMIG...")
        
        try:
            self.driver.get(self.base_url)
            self.random_delay(3, 5)
            
            chamadas = []
            
            # Extrair chamadas da página principal
            page_chamadas = self._extract_page_chamadas()
            chamadas.extend(page_chamadas)
            
            # Tentar expandir detalhes se possível
            chamadas = self._expand_chamadas_details(chamadas)
            
            logger.info(f"✅ FAPEMIG: {len(chamadas)} chamadas extraídas")
            return chamadas
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair FAPEMIG: {e}")
            return []
            
    def _extract_page_chamadas(self) -> List[Dict]:
        """Extrai chamadas da página principal com funcionalidades robustas"""
        chamadas = []
        titulos_processados = set()  # Para evitar duplicatas
        
        try:
            # Procurar por títulos de chamadas de forma mais abrangente
            titulos = self.safe_find_elements(By.CSS_SELECTOR, 'h1, h2, h3, h4, h5, h6, .chamada, .edital, .oportunidade')
            
            for titulo in titulos:
                try:
                    texto = self.safe_get_text(titulo)
                    
                    if texto and any(palavra in texto.lower() for palavra in ['chamada', 'edital', 'oportunidade', 'programa']):
                        # Verificar se já processamos este título
                        if texto in titulos_processados:
                            continue
                        titulos_processados.add(texto)
                        
                        # Procurar link associado de forma mais robusta
                        link = self._find_link_near_title(titulo)
                        
                        # Se não encontrou link próximo, procurar na página inteira
                        if not link:
                            link = self._find_link_by_title_text(texto)
                        
                        # Extrair contexto da página para obter mais informações
                        contexto = self._extract_context_around_title(titulo)
                        
                        chamada = {
                            'titulo': texto,
                            'url': link,
                            'contexto': contexto,
                            'fonte': 'FAPEMIG',
                            'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'driver': self.driver  # Para o extrator usar
                        }
                        
                        # Extrair PDF de forma robusta se for um link de PDF
                        if link and self._eh_url_pdf(link):
                            logger.info(f"📄 Extraindo PDF robusto FAPEMIG: {texto}")
                            pdf_info = self.extrair_pdf_robusto(link, texto)
                            
                            if 'erro' not in pdf_info:
                                chamada.update({
                                    'pdf_extraido': True,
                                    'pdf_info': pdf_info
                                })
                            else:
                                chamada.update({
                                    'pdf_extraido': False,
                                    'pdf_erro': pdf_info.get('erro', 'Falha na extração')
                                })
                        else:
                            chamada.update({
                                'pdf_extraido': False,
                                'pdf_motivo': 'Link não é PDF ou não disponível'
                            })
                        
                        chamadas.append(chamada)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar título FAPEMIG: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Erro ao extrair página FAPEMIG: {e}")
            
        return chamadas
    
    def _find_link_by_title_text(self, titulo_texto: str) -> str:
        """Encontra link baseado no texto do título"""
        try:
            # Procurar por links que contenham palavras do título
            palavras_chave = [palavra.lower() for palavra in titulo_texto.split() if len(palavra) > 3]
            
            links = self.safe_find_elements(By.TAG_NAME, "a")
            for link in links:
                href = self.safe_get_attribute(link, "href")
                texto_link = self.safe_get_text(link)
                
                if href and href.startswith("http"):
                    # Verificar se o link contém palavras-chave do título
                    for palavra in palavras_chave:
                        if palavra in texto_link.lower() or palavra in href.lower():
                            return href
                            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao procurar link por título: {e}")
            
        return ""
    
    def _extract_context_around_title(self, titulo_element) -> str:
        """Extrai contexto ao redor do título para obter mais informações"""
        try:
            # Procurar por parágrafo próximo ao título
            parent = titulo_element.find_element(By.XPATH, "./..")
            
            # Procurar por parágrafos próximos
            paragrafos = parent.find_elements(By.TAG_NAME, "p")
            if paragrafos:
                contexto = " ".join([p.text.strip() for p in paragrafos[:3] if p.text.strip()])
                if contexto:
                    return contexto
            
            # Se não encontrou parágrafos, procurar por divs com texto
            divs = parent.find_elements(By.TAG_NAME, "div")
            for div in divs[:3]:
                texto = div.text.strip()
                if texto and len(texto) > 20:  # Texto significativo
                    return texto
                    
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair contexto: {e}")
            
        return ""
        
    def _eh_url_pdf(self, url: str) -> bool:
        """Verifica se a URL é um PDF"""
        if not url:
            return False
        
        url_lower = url.lower()
        return '.pdf' in url_lower or 'pdf' in url_lower
        
    def _find_link_near_title(self, titulo_element) -> str:
        """Encontra link próximo ao título"""
        try:
            # Procurar por link próximo ao título
            parent = titulo_element.find_element(By.XPATH, "./..")
            links = parent.find_elements(By.TAG_NAME, "a")
            
            for link in links:
                href = self.safe_get_attribute(link, "href")
                texto_link = self.safe_get_text(link)
                
                # Priorizar links que parecem ser PDFs ou editais
                if href and href.startswith("http"):
                    if any(ext in href.lower() for ext in ['.pdf', '.doc', '.docx']):
                        return href
                    if any(palavra in texto_link.lower() for palavra in ['edital', 'chamada', 'pdf', 'download']):
                        return href
                    return href  # Retorna o primeiro link válido
                    
        except:
            pass
            
        # Se não encontrou no parent, procurar em toda a página
        try:
            links_globais = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links_globais:
                href = self.safe_get_attribute(link, "href")
                texto_link = self.safe_get_text(link)
                
                if href and href.startswith("http") and any(palavra in texto_link.lower() for palavra in ['edital', 'chamada', 'pdf']):
                    return href
                    
        except:
            pass
            
        return ""
        
    def _expand_chamadas_details(self, chamadas: List[Dict]) -> List[Dict]:
        """Tenta expandir detalhes das chamadas"""
        expanded_chamadas = []
        
        for chamada in chamadas:
            try:
                if chamada.get('url') and not self._eh_url_pdf(chamada['url']):
                    # Tentar acessar página de detalhes (apenas se não for PDF direto)
                    logger.info(f"🔍 Expandindo detalhes FAPEMIG: {chamada.get('titulo', 'Sem título')}")
                    self.driver.get(chamada['url'])
                    self.random_delay(2, 3)
                    
                    # Extrair informações adicionais
                    detalhes = self._extract_chamada_details()
                    chamada.update(detalhes)
                    
            except Exception as e:
                logger.warning(f"⚠️ Erro ao expandir detalhes FAPEMIG: {e}")
                
            expanded_chamadas.append(chamada)
            
        return expanded_chamadas
        
    def _extract_chamada_details(self) -> Dict:
        """Extrai detalhes de uma chamada específica"""
        detalhes = {}
        
        try:
            # Procurar por valores/recursos de forma mais abrangente
            valor_elements = self.safe_find_elements(By.XPATH, 
                '//*[contains(text(), "R$") or contains(text(), "valor") or contains(text(), "recurso") or contains(text(), "investimento")]')
            if valor_elements:
                detalhes['valor'] = self.safe_get_text(valor_elements[0])
                
            # Procurar por datas de forma mais abrangente
            data_elements = self.safe_find_elements(By.XPATH, 
                '//*[contains(text(), "data") or contains(text(), "prazo") or contains(text(), "período") or contains(text(), "inscrição") or contains(text(), "submissão")]')
            if data_elements:
                detalhes['prazo'] = self.safe_get_text(data_elements[0])
            
            # Procurar por objetivos
            objetivo_elements = self.safe_find_elements(By.XPATH, 
                '//*[contains(text(), "objetivo") or contains(text(), "finalidade") or contains(text(), "público")]')
            if objetivo_elements:
                detalhes['objetivo'] = self.safe_get_text(objetivo_elements[0])
            
            # Procurar por áreas
            area_elements = self.safe_find_elements(By.XPATH, 
                '//*[contains(text(), "área") or contains(text(), "campo") or contains(text(), "setor")]')
            if area_elements:
                detalhes['area'] = self.safe_get_text(area_elements[0])
            
            # Extrair texto da página para análise posterior
            body_text = self.safe_find_element(By.TAG_NAME, "body")
            if body_text:
                texto_pagina = self.safe_get_text(body_text)
                if texto_pagina:
                    detalhes['texto_pagina'] = texto_pagina[:2000]  # Primeiros 2000 caracteres
                
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair detalhes FAPEMIG: {e}")
            
        return detalhes

class CNPqScraperRobusto(BaseScraperRobusto):
    """Scraper robusto para CNPq - Chamadas Públicas"""
    
    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
        self.base_url = "http://memoria2.cnpq.br/web/guest/chamadas-publicas"
        
    def extract_chamadas(self) -> List[Dict]:
        """Extrai chamadas do CNPq com funcionalidades robustas"""
        logger.info("🚀 Iniciando extração robusta CNPq...")
        
        try:
            self.driver.get(self.base_url)
            self.random_delay(3, 5)
            
            chamadas = []
            
            # Extrair chamadas da página principal
            page_chamadas = self._extract_page_chamadas()
            chamadas.extend(page_chamadas)
            
            # Tentar expandir detalhes
            chamadas = self._expand_chamadas_details(chamadas)
            
            logger.info(f"✅ CNPq: {len(chamadas)} chamadas extraídas")
            return chamadas
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair CNPq: {e}")
            return []
            
    def _extract_page_chamadas(self) -> List[Dict]:
        """Extrai chamadas da página principal com funcionalidades robustas"""
        chamadas = []
        
        try:
            # Procurar por títulos de chamadas de forma mais abrangente
            titulos = self.safe_find_elements(By.XPATH, 
                '//h4[contains(text(), "CHAMADA") or contains(text(), "Chamada") or contains(text(), "PROGRAMA") or contains(text(), "Programa")]')
            
            # Se não encontrou títulos específicos, procurar por outros elementos
            if not titulos:
                titulos = self.safe_find_elements(By.CSS_SELECTOR, 'h1, h2, h3, h4, h5, h6, .chamada, .programa')
            
            for titulo in titulos:
                try:
                    texto = self.safe_get_text(titulo)
                    
                    if texto and any(palavra in texto.lower() for palavra in ['chamada', 'programa', 'edital', 'bolsa', 'auxílio']):
                        # Procurar período de inscrição
                        periodo = self._find_periodo_near_title(titulo)
                        
                        # Procurar link para detalhes
                        link_detalhes = self._find_link_detalhes_near_title(titulo)
                        
                        # Extrair contexto ao redor do título
                        contexto = self._extract_context_around_title(titulo)
                        
                        # Extrair PDF de forma robusta se for um link de PDF
                        pdf_info = {}
                        if link_detalhes and self._eh_url_pdf(link_detalhes):
                            logger.info(f"📄 Extraindo PDF robusto CNPq: {texto}")
                            pdf_info = self.extrair_pdf_robusto(link_detalhes, texto)
                        
                        chamada = {
                            'titulo': texto,
                            'periodo_inscricao': periodo,
                            'url_detalhes': link_detalhes,
                            'contexto': contexto,
                            'fonte': 'CNPq',
                            'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'driver': self.driver  # Para o extrator usar
                        }
                        
                        # Adicionar informações do PDF se disponível
                        if pdf_info and 'erro' not in pdf_info:
                            chamada.update({
                                'pdf_extraido': True,
                                'pdf_info': pdf_info
                            })
                        else:
                            chamada.update({
                                'pdf_extraido': False,
                                'pdf_motivo': 'Link não é PDF ou não disponível'
                            })
                        
                        chamadas.append(chamada)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar título CNPq: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Erro ao extrair página CNPq: {e}")
            
        return chamadas
    
    def _eh_url_pdf(self, url: str) -> bool:
        """Verifica se a URL é um PDF"""
        if not url:
            return False
        
        url_lower = url.lower()
        return '.pdf' in url_lower or 'pdf' in url_lower
        
    def _find_periodo_near_title(self, titulo_element) -> str:
        """Encontra período de inscrição próximo ao título"""
        try:
            # Procurar por texto com período próximo ao título
            parent = titulo_element.find_element(By.XPATH, "./..")
            parent_text = self.safe_get_text(parent)
            
            # Procurar padrões de período
            import re
            periodo_patterns = [
                r'Inscrições:\s*\d{2}/\d{2}/\d{4}\s*a\s*\d{2}/\d{2}/\d{4}',
                r'Período:\s*\d{2}/\d{2}/\d{4}\s*a\s*\d{2}/\d{2}/\d{4}',
                r'\d{2}/\d{2}/\d{4}\s*a\s*\d{2}/\d{2}/\d{4}'
            ]
            
            for pattern in periodo_patterns:
                match = re.search(pattern, parent_text)
                if match:
                    return match.group()
                    
        except:
            pass
            
        return "Período não encontrado"
        
    def _find_link_detalhes_near_title(self, titulo_element) -> str:
        """Encontra link para detalhes próximo ao título"""
        try:
            # Procurar por link próximo ao título
            parent = titulo_element.find_element(By.XPATH, "./..")
            links = parent.find_elements(By.TAG_NAME, "a")
            
            for link in links:
                href = self.safe_get_attribute(link, "href")
                texto = self.safe_get_text(link)
                
                if href and ("chamada" in texto.lower() or "detalhes" in texto.lower() or "pdf" in texto.lower()):
                    return href
                    
        except:
            pass
            
        # Se não encontrou no parent, procurar em toda a página
        try:
            links_globais = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links_globais:
                href = self.safe_get_attribute(link, "href")
                texto = self.safe_get_text(link)
                
                if href and href.startswith("http") and any(palavra in texto.lower() for palavra in ['chamada', 'detalhes', 'pdf', 'edital']):
                    return href
                    
        except:
            pass
            
        return ""
        
    def _expand_chamadas_details(self, chamadas: List[Dict]) -> List[Dict]:
        """Tenta expandir detalhes das chamadas do CNPq"""
        expanded_chamadas = []
        
        for chamada in chamadas:
            try:
                if chamada.get('url_detalhes') and not self._eh_url_pdf(chamada['url_detalhes']):
                    # Tentar acessar página de detalhes (apenas se não for PDF direto)
                    logger.info(f"🔍 Expandindo detalhes CNPq: {chamada.get('titulo', 'Sem título')}")
                    self.driver.get(chamada['url_detalhes'])
                    self.random_delay(2, 3)
                    
                    # Extrair informações adicionais
                    detalhes = self._extract_cnpq_details()
                    chamada.update(detalhes)
                    
            except Exception as e:
                logger.warning(f"⚠️ Erro ao expandir detalhes CNPq: {e}")
                
            expanded_chamadas.append(chamada)
            
        return expanded_chamadas
        
    def _extract_cnpq_details(self) -> Dict:
        """Extrai detalhes de uma chamada específica do CNPq"""
        detalhes = {}
        
        try:
            # Procurar por valores/recursos
            valor_elements = self.safe_find_elements(By.XPATH, 
                '//*[contains(text(), "R$") or contains(text(), "valor") or contains(text(), "recurso") or contains(text(), "investimento")]')
            if valor_elements:
                detalhes['valor'] = self.safe_get_text(valor_elements[0])
                
            # Procurar por datas de forma mais abrangente
            data_elements = self.safe_find_elements(By.XPATH, 
                '//*[contains(text(), "data") or contains(text(), "prazo") or contains(text(), "período") or contains(text(), "inscrição") or contains(text(), "submissão")]')
            if data_elements:
                detalhes['prazo'] = self.safe_get_text(data_elements[0])
            
            # Procurar por objetivos
            objetivo_elements = self.safe_find_elements(By.XPATH, 
                '//*[contains(text(), "objetivo") or contains(text(), "finalidade") or contains(text(), "público") or contains(text(), "destinatário")]')
            if objetivo_elements:
                detalhes['objetivo'] = self.safe_get_text(objetivo_elements[0])
            
            # Procurar por áreas
            area_elements = self.safe_find_elements(By.XPATH, 
                '//*[contains(text(), "área") or contains(text(), "campo") or contains(text(), "setor") or contains(text(), "grande área")]')
            if area_elements:
                detalhes['area'] = self.safe_get_text(area_elements[0])
            
            # Extrair texto da página para análise posterior
            body_text = self.safe_find_element(By.TAG_NAME, "body")
            if body_text:
                texto_pagina = self.safe_get_text(body_text)
                if texto_pagina:
                    detalhes['texto_pagina'] = texto_pagina[:2000]  # Primeiros 2000 caracteres
                
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair detalhes CNPq: {e}")
            
        return detalhes

class ScraperRobustoUnificado:
    """Classe principal robusta que coordena todos os scrapers"""
    
    def __init__(self):
        self.driver = None
        self.results = {
            'ufmg': [],
            'fapemig': [],
            'cnpq': [],
            'timestamp': datetime.now().isoformat(),
            'total_editais': 0
        }
        self.integrador = IntegradorPDFRobusto()
        self.gerador_resumo = None
        
    def setup_driver(self):
        """Configura o driver do Chrome"""
        try:
            # Instalar ChromeDriver
            chromedriver_autoinstaller.install()
            
            # Configurações para modo headless
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            self.driver = webdriver.Chrome(options=options)
            logger.info("✅ Driver Chrome configurado com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar driver: {e}")
            raise
            
    def run_scraping(self):
        """Executa o scraping robusto de todos os sites"""
        try:
            logger.info("🚀 Iniciando scraping robusto unificado...")
            
            # UFMG
            try:
                ufmg_scraper = UFMGScraperRobusto(self.driver)
                self.results['ufmg'] = ufmg_scraper.extract_editais()
                logger.info(f"✅ UFMG: {len(self.results['ufmg'])} editais extraídos")
            except Exception as e:
                logger.error(f"❌ Erro UFMG: {e}")
                self.results['ufmg'] = []
                
            # FAPEMIG
            try:
                fapemig_scraper = FAPEMIGScraperRobusto(self.driver)
                self.results['fapemig'] = fapemig_scraper.extract_chamadas()
                logger.info(f"✅ FAPEMIG: {len(self.results['fapemig'])} chamadas extraídas")
            except Exception as e:
                logger.error(f"❌ Erro FAPEMIG: {e}")
                self.results['fapemig'] = []
                
            # CNPq
            try:
                cnpq_scraper = CNPqScraperRobusto(self.driver)
                self.results['cnpq'] = cnpq_scraper.extract_chamadas()
                logger.info(f"✅ CNPq: {len(self.results['cnpq'])} chamadas extraídas")
            except Exception as e:
                logger.error(f"❌ Erro CNPq: {e}")
                self.results['cnpq'] = []
                
            # Calcular total
            self.results['total_editais'] = (
                len(self.results['ufmg']) + 
                len(self.results['fapemig']) + 
                len(self.results['cnpq'])
            )
            
            logger.info(f"🎉 Scraping robusto concluído! Total: {self.results['total_editais']} oportunidades")
            
        except Exception as e:
            logger.error(f"❌ Erro geral no scraping: {e}")
    
    def integrar_pdfs(self):
        """Integra PDFs extraídos usando o integrador robusto"""
        try:
            logger.info("🔗 Iniciando integração robusta de PDFs...")
            
            # Usar o integrador robusto
            self.results = self.integrador.processar_editais_com_pdfs(self.results)
            
            logger.info("✅ Integração de PDFs concluída com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro na integração de PDFs: {e}")
    
    def gerar_resumo_completo(self):
        """Gera resumo completo usando o gerador robusto"""
        try:
            logger.info("📝 Iniciando geração de resumo completo...")
            
            # Usar o gerador robusto
            self.gerador_resumo = GeradorResumoCompleto(self.results)
            resumo = self.gerador_resumo.gerar_resumo_completo()
            
            logger.info("✅ Resumo completo gerado com sucesso")
            return resumo
            
        except Exception as e:
            logger.error(f"❌ Erro na geração de resumo: {e}")
            return "Erro ao gerar resumo"
            
    def save_results(self):
        """Salva os resultados em arquivos"""
        try:
            # Remover campos não serializáveis antes de salvar
            results_clean = self._clean_results_for_serialization()
            
            # Salvar JSON completo
            with open("resultados_robustos_completos.json", "w", encoding="utf-8") as f:
                json.dump(results_clean, f, ensure_ascii=False, indent=2)
                
            # Salvar resumo em texto
            resumo = self.gerar_resumo_completo()
            with open("resumo_scraping_robusto.txt", "w", encoding="utf-8") as f:
                f.write(resumo)
                
            logger.info("✅ Resultados robustos salvos com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar resultados: {e}")
    
    def _clean_results_for_serialization(self) -> Dict:
        """Remove campos não serializáveis dos resultados"""
        results_clean = self.results.copy()
        
        # Remover campos driver de todos os editais/chamadas
        for fonte in ['ufmg', 'fapemig', 'cnpq']:
            if fonte in results_clean:
                for item in results_clean[fonte]:
                    if 'driver' in item:
                        del item['driver']
        
        return results_clean
        
    def cleanup(self):
        """Limpa recursos"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Driver fechado com sucesso")
            except:
                pass
        
        # Limpar arquivos PDF baixados
        try:
            self.integrador.limpar_arquivos_pdf()
            logger.info("✅ Arquivos PDF limpos com sucesso")
        except:
            pass

def send_email_robusto(msg_text: str, subject: str = "🚀 Scraper Robusto - Novas Oportunidades!"):
    """Envia email com os resultados robustos"""
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = os.environ['EMAIL_USER']
        msg['To'] = os.environ.get('EMAIL_DESTINO', 'clevioferreira@gmail.com')
        
        # Corpo do email
        text_part = MIMEText(msg_text, 'plain', 'utf-8')
        msg.attach(text_part)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
            server.send_message(msg)
            
        logger.info(f"✅ Email robusto enviado com sucesso para {msg['To']}!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao enviar email: {e}")
        return False

def main():
    """Função principal"""
    logger.info("=" * 60)
    logger.info("🚀 SCRAPER ROBUSTO UNIFICADO - EDITAIS E CHAMADAS")
    logger.info("=" * 60)
    
    scraper = ScraperRobustoUnificado()
    
    try:
        # Configurar driver
        scraper.setup_driver()
        
        # Executar scraping robusto
        scraper.run_scraping()
        
        # Integrar PDFs extraídos
        scraper.integrar_pdfs()
        
        # Salvar resultados
        scraper.save_results()
        
        # Preparar email
        if scraper.results['total_editais'] > 0:
            email_content = scraper.gerar_resumo_completo()
            
            # Enviar email se as variáveis estiverem configuradas
            if 'EMAIL_USER' in os.environ and 'EMAIL_PASS' in os.environ:
                logger.info("📧 Enviando email robusto...")
                if send_email_robusto(email_content):
                    logger.info("✅ Processo robusto concluído com sucesso!")
                else:
                    logger.warning("⚠️ Scraping robusto concluído, mas email não foi enviado")
            else:
                logger.warning("⚠️ Variáveis de email não configuradas")
                logger.info("📧 Conteúdo que seria enviado:")
                logger.info("-" * 40)
                logger.info(email_content)
                logger.info("-" * 40)
        else:
            logger.warning("⚠️ Nenhuma oportunidade encontrada")
            
    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}")
        
    finally:
        # Limpeza
        scraper.cleanup()

if __name__ == "__main__":
    main()
