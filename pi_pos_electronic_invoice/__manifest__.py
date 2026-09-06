# -*- coding: utf-8 -*-
{
    'name': 'POS Electronic Invoice',
    'version': '19.0.1.0.0',
    'author': 'Andres Pineda',
    'license': 'LGPL-3',
    'category': 'Point of Sale',
    'depends': [
        'point_of_sale',
        'l10n_co_edi_jorels_pos',
    ],
    'data': [
        'views/pos_order.xml',
        'views/res_config_settings.xml',
        'data/server_action.xml',
    ],
    'external_dependencies': {},
    'application': False,
    'installable': True,
    'auto_install': False,
}
