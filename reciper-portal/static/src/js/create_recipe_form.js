/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.create_recipe_form = publicWidget.Widget.extend({
    selector: '.create_recipe_form',
    events: {
        'click .remove-line': '_removeLine',
        'change select[name="ingredient_id"]': '_onIngredientChange',
    },

    start() {
        this._super(...arguments);
        this._initTomSelect();
        this._ensureEmptyIngredientLine();
    },

    _initTomSelect(root) {
        const scope = root || this.el;
        scope.querySelectorAll('select.select2_box:not(.tomselected)').forEach(el => {
            new TomSelect(el, {
                allowEmptyOption: true,
                maxOptions: null,
            });
        });
    },

    _ensureEmptyIngredientLine() {
        const container = document.getElementById("ingredient_lines");
        const visibleLines = [...container.querySelectorAll('.ingredient-line-container:not(.d-none):not(#ingredient_template)')];
        const hasEmpty = visibleLines.some(line => {
            const sel = line.querySelector('select[name="ingredient_id"]');
            return sel && !sel.value;
        });
        if (!hasEmpty) {
            this._addIngredientLine();
        }
    },

    _addIngredientLine() {
        const container = document.getElementById("ingredient_lines");
        const template = document.getElementById("ingredient_template");
        const newLine = template.cloneNode(true);
        newLine.id = '';
        newLine.classList.remove('d-none');
        newLine.querySelector('input[name="quantity"]').value = 1;
        newLine.querySelectorAll('select[name="ingredient_id"]').forEach(s => s.classList.add('select2_box'));
        container.appendChild(newLine);
        setTimeout(() => this._initTomSelect(newLine), 0);
    },

    _removeLine(ev) {
        ev.target.closest('.ingredient-line-container').remove();
    },

    _onIngredientChange(ev) {
        const select = ev.currentTarget;
        const line = select.closest('.ingredient-line-container');
        const uomLabel = line.querySelector('.ingredient-line-uom');
        const selectedOption = select.options[select.selectedIndex];
        if (uomLabel) {
            uomLabel.textContent = (selectedOption && selectedOption.dataset.uom) || '';
        }

        this._ensureEmptyIngredientLine();
    },
});
