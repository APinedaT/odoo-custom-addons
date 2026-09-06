# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _default_electronic_invoice_journal(self):
        return self.env['account.journal'].search([
            *self.env['account.journal']._check_company_domain(self.env.company),
            ('type', '=', 'sale'),
        ], limit=1)

    electronic_invoice_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Electronic Invoice Journal',
        domain=[('type', '=', 'sale')],
        check_company=True,
        help="Accounting journal used to create the DIAN electronic invoices generated "
             "from the backend. It must carry the invoicing resolution.",
        default=_default_electronic_invoice_journal,
    )

    @api.constrains('electronic_invoice_journal_id', 'currency_id')
    def _check_electronic_invoice_journal_currency(self):
        for config in self:
            journal_currency = config.electronic_invoice_journal_id.currency_id
            if journal_currency and journal_currency != config.currency_id:
                raise ValidationError(_(
                    "The electronic invoice journal of %(config)s must use the same currency "
                    "as the point of sale.",
                    config=config.name,
                ))
