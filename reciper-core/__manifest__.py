{
    "name": "Recipe Shopping",
    "version": "3.0",
    "depends": ["base", "uom"],

    "data": [
        "security/groups.xml",
        "security/record_rules.xml",
        "security/ir.model.access.csv",
        "views/ingredient_views.xml",
        "views/recipe_views.xml",
        "views/store_views.xml",
        "views/store_aisle_views.xml",
        "views/shopping_list_views.xml",
        "views/menu.xml",
        "data/uom_uom.xml",
    ],

    "installable": True,
    "application": True,
}