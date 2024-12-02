from datetime import datetime
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd



def run(file_path):
    #st.set_page_config(page_title="HeadCount",
    #                page_icon=":bar_chart:", layout="wide")

    st.title(" :bar_chart: Incidentes")
    st.markdown(
        '<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

    ruta = file_path


    df = pd.read_excel(ruta, engine="openpyxl")
    
    
    st.sidebar.header('Elegí tu filtro: ')
    cc = st.sidebar.multiselect("CC", df["CC"].unique())
    if not cc:
        df2 = df.copy()
    else:
        df2 = df[df["CC"].isin(cc)]

    # GERENCIA
    gcia = st.sidebar.multiselect("GERENCIA", df2["GERENCIA"].unique())
    if not gcia:
        df3 = df2.copy()
    else:
        df3 = df2[df2["GERENCIA"].isin(gcia)]
        
        
    # FILTRO LOS DATOS SEGÚN HAYA SELECCIONADO
    if not cc and not gcia:
        filtered_df = df
    elif not cc :
        filtered_df = df[df["GERENCIA"].isin(gcia)]
    elif not gcia:
        filtered_df = df[df["CC"].isin(cc)]

    elif cc and gcia:
        filtered_df = df3[df["CC"].isin(cc) & df3["GERENCIA"].isin(gcia)]
        
    # elimino registros donde viene mal la fecha    
    filtered_df = filtered_df[filtered_df['FECHA'] != "00/00/0000"]
    # Formateo Fecha del incidente        
    filtered_df['FECHA'] = pd.to_datetime(filtered_df["FECHA"], format="%d/%m/%Y")       
    
    df_incidentes = filtered_df.sort_values("FECHA")
    
    # formateo el campo HORA int a un string 2:2
    df_incidentes['HORA_FORMATO'] = df_incidentes['HORA'].apply(
    lambda x: f"{x:04d}"[:2] + ":" + f"{x:04d}"[2:]
)   
    
    # Crear un nuevo DataFrame seleccionando las columnas necesarias para archivo completo debajo del grafico
    columnas_deseadas = [
    "LEGAJO", "APELLIDO", "NOMBRE", "FECHA", "HORA_FORMATO", 
    "CLASIFICACION", "NATURALEZA_LESION", "AGENTE_CAUSANTE", 
    "FORMA_INCIDENTE", "TIPO_CASO", "GERENCIA", "CC"
    ]
    df_detalle = df_incidentes[columnas_deseadas].copy()
    df_detalle = df_detalle.rename(columns={"HORA_FORMATO": "HORA"})
    #print(df_detalle)
    

    df_incidentes['PERIODO'] = df_incidentes['FECHA'].dt.to_period('M').astype(str)
    
    # AGRUPAMOS POR PERIODO Y CONTAMOS CANTIDAD DE INCIDENTES POR PERIODO        
    df_periodo = df_incidentes.groupby('PERIODO', as_index=False).size().rename(columns={'size': 'INCIDENTES'})
    df_periodo['INCIDENTES'] = df_periodo['INCIDENTES'].astype(int)
    df_periodo['PERIODO'] = pd.to_datetime(df_periodo['PERIODO'], format='%Y-%m')
    df_periodo['PERIODO_FORMATO'] = df_periodo['PERIODO'].dt.strftime('%Y-%m')
    
    
    
    
        # Selección inicial: Últimos 12 periodosif len(df_periodo) >= 12:
    if len(df_periodo) >= 12:            
        default_start = df_periodo.iloc[-12]['PERIODO_FORMATO']
    else:
        default_start = df_periodo.iloc[0]['PERIODO_FORMATO']

    default_end = df_periodo.iloc[-1]['PERIODO_FORMATO']

    col1, col2 = st.columns(2)
    with col1:
        selected_start = st.selectbox(
            "Inicio del periodo",
            options=df_periodo['PERIODO_FORMATO'],  # Lista de periodos formateados
            index=df_periodo['PERIODO_FORMATO'].tolist().index(default_start),  # Índice del valor por defecto
            key="start_period"
        )

    with col2:
        selected_end = st.selectbox(
            "Fin del periodo",
            options=df_periodo['PERIODO_FORMATO'],
            index=df_periodo['PERIODO_FORMATO'].tolist().index(default_end),
            key="end_period"
        )

    # Validar que el rango sea correcto
    if selected_start > selected_end:
        st.error("El periodo inicial debe ser anterior o igual al periodo final.")
    else:
        # Filtrar el DataFrame según el rango seleccionado
        df_periodo_filtrado = df_periodo[
            (df_periodo['PERIODO_FORMATO'] >= selected_start) &
            (df_periodo['PERIODO_FORMATO'] <= selected_end)
        ]
        df_periodo_filtrado2 = df_incidentes[
            (df_incidentes['PERIODO'] >= selected_start) &
            (df_incidentes['PERIODO'] <= selected_end)
        ]

        # Mostrar el DataFrame filtrado con el formato adecuado
        #st.write(df_periodo_filtrado[['PERIODO_FORMATO', 'INCIDENTES']])
        fig = go.Figure()
    # Agregar barras de ingresos
    fig.add_trace(go.Bar(
        x=df_periodo_filtrado['PERIODO'],
        y=df_periodo_filtrado['INCIDENTES'],
        name='Incidentes',
        marker_color='blue',
        text=df_periodo_filtrado['INCIDENTES'],  # Agregar valores como texto
        textposition='outside',  # Posicionar el texto afuera de la barra
        textangle=0  # Mantener el texto horizontal
    ))
    st.plotly_chart(fig, use_container_width=True, height=400)
    #print(df_periodo)
    with st.expander("Datos completos"):
        # Formatear la columna FECHA para mostrar solo día, mes y año
        df_periodo_filtrado2['FECHA'] = df_detalle['FECHA'].dt.strftime('%d/%m/%Y')
        df_periodo_filtrado2['LEGAJO'] = df_detalle['LEGAJO'].astype(str)
        st.write(df_periodo_filtrado2)
        csv = df_periodo_filtrado2.to_csv(sep=';', index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Detalle_incidentes.csv", mime="text/csv",
                        help='Click para bajar los datos en csv')
    
    
    
    ## PREPARO DATAFRAME PARA ESTADISTICAS DE CLASIFICACION Y TIPO DE CASO
    df_clasificacion = df_periodo_filtrado2.groupby('CLASIFICACION', as_index=False).size().rename(columns={'size': 'CASOS'})
    df_agente = df_periodo_filtrado2.groupby('AGENTE_CAUSANTE', as_index=False).size().rename(columns={'size': 'CASOS'})

    ####################     GRAFICO TORTAS  ##########################333
    #cl1, cl2 = st.columns(2)
    
    st.subheader("Clasificación")
    fig = px.pie(df_clasificacion, values="CASOS", names="CLASIFICACION", hole=0.5)

    fig.update_traces(text=df_clasificacion["CLASIFICACION"], textposition="inside")

    st.plotly_chart(fig, use_container_width=False)
    
    st.subheader("Agente Causante")
    fig = px.pie(df_agente, values="CASOS", names="AGENTE_CAUSANTE", hole=0.5)

    fig.update_traces(text=df_agente["AGENTE_CAUSANTE"], textposition="inside")

    st.plotly_chart(fig, use_container_width=False)
            