#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, Htparam, Queasy, H_rezlin, L_artikel

def prepare_recipe_list_webbl():

    prepare_cache ([H_rezept, Htparam, Queasy, H_rezlin, L_artikel])

    cost_list_list = []
    t_h_rezept_list = []
    price_type:int = 0
    curr_i:int = 0
    h_rezept = htparam = queasy = h_rezlin = l_artikel = None

    cost_list = t_h_rezept = r_list = r1_list = None

    cost_list_list, Cost_list = create_model("Cost_list", {"artnrrezept":int, "cost":Decimal})
    t_h_rezept_list, T_h_rezept = create_model_like(H_rezept, {"cost_percent":Decimal, "poten_sell_price":Decimal})
    r_list_list, R_list = create_model("R_list", {"max_n":int, "recipe_nr":[int,99]})

    R1_list = R_list
    r1_list_list = r_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_list_list, t_h_rezept_list, price_type, curr_i, h_rezept, htparam, queasy, h_rezlin, l_artikel
        nonlocal r1_list


        nonlocal cost_list, t_h_rezept, r_list, r1_list
        nonlocal cost_list_list, t_h_rezept_list, r_list_list

        return {"cost-list": cost_list_list, "t-h-rezept": t_h_rezept_list}

    def calculate_cost():

        nonlocal cost_list_list, t_h_rezept_list, price_type, curr_i, h_rezept, htparam, queasy, h_rezlin, l_artikel
        nonlocal r1_list


        nonlocal cost_list, t_h_rezept, r_list, r1_list
        nonlocal cost_list_list, t_h_rezept_list, r_list_list

        amount:Decimal = to_decimal("0.0")

        for h_rezept in db_session.query(H_rezept).order_by(H_rezept._recid).all():
            buffer_copy(r1_list, r_list)
            curr_i = 0

            cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.artnrrezept == h_rezept.artnrrezept), first=True)

            if not cost_list:
                cost_list = Cost_list()
                cost_list_list.append(cost_list)

                cost_list.artnrrezept = h_rezept.artnrrezept
                amount =  to_decimal("0")
                amount = cal_cost(h_rezept.artnrrezept, 1, amount)
                cost_list.cost =  to_decimal(amount)


    def cal_cost(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal cost_list_list, t_h_rezept_list, price_type, curr_i, h_rezept, htparam, queasy, h_rezlin, l_artikel
        nonlocal r1_list


        nonlocal cost_list, t_h_rezept, r_list, r1_list
        nonlocal cost_list_list, t_h_rezept_list, r_list_list

        inh:Decimal = to_decimal("0.0")
        i:int = 0
        h_recipe = None
        hrecipe = None

        def generate_inner_output():
            return (cost)

        H_recipe =  create_buffer("H_recipe",H_rezept)
        Hrecipe =  create_buffer("Hrecipe",H_rezept)

        h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, p_artnr)]})

        if h_recipe:

            for h_rezlin in db_session.query(H_rezlin).filter(
                     (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

                if h_rezlin.recipe_flag :

                    hrecipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})

                    if hrecipe:

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

    r1_list = R1_list()
    r1_list_list.append(r1_list)

    r_list = R_list()
    r_list_list.append(r_list)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger
    calculate_cost()

    for h_rezept in db_session.query(H_rezept).order_by(H_rezept._recid).all():
        t_h_rezept = T_h_rezept()
        t_h_rezept_list.append(t_h_rezept)

        buffer_copy(h_rezept, t_h_rezept)

        queasy = get_cache (Queasy, {"key": [(eq, 252)],"number1": [(eq, h_rezept.artnrrezept)]})

        if queasy:
            t_h_rezept.cost_percent =  to_decimal(queasy.deci1)
            t_h_rezept.poten_sell_price =  to_decimal(queasy.deci2)

    return generate_output()