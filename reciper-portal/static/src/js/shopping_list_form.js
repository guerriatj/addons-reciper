odoo.define('reciper-portal.shopping_list_form', ['web.public.widget', 'web.core', 'jquery'], function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');
    const $ = require('jquery');
    const core = require('web.core');

    publicWidget.registry.ShoppingListForm = publicWidget.Widget.extend({
        selector: '.shopping-list-form',

        start: function () {
            this._initSelect2();
            return this._super.apply(this, arguments);
        },

        _initSelect2: function () {
            const $form = this.$el;

            // Select2 pour les recettes
            const $recipeSelect = $form.find('#recipe_ids');
            if ($recipeSelect.length) {
                $recipeSelect.select2({
                    placeholder: 'Select Recipes',
                    width: '100%'
                });
            }

            // Select2 pour les ingrédients
            const $ingredientSelect = $form.find('#ingredient_ids');
            if ($ingredientSelect.length) {
                $ingredientSelect.select2({
                    placeholder: 'Select Ingredients',
                    width: '100%'
                });
            }

            // Filtre rapide côté client pour ingrédients
            $form.find('#ingredient_filter').on('input', function () {
                const search = $(this).val().toLowerCase();
                $ingredientSelect.find('option').each(function () {
                    const name = $(this).text().toLowerCase();
                    $(this).toggle(name.includes(search));
                });
                $ingredientSelect.trigger('change.select2');
            });
        },
    });
});
