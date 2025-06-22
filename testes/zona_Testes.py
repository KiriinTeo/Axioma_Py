import unittest
from analise.dadosLivros import pesquisarLivro, filtrarConsulta, adicionarLivro
from analise.analiseLivros import formatacaoDados, filtragemAvancada

class TestBiblioteca(unittest.TestCase):
    def test_pesquisarLivro_isbn(self):
        dados = pesquisarLivro(isbn="9780140328721")
        self.assertIsNotNone(dados)
        self.assertIn('docs', dados)

    def test_pesquisarLivro_titulo_autor(self):
        dados = pesquisarLivro(titulo="The Hobbit", autor="J.R.R. Tolkien")
        self.assertIsNotNone(dados)
        self.assertIn('docs', dados)

    def test_filtrarConsulta(self):
        dados = pesquisarLivro(titulo="The Hobbit", autor="J.R.R. Tolkien")
        filtrados = filtrarConsulta(dados, filtro_titulo="The Hobbit", filtro_ano="1937")
        self.assertGreater(len(filtrados), 0)
        for livro in filtrados:
            self.assertEqual(livro.get('title'), "The Hobbit")
    
    def test_formatacaoDados(self):
        dados = pesquisarLivro(titulo="The Hobbit", autor="Tolkien")
        df = formatacaoDados(dados)
        self.assertIsNotNone(df)
        self.assertIn('Título', df.columns)
        self.assertIn('Autor', df.columns)
        self.assertIn('Ano de Publicação', df.columns)
        self.assertIn('ISBN', df.columns)
        self.assertIn('Editora', df.columns)
        self.assertIn('Temas', df.columns)

    def test_filtragemAvancada(self):
        dados = pesquisarLivro(titulo="The Hobbit", autor="J.R.R. Tolkien")
        df = formatacaoDados(dados)
        self.assertIsNotNone(df)
        
        filtros = {
            'Título': 'The Hobbit',
            'Autor': 'Tolkien'
        }
        
        df_filtrado = filtragemAvancada(df, filtros)
        
        self.assertGreater(len(df_filtrado), 0)
        for _, row in df_filtrado.iterrows():
            self.assertIn('hobbit', row['Título'].lower())
            self.assertIn('tolkien', row['Autor'].lower())

if __name__ == '__main__':
    unittest.main()