from odoo import http
from odoo.http import request
from datetime import date


class ShoppingWebController(http.Controller):

    @http.route('/my/shopping', type='http', auth='user', website=True)
    def shopping_page(self, **kw):
        return request.render('reciper-portal.shopping_page_template', {})

    @http.route('/my/shopping/list', type='http', auth='user', website=True)
    def shopping_list_page(self, **kw):
        return request.render('reciper-portal.shopping_list_template', {})

    @http.route('/my/shopping/list/new', type='http', auth='user', website=True)
    def create_shopping_list_page(self, **kw):
        # Créer une shopping list avec date du jour
        shopping_list = request.env['shopping.list'].sudo().create({
            'date': date.today(),
        })
        return self.view_one_sopping_list(shopping_list.id)

    @http.route("/my/view_shopping_list", type='http', auth='user', website=True)
    def view_one_sopping_list(self, shopping_list_id=None, **kw):
        shopping_list = request.env['shopping.list'].sudo().browse(shopping_list_id)
        # Récupérer toutes les recettes et ingrédients pour le formulaire
        recipes = request.env['recipe'].sudo().search([])
        ingredients = request.env['recipe.ingredient'].sudo().search([])

        return request.render('reciper-portal.create_shopping_list_template', {
            'shopping_list': shopping_list,
            'recipes': recipes,
            'ingredients': ingredients,
        })

    @http.route('/my/shopping/recipe/new', type='http', auth='user', website=True)
    def create_recipe_page(self, **kw):
        return request.render('reciper-portal.create_recipe_template', {})