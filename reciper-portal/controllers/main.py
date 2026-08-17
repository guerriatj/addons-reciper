from odoo import http
from odoo.http import request
from datetime import date
import base64


class ShoppingWebController(http.Controller):

    @http.route('/my/shopping', type='http', auth='user', website=True)
    def shopping_page(self, **kw):
        recipes = request.env['recipe'].sudo().search([])

        # Les recettes de la dernière liste de courses confirmée/terminée
        # apparaissent en premier dans la galerie.
        last_list = request.env['shopping.list'].sudo().search(
            [('state', 'in', ('confirmed', 'completed'))],
            order='date desc, id desc',
            limit=1,
        )
        featured_recipe_ids = last_list.shopping_list_recipe_line_ids.recipe_id.ids
        recipes = recipes.sorted(
            key=lambda r: featured_recipe_ids.index(r.id)
            if r.id in featured_recipe_ids else len(featured_recipe_ids)
        )

        return request.render('reciper-portal.shopping_page_template', {
            'recipes': recipes,
            'featured_recipe_ids': featured_recipe_ids,
        })

    @http.route('/my/shopping/list', type='http', auth='user', website=True)
    def shopping_list_page(self, **kw):
        shopping_lists = request.env['shopping.list'].sudo().search([], order='date desc')
        return request.render('reciper-portal.shopping_list_template', {
            'shopping_lists': shopping_lists,
        })

    @http.route('/my/shopping/recipe/new', type='http', auth='user', website=True)
    def create_recipe_page(self, **kw):
        return request.render('reciper-portal.create_recipe_template', {})

    @http.route('/my/recipe/<int:recipe_id>/image', type='http', auth='user', website=True)
    def recipe_image(self, recipe_id, **kw):
        recipe = request.env['recipe'].sudo().browse(recipe_id)
        if not recipe.exists() or not recipe.image:
            return request.not_found()

        image_data = base64.b64decode(recipe.image)
        return request.make_response(
            image_data,
            headers=[
                ('Content-Type', 'image/png'),
                ('Cache-Control', 'public, max-age=3600'),
            ],
        )

    @http.route('/my/recipe/detail', type='json', auth='user', website=True)
    def recipe_detail(self, recipe_id, **kw):
        recipe = request.env['recipe'].sudo().browse(int(recipe_id))
        if not recipe.exists():
            return {}

        return {
            'id': recipe.id,
            'name': recipe.name,
            'people_count': recipe.people_count,
            'image_url': recipe.image and f'/my/recipe/{recipe.id}/image' or False,
            'instructions': recipe.instructions or '',
            'ingredients': [
                {
                    'name': line.recipe_ingredient_id.name,
                    'quantity': line.quantity,
                    'uom': line.uom_id.name or '',
                }
                for line in recipe.recipe_line_ids
            ],
        }
