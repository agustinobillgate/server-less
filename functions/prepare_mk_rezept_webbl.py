#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, H_rezept, Htparam, H_rezlin

t_artikel_data, T_artikel = create_model("T_artikel", {"artnr_no":string})

def prepare_mk_rezept_webbl(t_artikel_data:[T_artikel]):

    prepare_cache ([Htparam, H_rezlin])

    price_type = 0
    t_l_artikel_data = []
    t_h_rezept_data = []
    cost_list_data = []
    curr_i:int = 0
    l_artikel = h_rezept = htparam = h_rezlin = None

    t_l_artikel = t_h_rezept = cost_list = t_artikel = h_recipe = hrecipe = None

    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)
    t_h_rezept_data, T_h_rezept = create_model_like(H_rezept, {"cost_percent":Decimal, "poten_sell_price":Decimal})
    cost_list_data, Cost_list = create_model("Cost_list", {"artnrrezept":int, "cost":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_type, t_l_artikel_data, t_h_rezept_data, cost_list_data, curr_i, l_artikel, h_rezept, htparam, h_rezlin


        nonlocal t_l_artikel, t_h_rezept, cost_list, t_artikel, h_recipe, hrecipe
        nonlocal t_l_artikel_data, t_h_rezept_data, cost_list_data

        return {"price_type": price_type, "t-l-artikel": t_l_artikel_data, "t-h-rezept": t_h_rezept_data, "cost-list": cost_list_data}

    def create_all():

        nonlocal price_type, t_l_artikel_data, t_h_rezept_data, cost_list_data, curr_i, l_artikel, h_rezept, htparam, h_rezlin


        nonlocal t_l_artikel, t_h_rezept, cost_list, t_artikel, h_recipe, hrecipe
        nonlocal t_l_artikel_data, t_h_rezept_data, cost_list_data

        for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():
            t_l_artikel = T_l_artikel()
            t_l_artikel_data.append(t_l_artikel)

            buffer_copy(l_artikel, t_l_artikel)

        for h_rezept in db_session.query(H_rezept).order_by(H_rezept._recid).all():
            t_h_rezept = T_h_rezept()
            t_h_rezept_data.append(t_h_rezept)

            buffer_copy(h_rezept, t_h_rezept)


    def create_list():

        nonlocal price_type, t_l_artikel_data, t_h_rezept_data, cost_list_data, curr_i, l_artikel, h_rezept, htparam, h_rezlin


        nonlocal t_l_artikel, t_h_rezept, cost_list, t_artikel, h_recipe, hrecipe
        nonlocal t_l_artikel_data, t_h_rezept_data, cost_list_data

        h_rezlin_obj_list = {}
        for h_rezlin, h_rezept in db_session.query(H_rezlin, H_rezept).join(H_rezept,(H_rezept.artnrrezept == H_rezlin.artnrrezept)).filter(
                 (H_rezlin.artnrlager == l_artikel.artnr)).order_by(H_rezlin._recid).all():
            if h_rezlin_obj_list.get(h_rezlin._recid):
                continue
            else:
                h_rezlin_obj_list[h_rezlin._recid] = True

            if h_rezlin.recipe_flag:

                t_h_rezept = query(t_h_rezept_data, filters=(lambda t_h_rezept: t_h_rezept.artnrrezept == h_rezlin.artnrlager), first=True)

                if not t_h_rezept:
                    create_list()
            else:
                t_h_rezept = T_h_rezept()
                t_h_rezept_data.append(t_h_rezept)

                buffer_copy(h_rezept, t_h_rezept)


    def calculate_cost():

        nonlocal price_type, t_l_artikel_data, t_h_rezept_data, cost_list_data, curr_i, l_artikel, h_rezept, htparam, h_rezlin


        nonlocal t_l_artikel, t_h_rezept, cost_list, t_artikel, h_recipe, hrecipe
        nonlocal t_l_artikel_data, t_h_rezept_data, cost_list_data

        amount:Decimal = to_decimal("0.0")

        for t_h_rezept in query(t_h_rezept_data):
            curr_i = 0

            cost_list = query(cost_list_data, filters=(lambda cost_list: cost_list.artnrrezept == t_h_rezept.artnrrezept), first=True)

            if not cost_list:
                cost_list = Cost_list()
                cost_list_data.append(cost_list)

                cost_list.artnrrezept = t_h_rezept.artnrrezept
                amount =  to_decimal("0")
                amount = cal_cost(t_h_rezept.artnrrezept, 1, amount)
                cost_list.cost =  to_decimal(amount)


    def cal_cost(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal price_type, t_l_artikel_data, t_h_rezept_data, cost_list_data, curr_i, l_artikel, h_rezept, htparam, h_rezlin


        nonlocal t_l_artikel, t_h_rezept, cost_list, t_artikel, h_recipe, hrecipe
        nonlocal t_l_artikel_data, t_h_rezept_data, cost_list_data

        inh:Decimal = to_decimal("0.0")
        i:int = 0

        def generate_inner_output():
            return (cost)

        H_recipe = T_h_rezept
        h_recipe_data = t_h_rezept_data
        Hrecipe = T_h_rezept
        hrecipe_data = t_h_rezept_data

        h_recipe = query(h_recipe_data, filters=(lambda h_recipe: h_recipe.artnrrezept == p_artnr), first=True)

        if h_recipe:

            for h_rezlin in db_session.query(H_rezlin).filter(
                     (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

                if h_rezlin.recipe_flag :

                    hrecipe = query(hrecipe_data, filters=(lambda hrecipe: hrecipe.artnrrezept == h_rezlin.artnrlager), first=True)

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger

    for l_artikel in db_session.query(L_artikel).filter(
             (L_artikel.herkunft == "")).order_by(L_artikel._recid).all():
        l_artikel.herkunft = ";;"


    pass

    t_artikel = query(t_artikel_data, first=True)

    if t_artikel.artnr_no != "":

        t_artikel = query(t_artikel_data, first=True)

        l_artikel = db_session.query(L_artikel).filter(
                 (to_string(L_artikel.artnr) == t_artikel.artnr_no)).first()

        if l_artikel:
            create_list()
            calculate_cost()
    else:
        create_all()
        calculate_cost()

    return generate_output()