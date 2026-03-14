from odoo import _, api, models, fields
from odoo.exceptions import ValidationError
from collections import defaultdict


class ShoppingList(models.Model):
    _name = "shopping.list"
    _description = "Shopping List"

    display_name = fields.Char(compute="_compute_display_name")
    date = fields.Date(required=True)
    recipe_ids = fields.Many2many("recipe")
    store_id = fields.Many2one("store")

    other_ingredient_ids = fields.Many2many("recipe.ingredient")

    shopping_list_line_ids = fields.One2many(
        "shopping.list.line",
        "shopping_list_id"
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
        ],
        default="draft",
        required=True
    )

    @api.constrains("shopping_list_line_ids")
    def check_state(self):
        for shopping_list in self:
            if shopping_list.state != "draft":
                raise ValidationError(_("To change the list, please set it to draft state"))

    def _compute_display_name(self):
        for list in self:
            list.display_name = f"Liste de courses {list.date}"

    def action_confirm(self):
        for list in self:
            list.state = "confirmed"

    @api.constrains("other_ingredient_ids", "recipe_ids", "store_id")
    def action_generate_from_recipes(self):
        unit_uom = self.env.ref("uom.product_uom_unit")

        for shopping_list in self:

            qty_map = defaultdict(float)
            recipe_map = defaultdict(set)

            # collecter quantités + recettes
            for recipe in shopping_list.recipe_ids:
                for line in recipe.recipe_line_ids:
                    ingredient = line.recipe_ingredient_id
                    qty_map[ingredient] += line.quantity
                    recipe_map[ingredient].add(recipe)

            lines = []

            # lignes venant des recettes
            for ingredient, qty in qty_map.items():
                aisle = self.env["store.aisle"].search([
                    ("store_id", "=", shopping_list.store_id.id),
                    ("ingredient_ids", "in", ingredient.id)
                ], limit=1)

                recipes = recipe_map.get(ingredient, [])

                lines.append((0, 0, {
                    "recipe_ingredient_id": ingredient.id,
                    "quantity": qty,
                    "uom_id": ingredient.uom_id.id or unit_uom.id,
                    "aisle_id": aisle.id if aisle else False,
                    "recipe_ids": [(6, 0, [r.id for r in recipes])]
                }))

            # lignes venant de other_ingredient_ids (sans recette)
            for ingredient in shopping_list.other_ingredient_ids:
                aisle = self.env["store.aisle"].search([
                    ("store_id", "=", shopping_list.store_id.id),
                    ("ingredient_ids", "in", ingredient.id)
                ], limit=1)

                lines.append((0, 0, {
                    "recipe_ingredient_id": ingredient.id,
                    "quantity": 1,
                    "uom_id": ingredient.uom_id.id or unit_uom.id,
                    "aisle_id": aisle.id if aisle else False,
                    "recipe_ids": [(6, 0, [])]
                }))

            shopping_list.shopping_list_line_ids.unlink()
            shopping_list.shopping_list_line_ids = lines