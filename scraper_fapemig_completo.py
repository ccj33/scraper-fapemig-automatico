#!/usr/bin/env python3
"""
Scraper Completo para FAPEMIG
==============================

Extrai TODOS os PDFs e informações detalhadas das chamadas da FAPEMIG.
"""

import time
import json
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import chromedriver_autoinstaller

class ScraperFAPEMIGCompleto:
    def __init__(self):
        self.driver = None
        self.resultados = {
            'fapemig': [],
            'timestamp': datetime.now().isoformat()
        }
        self.wait = None
        
    def configurar_navegador(self):
        """Configura o navegador Chrome para extração completa"""
        try:
            chromedriver_autoinstaller.install()
            options = Options()
            
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            # Configurações para SSL
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--ignore-certificate-errors')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(15)
            self.wait = WebDriverWait(self.driver, 25)
            
            print("✅ Navegador configurado para extração completa da FAPEMIG!")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def extrair_fapemig_completo(self):
        """Extrai TODAS as informações da FAPEMIG com PDFs"""
        print("🔍 Extraindo FAPEMIG (extração COMPLETA com PDFs)...")
        
        try:
            url = "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/"
            self.driver.get(url)
            time.sleep(10)  # Aguardar carregamento completo
            
            print(f"   Título: {self.driver.title}")
            print(f"   URL atual: {self.driver.current_url}")
            
            # Buscar por todas as chamadas
            chamadas = self.driver.find_elements(By.CSS_SELECTOR, 'h5, h4, h3')
            
            for chamada in chamadas:
                try:
                    texto = chamada.text.strip()
                    
                    if texto and any(palavra in texto.upper() for palavra in ['CHAMADA', 'PORTARIA']):
                        # Extrair informações completas da chamada
                        info_completa = self.extrair_info_fapemig_completa(chamada)
                        if info_completa:
                            self.resultados['fapemig'].append(info_completa)
                            print(f"✅ FAPEMIG: {info_completa['titulo'][:60]}...")
                        
                        # Limitar a 15 chamadas para teste
                        if len(self.resultados['fapemig']) >= 15:
                            break
                            
                except Exception as e:
                    continue
            
            print(f"✅ FAPEMIG: {len(self.resultados['fapemig'])} chamadas extraídas com PDFs")
            
        except Exception as e:
            print(f"❌ Erro ao extrair FAPEMIG: {e}")
    
    def extrair_info_fapemig_completa(self, elemento):
        """Extrai informações COMPLETAS de uma chamada da FAPEMIG"""
        try:
            # Pegar o elemento pai que contém mais contexto
            try:
                elemento_pai = elemento.find_element(By.XPATH, "./..")
                texto_completo = elemento_pai.text.strip()
            except:
                texto_completo = elemento.text.strip()
            
            # Extrair título
            titulo = elemento.text.strip()
            
            # Extrair número da chamada
            numero_match = re.search(r'(\d{3}/\d{4})', titulo)
            numero = numero_match.group(1) if numero_match else ""
            
            # Extrair datas
            padrao_data = r'(\d{2}/\d{2}/\d{4})'
            datas = re.findall(padrao_data, texto_completo)
            data_inclusao = datas[0] if datas else ""
            prazo_final = ""
            
            # Buscar por prazo final
            if "Prazo final" in texto_completo:
                prazo_match = re.search(r'Prazo final.*?(\d{2}/\d{2}/\d{4})', texto_completo)
                if prazo_match:
                    prazo_final = prazo_match.group(1)
            
            # Extrair descrição
            linhas = texto_completo.split('\n')
            descricao = ""
            for linha in linhas:
                if linha.strip() and len(linha.strip()) > 20 and "Prazo final" not in linha:
                    descricao = linha.strip()
                    break
            
            if not descricao:
                descricao = titulo
            
            # Verificar se tem anexos
            tem_anexos = "DOWNLOAD DOS ARQUIVOS" in texto_completo
            
            # Extrair links para PDFs
            pdfs_disponiveis = self.extrair_pdfs_fapemig(elemento_pai)
            
            # Extrair links para vídeos
            links_video = self.extrair_links_video(texto_completo)
            
            resultado = {
                'titulo': titulo,
                'numero': numero,
                'descricao': descricao,
                'data_inclusao': data_inclusao,
                'prazo_final': prazo_final,
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat(),
                'tem_anexos': tem_anexos,
                'pdfs_disponiveis': pdfs_disponiveis,
                'links_video': links_video,
                'texto_completo': texto_completo[:500] + "..." if len(texto_completo) > 500 else texto_completo
            }
            
            return resultado
            
        except Exception as e:
            print(f"   ❌ Erro ao extrair info FAPEMIG: {e}")
            return None
    
    def extrair_pdfs_fapemig(self, elemento_pai):
        """Extrai todos os PDFs disponíveis de uma chamada"""
        pdfs = []
        
        try:
            # Buscar por links que contenham .pdf
            links_pdf = elemento_pai.find_elements(By.CSS_SELECTOR, 'a[href*=".pdf"]')
            
            for link in links_pdf:
                href = link.get_attribute('href')
                texto = link.text.strip()
                
                if href and texto:
                    pdfs.append({
                        'nome': texto,
                        'url': href,
                        'tipo': 'PDF'
                    })
            
            # Buscar por botões de download
            botoes_download = elemento_pai.find_elements(By.CSS_SELECTOR, 'a[href*="download"], a[href*="arquivo"]')
            
            for botao in botoes_download:
                href = botao.get_attribute('href')
                texto = botao.text.strip()
                
                if href and texto and href not in [p['url'] for p in pdfs]:
                    pdfs.append({
                        'nome': texto,
                        'url': href,
                        'tipo': 'Download'
                    })
            
        except Exception as e:
            print(f"   ❌ Erro ao extrair PDFs: {e}")
        
        return pdfs
    
    def extrair_links_video(self, texto_completo):
        """Extrai links para vídeos explicativos"""
        links_video = []
        
        try:
            # Buscar por links do YouTube
            padrao_youtube = r'https?://(?:www\.)?youtube\.com/[^\s]+'
            links = re.findall(padrao_youtube, texto_completo)
            
            for link in links:
                links_video.append({
                    'plataforma': 'YouTube',
                    'url': link,
                    'tipo': 'Vídeo Explicativo'
                })
            
        except Exception as e:
            print(f"   ❌ Erro ao extrair links de vídeo: {e}")
        
        return links_video
    
    def salvar_resultados(self):
        """Salva os resultados completos da FAPEMIG"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"fapemig_completo_{timestamp}.json"
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Resultados completos da FAPEMIG salvos em: {nome_arquivo}")
            return nome_arquivo
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return None
    
    def executar_extracao_completa(self):
        """Executa extração completa da FAPEMIG"""
        print("🚀 INICIANDO EXTRAÇÃO COMPLETA DA FAPEMIG")
        print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
        
        if not self.configurar_navegador():
            return False
        
        try:
            # Extrair FAPEMIG com todas as informações
            self.extrair_fapemig_completo()
            
            # Salvar resultados
            arquivo = self.salvar_resultados()
            
            # Fechar navegador
            if self.driver:
                self.driver.quit()
            
            print(f"🎉 EXTRAÇÃO COMPLETA DA FAPEMIG CONCLUÍDA!")
            print(f"📊 Total de chamadas: {len(self.resultados['fapemig'])}")
            print(f"💾 Arquivo salvo: {arquivo}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na extração: {e}")
            if self.driver:
                self.driver.quit()
            return False

if __name__ == "__main__":
    scraper = ScraperFAPEMIGCompleto()
    scraper.executar_extracao_completa()
