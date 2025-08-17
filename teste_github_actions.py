#!/usr/bin/env python3
"""
Script de teste para verificar se o ambiente GitHub Actions está funcionando
"""

import os
import sys

def main():
    """Teste básico do ambiente"""
    print("=" * 50)
    print("🧪 TESTE GITHUB ACTIONS - AMBIENTE")
    print("=" * 50)
    
    # Verificar Python
    print(f"🐍 Python: {sys.version}")
    
    # Verificar variáveis de ambiente
    print(f"📧 EMAIL_USER: {'✅ Configurado' if 'EMAIL_USER' in os.environ else '❌ Não configurado'}")
    print(f"🔐 EMAIL_PASS: {'✅ Configurado' if 'EMAIL_PASS' in os.environ else '❌ Não configurado'}")
    
    # Verificar diretório de trabalho
    print(f"📁 Diretório atual: {os.getcwd()}")
    
    # Listar arquivos
    print("\n📋 Arquivos no diretório:")
    for file in os.listdir('.'):
        if file.endswith('.py') or file.endswith('.txt') or file.endswith('.yml'):
            print(f"   - {file}")
    
    print("\n✅ Teste de ambiente concluído!")
    return True

if __name__ == "__main__":
    main()
