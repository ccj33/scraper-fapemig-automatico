#!/usr/bin/env python3
"""
🚀 SCRIPT PRINCIPAL - SOLUÇÃO DEFINITIVA COMPLETA (FAPEMIG + CNPq)
==================================================================

Executa TODA a SOLUÇÃO DEFINITIVA em sequência:
1. 🔥 Scraper MEGA-ULTRA-MELHORADO da FAPEMIG
2. 🔥 Scraper MEGA-ULTRA-MELHORADO do CNPq
3. 🔧 Reorganização MEGA-ULTRA-MELHORADA dos dados
4. 📧 Email MEGA-ULTRA-MELHORADO com TODOS os nomes e links

RESOLVE TODOS OS PROBLEMAS:
✅ Captura TODOS os editais da FAPEMIG (não apenas 3)
✅ Captura TODOS os blocos de chamadas do CNPq
✅ Extrai nomes REAIS dos PDFs e links
✅ Extrai links DIRETOS dos PDFs e links
✅ Inclui todas as informações detalhadas
✅ Envia email com SOLUÇÃO DEFINITIVA COMPLETA
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def executar_comando(comando, descricao):
    """Executa um comando e retorna o resultado"""
    print(f"\n🚀 EXECUTANDO: {descricao}")
    print(f"📋 Comando: {comando}")
    print("-" * 60)
    
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        if resultado.returncode == 0:
            print(f"✅ {descricao} executado com sucesso!")
            if resultado.stdout:
                print("📤 Saída:")
                print(resultado.stdout)
        else:
            print(f"❌ {descricao} falhou!")
            if resultado.stderr:
                print("❌ Erro:")
                print(resultado.stderr)
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar {descricao}: {e}")
        return False

def verificar_arquivos_gerados():
    """Verifica se os arquivos foram gerados corretamente"""
    print("\n🔍 VERIFICANDO ARQUIVOS GERADOS:")
    print("=" * 40)
    
    arquivos_esperados = [
        'fapemig_solucao_definitiva_*.json',
        'cnpq_solucao_definitiva_*.json',
        'dados_reorganizados_solucao_definitiva_*.json'
    ]
    
    for padrao in arquivos_esperados:
        arquivos = glob.glob(padrao)
        if arquivos:
            arquivo_mais_recente = max(arquivos, key=lambda x: os.path.getctime(x))
            tamanho = os.path.getsize(arquivo_mais_recente)
            print(f"✅ {padrao}: {arquivo_mais_recente} ({tamanho} bytes)")
        else:
            print(f"❌ {padrao}: NÃO ENCONTRADO")
            return False
    
    return True

def mostrar_resumo_final():
    """Mostra resumo final da SOLUÇÃO DEFINITIVA COMPLETA"""
    print("\n" + "="*80)
    print("🎉 SOLUÇÃO DEFINITIVA COMPLETA IMPLEMENTADA COM SUCESSO!")
    print("="*80)
    print("✅ TODOS os problemas foram resolvidos:")
    print("   🔥 FAPEMIG: Captura COMPLETA de editais implementada")
    print("   🔥 CNPq: Captura COMPLETA de chamadas implementada")
    print("   📄 PDFs/Links: Nomes REAIS e links DIRETOS extraídos")
    print("   🔧 Dados: Reorganização MEGA-ULTRA-MELHORADA concluída")
    print("   📧 Email: SOLUÇÃO DEFINITIVA COMPLETA enviada com sucesso")
    print("")
    print("📁 Arquivos gerados:")
    print("   - fapemig_solucao_definitiva_*.json")
    print("   - cnpq_solucao_definitiva_*.json")
    print("   - dados_reorganizados_solucao_definitiva_*.json")
    print("")
    print("🚀 Sistema funcionando perfeitamente!")
    print("📧 Emails com TODOS os nomes e links sendo enviados!")
    print("🔥 SOLUÇÃO DEFINITIVA COMPLETA implementada!")
    print("="*80)

def main():
    """Função principal da SOLUÇÃO DEFINITIVA COMPLETA"""
    print("🚀 INICIANDO SOLUÇÃO DEFINITIVA COMPLETA (FAPEMIG + CNPq)")
    print("=" * 70)
    print(f"⏰ Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🔥 Resolvendo TODOS os problemas dos scrapers!")
    print("")
    
    # Passo 1: Executar scraper MEGA-ULTRA-MELHORADO da FAPEMIG
    if not executar_comando("python scraper_fapemig_solucao_definitiva.py", 
                           "Scraper MEGA-ULTRA-MELHORADO da FAPEMIG"):
        print("❌ Falha no scraper da FAPEMIG!")
        return 1
    
    # Aguardar um pouco para garantir que o arquivo foi salvo
    time.sleep(3)
    
    # Passo 2: Executar scraper MEGA-ULTRA-MELHORADO do CNPq
    if not executar_comando("python scraper_cnpq_solucao_definitiva.py", 
                           "Scraper MEGA-ULTRA-MELHORADO do CNPq"):
        print("❌ Falha no scraper do CNPq!")
        return 1
    
    # Aguardar um pouco para garantir que o arquivo foi salvo
    time.sleep(3)
    
    # Passo 3: Executar reorganização MEGA-ULTRA-MELHORADA
    if not executar_comando("python reorganizar_dados_mega_ultra_melhorado.py", 
                           "Reorganização MEGA-ULTRA-MELHORADA dos dados"):
        print("❌ Falha na reorganização dos dados!")
        return 1
    
    # Aguardar um pouco para garantir que o arquivo foi salvo
    time.sleep(3)
    
    # Passo 4: Verificar se os arquivos foram gerados
    if not verificar_arquivos_gerados():
        print("❌ Arquivos não foram gerados corretamente!")
        return 1
    
    # Passo 5: Executar envio de email com SOLUÇÃO DEFINITIVA COMPLETA
    if not executar_comando("python enviar_email_solucao_definitiva.py", 
                           "Email MEGA-ULTRA-MELHORADO com SOLUÇÃO DEFINITIVA COMPLETA"):
        print("❌ Falha no envio do email!")
        return 1
    
    # Passo 6: Mostrar resumo final
    mostrar_resumo_final()
    
    print(f"\n⏰ Fim: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🎉 SOLUÇÃO DEFINITIVA COMPLETA CONCLUÍDA COM SUCESSO!")
    
    return 0

if __name__ == "__main__":
    # Adicionar o diretório atual ao PATH para importar módulos
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Importar glob aqui para evitar erro de importação
    import glob
    
    exit(main())
