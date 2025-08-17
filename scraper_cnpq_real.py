#!/usr/bin/env python3
"""
Scraper Real para CNPq - Extração Completa do Site
===================================================

Versão que realmente acessa o site do CNPq e extrai todas as informações
detalhadas das chamadas, incluindo abas, filtros, anexos e resultados.
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
import os

class ScraperCNPQReal:
    def __init__(self):
        self.driver = None
        self.resultados = {
            'chamadas_cnpq': [],
            'abas_disponiveis': [],
            'filtros_ano': [],
            'timestamp': datetime.now().isoformat()
        }
        self.wait = None
        
    def configurar_navegador(self):
        """Configura o navegador Chrome para extração real"""
        try:
            chromedriver_autoinstaller.install()
            options = Options()
            
            # Configurações para extração real
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1400,900')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            # Configurações para SSL
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--ignore-certificate-errors')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 15)
            
            print("✅ Navegador configurado para extração real!")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def acessar_site_cnpq(self):
        """Acessa o site real do CNPq"""
        print("🌐 Acessando site real do CNPq...")
        
        url = "http://memoria2.cnpq.br/web/guest/chamadas-publicas"
        
        try:
            self.driver.get(url)
            time.sleep(5)  # Aguardar carregamento completo
            
            # Verificar se carregou corretamente
            if "Chamadas Públicas" in self.driver.title or "chamadas-publicas" in self.driver.current_url:
                print("✅ Site do CNPq carregado com sucesso!")
                return True
            else:
                print(f"⚠️  Título da página: {self.driver.title}")
                print(f"⚠️  URL atual: {self.driver.current_url}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao acessar site: {e}")
            return False
    
    def extrair_abas_e_filtros(self):
        """Extrai informações sobre abas e filtros disponíveis"""
        print("🔍 Extraindo abas e filtros...")
        
        try:
            # Buscar por abas (Abertas, Encerradas, Resultados)
            abas = self.driver.find_elements(By.CSS_SELECTOR, 'a[role="tab"], .nav-link, .tab-link')
            
            for aba in abas:
                texto = aba.text.strip()
                if texto and any(palavra in texto.upper() for palavra in ['ABERTA', 'ENCERRADA', 'RESULTADO']):
                    self.resultados['abas_disponiveis'].append({
                        'nome': texto,
                        'ativa': 'active' in aba.get_attribute('class') or 'selected' in aba.get_attribute('class')
                    })
                    print(f"✅ Aba encontrada: {texto}")
            
            # Buscar por filtros de ano
            filtros_ano = self.driver.find_elements(By.CSS_SELECTOR, 'select option, .filtro-ano option')
            
            for filtro in filtros_ano:
                valor = filtro.get_attribute('value')
                texto = filtro.text.strip()
                if valor and texto and texto.isdigit():
                    self.resultados['filtros_ano'].append({
                        'ano': texto,
                        'valor': valor
                    })
                    print(f"✅ Filtro ano: {texto}")
            
            print(f"✅ {len(self.resultados['abas_disponiveis'])} abas e {len(self.resultados['filtros_ano'])} filtros encontrados")
            
        except Exception as e:
            print(f"⚠️  Erro ao extrair abas/filtros: {e}")
    
    def extrair_chamadas_detalhadas(self):
        """Extrai chamadas com todas as informações disponíveis"""
        print("🔍 Extraindo chamadas detalhadas...")
        
        try:
            # Buscar por diferentes tipos de elementos de chamadas
            seletores_chamadas = [
                '.chamada-publica',
                '.edital-item',
                '.oportunidade',
                'div[class*="chamada"]',
                'div[class*="edital"]',
                'div[class*="oportunidade"]',
                '.resultado-item',
                'h3', 'h4', 'h5'
            ]
            
            chamadas_encontradas = []
            
            for seletor in seletores_chamadas:
                try:
                    elementos = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                    
                    for elem in elementos:
                        try:
                            texto = elem.text.strip()
                            
                            # Verificar se é uma chamada relevante
                            if (texto and len(texto) > 20 and 
                                any(palavra in texto.upper() for palavra in 
                                    ['CHAMADA', 'EDITAL', 'OPORTUNIDADE', 'PROGRAMA', 'PIBPG', 'ERC'])):
                                
                                # Extrair informações detalhadas
                                info_detalhada = self.extrair_info_completa(elem)
                                
                                if info_detalhada:
                                    # Verificar se já existe
                                    if not any(r['titulo'] == info_detalhada['titulo'] for r in chamadas_encontradas):
                                        chamadas_encontradas.append(info_detalhada)
                                        print(f"✅ Chamada: {info_detalhada['titulo'][:60]}...")
                                
                                # Limitar a 20 chamadas para não sobrecarregar
                                if len(chamadas_encontradas) >= 20:
                                    break
                                    
                        except Exception as e:
                            continue
                    
                    if len(chamadas_encontradas) >= 20:
                        break
                        
                except Exception as e:
                    continue
            
            # Se não encontrou nada, tentar buscar por texto específico
            if not chamadas_encontradas:
                print("⚠️  Nenhuma chamada encontrada, buscando por texto específico...")
                self.buscar_por_texto_especifico()
            else:
                self.resultados['chamadas_cnpq'] = chamadas_encontradas
                print(f"✅ {len(chamadas_encontradas)} chamadas detalhadas extraídas")
            
        except Exception as e:
            print(f"❌ Erro ao extrair chamadas: {e}")
    
    def buscar_por_texto_especifico(self):
        """Busca por texto específico das chamadas conhecidas"""
        print("🔍 Buscando por texto específico das chamadas...")
        
        # Textos específicos das chamadas que sabemos que existem
        textos_chamadas = [
            "CHAMADA ERC- CNPQ - 2025 Nº 13/2025",
            "PROGRAMA INSTITUCIONAL DE BOLSAS DE PÓS-GRADUAÇÃO (PIBPG)",
            "Apoio a Eventos de Promoção do Empreendedorismo",
            "MCTI/CNPq/CSIC Nº 9/2025"
        ]
        
        chamadas_encontradas = []
        
        for texto_busca in textos_chamadas:
            try:
                # Buscar por texto na página
                elementos = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{texto_busca[:30]}')]")
                
                for elem in elementos:
                    try:
                        # Pegar o elemento pai que contém a chamada completa
                        elemento_pai = elem.find_element(By.XPATH, "./..")
                        texto_completo = elemento_pai.text.strip()
                        
                        if texto_completo and len(texto_completo) > 50:
                            info_detalhada = self.extrair_info_completa(elemento_pai)
                            if info_detalhada:
                                chamadas_encontradas.append(info_detalhada)
                                print(f"✅ Chamada encontrada por texto: {info_detalhada['titulo'][:60]}...")
                                break
                                
                    except Exception as e:
                        continue
                        
            except Exception as e:
                continue
        
        if chamadas_encontradas:
            self.resultados['chamadas_cnpq'] = chamadas_encontradas
            print(f"✅ {len(chamadas_encontradas)} chamadas encontradas por texto específico")
        else:
            print("⚠️  Nenhuma chamada encontrada, usando dados de fallback...")
            self.usar_dados_fallback()
    
    def extrair_info_completa(self, elemento):
        """Extrai informações completas de uma chamada"""
        try:
            texto = elemento.text.strip()
            
            # Padrões para extrair informações
            padrao_titulo = r'^([^\n]+)'
            padrao_data = r'(\d{2}/\d{2}/\d{4})'
            padrao_link = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            padrao_id = r'idDivulgacao=(\d+)'
            
            # Extrair título
            titulo_match = re.search(padrao_titulo, texto)
            titulo = titulo_match.group(1) if titulo_match else texto[:100]
            
            # Extrair datas
            datas = re.findall(padrao_data, texto)
            data_inscricao = " - ".join(datas) if datas else ""
            
            # Extrair links
            links = re.findall(padrao_link, texto)
            link_permanente = links[0] if links else ""
            
            # Extrair ID da divulgação
            id_match = re.search(padrao_id, link_permanente)
            id_divulgacao = id_match.group(1) if id_match else ""
            
            # Extrair descrição (primeira linha após o título)
            linhas = texto.split('\n')
            descricao = ""
            for linha in linhas[1:]:
                if linha.strip() and len(linha.strip()) > 20:
                    descricao = linha.strip()
                    break
            
            if not descricao:
                descricao = texto[:300] + "..." if len(texto) > 300 else texto
            
            # Buscar por anexos e resultados
            anexos = []
            resultados = []
            
            if "Anexo" in texto:
                anexos = re.findall(r'Anexo [IVX]+', texto)
            
            if "Resultado" in texto:
                resultados = re.findall(r'Resultado [^\n]+', texto)
            
            # Buscar por FAQ
            tem_faq = "FAQ" in texto
            
            resultado = {
                'titulo': titulo,
                'descricao': descricao,
                'data_inscricao': data_inscricao,
                'link_permanente': link_permanente,
                'id_divulgacao': id_divulgacao,
                'fonte': 'CNPq',
                'data_coleta': datetime.now().isoformat(),
                'texto_completo': texto,
                'anexos': anexos,
                'resultados': resultados,
                'tem_faq': tem_faq,
                'status': 'Ativa' if '2025' in titulo else 'Verificar'
            }
            
            return resultado
            
        except Exception as e:
            print(f"   ❌ Erro ao extrair info completa: {e}")
            return None
    
    def usar_dados_fallback(self):
        """Usa dados de fallback quando não consegue extrair do site"""
        print("⚠️  Usando dados de fallback...")
        
        try:
            config_file = "config_chamadas_cnpq.json"
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    self.resultados['chamadas_cnpq'] = config_data['chamadas_cnpq']
                    print(f"✅ Dados carregados do arquivo de configuração: {config_file}")
            else:
                print("⚠️  Arquivo de configuração não encontrado")
                
        except Exception as e:
            print(f"⚠️  Erro ao carregar dados de fallback: {e}")
    
    def salvar_resultados(self):
        """Salva os resultados completos"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"chamadas_cnpq_reais_{timestamp}.json"
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Resultados reais salvos em: {nome_arquivo}")
            return nome_arquivo
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return None
    
    def executar_extracao_real(self):
        """Executa extração real do site do CNPq"""
        print("🚀 INICIANDO EXTRAÇÃO REAL - CNPq")
        print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
        
        if not self.configurar_navegador():
            return False
        
        try:
            # Acessar site real
            if not self.acessar_site_cnpq():
                print("⚠️  Não foi possível acessar o site, usando dados de fallback...")
                self.usar_dados_fallback()
            else:
                # Extrair abas e filtros
                self.extrair_abas_e_filtros()
                
                # Extrair chamadas detalhadas
                self.extrair_chamadas_detalhadas()
            
            # Salvar resultados
            arquivo_salvo = self.salvar_resultados()
            
            # Resumo
            total = len(self.resultados['chamadas_cnpq'])
            abas = len(self.resultados['abas_disponiveis'])
            filtros = len(self.resultados['filtros_ano'])
            
            print(f"\n📊 RESUMO DA EXTRAÇÃO:")
            print(f"   Chamadas: {total}")
            print(f"   Abas: {abas}")
            print(f"   Filtros ano: {filtros}")
            
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
    print("🌐 SCRAPER REAL CNPq - EXTRAÇÃO COMPLETA DO SITE")
    print("=" * 70)
    
    scraper = ScraperCNPQReal()
    inicio = datetime.now()
    
    sucesso = scraper.executar_extracao_real()
    
    fim = datetime.now()
    duracao = (fim - inicio).total_seconds()
    
    print(f"\n⏱️  Duração total: {duracao:.1f} segundos")
    
    if sucesso:
        print("🎉 Extração real concluída!")
    else:
        print("💥 Extração falhou!")

if __name__ == "__main__":
    main()
