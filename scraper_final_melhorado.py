#!/usr/bin/env python3
"""
Scraper Final Melhorado - Sistema Completo de Extração
======================================================

Versão 3.2 - Configurado para enviar para clevioferreira@gmail.com
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

# Importar o gerador de resumos
from gerador_resumo_melhorado import GeradorResumoMelhorado

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_final.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScraperFinalMelhorado:
    """Scraper final com todas as melhorias e correções"""
    
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
            chromedriver_autoinstaller.install()
            
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
            logger.info("🚀 Iniciando scraping final melhorado...")
            
            # UFMG
            try:
                self.results['ufmg'] = self._scrape_ufmg()
                logger.info(f"✅ UFMG: {len(self.results['ufmg'])} editais extraídos")
            except Exception as e:
                logger.error(f"❌ Erro UFMG: {e}")
                self.results['ufmg'] = []
                
            # FAPEMIG
            try:
                self.results['fapemig'] = self._scrape_fapemig()
                logger.info(f"✅ FAPEMIG: {len(self.results['fapemig'])} chamadas extraídas")
            except Exception as e:
                logger.error(f"❌ Erro FAPEMIG: {e}")
                self.results['fapemig'] = []
                
            # CNPq
            try:
                self.results['cnpq'] = self._scrape_cnpq()
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
            
    def _scrape_ufmg(self) -> List[Dict]:
        """Scraper específico para UFMG"""
        logger.info("🚀 Iniciando extração UFMG...")
        
        try:
            self.driver.get("https://www.ufmg.br/prograd/editais-chamadas/")
            time.sleep(3)
            
            editais = []
            
            # Procurar por links de editais
            links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*=".pdf"], a[href*="edital"]')
            
            for link in links[:10]:  # Limitar a 10 para não sobrecarregar
                try:
                    titulo = link.text.strip()
                    href = link.get_attribute("href")
                    
                    if titulo and href and ("edital" in titulo.lower() or "pdf" in href.lower()):
                        edital = {
                            'titulo': titulo,
                            'url': href,
                            'fonte': 'UFMG',
                            'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        # Tentar extrair data próxima
                        try:
                            parent = link.find_element(By.XPATH, "./..")
                            parent_text = parent.text
                            date_match = re.search(r'\d{2}/\d{2}/\d{4}', parent_text)
                            if date_match:
                                edital['data'] = date_match.group()
                        except:
                            edital['data'] = "Data não encontrada"
                            
                        editais.append(edital)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar link UFMG: {e}")
                    continue
                    
            return editais
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair UFMG: {e}")
            return []
            
    def _scrape_fapemig(self) -> List[Dict]:
        """Scraper específico para FAPEMIG - CORRIGIDO DUPLICATAS"""
        logger.info("🚀 Iniciando extração FAPEMIG...")
        
        try:
            self.driver.get("http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/")
            time.sleep(3)
            
            chamadas = []
            titulos_processados = set()  # Para evitar duplicatas
            
            # Procurar por títulos de chamadas - ESTRATÉGIA MELHORADA
            titulos = self.driver.find_elements(By.CSS_SELECTOR, 'h1, h2, h3, h4, h5, h6')
            
            for titulo in titulos:
                try:
                    texto = titulo.text.strip()
                    
                    # Verificar se já processamos este título
                    if texto in titulos_processados:
                        continue
                        
                    if texto and any(palavra in texto.lower() for palavra in ['chamada', 'edital', 'oportunidade']):
                        # Adicionar ao set de processados
                        titulos_processados.add(texto)
                        
                        chamada = {
                            'titulo': texto,
                            'fonte': 'FAPEMIG',
                            'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        # Procurar link próximo - ESTRATÉGIA MELHORADA
                        try:
                            # Procurar em diferentes níveis da hierarquia
                            parent = titulo.find_element(By.XPATH, "./..")
                            links = parent.find_elements(By.TAG_NAME, "a")
                            
                            for link in links:
                                href = link.get_attribute("href")
                                if href and href.startswith("http") and "#" in href:
                                    chamada['url'] = href
                                    break
                                    
                            # Se não encontrou, procurar no próximo nível
                            if 'url' not in chamada:
                                grandparent = parent.find_element(By.XPATH, "./..")
                                links = grandparent.find_elements(By.TAG_NAME, "a")
                                for link in links:
                                    href = link.get_attribute("href")
                                    if href and href.startswith("http") and "#" in href:
                                        chamada['url'] = href
                                        break
                                        
                        except:
                            chamada['url'] = "Link não encontrado"
                            
                        chamadas.append(chamada)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar título FAPEMIG: {e}")
                    continue
                    
            logger.info(f"✅ FAPEMIG: {len(chamadas)} chamadas únicas extraídas")
            return chamadas
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair FAPEMIG: {e}")
            return []
            
    def _scrape_cnpq(self) -> List[Dict]:
        """Scraper específico para CNPq - MELHORADO EXTRAÇÃO DE LINKS"""
        logger.info("🚀 Iniciando extração CNPq...")
        
        try:
            self.driver.get("http://memoria2.cnpq.br/web/guest/chamadas-publicas")
            time.sleep(3)
            
            chamadas = []
            
            # ESTRATÉGIA MELHORADA: Procurar por diferentes tipos de elementos
            # 1. Títulos de chamadas
            titulos = self.driver.find_elements(By.XPATH, '//h4[contains(text(), "CHAMADA") or contains(text(), "Chamada")]')
            
            for titulo in titulos[:8]:  # Aumentar limite
                try:
                    texto = titulo.text.strip()
                    
                    if texto:
                        chamada = {
                            'titulo': texto,
                            'fonte': 'CNPq',
                            'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        # Procurar período próximo
                        try:
                            parent = titulo.find_element(By.XPATH, "./..")
                            parent_text = parent.text
                            periodo_match = re.search(r'\d{2}/\d{2}/\d{4}\s*a\s*\d{2}/\d{2}/\d{4}', parent_text)
                            if periodo_match:
                                chamada['periodo_inscricao'] = periodo_match.group()
                        except:
                            chamada['periodo_inscricao'] = "Período não encontrado"
                            
                        # ESTRATÉGIA MELHORADA PARA LINKS
                        try:
                            # Procurar em diferentes níveis
                            parent = titulo.find_element(By.XPATH, "./..")
                            
                            # 1. Procurar por links diretos
                            links = parent.find_elements(By.TAG_NAME, "a")
                            for link in links:
                                href = link.get_attribute("href")
                                texto_link = link.text.strip()
                                if href and href.startswith("http"):
                                    chamada['url_detalhes'] = href
                                    chamada['tipo_link'] = "Link direto"
                                    break
                                    
                            # 2. Se não encontrou, procurar por botões
                            if 'url_detalhes' not in chamada:
                                botoes = parent.find_elements(By.CSS_SELECTOR, 'button, input[type="button"], .btn')
                                for botao in botoes:
                                    onclick = botao.get_attribute("onclick")
                                    if onclick and "window.open" in onclick:
                                        # Extrair URL do onclick
                                        url_match = re.search(r"window\.open\('([^']+)'", onclick)
                                        if url_match:
                                            chamada['url_detalhes'] = url_match.group(1)
                                            chamada['tipo_link'] = "Botão onclick"
                                            break
                                            
                            # 3. Procurar no próximo nível da hierarquia
                            if 'url_detalhes' not in chamada:
                                grandparent = parent.find_element(By.XPATH, "./..")
                                links = grandparent.find_elements(By.TAG_NAME, "a")
                                for link in links:
                                    href = link.get_attribute("href")
                                    if href and href.startswith("http"):
                                        chamada['url_detalhes'] = href
                                        chamada['tipo_link'] = "Link próximo nível"
                                        break
                                        
                        except Exception as e:
                            logger.warning(f"⚠️ Erro ao extrair link CNPq: {e}")
                            chamada['url_detalhes'] = "Link não encontrado"
                            
                        chamadas.append(chamada)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar título CNPq: {e}")
                    continue
                    
            logger.info(f"✅ CNPq: {len(chamadas)} chamadas extraídas")
            return chamadas
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair CNPq: {e}")
            return []
            
    def save_results(self):
        """Salva os resultados em arquivos"""
        try:
            # Salvar JSON completo
            with open("resultados_finais.json", "w", encoding="utf-8") as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
                
            # Gerar resumo melhorado
            gerador = GeradorResumoMelhorado(self.results)
            resumo = gerador.gerar_resumo_completo()
            
            # Salvar resumo em texto
            with open("relatorio_final.txt", "w", encoding="utf-8") as f:
                f.write(resumo)
                
            logger.info("✅ Resultados salvos com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar resultados: {e}")
            
    def cleanup(self):
        """Limpa recursos"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Driver fechado com sucesso")
            except:
                pass

def send_email_final(msg_text: str, subject: str = "🚀 RELATÓRIO FINAL - Oportunidades Encontradas!"):
    """Envia email com o relatório final para clevioferreira@gmail.com"""
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = os.environ['EMAIL_USER']
        
        # CONFIGURAÇÃO DE EMAIL: Enviar para clevioferreira@gmail.com
        email_destino = os.environ.get('EMAIL_DESTINO', 'clevioferreira@gmail.com')
        msg['To'] = email_destino
        
        text_part = MIMEText(msg_text, 'plain', 'utf-8')
        msg.attach(text_part)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
            server.send_message(msg)
            
        logger.info(f"✅ Email enviado com sucesso para: {email_destino}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao enviar email: {e}")
        return False

def main():
    """Função principal"""
    logger.info("=" * 60)
    logger.info("🚀 SCRAPER FINAL MELHORADO - EDITAIS E CHAMADAS")
    logger.info("=" * 60)
    
    scraper = ScraperFinalMelhorado()
    
    try:
        # Configurar driver
        scraper.setup_driver()
        
        # Executar scraping
        scraper.run_scraping()
        
        # Salvar resultados
        scraper.save_results()
        
        # Preparar email
        if scraper.results['total_editais'] > 0:
            # Ler o relatório gerado
            with open("relatorio_final.txt", "r", encoding="utf-8") as f:
                email_content = f.read()
            
            # Enviar email se as variáveis estiverem configuradas
            if 'EMAIL_USER' in os.environ and 'EMAIL_PASS' in os.environ:
                logger.info("📧 Enviando email...")
                if send_email_final(email_content):
                    logger.info("✅ Processo concluído com sucesso!")
                else:
                    logger.warning("⚠️ Scraping concluído, mas email não foi enviado")
            else:
                logger.warning("⚠️ Variáveis de email não configuradas")
                logger.info("📧 Conteúdo que seria enviado:")
                logger.info("-" * 40)
                logger.info(email_content[:500] + "...")
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
