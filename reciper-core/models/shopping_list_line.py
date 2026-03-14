from odoo import models, fields


class ShoppingListLine(models.Model):
    _name = "shopping.list.line"
    _description = "Shopping List Line"
    _order = "shopping_list_id, aisle_sequence, recipe_ingredient_id"

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
    recipe_ids = fields.Many2many("recipe")

    quantity = fields.Float()

    uom_id = fields.Many2one(
        "uom.uom",
    )

    is_picked = fields.Boolean()

    def set_picked(self):
        for rec in self:
            if rec.shopping_list_id.state != "confirmed":
                rec.shopping_list_id.state = "confirmed"
            rec.is_picked = True

            all_picked = all(line.is_picked for line in rec.shopping_list_id.shopping_list_line_ids)
            if all_picked:
                rec.shopping_list_id.state = "completed"
