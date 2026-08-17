{
    "name": "Recipe Portal",
    "version": "3.0",
    "depends": ["reciper-core", "portal", "website", "web"],

    "data": [
        "views/recipe_gallery_templates.xml",
        "views/create_recipe_page.xml",
        "views/view_draft_shopping_list.xml",
        "views/view_validated_shopping_list.xml",
        "views/main_page.xml",
        "views/view_all_shopping_list.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'reciper-portal/static/src/js/recipe_gallery.js',
            'reciper-portal/static/src/js/shopping_list_form.js',
            'reciper-portal/static/src/js/shopping_list_line.js',
            'reciper-portal/static/src/js/create_recipe_form.js',
            'reciper-portal/static/src/css/style.css',
        ],
    },
    "installable": True,
    "application": True,
}