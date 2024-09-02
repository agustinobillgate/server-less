from functions.additional_functions import *
import decimal
from models import H_rezept, H_rezlin, H_artikel

def recipe_list_chk_btn_delbl(pvilanguage:int, t_h_rezept_artnrrezept:int):
    msg_str = ""
    lvcarea:str = "recipe_list"
    h_rezept = h_rezlin = h_artikel = None

    h_recipe = None

    H_recipe = H_rezept

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, h_rezept, h_rezlin, h_artikel
        nonlocal h_recipe


        nonlocal h_recipe
        return {"msg_str": msg_str}


    h_rezlin = db_session.query(H_rezlin).filter(
            (H_rezlin.artnrlager == t_h_rezept_artnrrezept)).first()

    if h_rezlin:

        h_recipe = db_session.query(H_recipe).filter(
                (H_recipe.artnrrezept == h_rezlin.artnrrezept)).first()
        msg_str = msg_str + chr(2) + translateExtended ("Deleting not possible, used by other recipe", lvcarea, "") + chr(10) + to_string(h_recipe.artnrrezept) + " - " + h_recipe.bezeich

        return generate_output()

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnrrezept == t_h_rezept_artnrrezept)).first()

    if h_artikel:
        msg_str = msg_str + chr(2) + translateExtended ("Deleting not possible, used by F/B_Article", lvcarea, "") + chr(10) + to_string(h_artikel.artnr) + " - " + h_artikel.bezeich

        return generate_output()