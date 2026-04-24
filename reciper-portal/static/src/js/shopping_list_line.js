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

        const notPicked = document.getElementById('not_picked_lines');
        const picked = document.getElementById('picked_lines');

        if (!notPicked || !picked) {
            console.warn("Containers introuvables");
            return;
        }

        row.classList.remove('picked', 'not-picked', 'text-danger');

        if (result.is_picked) {
            row.classList.add('picked', 'text-danger');
            picked.appendChild(row);
        } else {
            row.classList.add('not-picked');
            notPicked.prepend(row);
        }

    } catch (error) {
        console.error(error);
    }
}

});