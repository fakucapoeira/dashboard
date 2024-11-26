import streamlit as st
import headcount
import capaweb
# Obtener parámetros de consulta
# Configuración inicial de la página
st.set_page_config(page_title="Aplicación", layout="wide")
visualization = st.query_params.get("visualization")
legajo = st.query_params.get("legajo")
print(legajo)
print(visualization)
# Definir las fuentes disponibles
sources = {
    "26ede568-1f3f-4a26-9755-37dc36131112": {
        "file": "c:\\gvwin\\tvom\\tmp\\dashboard.xlsx",
        "file2": "c:\\gvwin\\tvom\\tmp\\dashboard_head.xlsx",
        "capaweb": True,
        "headcount": True,
        "foto": True,
    },
    "2141b1d6-8705-4a95-b0e6-b4c63bdec8a1": {
        "file": "c:\\gvwin\\socotherm\\tmp\\dashboard.xlsx",
        "capaweb": True,
        "headcount": False,
    },
}

# Validar si el parámetro `visualization` está en las fuentes
if visualization not in sources:
    st.error("El parámetro 'visualization' no es válido.")
else:
    # Obtener configuración correspondiente al UUID
    config = sources[visualization]
    file_path_capa = config["file"]
    file_path_head = config["file2"]

    # Crear lista de módulos habilitados
    available_modules = []
    if config["capaweb"]:
        available_modules.append("Capacitacion")
    if config["headcount"]:
        available_modules.append("HeadCount")

    # Preguntar al usuario qué módulo quiere ver
    st.sidebar.header("Selecciona el módulo:")
    selected_module = st.sidebar.radio("Módulos disponibles", available_modules)

    # Ejecutar el módulo seleccionado
    if selected_module == "Capacitacion":
        #st.subheader("Módulo: capaweb")
        capaweb.run(file_path_capa)  # Delegar al módulo `capaweb`
    elif selected_module == "HeadCount":
        #st.subheader("Módulo: HeadCount")
        headcount.run(file_path_head)  # Delegar al módulo `headcount`
