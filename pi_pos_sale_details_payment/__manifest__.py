{
    'name': 'POS Sale Details Payment Method',
    'version': '19.0.0.0.1',
    'license': 'AGPL-3',
    'author': 'Andres Pineda',
    'support': 'apineda099@gmail.com',
    'category': 'Sales/Point of Sale',
    'website': 'https://pitechnology.site',
    'summary': 'Muestra el metodo de pago de cada orden en el reporte de detalles de ventas del POS y elimina el codigo de barras',
    'depends': ['point_of_sale'],
    'data': [
        'views/report_saledetails.xml',
    ],
    'installable': True,
    'auto_install': False,
}
