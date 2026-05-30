{
    'name': 'POS Min Price Tag',
    'version': '19.0.0.0.1',
    'license': 'AGPL-3',
    'author': 'Andres Pineda',
    'support': 'apineda099@gmail.com',
    'category': 'Sales/Point of Sale',
    'website': 'https://pitechnology.site',
    'depends': ['point_of_sale'],
    'data': ['views/product_template_views.xml'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pi_pos_min_price/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
}
