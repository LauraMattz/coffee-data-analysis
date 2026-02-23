# Análise de Dados de Café ☕

👋 Bem-vindo ao repositório do projeto de Análise de Dados de Café, uma aplicação Streamlit que fornece insights visuais detalhados sobre as tendências dos preços do café ao longo dos anos. Este projeto utiliza dados históricos para apresentar análises dinâmicas e interativas, permitindo aos usuários explorar variações de preços em diferentes períodos e condições de mercado.

## 📄 Visão Geral dos Arquivos

- **app.py**: Contém o código principal do aplicativo Streamlit.
- **coffee_data.xlsx**: Arquivo Excel com dados anuais do café CEPEA (2001-2026).
- **requirements.txt**: Lista as dependências necessárias para executar o aplicativo.

**Nota:** Este app trabalha com **dados anuais agregados** do CEPEA ROBUSTA, mostrando médias anuais de preços.

## 🛠️ Instruções de Configuração

1. Clone o repositório ou baixe o código-fonte:
    ```sh
    git clone https://github.com/seu-usuario/coffee-data-analysis.git
    cd coffee-data-analysis
    ```

2. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

3. Execute o aplicativo:
    ```sh
    streamlit run app.py
    ```

## 🌟 Funcionalidades

- **Filtros por ano**: Permite selecionar os anos para análise.
- **📈 Gráficos de preços de café**: Exibe a evolução dos preços médios anuais e a variação percentual anual.
- **📊 Tabela de dados filtrados**: Mostra os dados filtrados com formatação condicional.

## 📉 Menor Preço Médio
- **R$ 118.09**
- **Ano: 2001**

## 📈 Maior Preço Médio
- **R$ 2449.18**
- **Ano: 2025**

## 💵 Preço Médio Anual
- **R$ 483.32**

## ☕ Preço por Xícara
- **R$ 0.0806**
- **(6000 xícaras/saca)**

## 📈 Tendência de Crescimento

- **Crescimento Acumulado Total:** De 1996 a 2025, o preço médio aumentou **1949.01%**.
- **Taxa de Crescimento Anual Média:** Em média, o preço médio aumentou **14.92%** ao ano.

## 📊 Resumo Anual e Variação Percentual

- **Evolução dos Preços Médios Anuais**

## 🤝 Contribuindo

Sinta-se à vontade para enviar issues ou pull requests para melhorias ou correções de bugs.

## 📞 Contato

Para mais informações, visite meu [LinkedIn](https://www.linkedin.com/in/lauramattosc/).

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.

---

## 📝 Changelog

### 23/02/2026 - v2.0
- ✅ **Dados atualizados**: Arquivo atualizado com dados anuais CEPEA até 2026 (26 anos)
- ✅ **Correções de deprecação do Streamlit**:
  - Substituído `.applymap()` por `.map()` para compatibilidade com pandas moderno
  - Atualizado `use_container_width` para o novo parâmetro `width` em todos os gráficos e dataframes
  - Corrigidas 3 ocorrências de warnings de deprecação
- ✅ **Adaptação para dados anuais**:
  - App adaptado para trabalhar com médias anuais agregadas ao invés de dados diários
  - Arquivo convertido de `.xls` (formato antigo CEPEA) para `.xlsx` processado
  - Função `load_data()` simplificada para melhor compatibilidade
  - Filtro de anos ajustado para 2001-2026

**Data de Atualização:** 23/02/2026
