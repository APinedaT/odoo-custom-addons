/** @odoo-module */
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";

// Listen to the stock updates pushed by the server (stock.quant changes) and
// refresh the quantities of the loaded products, so the product cards update
// in real time without reloading the POS.
patch(PosStore.prototype, {
    async afterProcessServerData() {
        this.data.connectWebSocket("POS_STOCK_UPDATE", this.onPosStockUpdate.bind(this));
        return await super.afterProcessServerData(...arguments);
    },
    onPosStockUpdate(data) {
        for (const model of ["product.product", "product.template"]) {
            for (const [id, [qty, virtual]] of Object.entries(data[model] || {})) {
                this.models[model].get(id)?.update(
                    { qty_available: qty, virtual_available: virtual },
                    { omitUnknownField: true }
                );
            }
        }
    },
});
