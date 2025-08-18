import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

class ScraperFAPEMIGSimples:
    def __init__(self):
        """Scraper FAPEMIG simples usando requests + BeautifulSoup"""
        self.url = "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/"
        self.resultados = []
        
    def fazer_requisicao(self):
        """Faz a requisição HTTP para a página"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            print(f"🌐 Fazendo requisição para: {self.url}")
            response = requests.get(self.url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                print("✅ Página carregada com sucesso!")
                return response.text
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
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
        pdfs = []
        
        # Busca por links
        links = elemento.find_all('a', href=True)
        
        for link in links:
            href = link.get('href')
            texto = link.get_text(strip=True)
            
            if href:
                # Converte URLs relativas em absolutas
                if href.startswith('/'):
                    href = f"http://www.fapemig.br{href}"
                elif not href.startswith('http'):
                    href = f"http://www.fapemig.br/{href}"
                
                if href.endswith('.pdf') or 'pdf' in href.lower():
                    pdfs.append({
                        'url': href,
                        'texto': texto or 'PDF'
                    })
                elif 'download' in href.lower() or 'arquivo' in href.lower():
                    pdfs.append({
                        'url': href,
                        'texto': texto or 'Download'
                    })
        
        return pdfs
    
    def processar_elemento(self, elemento):
        """Processa um elemento HTML para extrair informações da chamada"""
        try:
            # Extrai texto completo
            texto_completo = elemento.get_text(strip=True)
            
            if not texto_completo or len(texto_completo) < 20:
                return None
            
            # Verifica se é uma chamada/edital
            texto_lower = texto_completo.lower()
            if not any(palavra in texto_lower for palavra in ['chamada', 'edital', 'fapemig', 'portaria']):
                return None
            
            chamada = {
                'titulo': texto_completo[:200] + '...' if len(texto_completo) > 200 else texto_completo,
                'data_inclusao': '',
                'prazo_final': '',
                'numero_chamada': '',
                'pdfs': [],
                'texto_completo': texto_completo,
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat()
            }
            
            # Extrai número da chamada
            numero_match = re.search(r'(\d+/\d+)', texto_completo)
            if numero_match:
                chamada['numero_chamada'] = numero_match.group(1)
            
            # Extrai datas
            datas_encontradas = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}', texto_completo)
            if datas_encontradas:
                if len(datas_encontradas) >= 2:
                    chamada['prazo_final'] = f"{datas_encontradas[0]} a {datas_encontradas[1]}"
                else:
                    chamada['prazo_final'] = datas_encontradas[0]
            
            # Extrai links PDF
            chamada['pdfs'] = self.extrair_links_pdf(elemento)
            
            return chamada
            
        except Exception as e:
            print(f"⚠️ Erro ao processar elemento: {e}")
            return None
    
    def extrair_chamadas(self, html):
        """Extrai chamadas do HTML"""
        try:
            print("🔍 Analisando HTML...")
            soup = BeautifulSoup(html, 'html.parser')
            
            # Estratégias de busca
            estrategias = [
                # Estratégia 1: Busca por títulos
                soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']),
                
                # Estratégia 2: Busca por divs com classes específicas
                soup.find_all('div', class_=re.compile(r'chamada|edital|title|header', re.I)),
                
                # Estratégia 3: Busca por elementos com texto específico
                soup.find_all(text=re.compile(r'CHAMADA|Edital|FAPEMIG', re.I)),
                
                # Estratégia 4: Busca por parágrafos longos
                soup.find_all('p', text=re.compile(r'.{50,}')),
            ]
            
            elementos_processados = set()
            chamadas_encontradas = []
            
            for estrategia in estrategias:
                if not estrategia:
                    continue
                
                print(f"🔍 Estratégia: {len(estrategia)} elementos encontrados")
                
                for elemento in estrategia:
                    # Pega o elemento pai se for texto
                    if hasattr(elemento, 'parent'):
                        elemento_para_processar = elemento.parent
                    else:
                        elemento_para_processar = elemento
                    
                    # Evita processar o mesmo elemento
                    if id(elemento_para_processar) in elementos_processados:
                        continue
                    
                    elementos_processados.add(id(elemento_para_processar))
                    
                    chamada = self.processar_elemento(elemento_para_processar)
                    if chamada:
                        chamadas_encontradas.append(chamada)
                        print(f"   ✅ {chamada['titulo'][:50]}...")
                
                if chamadas_encontradas:
                    break
            
            # Remove duplicatas baseado no título
            chamadas_unicas = []
            titulos_vistos = set()
            
            for chamada in chamadas_encontradas:
                titulo_limpo = re.sub(r'\s+', ' ', chamada['titulo'].strip())
                if titulo_limpo not in titulos_vistos:
                    titulos_vistos.add(titulo_limpo)
                    chamadas_unicas.append(chamada)
            
            self.resultados = chamadas_unicas
            print(f"\n🎯 Total de chamadas únicas encontradas: {len(self.resultados)}")
            
        except Exception as e:
            print(f"❌ Erro ao extrair chamadas: {e}")
    
    def salvar_resultados(self, nome_arquivo=None):
        """Salva os resultados em arquivo JSON"""
        if not nome_arquivo:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_arquivo = f"fapemig_simples_{timestamp}.json"
        
        resultado_final = {
            'fapemig': self.resultados,
            'total_chamadas': len(self.resultados),
            'timestamp': datetime.now().isoformat(),
            'url_fonte': self.url,
            'metodo': 'Requests + BeautifulSoup'
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
        print("🚀 Iniciando Scraper FAPEMIG Simples")
        print("=" * 50)
        
        # Faz a requisição
        html = self.fazer_requisicao()
        if not html:
            return False
        
        # Extrai as chamadas
        self.extrair_chamadas(html)
        
        if self.resultados:
            arquivo_salvo = self.salvar_resultados()
            if arquivo_salvo:
                print(f"\n🎉 Scraping concluído! {len(self.resultados)} chamadas extraídas")
                return True
        else:
            print("❌ Nenhuma chamada foi extraída")
            return False
    
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
    print("🔍 Scraper FAPEMIG Simples")
    print("=" * 50)
    
    # Cria e executa o scraper
    scraper = ScraperFAPEMIGSimples()
    
    if scraper.executar():
        scraper.mostrar_resultados()
    else:
        print("❌ Falha na execução do scraper")

if __name__ == "__main__":
    main()
