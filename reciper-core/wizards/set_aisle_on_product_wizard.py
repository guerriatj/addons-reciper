from odoo import api, models, fields
import json

class ShoppingListLine(models.TransientModel):
    _name = "set.aisle.wizard"

    store_id = fields.Many2one("store", required=True)
    aisle_id = fields.Many2one("store.aisle", string="Set product for aisle", required=True)
    ingredient_to_set_ids = fields.Many2many("recipe.ingredient", string="Products to Update")
    ingredient_domain = fields.Char()

    @api.onchange("store_id")
    def _onchange_store_id(self):
        self.ensure_one()
        self.aisle_id = False
        self.ingredient_to_set_ids = False

    @api.onchange('store_id')
    def _compute_employee_id_domain(self):
        for rec in self:
            ingredients_with_aisle = self.store_id.mapped("aisle_ids.ingredient_ids")
            rec.ingredient_domain = json.dumps([("id", "not in", ingredients_with_aisle.ids)])

    def action_apply(self):
        self.aisle_id.ingredient_ids |= self.ingredient_to_set_ids
