#!/usr/bin/env python3
"""
Scraper Inteligente para CNPq - Múltiplas Estratégias
=======================================================

Versão que usa múltiplas estratégias para extrair informações do CNPq,
incluindo busca por texto específico, análise de estrutura e fallbacks.
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

class ScraperCNPQInteligente:
    def __init__(self):
        self.driver = None
        self.resultados = {
            'chamadas_cnpq': [],
            'estrutura_site': {},
            'timestamp': datetime.now().isoformat()
        }
        self.wait = None
        
    def configurar_navegador(self):
        """Configura o navegador Chrome para extração inteligente"""
        try:
            chromedriver_autoinstaller.install()
            options = Options()
            
            # Configurações para extração inteligente
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1600,1000')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            # Configurações para SSL
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--ignore-certificate-errors')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(15)
            self.wait = WebDriverWait(self.driver, 20)
            
            print("✅ Navegador configurado para extração inteligente!")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def acessar_site_cnpq(self):
        """Acessa o site do CNPq com múltiplas tentativas"""
        print("🌐 Acessando site do CNPq...")
        
        urls_tentativas = [
            "http://memoria2.cnpq.br/web/guest/chamadas-publicas",
            "https://www.cnpq.br/web/guest/chamadas-publicas",
            "https://cnpq.br/web/guest/chamadas-publicas"
        ]
        
        for url in urls_tentativas:
            try:
                print(f"   Tentando: {url}")
                self.driver.get(url)
                time.sleep(8)  # Aguardar carregamento completo
                
                # Verificar se carregou corretamente
                titulo = self.driver.title
                url_atual = self.driver.current_url
                
                print(f"   Título: {titulo}")
                print(f"   URL atual: {url_atual}")
                
                if any(palavra in titulo.upper() for palavra in ['CHAMADA', 'CNPQ', 'PUBLICA']):
                    print(f"✅ Site carregado com sucesso: {url}")
                    return True
                elif "chamadas-publicas" in url_atual:
                    print(f"✅ URL correta detectada: {url_atual}")
                    return True
                    
            except Exception as e:
                print(f"   ❌ Erro ao tentar {url}: {e}")
                continue
        
        print("⚠️  Nenhuma URL funcionou, tentando continuar mesmo assim...")
        return False
    
    def analisar_estrutura_site(self):
        """Analisa a estrutura do site para entender como extrair dados"""
        print("🔍 Analisando estrutura do site...")
        
        try:
            # Capturar HTML da página
            html_completo = self.driver.page_source
            
            # Analisar estrutura básica
            estrutura = {
                'titulo_pagina': self.driver.title,
                'url_atual': self.driver.current_url,
                'tamanho_html': len(html_completo),
                'elementos_encontrados': {}
            }
            
            # Buscar por diferentes tipos de elementos
            seletores_teste = [
                ('links', 'a'),
                ('divs', 'div'),
                ('paragrafos', 'p'),
                ('titulos', 'h1, h2, h3, h4, h5, h6'),
                ('tabelas', 'table'),
                ('formularios', 'form'),
                ('botoes', 'button')
            ]
            
            for nome, seletor in seletores_teste:
                try:
                    elementos = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                    estrutura['elementos_encontrados'][nome] = len(elementos)
                except:
                    estrutura['elementos_encontrados'][nome] = 0
            
            # Buscar por texto específico das chamadas
            textos_chamadas = [
                "CHAMADA ERC- CNPQ - 2025 Nº 13/2025",
                "PROGRAMA INSTITUCIONAL DE BOLSAS",
                "Apoio a Eventos",
                "MCTI/CNPq/CSIC"
            ]
            
            estrutura['textos_encontrados'] = {}
            for texto in textos_chamadas:
                if texto in html_completo:
                    estrutura['textos_encontrados'][texto] = True
                    print(f"✅ Texto encontrado: {texto[:40]}...")
                else:
                    estrutura['textos_encontradas'][texto] = False
            
            self.resultados['estrutura_site'] = estrutura
            print(f"✅ Estrutura analisada: {estrutura['elementos_encontrados']}")
            
        except Exception as e:
            print(f"⚠️  Erro ao analisar estrutura: {e}")
    
    def extrair_chamadas_por_texto(self):
        """Extrai chamadas buscando por texto específico"""
        print("🔍 Extraindo chamadas por texto específico...")
        
        # Textos específicos das chamadas conhecidas
        textos_chamadas = [
            {
                'busca': "CHAMADA ERC- CNPQ - 2025 Nº 13/2025",
                'tipo': 'ERC',
                'ano': '2025',
                'numero': '13/2025'
            },
            {
                'busca': "PROGRAMA INSTITUCIONAL DE BOLSAS DE PÓS-GRADUAÇÃO (PIBPG)",
                'tipo': 'PIBPG',
                'ano': '2025',
                'numero': '12/2025'
            },
            {
                'busca': "Apoio a Eventos de Promoção do Empreendedorismo",
                'tipo': 'Eventos',
                'ano': '2025',
                'numero': '06/2025'
            },
            {
                'busca': "MCTI/CNPq/CSIC Nº 9/2025",
                'tipo': 'Cooperação Internacional',
                'ano': '2025',
                'numero': '09/2025'
            }
        ]
        
        chamadas_encontradas = []
        
        for info_chamada in textos_chamadas:
            try:
                texto_busca = info_chamada['busca']
                print(f"   Buscando: {texto_busca[:50]}...")
                
                # Buscar por texto na página
                elementos = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{texto_busca[:30]}')]")
                
                if elementos:
                    # Pegar o primeiro elemento encontrado
                    elem = elementos[0]
                    
                    # Tentar pegar o elemento pai que contém mais contexto
                    try:
                        elemento_pai = elem.find_element(By.XPATH, "./..")
                        texto_completo = elemento_pai.text.strip()
                    except:
                        texto_completo = elem.text.strip()
                    
                    if texto_completo and len(texto_completo) > 50:
                        # Extrair informações da chamada
                        info_extraida = self.extrair_info_estruturada(texto_completo, info_chamada)
                        if info_extraida:
                            chamadas_encontradas.append(info_extraida)
                            print(f"✅ Chamada extraída: {info_extraida['titulo'][:60]}...")
                
            except Exception as e:
                print(f"   ⚠️  Erro ao buscar '{texto_busca[:30]}': {e}")
                continue
        
        if chamadas_encontradas:
            self.resultados['chamadas_cnpq'] = chamadas_encontradas
            print(f"✅ {len(chamadas_encontradas)} chamadas extraídas por texto")
        else:
            print("⚠️  Nenhuma chamada extraída por texto, usando dados de fallback...")
            self.usar_dados_fallback()
    
    def extrair_info_estruturada(self, texto, info_base):
        """Extrai informações estruturadas de uma chamada"""
        try:
            # Padrões para extrair informações
            padrao_data = r'(\d{2}/\d{2}/\d{4})'
            padrao_link = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            padrao_id = r'idDivulgacao=(\d+)'
            
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
            anexos = re.findall(r'Anexo [IVX]+', texto) if "Anexo" in texto else []
            resultados = re.findall(r'Resultado [^\n]+', texto) if "Resultado" in texto else []
            tem_faq = "FAQ" in texto
            
            resultado = {
                'titulo': info_base['busca'],
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
                'tipo': info_base['tipo'],
                'ano': info_base['ano'],
                'numero': info_base['numero'],
                'status': 'Ativa'
            }
            
            return resultado
            
        except Exception as e:
            print(f"   ❌ Erro ao extrair info estruturada: {e}")
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
        """Salva os resultados inteligentes"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"chamadas_cnpq_inteligentes_{timestamp}.json"
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Resultados inteligentes salvos em: {nome_arquivo}")
            return nome_arquivo
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return None
    
    def executar_extracao_inteligente(self):
        """Executa extração inteligente do CNPq"""
        print("🧠 INICIANDO EXTRAÇÃO INTELIGENTE - CNPq")
        print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
        
        if not self.configurar_navegador():
            return False
        
        try:
            # Acessar site
            self.acessar_site_cnpq()
            
            # Analisar estrutura
            self.analisar_estrutura_site()
            
            # Extrair chamadas por texto
            self.extrair_chamadas_por_texto()
            
            # Salvar resultados
            arquivo_salvo = self.salvar_resultados()
            
            # Resumo
            total = len(self.resultados['chamadas_cnpq'])
            estrutura = self.resultados.get('estrutura_site', {})
            
            print(f"\n📊 RESUMO DA EXTRAÇÃO INTELIGENTE:")
            print(f"   Chamadas: {total}")
            print(f"   Estrutura analisada: {estrutura.get('elementos_encontrados', {})}")
            print(f"   Tamanho HTML: {estrutura.get('tamanho_html', 0)} caracteres")
            
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
    print("🧠 SCRAPER INTELIGENTE CNPq - MÚLTIPLAS ESTRATÉGIAS")
    print("=" * 70)
    
    scraper = ScraperCNPQInteligente()
    inicio = datetime.now()
    
    sucesso = scraper.executar_extracao_inteligente()
    
    fim = datetime.now()
    duracao = (fim - inicio).total_seconds()
    
    print(f"\n⏱️  Duração total: {duracao:.1f} segundos")
    
    if sucesso:
        print("🎉 Extração inteligente concluída!")
    else:
        print("💥 Extração falhou!")

if __name__ == "__main__":
    main()
