#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, H_rezept, Htparam, H_rezlin, Queasy

def prepare_ins_rezept_webbl(fr_artnr:int, to_artnr:int, h_artnr:int):

    prepare_cache ([H_rezept, Htparam, H_rezlin, Queasy])

    katnr = 0
    katbezeich = ""
    h_bezeich = ""
    portion = 0
    price_type = 0
    amount = to_decimal("0.0")
    cost_percent = to_decimal("0.0")
    poten_sell_price = to_decimal("0.0")
    t_l_artikel_data = []
    t_h_rezept_data = []
    s_rezlin_data = []
    curr_pos:int = 0
    l_artikel = h_rezept = htparam = h_rezlin = queasy = None

    t_l_artikel = t_h_rezept = s_rezlin = None

    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)
    t_h_rezept_data, T_h_rezept = create_model_like(H_rezept)
    s_rezlin_data, S_rezlin = create_model("S_rezlin", {"new_created":bool, "h_recid":int, "pos":int, "artnr":int, "bezeich":string, "masseinheit":string, "inhalt":Decimal, "vk_preis":Decimal, "cost":Decimal, "menge":Decimal, "lostfact":Decimal, "recipe_flag":bool, "s_unit":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal katnr, katbezeich, h_bezeich, portion, price_type, amount, cost_percent, poten_sell_price, t_l_artikel_data, t_h_rezept_data, s_rezlin_data, curr_pos, l_artikel, h_rezept, htparam, h_rezlin, queasy
        nonlocal fr_artnr, to_artnr, h_artnr


        nonlocal t_l_artikel, t_h_rezept, s_rezlin
        nonlocal t_l_artikel_data, t_h_rezept_data, s_rezlin_data

        return {"katnr": katnr, "katbezeich": katbezeich, "h_bezeich": h_bezeich, "portion": portion, "price_type": price_type, "amount": amount, "cost_percent": cost_percent, "poten_sell_price": poten_sell_price, "t-l-artikel": t_l_artikel_data, "t-h-rezept": t_h_rezept_data, "s-rezlin": s_rezlin_data}

    def create_list():

        nonlocal katnr, katbezeich, h_bezeich, portion, price_type, amount, cost_percent, poten_sell_price, t_l_artikel_data, t_h_rezept_data, s_rezlin_data, curr_pos, l_artikel, h_rezept, htparam, h_rezlin, queasy
        nonlocal fr_artnr, to_artnr, h_artnr


        nonlocal t_l_artikel, t_h_rezept, s_rezlin
        nonlocal t_l_artikel_data, t_h_rezept_data, s_rezlin_data

        cost:Decimal = to_decimal("0.0")
        h_recipe = None
        vk_preis:Decimal = to_decimal("0.0")
        H_recipe =  create_buffer("H_recipe",H_rezept)

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == h_artnr)).order_by(H_rezlin._recid).all():
            curr_pos = curr_pos + 1
            s_rezlin = S_rezlin()
            s_rezlin_data.append(s_rezlin)

            s_rezlin.pos = curr_pos
            s_rezlin.artnr = h_rezlin.artnrlager
            s_rezlin.menge =  to_decimal(h_rezlin.menge)
            s_rezlin.lostfact =  to_decimal(h_rezlin.lostfact)

            if h_rezlin.recipe_flag == False:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    vk_preis =  to_decimal(l_artikel.ek_aktuell)
                s_rezlin.bezeich = l_artikel.bezeich
                s_rezlin.masseinheit = to_string(l_artikel.masseinheit, "x(3)")
                s_rezlin.inhalt =  to_decimal(l_artikel.inhalt)
                s_rezlin.vk_preis =  to_decimal(vk_preis)
                s_rezlin.cost =  to_decimal(h_rezlin.menge) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))

                if num_entries(l_artikel.herkunft, ";") > 1:
                    s_rezlin.s_unit = entry(1, l_artikel.herkunft, ";")

                if s_rezlin.s_unit == " ":
                    s_rezlin.s_unit = l_artikel.masseinheit

            elif h_rezlin.recipe_flag :

                h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})
                s_rezlin.bezeich = h_recipe.bezeich
                s_rezlin.recipe_flag = True
                s_rezlin.inhalt =  to_decimal(h_recipe.portion)
                cost =  to_decimal("0")
                cost = cal_cost(h_rezlin.artnrlager, 1, cost)
                s_rezlin.cost =  to_decimal(h_rezlin.menge) * to_decimal(cost)
            amount =  to_decimal(amount) + to_decimal(s_rezlin.cost)

            queasy = get_cache (Queasy, {"key": [(eq, 252)],"number1": [(eq, h_rezlin.artnrrezept)]})

            if queasy:
                cost_percent =  to_decimal(queasy.deci1)
                poten_sell_price =  to_decimal(queasy.deci2)


    def cal_cost(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal katnr, katbezeich, h_bezeich, portion, price_type, amount, cost_percent, poten_sell_price, t_l_artikel_data, t_h_rezept_data, s_rezlin_data, curr_pos, l_artikel, h_rezept, htparam, h_rezlin, queasy
        nonlocal fr_artnr, to_artnr, h_artnr


        nonlocal t_l_artikel, t_h_rezept, s_rezlin
        nonlocal t_l_artikel_data, t_h_rezept_data, s_rezlin_data

        inh:Decimal = to_decimal("0.0")
        vk_preis:Decimal = to_decimal("0.0")
        h_rezlin1 = None
        hrecipe = None

        def generate_inner_output():
            return (cost)

        H_rezlin1 =  create_buffer("H_rezlin1",H_rezlin)
        Hrecipe =  create_buffer("Hrecipe",H_rezept)

        for h_rezlin1 in db_session.query(H_rezlin1).filter(
                 (H_rezlin1.artnrrezept == p_artnr)).order_by(H_rezlin1._recid).all():

            hrecipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin1.artnrrezept)]})

            if hrecipe.portion > 1:
                inh =  to_decimal(menge) * to_decimal(h_rezlin1.menge) / to_decimal(hrecipe.portion)


            else:
                inh =  to_decimal(menge) * to_decimal(h_rezlin1.menge)

            if h_rezlin1.recipe_flag :
                cost = cal_cost(h_rezlin1.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin1.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    vk_preis =  to_decimal(l_artikel.ek_aktuell)
                cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal((1) - to_decimal(h_rezlin1.lostfact) / to_decimal(100))

        return generate_inner_output()


    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artnr)]})
    katnr = h_rezept.kategorie
    katbezeich = substring(h_rezept.bezeich, 24, 24)
    h_bezeich = substring(h_rezept.bezeich, 0, 24)
    portion = h_rezept.portion
    amount =  to_decimal("0")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger
    create_list()

    for l_artikel in db_session.query(L_artikel).filter(
             (L_artikel.artnr >= fr_artnr) & (L_artikel.artnr <= to_artnr)).order_by(L_artikel._recid).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)

    for h_rezept in db_session.query(H_rezept).order_by(H_rezept._recid).all():
        t_h_rezept = T_h_rezept()
        t_h_rezept_data.append(t_h_rezept)

        buffer_copy(h_rezept, t_h_rezept)

    return generate_output()