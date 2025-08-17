#!/usr/bin/env python3
"""
Extrator de PDF Robusto e Completo
==================================

Resolve todos os problemas críticos identificados:
1. Captura de link direto via Selenium
2. Download robusto com httpx e redirecionamentos
3. Cálculo de hash SHA256 para deduplicação
4. Validação de conteúdo e tipo
5. Fallbacks para OCR e múltiplos métodos de extração
6. Normalização adequada de dados
7. Campos link_pdf e pdf_hash
"""

import os
import hashlib
import logging
import re
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime
from urllib.parse import urlparse, urljoin
import json

# Dependências principais
try:
    import httpx
    import fitz  # PyMuPDF
    import PyPDF2
    from pdfminer.high_level import extract_text as pdfminer_extract
    import pytesseract
    from PIL import Image
    import io
except ImportError as e:
    logging.warning(f"⚠️ Algumas dependências não estão disponíveis: {e}")

# Configuração de logging
logger = logging.getLogger(__name__)

class ExtratorPDFRobusto:
    """Extrator de PDF robusto com todas as funcionalidades necessárias"""
    
    def __init__(self, diretorio_base: str = "data"):
        self.diretorio_base = diretorio_base
        self.diretorio_pdfs = os.path.join(diretorio_base, "pdfs")
        self.diretorio_textos = os.path.join(diretorio_base, "textos")
        self._criar_diretorios()
        
    def _criar_diretorios(self):
        """Cria diretórios necessários"""
        for diretorio in [self.diretorio_base, self.diretorio_pdfs, self.diretorio_textos]:
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)
                logger.info(f"📁 Diretório criado: {diretorio}")
    
    def extrair_de_url_com_selenium(self, driver, url: str, titulo: str = None) -> Dict:
        """
        Extrai PDF usando Selenium para capturar link direto
        
        Args:
            driver: Driver do Selenium
            url: URL da página que contém o PDF
            titulo: Título para identificação
            
        Returns:
            Dicionário com dados extraídos e metadados
        """
        try:
            logger.info(f"🔍 Iniciando extração robusta: {url}")
            
            # Passo 1: Capturar link direto do PDF via Selenium
            link_pdf = self._capturar_link_pdf_selenium(driver, url)
            
            if not link_pdf:
                return {
                    'status_baixa': 'link_nao_encontrado',
                    'erro': 'Não foi possível encontrar link direto para PDF',
                    'url_origem': url,
                    'data_extracao': datetime.now().isoformat()
                }
            
            # Passo 2: Baixar PDF com httpx (robusto)
            pdf_bytes, status_baixa = self._baixar_pdf_robusto(link_pdf)
            
            if not pdf_bytes:
                return {
                    'status_baixa': status_baixa,
                    'erro': f'Falha ao baixar PDF: {status_baixa}',
                    'url_origem': url,
                    'link_pdf': link_pdf,
                    'data_extracao': datetime.now().isoformat()
                }
            
            # Passo 3: Calcular hash e salvar arquivo
            pdf_hash = self._calcular_hash_pdf(pdf_bytes)
            caminho_pdf = os.path.join(self.diretorio_pdfs, f"{pdf_hash}.pdf")
            
            with open(caminho_pdf, 'wb') as f:
                f.write(pdf_bytes)
            
            # Passo 4: Extrair texto com múltiplos fallbacks
            texto_extraido, status_analise = self._extrair_texto_robusto(pdf_bytes)
            
            # Passo 5: Salvar texto extraído
            caminho_texto = os.path.join(self.diretorio_textos, f"{pdf_hash}.txt")
            if texto_extraido:
                with open(caminho_texto, 'w', encoding='utf-8') as f:
                    f.write(texto_extraido)
            
            # Passo 6: Analisar conteúdo normalizado
            analise_conteudo = self._analisar_conteudo_normalizado(texto_extraido) if texto_extraido else {}
            
            # Passo 7: Montar resultado final
            resultado = {
                'status_baixa': status_baixa,
                'status_analise': status_analise,
                'url_origem': url,
                'link_pdf': link_pdf,
                'pdf_hash': pdf_hash,
                'caminho_pdf': caminho_pdf,
                'caminho_texto': caminho_texto,
                'tamanho_bytes': len(pdf_bytes),
                'data_extracao': datetime.now().isoformat(),
                'texto_completo': texto_extraido,
                **analise_conteudo
            }
            
            logger.info(f"✅ Extração robusta concluída: {pdf_hash}")
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro na extração robusta: {e}")
            return {
                'status_baixa': 'erro_critico',
                'erro': str(e),
                'url_origem': url,
                'data_extracao': datetime.now().isoformat()
            }
    
    def _capturar_link_pdf_selenium(self, driver, url: str) -> Optional[str]:
        """Captura link direto do PDF usando Selenium"""
        try:
            # Acessar página
            driver.get(url)
            driver.implicitly_wait(5)
            
            # Estratégia 1: Procurar por links diretos de PDF
            pdf_links = driver.find_elements("css selector", 'a[href*=".pdf"]')
            for link in pdf_links:
                href = link.get_attribute("href")
                if href and self._eh_url_pdf_valida(href):
                    logger.info(f"✅ Link PDF encontrado: {href}")
                    return href
            
            # Estratégia 2: Procurar por botões que abrem PDFs
            botoes_pdf = driver.find_elements("xpath", 
                '//*[contains(text(), "PDF") or contains(text(), "Download") or contains(text(), "Edital")]')
            
            for botao in botoes_pdf:
                try:
                    # Tentar clicar no botão
                    driver.execute_script("arguments[0].click();", botao)
                    driver.implicitly_wait(3)
                    
                    # Verificar se nova aba foi aberta
                    if len(driver.window_handles) > 1:
                        # Mudar para nova aba
                        nova_aba = driver.window_handles[-1]
                        driver.switch_to.window(nova_aba)
                        
                        # Capturar URL final
                        url_final = driver.current_url
                        driver.close()
                        
                        # Voltar para aba original
                        driver.switch_to.window(driver.window_handles[0])
                        
                        if self._eh_url_pdf_valida(url_final):
                            logger.info(f"✅ Link PDF capturado via botão: {url_final}")
                            return url_final
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao clicar no botão: {e}")
                    continue
            
            # Estratégia 3: Procurar por iframes que podem conter PDFs
            iframes = driver.find_elements("tag name", "iframe")
            for iframe in iframes:
                try:
                    driver.switch_to.frame(iframe)
                    iframe_links = driver.find_elements("css selector", 'a[href*=".pdf"]')
                    for link in iframe_links:
                        href = link.get_attribute("href")
                        if href and self._eh_url_pdf_valida(href):
                            driver.switch_to.default_content()
                            logger.info(f"✅ Link PDF encontrado em iframe: {href}")
                            return href
                    driver.switch_to.default_content()
                except:
                    driver.switch_to.default_content()
                    continue
            
            logger.warning(f"⚠️ Nenhum link PDF encontrado em: {url}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao capturar link PDF: {e}")
            return None
    
    def _eh_url_pdf_valida(self, url: str) -> bool:
        """Verifica se URL é um PDF válido"""
        if not url:
            return False
        
        # Verificar extensão
        if url.lower().endswith('.pdf'):
            return True
        
        # Verificar se contém 'pdf' na URL
        if 'pdf' in url.lower():
            return True
        
        # Verificar se é uma URL válida
        try:
            parsed = urlparse(url)
            return bool(parsed.scheme and parsed.netloc)
        except:
            return False
    
    def _baixar_pdf_robusto(self, url: str) -> Tuple[Optional[bytes], str]:
        """Baixa PDF usando httpx com redirecionamentos"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            with httpx.Client(follow_redirects=True, timeout=30.0) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                
                # Verificar se é realmente um PDF
                content_type = response.headers.get('content-type', '').lower()
                if 'application/pdf' not in content_type and 'pdf' not in content_type:
                    return None, 'nao_pdf'
                
                # Verificar tamanho mínimo
                if len(response.content) < 1000:  # Menos de 1KB
                    return None, 'arquivo_muito_pequeno'
                
                logger.info(f"📥 PDF baixado: {len(response.content)} bytes")
                return response.content, 'ok'
                
        except httpx.TimeoutException:
            return None, 'timeout'
        except httpx.HTTPStatusError as e:
            return None, f'erro_http_{e.response.status_code}'
        except Exception as e:
            logger.error(f"❌ Erro ao baixar PDF: {e}")
            return None, 'erro_download'
    
    def _calcular_hash_pdf(self, pdf_bytes: bytes) -> str:
        """Calcula hash SHA256 do PDF"""
        return hashlib.sha256(pdf_bytes).hexdigest()
    
    def _extrair_texto_robusto(self, pdf_bytes: bytes) -> Tuple[Optional[str], str]:
        """Extrai texto com múltiplos fallbacks"""
        texto_extraido = None
        
        # Método 1: PyMuPDF (mais robusto)
        try:
            texto_extraido = self._extrair_com_pymupdf(pdf_bytes)
            if texto_extraido and len(texto_extraido.strip()) > 800:
                return texto_extraido, 'ok'
        except Exception as e:
            logger.warning(f"⚠️ PyMuPDF falhou: {e}")
        
        # Método 2: PyPDF2
        try:
            texto_extraido = self._extrair_com_pypdf2(pdf_bytes)
            if texto_extraido and len(texto_extraido.strip()) > 800:
                return texto_extraido, 'ok'
        except Exception as e:
            logger.warning(f"⚠️ PyPDF2 falhou: {e}")
        
        # Método 3: pdfminer.six
        try:
            texto_extraido = self._extrair_com_pdfminer(pdf_bytes)
            if texto_extraido and len(texto_extraido.strip()) > 800:
                return texto_extraido, 'ok'
        except Exception as e:
            logger.warning(f"⚠️ pdfminer falhou: {e}")
        
        # Método 4: OCR com Tesseract (primeiras páginas)
        try:
            texto_extraido = self._extrair_com_ocr(pdf_bytes)
            if texto_extraido and len(texto_extraido.strip()) > 800:
                return texto_extraido, 'ok_ocr'
        except Exception as e:
            logger.warning(f"⚠️ OCR falhou: {e}")
        
        # Se nenhum método funcionou
        if texto_extraido and len(texto_extraido.strip()) > 0:
            return texto_extraido, 'texto_insuficiente'
        
        return None, 'falha_total'
    
    def _extrair_com_pymupdf(self, pdf_bytes: bytes) -> Optional[str]:
        """Extrai texto usando PyMuPDF"""
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            texto_completo = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                texto_pagina = page.get_text("text")
                texto_completo.append(texto_pagina)
            
            doc.close()
            return '\n'.join(texto_completo)
        except Exception as e:
            logger.warning(f"⚠️ PyMuPDF falhou: {e}")
            return None
    
    def _extrair_com_pypdf2(self, pdf_bytes: bytes) -> Optional[str]:
        """Extrai texto usando PyPDF2"""
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PyPDF2.PdfReader(pdf_file)
            texto_completo = []
            
            for page in reader.pages:
                texto_pagina = page.extract_text()
                if texto_pagina:
                    texto_completo.append(texto_pagina)
            
            return '\n'.join(texto_completo)
        except Exception as e:
            logger.warning(f"⚠️ PyPDF2 falhou: {e}")
            return None
    
    def _extrair_com_pdfminer(self, pdf_bytes: bytes) -> Optional[str]:
        """Extrai texto usando pdfminer.six"""
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            texto = pdfminer_extract(pdf_file)
            return texto
        except Exception as e:
            logger.warning(f"⚠️ pdfminer falhou: {e}")
            return None
    
    def _extrair_com_ocr(self, pdf_bytes: bytes, max_paginas: int = 3) -> Optional[str]:
        """Extrai texto usando OCR (primeiras páginas)"""
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            texto_completo = []
            
            for page_num in range(min(len(doc), max_paginas)):
                page = doc.load_page(page_num)
                
                # Converter página para imagem
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom para melhor qualidade
                img_data = pix.tobytes("png")
                
                # Usar PIL para abrir imagem
                img = Image.open(io.BytesIO(img_data))
                
                # OCR com Tesseract
                texto_pagina = pytesseract.image_to_string(img, lang='por+eng')
                if texto_pagina.strip():
                    texto_completo.append(texto_pagina)
            
            doc.close()
            return '\n'.join(texto_completo)
        except Exception as e:
            logger.warning(f"⚠️ OCR falhou: {e}")
            return None
    
    def _analisar_conteudo_normalizado(self, texto: str) -> Dict:
        """Analisa conteúdo com normalização adequada"""
        if not texto:
            return {}
        
        # Limpar e normalizar texto
        texto_limpo = self._normalizar_texto(texto)
        
        # Extrair informações com padrões robustos
        analise = {}
        
        # Valores monetários (padrões robustos)
        analise.update(self._extrair_valores_monetarios(texto_limpo))
        
        # Datas (padrões robustos)
        analise.update(self._extrair_datas_robustas(texto_limpo))
        
        # Prazos (padrões robustos)
        analise.update(self._extrair_prazos_robustos(texto_limpo))
        
        # Objetivos (texto completo, sem truncamento)
        analise.update(self._extrair_objetivos_completos(texto_limpo))
        
        # Áreas temáticas (texto completo, sem truncamento)
        analise.update(self._extrair_areas_completas(texto_limpo))
        
        # Estatísticas
        analise['estatisticas'] = {
            'total_caracteres': len(texto),
            'total_palavras': len(texto.split()),
            'total_linhas': len(texto.split('\n')),
            'caracteres_limpos': len(texto_limpo)
        }
        
        return analise
    
    def _normalizar_texto(self, texto: str) -> str:
        """Normaliza texto removendo problemas comuns"""
        if not texto:
            return ""
        
        # Remover hífens de quebra de linha
        texto = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', texto)
        
        # Normalizar espaços duplicados
        texto = re.sub(r'\s+', ' ', texto)
        
        # Normalizar quebras de linha
        texto = re.sub(r'\n\s*\n', '\n', texto)
        
        # Remover caracteres invisíveis problemáticos
        texto = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', texto)
        
        # Limpar linhas muito curtas (ruído)
        linhas = texto.split('\n')
        linhas_limpas = [linha.strip() for linha in linhas if len(linha.strip()) > 3]
        
        return '\n'.join(linhas_limpas)
    
    def _extrair_valores_monetarios(self, texto: str) -> Dict:
        """Extrai valores monetários com padrões robustos"""
        valores_encontrados = []
        
        # Padrões para valores em reais (robustos)
        padroes_valor = [
            r'R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',  # R$ 50.000,00
            r'R\$\s*(\d+(?:,\d{2})?)',  # R$ 50000,00
            r'valor[:\s]*R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',  # valor: R$ 100.000,00
            r'até\s*R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',  # até R$ 100.000,00
            r'máximo\s*R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',  # máximo R$ 100.000,00
            r'limite\s*R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',  # limite R$ 100.000,00
        ]
        
        for padrao in padroes_valor:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match) > 1:
                    # Validar se é um valor monetário válido
                    if self._eh_valor_monetario_valido(match):
                        valores_encontrados.append(f"R$ {match}")
        
        # Padrões para valores por extenso
        padroes_extenso = [
            r'(\d+(?:\.\d{3})*(?:,\d{2})?)\s*mil\s*reais?',  # 50 mil reais
            r'(\d+(?:\.\d{3})*(?:,\d{2})?)\s*milhões?\s*de\s*reais?',  # 2 milhões de reais
        ]
        
        for padrao in padroes_extenso:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and self._eh_valor_monetario_valido(match):
                    valores_encontrados.append(f"R$ {match}")
        
        # Remover duplicatas e valores muito pequenos
        valores_unicos = []
        for valor in valores_encontrados:
            if valor not in valores_unicos:
                valores_unicos.append(valor)
        
        return {'valores_encontrados': valores_unicos[:5]} if valores_unicos else {}
    
    def _eh_valor_monetario_valido(self, valor: str) -> bool:
        """Valida se um valor monetário é válido"""
        if not valor:
            return False
        
        # Deve ter pelo menos 3 caracteres
        if len(valor) < 3:
            return False
        
        # Deve conter apenas números, pontos e vírgulas
        if not re.match(r'^[\d.,]+$', valor):
            return False
        
        # Deve ter formato válido (não apenas números isolados)
        if re.match(r'^\d{1,2}$', valor):  # Apenas 1-2 dígitos
            return False
        
        return True
    
    def _extrair_datas_robustas(self, texto: str) -> Dict:
        """Extrai datas com padrões robustos"""
        datas_encontradas = []
        
        # Padrões para datas brasileiras (robustos)
        padroes_data_br = [
            r'(\d{1,2}/\d{1,2}/\d{4})',  # DD/MM/AAAA
            r'(\d{1,2}-\d{1,2}-\d{4})',  # DD-MM-AAAA
            r'(\d{1,2}\.\d{1,2}\.\d{4})',  # DD.MM.AAAA
        ]
        
        # Padrões para datas por extenso
        padroes_extenso = [
            r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',  # 15 de agosto de 2025
            r'(\w+\s+\d{1,2},\s+\d{4})',  # agosto 15, 2025
        ]
        
        for padrao in padroes_data_br + padroes_extenso:
            matches = re.findall(padrao, texto)
            for match in matches:
                if match and len(match) > 8 and self._eh_data_valida(match):
                    datas_encontradas.append(match)
        
        # Remover duplicatas
        datas_unicas = list(set(datas_encontradas))
        return {'datas_encontradas': datas_unicas[:10]} if datas_unicas else {}
    
    def _eh_data_valida(self, data: str) -> bool:
        """Valida se uma data é válida"""
        if not data:
            return False
        
        # Deve ter formato mínimo
        if len(data) < 8:
            return False
        
        # Deve conter números
        if not re.search(r'\d', data):
            return False
        
        return True
    
    def _extrair_prazos_robustos(self, texto: str) -> Dict:
        """Extrai prazos com padrões robustos"""
        prazos_encontrados = []
        
        # Padrões para prazos (robustos)
        padroes_prazo = [
            r'prazo.*?(\d{1,2}/\d{1,2}/\d{4})',  # prazo até 30/09/2025
            r'até.*?(\d{1,2}/\d{1,2}/\d{4})',  # até 30/09/2025
            r'vencimento.*?(\d{1,2}/\d{1,2}/\d{4})',  # vencimento 30/09/2025
            r'inscrições.*?(\d{1,2}/\d{1,2}/\d{4})',  # inscrições até 30/09/2025
            r'data\s+limite.*?(\d{1,2}/\d{1,2}/\d{4})',  # data limite 30/09/2025
            r'encerramento.*?(\d{1,2}/\d{1,2}/\d{4})',  # encerramento 30/09/2025
        ]
        
        for padrao in padroes_prazo:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and self._eh_data_valida(match):
                    prazos_encontrados.append(match)
        
        # Remover duplicatas
        prazos_unicos = list(set(prazos_encontrados))
        return {'prazos_encontrados': prazos_unicos[:5]} if prazos_unicos else {}
    
    def _extrair_objetivos_completos(self, texto: str) -> Dict:
        """Extrai objetivos completos (sem truncamento)"""
        objetivos_encontrados = []
        
        # Padrões para objetivos (capturar texto completo)
        padroes_objetivo = [
            r'Objetivo[:\s]*([^.\n]{20,500})',  # Objetivo: descrição completa...
            r'Objetivos[:\s]*([^.\n]{20,500})',  # Objetivos: descrição completa...
            r'Descrição[:\s]*([^.\n]{20,500})',  # Descrição: descrição completa...
            r'Resumo[:\s]*([^.\n]{20,500})',  # Resumo: descrição completa...
            r'Finalidade[:\s]*([^.\n]{20,500})',  # Finalidade: descrição completa...
        ]
        
        for padrao in padroes_objetivo:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match.strip()) > 20:
                    objetivo_limpo = match.strip()
                    objetivos_encontrados.append(objetivo_limpo)
        
        # Remover duplicatas
        objetivos_unicos = []
        for objetivo in objetivos_encontrados:
            if objetivo not in objetivos_unicos:
                objetivos_unicos.append(objetivo)
        
        return {'objetivos_encontrados': objetivos_unicos[:5]} if objetivos_unicos else {}
    
    def _extrair_areas_completas(self, texto: str) -> Dict:
        """Extrai áreas temáticas completas (sem truncamento)"""
        areas_encontradas = []
        
        # Padrões para áreas (capturar texto completo)
        padroes_area = [
            r'Área[:\s]*([^.\n]{10,300})',  # Área: descrição completa...
            r'Áreas[:\s]*([^.\n]{10,300})',  # Áreas: descrição completa...
            r'Tema[:\s]*([^.\n]{10,300})',  # Tema: descrição completa...
            r'Temas[:\s]*([^.\n]{10,300})',  # Temas: descrição completa...
            r'Linha[:\s]*([^.\n]{10,300})',  # Linha: descrição completa...
            r'Campo[:\s]*([^.\n]{10,300})',  # Campo: descrição completa...
        ]
        
        for padrao in padroes_area:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if match and len(match.strip()) > 10:
                    area_limpa = match.strip()
                    areas_encontradas.append(area_limpa)
        
        # Remover duplicatas
        areas_unicas = []
        for area in areas_encontradas:
            if area not in areas_unicas:
                areas_unicas.append(area)
        
        return {'areas_encontradas': areas_unicas[:5]} if areas_unicas else {}
    
    def limpar_arquivos(self):
        """Remove arquivos baixados"""
        try:
            import shutil
            if os.path.exists(self.diretorio_base):
                shutil.rmtree(self.diretorio_base)
                logger.info(f"🗑️ Diretório limpo: {self.diretorio_base}")
        except Exception as e:
            logger.error(f"❌ Erro ao limpar arquivos: {e}")

def main():
    """Teste do extrator robusto"""
    print("🧪 Testando extrator de PDF robusto...")
    
    # Este é apenas um teste básico - o uso real requer Selenium
    extrator = ExtratorPDFRobusto()
    
    # Testar normalização de texto
    texto_teste = """
    Este é um texto com hífens de quebra
    de linha e espaços    duplicados.
    
    Objetivo: Desenvolver uma solução inovadora para
    problemas complexos de engenharia.
    
    Valor: R$ 50.000,00 até 30/09/2025
    """
    
    texto_normalizado = extrator._normalizar_texto(texto_teste)
    print(f"Texto normalizado:\n{texto_normalizado}")
    
    # Testar extração de valores
    valores = extrator._extrair_valores_monetarios(texto_normalizado)
    print(f"Valores encontrados: {valores}")
    
    # Testar extração de datas
    datas = extrator._extrair_datas_robustas(texto_normalizado)
    print(f"Datas encontradas: {datas}")
    
    # Testar extração de objetivos
    objetivos = extrator._extrair_objetivos_completos(texto_normalizado)
    print(f"Objetivos encontrados: {objetivos}")

if __name__ == "__main__":
    main()
