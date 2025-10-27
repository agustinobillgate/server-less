#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, H_rezlin, L_artikel

def fb_cost_count_recipe_costbl(grid_list_artnrrezept:int, price_type:int, amount:Decimal):

    prepare_cache ([H_rezept, H_rezlin, L_artikel])

    o_portion:int = 0
    curr_i:int = 0
    curr_artnr:int = 0
    recipe_cost:Decimal = to_decimal("0.0")
    h_rezept = h_rezlin = l_artikel = None

    s_rezlin = None

    s_rezlin_data, S_rezlin = create_model("S_rezlin", {"h_recid":int, "pos":int, "artnr":int, "bezeich":string, "masseinheit":string, "inhalt":Decimal, "vk_preis":Decimal, "cost":Decimal, "menge":Decimal, "lostfact":Decimal, "recipe_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal o_portion, curr_i, curr_artnr, recipe_cost, h_rezept, h_rezlin, l_artikel
        nonlocal grid_list_artnrrezept, price_type, amount


        nonlocal s_rezlin
        nonlocal s_rezlin_data

        return {"amount": amount}

    def create_list(p_artnr:int, menge:Decimal):

        nonlocal o_portion, curr_i, curr_artnr, recipe_cost, h_rezept, h_rezlin, l_artikel
        nonlocal grid_list_artnrrezept, price_type, amount


        nonlocal s_rezlin
        nonlocal s_rezlin_data

        c_artnr:int = 0
        cost:Decimal = to_decimal("0.0")
        i:int = 0
        h_recipe = None
        hrecipe = None
        t_h_rezlin = None
        H_recipe =  create_buffer("H_recipe",H_rezept)
        Hrecipe =  create_buffer("Hrecipe",H_rezept)
        T_h_rezlin =  create_buffer("T_h_rezlin",H_rezlin)

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

            if h_rezlin.recipe_flag :
                curr_artnr = p_artnr

                h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})
                create_list(h_rezlin.artnrlager, menge * h_rezlin.menge / h_recipe.portion)
            else:

                h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, p_artnr)]})

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                t_h_rezlin = get_cache (H_rezlin, {"artnrrezept": [(eq, curr_artnr)],"artnrlager": [(eq, p_artnr)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost = ( to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.vk_preis)) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                else:
                    cost = ( to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.ek_aktuell)) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                recipe_cost =  to_decimal(recipe_cost) + to_decimal(cost)


    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, grid_list_artnrrezept)]})

    if h_rezept:
        o_portion = h_rezept.portion
        
    curr_i = 1
    recipe_cost =  to_decimal("0")
    create_list(grid_list_artnrrezept, curr_i)
    amount =  to_decimal(recipe_cost) / to_decimal(o_portion)

    return generate_output()