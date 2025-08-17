#!/usr/bin/env python3
"""
Scraper Unificado para Editais e Chamadas
=========================================

Coleta dados de:
- UFMG: Editais e Chamadas
- FAPEMIG: Oportunidades
- CNPq: Chamadas Públicas

Desenvolvido seguindo as melhores práticas de web scraping
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
import chromedriver_autoinstaller
import logging
from typing import List, Dict, Optional, Tuple
import random
import requests
import os
import PyPDF2
import fitz  # PyMuPDF

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BaseScraper:
    """Classe base para todos os scrapers"""
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
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
        
    def download_pdf_if_available(self, url: str, titulo: str) -> tuple:
        """Baixa PDF se disponível e retorna (caminho_arquivo, url_pdf)"""
        try:
            if not url:
                return "", ""
                
            # Verificar se é um arquivo que pode ser baixado
            if not any(ext in url.lower() for ext in ['.pdf', '.doc', '.docx']):
                # Se não é arquivo direto, tentar encontrar PDF na página
                return self._find_and_download_pdf_from_page(url, titulo)
                
            # Criar diretório para PDFs se não existir
            pdf_dir = "pdfs_baixados"
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)
                
            # Nome do arquivo baseado no título
            safe_title = "".join(c for c in titulo if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50]  # Limitar tamanho
            filename = f"{pdf_dir}/{safe_title}.pdf"
            
            # Baixar PDF
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
                
            logger.info(f"✅ PDF baixado: {filename}")
            return filename, url
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao baixar PDF {url}: {e}")
            return "", ""
            
    def _find_and_download_pdf_from_page(self, url: str, titulo: str) -> tuple:
        """Tenta encontrar e baixar PDF de uma página específica"""
        try:
            # Acessar a página para procurar PDFs
            self.driver.get(url)
            self.random_delay(2, 3)
            
            # Procurar por links de PDF
            pdf_links = self.safe_find_elements(By.CSS_SELECTOR, 'a[href*=".pdf"], a[href*=".doc"], a[href*=".docx"]')
            
            for link in pdf_links:
                href = self.safe_get_attribute(link, "href")
                if href and href.startswith("http"):
                    # Tentar baixar este PDF
                    return self._download_specific_pdf(href, titulo)
                    
            # Procurar especificamente por anexos (comum no CNPq)
            anexo_links = self.safe_find_elements(By.XPATH, '//a[contains(text(), "Anexo") or contains(text(), "anexo")]')
            for link in anexo_links:
                href = self.safe_get_attribute(link, "href")
                if href and href.startswith("http"):
                    # Tentar baixar este anexo
                    return self._download_specific_pdf(href, titulo)
                    
            # Procurar por texto que sugira PDF
            text_elements = self.safe_find_elements(By.XPATH, '//*[contains(text(), "PDF") or contains(text(), "Download") or contains(text(), "Edital") or contains(text(), "Anexo")]')
            for element in text_elements:
                parent = element.find_element(By.XPATH, "./..")
                links = parent.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = self.safe_get_attribute(link, "href")
                    if href and href.startswith("http"):
                        return self._download_specific_pdf(href, titulo)
                        
        except Exception as e:
            logger.warning(f"⚠️ Erro ao procurar PDF na página {url}: {e}")
            
        return "", ""
        
    def _download_specific_pdf(self, url: str, titulo: str) -> tuple:
        """Baixa um PDF específico e retorna (caminho_arquivo, url_pdf)"""
        try:
            # Criar diretório para PDFs se não existir
            pdf_dir = "pdfs_baixados"
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)
                
            # Nome do arquivo baseado no título
            safe_title = "".join(c for c in titulo if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50]  # Limitar tamanho
            filename = f"{pdf_dir}/{safe_title}.pdf"
            
            # Baixar PDF
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
                
            logger.info(f"✅ PDF encontrado e baixado: {filename}")
            return filename, url
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao baixar PDF específico {url}: {e}")
            return "", ""
            
    def extract_pdf_content(self, pdf_path: str) -> Dict:
        """Extrai conteúdo e informações detalhadas de um PDF"""
        if not pdf_path or not os.path.exists(pdf_path):
            return {}
            
        try:
            logger.info(f"📖 Lendo conteúdo do PDF: {pdf_path}")
            
            # Tentar com PyMuPDF primeiro (mais robusto)
            try:
                return self._extract_with_pymupdf(pdf_path)
            except:
                # Fallback para PyPDF2
                try:
                    return self._extract_with_pypdf2(pdf_path)
                except:
                    logger.warning(f"⚠️ Não foi possível ler o PDF: {pdf_path}")
                    return {}
                    
        except Exception as e:
            logger.error(f"❌ Erro ao extrair conteúdo do PDF {pdf_path}: {e}")
            return {}
            
    def _extract_with_pymupdf(self, pdf_path: str) -> Dict:
        """Extrai conteúdo usando PyMuPDF"""
        doc = fitz.open(pdf_path)
        texto_completo = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            texto_completo += page.get_text()
            
        doc.close()
        
        return self._analyze_pdf_text(texto_completo)
        
    def _extract_with_pypdf2(self, pdf_path: str) -> Dict:
        """Extrai conteúdo usando PyPDF2"""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            
            for page in reader.pages:
                texto_completo += page.extract_text()
                
        return self._analyze_pdf_text(texto_completo)
        
    def _analyze_pdf_text(self, texto: str) -> Dict:
        """Analisa o texto extraído do PDF para encontrar informações importantes"""
        import re
        
        info = {}
        
        # Padrões para datas
        date_patterns = [
            r'(\d{2}/\d{2}/\d{4})',  # DD/MM/AAAA
            r'(\d{2}-\d{2}-\d{4})',  # DD-MM-AAAA
            r'(\d{2}\.\d{2}\.\d{4})', # DD.MM.AAAA
            r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})', # 15 de agosto de 2025
        ]
        
        datas_encontradas = []
        for pattern in date_patterns:
            matches = re.findall(pattern, texto)
            datas_encontradas.extend(matches)
            
        if datas_encontradas:
            info['datas_encontradas'] = list(set(datas_encontradas))  # Remove duplicatas
            
        # Padrões para valores/recursos
        valor_patterns = [
            r'R\$\s*([\d.,]+)',  # R$ 50.000,00
            r'(\d+\.?\d*)\s*mil\s*reais',  # 50 mil reais
            r'(\d+\.?\d*)\s*milhões?\s*de\s*reais',  # 2 milhões de reais
            r'Valor:\s*R\$\s*([\d.,]+)',  # Valor: R$ 100.000,00
        ]
        
        valores_encontrados = []
        for pattern in valor_patterns:
            matches = re.findall(pattern, texto, re.IGNORECASE)
            valores_encontrados.extend(matches)
            
        if valores_encontrados:
            info['valores_encontrados'] = valores_encontrados
            
        # Padrões para prazos
        prazo_patterns = [
            r'prazo.*?(\d{2}/\d{2}/\d{4})',  # prazo até 30/09/2025
            r'até.*?(\d{2}/\d{2}/\d{4})',    # até 30/09/2025
            r'vencimento.*?(\d{2}/\d{2}/\d{4})', # vencimento 30/09/2025
            r'inscrições.*?(\d{2}/\d{2}/\d{4})', # inscrições até 30/09/2025
        ]
        
        prazos_encontrados = []
        for pattern in prazo_patterns:
            matches = re.findall(pattern, texto, re.IGNORECASE)
            prazos_encontrados.extend(matches)
            
        if prazos_encontrados:
            info['prazos_encontrados'] = list(set(prazos_encontrados))
            
        # Padrões para objetivos/descrição
        objetivo_patterns = [
            r'Objetivo[:\s]*([^.\n]+)',
            r'Objetivos[:\s]*([^.\n]+)',
            r'Descrição[:\s]*([^.\n]+)',
            r'Resumo[:\s]*([^.\n]+)',
        ]
        
        for pattern in objetivo_patterns:
            match = re.search(pattern, texto, re.IGNORECASE)
            if match:
                info['objetivo'] = match.group(1).strip()
                break
                
        # Padrões para área/tema
        area_patterns = [
            r'Área[:\s]*([^.\n]+)',
            r'Tema[:\s]*([^.\n]+)',
            r'Linha[:\s]*([^.\n]+)',
            r'Campo[:\s]*([^.\n]+)',
        ]
        
        for pattern in area_patterns:
            match = re.search(pattern, texto, re.IGNORECASE)
            if match:
                info['area_tema'] = match.group(1).strip()
                break
                
        # Contar páginas e tamanho
        info['tamanho_texto'] = len(texto)
        info['palavras'] = len(texto.split())
        
        logger.info(f"✅ PDF analisado: {len(info)} informações extraídas")
        return info

class UFMGScraper(BaseScraper):
    """Scraper para UFMG - Editais e Chamadas"""
    
    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
        self.base_url = "https://www.ufmg.br/prograd/editais-chamadas/"
        
    def extract_editais(self) -> List[Dict]:
        """Extrai editais da UFMG"""
        logger.info("🚀 Iniciando extração UFMG...")
        
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
        """Extrai editais de uma página específica"""
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
                        
                        # Tentar baixar PDF se for um link de PDF
                        pdf_result = self.download_pdf_if_available(href, titulo)
                        pdf_path, pdf_url = pdf_result if isinstance(pdf_result, tuple) else (pdf_result, "")
                        
                        # Se PDF foi baixado, extrair conteúdo detalhado
                        pdf_info = {}
                        if pdf_path:
                            pdf_info = self.extract_pdf_content(pdf_path)
                        
                        # Extrair contexto da página
                        contexto = self._extract_context_from_page(href)
                        
                        edital = {
                            'titulo': titulo,
                            'url': href,
                            'data': data,
                            'fonte': 'UFMG',
                            'pdf_baixado': pdf_path,
                            'pdf_url': pdf_url,
                            'pdf_info': pdf_info,
                            'contexto': contexto, # Adicionar contexto ao dicionário
                            'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        editais.append(edital)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar link UFMG: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Erro ao extrair página UFMG: {e}")
            
        return editais
        
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
        
    def _extract_context_from_page(self, url: str) -> str:
        """Extrai contexto/descrição da página do edital (NOVA FUNÇÃO)"""
        try:
            # Acessar a página para extrair contexto
            self.driver.get(url)
            self.random_delay(2, 3)
            
            # Estratégia 1: Procurar por parágrafos com texto descritivo
            context_elements = self.safe_find_elements(By.XPATH, '//p[string-length(text()) > 100]')
            
            for element in context_elements:
                texto = self.safe_get_text(element)
                if texto and len(texto) > 100:
                    # Verificar se parece ser uma descrição de edital
                    if any(palavra in texto.lower() for palavra in ['objetivo', 'selecionar', 'propostas', 'apoio', 'desenvolvimento', 'científico', 'tecnológico', 'edital', 'chamada']):
                        return texto[:500] + "..." if len(texto) > 500 else texto
            
            # Estratégia 2: Procurar por divs com texto longo
            div_elements = self.safe_find_elements(By.XPATH, '//div[string-length(text()) > 150]')
            for element in div_elements:
                texto = self.safe_get_text(element)
                if texto and len(texto) > 150:
                    # Filtrar por conteúdo relevante
                    if any(palavra in texto.lower() for palavra in ['edital', 'chamada', 'objetivo', 'selecionar', 'propostas']):
                        return texto[:500] + "..." if len(texto) > 500 else texto
            
            # Estratégia 3: Procurar por elementos com classes específicas
            class_selectors = [
                '//div[contains(@class, "content")]',
                '//div[contains(@class, "description")]',
                '//div[contains(@class, "text")]',
                '//section[contains(@class, "content")]',
                '//article[contains(@class, "content")]'
            ]
            
            for selector in class_selectors:
                try:
                    elements = self.safe_find_elements(By.XPATH, selector)
                    for element in elements:
                        texto = self.safe_get_text(element)
                        if texto and len(texto) > 200:
                            # Verificar se contém informações relevantes
                            if any(palavra in texto.lower() for palavra in ['edital', 'chamada', 'objetivo', 'selecionar', 'propostas', 'apoio']):
                                return texto[:500] + "..." if len(texto) > 500 else texto
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair contexto da página UFMG: {e}")
            
        return ""
        
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

class FAPEMIGScraper(BaseScraper):
    """Scraper para FAPEMIG - Oportunidades"""
    
    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
        self.base_url = "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/"
        
    def extract_chamadas(self) -> List[Dict]:
        """Extrai chamadas da FAPEMIG"""
        logger.info("🚀 Iniciando extração FAPEMIG...")
        
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
        """Extrai chamadas da página principal"""
        chamadas = []
        titulos_processados = set()  # Para evitar duplicatas
        
        try:
            # Procurar por títulos de chamadas
            titulos = self.safe_find_elements(By.CSS_SELECTOR, 'h1, h2, h3, h4, h5, h6')
            
            for titulo in titulos:
                try:
                    texto = self.safe_get_text(titulo)
                    
                    if texto and any(palavra in texto.lower() for palavra in ['chamada', 'edital', 'oportunidade']):
                        # Verificar se já processamos este título
                        if texto in titulos_processados:
                            continue
                        titulos_processados.add(texto)
                        
                        # Procurar link associado
                        link = self._find_link_near_title(titulo)
                        
                        # Tentar baixar PDF se for um link de PDF
                        pdf_result = self.download_pdf_if_available(link, texto)
                        pdf_path, pdf_url = pdf_result if isinstance(pdf_result, tuple) else (pdf_result, "")
                        
                        # Se PDF foi baixado, extrair conteúdo detalhado
                        pdf_info = {}
                        if pdf_path:
                            pdf_info = self.extract_pdf_content(pdf_path)
                        
                        chamada = {
                            'titulo': texto,
                            'url': link,
                            'fonte': 'FAPEMIG',
                            'pdf_baixado': pdf_path,
                            'pdf_url': pdf_url,
                            'pdf_info': pdf_info,
                            'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        chamadas.append(chamada)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar título FAPEMIG: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Erro ao extrair página FAPEMIG: {e}")
            
        return chamadas
        
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
                if chamada['url']:
                    # Tentar acessar página de detalhes
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
            # Procurar por valores/recursos
            valor_elements = self.safe_find_elements(By.XPATH, '//*[contains(text(), "R$") or contains(text(), "valor") or contains(text(), "recurso")]')
            if valor_elements:
                detalhes['valor'] = self.safe_get_text(valor_elements[0])
                
            # Procurar por descrição/contexto (NOVO - PRIORIDADE ALTA)
            contexto = self._extract_context_from_page()
            if contexto:
                detalhes['contexto'] = contexto
                
            # Procurar por datas
            data_elements = self.safe_find_elements(By.XPATH, '//*[contains(text(), "data") or contains(text(), "prazo") or contains(text(), "período")]')
            if data_elements:
                detalhes['prazo'] = self.safe_get_text(data_elements[0])
                
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair detalhes FAPEMIG: {e}")
            
        return detalhes
        
    def _extract_context_from_page(self) -> str:
        """Extrai contexto/descrição da página atual (NOVA FUNÇÃO)"""
        try:
            # Estratégia 1: Procurar por parágrafos com texto descritivo
            context_elements = self.safe_find_elements(By.XPATH, '//p[string-length(text()) > 100]')
            
            for element in context_elements:
                texto = self.safe_get_text(element)
                if texto and len(texto) > 100:
                    # Verificar se parece ser uma descrição de edital
                    if any(palavra in texto.lower() for palavra in ['objetivo', 'selecionar', 'propostas', 'apoio', 'desenvolvimento', 'científico', 'tecnológico']):
                        return texto[:500] + "..." if len(texto) > 500 else texto
            
            # Estratégia 2: Procurar por divs com texto longo
            div_elements = self.safe_find_elements(By.XPATH, '//div[string-length(text()) > 150]')
            for element in div_elements:
                texto = self.safe_get_text(element)
                if texto and len(texto) > 150:
                    # Filtrar por conteúdo relevante
                    if any(palavra in texto.lower() for palavra in ['chamada', 'pública', 'objetivo', 'selecionar', 'propostas']):
                        return texto[:500] + "..." if len(texto) > 500 else texto
            
            # Estratégia 3: Procurar por elementos com classes específicas
            class_selectors = [
                '//div[contains(@class, "content")]',
                '//div[contains(@class, "description")]',
                '//div[contains(@class, "text")]',
                '//section[contains(@class, "content")]',
                '//article[contains(@class, "content")]'
            ]
            
            for selector in class_selectors:
                try:
                    elements = self.safe_find_elements(By.XPATH, selector)
                    for element in elements:
                        texto = self.safe_get_text(element)
                        if texto and len(texto) > 200:
                            # Verificar se contém informações relevantes
                            if any(palavra in texto.lower() for palavra in ['chamada', 'objetivo', 'selecionar', 'propostas', 'apoio']):
                                return texto[:500] + "..." if len(texto) > 500 else texto
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair contexto da página: {e}")
            
        return ""

class CNPqScraper(BaseScraper):
    """Scraper para CNPq - Chamadas Públicas - VERSÃO MELHORADA"""
    
    # Mapeamento para casefold em XPath, incluindo acentos mais comuns
    LOWER = ('translate(normalize-space(string(.)),'
             '"ÁÀÂÃÄÅÇÉÈÊËÍÌÎÏÑÓÒÔÕÖÚÙÛÜÝŶABCDEFGHIJKLMNOPQRSTUVWXYZ",'
             '"aaaaaaceeeeiiiinooooouuuuyyabcdefghijklmnopqrstuvwxyz")')

    # Palavras-chave para título e URL
    KW_TITULO = ("chamada", "edital", "seleção", "selecoes", "bolsa", "bolsas", "fomento")
    KW_URL = ("chamada", "chamadas", "edital", "editais")

    # Regex de datas comuns
    REGEX_DATAS = [
        re.compile(r'(\d{1,2}/\d{1,2}/\d{2,4})\s*(?:a|até|-|–|—)\s*(\d{1,2}/\d{1,2}/\d{2,4})', re.I),
        re.compile(r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4}).{0,30}?(?:a|até|-|–|—).{0,30}?(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})', re.I),
        re.compile(r'(?:prazo|inscriç(?:ão|oes)|submiss(?:ão|ões)).{0,40}?(?:até|encerra(?:m)? em)\s+(\d{1,2}/\d{1,2}/\d{2,4})', re.I),
        re.compile(r'(?:prazo|inscriç(?:ão|oes)|submiss(?:ão|ões)).{0,40}?(?:até|encerra(?:m)? em)\s+(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})', re.I),
    ]

    MESES_PT_EN = {
        "janeiro":"january","fevereiro":"february","março":"march","marco":"march","abril":"april",
        "maio":"may","junho":"june","julho":"july","agosto":"august","setembro":"september",
        "outubro":"october","novembro":"november","dezembro":"december"
    }

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
        self._seen = set()
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; CNPqScraper/1.0; +https://cnpq.br)"
        })
        # pasta padrão para PDFs se sua base não definir
        self._pdf_dir = getattr(self, "pdf_dir", os.path.join(os.getcwd(), "pdfs_baixados"))
        os.makedirs(self._pdf_dir, exist_ok=True)
        
    def extract_chamadas(self) -> List[Dict]:
        """Extrai chamadas do CNPq usando o novo sistema robusto"""
        logger.info("🚀 Iniciando extração CNPq com sistema robusto...")
        
        # URLs atualizadas do CNPq
        base_urls = [
            "https://www.gov.br/cnpq/pt-br/acesso-a-informacao/acoes-e-programas/programas/chamadas-publicas",
            "https://www.gov.br/cnpq/pt-br/acesso-a-informacao/acoes-e-programas/programas",
            "http://memoria2.cnpq.br/web/guest/chamadas-publicas"  # Fallback
        ]
        
        chamadas = []
        
        # Tentar múltiplas URLs até encontrar chamadas
        for base_url in base_urls:
            try:
                logger.info(f"🔍 Tentando URL: {base_url}")
                self.driver.get(base_url)
                self.random_delay(3, 5)
                
                # Extrair chamadas da página atual
                page_chamadas = self.extract_cnpq_chamadas()
                if page_chamadas:
                    chamadas.extend(page_chamadas)
                    logger.info(f"✅ Encontradas {len(page_chamadas)} chamadas em {base_url}")
                    break
                else:
                    logger.warning(f"⚠️ Nenhuma chamada encontrada em {base_url}")
                    
            except Exception as e:
                logger.warning(f"⚠️ Erro ao acessar {base_url}: {e}")
                continue
        
        if chamadas:
            # Tentar expandir detalhes
            chamadas = self._expand_chamadas_details(chamadas)
            logger.info(f"✅ CNPq: {len(chamadas)} chamadas extraídas")
        else:
            logger.warning("⚠️ Nenhuma chamada encontrada em nenhuma URL do CNPq")
            
        return chamadas
        
    # --------- Utils ---------
    @staticmethod
    def _norm(s: str) -> str:
        return ' '.join((s or '').split()).strip().lower()

    @staticmethod
    def _canon(url: str) -> str:
        if not url:
            return ""
        u = url.strip()
        q = u.split('#')[0]
        q = q.split('?')[0]
        return q

    @staticmethod
    def _safe_hash(s: str) -> str:
        import hashlib
        return hashlib.md5((s or '').encode('utf-8')).hexdigest()

    def _key(self, title: str, url: str) -> str:
        return f"{self._safe_hash(self._norm(title))}|{self._canon(url)}"

    def _translate_href_xpath(self, attr="href") -> str:
        return f'translate(@{attr},"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")'

    # --------- Datas ---------
    def _pt_to_iso(self, s: str) -> str | None:
        if not s:
            return None
        txt = self._norm(s)
        # dd/mm/yyyy
        m = re.match(r'(\d{1,2})/(\d{1,2})/(\d{2,4})', txt)
        if m:
            d, M, y = map(int, m.groups())
            y = 2000 + y if y < 100 else y
            try:
                return datetime(y, M, d).date().isoformat()
            except ValueError:
                return None
        # d de mês de yyyy
        m2 = re.match(r'(\d{1,2})\s+de\s+([a-zç]+)\s+de\s+(\d{4})', txt)
        if m2:
            d = int(m2.group(1))
            mes = m2.group(2)
            y = int(m2.group(3))
            mes_en = self.MESES_PT_EN.get(mes, None)
            if mes_en:
                try:
                    # map to month index
                    M = datetime.strptime(mes_en[:3], "%b").month
                    return datetime(y, M, d).date().isoformat()
                except ValueError:
                    return None
        return None

    def _extract_periodo(self, blob: str) -> dict | None:
        if not blob:
            return None
        for rx in self.REGEX_DATAS:
            m = rx.search(blob)
            if not m:
                continue
            if m.lastindex == 2:
                ini = self._pt_to_iso(m.group(1))
                fim = self._pt_to_iso(m.group(2))
                if ini or fim:
                    return {"inicio": ini, "fim": fim}
            elif m.lastindex == 1:
                fim = self._pt_to_iso(m.group(1))
                if fim:
                    return {"inicio": None, "fim": fim}
        return None

    # --------- Heurística ---------
    def _score(self, titulo: str, href: str | None, contexto: str | None, periodo: dict | None) -> int:
        s = 0
        t = self._norm(titulo)
        for kw in self.KW_TITULO:
            if kw in t:
                s += 1
        h = self._norm(href or "")
        if any(k in h for k in self.KW_URL):
            s += 1
        if periodo:
            s += 1
        if contexto:
            c = self._norm(contexto)
            if any(k in c for k in self.KW_TITULO):
                s += 1
        return s

    # --------- PDFs ---------
    def download_pdf_if_available(self, href: str, titulo: str):
        """Compatível com sua interface anterior. Retorna (pdf_path, pdf_url) ou ("", url)."""
        if not href:
            return ("", "")
        url = self._canon(href)
        try:
            head = self._session.head(url, allow_redirects=True, timeout=15)
            ctype = (head.headers.get("Content-Type") or "").lower()
            clen = head.headers.get("Content-Length")
            clen = int(clen) if clen and clen.isdigit() else None
        except Exception as e:
            logger.debug(f"HEAD falhou, prosseguindo por extensão: {e}")
            ctype = ""
            clen = None

        is_pdf = url.lower().endswith(".pdf") or "application/pdf" in ctype
        if not is_pdf:
            return ("", url)

        # limite opcional de tamanho, p.ex. 35MB
        if clen and clen > 35 * 1024 * 1024:
            logger.info(f"PDF muito grande, ignorado: {clen} bytes")
            return ("", url)

        safe_name = re.sub(r'[^a-z0-9._-]+', '_', self._norm(titulo))[:80] or "chamada"
        fpath = os.path.join(self._pdf_dir, f"{safe_name}.pdf")

        try:
            with self._session.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(fpath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            return (fpath, url)
        except Exception as e:
            logger.warning(f"Falha ao baixar PDF: {e}")
            return ("", url)

    # --------- Busca de link próximo ---------
    def _find_link_detalhes_near_title(self, titulo_element) -> str:
        # 1) container mais próximo plausível
        containers = [
            'ancestor::section[1]', 'ancestor::article[1]', 'ancestor::div[1]'
        ]
        for c in containers:
            try:
                container = titulo_element.find_element(By.XPATH, c)
                href = container.find_element(
                    By.XPATH,
                    f'.//a[@href and (contains({self.LOWER}, "chamada") or contains({self.LOWER}, "edital"))]'
                ).get_attribute("href")
                if href and href.startswith("http"):
                    return href
            except Exception:
                pass
        # 2) primeiro link visível após o título
        try:
            href = titulo_element.find_element(By.XPATH, 'following::a[@href][1]').get_attribute("href")
            if href and href.startswith("http"):
                return href
        except Exception:
            pass
        # 3) global por href contendo palavra-chave
        try:
            links = self.safe_find_elements(
                By.XPATH,
                f'//a[@href and (contains({self._translate_href_xpath()},"chamada") or contains({self._translate_href_xpath()},"edital"))]'
            )
            for lk in links:
                h = self.safe_get_attribute(lk, "href")
                if h and h.startswith("http"):
                    return h
        except Exception:
            pass
        return ""

    # --------- Período próximo ao título ---------
    def _find_periodo_near_title(self, titulo_element) -> dict | None:
        blobs = []
        x_local = [
            '.',  # próprio título
            'following-sibling::*[position()<=3]',
            'ancestor::section[1]',
            'ancestor::div[1]',
        ]
        for xp in x_local:
            try:
                if xp == '.':
                    blobs.append(self.safe_get_text(titulo_element))
                else:
                    nodes = titulo_element.find_elements(By.XPATH, xp)
                    txt = ' '.join(self.safe_get_text(n) for n in nodes if n)
                    blobs.append(txt)
            except Exception:
                continue

        # concatena e tenta regex
        for blob in blobs:
            per = self._extract_periodo(blob)
            if per:
                return per
        return None
        
    def extract_cnpq_chamadas(self) -> List[Dict]:
        """Extrai chamadas do CNPq usando o novo sistema robusto"""
        chamadas = []
        seen = self._seen

        # XPath amplo porém controlado
        X_TITULOS = (
            f'//*[self::h1 or self::h2 or self::h3 or self::h4 or self::a]'
            f'[contains({self.LOWER}, "chamada") or contains({self.LOWER}, "edital") or '
            f' contains({self.LOWER}, "seleção") or contains({self.LOWER}, "bolsas")]'
        )

        wait = WebDriverWait(self.driver, 15)
        try:
            wait.until(EC.visibility_of_any_elements_located((By.XPATH, X_TITULOS)))
        except TimeoutException:
            logger.info("Nenhum título visível no tempo limite")
            return chamadas

        # Estratégia 1: títulos relevantes
        titulos = self.safe_find_elements(By.XPATH, X_TITULOS)
        MAX_ITEMS = 50
        count = 0

        for el in titulos:
            if count >= MAX_ITEMS:
                break
            try:
                texto = self._norm(self.safe_get_text(el))
                if len(texto) < 12:
                    continue

                link_detalhes = self._find_link_detalhes_near_title(el)
                periodo = self._find_periodo_near_title(el)
                k = self._key(texto, link_detalhes)
                if k in seen:
                    continue

                score = self._score(texto, link_detalhes, None, periodo)
                if score < 2:
                    continue  # filtra ruído

                # PDF
                pdf_path, pdf_url = self.download_pdf_if_available(link_detalhes, texto)
                pdf_info = {}
                if pdf_path:
                    try:
                        pdf_info = self.extract_pdf_content(pdf_path)  # usa seu extrator existente
                        # tenta extrair período também do PDF
                        if not periodo:
                            periodo = self._extract_periodo(json.dumps(pdf_info, ensure_ascii=False))
                    except Exception as e:
                        logger.warning(f"Falha ao extrair PDF: {e}")

                chamadas.append({
                    "titulo": texto,
                    "periodo_inscricao": periodo,
                    "url_detalhes": link_detalhes,
                    "fonte": "CNPq",
                    "pdf_baixado": pdf_path,
                    "pdf_url": pdf_url,
                    "pdf_info": pdf_info,
                    "data_extracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
                seen.add(k)
                count += 1
                logger.info(f"✅ Chamada CNPq: {texto[:80]}...")
                time.sleep(random.uniform(0.2, 0.6))
            except (StaleElementReferenceException, NoSuchElementException):
                continue
            except Exception as e:
                logger.warning(f"Falha ao processar título: {e}")
                continue

        if chamadas:
            return chamadas

        # Estratégia 2: links com href contendo palavras-chave
        try:
            links_ch = self.safe_find_elements(
                By.XPATH,
                f'//a[@href and (contains({self._translate_href_xpath()},"/chamada") or '
                f'contains({self._translate_href_xpath()},"/editais") or '
                f'contains({self._translate_href_xpath()},"/edital"))]'
            )
        except Exception:
            links_ch = []

        for lk in links_ch[:MAX_ITEMS]:
            try:
                href = self.safe_get_attribute(lk, "href")
                texto = self._norm(self.safe_get_text(lk))
                if not href:
                    continue
                k = self._key(texto or href, href)
                if k in seen:
                    continue

                periodo = self._find_periodo_near_title(lk)
                score = self._score(texto or href, href, None, periodo)
                if score < 2:
                    continue

                pdf_path, pdf_url = self.download_pdf_if_available(href, texto or "chamada")
                pdf_info = {}
                if pdf_path:
                    try:
                        pdf_info = self.extract_pdf_content(pdf_path)
                        if not periodo:
                            periodo = self._extract_periodo(json.dumps(pdf_info, ensure_ascii=False))
                    except Exception as e:
                        logger.warning(f"Falha ao extrair PDF: {e}")

                chamadas.append({
                    "titulo": texto or href,
                    "periodo_inscricao": periodo,
                    "url_detalhes": href,
                    "fonte": "CNPq",
                    "pdf_baixado": pdf_path,
                    "pdf_url": pdf_url,
                    "pdf_info": pdf_info,
                    "data_extracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
                seen.add(k)
                logger.info(f"✅ Chamada CNPq (href): {(texto or href)[:80]}...")
                time.sleep(random.uniform(0.2, 0.6))
            except Exception:
                continue

        if chamadas:
            return chamadas

        # Estratégia 3: fallback global por qualquer elemento com "chamada"
        try:
            all_elements = self.safe_find_elements(
                By.XPATH, f'//*[contains({self.LOWER}, "chamada") or contains({self.LOWER}, "edital")]'
            )
        except Exception:
            all_elements = []

        for el in all_elements[:MAX_ITEMS]:
            try:
                texto = self._norm(self.safe_get_text(el))
                if len(texto) < 12:
                    continue
                href = self._find_link_detalhes_near_title(el)
                periodo = self._find_periodo_near_title(el)
                k = self._key(texto, href)
                if k in seen:
                    continue

                score = self._score(texto, href, texto, periodo)
                if score < 2:
                    continue

                pdf_path, pdf_url = self.download_pdf_if_available(href, texto)
                pdf_info = {}
                if pdf_path:
                    try:
                        pdf_info = self.extract_pdf_content(pdf_path)
                        if not periodo:
                            periodo = self._extract_periodo(json.dumps(pdf_info, ensure_ascii=False))
                    except Exception as e:
                        logger.warning(f"Falha ao extrair PDF: {e}")

                chamadas.append({
                    "titulo": texto,
                    "periodo_inscricao": periodo,
                    "url_detalhes": href,
                    "fonte": "CNPq",
                    "pdf_baixado": pdf_path,
                    "pdf_url": pdf_url,
                    "pdf_info": pdf_info,
                    "data_extracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
                seen.add(k)
                logger.info(f"✅ Chamada CNPq (fallback): {texto[:80]}...")
                time.sleep(random.uniform(0.2, 0.6))
            except Exception:
                continue

        return chamadas
        
    def _expand_chamadas_details(self, chamadas: List[Dict]) -> List[Dict]:
        """Tenta expandir detalhes das chamadas"""
        expanded_chamadas = []
        
        for chamada in chamadas:
            try:
                if chamada['url_detalhes']:
                    # Tentar acessar página de detalhes
                    self.driver.get(chamada['url_detalhes'])
                    self.random_delay(2, 3)
                    
                    # Extrair informações adicionais
                    detalhes = self._extract_chamada_details()
                    chamada.update(detalhes)
                    
            except Exception as e:
                logger.warning(f"⚠️ Erro ao expandir detalhes CNPq: {e}")
                
            expanded_chamadas.append(chamada)
            
        return expanded_chamadas
        
    def _extract_chamada_details(self) -> Dict:
        """Extrai detalhes de uma chamada específica"""
        detalhes = {}
        
        try:
            # Procurar por valores/recursos
            valor_elements = self.safe_find_elements(By.XPATH, '//*[contains(text(), "R$") or contains(text(), "valor") or contains(text(), "recurso")]')
            if valor_elements:
                detalhes['valor'] = self.safe_get_text(valor_elements[0])
                
            # Procurar por descrição/contexto (NOVO - PRIORIDADE ALTA)
            contexto = self._extract_context_from_page()
            if contexto:
                detalhes['contexto'] = contexto
                
            # Procurar por descrição
            desc_elements = self.safe_find_elements(By.XPATH, '//p[contains(text(), "Objetivo") or contains(text(), "Descrição")]')
            if desc_elements:
                detalhes['descricao'] = self.safe_get_text(desc_elements[0])
                
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair detalhes CNPq: {e}")
            
        return detalhes
        
    def _extract_context_from_page(self) -> str:
        """Extrai contexto/descrição da página atual (NOVA FUNÇÃO)"""
        try:
            # Estratégia 1: Procurar por parágrafos com texto descritivo
            context_elements = self.safe_find_elements(By.XPATH, '//p[string-length(text()) > 100]')
            
            for element in context_elements:
                texto = self.safe_get_text(element)
                if texto and len(texto) > 100:
                    # Verificar se parece ser uma descrição de chamada
                    if any(palavra in texto.lower() for palavra in ['objetivo', 'selecionar', 'propostas', 'apoio', 'desenvolvimento', 'científico', 'tecnológico']):
                        return texto[:500] + "..." if len(texto) > 500 else texto
            
            # Estratégia 2: Procurar por divs com texto longo
            div_elements = self.safe_find_elements(By.XPATH, '//div[string-length(text()) > 150]')
            for element in div_elements:
                texto = self.safe_get_text(element)
                if texto and len(texto) > 150:
                    # Filtrar por conteúdo relevante
                    if any(palavra in texto.lower() for palavra in ['chamada', 'pública', 'objetivo', 'selecionar', 'propostas']):
                        return texto[:500] + "..." if len(texto) > 500 else texto
            
            # Estratégia 3: Procurar por elementos com classes específicas
            class_selectors = [
                '//div[contains(@class, "content")]',
                '//div[contains(@class, "description")]',
                '//div[contains(@class, "text")]',
                '//section[contains(@class, "content")]',
                '//article[contains(@class, "content")]'
            ]
            
            for selector in class_selectors:
                try:
                    elements = self.safe_find_elements(By.XPATH, selector)
                    for element in elements:
                        texto = self.safe_get_text(element)
                        if texto and len(texto) > 200:
                            # Verificar se contém informações relevantes
                            if any(palavra in texto.lower() for palavra in ['chamada', 'objetivo', 'selecionar', 'propostas', 'apoio']):
                                return texto[:500] + "..." if len(texto) > 500 else texto
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair contexto da página: {e}")
            
        return ""

class ScraperUnificado:
    """Classe principal que coordena todos os scrapers"""
    
    def __init__(self):
        self.driver = None
        self.results = {
            'ufmg': [],
            'fapemig': [],
            'cnpq': [],
            'timestamp': datetime.now().isoformat(),
            'total_editais': 0
        }
        
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
        """Executa o scraping de todos os sites"""
        try:
            logger.info("🚀 Iniciando scraping unificado...")
            
            # UFMG
            try:
                ufmg_scraper = UFMGScraper(self.driver)
                self.results['ufmg'] = ufmg_scraper.extract_editais()
                logger.info(f"✅ UFMG: {len(self.results['ufmg'])} editais extraídos")
            except Exception as e:
                logger.error(f"❌ Erro UFMG: {e}")
                self.results['ufmg'] = []
                
            # FAPEMIG
            try:
                fapemig_scraper = FAPEMIGScraper(self.driver)
                self.results['fapemig'] = fapemig_scraper.extract_chamadas()
                logger.info(f"✅ FAPEMIG: {len(self.results['fapemig'])} chamadas extraídas")
            except Exception as e:
                logger.error(f"❌ Erro FAPEMIG: {e}")
                self.results['fapemig'] = []
                
            # CNPq
            try:
                cnpq_scraper = CNPqScraper(self.driver)
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
            
            logger.info(f"🎉 Scraping concluído! Total: {self.results['total_editais']} oportunidades")
            
        except Exception as e:
            logger.error(f"❌ Erro geral no scraping: {e}")
            
    def save_results(self):
        """Salva os resultados em arquivos"""
        try:
            # Salvar JSON completo
            with open("resultados_completos.json", "w", encoding="utf-8") as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
                
            # Salvar resumo em texto
            with open("resumo_scraping.txt", "w", encoding="utf-8") as f:
                f.write(self._generate_summary())
                
            logger.info("✅ Resultados salvos com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar resultados: {e}")
            
    def _generate_summary(self) -> str:
        """Gera resumo em texto dos resultados"""
        # Contar PDFs baixados e analisados
        pdfs_ufmg = sum(1 for e in self.results['ufmg'] if e.get('pdf_baixado'))
        pdfs_fapemig = sum(1 for e in self.results['fapemig'] if e.get('pdf_baixado'))
        pdfs_cnpq = sum(1 for e in self.results['cnpq'] if e.get('pdf_baixado'))
        total_pdfs = pdfs_ufmg + pdfs_fapemig + pdfs_cnpq
        
        # Contar PDFs com conteúdo extraído
        pdfs_analisados = sum(1 for e in self.results['ufmg'] + self.results['fapemig'] + self.results['cnpq'] if e.get('pdf_info'))
        
        summary = f"""
🚀 RESUMO DO SCRAPING UNIFICADO
================================
Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
Total de Oportunidades: {self.results['total_editais']}
📄 PDFs Baixados: {total_pdfs}
📖 PDFs Analisados: {pdfs_analisados}

📊 UFMG - Editais e Chamadas
-----------------------------
Total: {len(self.results['ufmg'])} editais
PDFs: {pdfs_ufmg} baixados
{self._format_editais_list(self.results['ufmg'])}

📊 FAPEMIG - Oportunidades
---------------------------
Total: {len(self.results['fapemig'])} chamadas
PDFs: {pdfs_fapemig} baixados
{self._format_editais_list(self.results['fapemig'])}

📊 CNPq - Chamadas Públicas
----------------------------
Total: {len(self.results['cnpq'])} chamadas
PDFs: {pdfs_cnpq} baixados
{self._format_editais_list(self.results['cnpq'])}

---
🤖 Scraper automatizado executado via GitHub Actions
📅 Executado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
        """
        return summary
        
    def _format_editais_list(self, editais: List[Dict]) -> str:
        """Formata lista de editais para o resumo"""
        if not editais:
            return "Nenhuma oportunidade encontrada"
            
        formatted = ""
        for i, edital in enumerate(editais[:5], 1):  # Mostrar apenas os 5 primeiros
            titulo = edital.get('titulo', 'Sem título')
            # Mostrar título completo se for menor que 80 caracteres
            if len(titulo) <= 80:
                formatted += f"{i}. {titulo}\n"
            else:
                formatted += f"{i}. {titulo[:80]}... (📄 Título completo disponível)\n"
            
            # Adicionar informações extras se disponíveis
            if edital.get('data'):
                formatted += f"   📅 Data: {edital['data']}\n"
            if edital.get('periodo_inscricao'):
                formatted += f"   📅 Período: {edital['periodo_inscricao']}\n"
            if edital.get('valor'):
                formatted += f"   💰 Valor: {edital['valor']}\n"
                
            # NOVO: Contexto extraído da página web (prioridade alta)
            if edital.get('contexto'):
                contexto = edital['contexto']
                if len(contexto) > 120:
                    formatted += f"   📋 Contexto: {contexto[:120]}... (📄 Texto completo disponível)\n"
                else:
                    formatted += f"   📋 Contexto: {contexto}\n"
                
            # Informações extraídas do PDF
            if edital.get('pdf_info'):
                pdf_info = edital['pdf_info']
                
                if pdf_info.get('datas_encontradas'):
                    formatted += f"   📅 Datas no PDF: {', '.join(pdf_info['datas_encontradas'][:3])}\n"
                if pdf_info.get('prazos_encontrados'):
                    formatted += f"   ⏰ Prazos: {', '.join(pdf_info['prazos_encontrados'][:2])}\n"
                if pdf_info.get('valores_encontrados'):
                    formatted += f"   💰 Valores: {', '.join(pdf_info['valores_encontrados'][:2])}\n"
                if pdf_info.get('objetivo'):
                    objetivo = pdf_info['objetivo']
                    if len(objetivo) > 80:
                        formatted += f"   🎯 Objetivo: {objetivo[:80]}... (📄 Texto completo disponível)\n"
                    else:
                        formatted += f"   🎯 Objetivo: {objetivo}\n"
                if pdf_info.get('area_tema'):
                    area = pdf_info['area_tema']
                    if len(area) > 60:
                        formatted += f"   🔬 Área: {area[:60]}... (📄 Texto completo disponível)\n"
                    else:
                        formatted += f"   🔬 Área: {area}\n"
                    
            if edital.get('pdf_baixado'):
                formatted += f"   📄 PDF: Baixado ✅\n"
                # Adicionar link do PDF se disponível
                if edital.get('pdf_url'):
                    formatted += f"   🔗 Link PDF: {edital['pdf_url']}\n"
                elif edital.get('url') and edital['url'].lower().endswith('.pdf'):
                    formatted += f"   🔗 Link PDF: {edital['url']}\n"
            elif edital.get('url') and edital['url'].lower().endswith('.pdf'):
                formatted += f"   📄 PDF: Disponível (não baixado)\n"
                formatted += f"   🔗 Link PDF: {edital['url']}\n"
            formatted += "\n"
            
        if len(editais) > 5:
            formatted += f"... e mais {len(editais) - 5} oportunidades\n"
            
        return formatted
        
    def cleanup(self):
        """Limpa recursos"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Driver fechado com sucesso")
            except:
                pass

def send_email_unified(msg_text: str, subject: str = "🚀 Scraping Unificado - Novas Oportunidades!"):
    """Envia email com os resultados unificados"""
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
            
        logger.info(f"✅ Email enviado com sucesso para {msg['To']}!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao enviar email: {e}")
        return False

def main():
    """Função principal"""
    logger.info("=" * 60)
    logger.info("🚀 SCRAPER UNIFICADO - EDITAIS E CHAMADAS")
    logger.info("=" * 60)
    
    scraper = ScraperUnificado()
    
    try:
        # Configurar driver
        scraper.setup_driver()
        
        # Executar scraping
        scraper.run_scraping()
        
        # Salvar resultados
        scraper.save_results()
        
        # Preparar email
        if scraper.results['total_editais'] > 0:
            email_content = scraper._generate_summary()
            
            # Enviar email se as variáveis estiverem configuradas
            if 'EMAIL_USER' in os.environ and 'EMAIL_PASS' in os.environ:
                logger.info("📧 Enviando email...")
                if send_email_unified(email_content):
                    logger.info("✅ Processo concluído com sucesso!")
                else:
                    logger.warning("⚠️ Scraping concluído, mas email não foi enviado")
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
