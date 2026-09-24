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


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Include qty_available and virtual_available in the template fields
        sent to the POS session. Location-scoped values are injected by the
        _load_pos_data_read override below."""
        fields = super(ProductTemplate, self)._load_pos_data_fields(config_id)
        if 'qty_available' not in fields:
            fields.append('qty_available')
        if 'virtual_available' not in fields:
            fields.append('virtual_available')
        return fields

    @api.model
    def _load_pos_data_read(self, records, config):
        """After the base read, replace qty_available / virtual_available
        with quantities scoped to the POS source location."""
        result = super()._load_pos_data_read(records, config)
        quantities = config._get_pos_stock_quantities(
            'product_tmpl_id', [d['id'] for d in result if d.get('id')])
        if quantities is None:
            return result
        for template_dict in result:
            qty, virtual = quantities.get(template_dict.get('id'), (0.0, 0.0))
            template_dict['qty_available'] = qty
            template_dict['virtual_available'] = virtual
        return result
