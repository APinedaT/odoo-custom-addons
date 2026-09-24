# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2026-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author:Yadhu Shankar E(<https://www.cybrosys.com>)
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, models

PRECOMMIT_KEY = 'pos_restrict_product_stock.product_ids'


class StockQuant(models.Model):
    """Push the new stock quantities to the open POS sessions whenever a quant
    changes (POS sales, receipts, deliveries, inventory adjustments,
    reservations), so the product cards update without reloading the POS."""
    _inherit = 'stock.quant'

    @api.model
    def _update_available_quantity(self, product_id, location_id, *args, **kwargs):
        result = super()._update_available_quantity(product_id, location_id, *args, **kwargs)
        self._pos_stock_mark_changed(product_id)
        return result

    @api.model
    def _update_reserved_quantity(self, product_id, location_id, *args, **kwargs):
        result = super()._update_reserved_quantity(product_id, location_id, *args, **kwargs)
        self._pos_stock_mark_changed(product_id)
        return result

    @api.model
    def _pos_stock_mark_changed(self, products):
        """Collect the changed products and send one notification per open
        POS right before the transaction is committed."""
        products = products.filtered('is_storable')
        if not products:
            return
        precommit = self.env.cr.precommit
        if PRECOMMIT_KEY not in precommit.data:
            precommit.data[PRECOMMIT_KEY] = set()
            precommit.add(self.sudo()._pos_stock_notify)
        precommit.data[PRECOMMIT_KEY].update(products.ids)

    def _pos_stock_notify(self):
        product_ids = self.env.cr.precommit.data.pop(PRECOMMIT_KEY, set())
        products = self.env['product.product'].browse(product_ids).exists()
        if not products:
            return
        configs = self.env['pos.session'].search(
            [('state', '!=', 'closed')]).config_id
        for config in configs:
            product_qty = config._get_pos_stock_quantities(
                'product_id', products.ids)
            if product_qty is None:
                continue
            config._notify('POS_STOCK_UPDATE', {
                'product.product': product_qty,
                'product.template': config._get_pos_stock_quantities(
                    'product_tmpl_id', products.product_tmpl_id.ids),
            })
