
import streamlit as st

from modules.navegacion import configurar_navegacion


st.set_page_config(
    page_title="Dashboard de Gestión | PRILLEX",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* Fondo azul del menú lateral */
[data-testid="stSidebar"] {
    background-color: #245A91;
}

/* Textos e iconos blancos */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stIcon"],
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] a {
    color: white !important;
}

/* Elemento seleccionado */
[data-testid="stSidebar"] [aria-current="page"] {
    background-color: #E6EFF9 !important;
    border-radius: 8px;
}

[data-testid="stSidebar"] [aria-current="page"] span {
    color: #173B65 !important;
    font-weight: 700;
}

/* Efecto al pasar el cursor */
[data-testid="stSidebar"] a:hover {
    background-color: rgba(255,255,255,0.15);
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


configurar_navegacion()

