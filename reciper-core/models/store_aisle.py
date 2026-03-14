from odoo import models, fields


class StoreAisle(models.Model):
    _name = "store.aisle"
    _description = "Store Aisle"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    store_id = fields.Many2one("store", required=True)
    ingredient_ids = fields.Many2many("recipe.ingredient")