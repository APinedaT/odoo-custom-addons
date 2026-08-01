# -*- coding: utf-8 -*-

{
    'name': "POS Set Methods Polyfill",

    'summary': "Fix 'this._tables.difference is not a function' on older browsers in the POS.",

    'description': """
Odoo bundles its JS polyfills (web/static/src/polyfills/**) only into
web.assets_backend and web.assets_frontend_minimal. The Point of Sale bundles
never include them, so on a browser without native ES2025 Set methods the POS
crashes at startup in web/static/src/core/utils/indexed_db.js:

    TypeError: this._tables.difference is not a function

This module injects a Set methods polyfill into the POS bundles.
Native support: Chrome/Edge 122+, Firefox 127+, Safari 17+.
""",

    'license': 'LGPL-3',
    'category': 'Point of Sale',
    'version': '19.0.1.0.0',

    'depends': ['point_of_sale'],

    'data': [],

    'assets': {
        # Included by point_of_sale._assets_pos (-> assets_prod / assets_prod_dark)
        # and by point_of_sale.customer_display_assets.
        'point_of_sale.base_app': [
            ('prepend', 'pos_set_polyfill/static/src/polyfills/set.js'),
        ],
    },

    'installable': True,
    'auto_install': True,
}
