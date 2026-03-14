{
    "name": "Recipe Portal",
    "version": "3.0",
    "depends": ["reciper-core", "portal", "website", "web"],

    "data": [
        "views/create_recipe_page.xml",
        "views/view_one_shopping_list.xml",
        "views/main_page.xml",
        "views/view_all_shopping_list.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'web/static/lib/jquery/jquery.js',
            'reciper-portal/static/src/lib/select2.min.css',
            'reciper-portal/static/src/lib/select2.min.js',
            'reciper-portal/static/src/js/shopping_list_form.js',
        ],
    },
    "installable": True,
    "application": True,
}