Axioma\_Py

Axioma\_Py é um sistema modular para \*\*coleta, processamento, análise e visualização de dados\*\*. Ele oferece um menu interativo para que o usuário possa importar dados, analisar estatísticas, criar gráficos e realizar operações como salvar ou visualizar os dados formatados.

🔍 Visão Geral

O sistema permite:

\- Coletar dados de \*\*arquivos locais (CSV ou JSON)\*\* ou de \*\*APIs externas configuráveis\*\*.

\- Realizar formatação e seleção de colunas.

\- Gerar \*\*estatísticas descritivas\*\* e diversos tipos de gráficos.

\- Salvar os dados processados em arquivos JSON.

\- Executar análises práticas como desempenho de equipes ou análise de preços.

\- Navegar por todas as funcionalidades através de menus intuitivos.

🗂️ Estrutura de Pastas

Axioma\_Py/

├── analise/ # Manipulação e formatação de dados

├── coleta/ # Coleta local e via API

├── utils/ # Funções auxiliares (seleção de arquivo, salvamento)

├── visualizacao/ # Geração de gráficos e estatísticas

├── testes/ # Testes automatizados

├── .github/workflows/ # Pipeline de testes (GitHub Actions)

├── config.json # Configuração das APIs utilizadas

├── requirements.txt # Bibliotecas necessárias

└── main.py # Execução principal do sistema

✅ Como Usar o Sistema

Execute o arquivo principal:

bash

Copiar

Editar

python main.py

Utilize o menu interativo para:

Selecionar a origem dos dados: API ou arquivo local.

Formatar as colunas (selecionar e renomear).

Explorar estatísticas descritivas.

Gerar gráficos: barras, pizza, linha, boxplot, dispersão e histograma.

Realizar análises práticas como desempenho ou evolução de preços.

Salvar os dados processados.

🌐 Como Adicionar uma Nova API

As APIs disponíveis são configuradas no arquivo config.json.

Exemplo de configuração:

json

Copiar

Editar

{

"apis": \[

{

"nome": "OpenLibrary",

"url\_base": "https://openlibrary.org/search.json",

"parametros": {

"q": "query",

"limit": "limit"

}

}

\]

}

Passos:

Adicione um novo objeto no array apis com:

nome: Nome identificador da API.

url\_base: URL base da API.

parametros: Parâmetros aceitos pela API.

O sistema automaticamente reconhecerá a nova API na execução.

💡 Casos de Uso Recomendados

Análise de Desempenho de Funcionários: Comparação entre horas trabalhadas e metas estabelecidas.

Análise de Preços: Exploração de listas de produtos e seus valores.

Exploração de APIs Externas: Importação de informações de bibliotecas públicas ou APIs customizadas.

Análises Categóricas: Frequência de produtos, clientes ou eventos.

Análises Temporais: Evolução de dados ao longo de períodos, como vendas mensais ou produção diária.

🔧 Requisitos

Python 3.11 ou superior

Instale as dependências com:

bash

Copiar

Editar

pip install -r requirements.txt