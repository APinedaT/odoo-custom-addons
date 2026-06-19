/** @odoo-module **/
import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
import { htmlToText } from "@pi_pos_product_description/utils/html_to_text";

patch(Orderline.prototype, {
    get saleDescription() {
        return htmlToText(this.line.product_id?.product_tmpl_id?.description);
    },
});
