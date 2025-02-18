# Análise de Dados de Café

Este é um aplicativo Streamlit para analisar dados de café a partir de uma planilha XLS e dados atuais obtidos via API.

## Estrutura do Projeto
coffee-data-analysis 
├── src 
│ ├── app.py 
│ ├── coffee_data.xls 
│ ├── requirements.txt 
└── README.md


## Visão Geral dos Arquivos

- **src/app.py**: Contém o código principal do aplicativo Streamlit.
- **src/coffee_data.xls**: Planilha XLS com os dados de café.
- **src/requirements.txt**: Lista as dependências necessárias para executar o aplicativo.

## Instruções de Configuração

1. Clone o repositório ou baixe o código-fonte.
2. Navegue até o diretório `src`.
3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```
4. Execute o aplicativo:
    ```sh
    streamlit run app.py
    ```

## Funcionalidades

- Filtros por ano
- Gráficos de preços de café
- Tabela de dados filtrados

## Contribuindo

Sinta-se à vontade para enviar issues ou pull requests para melhorias ou correções de bugs.
