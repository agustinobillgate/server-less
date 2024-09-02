from functions.additional_functions import *
import decimal
from models import L_artikel, H_rezlin

def ins_rezept_create_rezlinbl(artnr:int, h_artnr:int, s_artnr:int, qty:decimal, recipetype:int, price_type:int, inhalt:decimal, descript:str, lostfact:decimal):
    warn_flag = 0
    vk_preis = 0
    s_rezlin_list = []
    curr_pos:int = 0
    l_artikel = h_rezlin = None

    s_rezlin = None

    s_rezlin_list, S_rezlin = create_model("S_rezlin", {"new_created":bool, "h_recid":int, "pos":int, "artnr":int, "bezeich":str, "masseinheit":str, "inhalt":decimal, "vk_preis":decimal, "cost":decimal, "menge":decimal, "lostfact":decimal, "recipe_flag":bool, "s_unit":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal warn_flag, vk_preis, s_rezlin_list, curr_pos, l_artikel, h_rezlin


        nonlocal s_rezlin
        nonlocal s_rezlin_list
        return {"warn_flag": warn_flag, "vk_preis": vk_preis, "s-rezlin": s_rezlin_list}

    def create_rezlin():

        nonlocal warn_flag, vk_preis, s_rezlin_list, curr_pos, l_artikel, h_rezlin


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
        s_rezlin.new_created = True

        if recipetype == 1:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == artnr)).first()

            if price_type == 0 or l_artikel.ek_aktuell == 0:
                vk_preis = l_artikel.vk_preis
            else:
                vk_preis = l_artikel.ek_aktuell
            s_rezlin.masseinheit = to_string(l_artikel.masseinheit, "x(3)")
            s_rezlin.inhalt = l_artikel.inhalt
            s_rezlin.vk_preis = vk_preis
            s_rezlin.cost = qty / l_artikel.inhalt * vk_preis / (1 - s_rezlin.lostfact / 100)

            if num_entries(l_artikel.herkunft, ";") > 1:
                s_rezlin.s_unit = entry(1, l_artikel.herkunft, ";")

            if s_rezlin.s_unit == " ":
                s_rezlin.s_unit = l_artikel.masseinheit

            if s_rezlin.cost == 0:
                warn_flag = 1

        elif recipetype == 2:
            s_rezlin.recipe_flag = True
            s_rezlin.inhalt = inhalt
            s_rezlin.cost = qty * vk_preis

            if s_rezlin.cost == 0:
                warn_flag = 2
        h_rezlin = H_rezlin()
        db_session.add(h_rezlin)

        h_rezlin.artnrrezept = h_artnr
        h_rezlin.artnrlager = s_rezlin.artnr
        h_rezlin.menge = s_rezlin.menge
        h_rezlin.lostfact = s_rezlin.lostfact
        h_rezlin.recipe_flag = s_rezlin.recipe_flag

        h_rezlin = db_session.query(H_rezlin).first()
        s_rezlin.h_recid = h_rezlin._recid


    create_rezlin()

    return generate_output()