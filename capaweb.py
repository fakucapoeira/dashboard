import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import os


# df = pd.read_csv("superstore.csv", sep=";",encoding = "ISO-8859-1")

def run(file_path):
    #st.set_page_config(page_title="Capacitacion",
    #                page_icon=":bar_chart:", layout="wide")

    st.title(" :bar_chart: Dash capacitacion")
    st.markdown(
        '<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

    # visualization = st.query_params.get("visualization")
    #   UUID
    #sources = {
    #    "26ede568-1f3f-4a26-9755-37dc36131112": "c:\\gvwin\\tvom\\tmp\\dashboard.xlsx",
    #    "2141b1d6-8705-4a95-b0e6-b4c63bdec8a1": "c:\\gvwin\\socotherm\\tmp\\dashboard.xlsx"
    #}

    # print(visualization)
    ruta = file_path
    # print( " la ruta es la siguiente")
    # print(ruta)


    # fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
    # if fl is not None:
    #    filename = fl.name
    #    st.write(filename)
    #   df = pd.read_excel(filename,engine="openpyxl")
    # else:
    #   #os.chdir(r"E:\python\Streamlit")
    #   ruta = "C:\gvwin\dashboard.xlsx"

    df = pd.read_excel(ruta, engine="openpyxl")

    col1, col2 = st.columns((2))

    df['FECHA DESDE'] = pd.to_datetime(df["FECHA DESDE"], format="%d/%m/%Y")
    df['FECHA HASTA'] = pd.to_datetime(df["FECHA HASTA"], format="%d/%m/%Y")

    startDate = df["FECHA DESDE"].min()
    endDate = df["FECHA HASTA"].max()
    # print(startDate)

    with col1:
        date1 = pd.to_datetime(st.date_input(
            "FECHA DESDE", startDate, format="MM/DD/YYYY"))

    with col2:
        date2 = pd.to_datetime(st.date_input(
            'FECHA HASTA', endDate, format="MM/DD/YYYY"))

    df = df[(df["FECHA DESDE"] >= date1) & (df["FECHA HASTA"] <= date2)].copy()
    # print(df['FECHA DESDE'])

    #  EJE
    st.sidebar.header('Elegí tu filtro: ')
    eje = st.sidebar.multiselect("Elegi el Eje", df["EJE"].unique())
    if not eje:
        df2 = df.copy()
    else:
        df2 = df[df["EJE"].isin(eje)]

    # CURSO
    curso = st.sidebar.multiselect("Elegí el curso", df2["CURSO"].unique())
    if not curso:
        df3 = df2.copy()
    else:
        df3 = df2[df2["CURSO"].isin(curso)]

    # ESTADO
    estado = st.sidebar.multiselect(
        "Elegí ESTADO del curso", df3["ESTADO"].unique())

    # FILTRO LOS DATOS SEGÚN HAYA SELECCIONADO
    if not eje and not curso and not estado:
        filtered_df = df
    elif not curso and not estado:
        filtered_df = df[df["EJE"].isin(eje)]
    elif not eje and not estado:
        filtered_df = df[df["CURSO"].isin(curso)]

    elif curso and estado:
        filtered_df = df3[df["CURSO"].isin(curso) & df3["ESTADO"].isin(estado)]

    elif eje and estado:
        filtered_df = df3[df["EJE"].isin(eje) & df3["ESTADO"].isin(estado)]

    elif eje and curso:
        filtered_df = df3[df["EJE"].isin(eje) & df3["curso"].isin(curso)]

    elif estado:
        filtered_df = df3[df3["ESTADO"].isin(estado)]
    else:
        filtered_df = df3[df3["EJE"].isin(eje) & df3["CURSO"].isin(
            curso) & df3["ESTADO"].isin(estado)]


    filtered_df['COSTO'] = pd.to_numeric(filtered_df['COSTO'])

    # corta por clave y deja todo el dataframe
    cursos_sin_duplicar = filtered_df.drop_duplicates(
        subset=["EJE", "CURSO", "FECHA DESDE"])
    # suma costos por eje
    eje_df = cursos_sin_duplicar.groupby(by=["EJE"], as_index=False)["COSTO"].sum()

    # ELIMINO COLUMNAS QUE NO QUIERO
    eje_df2 = cursos_sin_duplicar.drop(["PARTICIPANTE_ape", "PARTICIPANTE_nom", "CC  COD", "CENTRO DE COSTO", "EVA_CURSO", "EVA_DOCENTE",
                                        "ENCUENTRO_PLAN", "HORAS_PLAN", "COD EJE", "COD CURSO", "EJE", "HORAS"], axis=1)
    # FORMATEO FECHAS
    eje_df2["FECHA DESDE"] = pd.to_datetime(
        eje_df2["FECHA DESDE"], format="%d/%m/%Y")
    eje_df2["FECHA HASTA"] = pd.to_datetime(
        eje_df2["FECHA HASTA"], format="%d/%m/%Y")

    # print(" a ver")
    # print(eje_df2)

    with col1:
        st.subheader('Costos por EJE')
        fig = px.bar(eje_df, x="EJE", y="COSTO", text=['$ {:,.2f}'.format(x) for x in eje_df["COSTO"]],
                    template="seaborn")

        st.plotly_chart(fig, use_container_width=True, height=200)


    with col2:
        st.subheader("Costos por Curso")
        fig = px.pie(cursos_sin_duplicar, values="COSTO", names="CURSO", hole=0.5)

        fig.update_traces(text=cursos_sin_duplicar["CURSO"], textposition="inside")

        st.plotly_chart(fig, use_container_width=False)

    cl1, cl2 = st.columns(2)
    with cl1:
        with st.expander("Datos por EJE"):
            st.write(eje_df.style.background_gradient(cmap="Blues"))
            csv = eje_df.to_csv(sep=';', index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="Cursos_por_eje.csv", mime="text/csv",
                            help='Click para bajar los datos en csv')

    with cl2:
        with st.expander("Datos por Curso"):
            # Crear una columna temporal para mostrar la fecha formateada, sin alterar los datos originales
            eje_df2['FECHA FORMATEADA'] = eje_df2['FECHA DESDE'].dt.strftime('%d/%m/%Y')
            eje_df2['FECHA FORMATEADA2'] = eje_df2['FECHA HASTA'].dt.strftime('%d/%m/%Y')
            # Eliminar la columna "FECHA FORMATEADA" de su posición actual y guardarla
            col_formateada = eje_df2.pop('FECHA FORMATEADA')
            col_formateada2 = eje_df2.pop('FECHA FORMATEADA2')

            # Insertar la columna "FECHA FORMATEADA" en la posición deseada (índice 2, que corresponde a la columna 3)
            eje_df2.insert(2, 'FECHA D.', col_formateada)
            eje_df2.insert(3, 'FECHA H.', col_formateada2)
    
            # Usar la columna formateada solo para la visualización
            st.write(eje_df2.drop(columns=['FECHA DESDE', 'FECHA HASTA']).style.background_gradient(cmap="Oranges"))
            csv = eje_df2.to_csv(sep=';', index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="Cursos_datos.csv", mime="text/csv",
                            help='Click para bajar los datos en csv')

    # PLANIIFICACION TIEMPO CALENDDARIO
    # filtered_df["PERIODO"] = filtered_df["FECHA DESDE"].dt.to_period("M")
    # print(filtered_df)
    st.subheader('PLANIFICACIÓN PERÍODOS')
    tasks_df = eje_df2['CURSO']
    start_date = eje_df2['FECHA DESDE']
    finish_date = eje_df2['FECHA HASTA']
    state = eje_df2['ESTADO']
    fig3 = px.timeline(
        eje_df2, x_start=start_date, x_end=finish_date, y=tasks_df,
        color=state, color_continuous_scale="Viridis",
        title="CURSOS ESTADOS"
    )
    fig3.update_layout(
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            zeroline=True,
            showline=True,
            linecolor='black',
            linewidth=2),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgrey',
            zeroline=True,
            showline=True,
            linecolor='black',
            linewidth=2)
    )
    st.plotly_chart(fig3, use_container_width=True)

    conteo_estado = eje_df2.groupby('ESTADO')['ESTADO'].value_counts()
    ce = pd.DataFrame(conteo_estado)
    ce.reset_index(level=0, inplace=True)  # Para mantener el índice como columna
    ce.columns = ['ESTADO', 'CONTEO']  # Cambia el nombre de las columnas

    st.subheader('ESTADO DE LOS CURSOS')
    fig = px.pie(ce, values="CONTEO", names="ESTADO", template="plotly_dark")
    fig.update_traces(text=ce["ESTADO"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)


    ########################################
    df_horas = cursos_sin_duplicar.drop(["PARTICIPANTE_ape", "PARTICIPANTE_nom", "CC  COD", "CENTRO DE COSTO", "EVA_CURSO", "EVA_DOCENTE",
                                        "ENCUENTRO_PLAN", "COD EJE", "COD CURSO", "EJE", "COSTO", "ENTE"], axis=1)
    print(df_horas)

    st.subheader('HORAS PLANIFICADAS / CURSADAS')
    fig4 = px.bar(df_horas, x="CURSO", y="HORAS", text=[
                '{:,.2f}   Hs'.format(x) for x in df_horas["HORAS"]], template="seaborn")
    fig4.add_trace(
        go.Scatter(
            x=df_horas['CURSO'],
            y=df_horas['HORAS_PLAN'],
            mode='markers',
            name='Horas Plan',
            marker=dict(color='red', size=10)
        )
    )
    fig4.update_layout(
        yaxis_title='Horas Planificadas',
        yaxis2=dict(
            title='HORAS PLANIFICADAS',
            overlaying='y',
            side='right'
        ),
        xaxis_title='Curso'
    )
    st.plotly_chart(fig4, use_container_width=True, height=200)
    with st.expander("horas"):
        
        # Crear una columna temporal para mostrar la fecha formateada, sin alterar los datos originales
        df_horas['FECHA FORMATEADA'] = df_horas['FECHA DESDE'].dt.strftime('%d/%m/%Y')
        df_horas['FECHA FORMATEADA2'] = df_horas['FECHA HASTA'].dt.strftime('%d/%m/%Y')
            # Eliminar la columna "FECHA FORMATEADA" de su posición actual y guardarla
        col_formateada = df_horas.pop('FECHA FORMATEADA')
        col_formateada2 = df_horas.pop('FECHA FORMATEADA2')

            # Insertar la columna "FECHA FORMATEADA" en la posición deseada (índice 2, que corresponde a la columna 3)
        df_horas.insert(2, 'FECHA D.', col_formateada)
        df_horas.insert(3, 'FECHA H.', col_formateada2)
    
        
            
        # st.dataframe(df_horas.style.background_gradient(cmap="Blues"))
        styled_df = df_horas.drop(columns=['FECHA DESDE', 'FECHA HASTA']).style.background_gradient(
            cmap="Blues").format({'HORAS': '{:.2f}'})
        st.write(styled_df)
        csv = df_horas.to_csv(sep=';', index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Cursos_horas.csv", mime="text/csv",
                        help='Click para bajar los datos en csv')
