# -*- coding: utf-8 -*-
{
    'name': 'Theme Ferretería y Cerrajería Pineda',
    'category': 'Theme/Retail',
    'summary': 'Pineda Design System — rojo ferretería, amarillo casco, tinta negra',
    'description': """
    """,
    'version': '19.0.1.0.0',
    'author': 'Andres Pineda',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'website_sale',
    ],
    'data': [
        'views/product_card_template.xml',
        'views/snippets/s_pineda_hero.xml',
        'views/snippets/s_pineda_categories.xml',
        'views/snippets/s_pineda_delivery.xml',
        'views/snippets/s_pineda_services.xml',
        'views/snippets_register.xml',
        'views/layout.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'theme_ferrepineda/static/src/scss/primary_variables.scss',
        ],
        'web.assets_frontend': [
            'theme_ferrepineda/static/src/scss/tokens.scss',
            'theme_ferrepineda/static/src/scss/theme.scss',
            'theme_ferrepineda/static/src/scss/snippets.scss',
            'theme_ferrepineda/static/src/scss/website_sale.scss',
        ],
    },
    'installable': True,
    'application': False,
}
