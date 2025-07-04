import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import pandas as pd
from utils.io import salvar_dados
from analise.dadosFormatar import formatar_colunas
from coleta.local_Coleta import carregarArquivoLoc
from visualizacao.dadosGraficos import VisualizadorDados

class TestSistemaAxiomaPy:
    def test_salvar_e_carregar_dados(self, tmp_path):
        dados = [{'nome': 'Item 1', 'valor': 10}]
        nome_arquivo = 'test_dados'
        salvar_dados(dados, tmp_path, nome_arquivo)

        caminho = tmp_path / f'{nome_arquivo}.json'
        assert caminho.exists()

        with open(caminho, 'r', encoding='utf-8') as f:
            dados_carregados = json.load(f)

        assert dados_carregados == dados

    def test_formatar_colunas(self):
        df = pd.DataFrame({' Nome ': ['A', 'B'], 'Idade ': [20, 30]})
    
        df_formatado = formatar_colunas(df, ['Nome', 'Idade'])
        assert df_formatado is not None, "A formatação das colunas falhou e retornou None"
        assert 'Nome' in df_formatado.columns
        assert 'Idade' in df_formatado.columns


    def test_coleta_local_e_formata(self, tmp_path):
        dados = [{'Nome': 'Produto 1', 'Preço': 50}]
        arquivo_teste = tmp_path / 'arquivo.json'
        with open(arquivo_teste, 'w', encoding='utf-8') as f:
            json.dump(dados, f)

        df = carregarArquivoLoc(str(arquivo_teste))
        assert not df.empty
        
        df_formatado = formatar_colunas(df, ['Nome', 'Preço'])
        assert 'Nome' in df_formatado.columns
        assert 'Preço' in df_formatado.columns

    def test_fluxo_completo_local(self, tmp_path):
        dados = [{' Nome ': 'Item 1', ' Valor ': 100}, {' Nome ': 'Item 2', ' Valor ': 200}]
        df = pd.DataFrame(dados)

        df_formatado = formatar_colunas(df, ['Nome', 'Valor'])
        assert df_formatado is not None, "A formatação das colunas falhou e retornou None"
        assert 'Nome' in df_formatado.columns
        assert 'Valor' in df_formatado.columns

        nome_arquivo = 'fluxo_completo'
        salvar_dados(df_formatado.to_dict(orient='records'), tmp_path, nome_arquivo)
        assert (tmp_path / f'{nome_arquivo}.json').exists()

        caminho = tmp_path / f'{nome_arquivo}.json'
        df_recarregado = carregarArquivoLoc(str(caminho))
        assert df_recarregado is not None, "O carregamento local falhou e retornou None"
        assert not df_recarregado.empty
        assert 'Nome' in df_recarregado.columns
        assert df_recarregado.iloc[0]['Nome'] == 'Item 1'

    def test_visualizacao_estatisticas(self):
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [10, 20, 30, 40, 50]})
        VisualizadorDados.estatisticas_descritivas(df) 

    def test_visualizacao_graficos(self):
        df = pd.DataFrame({'Categoria': ['A', 'B', 'A', 'C', 'B'], 'Valor': [10, 20, 15, 25, 30]})

        VisualizadorDados.plot_histograma(df, 'Valor')
        VisualizadorDados.plot_barras(df, 'Categoria')
        VisualizadorDados.plot_scatter(df, 'Valor', 'Valor')
        VisualizadorDados.plot_pizza(df, 'Categoria')
        VisualizadorDados.plot_linha(df, 'Valor', 'Valor')
        VisualizadorDados.plot_boxplot(df, 'Valor')
