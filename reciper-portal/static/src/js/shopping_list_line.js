/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.shopping_list_toggle = publicWidget.Widget.extend({

    selector: "#shopping_lines",

    events: {
        "dblclick .shopping-line": "_toggleLine",  // <=== double-clic
    },

    async _toggleLine(ev) {
        const row = ev.currentTarget;
        const lineId = row.dataset.lineId;
        if (!lineId) return;
        try {
            const result = await rpc("/shopping_list/toggle_line", {
                line_id: lineId,
            });
            if (!result.success) return;

            const tbody = row.parentNode;
            row.classList.remove("picked", "not-picked");

            if (result.is_picked) {
                row.classList.add("picked");
                tbody.appendChild(row); // déplacer en bas
            } else {
                row.classList.add("not-picked");
                tbody.prepend(row); // déplacer en haut
            }

        } catch (error) {
            console.error(error);
        }
    },

});