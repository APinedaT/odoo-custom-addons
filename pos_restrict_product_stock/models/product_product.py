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


class ProductProduct(models.Model):
    """Extend product.product POS data loading to return stock quantities
    scoped to the POS session's configured source location
    (pos.config → picking_type_id → default_location_src_id) instead of
    the company-wide total."""

    _inherit = 'product.product'

    @api.model
    def _load_pos_data_fields(self, config):
        """Add qty_available, virtual_available and type to the fields
        loaded into the POS session for each product.product record.
        In Odoo 19, `config` here is the pos.config record object."""
        fields = super()._load_pos_data_fields(config)
        for field in ('qty_available', 'virtual_available', 'type'):
            if field not in fields:
                fields.append(field)
        return fields

    @api.model
    def _load_pos_data_read(self, records, config):
        """After the base read, replace qty_available / virtual_available
        with quantities scoped to the POS source location."""
        result = super()._load_pos_data_read(records, config)
        quantities = config._get_pos_stock_quantities(
            'product_id', [d['id'] for d in result if d.get('id')])
        if quantities is None:
            return result
        for product_dict in result:
            qty, virtual = quantities.get(product_dict.get('id'), (0.0, 0.0))
            product_dict['qty_available'] = qty
            product_dict['virtual_available'] = virtual
        return result
