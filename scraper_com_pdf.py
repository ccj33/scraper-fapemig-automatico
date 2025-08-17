#!/usr/bin/env python3
"""
Scraper Unificado com Extração de PDFs
======================================

Sistema completo que:
1. Coleta dados de editais e chamadas
2. Extrai dados de PDFs quando disponíveis
3. Gera relatórios enriquecidos
"""

import logging
import json
from datetime import datetime
from scraper_unificado import ScraperUnificado
from integrador_pdf import IntegradorPDF
from gerador_resumo_melhorado import GeradorResumoMelhorado

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_com_pdf.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScraperComPDF:
    """Sistema completo de scraping com extração de PDFs"""
    
    def __init__(self):
        self.scraper = ScraperUnificado()
        self.integrador = IntegradorPDF()
        self.gerador = None
        
    def executar_scraping_completo(self) -> Dict:
        """
        Executa o processo completo:
        1. Scraping dos sites
        2. Extração de PDFs
        3. Geração de relatórios
        """
        logger.info("🚀 Iniciando processo completo de scraping com PDFs...")
        
        try:
            # Etapa 1: Scraping tradicional
            logger.info("📡 Etapa 1: Executando scraping tradicional...")
            dados_scraping = self.scraper.executar_scraping_completo()
            
            if not dados_scraping:
                logger.error("❌ Falha no scraping tradicional")
                return None
            
            logger.info(f"✅ Scraping concluído: {dados_scraping.get('total_editais', 0)} oportunidades encontradas")
            
            # Etapa 2: Extração de PDFs
            logger.info("📄 Etapa 2: Extraindo dados de PDFs...")
            dados_enriquecidos = self.integrador.processar_editais_com_pdfs(dados_scraping)
            
            logger.info(f"✅ PDFs processados: {dados_enriquecidos['pdf_metadata']['total_pdfs_processados']} extraídos")
            
            # Etapa 3: Geração de relatórios
            logger.info("📊 Etapa 3: Gerando relatórios...")
            self.gerador = GeradorResumoMelhorado(dados_enriquecidos)
            resumo_completo = self.gerador.gerar_resumo_completo()
            
            # Salvar dados enriquecidos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_dados = f"dados_completos_com_pdf_{timestamp}.json"
            self.integrador.salvar_dados_enriquecidos(dados_enriquecidos, arquivo_dados)
            
            # Salvar resumo em texto
            arquivo_resumo = f"resumo_completo_com_pdf_{timestamp}.txt"
            with open(arquivo_resumo, 'w', encoding='utf-8') as f:
                f.write(resumo_completo)
            
            logger.info(f"💾 Dados salvos: {arquivo_dados}")
            logger.info(f"💾 Resumo salvo: {arquivo_resumo}")
            
            # Retornar dados completos
            return {
                'dados_enriquecidos': dados_enriquecidos,
                'resumo_completo': resumo_completo,
                'arquivos_gerados': {
                    'dados': arquivo_dados,
                    'resumo': arquivo_resumo
                },
                'timestamp': timestamp
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no processo completo: {e}")
            return None
    
    def executar_apenas_pdfs(self, dados_existentes: Dict) -> Dict:
        """
        Executa apenas a extração de PDFs em dados já existentes
        
        Args:
            dados_existentes: Dados de scraping já coletados
            
        Returns:
            Dados enriquecidos com PDFs
        """
        logger.info("📄 Executando apenas extração de PDFs...")
        
        try:
            dados_enriquecidos = self.integrador.processar_editais_com_pdfs(dados_existentes)
            
            # Salvar dados
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_dados = f"dados_pdf_enriquecidos_{timestamp}.json"
            self.integrador.salvar_dados_enriquecidos(dados_enriquecidos, arquivo_dados)
            
            logger.info(f"💾 Dados com PDFs salvos: {arquivo_dados}")
            
            return dados_enriquecidos
            
        except Exception as e:
            logger.error(f"❌ Erro na extração de PDFs: {e}")
            return None
    
    def gerar_relatorio_pdf(self, dados: Dict) -> str:
        """
        Gera relatório específico sobre PDFs extraídos
        
        Args:
            dados: Dados enriquecidos com PDFs
            
        Returns:
            Relatório formatado
        """
        if not self.gerador:
            self.gerador = GeradorResumoMelhorado(dados)
        
        return self.gerador.gerar_resumo_completo()
    
    def limpar_arquivos_temporarios(self):
        """Limpa arquivos PDF baixados e temporários"""
        try:
            self.integrador.limpar_arquivos_pdf()
            logger.info("🗑️ Arquivos temporários limpos")
        except Exception as e:
            logger.warning(f"⚠️ Erro ao limpar arquivos: {e}")

def main():
    """Função principal para teste"""
    scraper_pdf = ScraperComPDF()
    
    print("🧪 Testando sistema completo de scraping com PDFs...")
    
    # Opção 1: Executar processo completo
    print("\n🔍 Opção 1: Executar processo completo")
    resultado = scraper_pdf.executar_scraping_completo()
    
    if resultado:
        print(f"\n✅ Processo concluído com sucesso!")
        print(f"📊 Total de oportunidades: {resultado['dados_enriquecidos'].get('total_editais', 0)}")
        print(f"📄 PDFs extraídos: {resultado['dados_enriquecidos']['pdf_metadata']['total_pdfs_processados']}")
        print(f"💾 Arquivos gerados:")
        for tipo, arquivo in resultado['arquivos_gerados'].items():
            print(f"   • {tipo}: {arquivo}")
        
        # Mostrar resumo
        print(f"\n📋 RESUMO EXECUTIVO:")
        print("=" * 50)
        print(resultado['resumo_completo'][:1000] + "...")
        
    else:
        print("❌ Falha no processo completo")
    
    # Limpar arquivos temporários
    scraper_pdf.limpar_arquivos_temporarios()

if __name__ == "__main__":
    main()
