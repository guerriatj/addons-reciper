/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

publicWidget.registry.recipe_shopping_list = publicWidget.Widget.extend({
    selector: '.shopping_list_form',
    events: {
        'click span[name="add_recipe"]': '_addRecipe',
        'click span[name="add_ingredient"]': '_addIngredient',
        'click .remove-line': '_removeLine',
        'change select[name="recipe_id"]': '_onRecipeChange',
        'change select[name="ingredient_id"]': '_onIngredientChange',
    },


    _addRecipe() {
        const container = document.getElementById("recipe_lines");
        const template = document.getElementById("recipe_template");
        const newLine = template.cloneNode(true);
        newLine.id = '';
        newLine.classList.remove('d-none');

        newLine.querySelector('input[name="people_count"]').value = 1;

        container.appendChild(newLine);
        // Select2 sera initialisé par le MutationObserver
    },

    _addIngredient() {
        const container = document.getElementById("ingredient_lines");
        const template = document.getElementById("ingredient_template");
        const newLine = template.cloneNode(true);
        newLine.id = '';
        newLine.classList.remove('d-none');

        newLine.querySelector('input[name="ingredient_count"]').value = 1;

        container.appendChild(newLine);
        // Select2 sera initialisé par le MutationObserver
    },

    _removeLine (){
        const line = event.target.closest(
            ".recipe-line-container, .ingredient-line-container"
        );
        const parent = line.parentNode;
        line.remove();
    },

    _onRecipeChange(ev) {
        const $select = $(ev.currentTarget);
        const val = $select.val();
        if (!val) return;

        const recipeId = parseInt(val, 10);
        if (isNaN(recipeId)) return;

        const $line = $select.closest('.recipe-line-container');
        const $peopleCount = $line.find('input[name="people_count"]');
        if (!$peopleCount.length) return;

        if (window.recipes_data && window.recipes_data[recipeId]) {
            $peopleCount.val(window.recipes_data[recipeId].people_count || 1);
        }
    },

    _onIngredientChange(ev) {
        const $select = $(ev.currentTarget);
        const val = $select.val();

        if (!val) return;

        const ingredientId = parseInt(val, 10);
        if (isNaN(ingredientId)) return;

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
    }
});
