import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { patch } from "@web/core/utils/patch";

// En Odoo 19 OrderReceipt recibe `order` (registro pos.order) en lugar del
// antiguo `data` exportado. Se declara la prop extra usada por la cotizacion.
patch(OrderReceipt, {
    props: {
        ...OrderReceipt.props,
        isQuotation: { type: Boolean, optional: true },
    },
    defaultProps: {
        ...OrderReceipt.defaultProps,
        isQuotation: false,
    },
});
