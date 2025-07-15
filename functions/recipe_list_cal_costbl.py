#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, H_rezlin, L_artikel

def recipe_list_cal_costbl(p_artnr:int, menge:Decimal, cost:Decimal, price_type:int):

    prepare_cache ([H_rezept, H_rezlin, L_artikel])

    h_rezept = h_rezlin = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal p_artnr, menge, cost, price_type

        return {"cost": cost}

    def cal_cost(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal price_type

        inh:Decimal = to_decimal("0.0")
        i:int = 0
        h_recipe = None
        hrecipe = None

        def generate_inner_output():
            return (cost)

        H_recipe =  create_buffer("H_recipe",H_rezept)
        Hrecipe =  create_buffer("Hrecipe",H_rezept)

        h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, p_artnr)]})

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

            if h_rezlin.recipe_flag :

                hrecipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})

                if hrecipe.portion > 1:
                    inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(hrecipe.portion)


                else:
                    inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)
                cost = cal_cost(h_rezlin.artnrlager, inh, cost)
            else:
                inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                else:
                    cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.ek_aktuell) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))

        return generate_inner_output()


    cost = cal_cost(p_artnr, menge, cost)

    return generate_output()