from functions.additional_functions import *
import decimal
from models import H_rezept

def prepare_select_recipekatbl():
    recipe_list = []
    h_rezept = None

    recipe = None

    recipe_list, Recipe = create_model("Recipe", {"katno":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal recipe_list, h_rezept


        nonlocal recipe
        nonlocal recipe_list
        return {"recipe": recipe_list}

    for h_rezept in db_session.query(H_rezept).all():

        recipe = query(recipe_list, filters=(lambda recipe :recipe.katno == h_rezept.kategorie), first=True)

        if not recipe:
            recipe = Recipe()
            recipe_list.append(recipe)

            recipe.katno = h_rezept.kategorie

            if num_entries(h_rezept.bezeich, ";") > 1:
                recipe.bezeich = entry(1, h_rezept.bezeich, ";")
            else:
                recipe.bezeich = substring(h_rezept.bezeich, 24, 24)

    return generate_output()