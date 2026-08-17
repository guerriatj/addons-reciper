/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { RecipeGalleryWidget } from "@reciper-portal/js/recipe_gallery";

// Mode "sélection" de la galerie de recettes : hérite du tronc commun
// (filtre, ouverture/fermeture du modal) et ajoute la sélection multiple
// avec compteur de personnes, utilisée pour peupler les lignes de la liste
// de courses.
publicWidget.registry.recipe_shopping_list = RecipeGalleryWidget.extend({
    selector: '.shopping_list_form',
    events: Object.assign({}, RecipeGalleryWidget.prototype.events, {
        'click .remove-line': '_removeLine',
        'change select[name="recipe_id"]': '_onRecipeChange',
        'change select[name="ingredient_id"]': '_onIngredientChange',
        'click .recipe-count-minus': '_onGalleryCountMinus',
        'click .recipe-count-plus': '_onGalleryCountPlus',
        'click .recipe-gallery-confirm': '_onGalleryConfirm',
    }),

    start() {
        const def = this._super(...arguments);
        this._initTomSelect();
        this._ensureEmptyRecipeLine();
        this._ensureEmptyIngredientLine();
        return def;
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
    // ─── Galerie de recettes (mode sélection) ───────────────────────────────

    _onGalleryItemClick(ev) {
        if (ev.target.closest('.recipe-count-minus, .recipe-count-plus')) return;

        const item = ev.currentTarget;
        const counter = item.querySelector('.recipe-gallery-counter');
        const isSelected = item.classList.toggle('selected');

        if (isSelected) {
            counter.classList.remove('d-none');
            counter.classList.add('d-flex');
            const countValue = item.querySelector('.recipe-count-value');
            countValue.textContent = item.dataset.peopleCount || 1;
        } else {
            counter.classList.add('d-none');
            counter.classList.remove('d-flex');
        }
    },

    _onGalleryCountMinus(ev) {
        const valueEl = ev.currentTarget.closest('.recipe-gallery-item').querySelector('.recipe-count-value');
        valueEl.textContent = Math.max(0, parseInt(valueEl.textContent, 10) - 1);
    },

    _onGalleryCountPlus(ev) {
        const valueEl = ev.currentTarget.closest('.recipe-gallery-item').querySelector('.recipe-count-value');
        valueEl.textContent = parseInt(valueEl.textContent, 10) + 1;
    },

    async _onGalleryConfirm() {
        const selectedItems = [...this.el.querySelectorAll('.recipe-gallery-item.selected')];
        const selections = selectedItems.map(item => ({
            recipeId: item.dataset.recipeId,
            peopleCount: item.querySelector('.recipe-count-value').textContent,
        }));

        await this._addRecipeLinesFromGallery(selections);

        window.Modal.getOrCreateInstance(this.galleryModalEl).hide();
    },

    _onGalleryShow() {
        const container = document.getElementById("recipe_lines");
        const lines = [...container.querySelectorAll('.recipe-line-container:not(.d-none):not(#recipe_template)')];

        const countByRecipeId = new Map();
        lines.forEach(line => {
            const recipeId = line.querySelector('select[name="recipe_id"]').value;
            if (!recipeId) return;
            const peopleCount = line.querySelector('input[name="people_count"]').value;
            countByRecipeId.set(recipeId, peopleCount);
        });

        this.el.querySelectorAll('.recipe-gallery-item').forEach(item => {
            const counter = item.querySelector('.recipe-gallery-counter');
            const recipeId = item.dataset.recipeId;
            if (countByRecipeId.has(recipeId)) {
                item.classList.add('selected');
                counter.classList.remove('d-none');
                counter.classList.add('d-flex');
                item.querySelector('.recipe-count-value').textContent =
                    countByRecipeId.get(recipeId) || item.dataset.peopleCount || 1;
            } else {
                item.classList.remove('selected');
                counter.classList.add('d-none');
                counter.classList.remove('d-flex');
            }
        });
    },

    _onGalleryHidden() {
        this._super(...arguments);
        this.el.querySelectorAll('.recipe-gallery-item.selected').forEach(item => {
            item.classList.remove('selected');
            const counter = item.querySelector('.recipe-gallery-counter');
            counter.classList.add('d-none');
            counter.classList.remove('d-flex');
        });
    },

    async _addRecipeLinesFromGallery(selections) {
        const container = document.getElementById("recipe_lines");
        const usedLines = new Set();

        for (const {recipeId, peopleCount} of selections) {
            // La recette est déjà présente dans une ligne : on met juste à jour
            // le nombre de personnes, on ne l'ajoute pas une deuxième fois.
            const existingLine = [...container.querySelectorAll('.recipe-line-container:not(.d-none):not(#recipe_template)')]
                .find(l => !usedLines.has(l) && l.querySelector('select[name="recipe_id"]').value === String(recipeId));

            if (existingLine) {
                usedLines.add(existingLine);
                existingLine.querySelector('input[name="people_count"]').value = peopleCount;
                continue;
            }

            const line = await this._claimRecipeLine(usedLines);
            usedLines.add(line);

            const select = line.querySelector('select[name="recipe_id"]');
            const input = line.querySelector('input[name="people_count"]');
            if (select.tomselect) {
                select.tomselect.setValue(String(recipeId));
            } else {
                select.value = recipeId;
                select.dispatchEvent(new Event('change', {bubbles: true}));
            }
            input.value = peopleCount;
        }
        this._ensureEmptyRecipeLine();
    },

    // Finds an unclaimed empty recipe line, or creates one and waits for its
    // TomSelect instance to be ready (it's initialized asynchronously).
    _claimRecipeLine(usedLines) {
        const container = document.getElementById("recipe_lines");
        const existing = [...container.querySelectorAll('.recipe-line-container:not(.d-none):not(#recipe_template)')]
            .find(l => !usedLines.has(l) && !l.querySelector('select[name="recipe_id"]').value);

        if (existing) return Promise.resolve(existing);

        this._addRecipeLine();
        const lines = container.querySelectorAll('.recipe-line-container:not(.d-none):not(#recipe_template)');
        const newLine = lines[lines.length - 1];

        return new Promise(resolve => {
            const select = newLine.querySelector('select[name="recipe_id"]');
            const check = () => {
                if (select.tomselect) resolve(newLine);
                else setTimeout(check, 10);
            };
            check();
        });
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