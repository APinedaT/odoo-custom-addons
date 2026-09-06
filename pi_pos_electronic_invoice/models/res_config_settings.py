# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_electronic_invoice_journal_id = fields.Many2one(
        related='pos_config_id.electronic_invoice_journal_id', readonly=False)
