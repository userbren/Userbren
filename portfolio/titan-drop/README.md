# TitanDrop — Sistema de Dropshipping

Sistema completo de tienda online con panel de administración, pasarela de pago y gestión de pedidos.

## Tecnologías

- **Backend:** Node.js, Express
- **Frontend:** HTML, CSS, JavaScript
- **Base de datos:** PostgreSQL (Supabase)
- **Pagos:** Stripe
- **Despliegue:** Render

## Funcionalidades

- Catálogo de productos con gestión de inventario
- Carrito de compras y checkout
- Pasarela de pago integrada
- Panel de administración para gestionar pedidos
- Notificaciones de estado de pedidos
- Diseño responsive

## Instalación

```bash
# Clonar
git clone https://github.com/userbren/titan-drop.git
cd titan-drop/server

# Instalar dependencias
npm install

# Configurar variables de entorno (ver .env.example)
cp .env.example .env

# Iniciar servidor
npm start
```

## Estado

🚧 En desarrollo — MVP funcional con Stripe integrado en modo test.
