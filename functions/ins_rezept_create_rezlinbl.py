#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, H_rezlin

def ins_rezept_create_rezlinbl(artnr:int, h_artnr:int, s_artnr:int, qty:Decimal, recipetype:int, price_type:int, inhalt:Decimal, descript:string, lostfact:Decimal):

    prepare_cache ([L_artikel, H_rezlin])

    warn_flag = 0
    vk_preis = to_decimal("0.0")
    s_rezlin_data = []
    curr_pos:int = 0
    l_artikel = h_rezlin = None

    s_rezlin = None

    s_rezlin_data, S_rezlin = create_model("S_rezlin", {"new_created":bool, "h_recid":int, "pos":int, "artnr":int, "bezeich":string, "masseinheit":string, "inhalt":Decimal, "vk_preis":Decimal, "cost":Decimal, "menge":Decimal, "lostfact":Decimal, "recipe_flag":bool, "s_unit":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal warn_flag, vk_preis, s_rezlin_data, curr_pos, l_artikel, h_rezlin
        nonlocal artnr, h_artnr, s_artnr, qty, recipetype, price_type, inhalt, descript, lostfact


        nonlocal s_rezlin
        nonlocal s_rezlin_data

        return {"warn_flag": warn_flag, "vk_preis": vk_preis, "s-rezlin": s_rezlin_data}

    def create_rezlin():

        nonlocal warn_flag, vk_preis, s_rezlin_data, curr_pos, l_artikel, h_rezlin
        nonlocal artnr, h_artnr, s_artnr, qty, recipetype, price_type, inhalt, descript, lostfact


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
        s_rezlin.new_created = True

        if recipetype == 1:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, artnr)]})

            if price_type == 0 or l_artikel.ek_aktuell == 0:
                vk_preis =  to_decimal(l_artikel.vk_preis)
            else:
                vk_preis =  to_decimal(l_artikel.ek_aktuell)
            s_rezlin.masseinheit = to_string(l_artikel.masseinheit, "x(3)")
            s_rezlin.inhalt =  to_decimal(l_artikel.inhalt)
            s_rezlin.vk_preis =  to_decimal(vk_preis)
            s_rezlin.cost =  to_decimal(qty) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal((1) - to_decimal(s_rezlin.lostfact) / to_decimal(100))

            if num_entries(l_artikel.herkunft, ";") > 1:
                s_rezlin.s_unit = entry(1, l_artikel.herkunft, ";")

            if s_rezlin.s_unit == " ":
                s_rezlin.s_unit = l_artikel.masseinheit

            if s_rezlin.cost == 0:
                warn_flag = 1

        elif recipetype == 2:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, artnr)]})

            if price_type == 0 or l_artikel.ek_aktuell == 0:
                vk_preis =  to_decimal(l_artikel.vk_preis)
            else:
                vk_preis =  to_decimal(l_artikel.ek_aktuell)
            s_rezlin.recipe_flag = True
            s_rezlin.inhalt =  to_decimal(inhalt)
            s_rezlin.cost =  to_decimal(qty) * to_decimal(vk_preis)

            if s_rezlin.cost == 0:
                warn_flag = 2
        h_rezlin = H_rezlin()
        db_session.add(h_rezlin)

        h_rezlin.artnrrezept = h_artnr
        h_rezlin.artnrlager = s_rezlin.artnr
        h_rezlin.menge =  to_decimal(s_rezlin.menge)
        h_rezlin.lostfact =  to_decimal(s_rezlin.lostfact)
        h_rezlin.recipe_flag = s_rezlin.recipe_flag
        pass
        s_rezlin.h_recid = h_rezlin._recid

    create_rezlin()

    return generate_output()