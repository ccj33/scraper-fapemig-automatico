#!/usr/bin/env python3
"""
🔥 SCRAPER MEGA-ULTRA-MELHORADO PARA CNPq - SOLUÇÃO DEFINITIVA
================================================================

Versão que resolve TODOS os problemas baseada na estrutura HTML real:
✅ Captura TODOS os blocos de chamadas
✅ Extrai títulos, descrições e períodos de inscrição
✅ Encontra TODOS os links importantes (Chamada, Anexo, FAQ, etc.)
✅ Funciona com a estrutura HTML real identificada
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

class ScraperCNPqSolucaoDefinitiva:
    def __init__(self):
        self.driver = None
        self.resultados = {
            'chamadas_cnpq': [],
            'timestamp': datetime.now().isoformat(),
            'total_chamadas': 0,
            'total_links': 0
        }
        self.wait = None
        
    def configurar_navegador(self):
        """Configura o navegador Chrome para extração MEGA-ULTRA-MELHORADA"""
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
            
            print("✅ Navegador configurado para SOLUÇÃO DEFINITIVA do CNPq!")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def extrair_cnpq_solucao_definitiva(self):
        """Extrai CNPq com SOLUÇÃO DEFINITIVA baseada na estrutura HTML real"""
        print("🔥 Extraindo CNPq com SOLUÇÃO DEFINITIVA...")
        
        try:
            url = "http://memoria2.cnpq.br/web/guest/chamadas-publicas"
            self.driver.get(url)
            time.sleep(15)  # Aguardar carregamento completo
            
            print(f"   Título: {self.driver.title}")
            print(f"   URL atual: {self.driver.current_url}")
            
            # 🔥 MÉTODO 1: Buscar por blocos de chamadas usando XPath
            self.buscar_chamadas_metodo_1()
            
            # 🔥 MÉTODO 2: Buscar por padrões específicos no HTML
            if len(self.resultados['chamadas_cnpq']) < 10:  # Se não encontrou muitos
                self.buscar_chamadas_metodo_2()
            
            # 🔥 MÉTODO 3: Buscar por elementos específicos do CNPq
            if len(self.resultados['chamadas_cnpq']) < 15:  # Se ainda não encontrou muitos
                self.buscar_chamadas_metodo_3()
            
            print(f"✅ CNPq: {len(self.resultados['chamadas_cnpq'])} chamadas extraídas com SOLUÇÃO DEFINITIVA!")
            
        except Exception as e:
            print(f"❌ Erro ao extrair CNPq: {e}")
    
    def buscar_chamadas_metodo_1(self):
        """MÉTODO 1: Buscar por blocos de chamadas usando XPath baseado na estrutura real"""
        print("   🔍 MÉTODO 1: Buscando blocos de chamadas com XPath...")
        
        try:
            # Buscar por blocos de chamadas usando XPath baseado na estrutura real
            xpath_patterns = [
                "//h4[contains(., 'CHAMADA') or contains(., 'Chamada')]",
                "//h3[contains(., 'CHAMADA') or contains(., 'Chamada')]",
                "//h2[contains(., 'CHAMADA') or contains(., 'Chamada')]",
                "//div[contains(@class, 'chamada')]//h4",
                "//div[contains(@class, 'resultado')]//h4"
            ]
            
            chamadas_encontradas = []
            
            for xpath in xpath_patterns:
                try:
                    elementos = self.driver.find_elements(By.XPATH, xpath)
                    for elemento in elementos:
                        texto = elemento.text.strip()
                        if self.eh_chamada_valida(texto):
                            chamadas_encontradas.append(elemento)
                except:
                    continue
            
            print(f"      📋 Encontradas {len(chamadas_encontradas)} possíveis chamadas")
            
            # Processar cada chamada encontrada
            for i, elemento in enumerate(chamadas_encontradas, 1):
                try:
                    info_completa = self.extrair_chamada_completa(elemento, i)
                    if info_completa and info_completa not in self.resultados['chamadas_cnpq']:
                        self.resultados['chamadas_cnpq'].append(info_completa)
                        print(f"      ✅ Chamada {i}: {info_completa['titulo'][:50]}...")
                except Exception as e:
                    print(f"      ❌ Erro ao processar chamada {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"      ❌ Erro no método 1: {e}")
    
    def buscar_chamadas_metodo_2(self):
        """MÉTODO 2: Buscar por padrões específicos no HTML"""
        print("   🔍 MÉTODO 2: Buscando por padrões específicos...")
        
        try:
            # Buscar por texto que contenha padrões de chamadas
            html_completo = self.driver.page_source
            
            # Padrões para encontrar chamadas baseados na estrutura real
            padroes = [
                r'CHAMADA\s+[^<]+',
                r'Chamada\s+[^<]+',
                r'<h[234][^>]*>([^<]*CHAMADA[^<]*)</h[234]>',
                r'<h[234][^>]*>([^<]*Chamada[^<]*)</h[234]>'
            ]
            
            for padrao in padroes:
                matches = re.findall(padrao, html_completo, re.IGNORECASE)
                for match in matches:
                    print(f"      📋 Padrão encontrado: {match}")
                    
                    # Buscar o elemento que contém este padrão
                    elemento = self.buscar_elemento_por_texto(match)
                    if elemento:
                        info_completa = self.extrair_chamada_por_texto(match, elemento)
                        if info_completa and info_completa not in self.resultados['chamadas_cnpq']:
                            self.resultados['chamadas_cnpq'].append(info_completa)
                            
        except Exception as e:
            print(f"      ❌ Erro no método 2: {e}")
    
    def buscar_chamadas_metodo_3(self):
        """MÉTODO 3: Buscar por elementos específicos do CNPq"""
        print("   🔍 MÉTODO 3: Buscando elementos específicos do CNPq...")
        
        try:
            # Buscar por elementos com classes específicas do CNPq
            seletores_cnpq = [
                '.resultado-item',
                '.chamada-item',
                '.publicacao-item',
                '[data-tipo="chamada"]',
                '[data-tipo="publicacao"]',
                '.cnpq-chamada',
                '.cnpq-publicacao'
            ]
            
            for seletor in seletores_cnpq:
                try:
                    elementos = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                    for elemento in elementos:
                        texto = elemento.text.strip()
                        if texto and len(texto) > 20:
                            info_completa = self.extrair_chamada_completa(elemento, len(self.resultados['chamadas_cnpq']) + 1)
                            if info_completa and info_completa not in self.resultados['chamadas_cnpq']:
                                self.resultados['chamadas_cnpq'].append(info_completa)
                except:
                    continue
                    
        except Exception as e:
            print(f"      ❌ Erro no método 3: {e}")
    
    def eh_chamada_valida(self, texto):
        """Verifica se um texto parece ser uma chamada válida"""
        if not texto or len(texto) < 10:
            return False
        
        # Padrões que indicam que é uma chamada
        padroes_chamada = [
            r'CHAMADA\s+[A-Z]+\s+\d{4}',
            r'Chamada\s+[A-Z]+\s+\d{4}',
            r'CHAMADA\s+PÚBLICA',
            r'Chamada\s+Pública',
            r'CHAMADA\s+CNPq',
            r'Chamada\s+CNPq'
        ]
        
        for padrao in padroes_chamada:
            if re.search(padrao, texto, re.IGNORECASE):
                return True
        
        return False
    
    def extrair_chamada_completa(self, elemento, numero):
        """Extrai informações COMPLETAS de uma chamada baseada na estrutura HTML real"""
        try:
            # Pegar o bloco do conteúdo logo abaixo do título
            try:
                container = elemento.find_element(By.XPATH, "./following-sibling::*[1]")
                texto_completo = container.text.strip()
            except:
                texto_completo = elemento.text.strip()
            
            # Extrair título
            titulo = elemento.text.strip()
            
            # Extrair número da chamada
            numero_match = re.search(r'(\d{4})', titulo)
            numero_chamada = numero_match.group(1) if numero_match else ""
            
            # Extrair período de inscrições
            periodo_inscricao = ""
            try:
                validade_element = container.find_element(By.XPATH, ".//*[contains(text(),'Inscrições')]")
                periodo_inscricao = validade_element.text.strip()
            except:
                # Buscar por padrões de data no texto
                padrao_data = r'(\d{2}/\d{2}/\d{4})\s*a\s*(\d{2}/\d{2}/\d{4})'
                datas = re.findall(padrao_data, texto_completo)
                if datas:
                    periodo_inscricao = f"Inscrições: {datas[0][0]} a {datas[0][1]}"
            
            # Extrair descrição
            descricao = ""
            try:
                # Buscar por descrição próxima ao título
                descricao_element = container.find_element(By.XPATH, ".//p | .//div[contains(@class, 'descricao')]")
                descricao = descricao_element.text.strip()
            except:
                # Se não encontrar, usar parte do texto completo
                linhas = texto_completo.split('\n')
                for linha in linhas:
                    if linha.strip() and len(linha.strip()) > 20 and "Inscrições" not in linha:
                        descricao = linha.strip()
                        break
            
            if not descricao:
                descricao = titulo
            
            # 🔥 BUSCA MEGA-ULTRA-MELHORADA POR LINKS
            links_importantes = self.buscar_links_mega_ultra_melhorado(container, titulo)
            
            # Extrair ID da chamada se disponível
            id_chamada = ""
            try:
                # Buscar por ID em atributos ou links
                link_element = container.find_element(By.TAG_NAME, "a")
                href = link_element.get_attribute("href")
                if "idDivulgacao=" in href:
                    id_match = re.search(r'idDivulgacao=(\d+)', href)
                    if id_match:
                        id_chamada = id_match.group(1)
            except:
                pass
            
            resultado = {
                'id': id_chamada,
                'titulo': titulo,
                'numero': numero_chamada,
                'descricao': descricao,
                'periodo_inscricao': periodo_inscricao,
                'fonte': 'CNPq',
                'data_coleta': datetime.now().isoformat(),
                'links_importantes': links_importantes,
                'total_links': len(links_importantes),
                'texto_completo': texto_completo[:500] + "..." if len(texto_completo) > 500 else texto_completo
            }
            
            return resultado
            
        except Exception as e:
            print(f"         ❌ Erro ao extrair chamada completa: {e}")
            return None
    
    def extrair_chamada_por_texto(self, texto_padrao, elemento):
        """Extrai chamada baseado em texto encontrado"""
        try:
            # Criar uma chamada básica baseada no padrão encontrado
            resultado = {
                'id': "",
                'titulo': texto_padrao,
                'numero': re.search(r'(\d{4})', texto_padrao).group(1) if re.search(r'(\d{4})', texto_padrao) else "",
                'descricao': texto_padrao,
                'periodo_inscricao': "",
                'fonte': 'CNPq',
                'data_coleta': datetime.now().isoformat(),
                'links_importantes': [],
                'total_links': 0,
                'texto_completo': texto_padrao
            }
            
            # Tentar extrair mais informações do elemento
            if elemento:
                info_completa = self.extrair_chamada_completa(elemento, len(self.resultados['chamadas_cnpq']) + 1)
                if info_completa:
                    resultado.update(info_completa)
            
            return resultado
            
        except Exception as e:
            print(f"         ❌ Erro ao extrair chamada por texto: {e}")
            return None
    
    def buscar_elemento_por_texto(self, texto):
        """Busca um elemento que contenha o texto especificado"""
        try:
            # Buscar por XPath que contenha o texto
            xpath = f"//*[contains(text(), '{texto}')]"
            elementos = self.driver.find_elements(By.XPATH, xpath)
            
            if elementos:
                return elementos[0]  # Retorna o primeiro encontrado
            
            return None
            
        except Exception as e:
            return None
    
    def buscar_links_mega_ultra_melhorado(self, container, titulo_chamada):
        """Busca MEGA-ULTRA-MELHORADA por links importantes relacionados à chamada"""
        links = []
        
        try:
            print(f"         🔍 Buscando links MEGA-ULTRA-MELHORADO para: {titulo_chamada[:40]}...")
            
            # 1. Buscar por TODOS os links no container
            links_elementos = container.find_elements(By.TAG_NAME, "a")
            for link in links_elementos:
                href = link.get_attribute('href')
                texto = link.text.strip()
                
                if href and texto:
                    # Classificar o tipo de link baseado no texto
                    tipo_link = self.classificar_tipo_link(texto)
                    
                    links.append({
                        'texto': texto,
                        'url': href,
                        'tipo': tipo_link,
                        'metodo': 'Container Direto'
                    })
                    print(f"            🔗 Link encontrado: {texto} ({tipo_link})")
            
            # 2. Buscar por links específicos mencionados no texto
            if not links:
                print(f"            🔍 Buscando por menções a links...")
                links_texto = self.buscar_links_por_texto(titulo_chamada, container.text)
                links.extend(links_texto)
            
            # 3. Buscar por elementos próximos que possam conter links
            if not links:
                print(f"            🔍 Buscando elementos próximos...")
                links_proximos = self.buscar_links_elementos_proximos(container)
                links.extend(links_proximos)
            
            print(f"            ✅ Total de links encontrados: {len(links)}")
            
        except Exception as e:
            print(f"         ❌ Erro na busca MEGA-ULTRA-MELHORADA: {e}")
        
        return links
    
    def classificar_tipo_link(self, texto_link):
        """Classifica o tipo de link baseado no texto"""
        texto_lower = texto_link.lower()
        
        if 'chamada' in texto_lower:
            return 'Chamada Principal'
        elif 'anexo' in texto_lower:
            return 'Anexo'
        elif 'faq' in texto_lower:
            return 'FAQ'
        elif 'pdf' in texto_lower:
            return 'PDF'
        elif 'resultado' in texto_lower:
            return 'Resultado'
        elif 'edital' in texto_lower:
            return 'Edital'
        else:
            return 'Link Geral'
    
    def buscar_links_por_texto(self, titulo_chamada, texto_completo):
        """Busca links mencionados no texto da chamada"""
        links = []
        
        try:
            # Buscar por menções a links no texto
            if "DOWNLOAD" in texto_completo or "Arquivos" in texto_completo:
                # Tentar encontrar nomes de arquivos mencionados
                padrao_arquivo = r'([A-Z][^.]*\.pdf)'
                matches = re.findall(padrao_arquivo, texto_completo)
                
                for nome_arquivo in matches:
                    links.append({
                        'texto': nome_arquivo,
                        'url': f"http://memoria2.cnpq.br/web/guest/chamadas-publicas",
                        'tipo': 'PDF Mencionado',
                        'metodo': 'Texto da Chamada',
                        'instrucoes': 'Acesse a página para encontrar este arquivo'
                    })
                    print(f"               🔗 Link mencionado: {nome_arquivo}")
            
        except Exception as e:
            print(f"               ❌ Erro na busca por texto: {e}")
        
        return links
    
    def buscar_links_elementos_proximos(self, container):
        """Busca links em elementos próximos ao container"""
        links = []
        
        try:
            # Buscar por elementos irmãos
            try:
                elemento_pai = container.find_element(By.XPATH, "./..")
                elementos_irmaos = elemento_pai.find_elements(By.CSS_SELECTOR, '*')
                
                for elem in elementos_irmaos:
                    try:
                        links_elementos = elem.find_elements(By.TAG_NAME, "a")
                        for link in links_elementos:
                            href = link.get_attribute('href')
                            texto = link.text.strip()
                            
                            if href and texto and href not in [l['url'] for l in links]:
                                tipo_link = self.classificar_tipo_link(texto)
                                links.append({
                                    'texto': texto,
                                    'url': href,
                                    'tipo': tipo_link,
                                    'metodo': 'Elemento Próximo'
                                })
                                print(f"                  🔗 Link próximo: {texto}")
                    except:
                        continue
                        
            except:
                pass
            
        except Exception as e:
            print(f"                  ❌ Erro na busca por elementos próximos: {e}")
        
        return links
    
    def salvar_resultados(self):
        """Salva os resultados da SOLUÇÃO DEFINITIVA do CNPq"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"cnpq_solucao_definitiva_{timestamp}.json"
            
            # Calcular totais
            total_links = sum(len(item.get('links_importantes', [])) for item in self.resultados['chamadas_cnpq'])
            self.resultados['total_chamadas'] = len(self.resultados['chamadas_cnpq'])
            self.resultados['total_links'] = total_links
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Resultados da SOLUÇÃO DEFINITIVA do CNPq salvos em: {nome_arquivo}")
            return nome_arquivo
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return None
    
    def executar_solucao_definitiva(self):
        """Executa a SOLUÇÃO DEFINITIVA do CNPq"""
        print("🚀 INICIANDO SOLUÇÃO DEFINITIVA DO CNPq")
        print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
        
        if not self.configurar_navegador():
            return False
        
        try:
            # Extrair CNPq com SOLUÇÃO DEFINITIVA
            self.extrair_cnpq_solucao_definitiva()
            
            # Salvar resultados
            arquivo = self.salvar_resultados()
            
            # Fechar navegador
            if self.driver:
                self.driver.quit()
            
            print(f"🎉 SOLUÇÃO DEFINITIVA DO CNPq CONCLUÍDA!")
            print(f"📊 Total de chamadas: {len(self.resultados['chamadas_cnpq'])}")
            print(f"🔗 Total de links: {self.resultados['total_links']}")
            print(f"💾 Arquivo salvo: {arquivo}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na execução: {e}")
            if self.driver:
                self.driver.quit()
            return False

if __name__ == "__main__":
    scraper = ScraperCNPqSolucaoDefinitiva()
    scraper.executar_solucao_definitiva()
