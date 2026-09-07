# Backend Favicon

Muestra en el backend de Odoo el mismo favicon configurado en **Sitio web →
Configuración → Ajustes → Favicon**.

## Por qué hace falta

`web.layout` (el `<head>` común a frontend y backend) pinta el icono así:

```xml
<link type="image/x-icon" rel="shortcut icon" t-att-href="x_icon or '/web/static/img/favicon.ico'"/>
```

La variable `x_icon` solo la define `website.layout`, con el campo
`website.favicon`. `web.webclient_bootstrap` (el backend) llama a `web.layout`
sin definirla, así que cae siempre al icono morado estático de Odoo. Además, en
Odoo 19 `res.company` ya no tiene campo `favicon`, por lo que no hay ninguna
opción de configuración que cambie el icono del backend.

Este módulo hereda `web.webclient_bootstrap` y define `x_icon` con el favicon
del website actual (`get_current_website()`, que en el backend resuelve por
dominio y si no cae al primer website).

## Notas

- Los navegadores cachean el favicon de forma muy agresiva: tras instalar,
  recarga con `Ctrl+Shift+R` o prueba en una ventana privada.
- Multi-website: se usa el website que corresponda al dominio con el que entras
  al backend.
- No toca el `apple-touch-icon` ni el icono de la PWA (`/scoped_app_icon_png`),
  que siguen siendo los de Odoo.
