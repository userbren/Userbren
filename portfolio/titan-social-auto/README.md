# Titan Social Auto

Bot que extrae noticias de fuentes RSS y las envía a la bandeja de Ideas de Buffer mediante su API GraphQL, con memoria SQLite para evitar duplicados.

## Tecnologías

- **Python 3.8+**
- **API:** Buffer GraphQL
- **Fuentes:** RSS/Atom feeds
- **Base de datos:** SQLite
- **Librerías:** requests, feedparser, python-dotenv

## Cómo funciona

```
Feeds RSS → Extraer noticias → ¿Ya publicada? → No → Enviar a Buffer → Guardar en DB
                                  │
                                  └→ Sí → Saltar
```

- Cada ejecución procesa los feeds y envía **1 noticia nueva** (evita spam)
- La base de datos SQLite guarda las URLs ya procesadas
- Las credenciales van en `.env` (no se suben al repo)

## Instalación

```bash
# 1. Clonar
git clone https://github.com/userbren/titan-social-auto.git
cd titan-social-auto

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar credenciales
cp .env.example .env
# Edita .env con tu Access Token y Organization ID de Buffer

# 4. Ejecutar
python bot_retweet.py
```

## Configuración

Edita `config.json` para añadir o cambiar fuentes RSS:

```json
{
  "feeds_industria": [
    "https://techcrunch.com/feed/",
    "https://feeds.wired.com/wired/index"
  ]
}
```

## Obtener credenciales de Buffer

1. Ve a [Buffer Personal Keys](https://publish.buffer.com/settings/api)
2. Genera una Personal Key
3. Copia el Access Token
4. Obtén tu Organization ID desde el [GraphQL Explorer](https://developers.buffer.com/explorer.html)

## Estado

✅ Funcional — En uso para automatización de contenido.
