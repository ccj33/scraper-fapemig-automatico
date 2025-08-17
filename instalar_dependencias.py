#!/usr/bin/env python3
"""
Script de Instalação de Dependências
====================================

Instala todas as bibliotecas necessárias para o sistema de PDFs
"""

import subprocess
import sys
import os

def instalar_pacote(pacote):
    """Instala um pacote usando pip"""
    try:
        print(f"📦 Instalando {pacote}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
        print(f"✅ {pacote} instalado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {pacote}: {e}")
        return False

def verificar_pacote(pacote):
    """Verifica se um pacote está instalado"""
    try:
        __import__(pacote)
        return True
    except ImportError:
        return False

def main():
    """Função principal de instalação"""
    print("🚀 INSTALADOR DE DEPENDÊNCIAS - SISTEMA DE PDFs")
    print("=" * 60)
    
    # Lista de pacotes necessários
    pacotes = [
        "requests>=2.31.0",
        "PyPDF2>=3.0.0", 
        "PyMuPDF>=1.23.0"
    ]
    
    # Pacotes já existentes
    pacotes_existentes = [
        "selenium",
        "chromedriver-autoinstaller"
    ]
    
    print("📋 Verificando dependências existentes...")
    
    # Verificar pacotes existentes
    for pacote in pacotes_existentes:
        if verificar_pacote(pacote):
            print(f"✅ {pacote} já está instalado")
        else:
            print(f"⚠️ {pacote} não encontrado (será instalado)")
    
    print("\n📦 Instalando novas dependências...")
    
    # Instalar novos pacotes
    sucessos = 0
    total = len(pacotes)
    
    for pacote in pacotes:
        if instalar_pacote(pacote):
            sucessos += 1
        print()  # Linha em branco
    
    # Resumo final
    print("=" * 60)
    print("📊 RESUMO DA INSTALAÇÃO")
    print("=" * 60)
    print(f"✅ Pacotes instalados com sucesso: {sucessos}/{total}")
    
    if sucessos == total:
        print("\n🎉 Todas as dependências foram instaladas!")
        print("💡 Agora você pode executar:")
        print("   python teste_pdf_simples.py")
        print("   python extrator_pdf.py")
        print("   python integrador_pdf.py")
    else:
        print(f"\n⚠️ {total - sucessos} pacotes falharam na instalação")
        print("💡 Tente instalar manualmente:")
        for pacote in pacotes:
            print(f"   pip install {pacote}")
    
    print("\n🔍 Verificando instalação...")
    
    # Verificar se tudo foi instalado
    todos_ok = True
    for pacote in ["requests", "PyPDF2", "fitz"]:
        try:
            if pacote == "fitz":
                import fitz
            else:
                __import__(pacote)
            print(f"✅ {pacote} funcionando")
        except ImportError:
            print(f"❌ {pacote} não funcionando")
            todos_ok = False
    
    if todos_ok:
        print("\n🎯 Sistema pronto para uso!")
    else:
        print("\n⚠️ Alguns módulos não estão funcionando corretamente")

if __name__ == "__main__":
    main()
