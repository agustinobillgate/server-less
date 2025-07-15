#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, H_rezlin, L_artikel

def mk_rezept_cal_costbl(p_artnr:int, menge:Decimal, cost:Decimal, price_type:int):

    prepare_cache ([H_rezept, H_rezlin, L_artikel])

    h_rezept = h_rezlin = l_artikel = None

    hrecipe = None

    Hrecipe = create_buffer("Hrecipe",H_rezept)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal p_artnr, menge, cost, price_type
        nonlocal hrecipe


        nonlocal hrecipe

        return {"cost": cost}

    def cal_cost():

        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal p_artnr, menge, cost, price_type
        nonlocal hrecipe


        nonlocal hrecipe

        inh:Decimal = to_decimal("0.0")
        vk_preis:Decimal = to_decimal("0.0")

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

            if not h_rezlin.recipe_flag:
                inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
            else:

                hrecipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})

                if hrecipe.portion > 1:
                    inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(hrecipe.portion)


                else:
                    inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)

            if h_rezlin.recipe_flag :
                cost = cal_cost2(h_rezlin.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    vk_preis =  to_decimal(l_artikel.ek_aktuell)
                cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis)


    def cal_cost2(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal price_type
        nonlocal hrecipe


        nonlocal hrecipe

        inh:Decimal = to_decimal("0.0")
        vk_preis:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (cost)


        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

            if not h_rezlin.recipe_flag:
                inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
            else:

                hrecipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})

                if hrecipe.portion > 1:
                    inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(hrecipe.portion)


                else:
                    inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)

            if h_rezlin.recipe_flag :
                cost = cal_cost3(h_rezlin.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    vk_preis =  to_decimal(l_artikel.ek_aktuell)
                cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis)

        return generate_inner_output()


    def cal_cost3(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal price_type
        nonlocal hrecipe


        nonlocal hrecipe

        inh:Decimal = to_decimal("0.0")
        vk_preis:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (cost)


        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

            if not h_rezlin.recipe_flag:
                inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
            else:

                hrecipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})

                if hrecipe.portion > 1:
                    inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(hrecipe.portion)


                else:
                    inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)

            if h_rezlin.recipe_flag :
                cost = cal_cost3(h_rezlin.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    vk_preis =  to_decimal(l_artikel.ek_aktuell)
                cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis)

        return generate_inner_output()


    cal_cost()

    return generate_output()