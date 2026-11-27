
import io
import pandas as pd
import streamlit as st
from openpyxl import load_workbook

from modules.github_storage import gh_leer


RUTA_MRP = "data/MRP/Planificacion_MRP.xlsm"

# La fila 10 contiene los encabezados reales
FILA_ENCABEZADOS = 10

CENTRO_PRILLEX = "E002"

COLUMNAS_MRP = [
    "Centro",
    "Material",
    "Descripción del material",
    "UM",
    "MMPP Activa",
    "Riesgo MMPP",
    "Riesgo",
    "Producto",
    "Concat",
    "Consumo X̄",
    "Stock Actual",
    "Stock Óptimo",
    "Stock Seguridad",
    "Stock Máximo",
    "Prod. saldo m",
    "Cob. [Meses]",
    "Cobertura a [Días]",
    "Sobrestock [%]",
    "NS",
    "NS Corregido",
    "Comentario"
]


# =====================================================
# 1. LIMPIEZA DE TEXTOS
# =====================================================

def limpiar_texto(valor):

    if pd.isna(valor):
        return ""

    return str(valor).strip()


# =====================================================
# 2. LECTURA DEL MRP DESDE GITHUB
# =====================================================

@st.cache_data(ttl=60)
def cargar_mrp():

    contenido = gh_leer(RUTA_MRP)

    if contenido is None:
        raise FileNotFoundError(
            "No se encontró el archivo MRP de PRILLEX en GitHub."
        )

    archivo = io.BytesIO(contenido)

    libro = load_workbook(
        archivo,
        read_only=True,
        data_only=True
    )

    try:

        if "NS" not in libro.sheetnames:
            raise ValueError(
                "No se encontró la hoja NS."
            )

        hoja = libro["NS"]

        # Leer encabezados desde la fila 10
        filas = list(
            hoja.iter_rows(
                min_row=FILA_ENCABEZADOS,
                min_col=1,
                max_col=21,
                values_only=True
            )
        )

        if not filas:
            raise ValueError(
                "La hoja NS está vacía."
            )

        encabezados_excel = [
            limpiar_texto(valor)
            for valor in filas[0]
        ]

        # Validar estructura de las columnas
        if encabezados_excel[:4] != [
            "Centro",
            "Material",
            "Descripción del material",
            "UM"
        ]:

            raise ValueError(
                "Los encabezados de la hoja NS "
                "no coinciden con la estructura esperada. "
                f"Se encontraron: {encabezados_excel[:4]}"
            )

        # Crear DataFrame
        df = pd.DataFrame(
            filas[1:],
            columns=COLUMNAS_MRP
        )

        # Eliminar filas completamente vacías
        df = df.dropna(how="all").copy()

        # Limpiar columnas de texto
        for columna in df.select_dtypes(
            include=["object"]
        ).columns:

            df[columna] = df[columna].apply(
                limpiar_texto
            )

        # Conservar Centro y Material como texto
        df["Centro"] = (
            df["Centro"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        df["Material"] = (
            df["Material"]
            .astype(str)
            .str.strip()
        )

        # Eliminar registros sin centro o material
        df = df[
            (df["Centro"] != "")
            & (df["Centro"] != "NONE")
            & (df["Material"] != "")
            & (df["Material"] != "NONE")
        ].copy()

        df = df.reset_index(drop=True)

        return df, libro.sheetnames

    finally:
        libro.close()


# =====================================================
# 3. OBTENER TODAS LAS MATERIAS PRIMAS DE PRILLEX
# =====================================================

@st.cache_data(ttl=60)
def obtener_datos_prillex():

    df, _ = cargar_mrp()

    # Identificar exclusivamente el centro E002
    datos_prillex = df[
        df["Centro"].astype(str).str.strip().str.upper()
        == CENTRO_PRILLEX
    ].copy()

    datos_prillex = datos_prillex.reset_index(
        drop=True
    )

    return datos_prillex


# =====================================================
# 4. OBTENER MATERIAS PRIMAS ACTIVAS DE PRILLEX
# =====================================================

@st.cache_data(ttl=60)
def obtener_materias_primas_activas():

    df = obtener_datos_prillex()

    if df.empty:
        return df

    activas = (
        df["MMPP Activa"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    datos_activos = df[
        activas.isin(["SI", "SÍ", "1", "TRUE", "X"])
    ].copy()

    return datos_activos.reset_index(drop=True)


# =====================================================
# 5. RESUMEN DEL MRP
# =====================================================

def obtener_resumen_mrp():

    df, hojas = cargar_mrp()

    datos_prillex = obtener_datos_prillex()

    return {
        "datos": df,
        "datos_prillex": datos_prillex,
        "hojas": hojas,
        "columnas": df.columns.tolist(),
        "cantidad_registros": len(df),
        "cantidad_prillex": len(datos_prillex)
    }

