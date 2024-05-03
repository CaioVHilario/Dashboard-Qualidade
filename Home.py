import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# lê arquivos
df_backlog = pd.read_csv("datasets/Backlog.csv")
df_backlog_all = pd.read_csv("datasets/Backlog_all.csv")
df_backlog_real = pd.read_csv("datasets/Backlog_real.csv")

# Transforma coluna com seta em duas (data final e data incial)
# e em seguida apaga a coluna original
df_backlog_all[['Data Inicial', 'Data Final']
               ] = df_backlog_all['Data'].str.split(' → ', expand=True)
df_backlog_all.drop(columns=['Data'], inplace=True)

df_backlog_real[['Data Inicial', 'Data Final']
                ] = df_backlog_real['Data'].str.split(' → ', expand=True)
df_backlog_real.drop(columns=['Data'], inplace=True)

# Muda type das datas de object para datetime64ns[]
df_backlog_all["Data Inicial"] = pd.to_datetime(df_backlog_all["Data Inicial"])
df_backlog_all["Data Final"] = pd.to_datetime(df_backlog_all["Data Final"])
df_backlog_real["Data Inicial"] = pd.to_datetime(
    df_backlog_real["Data Inicial"])
df_backlog_real["Data Final"] = pd.to_datetime(df_backlog_real["Data Final"])

# Separa dados com "Em andamento"
df_inprogress = df_backlog_all[df_backlog_all["Status"] == "Em andamento"]

# ordena lista com as datas
df_backlog_all = df_backlog_all.sort_values(by="Data Inicial")
df_backlog_real = df_backlog_real.sort_values(by="Data Inicial")

# Cria uma coluna com o mês e ano
df_backlog_all["Month"] = df_backlog_all["Data Inicial"].apply(
    lambda x: str(x.year) + "-" + str(x.month))

df_backlog_real["Month"] = df_backlog_real["Data Inicial"].apply(
    lambda x: str(x.year) + "-" + str(x.month))

# Cria uma caixa de seleção para a o mês
month = st.sidebar.selectbox("Mês", df_backlog_all["Month"].unique())
# month = st.sidebar.selectbox("Mês", df_backlog_real["Month"].unique())

processo = df_backlog_real['Nome'].iloc[1]
# book_title = df_book["book title"].iloc[0]

st.title('Em andamento')
st.subheader(processo)

# Filtra o dataframe de acordo com a selectbox
df_filter = df_backlog_all[df_backlog_all["Month"] == month]
df_filter_real = df_backlog_real[df_backlog_real["Month"] == month]
# df_filter
df_filter_real

porcentagem_total = df_backlog_all['%'].sum() / len(df_backlog_all)
print(f"Porcentagem total do projeto: {porcentagem_total:.2%}")

# Define os dados para o gráfico de medidor de progresso circular
dados = {'Categoria': ['Concluído', 'Restante'],
         'Porcentagem': [porcentagem_total, 1 - porcentagem_total]}

# Cria um DataFrame a partir dos dados
df_medidor = pd.DataFrame(dados)

# Cria o gráfico de medidor de progresso circular
fig = px.pie(df_medidor, values='Porcentagem', names='Categoria',
             color='Categoria', color_discrete_map={'Concluído': 'green', 'Restante': 'lightgrey'},
             hole=0.7, width=400, height=400)

# Adiciona anotação com a porcentagem total no meio do gráfico
fig.add_annotation(x=0.5, y=0.5, text=f"{porcentagem_total*100:.2f}%",
                   font=dict(size=30, color="black", family="Roboto"), showarrow=False)

# Configurações adicionais do layout
fig.update_traces(textinfo='none')
fig.update_layout(title_text='Progresso do Projeto', showlegend=False)

st.plotly_chart(fig)

fig_gantt = px.timeline(
    df_filter_real,
    x_start='Data Inicial',
    x_end='Data Final',
    y='Nome',
    title='Gráfico de Gantt'
)

fig_gantt.update_yaxes(categoryorder='total ascending')
fig_gantt.update_layout(xaxis=dict(title='Data'),
                        yaxis=dict(title='Atividade'))

st.plotly_chart(fig_gantt)


# df_backlog_all
