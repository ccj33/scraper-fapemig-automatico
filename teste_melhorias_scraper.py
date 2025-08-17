#!/usr/bin/env python3
"""
Teste das Melhorias do Scraper Robusto
======================================

Testa as melhorias implementadas:
1. Captura de contexto das páginas
2. Extração de mais detalhes
3. Melhor formatação dos resumos
"""

import os
import sys
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def testar_melhorias():
    """Testa as melhorias implementadas"""
    logger.info("🧪 Iniciando teste das melhorias do scraper...")
    
    try:
        # Importar o scraper melhorado
        from scraper_robusto_unificado import ScraperRobustoUnificado, FAPEMIGScraperRobusto, CNPqScraperRobusto
        
        # Criar instância
        scraper = ScraperRobustoUnificado()
        
        # Testar configuração do driver
        logger.info("🔧 Testando configuração do driver...")
        scraper.setup_driver()
        logger.info("✅ Driver configurado com sucesso")
        
        # Testar extração da FAPEMIG
        logger.info("🔍 Testando extração FAPEMIG...")
        fapemig_scraper = FAPEMIGScraperRobusto(scraper.driver)
        chamadas = fapemig_scraper.extract_chamadas()
        
        logger.info(f"📊 FAPEMIG: {len(chamadas)} chamadas encontradas")
        
        # Verificar se os novos campos estão sendo capturados
        for i, chamada in enumerate(chamadas[:3], 1):  # Primeiras 3
            logger.info(f"\n🔸 Chamada #{i}:")
            logger.info(f"   Título: {chamada.get('titulo', 'N/A')}")
            logger.info(f"   Contexto: {chamada.get('contexto', 'N/A')[:100]}...")
            logger.info(f"   URL: {chamada.get('url', 'N/A')}")
            logger.info(f"   PDF Extraído: {chamada.get('pdf_extraido', False)}")
            
            if chamada.get('pdf_extraido'):
                logger.info(f"   PDF Hash: {chamada.get('pdf_hash', 'N/A')[:16]}...")
        
        # Testar extração do CNPq
        logger.info("\n🔍 Testando extração CNPq...")
        cnpq_scraper = CNPqScraperRobusto(scraper.driver)
        chamadas_cnpq = cnpq_scraper.extract_chamadas()
        
        logger.info(f"📊 CNPq: {len(chamadas_cnpq)} chamadas encontradas")
        
        # Verificar campos do CNPq
        for i, chamada in enumerate(chamadas_cnpq[:3], 1):  # Primeiras 3
            logger.info(f"\n🔸 Chamada CNPq #{i}:")
            logger.info(f"   Título: {chamada.get('titulo', 'N/A')}")
            logger.info(f"   Contexto: {chamada.get('contexto', 'N/A')[:100]}...")
            logger.info(f"   Período: {chamada.get('periodo_inscricao', 'N/A')}")
            logger.info(f"   URL Detalhes: {chamada.get('url_detalhes', 'N/A')}")
        
        # Testar geração de resumo
        logger.info("\n📝 Testando geração de resumo...")
        scraper.results = {
            'fapemig': chamadas,
            'cnpq': chamadas_cnpq,
            'ufmg': [],
            'total_editais': len(chamadas) + len(chamadas_cnpq)
        }
        
        resumo = scraper.gerar_resumo_completo()
        logger.info("✅ Resumo gerado com sucesso")
        
        # Salvar resumo de teste
        with open("resumo_teste_melhorias.txt", "w", encoding="utf-8") as f:
            f.write(resumo)
        
        logger.info("💾 Resumo salvo em 'resumo_teste_melhorias.txt'")
        
        # Mostrar estatísticas
        logger.info("\n📊 ESTATÍSTICAS DO TESTE:")
        logger.info(f"   FAPEMIG: {len(chamadas)} chamadas")
        logger.info(f"   CNPq: {len(chamadas_cnpq)} chamadas")
        logger.info(f"   Total: {len(chamadas) + len(chamadas_cnpq)} oportunidades")
        
        # Verificar campos novos
        campos_novos = ['contexto', 'objetivo', 'area']
        for campo in campos_novos:
            fapemig_com_campo = sum(1 for c in chamadas if c.get(campo))
            cnpq_com_campo = sum(1 for c in chamadas_cnpq if c.get(campo))
            logger.info(f"   {campo.capitalize()}: FAPEMIG={fapemig_com_campo}, CNPq={cnpq_com_campo}")
        
        logger.info("\n🎉 Teste das melhorias concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Limpeza
        if 'scraper' in locals():
            scraper.cleanup()

if __name__ == "__main__":
    testar_melhorias()
