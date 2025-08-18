#!/usr/bin/env python3
"""
🔧 REORGANIZAÇÃO MEGA-ULTRA-MELHORADA DOS DADOS - SOLUÇÃO DEFINITIVA
=====================================================================

Versão que resolve TODOS os problemas de reorganização:
✅ Processa dados da FAPEMIG com SOLUÇÃO DEFINITIVA
✅ Processa dados do CNPq com SOLUÇÃO DEFINITIVA
✅ Inclui TODOS os nomes REAIS dos PDFs
✅ Inclui TODOS os links DIRETOS dos PDFs
✅ Reorganiza dados com estrutura MEGA-ULTRA-MELHORADA
✅ Gera arquivo final com SOLUÇÃO DEFINITIVA COMPLETA
"""

import json
import glob
import os
from datetime import datetime

class ReorganizadorDadosSolucaoDefinitiva:
    def __init__(self):
        self.dados_finais = {
            'fapemig': [],
            'cnpq': [],
            'ufmg': [],
            'timestamp': datetime.now().isoformat(),
            'total_editais': 0,
            'total_pdfs': 0,
            'solucao_definitiva': True
        }
        
    def encontrar_arquivos_solucao_definitiva(self):
        """Encontra arquivos da SOLUÇÃO DEFINITIVA"""
        print("🔍 Procurando arquivos da SOLUÇÃO DEFINITIVA...")
        
        # Buscar arquivos da FAPEMIG
        arquivos_fapemig = glob.glob("fapemig_solucao_definitiva_*.json")
        if arquivos_fapemig:
            arquivo_fapemig = max(arquivos_fapemig, key=lambda x: os.path.getctime(x))
            print(f"✅ FAPEMIG: {arquivo_fapemig}")
        else:
            print("❌ Arquivo da FAPEMIG não encontrado")
            arquivo_fapemig = None
        
        # Buscar arquivos do CNPq
        arquivos_cnpq = glob.glob("cnpq_solucao_definitiva_*.json")
        if arquivos_cnpq:
            arquivo_cnpq = max(arquivos_cnpq, key=lambda x: os.path.getctime(x))
            print(f"✅ CNPq: {arquivo_cnpq}")
        else:
            print("❌ Arquivo do CNPq não encontrado")
            arquivo_cnpq = None
        
        # Buscar arquivos da UFMG (se existirem)
        arquivos_ufmg = glob.glob("*ufmg*.json")
        if arquivos_ufmg:
            arquivo_ufmg = max(arquivos_ufmg, key=lambda x: os.path.getctime(x))
            print(f"✅ UFMG: {arquivo_ufmg}")
        else:
            print("⚠️ Arquivo da UFMG não encontrado")
            arquivo_ufmg = None
        
        return arquivo_fapemig, arquivo_cnpq, arquivo_ufmg
    
    def processar_fapemig_solucao_definitiva(self, arquivo):
        """Processa dados da FAPEMIG com SOLUÇÃO DEFINITIVA"""
        print("\n🔥 Processando FAPEMIG com SOLUÇÃO DEFINITIVA...")
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            editais_processados = 0
            pdfs_encontrados = 0
            
            for edital in dados.get('editais_fapemig', []):
                try:
                    # Extrair informações MEGA-ULTRA-MELHORADAS
                    edital_processado = {
                        'fonte': 'FAPEMIG',
                        'titulo': edital.get('titulo', ''),
                        'numero': edital.get('numero', ''),
                        'data_inclusao': edital.get('data_inclusao', ''),
                        'prazo_final': edital.get('prazo_final', ''),
                        'descricao': edital.get('descricao', ''),
                        'total_pdfs': edital.get('total_pdfs', 0),
                        'pdfs_disponiveis': [],
                        'links_importantes': edital.get('links_importantes', []),
                        'data_coleta': edital.get('data_coleta', ''),
                        'solucao_definitiva': True
                    }
                    
                    # 🔥 PROCESSAMENTO MEGA-ULTRA-MELHORADO DOS PDFs
                    pdfs = edital.get('pdfs_disponiveis', [])
                    for pdf in pdfs:
                        pdf_processado = {
                            'nome': pdf.get('nome', ''),
                            'url': pdf.get('url', ''),
                            'tipo': pdf.get('tipo', ''),
                            'instrucoes': pdf.get('instrucoes', ''),
                            'metodo_extracao': pdf.get('metodo', ''),
                            'solucao_definitiva': True
                        }
                        edital_processado['pdfs_disponiveis'].append(pdf_processado)
                        pdfs_encontrados += 1
                    
                    # Adicionar à lista final
                    self.dados_finais['fapemig'].append(edital_processado)
                    editais_processados += 1
                    
                    print(f"   ✅ Edital processado: {edital_processado['titulo'][:50]}...")
                    print(f"      📄 PDFs encontrados: {len(edital_processado['pdfs_disponiveis'])}")
                    
                except Exception as e:
                    print(f"   ❌ Erro ao processar edital: {e}")
                    continue
            
            print(f"✅ FAPEMIG: {editais_processados} editais processados, {pdfs_encontrados} PDFs encontrados")
            return editais_processados, pdfs_encontrados
            
        except Exception as e:
            print(f"❌ Erro ao processar FAPEMIG: {e}")
            return 0, 0
    
    def processar_cnpq_solucao_definitiva(self, arquivo):
        """Processa dados do CNPq com SOLUÇÃO DEFINITIVA"""
        print("\n🔥 Processando CNPq com SOLUÇÃO DEFINITIVA...")
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            chamadas_processadas = 0
            links_encontrados = 0
            
            for chamada in dados.get('chamadas_cnpq', []):
                try:
                    # Extrair informações MEGA-ULTRA-MELHORADAS
                    chamada_processada = {
                        'fonte': 'CNPq',
                        'titulo': chamada.get('titulo', ''),
                        'numero': chamada.get('numero', ''),
                        'id': chamada.get('id', ''),
                        'descricao': chamada.get('descricao', ''),
                        'periodo_inscricao': chamada.get('periodo_inscricao', ''),
                        'total_links': chamada.get('total_links', 0),
                        'links_importantes': [],
                        'data_coleta': chamada.get('data_coleta', ''),
                        'texto_completo': chamada.get('texto_completo', ''),
                        'solucao_definitiva': True
                    }
                    
                    # 🔥 PROCESSAMENTO MEGA-ULTRA-MELHORADO DOS LINKS
                    links = chamada.get('links_importantes', [])
                    for link in links:
                        link_processado = {
                            'texto': link.get('texto', ''),
                            'url': link.get('url', ''),
                            'tipo': link.get('tipo', ''),
                            'metodo': link.get('metodo', ''),
                            'solucao_definitiva': True
                        }
                        chamada_processada['links_importantes'].append(link_processado)
                        links_encontrados += 1
                    
                    # Adicionar à lista final
                    self.dados_finais['cnpq'].append(chamada_processada)
                    chamadas_processadas += 1
                    
                    print(f"   ✅ Chamada processada: {chamada_processada['titulo'][:50]}...")
                    print(f"      🔗 Links encontrados: {len(chamada_processada['links_importantes'])}")
                    
                except Exception as e:
                    print(f"   ❌ Erro ao processar chamada: {e}")
                    continue
            
            print(f"✅ CNPq: {chamadas_processadas} chamadas processadas, {links_encontrados} links encontrados")
            return chamadas_processadas, links_encontrados
            
        except Exception as e:
            print(f"❌ Erro ao processar CNPq: {e}")
            return 0, 0
    
    def processar_ufmg(self, arquivo):
        """Processa dados da UFMG (se existirem)"""
        if not arquivo:
            print("\n⚠️ UFMG: Nenhum arquivo encontrado para processar")
            return 0, 0
        
        print("\n🏫 Processando UFMG...")
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            editais_processados = 0
            pdfs_encontrados = 0
            
            # Processar editais da UFMG (estrutura pode variar)
            editais = dados.get('editais_ufmg', dados.get('ufmg', []))
            
            for edital in editais:
                try:
                    edital_processado = {
                        'fonte': 'UFMG',
                        'titulo': edital.get('titulo', ''),
                        'numero': edital.get('numero', ''),
                        'data': edital.get('data', ''),
                        'descricao': edital.get('descricao', ''),
                        'link_pdf': edital.get('link_pdf', ''),
                        'link_alternativo': edital.get('link_alternativo', ''),
                        'data_coleta': edital.get('data_coleta', ''),
                        'solucao_definitiva': True
                    }
                    
                    self.dados_finais['ufmg'].append(edital_processado)
                    editais_processados += 1
                    
                    if edital_processado['link_pdf'] or edital_processado['link_alternativo']:
                        pdfs_encontrados += 1
                    
                except Exception as e:
                    print(f"   ❌ Erro ao processar edital UFMG: {e}")
                    continue
            
            print(f"✅ UFMG: {editais_processados} editais processados, {pdfs_encontrados} PDFs encontrados")
            return editais_processados, pdfs_encontrados
            
        except Exception as e:
            print(f"❌ Erro ao processar UFMG: {e}")
            return 0, 0
    
    def calcular_totais_finais(self):
        """Calcula totais finais da SOLUÇÃO DEFINITIVA"""
        print("\n📊 Calculando totais finais...")
        
        total_editais = (
            len(self.dados_finais['fapemig']) +
            len(self.dados_finais['cnpq']) +
            len(self.dados_finais['ufmg'])
        )
        
        total_pdfs = 0
        for edital in self.dados_finais['fapemig']:
            total_pdfs += len(edital.get('pdfs_disponiveis', []))
        
        for chamada in self.dados_finais['cnpq']:
            total_pdfs += len(chamada.get('links_importantes', []))
        
        for edital in self.dados_finais['ufmg']:
            if edital.get('link_pdf') or edital.get('link_alternativo'):
                total_pdfs += 1
        
        self.dados_finais['total_editais'] = total_editais
        self.dados_finais['total_pdfs'] = total_pdfs
        
        print(f"📊 TOTAL FINAL:")
        print(f"   🏫 FAPEMIG: {len(self.dados_finais['fapemig'])} editais")
        print(f"   🔬 CNPq: {len(self.dados_finais['cnpq'])} chamadas")
        print(f"   🎓 UFMG: {len(self.dados_finais['ufmg'])} editais")
        print(f"   📄 TOTAL: {total_editais} oportunidades, {total_pdfs} PDFs/links")
        
        return total_editais, total_pdfs
    
    def salvar_dados_finais(self):
        """Salva dados finais da SOLUÇÃO DEFINITIVA"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"dados_reorganizados_solucao_definitiva_{timestamp}.json"
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.dados_finais, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Dados finais salvos em: {nome_arquivo}")
            return nome_arquivo
            
        except Exception as e:
            print(f"❌ Erro ao salvar dados finais: {e}")
            return None
    
    def executar_reorganizacao_completa(self):
        """Executa reorganização MEGA-ULTRA-MELHORADA completa"""
        print("🚀 INICIANDO REORGANIZAÇÃO MEGA-ULTRA-MELHORADA")
        print("=" * 60)
        print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
        
        # Encontrar arquivos
        arquivo_fapemig, arquivo_cnpq, arquivo_ufmg = self.encontrar_arquivos_solucao_definitiva()
        
        total_editais = 0
        total_pdfs = 0
        
        # Processar FAPEMIG
        if arquivo_fapemig:
            editais_fapemig, pdfs_fapemig = self.processar_fapemig_solucao_definitiva(arquivo_fapemig)
            total_editais += editais_fapemig
            total_pdfs += pdfs_fapemig
        
        # Processar CNPq
        if arquivo_cnpq:
            chamadas_cnpq, links_cnpq = self.processar_cnpq_solucao_definitiva(arquivo_cnpq)
            total_editais += chamadas_cnpq
            total_pdfs += links_cnpq
        
        # Processar UFMG
        if arquivo_ufmg:
            editais_ufmg, pdfs_ufmg = self.processar_ufmg(arquivo_ufmg)
            total_editais += editais_ufmg
            total_pdfs += pdfs_ufmg
        
        # Calcular totais finais
        self.calcular_totais_finais()
        
        # Salvar dados finais
        arquivo_final = self.salvar_dados_finais()
        
        print(f"\n🎉 REORGANIZAÇÃO MEGA-ULTRA-MELHORADA CONCLUÍDA!")
        print(f"📊 Total de oportunidades: {total_editais}")
        print(f"📄 Total de PDFs/links: {total_pdfs}")
        print(f"💾 Arquivo final: {arquivo_final}")
        
        return True

if __name__ == "__main__":
    reorganizador = ReorganizadorDadosSolucaoDefinitiva()
    reorganizador.executar_reorganizacao_completa()
