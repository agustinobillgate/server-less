#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def mk_rezept_create_rezlinbl(s_artnr:int, qty:Decimal, recipetype:int, price_type:int, descript:string, inhalt:Decimal, lostfact:Decimal, vk_preis:Decimal):

    prepare_cache ([L_artikel])

    warn_flag = 0
    s_rezlin_data = []
    curr_pos:int = 0
    l_artikel = None

    s_rezlin = None

    s_rezlin_data, S_rezlin = create_model("S_rezlin", {"pos":int, "artnr":int, "bezeich":string, "s_unit":string, "masseinheit":string, "menge":Decimal, "cost":Decimal, "vk_preis":Decimal, "inhalt":Decimal, "lostfact":Decimal, "recipe_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal warn_flag, s_rezlin_data, curr_pos, l_artikel
        nonlocal s_artnr, qty, recipetype, price_type, descript, inhalt, lostfact, vk_preis


        nonlocal s_rezlin
        nonlocal s_rezlin_data

        return {"warn_flag": warn_flag, "s-rezlin": s_rezlin_data}

    def create_rezlin():

        nonlocal warn_flag, s_rezlin_data, curr_pos, l_artikel
        nonlocal s_artnr, qty, recipetype, price_type, descript, inhalt, lostfact, vk_preis


        nonlocal s_rezlin
        nonlocal s_rezlin_data

        cost:Decimal = to_decimal("0.0")
        curr_pos = curr_pos + 1
        s_rezlin = S_rezlin()
        s_rezlin_data.append(s_rezlin)

        s_rezlin.pos = curr_pos
        s_rezlin.artnr = s_artnr
        s_rezlin.bezeich = descript
        s_rezlin.menge =  to_decimal(qty)
        s_rezlin.lostfact =  to_decimal(lostfact)

        if recipetype == 1:

            if price_type == 0 or l_artikel.ek_aktuell == 0:
                vk_preis =  to_decimal(l_artikel.vk_preis)
            else:
                vk_preis =  to_decimal(l_artikel.ek_aktuell)
            s_rezlin.masseinheit = l_artikel.masseinheit
            s_rezlin.s_unit = entry(1, l_artikel.herkunft, ";")
            s_rezlin.inhalt =  to_decimal(l_artikel.inhalt)
            s_rezlin.vk_preis =  to_decimal(vk_preis)
            s_rezlin.cost =  to_decimal(qty) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis)

            if s_rezlin.s_unit == "" and s_rezlin.inhalt == 1:
                s_rezlin.s_unit = s_rezlin.masseinheit

            if lostfact != 0:
                s_rezlin.cost =  to_decimal(s_rezlin.cost) / to_decimal((1) - to_decimal(lostfact) / to_decimal(100))

            if s_rezlin.cost == 0:
                warn_flag = 1

        elif recipetype == 2:
            s_rezlin.recipe_flag = True
            s_rezlin.inhalt =  to_decimal(inhalt)
            s_rezlin.cost =  to_decimal(qty) * to_decimal(vk_preis)

            if s_rezlin.cost == 0:
                warn_flag = 2


    if recipetype == 1:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
    create_rezlin()

    return generate_output()