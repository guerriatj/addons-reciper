from odoo import http
from odoo.http import request
from datetime import date


class ShoppingWebController(http.Controller):
    @http.route('/my/shopping/list/new', type='http', auth='user', website=True)
    def create_shopping_list_page(self, **kw):
        shopping_list = request.env['shopping.list'].sudo().create({})
        return request.redirect(f"/my/view_shopping_list?shopping_list_id={shopping_list.id}")

    @http.route("/my/view_shopping_list", type='http', auth='user', website=True)
    def view_one_sopping_list(self, shopping_list_id=None, **kw):
        shopping_list = request.env['shopping.list'].sudo().browse(int(shopping_list_id))

        if shopping_list.state == "draft":
            return self.display_draft_shopping_list(shopping_list)
        else:
            return self.display_confirmed_shopping_list(shopping_list)


    def display_draft_shopping_list(self, shopping_list):
        recipes = request.env['recipe'].sudo().search([])
        ingredients = request.env['recipe.ingredient'].sudo().search([])
        uoms = request.env['uom.uom'].sudo().search([])
        stores = request.env['store'].sudo().search([])

        return request.render('reciper-portal.shopping_list_draft', {
            'shopping_list': shopping_list,
            'stores': stores,
            'recipes': recipes,
            'ingredients': ingredients,
            'uoms': uoms,
        })

    def display_confirmed_shopping_list(self, shopping_list):

        lines = request.env["shopping.list.line"].sudo().search(
            [("shopping_list_id", "=", shopping_list.id)],
        )

        return request.render(
            "reciper-portal.shopping_list_confirmed",
            {
                "shopping_list": shopping_list,
            },
        )

    @http.route("/my/shopping_list/post", type='http', auth='user', website=True, methods=['POST'])
    def post_shopping_list(self, shopping_list_id=None, **kw):
        shopping_list_id = request.params.get("shopping_list_id")
        shopping_list = request.env['shopping.list'].browse(int(shopping_list_id))
        form = request.httprequest.form

        shopping_list.create_recipe_lines(form)
        shopping_list.create_ingredient_lines(form)

        if kw.get("state") == "confirmed":
            shopping_list.action_generate_from_recipes()
            shopping_list.action_confirm()

        if kw.get("store_id"):
            shopping_list.write({"store_id": int(kw.get("store_id"))})

        shopping_list.write({"notes":kw.get("notes")})

        return request.redirect(f"/my/view_shopping_list?shopping_list_id={shopping_list.id}")


    @http.route(
        "/shopping_list/toggle_line",
        type="json",
        auth="user",
        website=True,
    )
    def toggle_line(self, line_id):
        line = request.env["shopping.list.line"].sudo().browse(int(line_id))
        if not line.exists():
            return {"success": False}

        line.is_picked = not line.is_picked
        return {
            "success": True,
            "is_picked": line.is_picked,
        }
