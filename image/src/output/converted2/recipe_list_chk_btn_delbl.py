#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, H_rezlin, H_artikel

def recipe_list_chk_btn_delbl(pvilanguage:int, t_h_rezept_artnrrezept:int):

    prepare_cache ([H_rezept, H_rezlin, H_artikel])

    msg_str = ""
    lvcarea:string = "recipe-list"
    h_rezept = h_rezlin = h_artikel = None

    h_recipe = None

    H_recipe = create_buffer("H_recipe",H_rezept)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, h_rezept, h_rezlin, h_artikel
        nonlocal pvilanguage, t_h_rezept_artnrrezept
        nonlocal h_recipe


        nonlocal h_recipe

        return {"msg_str": msg_str}


    h_rezlin = get_cache (H_rezlin, {"artnrlager": [(eq, t_h_rezept_artnrrezept)]})

    if h_rezlin:

        h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrrezept)]})
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Deleting not possible, used by other recipe", lvcarea, "") + chr_unicode(10) + to_string(h_recipe.artnrrezept) + " - " + h_recipe.bezeich

        return generate_output()

    h_artikel = get_cache (H_artikel, {"artnrrezept": [(eq, t_h_rezept_artnrrezept)]})

    if h_artikel:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Deleting not possible, used by F/B-Article", lvcarea, "") + chr_unicode(10) + to_string(h_artikel.artnr) + " - " + h_artikel.bezeich

        return generate_output()

    return generate_output()