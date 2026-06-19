{
    'name': 'POS Require Customer',
    'version': '19.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Andres Pineda',
    'support': 'apineda099@gmail.com',
    'category': 'Sales/Point of Sale',
    'website': 'https://pitechnology.site',
    'summary': 'Hace obligatorio seleccionar el cliente antes de validar el pago en el POS',
    'depends': ['point_of_sale'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pi_pos_require_customer/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
}
