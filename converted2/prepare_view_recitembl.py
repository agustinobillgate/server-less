#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, Htparam, H_rezlin, L_artikel

def prepare_view_recitembl(artnr:int, curr_i:int):

    prepare_cache ([H_rezept, Htparam, H_rezlin, L_artikel])

    t_str = ""
    o_portion = 0
    price_type = 0
    amount = to_decimal("0.0")
    amount1 = to_decimal("0.0")
    h_list_data = []
    curr_artnr:int = 0
    h_rezept = htparam = h_rezlin = l_artikel = None

    h_list = None

    h_list_data, H_list = create_model("H_list", {"str":string, "portion":int, "artnr":int, "bezeich":string, "lostfact":Decimal, "menge":Decimal, "cost":Decimal, "r_artnr":int, "r_flag":bool, "costportion":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_str, o_portion, price_type, amount, amount1, h_list_data, curr_artnr, h_rezept, htparam, h_rezlin, l_artikel
        nonlocal artnr, curr_i


        nonlocal h_list
        nonlocal h_list_data

        return {"t_str": t_str, "o_portion": o_portion, "price_type": price_type, "amount": amount, "amount1": amount1, "h-list": h_list_data}

    def create_list(p_artnr:int, menge:Decimal):

        nonlocal t_str, o_portion, price_type, amount, amount1, h_list_data, curr_artnr, h_rezept, htparam, h_rezlin, l_artikel
        nonlocal artnr, curr_i


        nonlocal h_list
        nonlocal h_list_data

        c_artnr:int = 0
        cost:Decimal = to_decimal("0.0")
        h_recipe = None
        hrecipe = None
        t_h_rezlin = None
        i:int = 0
        H_recipe =  create_buffer("H_recipe",H_rezept)
        Hrecipe =  create_buffer("Hrecipe",H_rezept)
        T_h_rezlin =  create_buffer("T_h_rezlin",H_rezlin)

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

            if h_rezlin.recipe_flag :
                curr_artnr = p_artnr
                h_list = H_list()
                h_list_data.append(h_list)

                h_list.r_artnr = p_artnr

                h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})
                h_list.artnr = h_recipe.artnrrezept
                h_list.bezeich = h_recipe.bezeich
                h_list.menge =  to_decimal(h_rezlin.menge)
                h_list.portion = h_recipe.portion
                h_list.r_flag = True
                h_list.str = to_string(h_list.artnr, ">>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(" ", "x(12)") + to_string(h_list.menge, ">>>,>>9.999")
                create_list(h_rezlin.artnrlager, menge * h_rezlin.menge / h_recipe.portion)
            else:
                h_list = H_list()
                h_list_data.append(h_list)


                h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, p_artnr)]})

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                t_h_rezlin = get_cache (H_rezlin, {"artnrrezept": [(eq, curr_artnr)],"artnrlager": [(eq, p_artnr)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost = ( to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.vk_preis)) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                else:
                    cost = ( to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.ek_aktuell)) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                amount =  to_decimal(amount) + to_decimal(cost)
                h_list.r_artnr = p_artnr
                h_list.artnr = l_artikel.artnr
                h_list.bezeich = l_artikel.bezeich
                h_list.lostfact =  to_decimal(h_rezlin.lostfact)
                h_list.menge =  to_decimal(h_rezlin.menge) * to_decimal(menge)
                h_list.cost =  to_decimal(cost)

                if t_h_rezlin and t_h_rezlin.recipe_flag :
                    h_list.costportion =  to_decimal(cost) / to_decimal(o_portion)
                else:
                    h_list.costportion =  to_decimal(cost) / to_decimal(o_portion)
                h_list.str = to_string(h_list.artnr, "9999999") + to_string(h_list.bezeich, "x(31)") + to_string(h_list.lostfact, "99.99") + to_string(h_list.menge, ">>>,>>9.999") + to_string(h_list.cost, ">,>>>,>>>,>>9.99") + to_string(h_list.costportion, ">,>>>,>>>,>>9.99")


    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, artnr)]})
    t_str = "Recipe Items - " + to_string(artnr) + " " + trim(substring(h_rezept.bezeich, 0, 24)) + " (Portion " + to_string(h_rezept.portion) + ")"
    o_portion = h_rezept.portion

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger
    amount =  to_decimal("0")
    create_list(artnr, curr_i)
    amount1 =  to_decimal(amount) / to_decimal(o_portion)

    return generate_output()