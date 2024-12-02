import streamlit as st
import headcount
import capaweb
import foto
import incidentes
import bandas

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
        "file3": f"C:\\gvwin\\tvom\\imag\\mae010\\foto\\{legajo}.jpg",
        "file4": "C:\\gvwin\\solbayres\\tmp\\dashboard_incidentes.xlsx",
        "file5": "C:\\gvwin\\tvom\\tmp\\bandas_salariales.xlsx",
        "capaweb": True,
        "headcount": True,
        "foto": True,
        "smedico": True,
        "bandas": True,
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
    file_path_foto = config["file3"]
    file_path_incid = config["file4"]
    file_path_bandas = config["file5"]

    # Crear lista de módulos habilitados
    available_modules = []
    if config["capaweb"]:
        available_modules.append("Capacitacion")
    if config["headcount"]:
        available_modules.append("HeadCount")
    if config["foto"]:
        available_modules.append("Actualiza tus datos")
        
    if config["smedico"]:
        available_modules.append("Servicio Médico")
        
    if config["bandas"]:
        available_modules.append("Bandas Salariales")
            
            
        

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
    elif selected_module == "Actualiza tus datos":
        #st.subheader("Módulo: HeadCount")
        foto.run(file_path_foto)  # Delegar al módulo `foto`
    elif selected_module == "Servicio Médico":
        incidentes.run(file_path_incid)  # Delegar al módulo de incidentes
    elif selected_module == "Bandas Salariales":
        bandas.run(file_path_bandas)  # Delegar al módulo de Bandas Salariales
            
        
