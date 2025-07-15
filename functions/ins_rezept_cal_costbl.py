#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezlin, L_artikel

def ins_rezept_cal_costbl(p_artnr:int, menge:Decimal, price_type:int, cost:Decimal):

    prepare_cache ([H_rezlin, L_artikel])

    h_rezlin = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezlin, l_artikel
        nonlocal p_artnr, menge, price_type, cost

        return {"cost": cost}

    def cal_cost():

        nonlocal h_rezlin, l_artikel
        nonlocal p_artnr, menge, price_type, cost

        inh:Decimal = to_decimal("0.0")
        vk_preis:Decimal = to_decimal("0.0")
        h_rezlin1 = None
        H_rezlin1 =  create_buffer("H_rezlin1",H_rezlin)

        for h_rezlin1 in db_session.query(H_rezlin1).filter(
                 (H_rezlin1.artnrrezept == p_artnr)).order_by(H_rezlin1._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin1.menge)

            if h_rezlin1.recipe_flag :
                cost = cal_cost2(h_rezlin1.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin1.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    vk_preis =  to_decimal(l_artikel.ek_aktuell)
                cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal((1) - to_decimal(h_rezlin1.lostfact) / to_decimal(100))


    def cal_cost2():

        nonlocal h_rezlin, l_artikel
        nonlocal p_artnr, menge, price_type, cost

        inh:Decimal = to_decimal("0.0")
        vk_preis:Decimal = to_decimal("0.0")
        h_rezlin1 = None
        H_rezlin1 =  create_buffer("H_rezlin1",H_rezlin)

        for h_rezlin1 in db_session.query(H_rezlin1).filter(
                 (H_rezlin1.artnrrezept == p_artnr)).order_by(H_rezlin1._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin1.menge)

            if h_rezlin1.recipe_flag :
                cost = cal_cost2(h_rezlin1.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin1.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    vk_preis =  to_decimal(l_artikel.ek_aktuell)
                cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal((1) - to_decimal(h_rezlin1.lostfact) / to_decimal(100))


    cal_cost()

    return generate_output()