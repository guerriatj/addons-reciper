from odoo import _, api, models, fields
from odoo.exceptions import ValidationError
from collections import defaultdict


class ShoppingList(models.Model):
    _inherit = "shopping.list"


    def create_recipe_lines(self, form):
        self.ensure_one()
        recipe_ids = form.getlist("recipe_id")
        people_counts = form.getlist("people_count")

        self.shopping_list_recipe_line_ids.unlink()
        vals_list = []
        for recipe_id, people_count in zip(recipe_ids, people_counts):
            if not recipe_id:
                continue

            vals_list.append({
                "shopping_list_id": self.id,
                "recipe_id": int(recipe_id),
                "people_count": int(people_count),
            })
        self.env["shopping.list.recipe.line"].create(vals_list)


    def create_ingredient_lines(self, form):
        self.ensure_one()
        self.shopping_list_ingredient_line_ids.unlink()

        ingredient_ids = form.getlist("ingredient_id")
        ingredient_counts = form.getlist("ingredient_count")
        uom_ids = form.getlist("uom_id")
        vals_list = []

        for ingredient_id, ingredient_count, uom_id in zip(
                ingredient_ids,
                ingredient_counts,
                uom_ids
        ):
            # Ignore les lignes vides
            if not ingredient_id:
                continue

            vals_list.append({
                "shopping_list_id": self.id,
                "ingredient_id": int(ingredient_id),
                "ingredient_count": int(ingredient_count or 1),
                "uom_id": int(uom_id) if uom_id else False,
            })
        self.env["shopping.list.ingredient.line"].create(vals_list)