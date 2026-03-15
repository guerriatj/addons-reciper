from odoo import _, api, models, fields
from odoo.exceptions import ValidationError
from collections import defaultdict


class ShoppingListIngredientLine(models.Model):
    _name = "shopping.list.ingredient.line"
    _description = "Shopping List Ingredient Line"

    shopping_list_id = fields.Many2one("shopping.list", required=True, ondelete="cascade")
    ingredient_id = fields.Many2one("recipe.ingredient", required=True)
    ingredient_count = fields.Integer("How many?", default=1)
    uom_id = fields.Many2one("uom.uom", required=True)

    @api.onchange("ingredient_id")
    def set_uom(self):
        self.ensure_one()
        self.uom_id = self.ingredient_id.uom_id
