from datetime import datetime
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import os



def run(file_path):
    #st.set_page_config(page_title="HeadCount",
    #                page_icon=":bar_chart:", layout="wide")

    st.title(" :bar_chart: Dash HEADCOUNT")
    st.markdown(
        '<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

    #visualization = st.query_params.get("visualization")
    #   UUID 
    #sources = {
    #    "26ede568-1f3f-4a26-9755-37dc36131112": "c:\\gvwin\\tvom\\tmp\\dashboard.xlsx",
    #    "2141b1d6-8705-4a95-b0e6-b4c63bdec8a1": "c:\\gvwin\\socotherm\\tmp\\dashboard.xlsx"
    #}

    #visualization = st.query_params.get("visualization")
    #   UUID 
    #sources = {
    #    "26ede568-1f3f-4a26-9755-37dc36131112": "c:\\gvwin\\tvom\\tmp\\dashboard_head.xlsx",
    #    "2141b1d6-8705-4a95-b0e6-b4c63bdec8a1": "c:\\gvwin\\socotherm\\tmp\\dashboard_head.xlsx"
    #}

    #print(visualization)
    #ruta = sources.get(visualization, None)
    #print( " la ruta es la siguiente")
    #print(ruta)
    ruta = file_path


    df = pd.read_excel(ruta, engine="openpyxl")



    #  EMPRESA
    st.sidebar.header('Elegí tu filtro: ')
    emp = st.sidebar.multiselect("EMPRESA", df["EMPRESA"].unique())
    if not emp:
        df2 = df.copy()
    else:
        df2 = df[df["EMPRESA"].isin(emp)]

    # DEPARTAMENTO
    depto = st.sidebar.multiselect("SECTOR", df2["SECTOR"].unique())
    if not depto:
        df3 = df2.copy()
    else:
        df3 = df2[df2["SECTOR"].isin(depto)]

    # U.NEGOCIO
    #unegocio = st.sidebar.multiselect(
    #    "UNIDAD DE NEGOCIO", df3["U.NEGOCIO"].unique())



    # FILTRO LOS DATOS SEGÚN HAYA SELECCIONADO
    if not emp and not depto:
        filtered_df = df
    elif not depto:
        filtered_df = df[df["EMPRESA"].isin(emp)]
    elif not emp:
        filtered_df = df[df["SECTOR"].isin(depto)]    

    elif emp and depto:
        filtered_df = df3[df["EMPRESA"].isin(emp) & df3["SECTOR"].isin(depto)]

    

    ############################
    #  Ordena DF por fechas
    filtered_df['FECHA_INGRESO'] = pd.to_datetime(filtered_df["FECHA_INGRESO"], format="%d/%m/%Y")
    filtered_df['FECHA_EGRESO'] = pd.to_datetime(filtered_df["FECHA_EGRESO"], format="%d/%m/%Y")
    filtered_df['FECHA_NACIMIENTO'] = pd.to_datetime(filtered_df["FECHA_NACIMIENTO"], format="%d/%m/%Y", errors='coerce')
    #print(filtered_df['FECHA_NACIMIENTO'])
    df_ingresos = filtered_df.sort_values("FECHA_INGRESO")
    df_ingresos['PERIODO'] = df_ingresos['FECHA_INGRESO'].dt.to_period('M').astype(str)

    # Agrupamos por FECHA_INGRESO y añadimos la columna empresa
    df_periodo = df_ingresos.groupby('PERIODO', as_index=False).size().rename(columns={'size': 'INGRESOS'})  #.tail(12)

    # egresos
    df_egresos = filtered_df.sort_values("FECHA_EGRESO").dropna()
    df_egresos['PERIODO'] = df_egresos['FECHA_EGRESO'].dt.to_period('M').astype(str)
    df_periodo2 = df_egresos.groupby('PERIODO', as_index=False).size().rename(columns={'size': 'EGRESOS'})   #.tail(12)

    # Generar rango de periodos para calcular DOTACION
    min_periodo = filtered_df['FECHA_INGRESO'].min().to_period('M')
    max_periodo = filtered_df['FECHA_EGRESO'].max().to_period('M') if not filtered_df['FECHA_EGRESO'].isna().all() else pd.Timestamp.now().to_period('M')
    rango_periodos = pd.period_range(min_periodo, max_periodo, freq='M')

    # Calcular la dotación por período
    dotacion = []
    for periodo in rango_periodos:
        count = filtered_df[
            (filtered_df['FECHA_INGRESO'] <= periodo.end_time) & 
            ((filtered_df['FECHA_EGRESO'].isna()) | (filtered_df['FECHA_EGRESO'] >= periodo.start_time))
        ].shape[0]
        dotacion.append({'PERIODO': str(periodo), 'DOTACION': count})

    df_dotacion = pd.DataFrame(dotacion) #   .tail(12)
    #print(df_dotacion)





    # Unificar los datos de ingresos y egresos ###############################
    df_combinado = pd.merge(df_periodo, df_periodo2, on="PERIODO", how="outer").fillna(0)
    df_combinado = pd.merge(df_combinado, df_dotacion, on="PERIODO", how="outer").fillna(0)
    # Ordenar cronológicamente por PERIODO
    df_combinado['PERIODO_ORDEN'] = pd.to_datetime(df_combinado['PERIODO'], format='%Y-%m')
    df_combinado = df_combinado.sort_values('PERIODO_ORDEN').drop(columns=['PERIODO_ORDEN'])
    df_combinado['INGRESOS'] = df_combinado['INGRESOS'].astype(int)
    df_combinado['EGRESOS'] = df_combinado['EGRESOS'].astype(int)
    df_combinado['DOTACION'] = df_combinado['DOTACION'].astype(int)
   
    # Gráfico combinado
    periodos_unicos = sorted(df_combinado['PERIODO'].unique())

# Seleccionar el rango de periodos usando selectbox
    st.subheader("Selecciona el rango de periodos a visualizar:")
    # Selección inicial: Últimos 12 periodos
    default_start = periodos_unicos[-12] if len(periodos_unicos) >= 12 else periodos_unicos[0]
    default_end = periodos_unicos[-1]
    col1, col2 = st.columns(2)
    with col1:
        selected_start = st.selectbox(
        "Inicio del periodo",
        options=periodos_unicos,
        index=periodos_unicos.index(default_start),
        key="start_period"
    )

    with col2:
        selected_end = st.selectbox(
        "Fin del periodo",
        options=periodos_unicos,
        index=periodos_unicos.index(default_end),
        key="end_period"
    )
    # Validar que el rango sea correcto
    if selected_start > selected_end:
        st.error("El periodo inicial debe ser anterior o igual al periodo final.")
    else:
    # Filtrar el DataFrame según el rango seleccionado
        df_combinado_filtrado = df_combinado[
        (df_combinado['PERIODO'] >= selected_start) &
        (df_combinado['PERIODO'] <= selected_end)
    ]
        
    #print(df_combinado_filtrado)        
    
    st.subheader('DOTACION, INGRESOS Y EGRESOS POR PERIODO')
    fig = go.Figure()
    # Agregar barras de ingresos
    fig.add_trace(go.Bar(
        x=df_combinado_filtrado['PERIODO'],
        y=df_combinado_filtrado['INGRESOS'],
        name='Ingresos',
        marker_color='blue',
        text=df_combinado_filtrado['INGRESOS'],  # Agregar valores como texto
        textposition='outside',  # Posicionar el texto afuera de la barra
        textangle=0  # Mantener el texto horizontal
    ))

    # Agregar barras de egresos
    fig.add_trace(go.Bar(
        x=df_combinado_filtrado['PERIODO'],
        y=df_combinado_filtrado['EGRESOS'],
        name='Egresos',
        marker_color='red',
        text=df_combinado_filtrado['EGRESOS'],  # Agregar valores como texto
        textposition='outside',  # Posicionar el texto afuera de la barra
        textangle=0  # Mantener el texto horizontal
    ))
    # Agregar barras de  dOTACION
    fig.add_trace(go.Bar(
        x=df_combinado_filtrado['PERIODO'],
        y=df_combinado_filtrado['DOTACION'],
        name='Dotación',
        marker_color='green',
        text=df_combinado_filtrado['DOTACION'],  # Agregar valores como texto
        textposition='outside',  # Posicionar el texto afuera de la barra
        textangle=0  # Mantener el texto horizontal
    ))
    # Configuración del gráfico
    fig.update_layout(
        barmode='group',  # Barras agrupadas
        template='seaborn',
        xaxis_title='Periodo',
        yaxis_title='Cantidad',
        legend_title='Categoría'
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True, height=400)
    
    with st.expander("Dotaciion a CSV"):
        styled_df = (
        df_combinado_filtrado.style
        .background_gradient(subset=['INGRESOS'], cmap='Blues')  # Color azul para INGRESOS
        .background_gradient(subset=['EGRESOS'], cmap='Reds')   # Color rojo para EGRESOS
        .background_gradient(subset=['DOTACION'], cmap='Greens')  # Color verde para DOTACIÓN
        #.format({'EGRESOS': '{:.0f}', 'INGRESOS': '{:.0f}', 'DOTACION': '{:.0f}'})  # Formatear columnas
        )
        #st.write(df_combinado.style.background_gradient(cmap="Blues").format({'EGRESOS': '{:.0f}'}))
        st.write(styled_df)
        csv = df_combinado_filtrado.to_csv(sep=';', index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="dotacion.csv", mime="text/csv",
                           help='Click para bajar los datos en csv')
   
    # Porcentaje por sexo y edad
    
    sexo_counts = filtered_df['SEXO'].value_counts().reset_index()
    sexo_counts.columns = ['SEXO', 'COUNT']
    
    
    fecha_actual = datetime.now()
    filtered_df['EDAD'] = filtered_df['FECHA_NACIMIENTO'].apply(lambda x: fecha_actual.year - x.year - ((fecha_actual.month, fecha_actual.day) < (x.month, x.day)))

    print(filtered_df[['FECHA_NACIMIENTO', 'EDAD']])
    
    #Crear un rango de edades
    filtered_df['RANGO_EDAD'] = pd.cut(filtered_df['EDAD'], bins=[18, 25, 35, 45, 55, 65, 75], 
                                   labels=['18-25', '26-35', '36-45', '46-55', '56-65', '66-75'])

    #Contar las frecuencias por rango
    rango_edad_counts = filtered_df['RANGO_EDAD'].value_counts().sort_index().reset_index()
    rango_edad_counts.columns = ['RANGO_EDAD', 'COUNT']

    
    

    c1, c2 = st.columns((2))
    
    with c1:
        st.subheader("Diversidad")
        fig = px.pie(sexo_counts, values="COUNT", names="SEXO", hole=0.5)

        fig.update_traces(text=sexo_counts["SEXO"], textposition="inside")

        st.plotly_chart(fig, use_container_width=False)
  
    with c2:
        st.subheader("Rango Edades")
        fig = px.bar(rango_edad_counts, x='RANGO_EDAD', y='COUNT', 
        title='Frecuencia por Rango de Edad', labels={'COUNT': 'Cantidad', 'RANGO_EDAD': 'Rango de Edad'})
        fig.update_traces(marker_color='teal')
        st.plotly_chart(fig, use_container_width=False)



    with st.expander("Base Completa"):
        st.write(filtered_df.style.background_gradient(cmap="Blues"))
        csv = filtered_df.to_csv(sep=';', index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="base.csv", mime="text/csv",
                         help='Click para bajar los datos en csv')

   
   