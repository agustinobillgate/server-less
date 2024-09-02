from functions.additional_functions import *
import decimal
from models import L_artikel

def mk_rezept_create_rezlinbl(s_artnr:int, qty:decimal, recipetype:int, price_type:int, descript:str, inhalt:decimal, lostfact:decimal, vk_preis:decimal):
    warn_flag = 0
    s_rezlin_list = []
    curr_pos:int = 0
    l_artikel = None

    s_rezlin = None

    s_rezlin_list, S_rezlin = create_model("S_rezlin", {"pos":int, "artnr":int, "bezeich":str, "s_unit":str, "masseinheit":str, "menge":decimal, "cost":decimal, "vk_preis":decimal, "inhalt":decimal, "lostfact":decimal, "recipe_flag":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal warn_flag, s_rezlin_list, curr_pos, l_artikel


        nonlocal s_rezlin
        nonlocal s_rezlin_list
        return {"warn_flag": warn_flag, "s-rezlin": s_rezlin_list}

    def create_rezlin():

        nonlocal warn_flag, s_rezlin_list, curr_pos, l_artikel


        nonlocal s_rezlin
        nonlocal s_rezlin_list

        cost:decimal = 0
        curr_pos = curr_pos + 1
        s_rezlin = S_rezlin()
        s_rezlin_list.append(s_rezlin)

        s_rezlin.pos = curr_pos
        s_rezlin.artnr = s_artnr
        s_rezlin.bezeich = descript
        s_rezlin.menge = qty
        s_rezlin.lostfact = lostfact

        if recipetype == 1:

            if price_type == 0 or l_artikel.ek_aktuell == 0:
                vk_preis = l_artikel.vk_preis
            else:
                vk_preis = l_artikel.ek_aktuell
            s_rezlin.masseinheit = l_artikel.masseinheit
            s_rezlin.s_unit = entry(1, l_artikel.herkunft, ";")
            s_rezlin.inhalt = l_artikel.inhalt
            s_rezlin.vk_preis = vk_preis
            s_rezlin.cost = qty / l_artikel.inhalt * vk_preis

            if s_rezlin.s_unit == "" and s_rezlin.inhalt == 1:
                s_rezlin.s_unit = s_rezlin.masseinheit

            if lostfact != 0:
                s_rezlin.cost = s_rezlin.cost / (1 - lostfact / 100)

            if s_rezlin.cost == 0:
                warn_flag = 1

        elif recipetype == 2:
            s_rezlin.recipe_flag = True
            s_rezlin.inhalt = inhalt
            s_rezlin.cost = qty * vk_preis

            if s_rezlin.cost == 0:
                warn_flag = 2

    if recipetype == 1:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == s_artnr)).first()
    create_rezlin()

    return generate_output()