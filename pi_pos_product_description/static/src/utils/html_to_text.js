/** @odoo-module **/

export function htmlToText(html) {
    if (!html) {
        return "";
    }
    const doc = new DOMParser().parseFromString(html, "text/html");
    return (doc.body.textContent || "").trim();
}
