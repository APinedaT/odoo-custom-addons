import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { useAsyncLockedMethod } from "@point_of_sale/app/hooks/hooks";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { QuotationScreen } from "@pi_pos_receipt_custom/js/quotation_screen";

patch(ControlButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.quotationPrinter = useService("printer");
        this.clickPrintQuotation = useAsyncLockedMethod(this.clickPrintQuotation);
    },
    async clickPrintQuotation() {
        // Sin impresora de hardware `print` devuelve undefined: se muestra la
        // vista previa en un dialogo para imprimir/descargar desde ahi.
        const printed = await this.quotationPrinter.print(OrderReceipt, {
            order: this.pos.getOrder(),
            isQuotation: true,
        });
        if (!printed) {
            this.dialog.add(QuotationScreen);
        }
    },
});
