#!/usr/bin/env python3
"""
Scraper Rápido para Editais - Versão Otimizada
===============================================

Versão otimizada para execução rápida, com timeouts reduzidos
e configurações para ambiente CI/CD.
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

class ScraperRapido:
    def __init__(self):
        self.driver = None
        self.resultados = {
            'ufmg': [],
            'fapemig': [],
            'cnpq': [],
            'timestamp': datetime.now().isoformat()
        }
        self.wait = None
        
    def configurar_navegador(self):
        """Configura o navegador Chrome otimizado para velocidade"""
        try:
            chromedriver_autoinstaller.install()
            options = Options()
            
            # 🔥 CONFIGURAÇÕES PARA VELOCIDADE MÁXIMA
            options.add_argument('--headless')  # Sem interface gráfica
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')  # Não carregar imagens
            options.add_argument('--window-size=800,600')  # Janela menor
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            # 🔒 CONFIGURAÇÕES PARA SSL
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-insecure-localhost')
            options.add_argument('--disable-web-security')
            
            self.driver = webdriver.Chrome(options=options)
            
            # ⚡ TIMEOUTS ULTRA-RÁPIDOS
            self.driver.implicitly_wait(2)  # Era 10
            self.wait = WebDriverWait(self.driver, 5)  # Era 15
            
            print("✅ Navegador configurado para velocidade máxima!")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def extrair_ufmg_rapido(self):
        """Extrai editais da UFMG de forma rápida"""
        print("🔍 Extraindo UFMG (modo rápido)...")
        
        try:
            self.driver.get('https://www.ufmg.br/prograd/editais-chamadas/')
            time.sleep(1)  # Era 3
            
            # Buscar apenas links principais
            editais = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*=".pdf"]')
            
            for edital in editais[:5]:  # Limitar a 5 resultados para teste
                try:
                    texto = edital.text.strip()
                    href = edital.get_attribute('href')
                    
                    if texto and href and any(palavra in texto.lower() for palavra in ['edital', 'chamada']):
                        resultado = {
                            'titulo': texto,
                            'descricao': texto,
                            'link_pdf': href,
                            'data_limite': "",
                            'fonte': 'UFMG',
                            'data_coleta': datetime.now().isoformat()
                        }
                        
                        self.resultados['ufmg'].append(resultado)
                        print(f"✅ UFMG: {texto[:50]}...")
                        
                except Exception as e:
                    continue
            
            print(f"✅ UFMG: {len(self.resultados['ufmg'])} editais encontrados")
            
        except Exception as e:
            print(f"❌ Erro UFMG: {e}")
    
    def extrair_fapemig_rapido(self):
        """Extrai oportunidades da FAPEMIG de forma rápida"""
        print("🔍 Extraindo FAPEMIG (modo rápido)...")
        
        # 🔧 URLs alternativas para FAPEMIG
        urls_fapemig = [
            'https://fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
            'https://fapemig.br/pt/',
            'https://fapemig.br/',
            'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/?hl=pt-BR'
        ]
        
        for url in urls_fapemig:
            try:
                print(f"   Tentando: {url}")
                self.driver.get(url)
                time.sleep(2)
                
                # Verificar se carregou corretamente
                if "O site não é seguro" in self.driver.title or "chrome-error" in self.driver.current_url:
                    print(f"   ❌ {url} - Problema de SSL")
                    continue
                
                # Buscar por diferentes seletores
                seletores = ['h5', 'h4', 'h3', '.chamada', '.oportunidade', 'a']
                
                for seletor in seletores:
                    try:
                        elementos = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                        
                        for elem in elementos[:3]:  # Limitar a 3
                            texto = elem.text.strip()
                            
                            if texto and len(texto) > 10 and any(palavra in texto.upper() for palavra in ['CHAMADA', 'EDITAL', 'OPORTUNIDADE']):
                                resultado = {
                                    'titulo': texto,
                                    'descricao': texto,
                                    'link_pdf': "",
                                    'data_limite': "",
                                    'fonte': 'FAPEMIG',
                                    'data_coleta': datetime.now().isoformat()
                                }
                                
                                # Verificar se já existe
                                if not any(r['titulo'] == texto for r in self.resultados['fapemig']):
                                    self.resultados['fapemig'].append(resultado)
                                    print(f"✅ FAPEMIG: {texto[:50]}...")
                                
                                if len(self.resultados['fapemig']) >= 3:  # Limitar a 3
                                    break
                        
                        if len(self.resultados['fapemig']) >= 3:
                            break
                            
                    except Exception as e:
                        continue
                
                if len(self.resultados['fapemig']) > 0:
                    break  # Se encontrou algo, para de tentar outras URLs
                    
            except Exception as e:
                print(f"   ❌ Erro ao tentar {url}: {e}")
                continue
        
        print(f"✅ FAPEMIG: {len(self.resultados['fapemig'])} oportunidades encontradas")
    
    def extrair_cnpq_rapido(self):
        """Extrai chamadas do CNPq de forma rápida"""
        print("🔍 Extraindo CNPq (modo rápido)...")
        
        # 🔧 URLs alternativas para CNPq
        urls_cnpq = [
            'https://www.cnpq.br/web/guest/chamadas-publicas',
            'https://cnpq.br/web/guest/chamadas-publicas',
            'https://www.cnpq.br/',
            'http://memoria2.cnpq.br/web/guest/chamadas-publicas'
        ]
        
        for url in urls_cnpq:
            try:
                print(f"   Tentando: {url}")
                self.driver.get(url)
                time.sleep(2)
                
                # Verificar se carregou corretamente
                if "O site não é seguro" in self.driver.title or "chrome-error" in self.driver.current_url:
                    print(f"   ❌ {url} - Problema de SSL")
                    continue
                
                # Buscar por diferentes seletores
                seletores = ['h4', 'h3', 'h5', '.chamada', '.oportunidade', '.edital']
                
                for seletor in seletores:
                    try:
                        elementos = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                        
                        for elem in elementos[:3]:  # Limitar a 3
                            texto = elem.text.strip()
                            
                            if texto and len(texto) > 10 and any(palavra in texto.upper() for palavra in ['CHAMADA', 'EDITAL', 'OPORTUNIDADE', 'PROGRAMA']):
                                resultado = {
                                    'titulo': texto,
                                    'descricao': texto,
                                    'link_pdf': "",
                                    'data_limite': "",
                                    'fonte': 'CNPq',
                                    'data_coleta': datetime.now().isoformat()
                                }
                                
                                # Verificar se já existe
                                if not any(r['titulo'] == texto for r in self.resultados['cnpq']):
                                    self.resultados['cnpq'].append(resultado)
                                    print(f"✅ CNPq: {texto[:50]}...")
                                
                                if len(self.resultados['cnpq']) >= 3:  # Limitar a 3
                                    break
                        
                        if len(self.resultados['cnpq']) >= 3:
                            break
                            
                    except Exception as e:
                        continue
                
                if len(self.resultados['cnpq']) > 0:
                    break  # Se encontrou algo, para de tentar outras URLs
                    
            except Exception as e:
                print(f"   ❌ Erro ao tentar {url}: {e}")
                continue
        
        print(f"✅ CNPq: {len(self.resultados['cnpq'])} chamadas encontradas")
    
    def salvar_resultados(self):
        """Salva os resultados rapidamente"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"editais_rapidos_{timestamp}.json"
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Resultados salvos em: {nome_arquivo}")
            return nome_arquivo
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return None
    
    def executar_extracao_rapida(self):
        """Executa extração rápida"""
        print("🚀 INICIANDO EXTRAÇÃO RÁPIDA")
        print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
        
        if not self.configurar_navegador():
            return False
        
        try:
            # ⚡ EXECUÇÃO RÁPIDA
            self.extrair_ufmg_rapido()
            self.extrair_fapemig_rapido()
            self.extrair_cnpq_rapido()
            
            # Salvar resultados
            arquivo_salvo = self.salvar_resultados()
            
            # Resumo rápido
            total = len(self.resultados['ufmg']) + len(self.resultados['fapemig']) + len(self.resultados['cnpq'])
            print(f"\n📊 TOTAL: {total} itens em tempo recorde!")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 Navegador fechado")

def main():
    """Função principal"""
    print("⚡ SCRAPER RÁPIDO - VERSÃO OTIMIZADA")
    print("=" * 50)
    
    scraper = ScraperRapido()
    inicio = datetime.now()
    
    sucesso = scraper.executar_extracao_rapida()
    
    fim = datetime.now()
    duracao = (fim - inicio).total_seconds()
    
    print(f"\n⏱️  Duração total: {duracao:.1f} segundos")
    
    if sucesso:
        print("🎉 Extração rápida concluída!")
    else:
        print("💥 Extração falhou!")

if __name__ == "__main__":
    main()
