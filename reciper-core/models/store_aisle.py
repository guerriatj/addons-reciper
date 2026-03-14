from odoo import models, fields


class StoreAisle(models.Model):
    _name = "store.aisle"
    _description = "Store Aisle"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    store_id = fields.Many2one("store", required=True)
    ingredient_ids = fields.Many2many(
        "recipe.ingredient",
        "store_aisle_recipe_ingredient_rel",
        "aisle_id",
        "ingredient_id",
        string="Ingredients"
    )
