import pandas as pd
import plotly.express as px
import streamlit as st

# Carregar os dados diretamente do arquivo local
arquivo = 'MOVIMENTOS - FACAS.xlsx'
# Certifique-se de que 'Data' está no formato datetime
df = pd.read_excel(arquivo, parse_dates=['Data'])  

# Configurações da página
st.title("Visualização de Estoque por Tipo de Operação")
st.sidebar.header("Configurações do Filtro")

# Adicionar colunas de Ano e Mês
df['Ano'] = df['Data'].dt.year
df['Mes'] = df['Data'].dt.month

# Filtro por Tipo de Operação
tipo_operacao = st.sidebar.selectbox(
    "Selecione o Tipo de Operação",
    options=df['Tipo de Operação'].unique(),
    index=0
)

# Filtro por Nome Completo (Toggle)
usar_nome_completo = st.sidebar.checkbox("Filtrar por Nome Completo?", value=False)
if usar_nome_completo:
    nome_completo = st.sidebar.selectbox(
        "Selecione o Nome Completo",
        options=df['Nome Completo'].unique(),
        index=0
    )
else:
    nome_completo = None  # Sem filtro por nome completo

# Filtros por Ano e Mês
anos_selecionados = st.sidebar.multiselect(
    "Selecione os Anos",
    options=sorted(df['Ano'].unique()),
    default=sorted(df['Ano'].unique())
)

meses_selecionados = st.sidebar.multiselect(
    "Selecione os Meses",
    options=sorted(df['Mes'].unique()),
    default=sorted(df['Mes'].unique())
)

# Aplicação dos Filtros
df_filtered = df[df['Tipo de Operação'] == tipo_operacao]

if usar_nome_completo and nome_completo:
    df_filtered = df_filtered[df_filtered['Nome Completo'] == nome_completo]

if anos_selecionados:
    df_filtered = df_filtered[df_filtered['Ano'].isin(anos_selecionados)]

if meses_selecionados:
    df_filtered = df_filtered[df_filtered['Mes'].isin(meses_selecionados)]

# Criar Gráfico Dinâmico
if not df_filtered.empty:
    df_aux = df_filtered.groupby(['Data'])['Quantidade'].sum().reset_index()
    fig = px.line(df_aux, x='Data', y='Quantidade', title="Quantidade por Data (com filtros aplicados)")
    st.plotly_chart(fig)
else:
    st.warning("Nenhum dado encontrado para os filtros aplicados.")
