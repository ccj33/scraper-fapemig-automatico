#!/usr/bin/env python3
"""
Arquivo de teste para GitHub Actions
Verifica o ambiente e configurações básicas antes de executar o scraper
"""

import os
import sys
import json
from datetime import datetime

def testar_ambiente():
    """Testa o ambiente básico do Python"""
    print("🧪 Testando ambiente Python...")
    
    # Verificar versão do Python
    print(f"✅ Python {sys.version}")
    
    # Verificar diretório de trabalho
    print(f"✅ Diretório de trabalho: {os.getcwd()}")
    
    # Verificar arquivos disponíveis
    arquivos = os.listdir('.')
    print(f"✅ Arquivos no diretório: {len(arquivos)} arquivos encontrados")
    
    # Verificar se requirements.txt existe
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt encontrado")
        with open('requirements.txt', 'r') as f:
            dependencias = f.read().strip().split('\n')
        print(f"✅ Dependências: {len(dependencias)} pacotes listados")
    else:
        print("❌ requirements.txt não encontrado")
        return False
    
    return True

def testar_variaveis_ambiente():
    """Testa as variáveis de ambiente necessárias"""
    print("\n🔧 Testando variáveis de ambiente...")
    
    variaveis_necessarias = ['EMAIL_USER', 'EMAIL_PASS']
    todas_ok = True
    
    for var in variaveis_necessarias:
        valor = os.getenv(var)
        if valor:
            print(f"✅ {var}: {'*' * len(valor)} (configurada)")
        else:
            print(f"❌ {var}: não configurada")
            todas_ok = False
    
    return todas_ok

def testar_importacoes():
    """Testa se as bibliotecas principais podem ser importadas"""
    print("\n📚 Testando importações...")
    
    bibliotecas = [
        'requests',
        'beautifulsoup4',
        'pandas',
        'selenium',
        'openpyxl'
    ]
    
    todas_ok = True
    
    for lib in bibliotecas:
        try:
            __import__(lib)
            print(f"✅ {lib}: importada com sucesso")
        except ImportError as e:
            print(f"❌ {lib}: erro na importação - {e}")
            todas_ok = False
    
    return todas_ok

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes do GitHub Actions")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print("=" * 50)
    
    # Executar todos os testes
    teste1 = testar_ambiente()
    teste2 = testar_variaveis_ambiente()
    teste3 = testar_importacoes()
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    print(f"✅ Ambiente: {'OK' if teste1 else 'FALHOU'}")
    print(f"✅ Variáveis de ambiente: {'OK' if teste2 else 'FALHOU'}")
    print(f"✅ Importações: {'OK' if teste3 else 'FALHOU'}")
    
    if all([teste1, teste2, teste3]):
        print("\n🎉 Todos os testes passaram! Ambiente pronto para execução.")
        sys.exit(0)
    else:
        print("\n❌ Alguns testes falharam. Verifique as configurações.")
        sys.exit(1)

if __name__ == "__main__":
    main()
