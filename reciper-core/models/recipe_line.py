from odoo import models, fields


class RecipeLine(models.Model):
    _name = "recipe.line"
    _description = "Recipe Line"

    recipe_id = fields.Many2one(
        "recipe",
        required=True,
        ondelete="cascade"
    )

    recipe_ingredient_id = fields.Many2one(
        "recipe.ingredient",
        required=True
    )

    quantity = fields.Float()

    uom_id = fields.Many2one(
        "uom.uom",
        related="recipe_ingredient_id.uom_id",
        store=True
    )
