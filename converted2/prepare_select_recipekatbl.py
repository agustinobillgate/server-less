#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept

def prepare_select_recipekatbl():

    prepare_cache ([H_rezept])

    recipe_data = []
    h_rezept = None

    recipe = None

    recipe_data, Recipe = create_model("Recipe", {"katno":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal recipe_data, h_rezept


        nonlocal recipe
        nonlocal recipe_data

        return {"recipe": recipe_data}

    for h_rezept in db_session.query(H_rezept).order_by(H_rezept.kategorie).all():

        recipe = query(recipe_data, filters=(lambda recipe: recipe.katno == h_rezept.kategorie), first=True)

        if not recipe:
            recipe = Recipe()
            recipe_data.append(recipe)

            recipe.katno = h_rezept.kategorie

            if num_entries(h_rezept.bezeich, ";") > 1:
                recipe.bezeich = entry(1, h_rezept.bezeich, ";")
            else:
                recipe.bezeich = substring(h_rezept.bezeich, 24, 24)

    return generate_output()