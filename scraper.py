import smtplib
from email.mime.text import MIMEText
import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

def send_email(msg_text):
    """Envia email com as atualizações encontradas"""
    try:
        msg = MIMEText(msg_text, 'plain', 'utf-8')
        msg['Subject'] = '🚀 Atualização FAPEMIG - Novas Oportunidades Encontradas!'
        msg['From'] = os.environ['EMAIL_USER']
        msg['To'] = os.environ['EMAIL_USER']

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
            server.send_message(msg)
        print("✅ Email enviado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False

def extrair_chamadas_fapemig():
    """Extrai chamadas da FAPEMIG usando Selenium headless"""
    print("🚀 Iniciando extração FAPEMIG...")
    
    # Instala e configura o ChromeDriver
    chromedriver_autoinstaller.install()
    
    # Configurações para modo headless (GitHub Actions)
    options = Options()
    options.add_argument("--headless")          # Roda sem interface
    options.add_argument("--no-sandbox")        # Necessário para Linux
    options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória
    options.add_argument("--disable-gpu")       # Desabilita GPU
    options.add_argument("--window-size=1920,1080")  # Tamanho da janela virtual
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Navegador iniciado em modo headless")
        
        # URL da FAPEMIG
        url_fapemig = "https://fapemig.br/chamadas/"
        print(f"🌐 Acessando: {url_fapemig}")
        
        driver.get(url_fapemig)
        time.sleep(5)  # Aguarda carregamento
        
        # Verifica se a página carregou
        if "FAPEMIG" not in driver.title:
            print("⚠️ Página pode não ter carregado completamente")
        
        # Procura por elementos de chamadas/editais
        chamadas_encontradas = []
        
        # Estratégia 1: Procurar por links que contenham "chamada" ou "edital"
        try:
            links_chamadas = driver.find_elements(By.XPATH, "//a[contains(translate(text(), 'CHAMADA', 'chamada'), 'chamada') or contains(translate(text(), 'EDITAL', 'edital'), 'edital')]")
            
            for link in links_chamadas[:10]:  # Limita a 10 para não sobrecarregar
                try:
                    texto = link.text.strip()
                    href = link.get_attribute("href")
                    if texto and href and len(texto) > 5:
                        chamadas_encontradas.append({
                            'titulo': texto,
                            'url': href,
                            'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Erro ao buscar links específicos: {e}")
        
        # Estratégia 2: Procurar por elementos com classes comuns
        if not chamadas_encontradas:
            try:
                elementos_gerais = driver.find_elements(By.CSS_SELECTOR, "a, .card, .item, .chamada, .edital")
                
                for elem in elementos_gerais[:20]:
                    try:
                        texto = elem.text.strip()
                        href = elem.get_attribute("href")
                        if texto and href and len(texto) > 10 and any(palavra in texto.lower() for palavra in ['chamada', 'edital', 'oportunidade', 'financiamento']):
                            chamadas_encontradas.append({
                                'titulo': texto,
                                'url': href,
                                'data_extracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                    except:
                        continue
            except Exception as e:
                print(f"⚠️ Erro ao buscar elementos gerais: {e}")
        
        # Estratégia 3: Extrair texto da página para análise
        try:
            corpo = driver.find_element(By.TAG_NAME, "body")
            texto_pagina = corpo.text
            
            # Salva o texto da página para análise posterior
            with open("pagina_fapemig.txt", "w", encoding="utf-8") as f:
                f.write(texto_pagina)
            print("📄 Texto da página salvo para análise")
            
        except Exception as e:
            print(f"⚠️ Erro ao extrair texto da página: {e}")
        
        driver.quit()
        print("✅ Navegador fechado")
        
        return chamadas_encontradas
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        return []

def main():
    """Função principal que executa o scraping e envia email"""
    print("=" * 60)
    print("🚀 SCRAPER FAPEMIG - GITHUB ACTIONS")
    print("=" * 60)
    
    # Executa o scraping
    chamadas = extrair_chamadas_fapemig()
    
    if not chamadas:
        print("❌ Nenhuma chamada encontrada")
        return
    
    print(f"\n✅ Encontradas {len(chamadas)} chamadas/oportunidades:")
    
    # Prepara o conteúdo do email
    email_content = f"""
🚀 ATUALIZAÇÃO FAPEMIG - {datetime.now().strftime('%d/%m/%Y %H:%M')}

Encontradas {len(chamadas)} novas oportunidades:

"""
    
    for i, chamada in enumerate(chamadas, 1):
        print(f"{i}. {chamada['titulo']}")
        print(f"   URL: {chamada['url']}")
        
        email_content += f"""
{i}. {chamada['titulo']}
   URL: {chamada['url']}
   Data de extração: {chamada['data_extracao']}
"""
    
    email_content += f"""

---
🤖 Scraper automatizado executado via GitHub Actions
📅 Executado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
🌐 Fonte: https://fapemig.br/chamadas/
"""
    
    # Salva os dados em arquivo local (para debug)
    try:
        with open("chamadas_encontradas.json", "w", encoding="utf-8") as f:
            json.dump(chamadas, f, ensure_ascii=False, indent=2)
        print("💾 Dados salvos em chamadas_encontradas.json")
    except Exception as e:
        print(f"⚠️ Erro ao salvar arquivo: {e}")
    
    # Envia email se as variáveis de ambiente estiverem configuradas
    if 'EMAIL_USER' in os.environ and 'EMAIL_PASS' in os.environ:
        print("\n📧 Enviando email...")
        if send_email(email_content):
            print("✅ Processo concluído com sucesso!")
        else:
            print("⚠️ Scraping concluído, mas email não foi enviado")
    else:
        print("\n⚠️ Variáveis de email não configuradas")
        print("📧 Conteúdo que seria enviado:")
        print("-" * 40)
        print(email_content)
        print("-" * 40)

if __name__ == "__main__":
    main()
