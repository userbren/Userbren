"""
Titan Social Auto — Bot de Automatización RSS a Buffer

Extrae noticias de fuentes RSS y las envía a la bandeja de Ideas de Buffer
mediante su API GraphQL, con memoria SQLite para evitar duplicados.
"""

import os
import json
import sqlite3
import requests
import feedparser
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Cargar variables de entorno (API keys van en .env)
load_dotenv()

# ==========================================
# CONFIGURACIÓN
# ==========================================
BUFFER_ACCESS_TOKEN: Optional[str] = os.getenv("BUFFER_ACCESS_TOKEN")
BUFFER_ORGANIZATION_ID: Optional[str] = os.getenv("BUFFER_ORGANIZATION_ID")
CONFIG_FILE: str = "config.json"
DB_FILE: str = "memoria.db"


def init_db() -> None:
    """Inicializa la base de datos SQLite para memoria de publicaciones."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS publicaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def url_fue_publicada(url: str) -> bool:
    """Verifica si la URL ya fue publicada."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM publicaciones WHERE url = ?", (url,))
    resultado = cursor.fetchone()
    conn.close()
    return bool(resultado)


def registrar_publicacion(url: str) -> None:
    """Guarda la URL en memoria para no volverla a publicar."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO publicaciones (url) VALUES (?)", (url,))
    conn.commit()
    conn.close()


def cargar_configuracion() -> List[str]:
    """Carga los feeds RSS desde config.json."""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            return datos.get("feeds_industria", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"[!] Error: No se pudo cargar {CONFIG_FILE}.")
        return []


def obtener_noticias_rss(urls_rss: List[str], limite_por_feed: int = 3) -> List[Dict[str, str]]:
    """Extrae las últimas noticias de los feeds RSS."""
    print(f"[*] Escaneando feeds RSS...")
    noticias: List[Dict[str, str]] = []

    for url in urls_rss:
        try:
            feed = feedparser.parse(url)
            nombre_fuente = feed.feed.title if hasattr(feed, 'feed') and 'title' in feed.feed else url
            print(f"  -> Fuente: {nombre_fuente}")

            for entry in feed.entries[:limite_por_feed]:
                noticias.append({
                    "titulo": entry.title,
                    "url": entry.link,
                    "origen": nombre_fuente
                })
        except Exception as e:
            print(f"[!] Error en feed {url}: {e}")

    return noticias


def enviar_idea_buffer(noticia: Dict[str, str], org_id: str) -> bool:
    """Envía la noticia a la bandeja de Ideas de Buffer vía GraphQL."""
    print(f"\n[*] Enviando a Buffer (Org ID: {org_id})...")

    mensaje: str = (
        f"💡 {noticia['titulo']}\n\n"
        f"📎 {noticia['url']}\n"
        f"📰 {noticia['origen']}"
    )

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {BUFFER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    query = """
    mutation CreateIdea($orgId: ID!, $text: String!) {
      createIdea(input: {
        organizationId: $orgId,
        content: {
          text: $text
        }
      }) {
        ... on Idea {
          id
        }
      }
    }
    """

    payload: Dict[str, Any] = {
        "query": query,
        "variables": {
            "orgId": org_id,
            "text": mensaje
        }
    }

    try:
        response = requests.post("https://api.buffer.com", json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print(f"[!] Error API: {data['errors']}")
                return False
            if data.get("data", {}).get("createIdea", {}).get("id"):
                idea_id = data["data"]["createIdea"]["id"]
                print(f"[+] Idea enviada correctamente. ID: {idea_id}")
                return True
            print(f"[!] Respuesta inesperada: {data}")
            return False
        else:
            print(f"[!] Error HTTP {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[!] Error de conexión: {e}")
        return False


def main() -> None:
    print("=" * 55)
    print("  Titan Social Auto — RSS Auto-Poster (GraphQL)")
    print("=" * 55)

    if not BUFFER_ACCESS_TOKEN or not BUFFER_ORGANIZATION_ID:
        print("[!] Faltan credenciales. Crea un archivo .env con:")
        print("    BUFFER_ACCESS_TOKEN=tu_token")
        print("    BUFFER_ORGANIZATION_ID=tu_org_id")
        return

    # 1. Inicializar base de datos
    init_db()

    # 2. Cargar feeds
    feeds = cargar_configuracion()
    if not feeds:
        print("[-] No hay feeds configurados.")
        return

    # 3. Obtener noticias
    noticias = obtener_noticias_rss(feeds, limite_por_feed=3)
    if not noticias:
        print("[-] No se encontraron noticias.")
        return

    print(f"[*] Total artículos: {len(noticias)}")

    # 4. Enviar la primera noticia no duplicada
    publicado = False
    for n in noticias:
        if not url_fue_publicada(n['url']):
            print(f"\n[*] Nueva: {n['titulo']} ({n['origen']})")
            if enviar_idea_buffer(n, BUFFER_ORGANIZATION_ID):
                registrar_publicacion(n['url'])
                publicado = True
                break
        else:
            print(f"[-] Ya publicado: {n['titulo']}")

    if not publicado:
        print("\n[-] No hay noticias nuevas para enviar.")


if __name__ == "__main__":
    main()
