// Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import {PosOrder} from "@point_of_sale/app/models/pos_order";
import {PosOrderline} from "@point_of_sale/app/models/pos_order_line";
import {patch} from "@web/core/utils/patch";
import {roundCurrency} from "@point_of_sale/app/models/utils/currency";

// /////////////////////////////
// Overload models.PosOrder
// /////////////////////////////
patch(PosOrder.prototype, {
    getMargin() {
        return this.getOrderlines().reduce((margin, line) => margin + line.getMargin(), 0);
    },

    getMarginRate() {
        const priceWithoutTax = this.priceExcl;
        return priceWithoutTax ? (this.getMargin() / priceWithoutTax) * 100 : 0;
    },

    getMarginRateStr() {
        return roundCurrency(this.getMarginRate(), this.currency) + "%";
    },
});

// /////////////////////////////
// Overload models.PosOrderline
// /////////////////////////////
patch(PosOrderline.prototype, {
    getIfaceDisplayMargin() {
        return this.config.iface_display_margin;
    },

    getPurchasePrice() {
        // Overload the function to use another field that the default standard_price
        return this.product_id.standard_price;
    },

    getPriceWithoutTax() {
        // ``priceExcl`` flips the sign of the refund orders to display them as
        // positive amounts, whereas ``qty`` stays negative. Use the raw value so
        // that both terms of the margin keep the same sign.
        return this.currency.round(this.prices.total_excluded);
    },

    getMargin() {
        return this.getPriceWithoutTax() - this.qty * this.getPurchasePrice();
    },

    getMarginRate() {
        const priceWithoutTax = this.getPriceWithoutTax();
        return priceWithoutTax ? (this.getMargin() / priceWithoutTax) * 100 : 0;
    },

    getMarginRateStr() {
        return roundCurrency(this.getMarginRate(), this.currency) + "%";
    },
});
