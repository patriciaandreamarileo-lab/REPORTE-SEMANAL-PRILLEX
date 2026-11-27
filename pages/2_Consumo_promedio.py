import streamlit as st
import pandas as pd
import plotly.express as px

from io import BytesIO
from datetime import datetime, date
from openpyxl import load_workbook
from modules.github_storage import gh_leer


# =====================================================
# 1. CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="Consumo mensual | PRILLEX",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

RUTA_CONSUMO = "data/CONSUMO/consumo_prillex.xlsx"
RUTA_MRP = "data/MRP/Planificacion_MRP.xlsm"
CENTRO_PRILLEX = "E002"


# =====================================================
# 2. ESTILOS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FB;
}

.descripcion {
    color: #64748B;
    font-size: 16px;
    margin-bottom: 20px;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #E2E8F0;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. CARGAR ARCHIVO DE CONSUMO DESDE GITHUB
# =====================================================

@st.cache_data(ttl=300)
def cargar_consumo():

    contenido = gh_leer(RUTA_CONSUMO)

    if contenido is None:
        raise Exception(
            "No se encontró el archivo de consumo mensual de PRILLEX en GitHub."
        )

    df = pd.read_excel(
        BytesIO(contenido),
        sheet_name="Data",
        engine="openpyxl"
    )

    return df


# =====================================================
# 3.1 CARGAR INFORMACIÓN DE STOCK Y CONSUMO DEL MRP
# =====================================================

@st.cache_data(ttl=300)
def cargar_datos_mrp():

    """
    Lee la hoja MRP del archivo XLSM almacenado en GitHub.

    Obtiene:
    - Stock Actual: columna W.
    - Consumo acumulado: fila Cons. Acu.
    - Mes de actualización: fecha de la fila 6.
    """

    contenido = gh_leer(RUTA_MRP)

    if contenido is None:
        raise Exception(
            "No se encontró el archivo MRP de PRILLEX en GitHub."
        )

    libro = load_workbook(
        BytesIO(contenido),
        data_only=True,
        read_only=True
    )

    try:

        if "MRP" not in libro.sheetnames:
            raise Exception(
                "No se encontró la hoja 'MRP' dentro del archivo XLSM."
            )

        hoja = libro["MRP"]

        # -------------------------------------------------
        # IDENTIFICAR FECHA DE ACTUALIZACIÓN
        # -------------------------------------------------

        fechas_actualizacion = [
            valor
            for valor in next(
                hoja.iter_rows(
                    min_row=6,
                    max_row=6,
                    values_only=True
                )
            )
            if isinstance(valor, (datetime, date))
        ]

        if not fechas_actualizacion:
            raise Exception(
                "No se encontró la fecha de actualización del MRP en la fila 6."
            )

        fecha_actualizacion = max(fechas_actualizacion)

        mes_actualizacion = (
            fecha_actualizacion.year,
            fecha_actualizacion.month
        )

        # -------------------------------------------------
        # IDENTIFICAR COLUMNA DEL MES ACTUAL
        # -------------------------------------------------

        encabezados = next(
            hoja.iter_rows(
                min_row=8,
                max_row=8,
                values_only=True
            )
        )

        columna_mes = None

        for indice, valor in enumerate(encabezados, start=1):

            if isinstance(valor, (datetime, date)):

                if (
                    valor.year,
                    valor.month
                ) == mes_actualizacion:

                    columna_mes = indice
                    break

        if columna_mes is None:
            raise Exception(
                "No se encontró una columna mensual que coincida "
                "con la fecha de actualización del MRP."
            )

        # -------------------------------------------------
        # LEER MATERIAS PRIMAS
        # -------------------------------------------------

        resultados = {}

        # Estructura de la hoja MRP:
        #
        # A  = Centro
        # B  = Material
        # D  = UM
        # W  = Stock Actual
        # AA = Tipo de fila (Cons. Proy, Cons. Acu, etc.)
        # AB en adelante = Valores mensuales

        for fila in hoja.iter_rows(
            min_row=9,
            max_col=max(27, columna_mes),
            values_only=True
        ):

            centro = str(
                fila[0] or ""
            ).strip().upper()

            if centro != CENTRO_PRILLEX:
                continue

            material = fila[1]

            if material is None:
                continue

            if isinstance(material, float) and material.is_integer():
                codigo = str(int(material))
            else:
                codigo = str(material).strip()

            if codigo.endswith(".0"):
                codigo = codigo[:-2]

            unidad = str(
                fila[3] or ""
            ).strip()

            stock_actual = (
                fila[22]
                if len(fila) > 22
                else None
            )

            tipo_fila = str(
                fila[26]
                if len(fila) > 26 and fila[26] is not None
                else ""
            ).strip().upper()

            tipo_normalizado = (
                tipo_fila
                .replace(".", "")
                .replace(" ", "")
            )

            if codigo not in resultados:

                resultados[codigo] = {
                    "stock_actual": None,
                    "consumo_acumulado": None,
                    "unidad": unidad
                }

            # ---------------------------------------------
            # STOCK ACTUAL
            # ---------------------------------------------

            if stock_actual is not None:

                try:

                    valor_stock = float(stock_actual)

                    if resultados[codigo]["stock_actual"] is None:

                        resultados[codigo]["stock_actual"] = valor_stock

                except (TypeError, ValueError):
                    pass

            # ---------------------------------------------
            # CONSUMO ACUMULADO
            # ---------------------------------------------

            if tipo_normalizado == "CONSACU":

                valor_consumo = (
                    fila[columna_mes - 1]
                    if len(fila) >= columna_mes
                    else None
                )

                if valor_consumo is not None:

                    try:

                        resultados[codigo]["consumo_acumulado"] = float(
                            valor_consumo
                        )

                    except (TypeError, ValueError):
                        pass

                if unidad:
                    resultados[codigo]["unidad"] = unidad

        return (
            resultados,
            fecha_actualizacion.strftime("%d/%m/%Y")
        )

    finally:

        libro.close()


# =====================================================
# 3.2 OBTENER DATOS DEL MATERIAL SELECCIONADO
# =====================================================

def obtener_datos_mrp_material(codigo_material):

    """
    Devuelve:
    - Stock actual.
    - Consumo acumulado.
    - Unidad de medida.
    - Fecha de actualización del MRP.
    """

    datos_mrp, fecha_mrp = cargar_datos_mrp()

    codigo = str(codigo_material).strip()

    if codigo.endswith(".0"):
        codigo = codigo[:-2]

    informacion = datos_mrp.get(codigo)

    if informacion is None:

        return None, None, None, fecha_mrp

    return (
        informacion.get("stock_actual"),
        informacion.get("consumo_acumulado"),
        informacion.get("unidad"),
        fecha_mrp
    )


# =====================================================
# 4. ACTUALIZACIÓN MANUAL
# =====================================================

col_actualizar, col_estado = st.columns([1, 3])

with col_actualizar:

    if st.button(
        "🔄 Actualizar datos",
        use_container_width=True
    ):

        cargar_consumo.clear()
        cargar_datos_mrp.clear()

        st.rerun()


# =====================================================
# 5. OBTENER INFORMACIÓN
# =====================================================

try:

    datos_originales = cargar_consumo()

    if datos_originales.empty:

        st.error(
            "El archivo de consumo no contiene registros."
        )

        st.stop()

except Exception as error:

    st.error(
        f"No fue posible cargar el archivo de consumo: {error}"
    )

    st.stop()


# =====================================================
# 6. VALIDAR COLUMNAS
# =====================================================

columnas_requeridas = [
    "Material",
    "Centro",
    "Clase de movimiento",
    "Ctd.en UM entrada",
    "Fecha contabiliz."
]

faltantes = [
    columna
    for columna in columnas_requeridas
    if columna not in datos_originales.columns
]

if faltantes:

    st.error(
        "Faltan columnas necesarias en el archivo: "
        + ", ".join(faltantes)
    )

    st.stop()


# =====================================================
# 7. LIMPIEZA DE DATOS
# =====================================================

datos = datos_originales.copy()

# Limpiar códigos de materiales

datos["Material"] = (
    datos["Material"]
    .astype(str)
    .str.strip()
    .str.replace(r"\.0$", "", regex=True)
)

# Limpiar centro

datos["Centro"] = (
    datos["Centro"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Filtrar PRILLEX

datos = datos[
    datos["Centro"] == CENTRO_PRILLEX
].copy()

if datos.empty:

    st.error(
        "No se encontraron registros correspondientes "
        "al centro E002 (PRILLEX)."
    )

    st.stop()


# Normalizar clases de movimiento

datos["Clase de movimiento"] = (
    datos["Clase de movimiento"]
    .astype(str)
    .str.replace(r"\.0$", "", regex=True)
    .str.strip()
)

# Considerar exclusivamente movimientos 261 y 262

datos = datos[
    datos["Clase de movimiento"].isin(["261", "262"])
].copy()

# Convertir cantidades

datos["Ctd.en UM entrada"] = pd.to_numeric(
    datos["Ctd.en UM entrada"],
    errors="coerce"
).fillna(0)

# Convertir fechas

datos["Fecha contabiliz."] = pd.to_datetime(
    datos["Fecha contabiliz."],
    errors="coerce",
    dayfirst=True
)

datos = datos.dropna(
    subset=["Fecha contabiliz."]
).copy()

# Limpiar descripciones

if "Descripción material" in datos.columns:

    datos["Descripción material"] = (
        datos["Descripción material"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

else:

    datos["Descripción material"] = ""

# Limpiar unidad de medida

if "Un.medida de entrada" not in datos.columns:

    datos["Un.medida de entrada"] = "Sin unidad"

datos["Un.medida de entrada"] = (
    datos["Un.medida de entrada"]
    .fillna("Sin unidad")
    .astype(str)
    .str.strip()
)


# =====================================================
# 8. CATÁLOGO DE MATERIAS PRIMAS
# =====================================================

catalogo = (
    datos[
        ["Material", "Descripción material"]
    ]
    .drop_duplicates(subset=["Material"])
    .sort_values("Material")
    .copy()
)

catalogo["Descripción material"] = (
    catalogo["Descripción material"]
    .replace("", "Sin descripción")
)

if catalogo.empty:

    st.warning(
        "No existen materias primas para consultar."
    )

    st.stop()


# =====================================================
# 9. ENCABEZADO
# =====================================================

st.title("Consumo mensual de materias primas")

st.markdown(
    "Análisis histórico de los movimientos y consumo "
    "de materias primas de PRILLEX."
)

encabezado_html = (
    '<div style="background:linear-gradient(110deg,#153653 0%,#286B9B 100%);'
    'padding:35px;border-radius:16px;margin-top:20px;margin-bottom:25px;">'
    '<div style="font-size:13px;font-weight:bold;color:#FFFFFF;letter-spacing:2px;">'
    'ANÁLISIS INDIVIDUAL'
    '</div>'
    '<div style="font-size:34px;font-weight:750;color:#FFFFFF;margin-top:20px;">'
    'PRILLEX'
    '</div>'
    '<div style="font-size:17px;color:#FFFFFF;margin-top:20px;">'
    'Mejillones | Enaex Chile | Centro E002'
    '</div>'
    '</div>'
)

st.markdown(
    encabezado_html,
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# 10. BUSCADOR Y SELECTOR DE MATERIAS PRIMAS
# =====================================================

st.subheader("Selección de materia prima")

st.markdown(
    "Busca una materia prima por su código SAP "
    "o por su descripción."
)

busqueda = st.text_input(
    "Buscar material",
    placeholder="Escribe un código o nombre de material...",
    key="busqueda_consumo"
)

catalogo_filtrado = catalogo.copy()

if busqueda.strip():

    termino = busqueda.strip().lower()

    catalogo_filtrado = catalogo[
        catalogo["Material"].str.lower().str.contains(
            termino,
            na=False
        )
        |
        catalogo["Descripción material"].str.lower().str.contains(
            termino,
            na=False
        )
    ].copy()


if catalogo_filtrado.empty:

    st.warning(
        "No se encontraron materias primas con esa búsqueda."
    )

    st.stop()


opciones_materiales = [
    (
        str(fila["Material"]),
        str(fila["Descripción material"])
    )
    for _, fila in catalogo_filtrado.iterrows()
]

seleccion = st.selectbox(
    "Seleccionar materia prima",
    options=opciones_materiales,
    format_func=lambda material: (
        f"{material[0]} -- {material[1]}"
    ),
    key="selector_consumo_prillex"
)

codigo_seleccionado = seleccion[0]
descripcion_seleccionada = seleccion[1]


# =====================================================
# 11. FILTRAR MOVIMIENTOS DEL MATERIAL
# =====================================================

datos_material = datos[
    datos["Material"] == codigo_seleccionado
].copy()

if datos_material.empty:

    st.info(
        "No existen movimientos para esta materia prima."
    )

    st.stop()


st.write("")

st.markdown(
    f"### {descripcion_seleccionada}"
)

st.caption(
    f"Código SAP: {codigo_seleccionado}"
)


# =====================================================
# 12. UNIDAD DE MEDIDA
# =====================================================

unidades = sorted(
    datos_material["Un.medida de entrada"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

if len(unidades) > 1:

    st.warning(
        "Este material presenta más de una unidad de medida. "
        "Selecciona una para evitar sumar cantidades incompatibles."
    )

    unidad_seleccionada = st.selectbox(
        "Unidad de medida",
        options=unidades,
        key="unidad_consumo"
    )

    datos_material = datos_material[
        datos_material["Un.medida de entrada"]
        == unidad_seleccionada
    ].copy()

else:

    unidad_seleccionada = (
        unidades[0]
        if unidades
        else "Sin unidad"
    )


# =====================================================
# 13. CALCULAR CONSUMO MENSUAL
# =====================================================

datos_material["Mes"] = (
    datos_material["Fecha contabiliz."]
    .dt.to_period("M")
)

# Se conserva el signo original de SAP.
# 261 normalmente registra cantidades negativas.
# 262 registra anulaciones positivas.
# El negativo de la suma representa el consumo neto.

consumo_mensual = (
    datos_material
    .groupby("Mes", as_index=False)
    .agg(
        Cantidad_SAP=("Ctd.en UM entrada", "sum"),
        Movimientos=("Clase de movimiento", "count")
    )
)

consumo_mensual["Consumo"] = (
    -consumo_mensual["Cantidad_SAP"]
)

consumo_mensual["Fecha"] = (
    consumo_mensual["Mes"]
    .dt.to_timestamp()
)

consumo_mensual = consumo_mensual.sort_values("Fecha")


# =====================================================
# 14. INDICADORES DEL MATERIAL
# =====================================================

# Los dos primeros indicadores se obtienen directamente
# de la hoja MRP del Excel:
#
# - Stock Actual: columna W de la fila principal.
# - Consumo real a la fecha: fila Cons. Acu.
#   en la columna correspondiente al mes de actualización.
#
# El tercer indicador se mantiene desde los movimientos SAP.

cantidad_movimientos = len(datos_material)

try:

    (
        stock_actual_mrp,
        consumo_acumulado_mrp,
        unidad_mrp,
        fecha_mrp
    ) = obtener_datos_mrp_material(codigo_seleccionado)

except Exception as error:

    stock_actual_mrp = None
    consumo_acumulado_mrp = None
    unidad_mrp = None
    fecha_mrp = None

    st.warning(
        f"No fue posible obtener el stock y el consumo acumulado "
        f"desde el MRP: {error}"
    )


unidad_mostrar = (
    unidad_mrp
    if unidad_mrp and unidad_mrp != "None"
    else unidad_seleccionada
)

col1, col2, col3 = st.columns(3)


# -----------------------------------------------------
# PRIMERA TARJETA: STOCK ACTUAL
# -----------------------------------------------------

if stock_actual_mrp is not None:

    col1.metric(
        "Stock actual",
        f"{stock_actual_mrp:,.2f} {unidad_mostrar}"
    )

else:

    col1.metric(
        "Stock actual",
        "No disponible"
    )


# -----------------------------------------------------
# SEGUNDA TARJETA: CONSUMO REAL A LA FECHA
# -----------------------------------------------------

if consumo_acumulado_mrp is not None:

    col2.metric(
        "Consumo real a la fecha",
        f"{consumo_acumulado_mrp:,.2f} {unidad_mostrar}"
    )

else:

    col2.metric(
        "Consumo real a la fecha",
        "No disponible"
    )


# -----------------------------------------------------
# TERCERA TARJETA: MOVIMIENTOS SAP
# -----------------------------------------------------

col3.metric(
    "Movimientos SAP",
    f"{cantidad_movimientos:,}"
)


if fecha_mrp:

    st.caption(
        f"Stock y consumo acumulado obtenidos del MRP "
        f"actualizado al {fecha_mrp}. El consumo corresponde "
        f"al valor de la fila 'Cons. Acu.' en el mes de actualización."
    )


st.divider()


# =====================================================
# 15. GRÁFICO DE CONSUMO MENSUAL
# =====================================================

st.subheader("Evolución del consumo mensual")

st.markdown(
    "Consumo neto mensual calculado a partir de "
    "los movimientos SAP 261 y 262."
)

if not consumo_mensual.empty:

    fig = px.line(
        consumo_mensual,
        x="Fecha",
        y="Consumo",
        markers=True,
        custom_data=["Movimientos"],
        labels={
            "Fecha": "Mes",
            "Consumo": f"Consumo ({unidad_seleccionada})"
        }
    )

    fig.update_traces(
        line=dict(
            color="#245A91",
            width=3
        ),
        marker=dict(
            size=9,
            color="#078BCE"
        ),
        hovertemplate=(
            "<b>%{x|%B %Y}</b><br>"
            "Consumo: %{y:,.2f}<br>"
            "Movimientos: %{customdata[0]}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        height=430,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(
            t=25,
            b=30,
            l=20,
            r=20
        ),
        xaxis=dict(
            tickformat="%b %Y",
            title="Mes",
            showgrid=False
        ),
        yaxis=dict(
            title=f"Consumo ({unidad_seleccionada})",
            gridcolor="#E2E8F0",
            zeroline=True
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No existen datos para construir el gráfico."
    )


st.divider()


# =====================================================
# 16. TABLA DE MOVIMIENTOS SAP
# =====================================================

st.subheader("Detalle de movimientos SAP")

st.markdown(
    "Movimientos de consumo y anulaciones registrados "
    "para la materia prima seleccionada."
)

columnas_tabla = [
    "Fecha contabiliz.",
    "Material",
    "Descripción material",
    "Clase de movimiento",
    "Documento material",
    "Pedido",
    "Lote",
    "Ctd.en UM entrada",
    "Un.medida de entrada",
    "Texto clase de mov."
]

columnas_disponibles = [
    columna
    for columna in columnas_tabla
    if columna in datos_material.columns
]

movimientos = (
    datos_material[columnas_disponibles]
    .sort_values(
        "Fecha contabiliz.",
        ascending=False
    )
    .copy()
)

st.dataframe(
    movimientos,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Fecha contabiliz.": st.column_config.DateColumn(
            "Fecha",
            format="DD/MM/YYYY"
        ),
        "Ctd.en UM entrada": st.column_config.NumberColumn(
            "Cantidad SAP",
            format="%.3f"
        )
    }
)

st.caption(
    "Las cantidades de esta tabla mantienen el signo original "
    "registrado en SAP."
)


st.divider()



# =====================================================
# 17. PROYECCIÓN DE CONSUMO CON PROMEDIO MÓVIL
# =====================================================

st.subheader("Proyección de consumo")

st.markdown(
    "La proyección se calcula mediante un promedio móvil "
    "de los últimos tres meses. Cada nuevo mes proyectado "
    "considera los dos meses anteriores y el último valor "
    "proyectado, cuando corresponda."
)

if len(consumo_mensual) >= 3:

    # -------------------------------------------------
    # 1. ORDENAR LOS CONSUMOS REALES
    # -------------------------------------------------

    reales = (
        consumo_mensual[
            ["Mes", "Fecha", "Consumo"]
        ]
        .sort_values("Mes")
        .copy()
    )

    # Último mes real disponible
    ultimo_mes = reales["Mes"].max()

    # Últimos tres meses reales
    ultimos_tres = reales.tail(3)

    # -------------------------------------------------
    # 2. CALCULAR PROYECCIÓN CON PROMEDIO MÓVIL
    # -------------------------------------------------

    # Guardar los valores reales y proyectados.
    # Cada nueva proyección se incorpora a esta lista.

    historial_consumo = reales["Consumo"].tolist()

    proyecciones = []

    # Proyectar los siguientes tres meses
    for i in range(1, 4):

        # Tomar los últimos tres valores disponibles
        ultimos_valores = historial_consumo[-3:]

        # Calcular promedio móvil
        promedio_movil = sum(ultimos_valores) / 3

        # Calcular mes proyectado
        mes_proyectado = ultimo_mes + i

        fecha_proyectada = mes_proyectado.to_timestamp()

        # Guardar resultado
        proyecciones.append({
            "Mes": mes_proyectado,
            "Fecha": fecha_proyectada,
            "Consumo": promedio_movil,
            "Tipo": "Proyección"
        })

        # Incorporar la proyección al historial
        # para calcular el siguiente mes
        historial_consumo.append(promedio_movil)

    datos_futuros = pd.DataFrame(proyecciones)

    # -------------------------------------------------
    # 3. PREPARAR SERIE REAL
    # -------------------------------------------------

    reales_grafico = reales[
        ["Fecha", "Consumo"]
    ].copy()

    reales_grafico["Tipo"] = "Consumo real"

    # -------------------------------------------------
    # 4. PREPARAR SERIE PROYECTADA
    # -------------------------------------------------

    # Incorporar el último punto real a la proyección.
    # Esto permite que ambas líneas se unan exactamente
    # sin perder sus respectivos colores.

    punto_union = pd.DataFrame({
        "Fecha": [reales.iloc[-1]["Fecha"]],
        "Consumo": [reales.iloc[-1]["Consumo"]],
        "Tipo": ["Proyección"]
    })

    proyeccion_grafico = pd.concat(
        [
            punto_union,
            datos_futuros[["Fecha", "Consumo", "Tipo"]]
        ],
        ignore_index=True
    )

    # -------------------------------------------------
    # 5. CREAR GRÁFICO
    # -------------------------------------------------

    import plotly.graph_objects as go

    fig_proyeccion = go.Figure()

    # Línea de consumo real
    fig_proyeccion.add_trace(
        go.Scatter(
            x=reales_grafico["Fecha"],
            y=reales_grafico["Consumo"],
            mode="lines+markers",
            name="Consumo real",
            line=dict(
                color="#245A91",
                width=3
            ),
            marker=dict(
                size=8,
                color="#245A91"
            ),
            hovertemplate=(
                "<b>%{x|%B %Y}</b><br>"
                "Consumo real: %{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    # Línea de proyección
    fig_proyeccion.add_trace(
        go.Scatter(
            x=proyeccion_grafico["Fecha"],
            y=proyeccion_grafico["Consumo"],
            mode="lines+markers",
            name="Proyección",
            line=dict(
                color="#E58A26",
                width=3
            ),
            marker=dict(
                size=8,
                color="#E58A26"
            ),
            hovertemplate=(
                "<b>%{x|%B %Y}</b><br>"
                "Consumo proyectado: %{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    # -------------------------------------------------
    # 6. CONFIGURACIÓN VISUAL
    # -------------------------------------------------

    fig_proyeccion.update_layout(
        height=450,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(
            t=25,
            b=30,
            l=20,
            r=20
        ),
        xaxis=dict(
            tickformat="%b %Y",
            title="Mes",
            showgrid=False
        ),
        yaxis=dict(
            title=f"Consumo ({unidad_seleccionada})",
            gridcolor="#E2E8F0"
        ),
        legend_title_text="",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_proyeccion,
        use_container_width=True
    )

    # -------------------------------------------------
    # 7. MOSTRAR DETALLE DE LA PROYECCIÓN
    # -------------------------------------------------

    st.markdown("### Detalle del promedio móvil")

    detalle_proyeccion = datos_futuros.copy()

    detalle_proyeccion["Mes"] = (
        detalle_proyeccion["Mes"]
        .dt.strftime("%B %Y")
    )

    detalle_proyeccion["Consumo proyectado"] = (
        detalle_proyeccion["Consumo"]
        .round(2)
    )

    detalle_proyeccion = detalle_proyeccion[
        ["Mes", "Consumo proyectado"]
    ]

    st.dataframe(
        detalle_proyeccion,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "La proyección utiliza un promedio móvil de tres meses. "
        "A partir del segundo mes proyectado, se incorporan "
        "los valores estimados de los meses anteriores."
    )

else:

    st.info(
        "Se necesitan al menos tres meses de consumo "
        "registrado para generar la proyección mediante "
        "promedio móvil."
    )

# =====================================================
# 18. PIE DE PÁGINA
# =====================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#8492A6;
        font-size:12px;
        margin-top:45px;
        padding:15px;
    ">
        ENAEX CHILE | ANÁLISIS DE CONSUMO DE MATERIAS PRIMAS
        | PRILLEX | CENTRO E002
    </div>
    """,
    unsafe_allow_html=True
)
