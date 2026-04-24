/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.recipe_shopping_list = publicWidget.Widget.extend({
    selector: '.shopping_list_form',
    events: {
        'click .remove-line': '_removeLine',
        'change select[name="recipe_id"]': '_onRecipeChange',
        'change select[name="ingredient_id"]': '_onIngredientChange',
    },

    start() {
        this._super(...arguments);
        this._initTomSelect();
        this._ensureEmptyRecipeLine();
        this._ensureEmptyIngredientLine();

    },

    _waitForTomSelect() {
        return new Promise(resolve => {
            const check = () => {
                if (typeof TomSelect !== 'undefined') resolve();
                else setTimeout(check, 50);
            };
            check();
        });
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

    // ─── Recettes ────────────────────────────────────────────────────────────

    _ensureEmptyRecipeLine() {
        const container = document.getElementById("recipe_lines");
        const visibleLines = [...container.querySelectorAll('.recipe-line-container:not(.d-none):not(#recipe_template)')];
        const hasEmpty = visibleLines.some(line => {
            const sel = line.querySelector('select[name="recipe_id"]');
            return sel && !sel.value;
        });
        if (!hasEmpty) {
            this._addRecipeLine();
        }
    },

_addRecipeLine() {
    const container = document.getElementById("recipe_lines");
    const template = document.getElementById("recipe_template");
    const newLine = template.cloneNode(true);
    newLine.id = '';
    newLine.classList.remove('d-none');
    newLine.querySelector('input[name="people_count"]').value = 1;
    newLine.querySelectorAll('select[name="recipe_id"]').forEach(s => s.classList.add('select2_box'));
    container.appendChild(newLine);
    setTimeout(() => this._initTomSelect(newLine), 0);
},

    // ─── Ingrédients ─────────────────────────────────────────────────────────

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
    newLine.querySelector('input[name="ingredient_count"]').value = 1;
    newLine.querySelectorAll('select[name="ingredient_id"], select[name="uom_id"]').forEach(s => s.classList.add('select2_box'));
    container.appendChild(newLine);
    setTimeout(() => this._initTomSelect(newLine), 0);
},
    // ─── Handlers ────────────────────────────────────────────────────────────

    _removeLine(ev) {
        const line = ev.target.closest(
            ".recipe-line-container, .ingredient-line-container"
        );
        line.remove();
    },

    _onRecipeChange(ev) {
        const $select = $(ev.currentTarget);
        const val = $select.val();
        if (!val) return;

        const recipeId = parseInt(val, 10);
        if (isNaN(recipeId)) return;

        // Pré-remplir le nombre de personnes
        const $line = $select.closest('.recipe-line-container');
        const $peopleCount = $line.find('input[name="people_count"]');
        if ($peopleCount.length && window.recipes_data && window.recipes_data[recipeId]) {
            $peopleCount.val(window.recipes_data[recipeId].people_count || 1);
        }

        // Ajouter une nouvelle ligne vide si nécessaire
        this._ensureEmptyRecipeLine();
    },

    _onIngredientChange(ev) {
        const $select = $(ev.currentTarget);
        const val = $select.val();
        if (!val) return;

        const ingredientId = parseInt(val, 10);
        if (isNaN(ingredientId)) return;

        // Pré-remplir quantité et UoM
        const $line = $select.closest('.ingredient-line-container');
        const $ingredientCount = $line.find('input[name="ingredient_count"]');
        const $uomSelect = $line.find('select[name="uom_id"]');

        if (window.ingredients_data && window.ingredients_data[ingredientId]) {
            const data = window.ingredients_data[ingredientId];
            if ($ingredientCount.length && data.ingredient_count) {
                $ingredientCount.val(data.ingredient_count);
            }
            if ($uomSelect.length && data.uom_id) {
                $uomSelect.val(data.uom_id).trigger('change');
            }
        }

        // Ajouter une nouvelle ligne vide si nécessaire
        this._ensureEmptyIngredientLine();
    },
});
publicWidget.registry.recipe_shopping_list_validated = publicWidget.Widget.extend({
    selector: '.shopping_list_form_validated',
    start() {
        this._super(...arguments);
        const textarea = this.el.querySelector('textarea[name="notes"]');
        if (textarea) {
            this._autoResizeTextarea(textarea);

            textarea.addEventListener('input', (ev) => {
                this._autoResizeTextarea(ev.target);
            });
        }
    },

    _autoResizeTextarea(el) {
        el.style.height = 'auto';
        el.style.height = el.scrollHeight + 'px';
    }
});