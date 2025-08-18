from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time
import re
from datetime import datetime
from pathlib import Path

class ScraperFAPEMIG:
    def __init__(self, headless=True):
        """Inicializa o scraper FAPEMIG com Selenium"""
        self.url = "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/"
        self.headless = headless
        self.driver = None
        self.resultados = []
        
    def configurar_driver(self):
        """Configura o driver do Chrome"""
        options = Options()
        
        if self.headless:
            options.add_argument("--headless")
        
        # Configurações para melhor performance e compatibilidade
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # Configurações para ignorar problemas de SSL
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        
        # Configurações para melhor compatibilidade
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Configurações para evitar conflitos
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-extensions")
        
        try:
            self.driver = webdriver.Chrome(options=options)
            
            # Remove indicadores de automação
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Driver Chrome configurado com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar driver: {e}")
            return False
    
    def extrair_data_do_texto(self, texto):
        """Extrai datas do texto usando regex"""
        if not texto:
            return ""
        
        # Padrões para datas brasileiras
        padroes = [
            r'(\d{1,2}/\d{1,2}/\d{2,4})',  # Data única: 01/08/2025
            r'(\d{1,2}/\d{1,2}/\d{2,4})\s*(?:a|até|-)\s*(\d{1,2}/\d{1,2}/\d{2,4})',  # Período: 01/08/2025 a 30/09/2025
        ]
        
        for padrao in padroes:
            match = re.search(padrao, texto)
            if match:
                if len(match.groups()) == 2:
                    return f"{match.group(1)} a {match.group(2)}"
                else:
                    return match.group(1)
        
        return ""
    
    def extrair_links_pdf(self, elemento):
        """Extrai links de PDFs de um elemento"""
        try:
            links = elemento.find_elements(By.TAG_NAME, "a")
            pdfs = []
            
            for link in links:
                href = link.get_attribute("href")
                texto = link.text.strip()
                
                if href and (href.endswith('.pdf') or 'pdf' in href.lower()):
                    pdfs.append({
                        'url': href,
                        'texto': texto or 'PDF'
                    })
                elif href and ('download' in href.lower() or 'arquivo' in href.lower()):
                    pdfs.append({
                        'url': href,
                        'texto': texto or 'Download'
                    })
            
            return pdfs
        except Exception as e:
            print(f"⚠️ Erro ao extrair links PDF: {e}")
            return []
    
    def processar_bloco_chamada(self, bloco):
        """Processa um bloco de chamada individual"""
        try:
            chamada = {
                'titulo': '',
                'data_inclusao': '',
                'prazo_final': '',
                'numero_chamada': '',
                'pdfs': [],
                'texto_completo': '',
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat()
            }
            
            # Extrai título
            titulo = bloco.text.strip()
            if not titulo or len(titulo) < 10:  # Filtra títulos muito curtos
                return None
            
            chamada['titulo'] = titulo
            chamada['texto_completo'] = titulo
            
            # Busca por elementos irmãos para extrair detalhes
            elemento_atual = bloco
            elementos_processados = 0
            max_elementos = 15  # Limite para evitar loop infinito
            
            while elementos_processados < max_elementos:
                try:
                    # Pega o próximo elemento irmão
                    proximo = elemento_atual.find_element(By.XPATH, 'following-sibling::*[1]')
                    texto = proximo.text.strip()
                    
                    if not texto or proximo.tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        break
                    
                    chamada['texto_completo'] += "\n" + texto
                    
                    # Extrai informações específicas
                    texto_lower = texto.lower()
                    
                    # Data de inclusão
                    if any(palavra in texto_lower for palavra in ['data da inclusão', 'data da inclusao', 'incluído em']):
                        data = self.extrair_data_do_texto(texto)
                        if data:
                            chamada['data_inclusao'] = data
                    
                    # Prazo final
                    if any(palavra in texto_lower for palavra in ['prazo final', 'prazo para submissão', 'data limite', 'encerramento']):
                        data = self.extrair_data_do_texto(texto)
                        if data:
                            chamada['prazo_final'] = data
                    
                    # Número da chamada
                    if any(palavra in texto_lower for palavra in ['número da chamada', 'numero da chamada', 'chamada nº', 'chamada n°']):
                        numero = re.search(r'(\d+/\d+)', texto)
                        if numero:
                            chamada['numero_chamada'] = numero.group(1)
                    
                    # Links de PDF
                    pdfs_encontrados = self.extrair_links_pdf(proximo)
                    if pdfs_encontrados:
                        chamada['pdfs'].extend(pdfs_encontrados)
                    
                    elemento_atual = proximo
                    elementos_processados += 1
                    
                except NoSuchElementException:
                    break
                except Exception as e:
                    print(f"⚠️ Erro ao processar elemento: {e}")
                    break
            
            return chamada
            
        except Exception as e:
            print(f"❌ Erro ao processar bloco: {e}")
            return None
    
    def fazer_scroll_automatico(self):
        """Faz scroll automático para carregar todo o conteúdo"""
        print("🔄 Fazendo scroll automático...")
        
        # Scroll inicial
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Scroll progressivo
        altura_anterior = 0
        tentativas = 0
        max_tentativas = 10
        
        while tentativas < max_tentativas:
            altura_atual = self.driver.execute_script("return document.body.scrollHeight")
            
            if altura_atual == altura_anterior:
                tentativas += 1
            else:
                tentativas = 0
                altura_anterior = altura_atual
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        
        print("✅ Scroll concluído")
    
    def extrair_chamadas(self):
        """Extrai todas as chamadas da página"""
        try:
            print(f"🌐 Acessando: {self.url}")
            self.driver.get(self.url)
            
            # Aguarda carregamento inicial
            time.sleep(5)
            
            # Verifica se a página carregou
            print(f"📄 Título da página: {self.driver.title}")
            print(f"📏 URL atual: {self.driver.current_url}")
            
            # Faz scroll para carregar todo o conteúdo
            self.fazer_scroll_automatico()
            
            # Busca por elementos de título com múltiplas estratégias
            print("🔍 Buscando por elementos de chamadas...")
            
            # Estratégia 1: Seletores específicos
            seletores_especificos = [
                "//h5[contains(text(), 'CHAMADA') or contains(text(), 'Edital')]",
                "//h6[contains(text(), 'CHAMADA') or contains(text(), 'Edital')]",
                "//div[contains(@class, 'chamada') or contains(@class, 'edital')]//h5",
                "//div[contains(@class, 'chamada') or contains(@class, 'edital')]//h6"
            ]
            
            # Estratégia 2: Seletores genéricos
            seletores_genericos = [
                "//h5",
                "//h6",
                "//div[contains(@class, 'title')]",
                "//div[contains(@class, 'header')]"
            ]
            
            # Estratégia 3: Busca por texto
            seletores_texto = [
                "//*[contains(text(), 'CHAMADA')]",
                "//*[contains(text(), 'Edital')]",
                "//*[contains(text(), 'FAPEMIG')]"
            ]
            
            blocos_encontrados = []
            
            # Tenta seletores específicos primeiro
            for seletor in seletores_especificos:
                try:
                    blocos = self.driver.find_elements(By.XPATH, seletor)
                    if blocos:
                        blocos_encontrados.extend(blocos)
                        print(f"✅ Encontrados {len(blocos)} blocos com seletor específico: {seletor}")
                        break
                except Exception as e:
                    print(f"⚠️ Erro com seletor específico {seletor}: {e}")
                    continue
            
            # Se não encontrou, tenta genéricos
            if not blocos_encontrados:
                for seletor in seletores_genericos:
                    try:
                        blocos = self.driver.find_elements(By.XPATH, seletor)
                        if blocos:
                            blocos_encontrados.extend(blocos)
                            print(f"✅ Encontrados {len(blocos)} blocos com seletor genérico: {seletor}")
                            break
                    except Exception as e:
                        print(f"⚠️ Erro com seletor genérico {seletor}: {e}")
                        continue
            
            # Se ainda não encontrou, tenta por texto
            if not blocos_encontrados:
                for seletor in seletores_texto:
                    try:
                        blocos = self.driver.find_elements(By.XPATH, seletor)
                        if blocos:
                            blocos_encontrados.extend(blocos)
                            print(f"✅ Encontrados {len(blocos)} blocos com seletor de texto: {seletor}")
                            break
                    except Exception as e:
                        print(f"⚠️ Erro com seletor de texto {seletor}: {e}")
                        continue
            
            # Remove duplicatas
            blocos_unicos = []
            textos_vistos = set()
            
            for bloco in blocos_encontrados:
                texto = bloco.text.strip()
                if texto and texto not in textos_vistos:
                    textos_vistos.add(texto)
                    blocos_unicos.append(bloco)
            
            print(f"📊 Total de blocos únicos encontrados: {len(blocos_unicos)}")
            
            # Mostra alguns exemplos
            for i, bloco in enumerate(blocos_unicos[:5]):
                texto = bloco.text.strip()[:100]
                print(f"   Exemplo {i+1}: {texto}...")
            
            # Processa cada bloco
            for i, bloco in enumerate(blocos_unicos, 1):
                print(f"📝 Processando bloco {i}/{len(blocos_unicos)}")
                chamada = self.processar_bloco_chamada(bloco)
                
                if chamada:
                    self.resultados.append(chamada)
                    print(f"   ✅ {chamada['titulo'][:50]}...")
                else:
                    print(f"   ❌ Bloco {i} não processado")
            
            print(f"\n🎯 Total de chamadas extraídas: {len(self.resultados)}")
            
        except Exception as e:
            print(f"❌ Erro durante extração: {e}")
    
    def salvar_resultados(self, nome_arquivo=None):
        """Salva os resultados em arquivo JSON"""
        if not nome_arquivo:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_arquivo = f"fapemig_selenium_{timestamp}.json"
        
        resultado_final = {
            'fapemig': self.resultados,
            'total_chamadas': len(self.resultados),
            'timestamp': datetime.now().isoformat(),
            'url_fonte': self.url,
            'metodo': 'Selenium'
        }
        
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(resultado_final, f, ensure_ascii=False, indent=2)
            print(f"💾 Resultados salvos em: {nome_arquivo}")
            return nome_arquivo
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")
            return None
    
    def executar(self):
        """Executa o scraper completo"""
        print("🚀 Iniciando Scraper FAPEMIG com Selenium")
        print("=" * 60)
        
        if not self.configurar_driver():
            return False
        
        try:
            self.extrair_chamadas()
            
            if self.resultados:
                arquivo_salvo = self.salvar_resultados()
                if arquivo_salvo:
                    print(f"\n🎉 Scraping concluído! {len(self.resultados)} chamadas extraídas")
                    return True
            else:
                print("❌ Nenhuma chamada foi extraída")
                return False
                
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 Driver fechado")
    
    def mostrar_resultados(self):
        """Mostra os resultados de forma legível"""
        if not self.resultados:
            print("❌ Nenhum resultado para mostrar")
            return
        
        print(f"\n📋 RESULTADOS FAPEMIG ({len(self.resultados)} chamadas):")
        print("=" * 80)
        
        for i, chamada in enumerate(self.resultados, 1):
            print(f"\n{i}. {chamada['titulo']}")
            
            if chamada['numero_chamada']:
                print(f"   🔢 Número: {chamada['numero_chamada']}")
            
            if chamada['data_inclusao']:
                print(f"   📅 Inclusão: {chamada['data_inclusao']}")
            
            if chamada['prazo_final']:
                print(f"   ⏰ Prazo: {chamada['prazo_final']}")
            
            if chamada['pdfs']:
                print(f"   📎 PDFs ({len(chamada['pdfs'])}):")
                for pdf in chamada['pdfs']:
                    print(f"      • {pdf['texto']}: {pdf['url']}")
            else:
                print(f"   📎 PDFs: Nenhum encontrado")
            
            print(f"   📝 Texto: {chamada['texto_completo'][:100]}...")

def main():
    """Função principal"""
    print("🔍 Scraper FAPEMIG com Selenium")
    print("=" * 50)
    
    # Cria e executa o scraper
    scraper = ScraperFAPEMIG(headless=True)
    
    if scraper.executar():
        scraper.mostrar_resultados()
    else:
        print("❌ Falha na execução do scraper")

if __name__ == "__main__":
    main()
