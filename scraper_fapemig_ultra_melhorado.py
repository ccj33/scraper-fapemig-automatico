#!/usr/bin/env python3
"""
Scraper ULTRA-MELHORADO para FAPEMIG
=====================================

Versão que acessa CADA chamada individualmente para extrair
TODOS os PDFs e informações detalhadas.
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

class ScraperFAPEMIGUltraMelhorado:
    def __init__(self):
        self.driver = None
        self.resultados = {
            'fapemig': [],
            'timestamp': datetime.now().isoformat()
        }
        self.wait = None
        
    def configurar_navegador(self):
        """Configura o navegador Chrome para extração ULTRA-MELHORADA"""
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
            self.driver.implicitly_wait(20)
            self.wait = WebDriverWait(self.driver, 30)
            
            print("✅ Navegador configurado para extração ULTRA-MELHORADA da FAPEMIG!")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def extrair_fapemig_ultra_melhorado(self):
        """Extrai FAPEMIG com acesso individual a cada chamada"""
        print("🔍 Extraindo FAPEMIG (acesso individual a cada chamada)...")
        
        try:
            # Primeiro, acessar a página principal para listar todas as chamadas
            url_principal = "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/"
            self.driver.get(url_principal)
            time.sleep(15)  # Aguardar carregamento completo
            
            print(f"   Título: {self.driver.title}")
            print(f"   URL atual: {self.driver.current_url}")
            
            # Buscar por todas as chamadas na página principal
            chamadas_principais = self.driver.find_elements(By.CSS_SELECTOR, 'h5, h4, h3')
            
            chamadas_encontradas = []
            for chamada in chamadas_principais:
                try:
                    texto = chamada.text.strip()
                    
                    if texto and any(palavra in texto.upper() for palavra in ['CHAMADA', 'PORTARIA']):
                        # Extrair informações básicas da chamada
                        info_basica = self.extrair_info_basica_fapemig(chamada)
                        if info_basica:
                            chamadas_encontradas.append(info_basica)
                            print(f"   📋 Encontrada: {info_basica['titulo'][:60]}...")
                        
                        # Limitar a 10 chamadas para teste
                        if len(chamadas_encontradas) >= 10:
                            break
                            
                except Exception as e:
                    continue
            
            print(f"   ✅ {len(chamadas_encontradas)} chamadas encontradas na página principal")
            
            # Agora acessar cada chamada individualmente para extrair PDFs
            for i, chamada in enumerate(chamadas_encontradas, 1):
                try:
                    print(f"\n   🔍 Acessando chamada {i}/{len(chamadas_encontradas)}: {chamada['titulo'][:50]}...")
                    
                    # Acessar a página da chamada individual
                    info_completa = self.acessar_chamada_individual(chamada)
                    if info_completa:
                        self.resultados['fapemig'].append(info_completa)
                        print(f"   ✅ PDFs extraídos: {len(info_completa['pdfs_disponiveis'])} arquivos")
                    
                    # Aguardar entre acessos
                    time.sleep(5)
                    
                except Exception as e:
                    print(f"   ❌ Erro ao acessar chamada: {e}")
                    continue
            
            print(f"\n✅ FAPEMIG: {len(self.resultados['fapemig'])} chamadas processadas com PDFs")
            
        except Exception as e:
            print(f"❌ Erro ao extrair FAPEMIG: {e}")
    
    def extrair_info_basica_fapemig(self, elemento):
        """Extrai informações básicas de uma chamada da FAPEMIG"""
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
            
            resultado = {
                'titulo': titulo,
                'numero': numero,
                'data_inclusao': data_inclusao,
                'prazo_final': prazo_final,
                'texto_completo': texto_completo[:300] + "..." if len(texto_completo) > 300 else texto_completo
            }
            
            return resultado
            
        except Exception as e:
            print(f"   ❌ Erro ao extrair info básica: {e}")
            return None
    
    def acessar_chamada_individual(self, chamada):
        """Acessa uma chamada individual para extrair PDFs"""
        try:
            # Tentar encontrar o link para a chamada individual
            # Como o site da FAPEMIG não tem links diretos, vamos usar uma abordagem diferente
            
            # Buscar por elementos que possam conter links
            elementos_com_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="chamada"], a[href*="edital"], a[href*="portaria"]')
            
            link_chamada = None
            for elem in elementos_com_links:
                texto = elem.text.strip()
                if texto and chamada['titulo'][:30] in texto:
                    link_chamada = elem.get_attribute('href')
                    break
            
            if link_chamada:
                print(f"      🔗 Link encontrado: {link_chamada}")
                # Acessar a página da chamada
                self.driver.get(link_chamada)
                time.sleep(10)
                
                # Extrair PDFs da página da chamada
                pdfs = self.extrair_pdfs_da_chamada()
                
                # Extrair informações detalhadas
                info_detalhada = self.extrair_info_detalhada_chamada()
                
                # Combinar informações
                resultado = {
                    'titulo': chamada['titulo'],
                    'numero': chamada['numero'],
                    'data_inclusao': chamada['data_inclusao'],
                    'prazo_final': chamada['prazo_final'],
                    'fonte': 'FAPEMIG',
                    'data_coleta': datetime.now().isoformat(),
                    'pdfs_disponiveis': pdfs,
                    'info_detalhada': info_detalhada,
                    'link_chamada': link_chamada
                }
                
                return resultado
            else:
                print(f"      ⚠️  Link não encontrado, usando dados básicos")
                # Se não encontrar link, usar dados básicos com busca por PDFs na página principal
                pdfs = self.buscar_pdfs_na_pagina_principal(chamada['titulo'])
                
                resultado = {
                    'titulo': chamada['titulo'],
                    'numero': chamada['numero'],
                    'data_inclusao': chamada['data_inclusao'],
                    'prazo_final': chamada['prazo_final'],
                    'fonte': 'FAPEMIG',
                    'data_coleta': datetime.now().isoformat(),
                    'pdfs_disponiveis': pdfs,
                    'info_detalhada': {},
                    'link_chamada': None
                }
                
                return resultado
                
        except Exception as e:
            print(f"      ❌ Erro ao acessar chamada individual: {e}")
            return None
    
    def extrair_pdfs_da_chamada(self):
        """Extrai PDFs de uma página de chamada individual"""
        pdfs = []
        
        try:
            # Buscar por links que contenham .pdf
            links_pdf = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*=".pdf"]')
            
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
            botoes_download = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="download"], a[href*="arquivo"]')
            
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
            print(f"      ❌ Erro ao extrair PDFs da chamada: {e}")
        
        return pdfs
    
    def buscar_pdfs_na_pagina_principal(self, titulo_chamada):
        """Busca PDFs relacionados a uma chamada na página principal"""
        pdfs = []
        
        try:
            # Voltar para a página principal
            self.driver.get("http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/")
            time.sleep(10)
            
            # Buscar por elementos que contenham o título da chamada
            elementos_titulo = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{titulo_chamada[:30]}')]")
            
            for elem in elementos_titulo:
                try:
                    # Pegar o elemento pai que contém mais contexto
                    elemento_pai = elem.find_element(By.XPATH, "./..")
                    
                    # Buscar por PDFs neste contexto
                    links_pdf = elemento_pai.find_elements(By.CSS_SELECTOR, 'a[href*=".pdf"]')
                    
                    for link in links_pdf:
                        href = link.get_attribute('href')
                        texto = link.text.strip()
                        
                        if href and texto and href not in [p['url'] for p in pdfs]:
                            pdfs.append({
                                'nome': texto,
                                'url': href,
                                'tipo': 'PDF'
                            })
                    
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"      ❌ Erro ao buscar PDFs na página principal: {e}")
        
        return pdfs
    
    def extrair_info_detalhada_chamada(self):
        """Extrai informações detalhadas de uma chamada"""
        info = {}
        
        try:
            # Extrair descrição
            descricoes = self.driver.find_elements(By.CSS_SELECTOR, 'p, .descricao, .texto')
            for desc in descricoes:
                texto = desc.text.strip()
                if texto and len(texto) > 50:
                    info['descricao'] = texto
                    break
            
            # Extrair links para vídeos
            links_video = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="youtube"], a[href*="video"]')
            if links_video:
                info['links_video'] = [link.get_attribute('href') for link in links_video]
            
            # Extrair outras informações relevantes
            texto_pagina = self.driver.page_source
            if "DOWNLOAD DOS ARQUIVOS" in texto_pagina:
                info['tem_anexos'] = True
            
        except Exception as e:
            print(f"      ❌ Erro ao extrair info detalhada: {e}")
        
        return info
    
    def salvar_resultados(self):
        """Salva os resultados ULTRA-MELHORADOS da FAPEMIG"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"fapemig_ultra_melhorado_{timestamp}.json"
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Resultados ULTRA-MELHORADOS da FAPEMIG salvos em: {nome_arquivo}")
            return nome_arquivo
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return None
    
    def executar_extracao_ultra_melhorada(self):
        """Executa extração ULTRA-MELHORADA da FAPEMIG"""
        print("🚀 INICIANDO EXTRAÇÃO ULTRA-MELHORADA DA FAPEMIG")
        print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
        
        if not self.configurar_navegador():
            return False
        
        try:
            # Extrair FAPEMIG com acesso individual a cada chamada
            self.extrair_fapemig_ultra_melhorado()
            
            # Salvar resultados
            arquivo = self.salvar_resultados()
            
            # Fechar navegador
            if self.driver:
                self.driver.quit()
            
            print(f"🎉 EXTRAÇÃO ULTRA-MELHORADA DA FAPEMIG CONCLUÍDA!")
            print(f"📊 Total de chamadas: {len(self.resultados['fapemig'])}")
            print(f"💾 Arquivo salvo: {arquivo}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na extração: {e}")
            if self.driver:
                self.driver.quit()
            return False

if __name__ == "__main__":
    scraper = ScraperFAPEMIGUltraMelhorado()
    scraper.executar_extracao_ultra_melhorada()
