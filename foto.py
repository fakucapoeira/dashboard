import streamlit as st

def run(file_path):
    # Configurar la página de Streamlit
    st.set_page_config(page_title="Actualiza tu foto", layout="centered")

    # Encabezado principal
    st.title("📸 Actualiza tu foto")
    st.write("Carga una imagen desde tu dispositivo o toma una foto directamente con tu cámara.")

    # Opciones de entrada
    uploaded_file = st.file_uploader("Sube tu foto (formatos permitidos: JPG o PNG):", type=["jpg", "png"])
    camera_photo = st.camera_input("O toma una foto usando tu cámara:")

    # Manejo de entrada
    if uploaded_file:
        st.image(uploaded_file, caption="Foto cargada", use_column_width=True)
        with open("foto_subida.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ Tu foto se ha cargado correctamente y fue guardada como `foto_subida.jpg`.")

    elif camera_photo:
        st.image(camera_photo, caption="Foto tomada", use_column_width=True)
        with open("foto_tomada.jpg", "wb") as f:
            f.write(camera_photo.getbuffer())
        st.success("✅ Tu foto fue tomada correctamente y guardada como `foto_tomada.jpg`.")

    else:
        st.info("Por favor, sube una foto o toma una nueva.")

    # Información adicional para resolución de problemas
    st.write("---")
    st.write("Si el botón para tomar una foto no funciona:")
    st.markdown("""
    1. Verifica que el navegador tenga permiso para usar la cámara.
    2. Usa un navegador compatible como **Google Chrome** o **Microsoft Edge**.
    3. Asegúrate de estar ejecutando Streamlit en un entorno con acceso a cámara (no en servidores remotos sin soporte multimedia).
    """)
