#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_timebl import check_timebl
from models import H_rezept, L_artikel, Htparam, H_rezlin

def prepare_chg_rezeiptbl(pvilanguage:int, h_artnr:int, description:string):

    prepare_cache ([H_rezept, Htparam, H_rezlin])

    h_bezeich = ""
    katbezeich = ""
    katnr = 0
    portion = 0
    price_type = 0
    amount = to_decimal("0.0")
    msg_str = ""
    msg_str2 = ""
    msg_str3 = ""
    record_use = False
    init_time = 0
    init_date = None
    r_list_data = []
    s_rezlin_data = []
    t_l_artikel_data = []
    t_h_rezept_data = []
    curr_i:int = 0
    flag_ok:bool = False
    lvcarea:string = "chg-rezept"
    h_rezept = l_artikel = htparam = h_rezlin = None

    r_list = t_h_rezept = t_l_artikel = s_rezlin = hrecipe = None

    r_list_data, R_list = create_model("R_list", {"max_n":int, "recipe_nr":[int,99]})
    t_h_rezept_data, T_h_rezept = create_model_like(H_rezept, {"rec_id":int})
    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)
    s_rezlin_data, S_rezlin = create_model("S_rezlin", {"h_recid":int, "artnr":int, "bezeich":string, "masseinheit":string, "s_unit":string, "menge":Decimal, "cost":Decimal, "inhalt":Decimal, "vk_preis":Decimal, "lostfact":Decimal, "recipe_flag":bool})

    Hrecipe = create_buffer("Hrecipe",H_rezept)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bezeich, katbezeich, katnr, portion, price_type, amount, msg_str, msg_str2, msg_str3, record_use, init_time, init_date, r_list_data, s_rezlin_data, t_l_artikel_data, t_h_rezept_data, curr_i, flag_ok, lvcarea, h_rezept, l_artikel, htparam, h_rezlin
        nonlocal pvilanguage, h_artnr, description
        nonlocal hrecipe


        nonlocal r_list, t_h_rezept, t_l_artikel, s_rezlin, hrecipe
        nonlocal r_list_data, t_h_rezept_data, t_l_artikel_data, s_rezlin_data

        return {"h_bezeich": h_bezeich, "katbezeich": katbezeich, "katnr": katnr, "portion": portion, "price_type": price_type, "amount": amount, "msg_str": msg_str, "msg_str2": msg_str2, "msg_str3": msg_str3, "record_use": record_use, "init_time": init_time, "init_date": init_date, "r-list": r_list_data, "s-rezlin": s_rezlin_data, "t-l-artikel": t_l_artikel_data, "t-h-rezept": t_h_rezept_data}

    def create_rezlin():

        nonlocal h_bezeich, katbezeich, katnr, portion, price_type, amount, msg_str, msg_str2, msg_str3, record_use, init_time, init_date, r_list_data, s_rezlin_data, t_l_artikel_data, t_h_rezept_data, curr_i, flag_ok, lvcarea, h_rezept, l_artikel, htparam, h_rezlin
        nonlocal pvilanguage, h_artnr, description
        nonlocal hrecipe


        nonlocal r_list, t_h_rezept, t_l_artikel, s_rezlin, hrecipe
        nonlocal r_list_data, t_h_rezept_data, t_l_artikel_data, s_rezlin_data

        cost:Decimal = to_decimal("0.0")
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)
        s_rezlin = S_rezlin()
        s_rezlin_data.append(s_rezlin)

        s_rezlin.h_recid = h_rezlin._recid
        s_rezlin.artnr = h_rezlin.artnrlager
        s_rezlin.bezeich = description
        s_rezlin.menge =  to_decimal(h_rezlin.menge)
        s_rezlin.lostfact =  to_decimal(h_rezlin.lostfact)
        s_rezlin.recipe_flag = h_rezlin.recipe_flag

        if h_rezlin.recipe_flag == False:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})
            s_rezlin.bezeich = l_artikel.bezeich
            s_rezlin.masseinheit = to_string(l_artikel.masseinheit, "x(3)")
            s_rezlin.s_unit = entry(1, l_artikel.herkunft, ";")
            s_rezlin.inhalt =  to_decimal(l_artikel.inhalt)

            if s_rezlin.s_unit == "" and s_rezlin.inhalt == 1:
                s_rezlin.s_unit = s_rezlin.masseinheit

            if price_type == 0 or l_artikel.ek_aktuell == 0:
                s_rezlin.vk_preis =  to_decimal(l_artikel.vk_preis)
            else:
                s_rezlin.vk_preis =  to_decimal(l_artikel.ek_aktuell)
            s_rezlin.lostfact =  to_decimal(h_rezlin.lostfact)

            if price_type == 0 or l_artikel.ek_aktuell == 0:
                s_rezlin.cost =  to_decimal(h_rezlin.menge) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
            else:
                s_rezlin.cost =  to_decimal(h_rezlin.menge) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.ek_aktuell) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))

            if s_rezlin.cost == 0:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Article content or price not yet defined: ", lvcarea, "") + chr_unicode(10) + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich

        elif h_rezlin.recipe_flag :

            h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})
            s_rezlin.bezeich = to_string(h_recipe.bezeich, "x(24)")
            s_rezlin.recipe_flag = True
            s_rezlin.inhalt =  to_decimal("1")
            cost =  to_decimal("0")
            cost = cal_cost(h_recipe.artnr, 1, cost)
            s_rezlin.cost = ( to_decimal(cost) / to_decimal(h_recipe.portion)) * to_decimal(h_rezlin.menge)

            if s_rezlin.cost == 0:
                msg_str2 = msg_str2 + chr_unicode(2) + translateExtended ("Recipe cost = 0; cost calculation not possible:", lvcarea, "") + chr_unicode(10) + to_string(h_recipe.artnrrezept) + " - " + h_recipe.bezeich
        amount =  to_decimal(amount) + to_decimal(s_rezlin.cost)


    def cal_cost(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal h_bezeich, katbezeich, katnr, portion, price_type, amount, msg_str, msg_str2, msg_str3, record_use, init_time, init_date, r_list_data, s_rezlin_data, t_l_artikel_data, t_h_rezept_data, curr_i, flag_ok, lvcarea, h_rezept, l_artikel, htparam, h_rezlin
        nonlocal pvilanguage, h_artnr, description
        nonlocal hrecipe


        nonlocal r_list, t_h_rezept, t_l_artikel, s_rezlin, hrecipe
        nonlocal r_list_data, t_h_rezept_data, t_l_artikel_data, s_rezlin_data

        inh:Decimal = to_decimal("0.0")
        h_rezln = None
        hrecipe = None
        i:int = 0

        def generate_inner_output():
            return (cost)

        H_rezln =  create_buffer("H_rezln",H_rezlin)
        Hrecipe =  create_buffer("Hrecipe",H_rezept)
        for i in range(1,curr_i + 1) :

            if r_list.recipe_nr[i - 1] == p_artnr:
                pass
        curr_i = curr_i + 1
        r_list.recipe_nr[curr_i - 1] = p_artnr

        for h_rezln in db_session.query(H_rezln).filter(
                 (H_rezln.artnrrezept == p_artnr)).order_by(H_rezln._recid).all():

            if not h_rezln.recipe_flag:
                inh =  to_decimal(menge) * to_decimal(h_rezln.menge) / to_decimal((1) - to_decimal(h_rezln.lostfact) / to_decimal(100))
            else:

                hrecipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezln.artnrlager)]})

                if hrecipe.portion > 1:
                    inh =  to_decimal(menge) * to_decimal(h_rezln.menge) / to_decimal(hrecipe.portion)


                else:
                    inh =  to_decimal(menge) * to_decimal(h_rezln.menge)

            if h_rezln.recipe_flag :
                cost = cal_cost(h_rezln.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezln.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.vk_preis)
                else:
                    cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.ek_aktuell)

        return generate_inner_output()


    flag_ok, init_time, init_date = get_output(check_timebl(1, h_artnr, None, "h-rezept", None, None))

    if not flag_ok:
        record_use = True

        return generate_output()
    r_list = R_list()
    r_list_data.append(r_list)


    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artnr)]})
    h_bezeich = substring(h_rezept.bezeich, 0, 24)
    katnr = h_rezept.kategorie
    katbezeich = substring(h_rezept.bezeich, 24, 24)
    portion = h_rezept.portion
    t_h_rezept = T_h_rezept()
    t_h_rezept_data.append(t_h_rezept)

    buffer_copy(h_rezept, t_h_rezept)
    t_h_rezept.rec_id = h_rezept._recid

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger

    for h_rezlin in db_session.query(H_rezlin).filter(
             (H_rezlin.artnrrezept == h_artnr)).order_by(H_rezlin._recid).all():
        create_rezlin()

    for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)

    return generate_output()