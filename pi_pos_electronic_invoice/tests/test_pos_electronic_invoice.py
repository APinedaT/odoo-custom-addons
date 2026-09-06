# -*- coding: utf-8 -*-

from odoo.addons.point_of_sale.tests.common import CommonPosTest, TestPoSCommon
from odoo.exceptions import UserError
from odoo.tests.common import tagged


@tagged('post_install', '-at_install')
class TestPosElectronicInvoice(TestPoSCommon, CommonPosTest):

    def setUp(self):
        super().setUp()
        self.config = self.basic_config
        self.einvoice_journal = self.env['account.journal'].create({
            'name': 'Electronic Invoices',
            'code': 'EINV',
            'type': 'sale',
            'company_id': self.env.company.id,
        })
        self.config.electronic_invoice_journal_id = self.einvoice_journal
        self.sale_tax = self.taxes['tax7']
        self.product1 = self.create_product('Product 1', self.categ_basic, 10.0, tax_ids=self.sale_tax.ids)
        self.product1.default_code = 'REF-1'
        self.product2 = self.create_product('Product 2', self.categ_basic, 20.0, tax_ids=self.sale_tax.ids)

    def _create_order(self, product, qty=1, customer=None):
        orders = self._create_orders([{
            'pos_order_lines_ui_args': [(product, qty)],
            'customer': customer if customer is not None else self.customer,
            'is_invoiced': False,
        }])
        return sum(orders.values(), self.env['pos.order'])

    def test_single_order_uses_electronic_journal_without_taxes(self):
        self.open_new_session()
        order = self._create_order(self.product1)

        action = order.action_pos_order_einvoice()
        invoice = order.account_move

        self.assertTrue(invoice, "The electronic invoice should be linked to the order.")
        self.assertEqual(action['res_id'], invoice.id)
        self.assertEqual(invoice.journal_id, self.einvoice_journal)
        self.assertEqual(invoice.state, 'posted')
        self.assertEqual(order.state, 'done')
        self.assertFalse(invoice.invoice_line_ids.tax_ids, "Taxes must be dropped from the electronic invoice.")
        self.assertEqual(invoice.invoice_line_ids.name, '[REF-1] Product 1',
                         "The internal reference must appear exactly once in the line name.")
        self.assertEqual(invoice.ref, order.name)
        self.assertEqual(invoice.invoice_origin, order.name)

    def test_second_call_returns_existing_invoice(self):
        self.open_new_session()
        order = self._create_order(self.product1)

        invoice_id = order.action_pos_order_einvoice()['res_id']
        self.assertEqual(order.action_pos_order_einvoice()['res_id'], invoice_id)
        self.assertEqual(len(order.account_move), 1)

    def test_many_orders_merged_into_one_invoice(self):
        self.open_new_session()
        order1 = self._create_order(self.product1)
        order2 = self._create_order(self.product2, qty=2)
        orders = order1 | order2

        orders.action_many_pos_orders_einvoices()
        invoice = orders.account_move

        self.assertEqual(len(invoice), 1, "The selected orders should share a single invoice.")
        self.assertEqual(invoice.journal_id, self.einvoice_journal)
        self.assertEqual(len(invoice.invoice_line_ids), 2)
        for line in invoice.invoice_line_ids:
            self.assertRegex(line.name, r'\(POS: .+\)$', "Merged lines must carry their POS order reference.")

    def test_different_partners_are_rejected(self):
        self.open_new_session()
        orders = self._create_order(self.product1) | self._create_order(self.product2, customer=self.other_customer)

        with self.assertRaises(UserError):
            orders.action_many_pos_orders_einvoices()

    def test_missing_journal_is_rejected(self):
        self.open_new_session()
        self.config.electronic_invoice_journal_id = False
        order = self._create_order(self.product1)

        with self.assertRaises(UserError):
            order.action_pos_order_einvoice()

    def test_standard_invoicing_is_left_untouched(self):
        self.open_new_session()
        order = self._create_order(self.product1)

        order.action_pos_order_invoice()
        invoice = order.account_move

        self.assertEqual(invoice.journal_id, self.config.invoice_journal_id)
        self.assertEqual(invoice.invoice_line_ids.tax_ids, self.sale_tax)
