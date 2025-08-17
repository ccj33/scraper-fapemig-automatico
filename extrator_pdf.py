#!/usr/bin/env python3
"""
Extrator de Dados de PDFs Melhorado
===================================

Extrai e analisa dados de PDFs de editais e chamadas
com melhor qualidade de texto e padrões mais robustos
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
    """Classe para extrair dados de PDFs com melhor qualidade"""
    
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
                dados.update(self._analisar_conteudo_melhorado(dados['texto_completo']))
            
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
            
            # Extrair texto de todas as páginas com melhor formatação
            texto_completo = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                texto_pagina = page.get_text("text")  # Usar modo "text" para melhor formatação
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
    
    def _analisar_conteudo_melhorado(self, texto: str) -> Dict:
        """Analisa o conteúdo extraído com padrões mais robustos"""
        analise = {}
        
        try:
            # Limpar e normalizar texto
            texto_limpo = self._limpar_texto(texto)
            
            # Padrões melhorados para valores
            analise.update(self._extrair_valores_melhorado(texto_limpo))
            
            # Padrões melhorados para datas
            analise.update(self._extrair_datas_melhorado(texto_limpo))
            
            # Padrões melhorados para prazos
            analise.update(self._extrair_prazos_melhorado(texto_limpo))
            
            # Padrões melhorados para objetivos
            analise.update(self._extrair_objetivos_melhorado(texto_limpo))
            
            # Padrões melhorados para áreas temáticas
            analise.update(self._extrair_areas_melhorado(texto_limpo))
            
            # Estatísticas do texto
            analise['estatisticas'] = {
                'total_caracteres': len(texto),
                'total_palavras': len(texto.split()),
                'total_linhas': len(texto.split('\n')),
                'caracteres_limpos': len(texto_limpo)
            }
            
            # Detectar idioma
            analise['idioma_detectado'] = self._detectar_idioma(texto_limpo)
            
            # Resumo do conteúdo (primeiras linhas)
            linhas = texto_limpo.split('\n')
            analise['resumo_conteudo'] = '\n'.join(linhas[:10]) if len(linhas) > 10 else texto_limpo[:500]
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na análise de conteúdo: {e}")
        
        return analise
    
    def _limpar_texto(self, texto: str) -> str:
        """Limpa e normaliza o texto extraído"""
        if not texto:
            return ""
        
        # Remover caracteres especiais problemáticos
        texto = re.sub(r'[^\w\s\.,;:!?()\[\]{}"\'-]', ' ', texto)
        
        # Normalizar espaços
        texto = re.sub(r'\s+', ' ', texto)
        
        # Normalizar quebras de linha
        texto = re.sub(r'\n\s*\n', '\n', texto)
        
        # Remover linhas muito curtas (provavelmente ruído)
        linhas = texto.split('\n')
        linhas_limpas = [linha.strip() for linha in linhas if len(linha.strip()) > 3]
        
        return '\n'.join(linhas_limpas)
    
    def _extrair_valores_melhorado(self, texto: str) -> Dict:
        """Extrai valores com padrões mais robustos"""
        valores_encontrados = []
        
        # Padrões para valores em reais
        padroes_valor = [
            r'R\$\s*([\d.,]+)',  # R$ 50.000,00
            r'R\$\s*([\d]+(?:\.\d{3})*(?:,\d{2})?)',  # R$ 50.000,00 ou R$ 50000,00
            r'valor[:\s]*R\$\s*([\d.,]+)',  # valor: R$ 100.000,00
            r'até\s*R\$\s*([\d.,]+)',  # até R$ 100.000,00
            r'máximo\s*R\$\s*([\d.,]+)',  # máximo R$ 100.000,00
            r'limite\s*R\$\s*([\d.,]+)',  # limite R$ 100.000,00
            r'([\d.,]+)\s*reais?',  # 50.000,00 reais
            r'([\d.,]+)\s*mil\s*reais',  # 50 mil reais
            r'([\d.,]+)\s*milhões?\s*de\s*reais',  # 2 milhões de reais
        ]
        
        for padrao in padroes_valor:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match) > 0:
                    valores_encontrados.append(match)
        
        # Padrões para valores em outras moedas ou formatos
        padroes_outros = [
            r'USD\s*([\d.,]+)',  # USD 50,000.00
            r'EUR\s*([\d.,]+)',  # EUR 50,000.00
            r'([\d.,]+)\s*dólares?',  # 50,000 dólares
            r'([\d.,]+)\s*euros?',  # 50,000 euros
        ]
        
        for padrao in padroes_outros:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match) > 0:
                    valores_encontrados.append(f"{match} (outra moeda)")
        
        # Remover duplicatas e valores muito pequenos
        valores_unicos = []
        for valor in valores_encontrados:
            if valor not in valores_unicos and len(valor) > 1:
                valores_unicos.append(valor)
        
        return {'valores_encontrados': valores_unicos[:5]} if valores_unicos else {}
    
    def _extrair_datas_melhorado(self, texto: str) -> Dict:
        """Extrai datas com padrões mais robustos"""
        datas_encontradas = []
        
        # Padrões para datas brasileiras
        padroes_data_br = [
            r'(\d{1,2}/\d{1,2}/\d{4})',  # DD/MM/AAAA
            r'(\d{1,2}-\d{1,2}-\d{4})',  # DD-MM-AAAA
            r'(\d{1,2}\.\d{1,2}\.\d{4})',  # DD.MM.AAAA
            r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',  # 15 de agosto de 2025
            r'(\d{1,2}\s+\w+\s+\d{4})',  # 15 agosto 2025
        ]
        
        # Padrões para datas internacionais
        padroes_data_int = [
            r'(\d{4}-\d{1,2}-\d{1,2})',  # AAAA-MM-DD
            r'(\d{1,2}/\d{1,2}/\d{2})',  # DD/MM/AA
            r'(\d{1,2}-\d{1,2}-\d{2})',  # DD-MM-AA
        ]
        
        for padrao in padroes_data_br + padroes_data_int:
            matches = re.findall(padrao, texto)
            for match in matches:
                if match and len(match) > 5:
                    datas_encontradas.append(match)
        
        # Padrões para datas por extenso
        padroes_extenso = [
            r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',  # 15 de agosto de 2025
            r'(\w+\s+\d{1,2},\s+\d{4})',  # agosto 15, 2025
        ]
        
        for padrao in padroes_extenso:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match) > 10:
                    datas_encontradas.append(match)
        
        # Remover duplicatas
        datas_unicas = list(set(datas_encontradas))
        return {'datas_encontradas': datas_unicas[:10]} if datas_unicas else {}
    
    def _extrair_prazos_melhorado(self, texto: str) -> Dict:
        """Extrai prazos com padrões mais robustos"""
        prazos_encontrados = []
        
        # Padrões para prazos
        padroes_prazo = [
            r'prazo.*?(\d{1,2}/\d{1,2}/\d{4})',  # prazo até 30/09/2025
            r'até.*?(\d{1,2}/\d{1,2}/\d{4})',  # até 30/09/2025
            r'vencimento.*?(\d{1,2}/\d{1,2}/\d{4})',  # vencimento 30/09/2025
            r'inscrições.*?(\d{1,2}/\d{1,2}/\d{4})',  # inscrições até 30/09/2025
            r'data\s+limite.*?(\d{1,2}/\d{1,2}/\d{4})',  # data limite 30/09/2025
            r'encerramento.*?(\d{1,2}/\d{1,2}/\d{4})',  # encerramento 30/09/2025
            r'fim.*?(\d{1,2}/\d{1,2}/\d{4})',  # fim 30/09/2025
            r'termino.*?(\d{1,2}/\d{1,2}/\d{4})',  # termino 30/09/2025
        ]
        
        for padrao in padroes_prazo:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match) > 5:
                    prazos_encontrados.append(match)
        
        # Padrões para prazos por extenso
        padroes_extenso = [
            r'prazo.*?(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',  # prazo até 30 de setembro de 2025
            r'até.*?(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',  # até 30 de setembro de 2025
        ]
        
        for padrao in padroes_extenso:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match) > 10:
                    prazos_encontrados.append(match)
        
        # Remover duplicatas
        prazos_unicos = list(set(prazos_encontrados))
        return {'prazos_encontrados': prazos_unicos[:5]} if prazos_unicos else {}
    
    def _extrair_objetivos_melhorado(self, texto: str) -> Dict:
        """Extrai objetivos com padrões mais robustos"""
        objetivos_encontrados = []
        
        # Padrões para objetivos
        padroes_objetivo = [
            r'Objetivo[:\s]*([^.\n]{20,200})',  # Objetivo: descrição...
            r'Objetivos[:\s]*([^.\n]{20,200})',  # Objetivos: descrição...
            r'Descrição[:\s]*([^.\n]{20,200})',  # Descrição: descrição...
            r'Resumo[:\s]*([^.\n]{20,200})',  # Resumo: descrição...
            r'Finalidade[:\s]*([^.\n]{20,200})',  # Finalidade: descrição...
            r'Propósito[:\s]*([^.\n]{20,200})',  # Propósito: descrição...
            r'Justificativa[:\s]*([^.\n]{20,200})',  # Justificativa: descrição...
        ]
        
        for padrao in padroes_objetivo:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match.strip()) > 20:
                    objetivo_limpo = match.strip()
                    objetivos_encontrados.append(objetivo_limpo)
        
        # Padrões para objetivos sem dois pontos
        padroes_sem_colon = [
            r'Objetivo\s+([^.\n]{20,200})',  # Objetivo descrição...
            r'Objetivos\s+([^.\n]{20,200})',  # Objetivos descrição...
        ]
        
        for padrao in padroes_sem_colon:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match.strip()) > 20:
                    objetivo_limpo = match.strip()
                    objetivos_encontrados.append(objetivo_limpo)
        
        # Remover duplicatas e limitar tamanho
        objetivos_unicos = []
        for objetivo in objetivos_encontrados:
            if objetivo not in objetivos_unicos:
                # Limitar a 300 caracteres
                objetivo_limitado = objetivo[:300] + "..." if len(objetivo) > 300 else objetivo
                objetivos_unicos.append(objetivo_limitado)
        
        return {'objetivos_encontrados': objetivos_unicos[:3]} if objetivos_unicos else {}
    
    def _extrair_areas_melhorado(self, texto: str) -> Dict:
        """Extrai áreas temáticas com padrões mais robustos"""
        areas_encontradas = []
        
        # Padrões para áreas temáticas
        padroes_area = [
            r'Área[:\s]*([^.\n]{10,150})',  # Área: descrição...
            r'Áreas[:\s]*([^.\n]{10,150})',  # Áreas: descrição...
            r'Tema[:\s]*([^.\n]{10,150})',  # Tema: descrição...
            r'Temas[:\s]*([^.\n]{10,150})',  # Temas: descrição...
            r'Linha[:\s]*([^.\n]{10,150})',  # Linha: descrição...
            r'Linhas[:\s]*([^.\n]{10,150})',  # Linhas: descrição...
            r'Campo[:\s]*([^.\n]{10,150})',  # Campo: descrição...
            r'Campos[:\s]*([^.\n]{10,150})',  # Campos: descrição...
            r'Disciplina[:\s]*([^.\n]{10,150})',  # Disciplina: descrição...
            r'Especialidade[:\s]*([^.\n]{10,150})',  # Especialidade: descrição...
        ]
        
        for padrao in padroes_area:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match.strip()) > 10:
                    area_limpa = match.strip()
                    areas_encontradas.append(area_limpa)
        
        # Padrões para áreas sem dois pontos
        padroes_sem_colon = [
            r'Área\s+([^.\n]{10,150})',  # Área descrição...
            r'Tema\s+([^.\n]{10,150})',  # Tema descrição...
            r'Linha\s+([^.\n]{10,150})',  # Linha descrição...
        ]
        
        for padrao in padroes_sem_colon:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match.strip()) > 10:
                    area_limpa = match.strip()
                    areas_encontradas.append(area_limpa)
        
        # Remover duplicatas e limitar tamanho
        areas_unicas = []
        for area in areas_encontradas:
            if area not in areas_unicas:
                # Limitar a 200 caracteres
                area_limitada = area[:200] + "..." if len(area) > 200 else area
                areas_unicas.append(area_limitada)
        
        return {'areas_encontradas': areas_unicas[:3]} if areas_unicas else {}
    
    def _detectar_idioma(self, texto: str) -> str:
        """Detecta o idioma do texto"""
        if not texto:
            return "desconhecido"
        
        # Contar palavras em português vs inglês
        palavras_pt = len(re.findall(r'\b(de|para|com|por|em|não|são|está|ser|ter|que|uma|um|este|esta|como|mais|muito|pode|devem|todos|todas|outros|outras|primeiro|segundo|terceiro|quarto|quinto|sexto|sétimo|oitavo|nono|décimo)\b', texto, re.IGNORECASE))
        palavras_en = len(re.findall(r'\b(the|and|for|with|in|is|are|was|were|have|has|will|can|should|would|could|this|that|these|those|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\b', texto, re.IGNORECASE))
        
        if palavras_pt > palavras_en:
            return "português"
        elif palavras_en > palavras_pt:
            return "inglês"
        else:
            return "misto"
    
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
    """Teste do extrator de PDFs melhorado"""
    extrator = ExtratorPDF()
    
    # URLs de exemplo para teste
    urls_teste = [
        "https://www.ufmg.br/prograd/wp-content/uploads/2024/01/edital_exemplo.pdf",
        "https://www.fapemig.br/wp-content/uploads/2024/01/chamada_exemplo.pdf"
    ]
    
    print("🧪 Testando extrator de PDFs melhorado...")
    
    for url in urls_teste:
        print(f"\n🔍 Testando: {url}")
        resultado = extrator.extrair_de_url(url)
        
        if 'erro' not in resultado:
            print(f"✅ Páginas: {resultado.get('num_paginas', 'N/A')}")
            print(f"📊 Caracteres: {resultado.get('estatisticas', {}).get('total_caracteres', 'N/A')}")
            print(f"💰 Valores encontrados: {resultado.get('valores_encontrados', 'N/A')}")
            print(f"📅 Datas encontradas: {resultado.get('datas_encontradas', 'N/A')}")
            print(f"⏰ Prazos encontrados: {resultado.get('prazos_encontrados', 'N/A')}")
            print(f"🎯 Objetivos encontrados: {resultado.get('objetivos_encontrados', 'N/A')}")
            print(f"🔬 Áreas encontradas: {resultado.get('areas_encontradas', 'N/A')}")
        else:
            print(f"❌ Erro: {resultado['erro']}")
    
    # Limpar arquivos de teste
    extrator.limpar_arquivos_locais()

if __name__ == "__main__":
    main()
