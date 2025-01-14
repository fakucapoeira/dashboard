import streamlit as st
import pandas as pd



def run(file_path):
    st.write(f"Procesando el archivo para test: {file_path}")
    df = pd.read_excel(file_path)
    st.dataframe(df.describe())  # Mostrar estadísticas básicas