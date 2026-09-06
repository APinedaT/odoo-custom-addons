# -*- coding: utf-8 -*-

import logging

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# Context keys driving the electronic invoice specifics. They are only set by the
# actions of this module, so the standard POS invoicing flow is left untouched.
EINVOICE_KEY = 'pos_electronic_invoice'
EINVOICE_MULTI_KEY = 'pos_electronic_invoice_multi'


class PosOrder(models.Model):
    _inherit = 'pos.order'

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_electronic_invoice_journal(self):
        """Journal carrying the DIAN resolution used for POS electronic invoices."""
        journals = self.config_id.electronic_invoice_journal_id
        if not journals:
            raise UserError(_(
                "No electronic invoice journal is configured on the point of sale %(config)s.",
                config=', '.join(self.config_id.mapped('name')),
            ))
        if len(journals) > 1:
            raise UserError(_("The selected orders do not share the same electronic invoice journal."))
        return journals

    def _check_electronic_invoice(self):
        """Validate that ``self`` can be merged into one single electronic invoice.

        The grouping keys mirror the ones ``point_of_sale`` itself uses when it
        consolidates several orders on a single move (see ``pos.make.invoice``):
        a config, a partner, a salesperson and a fiscal position.
        """
        if not self:
            raise UserError(_("Select at least one POS order."))
        if any(not order.partner_id for order in self):
            raise UserError(_("Please provide a customer for every selected order."))
        if len(self.company_id) > 1:
            raise UserError(_("All the orders must belong to the same company."))
        if len(self.config_id) > 1:
            raise UserError(_("All the orders must belong to the same point of sale."))
        if len(self.partner_id) > 1:
            raise UserError(_("All the orders must share the same customer to be merged into a single electronic invoice."))
        if len(self.user_id) > 1:
            raise UserError(_("All the orders must share the same salesperson to be merged into a single electronic invoice."))
        if len(self.fiscal_position_id) > 1:
            raise UserError(_("All the orders must share the same fiscal position to be merged into a single electronic invoice."))
        if sum(self.mapped('amount_total')) <= 0:
            raise UserError(_("The electronic invoice cannot be generated for orders with a negative or zero total amount."))
        self._get_electronic_invoice_journal()

    def _get_electronic_invoice_narration(self):
        """Customer notes of the orders, followed by the company invoice terms."""
        parts = [note for note in self.mapped('general_customer_note') if note]
        use_terms = self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms')
        if use_terms and self.env.company.invoice_terms:
            parts.append(self.env.company.with_context(lang=self.partner_id.lang).invoice_terms)
        return '\n'.join(parts)

    # ------------------------------------------------------------------
    # Invoice preparation overrides
    # ------------------------------------------------------------------

    def _prepare_invoice_vals(self):
        vals = super()._prepare_invoice_vals()
        if not self.env.context.get(EINVOICE_KEY):
            return vals

        # ``resolution_id`` is not set here on purpose: since 19.0 it is a stored
        # computed field of l10n_co_edi_jorels derived from
        # ``journal_id.resolution_invoice_id``, so pointing at the right journal
        # is enough.
        vals['journal_id'] = self._get_electronic_invoice_journal().id

        references = ', '.join(self.mapped('name'))
        vals['payment_reference'] = references
        vals['invoice_origin'] = references
        if not vals.get('reversed_entry_id'):
            vals['ref'] = references

        narration = self._get_electronic_invoice_narration()
        if narration:
            vals['narration'] = narration

        _logger.info("Electronic invoice vals for %s: %s", references, vals)
        return vals

    @api.model
    def _get_invoice_lines_values(self, line_values, pos_line, move_type):
        vals = super()._get_invoice_lines_values(line_values, pos_line, move_type)
        if not self.env.context.get(EINVOICE_KEY) or vals.get('display_type'):
            return vals

        product = line_values['product_id']
        # ``get_product_multiline_description_sale`` builds on ``display_name``, which
        # already carries the "[default_code]" prefix, so only prepend the internal
        # reference when it is actually missing.
        description = product.get_product_multiline_description_sale()
        code = product.default_code
        name = f"{code} {description}" if code and code not in description else description
        if self.env.context.get(EINVOICE_MULTI_KEY):
            name = f"{name} (POS: {pos_line.order_id.name})"
        vals['name'] = name

        # Taxes are deliberately dropped from the electronic invoice lines, as in
        # the original 14.0 implementation. ``extra_tax_data`` goes with them,
        # otherwise account would still try to reconcile the POS tax details.
        vals['tax_ids'] = False
        vals.pop('extra_tax_data', None)
        return vals

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _generate_pos_order_einvoice(self):
        """Create one electronic invoice covering every order of ``self``."""
        self._check_electronic_invoice()

        orders = self.with_context(**{
            EINVOICE_KEY: True,
            EINVOICE_MULTI_KEY: len(self) > 1,
        })

        # Mirror ``action_pos_order_invoice``: flagging the orders as "to invoice"
        # may turn on the real time picking creation (anglo-saxon accounting).
        pending_pickings = orders.filtered(lambda o: not o._should_create_picking_real_time())
        orders.write({'to_invoice': True})
        for order in pending_pickings:
            if order._should_create_picking_real_time() and order.session_id.state != 'closed':
                order._create_order_picking()

        return orders._generate_pos_order_invoice()

    def _action_view_einvoice(self, move):
        return {
            'name': _('Customer Invoice'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'context': "{'move_type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': move.id,
        }

    def action_pos_order_einvoice(self):
        """Backend button: electronic invoice for a single POS order."""
        self.ensure_one()
        if self.account_move:
            return self._action_view_einvoice(self.account_move)
        return self._action_view_einvoice(self._generate_pos_order_einvoice())

    def action_many_pos_orders_einvoices(self):
        """Server action: merge the selected POS orders into one electronic invoice."""
        orders = self or self.browse(self.env.context.get('active_ids', []))
        already_invoiced = orders.filtered('account_move')
        if already_invoiced:
            raise UserError(_(
                "The following orders are already invoiced:\n\n%(orders)s",
                orders='\n'.join(already_invoiced.mapped('name')),
            ))
        return self._action_view_einvoice(orders.sudo()._generate_pos_order_einvoice())
