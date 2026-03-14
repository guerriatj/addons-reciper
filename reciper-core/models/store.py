from odoo import models, fields


class Store(models.Model):
    _name = "store"
    _description = "Store"

    name = fields.Char(required=True)
    aisle_ids = fields.One2many("store.aisle", "store_id", string="Aisles")
