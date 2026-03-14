from odoo import models, fields


class Recipe(models.Model):
    _name = "recipe"
    _description = "Recipe"

    name = fields.Char(required=True)

    recipe_line_ids = fields.One2many(
        "recipe.line",
        "recipe_id"
    )

    instructions = fields.Html()


