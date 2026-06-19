from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_pi_require_customer = fields.Boolean(
        related="pos_config_id.pi_require_customer",
        readonly=False,
    )
