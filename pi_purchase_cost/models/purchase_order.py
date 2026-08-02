# -*- coding: utf-8 -*-

from odoo import models, fields

class PiPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    sale_price = fields.Float(related='product_id.list_price',readonly=False)
    on_hand = fields.Float(related='product_id.qty_available')
    cost_price = fields.Float(related='product_id.standard_price')