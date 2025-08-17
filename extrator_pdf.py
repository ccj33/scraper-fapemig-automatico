#!/usr/bin/env python3
"""
Extrator de Dados de PDFs
==========================

Extrai e analisa dados de PDFs de editais e chamadas
"""

import requests
import PyPDF2
import io
import re
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import os
from datetime import datetime
import fitz  # PyMuPDF - mais robusto para PDFs complexos

# Configuração de logging
logger = logging.getLogger(__name__)

class ExtratorPDF:
    """Classe para extrair dados de PDFs"""
    
    def __init__(self, diretorio_downloads: str = "downloads_pdf"):
        self.diretorio_downloads = diretorio_downloads
        self._criar_diretorio()
        
    def _criar_diretorio(self):
        """Cria diretório para downloads se não existir"""
        if not os.path.exists(self.diretorio_downloads):
            os.makedirs(self.diretorio_downloads)
            logger.info(f"📁 Diretório criado: {self.diretorio_downloads}")
    
    def extrair_de_url(self, url: str, nome_arquivo: str = None) -> Dict:
        """
        Extrai dados de um PDF a partir de uma URL
        
        Args:
            url: URL do PDF
            nome_arquivo: Nome opcional para salvar o arquivo
            
        Returns:
            Dicionário com dados extraídos
        """
        try:
            logger.info(f"🔍 Iniciando extração de PDF: {url}")
            
            # Verificar se é um PDF
            if not self._eh_pdf(url):
                logger.warning(f"⚠️ URL não parece ser um PDF: {url}")
                return {"erro": "URL não é um PDF válido"}
            
            # Baixar PDF
            pdf_bytes = self._baixar_pdf(url)
            if not pdf_bytes:
                return {"erro": "Falha ao baixar PDF"}
            
            # Salvar arquivo localmente
            nome_arquivo = nome_arquivo or self._gerar_nome_arquivo(url)
            caminho_arquivo = os.path.join(self.diretorio_downloads, nome_arquivo)
            
            with open(caminho_arquivo, 'wb') as f:
                f.write(pdf_bytes)
            
            logger.info(f"💾 PDF salvo: {caminho_arquivo}")
            
            # Extrair dados
            dados_extraidos = self._extrair_dados_pdf(pdf_bytes)
            dados_extraidos.update({
                'url_origem': url,
                'arquivo_local': caminho_arquivo,
                'tamanho_bytes': len(pdf_bytes),
                'data_extracao': datetime.now().isoformat()
            })
            
            logger.info(f"✅ Extração concluída: {len(dados_extraidos)} campos extraídos")
            return dados_extraidos
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair PDF: {e}")
            return {"erro": str(e)}
    
    def _eh_pdf(self, url: str) -> bool:
        """Verifica se a URL aponta para um PDF"""
        try:
            # Verificar extensão
            parsed = urlparse(url)
            path = parsed.path.lower()
            
            if path.endswith('.pdf'):
                return True
            
            # Verificar se contém 'pdf' na URL
            if 'pdf' in url.lower():
                return True
                
            # Verificar headers HTTP
            try:
                response = requests.head(url, timeout=10)
                content_type = response.headers.get('content-type', '').lower()
                return 'pdf' in content_type or 'application/pdf' in content_type
            except:
                pass
                
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao verificar se é PDF: {e}")
            return False
    
    def _baixar_pdf(self, url: str) -> Optional[bytes]:
        """Baixa PDF da URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            if response.content:
                logger.info(f"📥 PDF baixado: {len(response.content)} bytes")
                return response.content
            else:
                logger.error("❌ PDF vazio recebido")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro ao baixar PDF: {e}")
            return None
    
    def _gerar_nome_arquivo(self, url: str) -> str:
        """Gera nome de arquivo baseado na URL"""
        try:
            parsed = urlparse(url)
            nome = os.path.basename(parsed.path)
            
            if not nome or not nome.endswith('.pdf'):
                nome = f"edital_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            # Limpar nome do arquivo
            nome = re.sub(r'[<>:"/\\|?*]', '_', nome)
            return nome
            
        except:
            return f"edital_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    def _extrair_dados_pdf(self, pdf_bytes: bytes) -> Dict:
        """Extrai dados do conteúdo do PDF"""
        dados = {}
        
        try:
            # Tentar com PyMuPDF primeiro (mais robusto)
            try:
                dados = self._extrair_com_pymupdf(pdf_bytes)
            except:
                # Fallback para PyPDF2
                dados = self._extrair_com_pypdf2(pdf_bytes)
            
            # Análise adicional do conteúdo
            if dados.get('texto_completo'):
                dados.update(self._analisar_conteudo(dados['texto_completo']))
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair dados do PDF: {e}")
            dados = {"erro_extracao": str(e)}
        
        return dados
    
    def _extrair_com_pymupdf(self, pdf_bytes: bytes) -> Dict:
        """Extrai dados usando PyMuPDF (mais robusto)"""
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            dados = {
                'num_paginas': len(doc),
                'texto_completo': '',
                'metadados': doc.metadata
            }
            
            # Extrair texto de todas as páginas
            texto_completo = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                texto_pagina = page.get_text()
                texto_completo.append(texto_pagina)
            
            dados['texto_completo'] = '\n'.join(texto_completo)
            doc.close()
            
            return dados
            
        except Exception as e:
            logger.warning(f"⚠️ PyMuPDF falhou, tentando PyPDF2: {e}")
            raise e
    
    def _extrair_com_pypdf2(self, pdf_bytes: bytes) -> Dict:
        """Extrai dados usando PyPDF2 (fallback)"""
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PyPDF2.PdfReader(pdf_file)
            
            dados = {
                'num_paginas': len(reader.pages),
                'texto_completo': '',
                'metadados': reader.metadata
            }
            
            # Extrair texto de todas as páginas
            texto_completo = []
            for page in reader.pages:
                texto_pagina = page.extract_text()
                if texto_pagina:
                    texto_completo.append(texto_pagina)
            
            dados['texto_completo'] = '\n'.join(texto_completo)
            
            return dados
            
        except Exception as e:
            logger.error(f"❌ PyPDF2 também falhou: {e}")
            raise e
    
    def _analisar_conteudo(self, texto: str) -> Dict:
        """Analisa o conteúdo extraído para encontrar informações importantes"""
        analise = {}
        
        try:
            # Padrões para encontrar informações importantes
            padroes = {
                'valor': [
                    r'R\$\s*[\d.,]+',
                    r'valor[:\s]*R\$\s*[\d.,]+',
                    r'até\s*R\$\s*[\d.,]+',
                    r'máximo\s*R\$\s*[\d.,]+'
                ],
                'prazo': [
                    r'\d{1,2}/\d{1,2}/\d{4}',
                    r'\d{1,2}-\d{1,2}-\d{4}',
                    r'prazo[:\s]*\d{1,2}/\d{1,2}/\d{4}',
                    r'até\s*\d{1,2}/\d{1,2}/\d{4}'
                ],
                'objetivo': [
                    r'objetivo[:\s]*(.*?)(?=\n|\.)',
                    r'finalidade[:\s]*(.*?)(?=\n|\.)',
                    r'propósito[:\s]*(.*?)(?=\n|\.)'
                ],
                'area_tematica': [
                    r'área[:\s]*(.*?)(?=\n|\.)',
                    r'temática[:\s]*(.*?)(?=\n|\.)',
                    r'linha[:\s]*(.*?)(?=\n|\.)'
                ]
            }
            
            for campo, lista_padroes in padroes.items():
                for padrao in lista_padroes:
                    matches = re.findall(padrao, texto, re.IGNORECASE)
                    if matches:
                        analise[campo] = matches[0] if isinstance(matches[0], str) else matches[0].group()
                        break
            
            # Contar palavras e caracteres
            analise['estatisticas'] = {
                'total_caracteres': len(texto),
                'total_palavras': len(texto.split()),
                'total_linhas': len(texto.split('\n'))
            }
            
            # Detectar idioma (português vs inglês)
            palavras_pt = len(re.findall(r'\b(de|para|com|por|em|não|são|está|ser|ter)\b', texto, re.IGNORECASE))
            palavras_en = len(re.findall(r'\b(the|and|for|with|in|is|are|was|were|have|has)\b', texto, re.IGNORECASE))
            
            if palavras_pt > palavras_en:
                analise['idioma_detectado'] = 'português'
            else:
                analise['idioma_detectado'] = 'inglês'
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na análise de conteúdo: {e}")
        
        return analise
    
    def extrair_multiplos_pdfs(self, urls: List[str]) -> List[Dict]:
        """Extrai dados de múltiplos PDFs"""
        resultados = []
        
        for i, url in enumerate(urls, 1):
            logger.info(f"📄 Processando PDF {i}/{len(urls)}: {url}")
            
            resultado = self.extrair_de_url(url)
            resultados.append(resultado)
            
            # Delay para não sobrecarregar servidores
            import time
            time.sleep(2)
        
        return resultados
    
    def limpar_arquivos_locais(self):
        """Remove arquivos PDF baixados localmente"""
        try:
            import shutil
            if os.path.exists(self.diretorio_downloads):
                shutil.rmtree(self.diretorio_downloads)
                logger.info(f"🗑️ Diretório limpo: {self.diretorio_downloads}")
        except Exception as e:
            logger.error(f"❌ Erro ao limpar arquivos: {e}")

def main():
    """Teste do extrator de PDFs"""
    extrator = ExtratorPDF()
    
    # URLs de exemplo para teste
    urls_teste = [
        "https://www.ufmg.br/prograd/wp-content/uploads/2024/01/edital_exemplo.pdf",
        "https://www.fapemig.br/wp-content/uploads/2024/01/chamada_exemplo.pdf"
    ]
    
    print("🧪 Testando extrator de PDFs...")
    
    for url in urls_teste:
        print(f"\n🔍 Testando: {url}")
        resultado = extrator.extrair_de_url(url)
        
        if 'erro' not in resultado:
            print(f"✅ Páginas: {resultado.get('num_paginas', 'N/A')}")
            print(f"📊 Caracteres: {resultado.get('estatisticas', {}).get('total_caracteres', 'N/A')}")
            print(f"💰 Valor encontrado: {resultado.get('valor', 'N/A')}")
            print(f"📅 Prazo encontrado: {resultado.get('prazo', 'N/A')}")
        else:
            print(f"❌ Erro: {resultado['erro']}")
    
    # Limpar arquivos de teste
    extrator.limpar_arquivos_locais()

if __name__ == "__main__":
    main()
