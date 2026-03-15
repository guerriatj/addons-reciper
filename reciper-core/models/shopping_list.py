from odoo import _, api, models, fields
from odoo.exceptions import ValidationError
from collections import defaultdict


class ShoppingList(models.Model):
    _name = "shopping.list"
    _description = "Shopping List"

    display_name = fields.Char(compute="_compute_display_name")
    date = fields.Date(required=True, default=fields.date.today())
    recipe_ids = fields.Many2many("recipe")
    store_id = fields.Many2one("store")

    shopping_list_recipe_line_ids = fields.One2many("shopping.list.recipe.line", "shopping_list_id")
    shopping_list_ingredient_line_ids = fields.One2many("shopping.list.ingredient.line", "shopping_list_id")

    shopping_list_line_ids = fields.One2many(
        "shopping.list.line",
        "shopping_list_id"
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
        ],
        default="draft",
        required=True
    )

    @api.constrains("shopping_list_recipe_line_ids", "shopping_list_ingredient_line_ids")
    def check_state(self):
        for shopping_list in self:
            if shopping_list.state != "draft":
                raise ValidationError(_("To change the list, please set it to draft state"))

    def _compute_display_name(self):
        for list in self:
            list.display_name = f"Liste de courses {list.date} {list.store_id.name or '(no store selected)'}"

    def action_confirm(self):
        for list in self:
            list.state = "confirmed"

    @api.constrains("shopping_list_recipe_line_ids", "shopping_list_ingredient_line_ids", "store_id")
    def action_generate_from_recipes(self):
        unit_uom = self.env.ref("uom.product_uom_unit")

        for shopping_list in self:
            ingredient_map = defaultdict(float)
            ingredient_recipes_map = defaultdict(set)

            # Recettes ajoutées
            for recipe_line in shopping_list.shopping_list_recipe_line_ids:
                recipe = recipe_line.recipe_id
                if not recipe:
                    continue

                recipe_people = recipe.people_count or 1
                line_people = recipe_line.people_count or recipe_people
                factor = line_people / recipe_people

                for line in recipe.recipe_line_ids:
                    ingredient = line.recipe_ingredient_id
                    uom = line.uom_id or unit_uom
                    qty = line.quantity * factor

                    key = (ingredient.id, uom.id)

                    ingredient_map[key] += qty
                    ingredient_recipes_map[key].add(recipe.id)

            # Ingrédients ajoutés manuellement
            for ingredient_line in shopping_list.shopping_list_ingredient_line_ids:
                ingredient = ingredient_line.ingredient_id
                if not ingredient:
                    continue

                uom = ingredient_line.uom_id or unit_uom
                qty = ingredient_line.ingredient_count or 0

                key = (ingredient.id, uom.id)

                ingredient_map[key] += qty

            lines = []

            for (ingredient_id, uom_id), qty in ingredient_map.items():
                aisle = self.env["store.aisle"].search([
                    ("store_id", "=", shopping_list.store_id.id),
                    ("ingredient_ids", "in", ingredient_id)
                ], limit=1)

                lines.append((0, 0, {
                    "recipe_ingredient_id": ingredient_id,
                    "quantity": qty,
                    "uom_id": uom_id,
                    "aisle_id": aisle.id if aisle else False,
                    "recipe_ids": [(6, 0, list(ingredient_recipes_map.get((ingredient_id, uom_id), [])))],
                }))

            shopping_list.shopping_list_line_ids.unlink()
            shopping_list.shopping_list_line_ids = lines