import base64
import requests
import streamlit as st


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

GITHUB_API = "https://api.github.com"
GITHUB_API_VERSION = "2022-11-28"


def _secret(nombre, default=None):
    """Obtiene un valor desde Streamlit Secrets."""
    try:
        return st.secrets.get(nombre, default)
    except Exception:
        return default


def _config():
    """Obtiene la configuración de GitHub."""

    return {
        "token": _secret("GITHUB_TOKEN"),
        "repo": _secret("GITHUB_REPO"),
        "branch": _secret("GITHUB_BRANCH", "main"),
    }


def gh_disponible():
    """Comprueba si están configuradas las credenciales de GitHub."""

    config = _config()

    return all([
        config["token"],
        config["repo"],
        config["branch"]
    ])


def _headers():
    """Encabezados para comunicarse con GitHub."""

    config = _config()

    return {
        "Authorization": f"Bearer {config['token']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION
    }


def limpiar_ruta(ruta):
    """Normaliza las rutas de archivos dentro del repositorio."""

    return str(ruta).replace("\\", "/").strip("/")


# =========================================================
# CONTRASEÑA DE ADMINISTRACIÓN
# =========================================================

def gh_password_configurada():
    """Comprueba si existe una contraseña de administración."""

    return bool(_secret("CLAVE_SUBIDA"))


def gh_password_ok(clave):
    """Valida la contraseña ingresada."""

    clave_correcta = _secret("CLAVE_SUBIDA")

    if not clave_correcta:
        return False

    return str(clave) == str(clave_correcta)


# =========================================================
# CONEXIÓN CON EL REPOSITORIO
# =========================================================

def _url_contenido(ruta):
    config = _config()
    ruta = limpiar_ruta(ruta)

    return (
        f"{GITHUB_API}/repos/{config['repo']}"
        f"/contents/{ruta}"
    )


def gh_diagnostico():
    """Comprueba la conexión con el repositorio."""

    if not gh_disponible():
        return {
            "ok": False,
            "mensaje": "Faltan credenciales de GitHub en Streamlit Secrets."
        }

    config = _config()

    url = f"{GITHUB_API}/repos/{config['repo']}"

    try:
        respuesta = requests.get(
            url,
            headers=_headers(),
            timeout=20
        )

        if respuesta.status_code == 200:
            return {
                "ok": True,
                "mensaje": "Conexión con GitHub correcta."
            }

        return {
            "ok": False,
            "mensaje": (
                f"GitHub respondió con código "
                f"{respuesta.status_code}: {respuesta.text}"
            )
        }

    except requests.RequestException as error:
        return {
            "ok": False,
            "mensaje": f"Error de conexión: {error}"
        }


# =========================================================
# CONSULTAR ARCHIVOS
# =========================================================

def _sha_de(ruta):
    """Obtiene el SHA de un archivo existente."""

    config = _config()

    respuesta = requests.get(
        _url_contenido(ruta),
        headers=_headers(),
        params={"ref": config["branch"]},
        timeout=30
    )

    if respuesta.status_code == 200:
        return respuesta.json().get("sha")

    if respuesta.status_code == 404:
        return None

    respuesta.raise_for_status()


def gh_leer(ruta):
    """Descarga el contenido de un archivo desde GitHub."""

    if not gh_disponible():
        raise RuntimeError(
            "GitHub no está configurado correctamente."
        )

    config = _config()

    respuesta = requests.get(
        _url_contenido(ruta),
        headers=_headers(),
        params={"ref": config["branch"]},
        timeout=60
    )

    if respuesta.status_code == 404:
        return None

    respuesta.raise_for_status()

    datos = respuesta.json()

    if datos.get("encoding") != "base64":
        raise ValueError(
            "GitHub no devolvió el archivo en formato Base64."
        )

    contenido = base64.b64decode(
        datos["content"].replace("\n", "")
    )

    return contenido


def gh_listar(ruta="data"):
    """Lista los archivos existentes en una carpeta."""

    if not gh_disponible():
        return []

    config = _config()

    respuesta = requests.get(
        _url_contenido(ruta),
        headers=_headers(),
        params={"ref": config["branch"]},
        timeout=30
    )

    if respuesta.status_code == 404:
        return []

    respuesta.raise_for_status()

    datos = respuesta.json()

    if isinstance(datos, dict):
        return [datos]

    return datos


# =========================================================
# GUARDAR Y REEMPLAZAR ARCHIVOS
# =========================================================

def _put(ruta, contenido, mensaje, sha=None):
    """Crea o actualiza un archivo en GitHub."""

    config = _config()

    contenido_base64 = base64.b64encode(
        contenido
    ).decode("utf-8")

    datos = {
        "message": mensaje,
        "content": contenido_base64,
        "branch": config["branch"]
    }

    if sha:
        datos["sha"] = sha

    respuesta = requests.put(
        _url_contenido(ruta),
        headers=_headers(),
        json=datos,
        timeout=90
    )

    respuesta.raise_for_status()

    return respuesta.json()


def gh_guardar(
    sub,
    nombre,
    contenido,
    reemplazar=True
):
    """
    Guarda un archivo en GitHub.

    sub: carpeta de destino, por ejemplo 'data'.
    nombre: nombre del archivo.
    contenido: bytes del archivo.
    reemplazar: permite actualizar un archivo existente.
    """

    if not gh_disponible():
        raise RuntimeError(
            "GitHub no está configurado correctamente."
        )

    ruta = limpiar_ruta(f"{sub}/{nombre}")

    sha = _sha_de(ruta)

    if sha and not reemplazar:
        raise FileExistsError(
            f"El archivo {nombre} ya existe en GitHub."
        )

    mensaje = (
        f"Actualizar archivo {ruta}"
        if sha
        else f"Subir archivo {ruta}"
    )

    return _put(
        ruta=ruta,
        contenido=contenido,
        mensaje=mensaje,
        sha=sha
    )


# =========================================================
# ELIMINAR ARCHIVOS
# =========================================================

def _delete(ruta, sha, mensaje):
    """Elimina un archivo del repositorio."""

    config = _config()

    datos = {
        "message": mensaje,
        "sha": sha,
        "branch": config["branch"]
    }

    respuesta = requests.delete(
        _url_contenido(ruta),
        headers=_headers(),
        json=datos,
        timeout=30
    )

    respuesta.raise_for_status()

    return respuesta.json()


def gh_eliminar(ruta):
    """Elimina un archivo existente en GitHub."""

    if not gh_disponible():
        raise RuntimeError(
            "GitHub no está configurado correctamente."
        )

    ruta = limpiar_ruta(ruta)
    sha = _sha_de(ruta)

    if not sha:
        return False

    _delete(
        ruta,
        sha,
        f"Eliminar archivo {ruta}"
    )

    return True

