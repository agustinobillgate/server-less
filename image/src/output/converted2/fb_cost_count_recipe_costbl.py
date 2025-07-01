#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, H_rezlin, L_artikel

def fb_cost_count_recipe_costbl(grid_list_artnrrezept:int, price_type:int, amount:Decimal):

    prepare_cache ([H_rezept, H_rezlin, L_artikel])

    portion:Decimal = 1
    vk_preis:Decimal = to_decimal("0.0")
    h_rezept = h_rezlin = l_artikel = None

    s_rezlin = h_recipe = None

    s_rezlin_list, S_rezlin = create_model("S_rezlin", {"h_recid":int, "pos":int, "artnr":int, "bezeich":string, "masseinheit":string, "inhalt":Decimal, "vk_preis":Decimal, "cost":Decimal, "menge":Decimal, "lostfact":Decimal, "recipe_flag":bool})

    H_recipe = create_buffer("H_recipe",H_rezept)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal portion, vk_preis, h_rezept, h_rezlin, l_artikel
        nonlocal grid_list_artnrrezept, price_type, amount
        nonlocal h_recipe


        nonlocal s_rezlin, h_recipe
        nonlocal s_rezlin_list

        return {"amount": amount}

    def cal_cost(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal portion, h_rezept, h_rezlin, l_artikel
        nonlocal grid_list_artnrrezept, price_type, amount
        nonlocal h_recipe


        nonlocal s_rezlin, h_recipe
        nonlocal s_rezlin_list

        inh:Decimal = to_decimal("0.0")
        vk_preis:Decimal = to_decimal("0.0")
        h_rezlin1 = None

        def generate_inner_output():
            return (cost)

        H_rezlin1 =  create_buffer("H_rezlin1",H_rezlin)

        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, p_artnr)]})

        for h_rezlin1 in db_session.query(H_rezlin1).filter(
                 (H_rezlin1.artnrrezept == p_artnr)).order_by(H_rezlin1._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin1.menge)

            if h_rezlin1.recipe_flag :
                cost = cal_cost(h_rezlin1.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin1.artnrlager)]})

                if l_artikel:

                    if price_type == 0 or l_artikel.ek_aktuell == 0:
                        vk_preis =  to_decimal(l_artikel.vk_preis)
                    else:
                        vk_preis =  to_decimal(l_artikel.ek_aktuell)
                    cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal(h_rezept.portion) / to_decimal((1) - to_decimal(h_rezlin1.lostfact) / to_decimal(100))

        return generate_inner_output()

    pass

    if grid_list_artnrrezept != 0:

        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, grid_list_artnrrezept)]})

    if h_rezept:
        portion =  to_decimal(h_rezept.portion)

    for h_rezlin in db_session.query(H_rezlin).filter(
             (H_rezlin.artnrrezept == grid_list_artnrrezept)).order_by(H_rezlin._recid).all():
        s_rezlin = S_rezlin()
        s_rezlin_list.append(s_rezlin)

        s_rezlin.artnr = h_rezlin.artnrlager
        s_rezlin.menge =  to_decimal(h_rezlin.menge) / to_decimal(portion)
        s_rezlin.lostfact =  to_decimal(h_rezlin.lostfact)

        if h_rezlin.recipe_flag == False:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

            if l_artikel:

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    vk_preis =  to_decimal(l_artikel.ek_aktuell)
                s_rezlin.bezeich = l_artikel.bezeich
                s_rezlin.masseinheit = to_string(l_artikel.masseinheit, "x(3)")
                s_rezlin.inhalt =  to_decimal(l_artikel.inhalt)
                s_rezlin.vk_preis =  to_decimal(vk_preis)
                s_rezlin.cost =  to_decimal(h_rezlin.menge) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal(portion) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))

        elif h_rezlin.recipe_flag :

            h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})
            s_rezlin.bezeich = h_recipe.bezeich
            s_rezlin.recipe_flag = True
            s_rezlin.inhalt =  to_decimal("1")
            cost = 0
            cost = cal_cost(h_rezlin.artnrlager, 1, cost)
            s_rezlin.cost =  to_decimal(h_rezlin.menge) * to_decimal(cost)
        amount =  to_decimal(amount) + to_decimal(s_rezlin.cost)

    return generate_output()