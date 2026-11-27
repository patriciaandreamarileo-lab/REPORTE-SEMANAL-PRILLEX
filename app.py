import streamlit as st

from modules.navegacion import configurar_navegacion


# =====================================================
# 1. CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="Dashboard de Gestión | PRILLEX",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

configurar_navegacion()


# =====================================================
# 2. ESTILOS GENERALES
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FB;
}

.main-title {
    color: #173F63;
    font-size: 34px;
    font-weight: 750;
    margin-bottom: 5px;
}

.main-description {
    color: #64748B;
    font-size: 16px;
    margin-bottom: 25px;
}

.welcome-card {
    background: linear-gradient(110deg, #123454, #24669A);
    padding: 35px;
    border-radius: 16px;
    margin-top: 20px;
    margin-bottom: 25px;
    color: white;
}

.welcome-card h2 {
    color: white;
    font-size: 30px;
    margin-bottom: 10px;
}

.welcome-card p {
    color: #DCEAF7;
    font-size: 16px;
    margin-bottom: 0;
}

div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    padding: 18px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. ENCABEZADO
# =====================================================

st.markdown(
    '<div class="main-title">Dashboard de Gestión de Materias Primas</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-description">'
    'Herramienta de consulta y seguimiento de la gestión '
    'de materias primas de Enaex Chile.'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# 4. IDENTIFICACIÓN DE LA PLANTA
# =====================================================

st.markdown("""
<div class="welcome-card">

    <div style="
        font-size:13px;
        font-weight:bold;
        letter-spacing:2px;
        color:#DCEAF7;
    ">
        ANÁLISIS INDIVIDUAL
    </div>

    <h2>PRILLEX</h2>

    <p>
        Mejillones | Enaex Chile | Centro SAP E002
    </p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# 5. DESCRIPCIÓN DEL DASHBOARD
# =====================================================

st.subheader("Módulos de consulta")

st.markdown(
    "Selecciona una de las secciones disponibles en el "
    "menú lateral para consultar la información de la planta."
)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 🏭 Análisis por planta")
        st.write(
            "Consulta el nivel de servicio, stock actual, "
            "coberturas y planificación de materias primas."
        )

with col2:
    with st.container(border=True):
        st.markdown("### 📊 Consumo promedio")
        st.write(
            "Revisa el comportamiento histórico del consumo "
            "y su evolución mensual."
        )

with col3:
    with st.container(border=True):
        st.markdown("### 📈 Evolución de precios")
        st.write(
            "Analiza los precios de compra, sus variaciones "
            "y el comportamiento histórico por materia prima."
        )


# =====================================================
# 6. PIE DE PÁGINA
# =====================================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#8492A6;
    font-size:12px;
    padding:15px;
">
    ENAEX CHILE | PRILLEX | CENTRO E002
    <br>
    Dashboard de gestión de materias primas
</div>
""", unsafe_allow_html=True)

