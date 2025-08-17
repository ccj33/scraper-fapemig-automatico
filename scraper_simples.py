#!/usr/bin/env python3
"""
Scraper Simples para Editais e Chamadas
=======================================

Sistema básico que coleta links de PDFs dos sites:
- FAPEMIG (Fundação de Amparo à Pesquisa de Minas Gerais)
- CNPq (Conselho Nacional de Desenvolvimento Científico e Tecnológico)
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import chromedriver_autoinstaller

class ScraperSimples:
    def __init__(self):
        self.driver = None
        self.resultados = {
            'fapemig': [],
            'cnpq': [],
            'timestamp': datetime.now().isoformat()
        }
        
    def configurar_navegador(self):
        """Configura o navegador Chrome em modo headless"""
        try:
            chromedriver_autoinstaller.install()
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(10)
            print("✅ Navegador configurado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def extrair_fapemig(self):
        """Extrai oportunidades da FAPEMIG"""
        print("\n🔍 Extraindo oportunidades da FAPEMIG...")
        
        try:
            # Tentar diferentes URLs da FAPEMIG
            urls_fapemig = [
                "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/",
                "https://fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/",
                "http://www.fapemig.br/pt/",
                "https://fapemig.br/pt/"
            ]
            
            oportunidades = []
            
            for url in urls_fapemig:
                try:
                    print(f"   Tentando: {url}")
                    self.driver.get(url)
                    time.sleep(5)  # Aguardar mais tempo para carregar
                    
                    # Estratégia 1: Buscar por links com texto específico
                    links = self.driver.find_elements(By.TAG_NAME, "a")
                    
                    for link in links:
                        try:
                            href = link.get_attribute('href')
                            texto = link.text.strip()
                            
                            if href and texto and len(texto) > 3:
                                # Verificar se é um link para PDF ou edital
                                if any(palavra in texto.lower() for palavra in ['edital', 'chamada', 'oportunidade', 'programa', 'bolsa', 'pesquisa']):
                                    if href.endswith('.pdf') or 'pdf' in href.lower():
                                        oportunidades.append({
                                            'titulo': texto,
                                            'link_pdf': href,
                                            'fonte': 'FAPEMIG',
                                            'url_origem': url,
                                            'data_coleta': datetime.now().isoformat()
                                        })
                                    elif 'chamadas' in href.lower() or 'editais' in href.lower() or 'oportunidades' in href.lower():
                                        # Link para página de detalhes
                                        oportunidades.append({
                                            'titulo': texto,
                                            'link_detalhes': href,
                                            'fonte': 'FAPEMIG',
                                            'url_origem': url,
                                            'data_coleta': datetime.now().isoformat()
                                        })
                        except Exception as e:
                            continue
                    
                    # Estratégia 2: Buscar por elementos com classes específicas
                    try:
                        elementos_chamada = self.driver.find_elements(By.CLASS_NAME, "chamada")
                        for elem in elementos_chamada:
                            links_elem = elem.find_elements(By.TAG_NAME, "a")
                            for link in links_elem:
                                href = link.get_attribute('href')
                                texto = link.text.strip()
                                if href and texto:
                                    oportunidades.append({
                                        'titulo': texto,
                                        'link_detalhes': href,
                                        'fonte': 'FAPEMIG',
                                        'url_origem': url,
                                        'data_coleta': datetime.now().isoformat()
                                    })
                    except:
                        pass
                    
                    # Se encontrou oportunidades, parar de tentar outras URLs
                    if oportunidades:
                        break
                        
                except Exception as e:
                    print(f"   Erro ao acessar {url}: {e}")
                    continue
            
            # Remover duplicatas
            oportunidades_unicas = []
            links_vistos = set()
            for op in oportunidades:
                if op.get('link_pdf') not in links_vistos and op.get('link_detalhes') not in links_vistos:
                    oportunidades_unicas.append(op)
                    if op.get('link_pdf'):
                        links_vistos.add(op.get('link_pdf'))
                    if op.get('link_detalhes'):
                        links_vistos.add(op.get('link_detalhes'))
            
            self.resultados['fapemig'] = oportunidades_unicas
            print(f"✅ FAPEMIG: {len(oportunidades_unicas)} oportunidades encontradas")
            
        except Exception as e:
            print(f"❌ Erro ao extrair FAPEMIG: {e}")
    
    def extrair_cnpq(self):
        """Extrai oportunidades do CNPq"""
        print("\n🔍 Extraindo oportunidades do CNPq...")
        
        try:
            # Tentar diferentes URLs do CNPq
            urls_cnpq = [
                "https://www.gov.br/cnpq/pt-br/acesso-a-informacao/acoes-e-programas/programas/chamadas-publicas",
                "https://www.gov.br/cnpq/pt-br/acesso-a-informacao/acoes-e-programas/programas",
                "https://www.gov.br/cnpq/pt-br/acesso-a-informacao/acoes-e-programas",
                "https://www.gov.br/cnpq/pt-br/"
            ]
            
            oportunidades = []
            
            for url in urls_cnpq:
                try:
                    print(f"   Tentando: {url}")
                    self.driver.get(url)
                    time.sleep(5)  # Aguardar mais tempo para carregar
                    
                    # Estratégia 1: Buscar por links com texto específico
                    try:
                        links = self.driver.find_elements(By.TAG_NAME, "a")
                        
                        for link in links:
                            try:
                                href = link.get_attribute('href')
                                texto = link.text.strip()
                                
                                if href and texto and len(texto) > 3:
                                    # Verificar se é um link para PDF ou edital
                                    if any(palavra in texto.lower() for palavra in ['edital', 'chamada', 'oportunidade', 'programa', 'chamada pública', 'bolsa', 'pesquisa']):
                                        if href.endswith('.pdf') or 'pdf' in href.lower():
                                            oportunidades.append({
                                                'titulo': texto,
                                                'link_pdf': href,
                                                'fonte': 'CNPq',
                                                'url_origem': url,
                                                'data_coleta': datetime.now().isoformat()
                                            })
                                        elif 'chamas' in href.lower() or 'editais' in href.lower() or 'oportunidades' in href.lower():
                                            # Link para página de detalhes
                                            oportunidades.append({
                                                'titulo': texto,
                                                'link_detalhes': href,
                                                'fonte': 'CNPq',
                                                'url_origem': url,
                                                'data_coleta': datetime.now().isoformat()
                                            })
                            except Exception as e:
                                continue
                    except Exception as e:
                        print(f"   Erro ao processar links: {e}")
                        continue
                    
                    # Estratégia 2: Buscar por elementos com classes específicas
                    try:
                        elementos_chamada = self.driver.find_elements(By.CLASS_NAME, "chamada")
                        for elem in elementos_chamada:
                            try:
                                links_elem = elem.find_elements(By.TAG_NAME, "a")
                                for link in links_elem:
                                    href = link.get_attribute('href')
                                    texto = link.text.strip()
                                    if href and texto:
                                        oportunidades.append({
                                            'titulo': texto,
                                            'link_detalhes': href,
                                            'fonte': 'CNPq',
                                            'url_origem': url,
                                            'data_coleta': datetime.now().isoformat()
                                        })
                            except:
                                continue
                    except:
                        pass
                    
                    # Se encontrou oportunidades, parar de tentar outras URLs
                    if oportunidades:
                        break
                        
                except Exception as e:
                    print(f"   Erro ao acessar {url}: {e}")
                    continue
            
            # Remover duplicatas
            oportunidades_unicas = []
            links_vistos = set()
            for op in oportunidades:
                if op.get('link_pdf') not in links_vistos and op.get('link_detalhes') not in links_vistos:
                    oportunidades_unicas.append(op)
                    if op.get('link_pdf'):
                        links_vistos.add(op.get('link_pdf'))
                    if op.get('link_detalhes'):
                        links_vistos.add(op.get('link_detalhes'))
            
            self.resultados['cnpq'] = oportunidades_unicas
            print(f"✅ CNPq: {len(oportunidades_unicas)} oportunidades encontradas")
            
        except Exception as e:
            print(f"❌ Erro ao extrair CNPq: {e}")
            # Mesmo com erro, definir lista vazia para não quebrar o processo
            self.resultados['cnpq'] = []
    
    def salvar_resultados(self):
        """Salva os resultados em arquivo JSON"""
        try:
            nome_arquivo = f"oportunidades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Resultados salvos em: {nome_arquivo}")
            return nome_arquivo
        except Exception as e:
            print(f"❌ Erro ao salvar resultados: {e}")
            return None
    
    def executar(self):
        """Executa o scraper completo"""
        print("🚀 Iniciando Scraper Simples...")
        
        if not self.configurar_navegador():
            return False
        
        try:
            # Extrair dados dos sites
            self.extrair_fapemig()
            self.extrair_cnpq()
            
            # Salvar resultados
            arquivo = self.salvar_resultados()
            
            # Resumo final
            total_fapemig = len(self.resultados['fapemig'])
            total_cnpq = len(self.resultados['cnpq'])
            
            print(f"\n📊 RESUMO FINAL:")
            print(f"   FAPEMIG: {total_fapemig} oportunidades")
            print(f"   CNPq: {total_cnpq} oportunidades")
            print(f"   Total: {total_fapemig + total_cnpq} oportunidades")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 Navegador fechado")

def main():
    """Função principal"""
    scraper = ScraperSimples()
    sucesso = scraper.executar()
    
    if sucesso:
        print("\n✅ Scraper executado com sucesso!")
    else:
        print("\n❌ Erro na execução do scraper!")

if __name__ == "__main__":
    main()
