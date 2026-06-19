{
    'name': 'POS Product Description',
    'version': '19.0.0.0.1',
    'license': 'AGPL-3',
    'author': 'Andres Pineda',
    'support': 'apineda099@gmail.com',
    'category': 'Sales/Point of Sale',
    'summary': 'Muestra la descripcion del producto en el catalogo y en la linea de pedido del POS',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pi_pos_product_description/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
}
