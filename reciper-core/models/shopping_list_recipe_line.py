from odoo import _, api, models, fields
from odoo.exceptions import ValidationError
from collections import defaultdict


class ShoppingListRecipeLine(models.Model):
    _name = "shopping.list.recipe.line"
    _description = "Shopping List Recipe"

    shopping_list_id = fields.Many2one("shopping.list", required=True, ondelete="cascade")
    recipe_id = fields.Many2one("recipe", required=True)
    people_count = fields.Integer("How many people?", default=2, required=True)
