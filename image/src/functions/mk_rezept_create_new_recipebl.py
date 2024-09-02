from functions.additional_functions import *
import decimal
from models import H_rezept, H_rezlin

def mk_rezept_create_new_recipebl(s_rezlin:[S_rezlin], h_artnr:int, h_bezeich:str, katbezeich:str, katnr:int, portion:int):
    r_recid = 0
    curr_pos:int = 0
    h_rezept = h_rezlin = None

    s_rezlin = b_rezept = None

    s_rezlin_list, S_rezlin = create_model("S_rezlin", {"pos":int, "artnr":int, "bezeich":str, "s_unit":str, "masseinheit":str, "menge":decimal, "cost":decimal, "vk_preis":decimal, "inhalt":decimal, "lostfact":decimal, "recipe_flag":bool})

    B_rezept = H_rezept

    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_recid, curr_pos, h_rezept, h_rezlin
        nonlocal b_rezept


        nonlocal s_rezlin, b_rezept
        nonlocal s_rezlin_list
        return {"r_recid": r_recid}

    def create_new_recipe():

        nonlocal r_recid, curr_pos, h_rezept, h_rezlin
        nonlocal b_rezept


        nonlocal s_rezlin, b_rezept
        nonlocal s_rezlin_list

        i:int = 0
        j:int = 0
        h_rezept = H_rezept()
        db_session.add(h_rezept)

        r_recid = h_rezept._recid
        h_rezept.artnrrezept = h_artnr
        h_rezept.bezeich = h_bezeich
        j = len(h_rezept.bezeich) + 1
        for i in range(j,24 + 1) :
            h_rezept.bezeich = h_rezept.bezeich + " "
        h_rezept.kategorie = katnr
        h_rezept.datumanlage = get_current_date()
        h_rezept.portion = portion

        b_rezept = db_session.query(B_rezept).first()

        if b_rezept:

            if num_entries(b_rezept.bezeich, ";") > 1:
                h_rezept.bezeich = h_rezept.bezeich + ";" + katbezeich


            else:
                h_rezept.bezeich = h_rezept.bezeich + katbezeich


        else:
            h_rezept.bezeich = h_rezept.bezeich + ";" + katbezeich

        h_rezept = db_session.query(H_rezept).first()

        for s_rezlin in query(s_rezlin_list):
            h_rezlin = H_rezlin()
            db_session.add(h_rezlin)

            h_rezlin.artnrrezept = h_artnr
            h_rezlin.artnrlager = s_rezlin.artnr
            h_rezlin.menge = s_rezlin.menge
            h_rezlin.lostfact = s_rezlin.lostfact
            h_rezlin.recipe_flag = s_rezlin.recipe_flag

            h_rezlin = db_session.query(H_rezlin).first()
        s_rezlin_list.clear()
        curr_pos = 0


    create_new_recipe()

    return generate_output()