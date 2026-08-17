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
    people_count = fields.Integer("How many people?", required=True, default=1)
    image = fields.Image("Image", max_width=1024, max_height=1024)

    category = fields.Selection([
        ("meal", "Repas"),
        ("breakfast", "Petit dej"),
        ("snack", "10h / 4h"),
        ("dessert", "Dessert"),
        ("other", "Autre"),
    ], string="Catégorie", default="meal", required=True)
