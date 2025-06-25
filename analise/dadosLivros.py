from coleta.api_Coleta import APIDados
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
        dados = self.consultar()

        if self.isbn:
            if not dados:
                print("Nenhum livro encontrado para o ISBN informado.")
                return None

            try:
                key = list(dados.keys())[0]
                livro = dados[key]

                if not isinstance(livro, dict):
                    livro = {}

                livro_formatado = {
                    'title': livro.get('title', 'N/A'),
                    'author_name': [autor['name'] for autor in livro.get('authors', [{'name': 'N/A'}])],
                    'first_publish_year': livro.get('publish_date', 'N/A'),
                    'isbn': [key.replace('ISBN:', '')],
                    'publisher': [editora['name'] for editora in livro.get('publishers', [{'name': 'N/A'}])]
                }

                # Exibição
                print(f"Título: {livro_formatado['title']}")
                print(f"Autor: {', '.join(livro_formatado['author_name'])}")
                print(f"Ano: {livro_formatado['first_publish_year']}")
                print(f"ISBN: {', '.join(livro_formatado['isbn'])}")
                print(f"Editora: {', '.join(livro_formatado['publisher'])}")
                print("-" * 40)

                return [livro_formatado]

            except Exception as e:
                print(f"Erro ao processar os dados retornados: {e}")
                return None

        else:
            docs = dados.get('docs', [])
            if not docs:
                print("Nenhum livro encontrado.")
                return None

            filtro_autor = input("Filtrar por autor (opcional): ")
            filtro_titulo = input("Filtrar por título (opcional): ")

            filtros = {'author_name': filtro_autor, 'title': filtro_titulo}
            dados_filtrados = filtrar_dados(docs, filtros) if (filtro_autor or filtro_titulo) else docs

            for livro in dados_filtrados:
                print(f"Título: {livro.get('title', 'N/A')}")
                autores = livro.get('author_name', [])
                print(f"Autor: {', '.join(autores)}")
                print(f"Ano: {livro.get('first_publish_year', 'N/A')}")
                print(f"ISBN: {', '.join(livro.get('isbn', ['N/A']))}")
                print("-" * 40)

            return dados_filtrados if dados_filtrados else None
