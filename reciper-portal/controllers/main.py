from odoo import http
from odoo.http import request
from datetime import date
import base64

# Doit correspondre à la clé "other" de fields.Selection sur recipe.category
# (utilisé pour rattacher les anciennes recettes sans catégorie à l'onglet
# "Autre" plutôt que de les faire disparaître de la galerie).
DEFAULT_RECIPE_CATEGORY = 'other'


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
            'categories': request.env['recipe']._fields['category'].selection,
            'default_category': DEFAULT_RECIPE_CATEGORY,
        })

    @http.route('/my/shopping/list', type='http', auth='user', website=True)
    def shopping_list_page(self, **kw):
        shopping_lists = request.env['shopping.list'].sudo().search([], order='date desc')
        return request.render('reciper-portal.shopping_list_template', {
            'shopping_lists': shopping_lists,
        })

    @http.route('/my/shopping/recipe/new', type='http', auth='user', website=True)
    def create_recipe_page(self, **kw):
        ingredients = request.env['recipe.ingredient'].sudo().search([])
        categories = request.env['recipe']._fields['category'].selection
        return request.render('reciper-portal.create_recipe_template', {
            'ingredients': ingredients,
            'categories': categories,
        })

    @http.route('/my/shopping/recipe/create', type='http', auth='user', website=True, methods=['POST'])
    def create_recipe(self, **kw):
        form = request.httprequest.form

        vals = {
            'name': form.get('name'),
            'people_count': int(form.get('people_count') or 1),
            'category': form.get('category') or DEFAULT_RECIPE_CATEGORY,
            'instructions': form.get('instructions') or '',
        }

        image_file = request.httprequest.files.get('image')
        if image_file and image_file.filename:
            vals['image'] = base64.b64encode(image_file.read())

        recipe = request.env['recipe'].sudo().create(vals)

        ingredient_ids = form.getlist('ingredient_id')
        quantities = form.getlist('quantity')

        line_vals = []
        for ingredient_id, quantity in zip(ingredient_ids, quantities):
            if not ingredient_id:
                continue
            line_vals.append({
                'recipe_id': recipe.id,
                'recipe_ingredient_id': int(ingredient_id),
                'quantity': float(quantity or 0),
            })
        if line_vals:
            request.env['recipe.line'].sudo().create(line_vals)

        return request.redirect('/my/shopping')

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
