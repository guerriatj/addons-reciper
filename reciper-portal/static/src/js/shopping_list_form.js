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

    _addRecipe () {
        const container = document.getElementById("recipe_lines");
        const lines = container.querySelectorAll(".recipe-line-container:not(#recipe_template)");

        let newLine;
        if (lines.length) {
            const lastLine = lines[lines.length - 1];
            newLine = lastLine.cloneNode(true);
        } else {
            const template = document.getElementById("recipe_template");
            newLine = template.cloneNode(true);
            newLine.id = '';
            newLine.classList.remove('d-none');
        }

        newLine.querySelector('select[name="recipe_id"]').value = '';
        newLine.querySelector('input[name="people_count"]').value = 1;

        container.appendChild(newLine);
    },

    _addIngredient () {
        const container = document.getElementById("ingredient_lines");
        const lines = container.querySelectorAll(".ingredient-line-container:not(#ingredient_template)");

        let newLine;
        if (lines.length) {
            // Cloner la dernière ligne existante
            const lastLine = lines[lines.length - 1];
            newLine = lastLine.cloneNode(true);
        } else {
            // Cloner le template caché
            const template = document.getElementById("ingredient_template");
            newLine = template.cloneNode(true);
            newLine.id = '';           // enlever l'ID
            newLine.classList.remove('d-none'); // afficher la ligne
        }

        // Réinitialiser les valeurs
        newLine.querySelector('select[name="ingredient_id"]').value = '';
        newLine.querySelector('input[name="ingredient_count"]').value = 1;
        newLine.querySelector('select[name="uom_id"]').value = '';

        container.appendChild(newLine);
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
        debugger

        if (!val) return;  // pas de valeur sélectionnée

        const ingredientId = parseInt(val, 10);
        if (isNaN(ingredientId)) return;

        // récupérer la ligne contenant le select
        const $line = $select.closest('.ingredient-line-container');

        // input du nombre d'ingrédients (si tu veux mettre une valeur par défaut)
        const $ingredientCount = $line.find('input[name="ingredient_count"]');

        // select de l'unité
        const $uomSelect = $line.find('select[name="uom_id"]');

        if (window.ingredients_data && window.ingredients_data[ingredientId]) {
            const data = window.ingredients_data[ingredientId];

            // remplir le nombre par défaut (optionnel)
            if ($ingredientCount.length && data.ingredient_count) {
                $ingredientCount.val(data.ingredient_count);
            }

            // remplir l'uom par défaut (optionnel)
            if ($uomSelect.length && data.uom_id) {
                $uomSelect.val(data.uom_id).trigger('change');
            }
        }
    }
//
//    _removeQuestion(ev) {
//        const counter_node = $("#question_count");
//        const count = parseInt(counter_node.val());
//        const questionId = $(ev.currentTarget).closest('.form-group').data('question-id');
//        $(`div[data-question-id="${questionId}"]`).remove();
//        counter_node.val(count-1);
//    },
//
//    async _deletePolLine(ev) {
//        ev.preventDefault();
//        const $btn = $(ev.currentTarget);
//        const polLineId = $btn.data('pol-line-id');
//        if (!polLineId) return;
//        await rpc('/web/dataset/call_kw', {
//            model: 'proof.of.life.line', method: 'unlink',
//            args: [polLineId],
//            kwargs: {},
//        })
//        $btn.closest('.pol-line-container').remove();
//    },
});
