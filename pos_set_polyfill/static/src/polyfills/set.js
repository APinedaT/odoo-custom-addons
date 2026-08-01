/**
 * ES2025 Set methods polyfill for the Point of Sale.
 *
 * `web/static/src/polyfills/**` is only bundled into `web.assets_backend` and
 * `web.assets_frontend_minimal`. The PoS bundles (`point_of_sale.base_app` ->
 * `web._assets_core`) never include it, so on browsers without native support
 * `web/static/src/core/utils/indexed_db.js` crashes on `this._tables.difference`
 * as soon as the PoS opens its IndexedDB.
 *
 * Native support: Chrome/Edge 122+, Firefox 127+, Safari 17+.
 *
 * Plain script (no import/export) on purpose: it runs at bundle evaluation time,
 * before the Odoo module loader starts any module.
 */
(function () {
    function asSetLike(other, method) {
        if (other instanceof Set) {
            return other;
        }
        if (other && typeof other.has === "function" && typeof other.keys === "function") {
            return new Set(other.keys());
        }
        throw new TypeError(`Set.prototype.${method} called with a non set-like argument`);
    }

    const methods = {
        difference(other) {
            const o = asSetLike(other, "difference");
            return new Set([...this].filter((e) => !o.has(e)));
        },
        intersection(other) {
            const o = asSetLike(other, "intersection");
            return new Set([...this].filter((e) => o.has(e)));
        },
        union(other) {
            const o = asSetLike(other, "union");
            return new Set([...this, ...o]);
        },
        symmetricDifference(other) {
            const o = asSetLike(other, "symmetricDifference");
            const result = new Set([...this].filter((e) => !o.has(e)));
            for (const e of o) {
                if (!this.has(e)) {
                    result.add(e);
                }
            }
            return result;
        },
        isSubsetOf(other) {
            const o = asSetLike(other, "isSubsetOf");
            return [...this].every((e) => o.has(e));
        },
        isSupersetOf(other) {
            const o = asSetLike(other, "isSupersetOf");
            return [...o].every((e) => this.has(e));
        },
        isDisjointFrom(other) {
            const o = asSetLike(other, "isDisjointFrom");
            return [...this].every((e) => !o.has(e));
        },
    };

    for (const [name, value] of Object.entries(methods)) {
        if (typeof Set.prototype[name] !== "function") {
            Object.defineProperty(Set.prototype, name, {
                enumerable: false,
                writable: true,
                configurable: true,
                value,
            });
        }
    }
})();
