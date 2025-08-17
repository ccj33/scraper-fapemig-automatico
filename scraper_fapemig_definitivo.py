#!/usr/bin/env python3
"""
Scraper MEGA-INTELIGENTE para FAPEMIG
======================================

Versão que analisa o HTML COMPLETO da página para extrair
TODOS os PDFs e informações detalhadas das chamadas.
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

class ScraperFAPEMIGDefinitivo:
    def __init__(self):
        self.driver = None
        self.resultados = {
            'fapemig': [],
            'timestamp': datetime.now().isoformat()
        }
        self.wait = None
        
    def configurar_navegador(self):
        """Configura o navegador Chrome para extração MEGA-INTELIGENTE"""
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
            
            print("✅ Navegador configurado para extração MEGA-INTELIGENTE da FAPEMIG!")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def extrair_fapemig_definitivo(self):
        """Extrai FAPEMIG com análise MEGA-INTELIGENTE do HTML"""
        print("🔍 Extraindo FAPEMIG (análise MEGA-INTELIGENTE do HTML)...")
        
        try:
            url = "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/"
            self.driver.get(url)
            time.sleep(15)  # Aguardar carregamento completo
            
            print(f"   Título: {self.driver.title}")
            print(f"   URL atual: {self.driver.current_url}")
            
            # Obter o HTML completo da página
            html_completo = self.driver.page_source
            print(f"   📄 HTML analisado: {len(html_completo)} caracteres")
            
            # Analisar o HTML para encontrar todas as chamadas e seus PDFs
            self.analisar_html_fapemig(html_completo)
            
            print(f"✅ FAPEMIG: {len(self.resultados['fapemig'])} chamadas extraídas com PDFs")
            
        except Exception as e:
            print(f"❌ Erro ao extrair FAPEMIG: {e}")
    
    def analisar_html_fapemig(self, html_completo):
        """Analisa o HTML completo para extrair chamadas e PDFs"""
        try:
            # Buscar por todas as chamadas na página
            chamadas = self.driver.find_elements(By.CSS_SELECTOR, 'h5, h4, h3')
            
            print(f"   📋 Encontradas {len(chamadas)} possíveis chamadas")
            
            for i, chamada in enumerate(chamadas, 1):
                try:
                    texto = chamada.text.strip()
                    
                    if texto and any(palavra in texto.upper() for palavra in ['CHAMADA', 'PORTARIA']):
                        print(f"\n   🔍 Processando chamada {i}: {texto[:60]}...")
                        
                        # Extrair informações completas da chamada
                        info_completa = self.extrair_chamada_completa(chamada, html_completo)
                        if info_completa:
                            self.resultados['fapemig'].append(info_completa)
                            print(f"   ✅ PDFs encontrados: {len(info_completa['pdfs_disponiveis'])} arquivos")
                        
                        # Limitar a 15 chamadas para teste
                        if len(self.resultados['fapemig']) >= 15:
                            break
                            
                except Exception as e:
                    print(f"   ❌ Erro ao processar chamada {i}: {e}")
                    continue
            
        except Exception as e:
            print(f"   ❌ Erro ao analisar HTML: {e}")
    
    def extrair_chamada_completa(self, elemento_chamada, html_completo):
        """Extrai informações COMPLETAS de uma chamada incluindo PDFs"""
        try:
            # Pegar o elemento pai que contém mais contexto
            try:
                elemento_pai = elemento_chamada.find_element(By.XPATH, "./..")
                texto_completo = elemento_pai.text.strip()
            except:
                texto_completo = elemento_chamada.text.strip()
            
            # Extrair título
            titulo = elemento_chamada.text.strip()
            
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
            
            # 🔥 BUSCA MEGA-INTELIGENTE POR PDFs
            pdfs_disponiveis = self.buscar_pdfs_mega_inteligente(elemento_pai, titulo, html_completo)
            
            # Extrair links para vídeos
            links_video = self.extrair_links_video(texto_completo)
            
            # Verificar se tem anexos
            tem_anexos = "DOWNLOAD DOS ARQUIVOS" in texto_completo or len(pdfs_disponiveis) > 0
            
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
            print(f"      ❌ Erro ao extrair chamada completa: {e}")
            return None
    
    def buscar_pdfs_mega_inteligente(self, elemento_pai, titulo_chamada, html_completo):
        """Busca MEGA-INTELIGENTE por PDFs relacionados à chamada"""
        pdfs = []
        
        try:
            print(f"      🔍 Buscando PDFs para: {titulo_chamada[:40]}...")
            
            # 1. Buscar por links diretos .pdf no elemento pai
            links_pdf_diretos = elemento_pai.find_elements(By.CSS_SELECTOR, 'a[href*=".pdf"]')
            for link in links_pdf_diretos:
                href = link.get_attribute('href')
                texto = link.text.strip()
                
                if href and texto:
                    pdfs.append({
                        'nome': texto,
                        'url': href,
                        'tipo': 'PDF Direto',
                        'metodo': 'Elemento Pai'
                    })
                    print(f"         📄 PDF direto encontrado: {texto}")
            
            # 2. Buscar por botões de download
            botoes_download = elemento_pai.find_elements(By.CSS_SELECTOR, 'a[href*="download"], a[href*="arquivo"]')
            for botao in botoes_download:
                href = botao.get_attribute('href')
                texto = botao.text.strip()
                
                if href and texto and href not in [p['url'] for p in pdfs]:
                    pdfs.append({
                        'nome': texto,
                        'url': href,
                        'tipo': 'Download',
                        'metodo': 'Botão Download'
                    })
                    print(f"         📄 Download encontrado: {texto}")
            
            # 3. 🔥 BUSCA MEGA-INTELIGENTE NO HTML COMPLETO
            if not pdfs:  # Se não encontrou PDFs pelos métodos tradicionais
                print(f"         🔍 Busca MEGA-INTELIGENTE no HTML...")
                pdfs_html = self.buscar_pdfs_no_html_completo(titulo_chamada, html_completo)
                pdfs.extend(pdfs_html)
            
            # 4. Buscar por elementos próximos que possam conter PDFs
            if not pdfs:
                print(f"         🔍 Buscando elementos próximos...")
                pdfs_proximos = self.buscar_pdfs_elementos_proximos(elemento_pai)
                pdfs.extend(pdfs_proximos)
            
            # 5. Buscar por texto que mencione PDFs
            if not pdfs:
                print(f"         🔍 Buscando por menções a PDFs...")
                pdfs_texto = self.buscar_pdfs_por_texto(titulo_chamada, texto_completo)
                pdfs.extend(pdfs_texto)
            
            print(f"         ✅ Total de PDFs encontrados: {len(pdfs)}")
            
        except Exception as e:
            print(f"         ❌ Erro na busca MEGA-INTELIGENTE: {e}")
        
        return pdfs
    
    def buscar_pdfs_no_html_completo(self, titulo_chamada, html_completo):
        """Busca PDFs no HTML completo usando regex avançado"""
        pdfs = []
        
        try:
            # Buscar por padrões de PDFs no HTML
            padrao_pdf = r'<a[^>]*href="([^"]*\.pdf)"[^>]*>([^<]+)</a>'
            matches = re.findall(padrao_pdf, html_completo, re.IGNORECASE)
            
            for url, texto in matches:
                # Verificar se o PDF está relacionado à chamada
                if self.pdf_relacionado_chamada(titulo_chamada, texto, url):
                    pdfs.append({
                        'nome': texto.strip(),
                        'url': url,
                        'tipo': 'PDF HTML',
                        'metodo': 'Regex HTML'
                    })
                    print(f"            📄 PDF no HTML: {texto.strip()}")
            
        except Exception as e:
            print(f"            ❌ Erro na busca no HTML: {e}")
        
        return pdfs
    
    def pdf_relacionado_chamada(self, titulo_chamada, texto_pdf, url_pdf):
        """Verifica se um PDF está relacionado a uma chamada específica"""
        try:
            # Extrair número da chamada
            numero_chamada = re.search(r'(\d{3}/\d{4})', titulo_chamada)
            if numero_chamada:
                numero = numero_chamada.group(1)
                # Verificar se o número aparece no texto do PDF ou na URL
                if numero in texto_pdf or numero in url_pdf:
                    return True
            
            # Verificar por palavras-chave
            palavras_chave = ['chamada', 'edital', 'anexo', 'portaria']
            for palavra in palavras_chave:
                if palavra.lower() in texto_pdf.lower():
                    return True
            
            # Verificar se o título da chamada aparece no texto do PDF
            palavras_titulo = titulo_chamada.split()[:5]  # Primeiras 5 palavras
            for palavra in palavras_titulo:
                if len(palavra) > 3 and palavra.lower() in texto_pdf.lower():
                    return True
            
            return False
            
        except Exception as e:
            return False
    
    def buscar_pdfs_elementos_proximos(self, elemento_pai):
        """Busca PDFs em elementos próximos ao elemento pai"""
        pdfs = []
        
        try:
            # Buscar por elementos irmãos
            try:
                elemento_avo = elemento_pai.find_element(By.XPATH, "./..")
                elementos_irmaos = elemento_avo.find_elements(By.CSS_SELECTOR, '*')
                
                for elem in elementos_irmaos:
                    try:
                        links_pdf = elem.find_elements(By.CSS_SELECTOR, 'a[href*=".pdf"]')
                        for link in links_pdf:
                            href = link.get_attribute('href')
                            texto = link.text.strip()
                            
                            if href and texto and href not in [p['url'] for p in pdfs]:
                                pdfs.append({
                                    'nome': texto,
                                    'url': href,
                                    'tipo': 'PDF Próximo',
                                    'metodo': 'Elemento Próximo'
                                })
                                print(f"            📄 PDF próximo: {texto}")
                    except:
                        continue
                        
            except:
                pass
            
        except Exception as e:
            print(f"            ❌ Erro na busca por elementos próximos: {e}")
        
        return pdfs
    
    def buscar_pdfs_por_texto(self, titulo_chamada, texto_completo):
        """Busca PDFs mencionados no texto da chamada"""
        pdfs = []
        
        try:
            # Buscar por menções a PDFs no texto
            if "DOWNLOAD DOS ARQUIVOS" in texto_completo:
                # Tentar encontrar nomes de arquivos mencionados
                padrao_arquivo = r'([A-Z][^.]*\.pdf)'
                matches = re.findall(padrao_arquivo, texto_completo)
                
                for nome_arquivo in matches:
                    pdfs.append({
                        'nome': nome_arquivo,
                        'url': f"http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/",
                        'tipo': 'PDF Mencionado',
                        'metodo': 'Texto da Chamada',
                        'instrucoes': 'Acesse a página para encontrar este arquivo'
                    })
                    print(f"            📄 PDF mencionado: {nome_arquivo}")
            
        except Exception as e:
            print(f"            ❌ Erro na busca por texto: {e}")
        
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
            print(f"      ❌ Erro ao extrair links de vídeo: {e}")
        
        return links_video
    
    def salvar_resultados(self):
        """Salva os resultados MEGA-INTELIGENTES da FAPEMIG"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"fapemig_mega_inteligente_{timestamp}.json"
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Resultados MEGA-INTELIGENTES da FAPEMIG salvos em: {nome_arquivo}")
            return nome_arquivo
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return None
    
    def executar_extracao_mega_inteligente(self):
        """Executa extração MEGA-INTELIGENTE da FAPEMIG"""
        print("🚀 INICIANDO EXTRAÇÃO MEGA-INTELIGENTE DA FAPEMIG")
        print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
        
        if not self.configurar_navegador():
            return False
        
        try:
            # Extrair FAPEMIG com análise MEGA-INTELIGENTE
            self.extrair_fapemig_definitivo()
            
            # Salvar resultados
            arquivo = self.salvar_resultados()
            
            # Fechar navegador
            if self.driver:
                self.driver.quit()
            
            print(f"🎉 EXTRAÇÃO MEGA-INTELIGENTE DA FAPEMIG CONCLUÍDA!")
            print(f"📊 Total de chamadas: {len(self.resultados['fapemig'])}")
            print(f"💾 Arquivo salvo: {arquivo}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na extração: {e}")
            if self.driver:
                self.driver.quit()
            return False

if __name__ == "__main__":
    scraper = ScraperFAPEMIGDefinitivo()
    scraper.executar_extracao_mega_inteligente()
