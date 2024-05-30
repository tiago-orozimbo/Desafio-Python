import streamlit as st
import pandas as pd
import plotly.express as px
# Nome da pagina
st.set_page_config(page_title="Desafio Python")
# Abrir o aquivo css de estilização
with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
#importar os dados CSV
@st.cache_data
def carrega_dados():
    dados_csv = pd.read_csv("city_temperature.csv")
    dados_csv = dados_csv.replace ('South/Central America & Carribean', 'South/Central America')
    return dados_csv
with st.container(): #Trtamento dos dados para os gráficos
    dados = carrega_dados()
    dados1 = carrega_dados()[["Country", "City","Day", "AvgTemperature"]]
    clima2 = carrega_dados()[["Country", "City","Year","Month", "Day", "AvgTemperature"]]
    clima3 = carrega_dados()
    with st.sidebar: #Criação da Sidebar
        st.title("Temperatura Mundial")
        with st.container(): #Region
            region = st.selectbox("Selecione a região", ["Africa", "Asia", "Australia/South Pacific", "Europe", "Middle East", "North America", "South/Central America"])
            clima = carrega_dados().loc[carrega_dados()['Region'] == region]
        with st.container(): #Country
            dCity = clima[['Region', 'Country']]
            ta1 = dCity.loc[dCity["Region"] == region]
            df = pd.DataFrame(ta1)
            df = df.drop_duplicates()
            df = df.sort_values('Country', ascending=True)
            lista = df['Country'].tolist()
            country = st.selectbox("Selecione a cidade",lista )
            clima = clima.loc[clima['Country'] == country]
            clima5 = clima.loc[clima['Country'] == country]
        with st.container(): #City
            dCity = clima[['Country', 'City']]
            ta1 = dCity.loc[dCity["Country"] == country]
            df = pd.DataFrame(ta1)
            df = df.drop_duplicates()
            df = df.sort_values('City', ascending=True)
            lista = df['City'].tolist()
            city = st.selectbox("Selecione a cidade",lista )
            clima = clima.loc[clima['City'] == city]
            clima5 = clima5.loc[clima5['City'] == city]
        with st.container(): #Year
            year = st.selectbox("Selecione o ano", [1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020])
            clima= clima.loc[clima['Year'] == year]
            clima2= clima2.loc[clima2['Year'] == year]
            clima4 = clima.loc[clima['Year'] == year]
        with st.container(): #Month
            month = st.selectbox("Selecione o mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
            if month == "Janeiro":
                mes = 1
            if month == "Fevereiro":
                mes = 2
            if month == "Março":
                mes = 3
            if month == "Abril":
                mes = 4
            if month == "Maio":
                mes = 5
            if month == "Junho":
                mes = 6
            if month == "Julho":
                mes = 7
            if month == "Agosto":
                mes = 8
            if month == "Setembro":
                mes = 9
            if month == "Outubro":
                mes = 10
            if month == "Novembro":
                mes = 11
            if month == "Dezembro":
                mes = 12
            clima= clima.loc[clima['Month'] == mes]
            clima5 = clima5.loc[clima5['Month'] == mes]
        with st.container(): #Days
            days = st.selectbox("Selecione o periodo", ["7 Dias", "15 Dias", "21 Dias", "30 Dias"])
            num_days = int(days.replace("Dias", ""))
            clima = clima.loc[clima['Day'] <= num_days]
            clima5 = clima5.loc[clima5['Day'] <= num_days]
        st.subheader("Desenvolvido por Tiago Orozimbo")
        st.subheader("PDITA-046")
    clima = clima [["Country", "City","Year","Month", "Day", "AvgTemperature"]]
    clima2 = clima2 [["Country", "City","Year","Month", "Day", "AvgTemperature"]]
    clima4 = clima4 [["Country", "City","Year","Month", "Day", "AvgTemperature"]]
    clima5 = clima5 [["Country", "City","Year","Month", "Day", "AvgTemperature"]]
with st.container(): #Gráfico de barras
        grafico1= px.bar(clima, x = "Day", y = "AvgTemperature", title=f'Temperatura no mes de {month} do ano de {year}')
        grafico1.update_layout(width=400, height=300)  
with st.container(): #Gráfico de dispersão
        grafico2 = px.scatter(clima5, x="AvgTemperature", y="Day", color="Year", hover_name="Country", log_x=True, size_max=60, title='Evolução da Temperatura ao longo dos anos')
        grafico2.update_layout(width=400, height=300)
with st.container(): #grafico de pizza
    df = carrega_dados()
    df = df[df['Year'] == year]  
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    # Agrupar os dados por região e cidade e calcular os dados obtidos
    df_pie = df.groupby('Region')['City'].nunique().reset_index()
    grafico3 = px.pie(df_pie, names='Region', values='City', title=f'Percentual de dados coletados por Região em {year}')
    grafico3.update_layout(width=400, height=300)
with st.container(): #Map de Temperatura Média por País
    clima2['Date'] = pd.to_datetime(clima2[['Year', 'Month', 'Day']])
    # Agrupar os dados por país e calcular a temperatura média
    df_country = clima2.groupby('Country')['AvgTemperature'].mean().reset_index()
    # Criar o Choropleth Map
    grafico4 = px.choropleth(df_country, locations="Country", locationmode="country names",color="AvgTemperature", hover_name="Country", color_continuous_scale=px.colors.sequential.Plasma,title= f"Temperatura Média por País em {year}",template= "gridon")
    grafico4.update_layout(width=500, height=500)
with st.container():
    df = carrega_dados()
    df = df[df['Year'] == year]  # Filtrar por ano para reduzir o tamanho do dataframe
    #Agrupar os dados
    df = df.groupby(['Region', 'Year','Month', 'Day'])['AvgTemperature'].mean().reset_index()
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    grafico5 = px.line(df, x='Date', y='AvgTemperature', color='Region', title=f'Evolução da Temperatura Média ao longo dos messes do ano de {year}')
    grafico5.update_layout(width=500, height=400)
with st.container(): #Criar as colunas e plotar os gráficos 
    # Linha 1: grafico1, grafico2 e grafico3
    col1, col2, col3 = st.columns([3, 3, 3])
    with col1:
        st.plotly_chart(grafico1, use_container_width=True)
    with col2:
        st.plotly_chart(grafico2, use_container_width=True)
    with col3:
        st.plotly_chart(grafico3, use_container_width=True)
    # Linha 2: grafico4 e grafico5
    col4, col5 = st.columns([5.5, 4.5])
    with col4:
        st.plotly_chart(grafico4, use_container_width=True)
    with col5:
        st.plotly_chart(grafico5, use_container_width=True)