{
    'name': 'POS Custom Receipt',
    'version': '19.0.0.0.1',
    'license': 'AGPL-3',
    'author': 'Andres Pineda',
    'support': 'apineda099@gmail.com',
    'category': 'Sales/Point of Sale',
    'website': 'https://pitechnology.site',
    'summary': 'Moves company info to top of receipt and hides tax breakdown',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pi_pos_custom_receipt/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
}
