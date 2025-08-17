#!/usr/bin/env python3
"""
Scraper Melhorado - Extração Completa de Editais e Chamadas
==========================================================

Coleta dados COMPLETOS de:
- UFMG: Editais e Chamadas com PDFs
- FAPEMIG: Oportunidades com detalhes
- CNPq: Chamadas Públicas com prazos

Versão 2.0 - Extração inteligente e legível
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
import re
from typing import List, Dict, Optional
import random

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_melhorado.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BaseScraperMelhorado:
    """Classe base melhorada para todos os scrapers"""
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        
    def safe_find_element(self, by: By, value: str):
        """Encontra elemento de forma segura"""
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            return None
            
    def safe_find_elements(self, by: By, value: str):
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
            
    def random_delay(self, min_seconds: float = 2.0, max_seconds: float = 4.0):
        """Delay aleatório para não sobrecarregar os sites"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def extract_pdf_content(self, pdf_url: str) -> Dict:
        """Tenta extrair conteúdo de PDFs"""
        try:
            logger.info(f"📄 Tentando extrair PDF: {pdf_url}")
            
            # Acessar URL do PDF
            self.driver.get(pdf_url)
            self.random_delay(3, 5)
            
            # Tentar extrair texto da página
            page_text = self.driver.page_source
            
            # Procurar por informações importantes
            info = {
                'valor': self._extract_valor_from_text(page_text),
                'prazo': self._extract_prazo_from_text(page_text),
                'objetivo': self._extract_objetivo_from_text(page_text),
                'publico_alvo': self._extract_publico_from_text(page_text)
            }
            
            return info
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair PDF: {e}")
            return {}
            
    def _extract_valor_from_text(self, text: str) -> str:
        """Extrai valores do texto"""
        patterns = [
            r'R\$\s*[\d.,]+',
            r'valor.*?R\$\s*[\d.,]+',
            r'recurso.*?R\$\s*[\d.,]+',
            r'bolsa.*?R\$\s*[\d.,]+'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group().strip()
        return "Valor não informado"
        
    def _extract_prazo_from_text(self, text: str) -> str:
        """Extrai prazos do texto"""
        patterns = [
            r'prazo.*?\d{2}/\d{2}/\d{4}',
            r'até.*?\d{2}/\d{2}/\d{4}',
            r'encerramento.*?\d{2}/\d{2}/\d{4}',
            r'\d{2}/\d{2}/\d{4}.*?prazo'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group().strip()
        return "Prazo não informado"
        
    def _extract_objetivo_from_text(self, text: str) -> str:
        """Extrai objetivo do texto"""
        patterns = [
            r'objetivo.*?[.!]',
            r'finalidade.*?[.!]',
            r'proposta.*?[.!]'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group().strip()
        return "Objetivo não informado"
        
    def _extract_publico_from_text(self, text: str) -> str:
        """Extrai público-alvo do texto"""
        patterns = [
            r'público.*?[.!]',
            r'destinatários.*?[.!]',
            r'beneficiários.*?[.!]'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group().strip()
        return "Público não informado"

class UFMGScraperMelhorado(BaseScraperMelhorado):
    """Scraper melhorado para UFMG"""
    
    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
        self.base_url = "https://www.ufmg.br/prograd/editais-chamadas/"
        
    def extract_editais(self) -> List[Dict]:
        """Extrai editais da UFMG com informações completas"""
        logger.info("🚀 Iniciando extração UFMG melhorada...")
        
        try:
            self.driver.get(self.base_url)
            self.random_delay(3, 5)
            
            editais = []
            page = 1
            
            while page <= 5:  # Limite de 5 páginas
                logger.info(f"📄 Processando página {page}...")
                
                page_editais = self._extract_page_editais()
                editais.extend(page_editais)
                
                if not self._go_to_next_page():
                    break
                    
                page += 1
                self.random_delay(3, 5)
                
            logger.info(f"✅ UFMG: {len(editais)} editais extraídos")
            return editais
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair UFMG: {e}")
            return []
            
    def _extract_page_editais(self) -> List[Dict]:
        """Extrai editais de uma página com informações completas"""
        editais = []
        
        try:
            # Procurar por links de editais
            edital_links = self.safe_find_elements(By.CSS_SELECTOR, 'a[href*=".pdf"], a[href*="edital"], a[href*="Edital"]')
            
            for link in edital_links:
                try:
                    titulo = self.safe_get_text(link)
                    href = self.safe_get_attribute(link, "href")
                    
                    if titulo and href and ("edital" in titulo.lower() or "pdf" in href.lower()):
                        # Extrair informações completas
                        info_completa = self._extract_edital_info(link, titulo, href)
                        editais.append(info_completa)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar link UFMG: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Erro ao extrair página UFMG: {e}")
            
        return editais
        
    def _extract_edital_info(self, link_element, titulo: str, href: str) -> Dict:
        """Extrai informações completas do edital"""
        info = {
            'titulo_completo': titulo,
            'url': href,
            'fonte': 'UFMG',
            'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # Procurar data próxima ao link
            data = self._extract_date_near_link(link_element)
            info['data'] = data
            
            # Se for PDF, tentar extrair conteúdo
            if href.lower().endswith('.pdf'):
                pdf_info = self.extract_pdf_content(href)
                info.update(pdf_info)
                
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair detalhes UFMG: {e}")
            
        return info
        
    def _extract_date_near_link(self, link_element) -> str:
        """Extrai data próxima ao link do edital"""
        try:
            # Procurar por texto com data próximo ao link
            parent = link_element.find_element(By.XPATH, "./..")
            parent_text = self.safe_get_text(parent)
            
            # Padrões de data mais específicos
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
            next_links = self.safe_find_elements(By.XPATH, '//a[contains(text(), "Próxima") or contains(text(), "»")]')
            
            for link in next_links:
                if link.is_enabled() and link.is_displayed():
                    link.click()
                    return True
                    
        except:
            pass
            
        return False

def main():
    """Função principal para teste"""
    logger.info("=" * 60)
    logger.info("🚀 SCRAPER MELHORADO - TESTE")
    logger.info("=" * 60)
    
    # Por enquanto, apenas teste básico
    logger.info("✅ Scraper melhorado criado com sucesso!")
    logger.info("📋 Próximos passos:")
    logger.info("   1. Implementar FAPEMIG e CNPq melhorados")
    logger.info("   2. Adicionar extração de PDFs")
    logger.info("   3. Melhorar formatação do resumo")
    logger.info("   4. Testar no GitHub Actions")

if __name__ == "__main__":
    main()
