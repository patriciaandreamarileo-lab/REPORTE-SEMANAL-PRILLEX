
import streamlit as st

from modules.navegacion import configurar_navegacion


st.set_page_config(
    page_title="Dashboard de Gestión | PRILLEX",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

configurar_navegacion()
