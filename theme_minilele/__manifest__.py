# -*- coding: utf-8 -*-
{
    'name': 'Theme Mini Lele Boutique',
    'category': 'Theme/Creative',
    'summary': 'Tema boutique de ropa infantil exclusiva — candy + dorado + crema',
    'description': """
=================================

Diseño boutique infantil con paleta candy (rosa, azul cielo, amarillo, menta,
verde, lila), acentos dorados, base crema y tipografías redondeadas (Fredoka +
Nunito + Pacifico).

Incluye:
* Paleta de colores 
* Tipografías Google Fonts (Fredoka, Nunito, Pacifico)
* Header translúcido con franja superior promocional
* Snippets de boutique:
    - Hero con confeti animado
    - Tarjetas de categoría (Niñas / Niños / Bebé)
    - Tira dorada de beneficios
    - Grid de productos destacados
    - Sección historia con marco rotado
    - Testimonios de clientas
    - Lookbook estilo Instagram
    - Newsletter con borde de costura rosa
* Página de inicio precargada
* Estilos compatibles con website_sale (eCommerce)
    """,
    'version': '1.0.0',
    'author': 'Andres Pineda',
    'depends': [
        'website',
        'website_sale',
    ],
    'data': [
        'views/snippets/s_minilele_hero.xml',
        'views/snippets/s_minilele_categories.xml',
        'views/snippets/s_minilele_promo_strip.xml',
        'views/snippets/s_minilele_products.xml',
        'views/snippets/s_minilele_story.xml',
        'views/snippets/s_minilele_testimonials.xml',
        'views/snippets/s_minilele_lookbook.xml',
        'views/snippets/s_minilele_newsletter.xml',
        'views/snippets_register.xml',
        'views/layout.xml',
    ],
    'assets': {
        # Appended so Odoo defines $o-color-palettes and $o-theme-font-configs first
        'web._assets_primary_variables': [
            'theme_minilele/static/src/scss/primary_variables.scss',
        ],
        # Loaded for the frontend (the website)
        'web.assets_frontend': [
            'theme_minilele/static/src/scss/theme.scss',
            'theme_minilele/static/src/scss/snippets.scss',
        ],
    },
    'images': [
        'static/description/cover.png',
    ],
    'installable': True,
    'application': False,
}
