# -*- coding: utf-8 -*-

{
    'name': 'Cambiar Costos de producto desde Orden de compra',
    'version': '19.0.0.1',
    'category': 'purchase',
    'author': 'Andres Pineda',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'purchase',
    ],
    'data': [
        'views/purchase_form.xml',
    ],
    'external_dependencies': {
    },
    'application': False,
    'installable': True,
    'auto_install': False,
}
