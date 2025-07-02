"""
from coleta.api_Coleta import APIDados
from analise.dadosFormatar import formatar_colunas
from utils.filtros import filtrar_dados

class LivrosAPI(APIDados):
    def __init__(self, api_url, query=None, limit=None, isbn=None):
        self.isbn = isbn
        params = {}

        if isbn:
            params['bibkeys'] = f"ISBN:{isbn}"
            params['format'] = 'json'
            params['jscmd'] = 'data'
        else:
            if query:
                params['title'] = query
            if limit:
                params['limit'] = limit

        super().__init__(api_url, params)

    def tratar_resposta(self):
        if self.isbn:
            df = self.consultar_dataframe()
        else:
            df = self.consultar_dataframe(chave_raiz='docs')

        if df is None or df.empty:
            print("Nenhum dado encontrado.")
            return None

        df_formatado = formatar_colunas(df)

        if self.isbn:
            print("Livro encontrado!")
            return df_formatado.to_dict(orient='records')

        filtro_autor = input("Filtrar por autor (opcional): ")
        filtro_titulo = input("Filtrar por título (opcional): ")

        filtros = {'author_name': filtro_autor, 'title': filtro_titulo}
        dados_filtrados = filtrar_dados(df_formatado.to_dict(orient='records'), filtros) if (filtro_autor or filtro_titulo) else df_formatado.to_dict(orient='records')

        print("Resultados filtrados!")
        return dados_filtrados

"""

#Arquivo para tratativas específicas de API`s (sem uso no momento)
