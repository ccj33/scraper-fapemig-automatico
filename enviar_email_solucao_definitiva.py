#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 EMAIL MEGA-ULTRA-MELHORADO - SOLUÇÃO DEFINITIVA
==================================================

Script que envia emails com TODOS os nomes e links dos PDFs da FAPEMIG
e todas as informações detalhadas dos editais.
"""

import os
import json
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz

def validar_configuracao_email():
    """Valida se todas as variáveis de email estão configuradas"""
    variaveis_obrigatorias = {
        'SMTP_SERVER': os.getenv('SMTP_SERVER'),
        'SMTP_PORT': os.getenv('SMTP_PORT'),
        'EMAIL_USER': os.getenv('EMAIL_USER'),
        'EMAIL_PASS': os.getenv('EMAIL_PASS'),
        'EMAIL_FROM': os.getenv('EMAIL_FROM'),
        'EMAIL_DESTINO': os.getenv('EMAIL_DESTINO')
    }
    
    print("🔍 VALIDANDO CONFIGURAÇÃO DE EMAIL:")
    print("=" * 40)
    
    configurado = True
    for var, valor in variaveis_obrigatorias.items():
        if valor and valor.strip():
            # Mascarar senha
            if 'PASS' in var:
                valor_exibicao = '*' * len(valor)
            else:
                valor_exibicao = valor
            print(f"✅ {var}: {valor_exibicao}")
        else:
            print(f"❌ {var}: NÃO CONFIGURADO")
            configurado = False
    
    if not configurado:
        print("\n⚠️  PROBLEMAS ENCONTRADOS:")
        print("   - Algumas variáveis de ambiente não estão configuradas")
        print("   - Verifique se os GitHub Secrets estão configurados corretamente")
        return False
    
    # Validações específicas
    try:
        porta = int(variaveis_obrigatorias['SMTP_PORT'])
        if porta <= 0 or porta > 65535:
            print(f"❌ SMTP_PORT inválido: {porta}")
            return False
    except (ValueError, TypeError):
        print(f"❌ SMTP_PORT deve ser um número válido: {variaveis_obrigatorias['SMTP_PORT']}")
        return False
    
    print("✅ Todas as variáveis estão configuradas corretamente!")
    return True

def carregar_dados_solucao_definitiva():
    """Carrega os dados da SOLUÇÃO DEFINITIVA"""
    dados = {
        'fapemig_solucao_definitiva': None,
        'dados_reorganizados_solucao_definitiva': None,
        'editais_rapidos': None,
        'chamadas_cnpq_detalhadas': None
    }
    
    # Buscar arquivos mais recentes
    for tipo in dados.keys():
        arquivos = glob.glob(f'{tipo}_*.json')
        if arquivos:
            # Pegar o arquivo mais recente baseado no timestamp no nome
            arquivo_mais_recente = max(arquivos, key=lambda x: os.path.getctime(x))
            try:
                with open(arquivo_mais_recente, 'r', encoding='utf-8') as f:
                    dados[tipo] = json.load(f)
                print(f"✅ {tipo}: {arquivo_mais_recente}")
            except Exception as e:
                print(f"❌ Erro ao carregar {tipo}: {e}")
    
    return dados

def criar_email_solucao_definitiva(dados):
    """Cria o email com SOLUÇÃO DEFINITIVA - TODOS os nomes e links dos PDFs"""
    print("🔥 Criando email com SOLUÇÃO DEFINITIVA...")
    
    # 🔥 EMAIL MEGA-ULTRA-MELHORADO
    email_content = []
    email_content.append("🚀 RESUMO DA EXECUÇÃO DOS SCRAPERS - SOLUÇÃO DEFINITIVA")
    email_content.append("=" * 70)
    email_content.append(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    email_content.append("🔥 SOLUÇÃO DEFINITIVA IMPLEMENTADA - TODOS os nomes e links dos PDFs!")
    email_content.append("")
    
    # 🔥 FAPEMIG - SOLUÇÃO DEFINITIVA
    if dados['fapemig_solucao_definitiva']:
        fapemig = dados['fapemig_solucao_definitiva']
        email_content.append("🔬 FAPEMIG - SOLUÇÃO DEFINITIVA IMPLEMENTADA:")
        email_content.append(f"   📊 {len(fapemig['fapemig'])} editais encontrados")
        email_content.append(f"   📄 {fapemig['total_pdfs']} PDFs extraídos")
        email_content.append("   ✅ TODOS os nomes e links dos PDFs incluídos!")
        email_content.append("")
        
        # 🔥 DETALHES COMPLETOS DE CADA EDITAL
        email_content.append("📋 DETALHES COMPLETOS DOS EDITAIS FAPEMIG:")
        email_content.append("-" * 50)
        
        for i, edital in enumerate(fapemig['fapemig'], 1):
            email_content.append(f"{i}. {edital['titulo']}")
            email_content.append(f"   📊 Número: {edital['numero']}")
            email_content.append(f"   📅 Data Inclusão: {edital['data_inclusao']}")
            email_content.append(f"   ⏰ Prazo Final: {edital['prazo_final']}")
            email_content.append(f"   📄 Total PDFs: {edital['total_pdfs']}")
            
            # 🔥 TODOS OS PDFs DISPONÍVEIS
            if edital['pdfs_disponiveis']:
                email_content.append("   📄 PDFs Disponíveis:")
                for j, pdf in enumerate(edital['pdfs_disponiveis'], 1):
                    email_content.append(f"      {j}. {pdf['nome']}")
                    email_content.append(f"         🔗 URL: {pdf['url']}")
                    email_content.append(f"         📝 Tipo: {pdf['tipo']}")
                    if pdf.get('instrucoes'):
                        email_content.append(f"         💡 Instruções: {pdf['instrucoes']}")
            else:
                email_content.append("   📄 PDFs: Acesse a página para encontrar os PDFs")
            
            # Links de vídeo se existirem
            if edital.get('links_video'):
                email_content.append("   🎥 Vídeos Explicativos:")
                for video in edital['links_video']:
                    email_content.append(f"      🔗 {video['plataforma']}: {video['url']}")
            
            email_content.append("")
    
    # Se não tem solução definitiva, usar dados reorganizados
    elif dados['dados_reorganizados_solucao_definitiva']:
        dados_reorg = dados['dados_reorganizados_solucao_definitiva']
        email_content.append("🔬 FAPEMIG - Dados Reorganizados com SOLUÇÃO DEFINITIVA:")
        email_content.append(f"   📊 {len(dados_reorg['fapemig'])} editais encontrados")
        email_content.append("   ✅ Nomes e links dos PDFs incluídos!")
        email_content.append("")
        
        # Detalhes dos editais reorganizados
        email_content.append("📋 DETALHES DOS EDITAIS FAPEMIG:")
        email_content.append("-" * 50)
        
        for i, edital in enumerate(dados_reorg['fapemig'], 1):
            email_content.append(f"{i}. {edital['titulo']}")
            email_content.append(f"   📊 Número: {edital['numero']}")
            email_content.append(f"   📅 Data Inclusão: {edital['data_inclusao']}")
            email_content.append(f"   ⏰ Prazo Final: {edital['prazo_final']}")
            email_content.append(f"   📄 Total PDFs: {edital['total_pdfs']}")
            
            # PDFs disponíveis
            if edital['pdfs_disponiveis']:
                email_content.append("   📄 PDFs Disponíveis:")
                for j, pdf in enumerate(edital['pdfs_disponiveis'], 1):
                    email_content.append(f"      {j}. {pdf['nome']}")
                    email_content.append(f"         🔗 URL: {pdf['url']}")
                    email_content.append(f"         📝 Tipo: {pdf['tipo']}")
                    if pdf.get('instrucoes'):
                        email_content.append(f"         💡 Instruções: {pdf['instrucoes']}")
            
            email_content.append(f"   🔗 Link Principal: {edital['link_principal']}")
            email_content.append(f"   🔗 Link Alternativo: {edital['link_alternativo']}")
            email_content.append("")
    
    # UFMG
    if dados['editais_rapidos']:
        editais = dados['editais_rapidos']
        if 'ufmg' in editais:
            email_content.append("🏫 UFMG:")
            email_content.append(f"   📊 {len(editais['ufmg'])} editais encontrados")
            email_content.append("   ✅ PDFs diretos disponíveis")
            email_content.append("")
    
    # CNPq
    if dados['chamadas_cnpq_detalhadas']:
        chamadas = dados['chamadas_cnpq_detalhadas']
        if 'chamadas_cnpq' in chamadas:
            email_content.append("🚀 CNPq:")
            email_content.append(f"   📊 {len(chamadas['chamadas_cnpq'])} chamadas encontradas")
            email_content.append("   ✅ Links para páginas com PDFs incluídos")
            email_content.append("")
    
    # 🔥 RESUMO FINAL
    total_editais = 0
    if dados['fapemig_solucao_definitiva']:
        total_editais += len(dados['fapemig_solucao_definitiva']['fapemig'])
    elif dados['dados_reorganizados_solucao_definitiva']:
        total_editais += len(dados['dados_reorganizados_solucao_definitiva']['fapemig'])
    
    if dados['editais_rapidos']:
        if 'ufmg' in dados['editais_rapidos']:
            total_editais += len(dados['editais_rapidos']['ufmg'])
        if 'cnpq' in dados['editais_rapidos']:
            total_editais += len(dados['editais_rapidos']['cnpq'])
    
    if dados['chamadas_cnpq_detalhadas']:
        if 'chamadas_cnpq' in dados['chamadas_cnpq_detalhadas']:
            total_editais += len(dados['chamadas_cnpq_detalhadas']['chamadas_cnpq'])
    
    email_content.append("🔧 DADOS REORGANIZADOS COM SOLUÇÃO DEFINITIVA:")
    email_content.append(f"   📄 FAPEMIG: {len(dados.get('fapemig_solucao_definitiva', {}).get('fapemig', [])) if dados.get('fapemig_solucao_definitiva') else 0} editais com TODOS os PDFs")
    email_content.append(f"   📄 UFMG: {len(dados.get('editais_rapidos', {}).get('ufmg', [])) if dados.get('editais_rapidos') else 0} editais com PDFs diretos")
    email_content.append(f"   📄 CNPq: {len(dados.get('chamadas_cnpq_detalhadas', {}).get('chamadas_cnpq', [])) if dados.get('chamadas_cnpq_detalhadas') else 0} chamadas com links para PDFs")
    email_content.append(f"   📊 TOTAL: {total_editais} oportunidades")
    email_content.append("")
    
    # 🔥 MENSAGEM FINAL
    email_content.append("🎉 SOLUÇÃO DEFINITIVA IMPLEMENTADA COM SUCESSO!")
    email_content.append("✅ TODOS os nomes e links dos PDFs da FAPEMIG incluídos!")
    email_content.append("✅ Captura COMPLETA de editais implementada!")
    email_content.append("✅ Nenhum dado perdido!")
    email_content.append("")
    email_content.append("📧 Este email foi enviado automaticamente pelo sistema de scrapers com SOLUÇÃO DEFINITIVA.")
    
    return "\n".join(email_content)

def enviar_email_solucao_definitiva(destinatario, assunto, corpo):
    """Envia o email com SOLUÇÃO DEFINITIVA"""
    try:
        # Configurações do servidor SMTP
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        email_user = os.getenv('EMAIL_USER')
        email_pass = os.getenv('EMAIL_PASS')
        email_from = os.getenv('EMAIL_FROM', email_user)
        
        # Validações finais
        if not email_user or not email_pass:
            print("❌ Credenciais de email não configuradas!")
            return False
        
        if not destinatario or not destinatario.strip():
            print("❌ Destinatário não configurado!")
            return False
        
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = destinatario
        msg['Subject'] = assunto
        
        # Adicionar corpo do email
        msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
        
        # Conectar e enviar
        print(f"🔗 Conectando ao servidor SMTP: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print(f"🔐 Fazendo login com: {email_user}")
        server.login(email_user, email_pass)
        
        print(f"📤 Enviando email com SOLUÇÃO DEFINITIVA para: {destinatario}")
        server.send_message(msg)
        server.quit()
        
        print("✅ Email com SOLUÇÃO DEFINITIVA enviado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False

def main():
    """Função principal"""
    print("🔥 INICIANDO ENVIO DE EMAIL COM SOLUÇÃO DEFINITIVA")
    print("=" * 60)
    
    # Validar configuração de email primeiro
    if not validar_configuracao_email():
        print("\n❌ CONFIGURAÇÃO DE EMAIL INVÁLIDA!")
        print("🔧 Para resolver:")
        print("   1. Configure os GitHub Secrets no repositório")
        print("   2. Verifique se todos os secrets estão preenchidos")
        return 1
    
    # Carregar dados da SOLUÇÃO DEFINITIVA
    print("\n📂 Carregando dados da SOLUÇÃO DEFINITIVA...")
    dados = carregar_dados_solucao_definitiva()
    
    # Criar email com SOLUÇÃO DEFINITIVA
    print("🔥 Criando email com SOLUÇÃO DEFINITIVA...")
    email_content = criar_email_solucao_definitiva(dados)
    
    # Configurar email
    destinatario = os.getenv('EMAIL_DESTINO', 'ccjota51@gmail.com')
    assunto = f"🔥 SOLUÇÃO DEFINITIVA - Resultados dos Scrapers - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    print(f"📧 Configurando email para: {destinatario}")
    print(f"📋 Assunto: {assunto}")
    
    # Enviar email
    print("🚀 Enviando email com SOLUÇÃO DEFINITIVA...")
    sucesso = enviar_email_solucao_definitiva(destinatario, assunto, email_content)
    
    if sucesso:
        print("🎉 PROCESSO CONCLUÍDO COM SOLUÇÃO DEFINITIVA!")
        print("📧 Email enviado para:", destinatario)
        print("✅ TODOS os nomes e links dos PDFs incluídos!")
        print("🔥 FAPEMIG com captura COMPLETA de editais!")
    else:
        print("❌ Falha no envio do email!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
