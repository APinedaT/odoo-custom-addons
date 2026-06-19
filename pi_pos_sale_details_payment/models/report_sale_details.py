# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class ReportPoint_Of_SaleReport_Saledetails(models.AbstractModel):
    _inherit = 'report.point_of_sale.report_saledetails'

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, config_ids=False, session_ids=False, **kwargs):
        res = super().get_sale_details(date_start, date_stop, config_ids, session_ids, **kwargs)

        # Rebuild the same set of orders used by the base report to list, per
        # order, which payment method(s) were used to settle it.
        if not session_ids:
            date_start, date_stop = self._get_date_start_and_date_stop(date_start, date_stop)
        domain = self._get_domain(date_start, date_stop, config_ids, session_ids)
        orders = self.env['pos.order'].search(domain, order='date_order, id')

        orders_list = []
        for order in orders:
            payment_methods = ', '.join(
                order.payment_ids.mapped('payment_method_id.name')
            ) or _('None')
            orders_list.append({
                'name': order.pos_reference or order.name,
                'date_order': order.date_order,
                'payment_methods': payment_methods,
                'amount_total': order.amount_total,
            })

        res['orders'] = orders_list
        return res
