#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Script de diagnóstico para problemas de email
Use este script para identificar exatamente o que está faltando
"""

import os
import sys
import glob

def verificar_variaveis_ambiente():
    """Verifica todas as variáveis de ambiente relacionadas ao email"""
    print("🔍 DIAGNÓSTICO COMPLETO DE EMAIL")
    print("=" * 50)
    
    # Lista de variáveis obrigatórias
    variaveis = {
        'SMTP_SERVER': {
            'descricao': 'Servidor SMTP',
            'valor_padrao': 'smtp.gmail.com',
            'obrigatorio': True
        },
        'SMTP_PORT': {
            'descricao': 'Porta SMTP',
            'valor_padrao': '587',
            'obrigatorio': True
        },
        'EMAIL_USER': {
            'descricao': 'Usuário do Gmail',
            'valor_padrao': 'ccjota51@gmail.com',
            'obrigatorio': True
        },
        'EMAIL_PASS': {
            'descricao': 'Senha de aplicativo Gmail',
            'valor_padrao': '[16 CARACTERES]',
            'obrigatorio': True
        },
        'EMAIL_FROM': {
            'descricao': 'Email remetente',
            'valor_padrao': 'ccjota51@gmail.com',
            'obrigatorio': True
        },
        'EMAIL_DESTINO': {
            'descricao': 'Email destinatário',
            'valor_padrao': 'ccjota51@gmail.com',
            'obrigatorio': True
        }
    }
    
    print("📋 VERIFICAÇÃO DAS VARIÁVEIS:")
    print("-" * 40)
    
    problemas = []
    configurado = True
    
    for var, info in variaveis.items():
        valor = os.getenv(var)
        
        if valor and valor.strip():
            # Mascarar senha
            if 'PASS' in var:
                valor_exibicao = '*' * len(valor)
            else:
                valor_exibicao = valor
            
            print(f"✅ {var}: {valor_exibicao}")
            print(f"   📝 {info['descricao']}")
            
            # Validações específicas
            if var == 'SMTP_PORT':
                try:
                    porta = int(valor)
                    if porta <= 0 or porta > 65535:
                        problemas.append(f"❌ {var}: Porta inválida ({porta})")
                        configurado = False
                except ValueError:
                    problemas.append(f"❌ {var}: Deve ser um número válido")
                    configurado = False
            
        else:
            print(f"❌ {var}: NÃO CONFIGURADO")
            print(f"   📝 {info['descricao']}")
            print(f"   💡 Valor padrão: {info['valor_padrao']}")
            configurado = False
    
    print("\n" + "=" * 50)
    
    if configurado:
        print("🎉 STATUS: Todas as variáveis estão configuradas!")
        print("✅ O script de email deve funcionar corretamente")
    else:
        print("❌ STATUS: Problemas encontrados na configuração!")
        print("\n🔧 SOLUÇÕES:")
        print("1. Configure os GitHub Secrets no repositório:")
        print("   Settings → Secrets and variables → Actions")
        print("2. Adicione cada variável como 'New repository secret'")
        print("3. Use os valores padrão sugeridos acima")
        print("4. Para EMAIL_PASS, gere uma senha de aplicativo Gmail")
    
    if problemas:
        print("\n⚠️  PROBLEMAS ESPECÍFICOS:")
        for problema in problemas:
            print(f"   {problema}")
    
    return configurado

def verificar_github_actions():
    """Verifica se estamos rodando no GitHub Actions"""
    print("\n🌐 VERIFICAÇÃO DO AMBIENTE:")
    print("-" * 40)
    
    github_actions = os.getenv('GITHUB_ACTIONS')
    if github_actions:
        print("✅ Executando no GitHub Actions")
        print(f"   Workflow: {os.getenv('GITHUB_WORKFLOW', 'N/A')}")
        print(f"   Job: {os.getenv('GITHUB_JOB', 'N/A')}")
        print(f"   Runner: {os.getenv('RUNNER_OS', 'N/A')}")
    else:
        print("🖥️  Executando localmente")
    
    print(f"   Python: {sys.version}")
    print(f"   Diretório: {os.getcwd()}")

def verificar_arquivos_json():
    """Verifica se existem arquivos JSON para enviar no email"""
    print("\n📁 VERIFICAÇÃO DOS ARQUIVOS DE DADOS:")
    print("-" * 40)
    
    padroes = [
        'editais_rapidos_*.json',
        'chamadas_cnpq_detalhadas_*.json',
        'chamadas_cnpq_inteligentes_*.json',
        'dados_reorganizados_com_pdfs_*.json'
    ]
    
    for padrao in padroes:
        arquivos = glob.glob(padrao)
        if arquivos:
            arquivo_mais_recente = max(arquivos, key=lambda x: os.path.getctime(x))
            tamanho = os.path.getsize(arquivo_mais_recente)
            print(f"✅ {padrao}: {arquivo_mais_recente} ({tamanho} bytes)")
        else:
            print(f"❌ {padrao}: Nenhum arquivo encontrado")

def main():
    """Função principal"""
    print("🔍 DIAGNÓSTICO DE EMAIL - SCRAPERS")
    print("=" * 60)
    
    # Verificar ambiente
    verificar_github_actions()
    
    # Verificar variáveis
    email_configurado = verificar_variaveis_ambiente()
    
    # Verificar arquivos
    verificar_arquivos_json()
    
    print("\n" + "=" * 60)
    
    if email_configurado:
        print("🎯 PRÓXIMOS PASSOS:")
        print("1. Execute o workflow no GitHub Actions")
        print("2. Verifique se o email foi enviado")
        print("3. Se houver erro, verifique os logs detalhados")
    else:
        print("🚨 AÇÃO NECESSÁRIA:")
        print("1. Configure TODOS os GitHub Secrets listados acima")
        print("2. Execute novamente este diagnóstico")
        print("3. Só então execute o workflow principal")
    
    print("\n📚 Para mais ajuda, consulte: README_EMAIL.md")
    
    return 0 if email_configurado else 1

if __name__ == "__main__":
    exit(main())
