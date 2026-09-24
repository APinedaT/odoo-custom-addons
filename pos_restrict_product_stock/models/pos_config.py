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
import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    """Inherited pos configuration setting for adding some
            fields for restricting out-of stock"""
    _inherit = 'pos.config'

    is_display_stock = fields.Boolean(string="Display Stock in POS",
                                      help="Enable if you want to show "
                                           "quantity of products")
    is_restrict_product = fields.Boolean(
        string="Restrict Product Out-of Stock in POS",
        help="Enable if you want restrict of stock product from pos")
    stock_type = fields.Selection([('qty_on_hand', 'Qty on Hand'),
                                   ('virtual_qty', 'Virtual Qty'),
                                   ('both', 'Both')], required=True,
                                  default='qty_on_hand', string="Stock Type",
                                  help="In which quantity type you"
                                       " have to restrict and display")

    def _get_pos_stock_quantities(self, groupby, ids):
        """Return ``{id: (qty_available, virtual_available)}`` for the given
        product (``groupby='product_id'``) or template
        (``groupby='product_tmpl_id'``) ids, scoped to the POS source location
        (picking_type_id → default_location_src_id) and its children.
        Ids without quants get (0.0, 0.0). Returns None when the operation
        type has no source location, meaning the global stock must be kept."""
        self.ensure_one()
        location = self.picking_type_id.default_location_src_id
        if not location:
            _logger.warning(
                "pos_restrict_product_stock: No source location on "
                "picking_type_id '%s' for POS config '%s'. "
                "Falling back to global stock.",
                self.picking_type_id.display_name, self.name,
            )
            return None
        quantities = dict.fromkeys(ids, (0.0, 0.0))
        quant_data = self.env['stock.quant'].sudo()._read_group(
            [
                ('location_id', 'child_of', location.id),
                (groupby, 'in', list(ids)),
            ],
            groupby=[groupby],
            aggregates=['quantity:sum', 'reserved_quantity:sum'],
        )
        for record, on_hand, reserved in quant_data:
            on_hand = on_hand or 0.0
            quantities[record.id] = (on_hand, on_hand - (reserved or 0.0))
        return quantities
