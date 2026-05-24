/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SocialMediaSidebar = publicWidget.Widget.extend({
    selector: ".s-media",
    events: {
        "click #sm-close": "_onClose",
    },

    start() {
        this._super(...arguments);
        this._openBtn = document.getElementById("sm-open");
        if (this._openBtn) {
            this._openBtn.addEventListener("click", this._onOpen.bind(this));
        }
    },

    _onClose() {
        this.el.classList.add("sm-collapse");
        if (this._openBtn) {
            setTimeout(() => (this._openBtn.style.right = "0"), 300);
        }
    },

    _onOpen() {
        if (this._openBtn) {
            this._openBtn.style.right = "-60px";
        }
        this.el.classList.remove("sm-collapse");
    },
});
