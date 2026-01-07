# Aviso: documentação atual desatualizada para refatoração do projeto por enquanto, estas informações estão válidas apenas para a versão legafo encontrada na branch "legado" do sistema. 

## **AxiomaPy**

> AxiomaPy é um sistema modular para: coleta, processamento, análise e visualização de dados. Ele oferece um menu interativo para que o usuário possa importar dados, analisar estatísticas, criar gráficos e realizar operações como salvar ou visualizar os dados formatados.

### Visão Geral

O sistema permite:

* Coletar dados de: Arquivos Locais (CSV ou JSON por enquanto) ou de APIs externas configuráveis.

* Realizar formatação e seleção de colunas.

* Gerar estatísticas descritivas e diversos tipos de gráficos.

* Salvar os dados processados em arquivos JSON.

* Executar análises práticas como desempenho de equipes, análise de preços, comparação de tempo de uso e diversas outros possíbilidades.

* Navegar por todas as funcionalidades através de menus.

### Estrutura de Pastas

**AxiomaPy**

| Pastas               | Função da pasta                                       |
|:-------------------- |:----------------------------------------------------- |
| analise/             | Manipulação e formatação de dados                     |
| coleta/              | Coleta local e via API                                |
| utils/               | Funções auxiliares (seleção de arquivo, salvamento)   |
| visualizacao/        | Geração de gráficos e estatísticas                    |
| testes/              | Testes automatizados                                  |
| .github/workflows/   | Pipeline de testes (GitHub Actions)                   |

**Arquivos Importantes**

| Arquivo             | Função
|:--------------------|:----------------------------
| api_Config.json     | Configuração das APIs utilizadas
| requirements.txt    | Bibliotecas necessárias
| main.py             | Execução principal do sistema


### Como Usar o Sistema

#### Execute o arquivo principal:

~~~~bash
python main.py
~~~~

#### Utilize o menu interativo para:

1. Selecionar a origem dos dados: API ou arquivo local.

2. Formatar as colunas (selecionar e renomear).

3. Explorar estatísticas descritivas.

4. Gerar gráficos: barras, pizza, linha, boxplot, dispersão e histograma.

5. Realizar análises práticas como desempenho ou evolução de preços.

6. Salvar os dados processados.

### Como Adicionar uma Nova API

As APIs disponíveis são configuradas no arquivo api_Config.json.

Exemplo de configuração:
~~~~json
{
  "nomeAPI": {
    "url": "https://apiSimples.org/search.json",
    "params": ["query", "limit"],
    "requires_key": false,
    "default_response_path": "docs",
    "default_fields": ["title", "author_name"]
  },
}
~~~~

**Passos:**

#### Adicione uma nova API ao sistema preenchendo os campos:

_nome:_ 

_url:_

_parametros:_

_requires-key_: (para caso a api requer um login ou algo do tipo para utiliza-lá)

_default-response-path_: (para definir a camada desejada dentro do JSON recebido da api)

_default-fields_: (campos que o sistema sempre coleta na resposta da api)
 
#### O sistema automaticamente reconhecerá a nova API na execução.

## Casos de Uso Recomendados

>Análise de Desempenho de Funcionários: Comparação entre horas trabalhadas e metas estabelecidas.
>
>>Análise de Preços: Exploração de listas de produtos e seus valores.
>
>>>Exploração de APIs Externas: Importação de informações de bibliotecas públicas ou APIs customizadas.
>
>>>>Análises Categóricas: Frequência de produtos, clientes ou eventos.
>
>>>>>Análises Temporais: Evolução de dados ao longo de períodos, como vendas mensais ou produção diária.

## Requisitos

#### **Python 3.11 ou superior**

Instale as dependências com:

~~~bash

pip install -r requirements.txt

~~~
