// Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import {Component} from "@odoo/owl";
import {OrderDisplay} from "@point_of_sale/app/components/order_display/order_display";
import {formatCurrency} from "@web/core/currency";

export class OrderSummaryMargin extends Component {
    static template = "pos_margin.OrderSummaryMargin";
    static props = {
        order: Object,
    };

    get order() {
        return this.props.order;
    }

    getOrderMargin() {
        const order = this.order;
        if (!order.getOrderlines().length) {
            return false;
        }
        return {
            margin: formatCurrency(order.getMargin(), order.currency.id),
            margin_rate: order.getMarginRateStr(),
        };
    }
}

// ``OrderDisplay`` is service-less by design, so the margin is rendered by a
// dedicated component that receives the order through its props.
OrderDisplay.components = {
    ...OrderDisplay.components,
    OrderSummaryMargin,
};
