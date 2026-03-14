from odoo import models, fields


class ShoppingListLine(models.Model):
    _name = "shopping.list.line"
    _description = "Shopping List Line"
    _order = "shopping_list_id, aisle_sequence"

    shopping_list_id = fields.Many2one(
        "shopping.list",
        ondelete="cascade"
    )

    recipe_ingredient_id = fields.Many2one(
        "recipe.ingredient",
        required=True
    )

    aisle_id = fields.Many2one("store.aisle")
    aisle_sequence = fields.Integer(related="aisle_id.sequence", store=False)

    quantity = fields.Float()

    uom_id = fields.Many2one(
        "uom.uom",
        related="recipe_ingredient_id.uom_id",
        store=True
    )

    is_picked = fields.Boolean()