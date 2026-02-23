import streamlit as st
import pandas as pd
import altair as alt
import os

# CONSTANTES
DATA_FILE = "coffee_data.xlsx"  # Arquivo de dados processado do CEPEA
LINKEDIN_URL = "https://www.linkedin.com/in/lauramattosc/"
UPDATE_DATE = "23/02/2026"

# CONFIGURAÇÕES E CSS
def configure_page():
    st.set_page_config(page_title="Análise de Dados de Café", page_icon="☕", layout="wide")
    st.markdown(
        """
        <style>
        body {
            background-color: #000;
            color: white;
        }
        .reportview-container .main .block-container{
             background-color: #000;
             color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# CARREGAMENTO DE DADOS
@st.cache_data(show_spinner=False)
def load_data(file_path: str) -> pd.DataFrame:
    """Carrega dados do arquivo Excel do CEPEA (dados anuais agregados)."""
    try:
        # Carrega arquivo XLSX processado
        df = pd.read_excel(file_path)

        # Garante que Data está em datetime
        df['Data'] = pd.to_datetime(df['Data'])

        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# PRÉ-PROCESSAMENTO
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepara dados anuais para análise."""
    try:
        # Garante que Data está em datetime
        if not pd.api.types.is_datetime64_any_dtype(df['Data']):
            df['Data'] = pd.to_datetime(df['Data'])
    except Exception as e:
        st.error(f"Erro na conversão da coluna 'Data': {e}")

    # Extrai ano
    df['year'] = df['Data'].dt.year

    # Filtra anos válidos
    current_year = pd.Timestamp.now().year
    df = df[(df['year'] <= current_year) & (df['year'] >= 2001)].copy()

    return df

# FILTROS INTERATIVOS NA SIDEBAR
def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros")
    anos = sorted(df['year'].unique())
    anos_selecionados = st.sidebar.multiselect("Selecione os anos", anos, default=anos)
    preco_min = float(df['À vista R$'].min())
    preco_max = float(df['À vista R$'].max())
    intervalo_preco = st.sidebar.slider("Intervalo de Preço Médio Anual (R$)",
                                         min_value=round(preco_min, 2),
                                         max_value=round(preco_max, 2),
                                         value=(round(preco_min, 2), round(preco_max, 2)))
    df_filtered = df[df['year'].isin(anos_selecionados)].copy()
    df_filtered = df_filtered[(df_filtered['À vista R$'] >= intervalo_preco[0]) &
                              (df_filtered['À vista R$'] <= intervalo_preco[1])]
    return df_filtered

# AGREGAR DADOS ANUAIS
def aggregate_annual(df: pd.DataFrame) -> pd.DataFrame:
    df_annual = df.groupby('year', as_index=False).agg(
        Preco_Medio=('À vista R$', 'mean')
    )
    df_annual['Preco_Medio'] = df_annual['Preco_Medio'].round(2)
    df_annual['Percentual de Aumento'] = df_annual['Preco_Medio'].pct_change() * 100
    df_annual['Percentual de Aumento'] = df_annual['Percentual de Aumento'].round(2)
    return df_annual

# EXIBIÇÃO DOS BIG NUMBERS
def display_big_numbers(df_annual: pd.DataFrame):
    menor_preco = df_annual['Preco_Medio'].min()
    maior_preco = df_annual['Preco_Medio'].max()
    preco_medio_total = df_annual['Preco_Medio'].mean()
    preco_xicara = preco_medio_total / 6000  # Considerando 6000 xícaras/saca
    ano_menor = int(df_annual.loc[df_annual['Preco_Medio'] == menor_preco, 'year'].iloc[0])
    ano_maior = int(df_annual.loc[df_annual['Preco_Medio'] == maior_preco, 'year'].iloc[0])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(
        f"<div style='padding: 20px; text-align: center;'>"
        f"<span style='font-size:1.5rem; color:green;'>📉 Menor Preço Médio</span><br>"
        f"<span style='font-size:2.5rem; color:green;'>R$ {menor_preco:.2f}</span><br>"
        f"<span style='font-size:1.2rem;'>Ano: {ano_menor}</span>"
        f"</div>", unsafe_allow_html=True)
    col2.markdown(
        f"<div style='padding: 20px; text-align: center;'>"
        f"<span style='font-size:1.5rem; color:red;'>📈 Maior Preço Médio</span><br>"
        f"<span style='font-size:2.5rem; color:red;'>R$ {maior_preco:.2f}</span><br>"
        f"<span style='font-size:1.2rem;'>Ano: {ano_maior}</span>"
        f"</div>", unsafe_allow_html=True)
    col3.markdown(
        f"<div style='padding: 20px; text-align: center;'>"
        f"<span style='font-size:1.5rem; color:blue;'>💵 Preço Médio Anual</span><br>"
        f"<span style='font-size:2.5rem; color:blue;'>R$ {preco_medio_total:.2f}</span>"
        f"</div>", unsafe_allow_html=True)
    col4.markdown(
        f"<div style='padding: 20px; text-align: center;'>"
        f"<span style='font-size:1.5rem; color:saddlebrown;'>☕ Preço por Xícara</span><br>"
        f"<span style='font-size:2.5rem; color:saddlebrown;'>R$ {preco_xicara:.4f}</span><br>"
        f"<span style='font-size:1.2rem;'>(6000 xícaras/saca)</span>"
        f"</div>", unsafe_allow_html=True)

# EXIBIÇÃO DOS INDICADORES DESCRITIVOS
def display_indicators(df_annual: pd.DataFrame):
    st.markdown(
        """
        **Tendência de Crescimento:**  
        - O **Crescimento Acumulado Total** indica o percentual de aumento da média anual do primeiro para o último ano selecionado.  
        - A **Taxa de Crescimento Anual Média** reflete, em média, o quanto o preço médio aumentou ano a ano.
        """
    )
    if len(df_annual) >= 2:
        primeiro_ano = df_annual.iloc[0]
        ultimo_ano = df_annual.iloc[-1]
        crescimento_acumulado = ((ultimo_ano['Preco_Medio'] / primeiro_ano['Preco_Medio']) - 1) * 100
        taxa_crescimento_simples = df_annual['Percentual de Aumento'][1:].mean()
        col_a, col_b = st.columns(2)
        col_a.markdown(
            f"**Crescimento Acumulado Total:** De {int(primeiro_ano['year'])} a {int(ultimo_ano['year'])}, o preço médio aumentou **{crescimento_acumulado:.2f}%**."
        )
        col_b.markdown(
            f"**Taxa de Crescimento Anual Média:** Em média, o preço médio aumentou **{taxa_crescimento_simples:.2f}%** ao ano."
        )
    else:
        st.info("Dados insuficientes para calcular os indicadores de crescimento.")

# EXIBIÇÃO DA TABELA RESUMO
def display_summary_table(df_annual: pd.DataFrame):
    def color_percent(val):
        if pd.isna(val):
            return ''
        color = 'red' if val < 0 else 'green'
        return f'color: {color}'
    resumo_anual_styled = df_annual.style.format({
        "Preco_Medio": "R$ {:.2f}",
        "Percentual de Aumento": "{:.2f}%"
    }).map(color_percent, subset=['Percentual de Aumento'])
    st.dataframe(resumo_anual_styled, width='stretch')

# EXIBIÇÃO DOS GRÁFICOS (INTERATIVOS)
def display_charts(df_annual: pd.DataFrame):
    st.sidebar.header("Visualizações")
    mostrar_evolucao = st.sidebar.checkbox("Evolução dos Preços Médios Anuais", value=True)    
    if mostrar_evolucao:
        with st.expander("Evolução dos Preços Médios Anuais", expanded=True):
            base_precos = alt.Chart(df_annual).encode(
                x=alt.X('year:O', title="Ano"),
                y=alt.Y('Preco_Medio:Q', title="Preço Médio (R$)")
            )
            linha_precos = base_precos.mark_line(color='orange').encode(
                tooltip=[alt.Tooltip('year:O', title="Ano"),
                         alt.Tooltip('Preco_Medio:Q', title="Preço Médio (R$)", format=",.2f")]
            )
            pontos_precos = base_precos.mark_circle(color='orange', size=60).encode(
                tooltip=[alt.Tooltip('year:O', title="Ano"),
                         alt.Tooltip('Preco_Medio:Q', title="Preço Médio (R$)", format=",.2f")]
            )
            labels_precos = base_precos.mark_text(dy=-10, color='orange').encode(
                text=alt.Text('Preco_Medio:Q', format=".2f")
            )
            grafico_precos = (linha_precos + pontos_precos + labels_precos).properties(
                width=800, height=400, title="Evolução dos Preços Médios Anuais"
            )
            st.altair_chart(grafico_precos, width='stretch')


# RODAPÉ E BOTÃO LINKEDIN
def display_footer():
    st.markdown(f"<div style='text-align: center; padding: 20px;'>Data de Atualização: {UPDATE_DATE}</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px;">
            <a href="{LINKEDIN_URL}" target="_blank">
                <button style="background-color: #0e76a8; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-size: 1.2rem;">
                    Visite meu LinkedIn: Laura Mattos
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# FUNÇÃO PRINCIPAL
def main():
    configure_page()
    st.title("📊 Análise de Dados de Café")
    st.markdown(
        """
        Esta aplicação exibe estatísticas e tendências dos preços do café com base na **média anual**.
        Selecione os filtros na barra lateral para personalizar a análise.
        
        **Nota:** Dados em Reais por saca de 60 kg líquido, considerando 10 g por xícara (~6000 xícaras/saca).
        """
    )
    df = load_data(DATA_FILE)
    if df.empty:
        st.error("Nenhum dado disponível para exibição.")
        st.stop()
    
    df = preprocess_data(df)
    df_filtered = filter_data(df)
    df_annual = aggregate_annual(df_filtered)
    
    display_big_numbers(df_annual)
    display_indicators(df_annual)
    
    st.header("Resumo Anual e Variação Percentual")
    col_table, col_graph = st.columns(2)
    with col_table:
        display_summary_table(df_annual)
    with col_graph:
        base_pct = alt.Chart(df_annual).encode(
            x=alt.X('year:O', title="Ano"),
            y=alt.Y('Percentual de Aumento:Q', title="Percentual de Aumento (%)")
        )
        linha_pct = base_pct.mark_line(color='green').encode(
            tooltip=[alt.Tooltip('year:O', title="Ano"),
                     alt.Tooltip('Percentual de Aumento:Q', title="Variação (%)", format=".2f")]
        )
        pontos_pct = base_pct.mark_circle(color='green', size=60).encode(
            tooltip=[alt.Tooltip('year:O', title="Ano"),
                     alt.Tooltip('Percentual de Aumento:Q', title="Variação (%)", format=".2f")]
        )
        linha_zero = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='red').encode(y='y:Q')
        labels_pct = base_pct.mark_text(dy=-10, color='green').encode(
            text=alt.Text('Percentual de Aumento:Q', format=".2f")
        )
        grafico_pct = (linha_pct + pontos_pct + linha_zero + labels_pct).properties(
            width=400, height=400, title="Variação Percentual Anual"
        )
        st.altair_chart(grafico_pct, width='stretch')
    
    display_charts(df_annual)
    display_footer()

if __name__ == "__main__":
    main()

