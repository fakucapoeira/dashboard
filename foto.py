import streamlit as st

def run(file_path_foto):
    # Configurar la página de Streamlit

    # Encabezado principal
    st.title("📸 Actualiza tu foto")
    st.write("Carga una imagen desde tu dispositivo")

    # Opciones de entrada
    uploaded_file = st.file_uploader("Sube tu foto (formatos permitidos: JPG o PNG):", type=["jpg", "png"])
    #camera_photo = st.camera_input("O toma una foto usando tu cámara:")

    # Manejo de entrada
    if uploaded_file:
        st.image(uploaded_file, caption=file_path_foto, use_column_width=True)
        with open(file_path_foto, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Tu foto se ha cargado correctamente")

    #elif camera_photo:
    #    st.image(camera_photo, caption="Foto tomada", use_column_width=True)
    #    with open("foto_tomada.jpg", "wb") as f:
     #       f.write(camera_photo.getbuffer())
     #   st.success("✅ Tu foto fue tomada correctamente y guardada como `foto_tomada.jpg`.")

    else:
        st.info("Por favor, sube una foto")

    # Información adicional para resolución de problemas
    #st.write("---")
    #st.write("Si el botón para tomar una foto no funciona:")
    #st.markdown("""
    #1. Verifica que el navegador tenga permiso para usar la cámara.
    #2. Usa un navegador compatible como **Google Chrome** o **Microsoft Edge**.
    #3. Asegúrate de estar ejecutando Streamlit en un entorno con acceso a cámara (no en servidores remotos sin soporte multimedia).
    #""")
