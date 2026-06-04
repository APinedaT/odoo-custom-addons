/** @odoo-module **/
import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    get minPriceTag() {
        const minPrice = this.line.product_id?.product_tmpl_id?.min_price ?? 0;
        if (minPrice > 0) {
            return "neos" + Math.floor(minPrice / 1000);
        }
        return null;
    },
});
