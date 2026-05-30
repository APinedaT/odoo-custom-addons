/** @odoo-module **/
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";

patch(ProductCard.prototype, {
    get minPriceTag() {
        const minPrice = this.props.product?.min_price ?? 0;
        if (minPrice > 0) {
            return "neos" + Math.floor(minPrice / 1000);
        }
        return null;
    },
});
