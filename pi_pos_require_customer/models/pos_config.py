from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    pi_require_customer = fields.Boolean(
        string="Require Customer",
        help="If enabled, a customer must be selected before validating a payment in the POS.",
    )
