
import streamlit as st

# =====================================================
# 1. CONFIGURACIÓN VISUAL
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #F3F6FA;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

h1 {
    color: #173B65 !important;
}

.tarjeta-titulo {
    color: #173B65;
    font-size: 23px;
    font-weight: 750;
    min-height: 75px;
}

.tarjeta-descripcion {
    color: #64748B;
    font-size: 16px;
    line-height: 1.65;
    min-height: 145px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 2. ENCABEZADO
# =====================================================

st.markdown(
    '<h1 style="font-size:38px;">Panel de control</h1>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        color:#64748B;
        font-size:19px;
        margin-bottom:35px;
    ">
        Selecciona el módulo que deseas consultar para acceder
        a los análisis de materias primas.
    </p>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 3. TARJETAS
# =====================================================

col1, col2, col3 = st.columns(3, gap="large")


# =====================================================
# TARJETA 1: ANÁLISIS POR PLANTA
# =====================================================

with col1:

    with st.container(border=True, height=440):

        st.markdown("## 🏭")

        st.markdown(
            '<div class="tarjeta-titulo">Análisis por planta</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="tarjeta-descripcion">
                Consulta los indicadores de inventario,
                cobertura, nivel de servicio y situación
                de las materias primas de PRILLEX.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.page_link(
            "pages/1_Analisis_por_planta.py",
            label="➡️ Ingresar al análisis"
        )


# =====================================================
# TARJETA 2: CONSUMO PROMEDIO
# =====================================================

with col2:

    with st.container(border=True, height=440):

        st.markdown("## 📊")

        st.markdown(
            '<div class="tarjeta-titulo">Consumo promedio</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="tarjeta-descripcion">
                Analiza el comportamiento histórico del
                consumo, sus variaciones mensuales y las
                tendencias de las materias primas.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.page_link(
            "pages/2_Consumo_promedio.py",
            label="➡️ Ingresar al consumo"
        )


# =====================================================
# TARJETA 3: EVOLUCIÓN DE PRECIOS
# =====================================================

with col3:

    with st.container(border=True, height=440):

        st.markdown("## 📈")

        st.markdown(
            '<div class="tarjeta-titulo">Evolución de precios</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="tarjeta-descripcion">
                Visualiza la evolución de los precios de
                compra, las variaciones de las órdenes
                de compra y el comportamiento de los
                proveedores.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.page_link(
            "pages/3_Evolucion_de_precios.py",
            label="➡️ Ingresar a precios"
        )


# =====================================================
# 4. PIE DE PÁGINA
# =====================================================

st.markdown(
    """
    <p style="
        text-align:center;
        color:#8492A6;
        font-size:12px;
        margin-top:45px;
        padding:15px;
    ">
        ENAEX CHILE | PRILLEX | CENTRO E002
    </p>
    """,
    unsafe_allow_html=True
)
