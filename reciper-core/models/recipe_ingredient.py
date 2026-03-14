from odoo import models, fields


class RecipeIngredient(models.Model):
    _name = "recipe.ingredient"
    _description = "Recipe Ingredient"

    name = fields.Char(required=True)
    uom_id = fields.Many2one("uom.uom", required=True)
    aisle_ids = fields.Many2many(
        "store.aisle",
        "store_aisle_recipe_ingredient_rel",
        "ingredient_id",
        "aisle_id",
        string="Aisles"
    )
