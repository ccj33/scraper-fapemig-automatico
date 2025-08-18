#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 Script SIMPLIFICADO para enviar emails com resultados dos scrapers
Usa apenas EMAIL_USER e EMAIL_PASS - Muito mais simples!
"""

import os
import json
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def carregar_dados_recentes():
    """Carrega os dados mais recentes dos scrapers"""
    dados = {
        'editais_rapidos': None,
        'chamadas_cnpq_detalhadas': None,
        'chamadas_cnpq_inteligentes': None,
        'dados_reorganizados': None
    }
    
    # Buscar arquivos mais recentes
    for tipo in dados.keys():
        arquivos = glob.glob(f'{tipo}_*.json')
        if arquivos:
            arquivo_mais_recente = max(arquivos, key=lambda x: os.path.getctime(x))
            try:
                with open(arquivo_mais_recente, 'r', encoding='utf-8') as f:
                    dados[tipo] = json.load(f)
                print(f"✅ {tipo}: {arquivo_mais_recente}")
            except Exception as e:
                print(f"❌ Erro ao carregar {tipo}: {e}")
    
    return dados

def criar_resumo_email(dados):
    """Cria o resumo para o email"""
    resumo = []
    resumo.append("🚀 RESUMO DA EXECUÇÃO DOS SCRAPERS")
    resumo.append("=" * 50)
    resumo.append(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    resumo.append("")
    
    # Resumo dos editais rápidos
    if dados['editais_rapidos']:
        editais = dados['editais_rapidos']
        resumo.append("📋 SCRAPER RÁPIDO:")
        if 'ufmg' in editais:
            resumo.append(f"   🏫 UFMG: {len(editais['ufmg'])} editais encontrados")
        if 'fapemig' in editais:
            resumo.append(f"   🔬 FAPEMIG: {len(editais['fapemig'])} oportunidades encontradas")
        if 'cnpq' in editais:
            resumo.append(f"   🎯 CNPq: {len(editais['cnpq'])} chamadas encontradas")
        resumo.append("")
    
    # Resumo das chamadas detalhadas CNPq
    if dados['chamadas_cnpq_detalhadas']:
        chamadas = dados['chamadas_cnpq_detalhadas']
        if 'chamadas_cnpq' in chamadas:
            resumo.append("🔍 SCRAPER DETALHADO CNPq:")
            resumo.append(f"   📊 {len(chamadas['chamadas_cnpq'])} chamadas detalhadas processadas")
            resumo.append("")
    
    # Resumo das chamadas inteligentes CNPq
    if dados['chamadas_cnpq_inteligentes']:
        chamadas = dados['chamadas_cnpq_inteligentes']
        if 'chamadas_cnpq' in chamadas:
            resumo.append("🧠 SCRAPER INTELIGENTE CNPq:")
            resumo.append(f"   🎯 {len(chamadas['chamadas_cnpq'])} chamadas extraídas inteligentemente")
            resumo.append("")
    
    # Resumo dos dados reorganizados
    if dados['dados_reorganizados']:
        dados_reorg = dados['dados_reorganizados']
        resumo.append("🔧 DADOS REORGANIZADOS:")
        total = 0
        for fonte, itens in dados_reorg.items():
            if isinstance(itens, list) and fonte != 'timestamp' and fonte != 'status':
                resumo.append(f"   📄 {fonte.upper()}: {len(itens)} itens com PDFs")
                total += len(itens)
        resumo.append(f"   📊 TOTAL: {total} oportunidades")
        resumo.append("")
    
    resumo.append("🎉 Execução concluída com sucesso!")
    resumo.append("📧 Este email foi enviado automaticamente pelo sistema de scrapers.")
    
    return "\n".join(resumo)

def enviar_email_simples(email_user, email_pass, destinatario, assunto, corpo):
    """Envia email usando apenas usuário e senha - MUITO SIMPLES!"""
    try:
        print(f"🔗 Conectando ao Gmail...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print(f"🔐 Fazendo login com: {email_user}")
        server.login(email_user, email_pass)
        
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = destinatario
        msg['Subject'] = assunto
        
        # Adicionar corpo do email
        msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
        
        print(f"📤 Enviando email para: {destinatario}")
        server.send_message(msg)
        server.quit()
        
        print("✅ Email enviado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False

def main():
    """Função principal - SUPER SIMPLES!"""
    print("📧 ENVIO SIMPLIFICADO DE EMAIL")
    print("=" * 40)
    
    # Apenas 2 variáveis necessárias!
    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASS')
    
    if not email_user or not email_pass:
        print("❌ Configure apenas 2 variáveis:")
        print("   EMAIL_USER: seu_email@gmail.com")
        print("   EMAIL_PASS: sua_senha_de_app")
        return 1
    
    print(f"✅ Usuário: {email_user}")
    print(f"✅ Senha: {'*' * len(email_pass)}")
    
    # Carregar dados dos scrapers
    print("\n📂 Carregando dados dos scrapers...")
    dados = carregar_dados_recentes()
    
    # Criar resumo para o email
    print("📝 Criando resumo do email...")
    resumo = criar_resumo_email(dados)
    
    # Configurar email (destinatário = usuário)
    destinatario = email_user  # Envia para o próprio usuário
    assunto = f"🚀 Resultados dos Scrapers - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    print(f"📧 Enviando para: {destinatario}")
    print(f"📋 Assunto: {assunto}")
    
    # Enviar email
    print("🚀 Enviando email...")
    sucesso = enviar_email_simples(email_user, email_pass, destinatario, assunto, resumo)
    
    if sucesso:
        print("🎉 Processo concluído com sucesso!")
        print("📧 Email enviado para:", destinatario)
    else:
        print("❌ Falha no envio do email!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
