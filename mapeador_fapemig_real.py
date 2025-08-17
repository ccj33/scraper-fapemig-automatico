#!/usr/bin/env python3
"""
Mapeador Inteligente para FAPEMIG
=================================

Usa os dados REAIS da FAPEMIG que você forneceu para criar
um relatório completo com TODOS os PDFs e informações.
"""

import json
from datetime import datetime

class MapeadorFAPEMIGReal:
    def __init__(self):
        self.resultados = {
            'fapemig': [],
            'timestamp': datetime.now().isoformat(),
            'status': 'Dados reais mapeados da FAPEMIG'
        }
        
    def mapear_dados_reais_fapemig(self):
        """Mapeia os dados REAIS da FAPEMIG que você forneceu"""
        print("🔍 Mapeando dados REAIS da FAPEMIG...")
        
        # Dados reais da FAPEMIG que você me forneceu
        dados_reais = [
            {
                'titulo': 'CHAMADA FAPEMIG 011/2025 - DEEP TECH - INSERÇÃO NO MERCADO E TRAÇÃO COMERCIAL',
                'numero': '011/2025',
                'data_inclusao': '04/07/2025',
                'prazo_final': '02/09/2025',
                'descricao': 'DEEP TECH - INSERÇÃO NO MERCADO E TRAÇÃO COMERCIAL',
                'pdfs_disponiveis': [
                    {
                        'nome': 'CHAMADA FAPEMIG 11/2025 DEEP TECH - INSERÇÃO NO MERCADO E TRAÇÃO COMERCIAL',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Chamada Principal',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'ANEXO II – PERMISSÕES E AUTORIZAÇÕES ESPECIAIS DE CARÁTER ÉTICO OU LEGAL',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo II',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'ANEXO III – TERMO DE DESIGNAÇÃO DE FISCAL REFERENTE À EXECUTORA',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo III',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'ANEXO IV – PLANO DE TRABALHO DE BOLSISTA BDCTI',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo IV',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'GUIA RÁPIDO - PONTOS IMPORTANTES DA CHAMADA',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Guia Rápido',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'SLIDES APRESENTAÇÃO DEEP TECH',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Slides',
                        'instrucoes': 'Acesse a página para download direto'
                    }
                ],
                'links_video': [
                    {
                        'plataforma': 'YouTube',
                        'url': 'https://youtube.com/playlist',
                        'tipo': 'Playlist oficial – Conexão FAPEMIG',
                        'descricao': 'Vídeos explicativos'
                    }
                ],
                'live_tira_duvidas': '08/08/2025 às 15:00 no Canal da Fapemig no Youtube',
                'link_live': 'https://www.youtube.com/@FapemigOficial',
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat(),
                'tem_anexos': True,
                'total_pdfs': 6
            },
            {
                'titulo': 'CHAMADA 016/2024 - PARTICIPAÇÃO COLETIVA EM EVENTOS TÉCNICOS NO PAÍS - 3ª ENTRADA',
                'numero': '016/2024',
                'data_inclusao': '02/06/2025',
                'prazo_final': '30/09/2025',
                'descricao': 'PARTICIPAÇÃO COLETIVA EM EVENTOS TÉCNICOS NO PAÍS - 3ª ENTRADA',
                'pdfs_disponiveis': [
                    {
                        'nome': 'Chamada 16/2024 - Participação Coletiva em Evento - 3ª entrada',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Chamada Principal',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Anexo I - Termo de Anuência para atuação sem Fundação de Apoio',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo I',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Anexo II - Termo de Outorga com Fundação de Apoio',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo II',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Anexo III - Termo de Outorga sem fundação de apoio',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo III',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Anexo IV - Termo de Indicação - Responsável pela Gestão e Fiscalização',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo IV',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Anexo V - Check List',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo V',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Chamada Retificada 016/2024',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Chamada Retificada',
                        'instrucoes': 'Acesse a página para download direto'
                    }
                ],
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat(),
                'tem_anexos': True,
                'total_pdfs': 7
            },
            {
                'titulo': 'CHAMADA 005/2025 - ORGANIZAÇÃO DE EVENTOS DE CARÁTER TÉCNICO CIENTÍFICO - 2ª ENTRADA',
                'numero': '005/2025',
                'data_inclusao': '05/05/2025',
                'prazo_final': 'Não informado',
                'descricao': 'ORGANIZAÇÃO DE EVENTOS DE CARÁTER TÉCNICO CIENTÍFICO - 2ª ENTRADA',
                'pdfs_disponiveis': [
                    {
                        'nome': 'Chamada 005/2025 - Organização de Eventos de Caráter Técnico Científico',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Chamada Principal',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Anexo I - Termo de Outorga com Fundação de Apoio',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo I',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Anexo II - Termo de Outorga sem Fundação de Apoio',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo II',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Anexo III - Termo de Indicação - Responsável pela Gestão e Fiscalização',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo III',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Anexo IV - Check List',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo IV',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'Guia Rápido - Chamada 005/2025 Organização de Eventos de Caráter Técnico Científico',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Guia Rápido',
                        'instrucoes': 'Acesse a página para download direto'
                    }
                ],
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat(),
                'tem_anexos': True,
                'total_pdfs': 6
            },
            {
                'titulo': 'PORTARIA FAPEMIG 021/2024 - CADASTRAMENTO DAS FUNDAÇÕES DE APOIO - FA',
                'numero': '021/2024',
                'data_inclusao': '05/07/2024',
                'prazo_final': 'FLUXO CONTÍNUO',
                'descricao': 'DISPÕE SOBRE O CADASTRAMENTO DAS FUNDAÇÕES DE APOIO NO ÂMBITO DA FUNDAÇÃO DE AMPARO À PESQUISA DO ESTADO DE MINAS GERAIS - FAPEMIG.',
                'pdfs_disponiveis': [
                    {
                        'nome': 'PORTARIA FAPEMIG n. 21-2024',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Portaria Principal',
                        'instrucoes': 'Acesse a página para download direto'
                    }
                ],
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat(),
                'tem_anexos': True,
                'total_pdfs': 1
            },
            {
                'titulo': 'PORTARIA FAPEMIG 020/2024 - CADASTRAMENTO DE INSTITUIÇÕES',
                'numero': '020/2024',
                'data_inclusao': '05/07/2024',
                'prazo_final': 'FLUXO CONTÍNUO',
                'descricao': 'DISPÕE SOBRE O CADASTRAMENTO DE INSTITUIÇÕES COM SEDE OU FILIAL LOCALIZADAS NO ESTADO DE MINAS GERAIS, QUE PRETENDAM CELEBRAR INSTRUMENTOS JURÍDICOS PARA O DESENVOLVIMENTO DE PROGRAMAS E PROJETOS APOIADOS PELA FUNDAÇÃO DE AMPARO À PESQUISA DO ESTADO DE MINAS GERAIS - FAPEMIG.',
                'pdfs_disponiveis': [
                    {
                        'nome': 'PORTARIA FAPEMIG n. 20-2024',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Portaria Principal',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'ANEXO ÚNICO',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo Único',
                        'instrucoes': 'Acesse a página para download direto'
                    }
                ],
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat(),
                'tem_anexos': True,
                'total_pdfs': 2
            },
            {
                'titulo': 'CREDENCIAMENTO AO PROGRAMA INSTITUCIONAL DE INICIAÇÃO CIENTÍFICA E TECNOLÓGICA JUNIOR - BICJR - PORTARIA PRE Nº 051/2023',
                'numero': '051/2023',
                'data_inclusao': '21/11/2023',
                'prazo_final': 'FLUXO CONTÍNUO',
                'descricao': 'DISPÕE SOBRE O CREDENCIAMENTO AO PROGRAMA INSTITUCIONAL DE INICIAÇÃO CIENTÍFICA E TECNOLÓGICA JUNIOR – BICJR – DA FUNDAÇÃO DE AMPARO À PESQUISA DO ESTADO DE MINAS GERAIS – FAPEMIG.',
                'pdfs_disponiveis': [
                    {
                        'nome': 'PORTARIA PRE N° 051-2023 - CREDENCIAMENTO AO BICJR',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Portaria Principal',
                        'instrucoes': 'Acesse a página para download direto'
                    }
                ],
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat(),
                'tem_anexos': True,
                'total_pdfs': 1
            },
            {
                'titulo': 'CREDENCIAMENTO AO PROGRAMA INSTITUCIONAL DE INICIAÇÃO CIENTÍFICA E TECNOLÓGICA - PIBIC - PORTARIA PRE Nº 046/2023',
                'numero': '046/2023',
                'data_inclusao': '13/11/2023',
                'prazo_final': 'FLUXO CONTÍNUO',
                'descricao': 'DISPÕE SOBRE O CREDENCIAMENTO AO PROGRAMA INSTITUCIONAL DE INICIAÇÃO CIENTÍFICA E TECNOLÓGICA – PIBIC – DA FUNDAÇÃO DE AMPARO À PESQUISA DO ESTADO DE MINAS GERAIS – FAPEMIG.',
                'pdfs_disponiveis': [
                    {
                        'nome': 'PORTARIA PRE N° 046-2023 - CREDENCIAMENTO AO PIBIC',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Portaria Principal',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'ANEXO I - DECLARAÇÃO ICTMG',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo I',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'ANEXO II - DECLARAÇÃO IES',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo II',
                        'instrucoes': 'Acesse a página para download direto'
                    }
                ],
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat(),
                'tem_anexos': True,
                'total_pdfs': 3
            },
            {
                'titulo': 'CREDENCIAMENTO AO PROGRAMA DE CAPACITAÇÃO DE RECURSOS HUMANOS - PCRH - PORTARIA PRE Nº 010/2023',
                'numero': '010/2023',
                'data_inclusao': '23/03/2023',
                'prazo_final': 'FLUXO CONTÍNUO',
                'descricao': 'DISPÕE SOBRE O CREDENCIAMENTO AO PROGRAMA DE CAPACITAÇÃO DE RECURSOS HUMANOS - PCRH DA FUNDAÇÃO DE AMPARO À PESQUISA DO ESTADO DE MINAS GERAIS - FAPEMIG.',
                'pdfs_disponiveis': [
                    {
                        'nome': 'PORTARIA PRE N° 010/2023 - CREDENCIAMENTO AO PCRH',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Portaria Principal',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'ANEXO I - QUADRO DE PESSOAL',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo I',
                        'instrucoes': 'Acesse a página para download direto'
                    },
                    {
                        'nome': 'ANEXO II - DECLARAÇÃO DE ICTMG',
                        'url': 'http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/',
                        'tipo': 'Anexo II',
                        'instrucoes': 'Acesse a página para download direto'
                    }
                ],
                'fonte': 'FAPEMIG',
                'data_coleta': datetime.now().isoformat(),
                'tem_anexos': True,
                'total_pdfs': 3
            }
        ]
        
        # Adicionar dados ao resultado
        self.resultados['fapemig'] = dados_reais
        
        print(f"✅ {len(dados_reais)} chamadas da FAPEMIG mapeadas com dados REAIS!")
        
        return dados_reais
    
    def mostrar_relatorio_completo(self):
        """Mostra relatório completo com todos os dados mapeados"""
        print("\n" + "="*100)
        print("📋 RELATÓRIO COMPLETO - FAPEMIG COM DADOS REAIS E TODOS OS PDFs")
        print("="*100)
        
        total_pdfs = 0
        
        for i, chamada in enumerate(self.resultados['fapemig'], 1):
            print(f"\n🔬 {i}. {chamada['titulo']}")
            print("-" * 80)
            print(f"   📊 Número: {chamada['numero']}")
            print(f"   📅 Data Inclusão: {chamada['data_inclusao']}")
            print(f"   ⏰ Prazo Final: {chamada['prazo_final']}")
            print(f"   📝 Descrição: {chamada['descricao'][:100]}...")
            print(f"   📄 Total de PDFs: {chamada['total_pdfs']}")
            
            # Mostrar PDFs disponíveis
            if chamada['pdfs_disponiveis']:
                print(f"   📚 PDFs Disponíveis:")
                for j, pdf in enumerate(chamada['pdfs_disponiveis'], 1):
                    print(f"      {j}. {pdf['nome']}")
                    print(f"         🔗 Tipo: {pdf['tipo']}")
                    print(f"         📥 URL: {pdf['url']}")
                    print(f"         💡 Instruções: {pdf['instrucoes']}")
            
            # Mostrar links de vídeo se houver
            if chamada.get('links_video'):
                print(f"   🎥 Vídeos Explicativos:")
                for video in chamada['links_video']:
                    print(f"      📺 {video['tipo']}: {video['url']}")
            
            # Mostrar live se houver
            if chamada.get('live_tira_duvidas'):
                print(f"   🎤 Live Tira Dúvidas: {chamada['live_tira_duvidas']}")
                if chamada.get('link_live'):
                    print(f"      🔗 Canal: {chamada['link_live']}")
            
            total_pdfs += chamada['total_pdfs']
        
        print(f"\n" + "="*100)
        print(f"📊 RESUMO FINAL:")
        print(f"   🔬 Total de Chamadas: {len(self.resultados['fapemig'])}")
        print(f"   📄 Total de PDFs Disponíveis: {total_pdfs}")
        print(f"   🎥 Chamadas com Vídeos: {len([c for c in self.resultados['fapemig'] if c.get('links_video')])}")
        print(f"   🎤 Chamadas com Live: {len([c for c in self.resultados['fapemig'] if c.get('live_tira_duvidas')])}")
        print(f"   ⏰ Chamadas com Prazo: {len([c for c in self.resultados['fapemig'] if c['prazo_final'] != 'FLUXO CONTÍNUO' and c['prazo_final'] != 'Não informado'])}")
        print("="*100)
    
    def salvar_resultados(self):
        """Salva os resultados mapeados da FAPEMIG"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"fapemig_dados_reais_{timestamp}.json"
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Resultados mapeados da FAPEMIG salvos em: {nome_arquivo}")
            return nome_arquivo
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return None
    
    def executar_mapeamento(self):
        """Executa o mapeamento completo da FAPEMIG"""
        print("🚀 INICIANDO MAPEAMENTO COMPLETO DA FAPEMIG")
        print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            # Mapear dados reais da FAPEMIG
            self.mapear_dados_reais_fapemig()
            
            # Mostrar relatório completo
            self.mostrar_relatorio_completo()
            
            # Salvar resultados
            arquivo = self.salvar_resultados()
            
            print(f"\n🎉 MAPEAMENTO COMPLETO DA FAPEMIG CONCLUÍDO!")
            print(f"📊 Total de chamadas: {len(self.resultados['fapemig'])}")
            print(f"💾 Arquivo salvo: {arquivo}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no mapeamento: {e}")
            return False

if __name__ == "__main__":
    mapeador = MapeadorFAPEMIGReal()
    mapeador.executar_mapeamento()
