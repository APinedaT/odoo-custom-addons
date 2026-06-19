import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ask } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(OrderPaymentValidation.prototype, {
    async askBeforeValidation() {
        if (this.pos.config.pi_require_customer && !this.order.getPartner()) {
            const confirmed = await ask(this.pos.dialog, {
                title: _t("Please select the Customer"),
                body: _t("You must select a customer before validating this order."),
            });
            if (confirmed) {
                this.pos.selectPartner();
            }
            return false;
        }
        return await super.askBeforeValidation(...arguments);
    },
});
