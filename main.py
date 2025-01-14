import streamlit as st
import headcount
import headcount_2
import headcount_soco
import capaweb
import foto
import incidentes
import bandas
import time


# e0ce6f103afe080f90772ea32155c4677591d0cbea4516ca2fa693f4fc07fa7a

# Obtener parámetros de consulta
# Configuración inicial de la página
st.set_page_config(page_title="Aplicación", layout="wide")
visualization = st.query_params.get("visualization")
tiempo = st.query_params.get("s")
legajo = st.query_params.get("l")

if tiempo is not None:
    try:
        tiempo = float(tiempo)
    except ValueError:
        st.error("El parámetro 's' no es un número válido.")
        tiempo = None
#print(legajo)
#print(visualization)


    
ts = time.time()
print("tiempo")
print(ts)
# Definir las fuentes disponibles
sources = {
    "26ede568-1f3f-4a26-9755-37dc36131112": {
        "file": "./datos/tvom/dashboard.xlsx",
        "file2": "./datos/tvom/dashboard_head.xlsx",
        "file3": f"./datos/tvom/imag/{legajo}.jpg",
        "file4": "./datos/solbayres/dashboard_incidentes.xlsx",
        "file5": "./datos/tvom/bandas_salariales.xlsx",
        "capaweb": True,
        "headcount": True,
        "headcount_2": False,
        "foto": True,
        "smedico": True,
        "bandas": True,
    },
    "2141b1d6-8705-4a95-b0e6-b4c63bdec8a1": {
        "file": "socotherm/dashboard.xlsx",
        "file2": "socotherm/dashboard_head.xlsx",
        "file3": "./datos/socotherm/dashboard_head.xlsx",
        "file4": "./datos/socotherm/dashboard_head.xlsx",
        "file5": "./datos/socotherm/dashboard_head.xlsx",
        "capaweb": False,
        "headcount": False,
        "headcount_2": False,
        "headcount_soco": True,
        "foto": False,
        "smedico": False,
        "bandas": False,
    },
    "2141X1d6-8705-4a91-b0e6-b4c62bdIc8a9": {
        "file": "./datos/lilas/dashboard.xlsx",
        "file2": "./datos/lilas/dashboard_head.xlsx",        
        "file3": f"./datos/lilas/imag/{legajo}.jpg",
        "file4": "./datos/lilas/dashboard_incidentes.xlsx",
        "file5": "./datos/lilas/bandas_salariales.xlsx",
        "capaweb": False,
        "headcount": False,   # version con Unidad Operativa y Departamento
        "headcount_2": True,  # Version con Sector 
        "foto": False,
        "smedico": False,
        "bandas": False,
    },
}

# Validar si el parámetro `visualization` está en las fuentes
if visualization not in sources:
    st.error("El parámetro 'visualization' no es válido.")
#    st.error("Tiempo acabado")
    
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
    if config["headcount_2"]:
        available_modules.append("Dotación")                    
    if config["headcount_soco"]:
        available_modules.append("HeadCount Dotación")
        
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
    # Socotherm    
    elif selected_module == "HeadCount Dotación":
        #st.subheader("Módulo: HeadCount")
        
        headcount_soco.run(file_path_head)  # Delegar al módulo `headcount`
       
    elif selected_module == "Actualiza tus datos":
        #st.subheader("Módulo: HeadCount")
        foto.run(file_path_foto)  # Delegar al módulo `foto`
    elif selected_module == "Servicio Médico":
        incidentes.run(file_path_incid)  # Delegar al módulo de incidentes
    elif selected_module == "Bandas Salariales":
        bandas.run(file_path_bandas)  # Delegar al módulo de Bandas Salariales
    elif selected_module == "Dotación":
        #st.subheader("Módulo: Dotación")
        headcount_2.run(file_path_head)  # Delegar al módulo `headcount`        
            
        
