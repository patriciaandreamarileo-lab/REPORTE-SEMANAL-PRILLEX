
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

.titulo-panel {
    color: #173B65;
    font-size: 38px;
    font-weight: 750;
    margin-bottom: 5px;
}

.subtitulo-panel {
    color: #64748B;
    font-size: 19px;
    margin-bottom: 35px;
}

.tarjeta {
    background-color: #F3F6FA;
    border: 1px solid #D6DCE5;
    border-radius: 11px;
    padding: 28px 19px 20px 19px;
    min-height: 395px;
    display: flex;
    flex-direction: column;
}

.tarjeta-icono {
    font-size: 43px;
    margin-bottom: 23px;
}

.tarjeta-titulo {
    color: #173B65;
    font-size: 24px;
    font-weight: 750;
    line-height: 1.65;
    min-height: 75px;
    margin-bottom: 15px;
}

.tarjeta-descripcion {
    color: #64748B;
    font-size: 16px;
    line-height: 1.65;
    min-height: 150px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 2. ENCABEZADO
# =====================================================

st.markdown(
    '<div class="titulo-panel">Panel de control</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo-panel">'
    'Selecciona el módulo que deseas consultar para acceder '
    'a los análisis de materias primas.'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# 3. TARJETAS DE LOS MÓDULOS
# =====================================================

col1, col2, col3 = st.columns(3, gap="large")


# -----------------------------------------------------
# TARJETA 1: ANÁLISIS POR PLANTA
# -----------------------------------------------------

with col1:

    st.markdown("""
    <div class="tarjeta">

        <div class="tarjeta-icono">🏭</div>

        <div class="tarjeta-titulo">
            Análisis por<br>planta
        </div>

        <div class="tarjeta-descripcion">
            Consulta los indicadores de inventario,
            cobertura, nivel de servicio y situación
            de las materias primas de PRILLEX.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/1_Analisis_por_planta.py",
        label="➡️ Ingresar al análisis",
        use_container_width=False
    )


# -----------------------------------------------------
# TARJETA 2: CONSUMO PROMEDIO
# -----------------------------------------------------

with col2:

    st.markdown("""
    <div class="tarjeta">

        <div class="tarjeta-icono">📊</div>

        <div class="tarjeta-titulo">
            Consumo<br>promedio
        </div>

        <div class="tarjeta-descripcion">
            Analiza el comportamiento histórico del
            consumo, sus variaciones mensuales y las
            tendencias de las materias primas.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/2_Consumo_promedio.py",
        label="➡️ Ingresar al consumo",
        use_container_width=False
    )


# -----------------------------------------------------
# TARJETA 3: EVOLUCIÓN DE PRECIOS
# -----------------------------------------------------

with col3:

    st.markdown("""
    <div class="tarjeta">

        <div class="tarjeta-icono">📈</div>

        <div class="tarjeta-titulo">
            Evolución de<br>precios
        </div>

        <div class="tarjeta-descripcion">
            Visualiza la evolución de los precios de
            compra, las variaciones de las órdenes
            de compra y el comportamiento de los
            proveedores.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/3_Evolucion_de_precios.py",
        label="➡️ Ingresar a precios",
        use_container_width=False
    )


# =====================================================
# 4. PIE DE PÁGINA
# =====================================================

st.markdown("""
<div style="
    text-align:center;
    color:#8492A6;
    font-size:12px;
    margin-top:55px;
    padding:15px;
">
    ENAEX CHILE | PRILLEX | CENTRO E002
</div>
""", unsafe_allow_html=True)
