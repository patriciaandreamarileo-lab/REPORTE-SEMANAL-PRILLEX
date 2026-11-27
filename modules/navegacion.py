
import streamlit as st


def configurar_navegacion():

    # =================================================
    # ESTILO DEL PANEL LATERAL
    # =================================================

    st.markdown("""
    <style>

    /* Fondo del panel */
    [data-testid="stSidebar"] {
        background-color: #102D49;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #102D49;
    }

    /* Textos generales */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #FFFFFF;
    }

    /* Encabezado */
    .sidebar-titulo {
        color: white;
        font-size: 27px;
        font-weight: 750;
        margin-top: 5px;
        margin-bottom: 22px;
    }

    .sidebar-subtitulo {
        color: #A8B8C8;
        font-size: 16px;
        margin-bottom: 60px;
    }

    .sidebar-seccion {
        color: white;
        font-size: 20px;
        font-weight: 700;
        margin-top: 45px;
        margin-bottom: 12px;
    }

    .sidebar-footer {
        color: #A8B8C8;
        font-size: 15px;
        font-weight: 600;
        margin-top: 45px;
    }

    /* Separadores */
    .sidebar-linea {
        border-top: 1px solid #A8B8C8;
        margin-top: 25px;
        margin-bottom: 25px;
    }

    /* Enlaces de navegación */
    [data-testid="stSidebarNav"] {
        background-color: transparent;
    }

    [data-testid="stSidebarNav"] a {
        color: white !important;
        border-radius: 9px;
        margin-bottom: 5px;
    }

    [data-testid="stSidebarNav"] a span {
        color: white !important;
    }

    /* Elemento seleccionado */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #29445D !important;
        border-radius: 9px;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: white !important;
        font-weight: 700;
    }

    /* Hover */
    [data-testid="stSidebarNav"] a:hover {
        background-color: #29445D !important;
    }

    /* Ocultar elementos automáticos innecesarios */
    [data-testid="stSidebarNavSeparator"] {
        display: none;
    }

    </style>
    """, unsafe_allow_html=True)


    # =================================================
    # ENCABEZADO DEL PANEL
    # =================================================

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-titulo">ENAEX CHILE</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sidebar-subtitulo">'
            'Gestión de materias primas'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sidebar-linea"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sidebar-seccion">NAVEGACIÓN</div>',
            unsafe_allow_html=True
        )


    # =================================================
    # PÁGINAS
    # =================================================

    paginas = [

        st.Page(
            "pages/0_Inicio.py",
            title="Inicio",
            icon="🏠",
            default=True
        ),

        st.Page(
            "pages/1_Analisis_por_planta.py",
            title="Análisis por planta",
            icon="🏭"
        ),

        st.Page(
            "pages/2_Consumo_promedio.py",
            title="Consumo promedio",
            icon="📊"
        ),

        st.Page(
            "pages/3_Evolucion_de_precios.py",
            title="Evolución de precios",
            icon="📈"
        ),

        st.Page(
            "pages/4_Administracion.py",
            title="Administración",
            icon="🔐"
        )

    ]


    navegacion = st.navigation(
        paginas,
        position="sidebar"
    )

    navegacion.run()

