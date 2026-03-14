from odoo import api, models, fields
from collections import defaultdict


class ShoppingList(models.Model):
    _name = "shopping.list"
    _description = "Shopping List"

    display_name = fields.Char(compute="_compute_display_name")
    date = fields.Date(required=True)
    recipe_ids = fields.Many2many("recipe")

    other_ingredient_ids = fields.Many2many("recipe.ingredient")

    shopping_list_line_ids = fields.One2many(
        "shopping.list.line",
        "shopping_list_id"
    )

    def _compute_display_name(self):
        for list in self:
            list.display_name = f"Liste de courses {list.date}"

    @api.constrains("other_ingredient_ids", "recipe_ids")
    def action_generate_from_recipes(self):
        unit_uom = self.env.ref("uom.product_uom_unit")

        for shopping_list in self:
            ingredient_map = defaultdict(float)
            for recipe in shopping_list.recipe_ids:
                for line in recipe.recipe_line_ids:
                    ingredient_map[line.recipe_ingredient_id] += line.quantity

            for ingredient in shopping_list.other_ingredient_ids:
                ingredient_map[ingredient] += 1

            lines = []

            for ingredient, qty in ingredient_map.items():
                lines.append((0, 0, {
                    "recipe_ingredient_id": ingredient.id,
                    "quantity": qty,
                    "uom_id": ingredient.uom_id.id or unit_uom.id,
                }))

            shopping_list.shopping_list_line_ids.unlink()
            shopping_list.shopping_list_line_ids = lines