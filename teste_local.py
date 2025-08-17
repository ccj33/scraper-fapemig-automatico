#!/usr/bin/env python3
"""
Script de teste local para o scraper FAPEMIG
Execute este arquivo para testar se tudo está funcionando antes de subir para o GitHub
"""

import os
import sys

def testar_dependencias():
    """Testa se todas as dependências estão instaladas"""
    print("🔍 Testando dependências...")
    
    try:
        import selenium
        print(f"✅ Selenium: {selenium.__version__}")
    except ImportError:
        print("❌ Selenium não encontrado. Execute: pip install selenium")
        return False
    
    try:
        import chromedriver_autoinstaller
        print("✅ chromedriver-autoinstaller encontrado")
    except ImportError:
        print("❌ chromedriver-autoinstaller não encontrado. Execute: pip install chromedriver-autoinstaller")
        return False
    
    return True

def testar_ambiente():
    """Testa se o ambiente está configurado corretamente"""
    print("\n🔍 Testando ambiente...")
    
    # Verifica se estamos na pasta correta
    if not os.path.exists("scraper.py"):
        print("❌ scraper.py não encontrado. Execute este script da pasta meu-scraper/")
        return False
    
    print("✅ Arquivo scraper.py encontrado")
    
    # Verifica se o Chrome está disponível (opcional)
    try:
        import subprocess
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Chrome encontrado: {result.stdout.strip()}")
        else:
            print("⚠️ Chrome não encontrado (não é obrigatório para teste local)")
    except:
        print("⚠️ Chrome não encontrado (não é obrigatório para teste local)")
    
    return True

def testar_scraper():
    """Testa o scraper em modo de teste (sem envio de email)"""
    print("\n🚀 Testando scraper...")
    
    # Simula ambiente do GitHub Actions
    os.environ['EMAIL_USER'] = 'teste@exemplo.com'
    os.environ['EMAIL_PASS'] = 'senha_teste'
    
    try:
        # Importa e executa o scraper
        from scraper import extrair_chamadas_fapemig
        
        print("✅ Função extrair_chamadas_fapemig importada com sucesso")
        
        # Testa a extração (pode demorar alguns segundos)
        print("🌐 Iniciando teste de extração...")
        chamadas = extrair_chamadas_fapemig()
        
        if chamadas:
            print(f"✅ Extração bem-sucedida! Encontradas {len(chamadas)} chamadas:")
            for i, chamada in enumerate(chamadas[:3], 1):  # Mostra apenas as 3 primeiras
                print(f"   {i}. {chamada['titulo'][:50]}...")
        else:
            print("⚠️ Nenhuma chamada encontrada (pode ser normal dependendo do site)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar scraper: {e}")
        return False

def main():
    """Função principal de teste"""
    print("=" * 60)
    print("🧪 TESTE LOCAL DO SCRAPER FAPEMIG")
    print("=" * 60)
    
    # Teste 1: Dependências
    if not testar_dependencias():
        print("\n❌ Falha no teste de dependências")
        sys.exit(1)
    
    # Teste 2: Ambiente
    if not testar_ambiente():
        print("\n❌ Falha no teste de ambiente")
        sys.exit(1)
    
    # Teste 3: Scraper
    if not testar_scraper():
        print("\n❌ Falha no teste do scraper")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 TODOS OS TESTES PASSARAM!")
    print("✅ Seu scraper está pronto para ser enviado ao GitHub")
    print("=" * 60)
    
    print("\n📋 Próximos passos:")
    print("1. Configure os secrets no GitHub (EMAIL_USER e EMAIL_PASS)")
    print("2. Faça push do código para o repositório")
    print("3. Verifique a primeira execução automática")
    print("4. Monitore as execuções diárias")

if __name__ == "__main__":
    main()
