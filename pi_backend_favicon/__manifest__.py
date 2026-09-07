{
  'name': 'Backend Favicon',
  'summary': 'Usa el favicon del sitio web también en el backend',
  'version': '19.0.0.0.1',
  "license": "AGPL-3",
  'description': """
Backend Favicon
===============

Por defecto Odoo solo aplica el favicon configurado en Ajustes de Website a las
páginas del frontend: la plantilla `web.layout` toma el icono de la variable
`x_icon`, que únicamente define `website.layout`. El backend llama a la misma
plantilla sin definirla, así que siempre cae al icono estático
`/web/static/img/favicon.ico`.

Este módulo hereda `web.webclient_bootstrap` y define `x_icon` con el favicon
del website actual, de modo que el backend muestre el mismo icono que el sitio.
""",
  'author': 'Andres Pineda',
  'support': 'apineda099@gmail.com',
  'category': 'Website',
  'website': "https://pitechnology.site",
  'depends': [
    'web',
    'website',
  ],
  'data': [
    "views/webclient_templates.xml",
  ],
  'installable': True,
  'auto_install': False,
}
