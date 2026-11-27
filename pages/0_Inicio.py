
import streamlit as st

st.title("Dashboard de Gestión | PRILLEX")

st.markdown(
    """
    <div style="
        background:linear-gradient(110deg,#173B65,#245A91);
        padding:32px;
        border-radius:14px;
        margin-bottom:25px;
    ">
        <div style="
            color:#DCEAF8;
            font-size:14px;
            font-weight:600;
            letter-spacing:1.5px;
        ">
            ENAEX CHILE
        </div>
        <div style="
            color:white;
            font-size:34px;
            font-weight:700;
            margin-top:8px;
        ">
            PRILLEX
        </div>
        <div style="
            color:#DCEAF8;
            font-size:16px;
            margin-top:8px;
        ">
            Mejillones | Centro SAP E002
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Panel de gestión de materias primas")

st.markdown(
    "Selecciona una sección del menú lateral para consultar "
    "la información y los indicadores de la planta."
)

col1, col2 = st.columns(2)

with col1:
    st.info(
        "**📊 Análisis por planta**\n\n"
        "Consulta el nivel de servicio, inventarios, "
        "coberturas y alertas de materias primas."
    )

    st.info(
        "**📦 Consumo promedio**\n\n"
        "Revisa los movimientos históricos y el consumo "
        "promedio mensual de los materiales."
    )

with col2:
    st.info(
        "**📈 Evolución de precios**\n\n"
        "Analiza los precios históricos de compra "
        "y sus variaciones por materia prima."
    )

    st.info(
        "**🔒 Administración**\n\n"
        "Actualiza los archivos MRP, consumo y precios "
        "del dashboard."
    )

st.markdown(
    """
    <div style="
        text-align:center;
        color:#8492A6;
        font-size:12px;
        margin-top:50px;
        padding:15px;
    ">
        ENAEX CHILE | PRILLEX | CENTRO E002
    </div>
    """,
    unsafe_allow_html=True
)
