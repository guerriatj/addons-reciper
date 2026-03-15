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


    @http.route('/my/shopping/recipe/new', type='http', auth='user', website=True)
    def create_recipe_page(self, **kw):
        return request.render('reciper-portal.create_recipe_template', {})
