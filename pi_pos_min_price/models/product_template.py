from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    min_price = fields.Float(
        string='Minimum Price',
        digits='Product Price',
        default=0.0,
        help='Minimum selling price shown in the POS as a tag (e.g. neos120).',
    )

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields += ['min_price']
        return fields
