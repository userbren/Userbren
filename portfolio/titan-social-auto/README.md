# Titan Social Auto — Automatización de Redes Sociales

Bot que extrae contenido de fuentes RSS y lo envía a Buffer para su programación en redes sociales, con memoria local para evitar duplicados.

## Tecnologías

- **Python 3.8+**
- **API:** Buffer GraphQL
- **Fuentes:** RSS/Atom feeds
- **Base de datos:** SQLite (memoria local)
- **Librerías:** requests, feedparser

## Funcionalidades

- Extracción automática de noticias de múltiples fuentes RSS
- Filtrado de URLs procesadas (memoria SQLite)
- Envío a Buffer mediante API GraphQL
- Configurable por archivo JSON
- Logging de operaciones

## Instalación

```bash
pip install requests feedparser python-dotenv
python bot_retweet.py
```

## Estado

✅ Funcional — En uso para automatización de contenido.
