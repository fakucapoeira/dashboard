import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import matplotlib as plt
import seaborn as sns


def run(file_path):
    
    # HTML y CSS para personalizar fuentes
    st.markdown("""
        <style>
        .metric-label {
            font-size: 14px; /* Tamaño del título */
            color: #333333; /* Color del texto */
        }
        .metric-value {
            font-size: 20px; /* Tamaño del valor */
            font-weight: bold;
            color: #FF5733; /* Color del valor */
        }
        </style>
    """, unsafe_allow_html=True)
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
    depto = st.sidebar.multiselect("DEPARTAMENTO", df2["DEPARTAMENTO"].unique())
    if not depto:
        df3 = df2.copy()
    else:
        df3 = df2[df2["DEPARTAMENTO"].isin(depto)]

    # U.NEGOCIO
    unegocio = st.sidebar.multiselect(
        "UNIDAD DE NEGOCIO", df3["U.NEGOCIO"].unique())



    # FILTRO LOS DATOS SEGÚN HAYA SELECCIONADO
    if not emp and not depto and not unegocio:
        filtered_df = df
    elif not depto and not unegocio:
        filtered_df = df[df["EMPRESA"].isin(emp)]
    elif not emp and not unegocio:
        filtered_df = df[df["DEPARTAMENTO"].isin(depto)]

    elif depto and unegocio:
        filtered_df = df3[df["DEPARTAMENTO"].isin(depto) & df3["U.NEGOCIO"].isin(unegocio)]

    elif emp and unegocio:
        filtered_df = df3[df["EMPRESA"].isin(emp) & df3["U.NEGOCIO"].isin(unegocio)]

    elif emp and depto:
        filtered_df = df3[df["EMPRESA"].isin(emp) & df3["DEPARTAMENTO"].isin(depto)]

    elif unegocio:
            filtered_df = df3[df3["U.NEGOCIO"].isin(unegocio)]
    else:
        filtered_df = df3[df3["EMPRESA"].isin(emp) & df3["DEPARTAMENTO"].isin(depto) & df3["U.NEGOCIO"].isin(unegocio)]
        
        
        
    # Cálculo de métricas clave
    salario_max = filtered_df["SALARIO"].max()
    salario_min = filtered_df["SALARIO"].min()
    salario_prom = filtered_df["SALARIO"].mean()
    empleados_totales = filtered_df.shape[0]

    # Mostrar métricas
    st.header("Métricas Clave")
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"<div class='metric-label'>Salario Máximo</div><div class='metric-value'>${salario_max:,.2f}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-label'>Salario Mínimo</div><div class='metric-value'>${salario_min:,.2f}</div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric-label'>Salario Promedio</div><div class='metric-value'>${salario_prom:,.2f}</div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='metric-label'>Total Empleados</div><div class='metric-value'>{empleados_totales}</div>", unsafe_allow_html=True)



    # Distribución Salarial: Histograma

    st.subheader('DISTRIBUCION SALARIAL')
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=filtered_df['SALARIO'],
        name="Distribución Salarial",
        marker_color='blue',
        opacity=0.7
    ))
    # Líneas y anotaciones para indicadores
    fig.add_trace(go.Scatter(
        x=[salario_prom, salario_prom],
        y=[0, 10],  # Ajusta el rango del eje Y según sea necesario
        mode="lines",
        line=dict(color="red", dash="dash"),
        name="Salario Promedio"
    ))
    fig.add_trace(go.Scatter(
        x=[salario_max, salario_max],
        y=[0, 10],
        mode="lines",
        line=dict(color="green", dash="dot"),
        name="Salario Máximo"
    ))

    # Agregar anotaciones
    fig.add_annotation(
        x=salario_prom,
        y=8,  # Ajusta para que quede visible
        text=f"Promedio: ${salario_prom:,.2f}",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-50
    )

    fig.add_annotation(
        x=salario_max,
        y=8,
        text=f"Máximo: ${salario_max:,.2f}",
        showarrow=True,
        arrowhead=2,
        ax=-40,
        ay=-50
    )


    fig.update_layout(
        title="Distribución Salarial con indicadores",
        xaxis_title="Salario",
        yaxis_title="Frecuencia",
        bargap=0.1,
        template="plotly_white"
    )
    st.plotly_chart(fig)
