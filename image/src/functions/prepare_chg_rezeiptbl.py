from functions.additional_functions import *
import decimal
from datetime import date
from functions.check_timebl import check_timebl
from models import H_rezept, L_artikel, Htparam, H_rezlin

def prepare_chg_rezeiptbl(pvilanguage:int, h_artnr:int, description:str):
    h_bezeich = ""
    katbezeich = ""
    katnr = 0
    portion = 0
    price_type = 0
    amount = 0
    msg_str = ""
    msg_str2 = ""
    msg_str3 = ""
    record_use = False
    init_time = 0
    init_date = None
    r_list_list = []
    s_rezlin_list = []
    t_l_artikel_list = []
    t_h_rezept_list = []
    curr_i:int = 0
    flag_ok:bool = False
    lvcarea:str = "chg_rezept"
    h_rezept = l_artikel = htparam = h_rezlin = None

    r_list = t_h_rezept = t_l_artikel = s_rezlin = hrecipe = h_recipe = h_rezln = None

    r_list_list, R_list = create_model("R_list", {"max_n":int, "recipe_nr":[int, 99]})
    t_h_rezept_list, T_h_rezept = create_model_like(H_rezept, {"rec_id":int})
    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)
    s_rezlin_list, S_rezlin = create_model("S_rezlin", {"h_recid":int, "artnr":int, "bezeich":str, "masseinheit":str, "s_unit":str, "menge":decimal, "cost":decimal, "inhalt":decimal, "vk_preis":decimal, "lostfact":decimal, "recipe_flag":bool})

    Hrecipe = H_rezept
    H_recipe = H_rezept
    H_rezln = H_rezlin

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bezeich, katbezeich, katnr, portion, price_type, amount, msg_str, msg_str2, msg_str3, record_use, init_time, init_date, r_list_list, s_rezlin_list, t_l_artikel_list, t_h_rezept_list, curr_i, flag_ok, lvcarea, h_rezept, l_artikel, htparam, h_rezlin
        nonlocal hrecipe, h_recipe, h_rezln


        nonlocal r_list, t_h_rezept, t_l_artikel, s_rezlin, hrecipe, h_recipe, h_rezln
        nonlocal r_list_list, t_h_rezept_list, t_l_artikel_list, s_rezlin_list
        return {"h_bezeich": h_bezeich, "katbezeich": katbezeich, "katnr": katnr, "portion": portion, "price_type": price_type, "amount": amount, "msg_str": msg_str, "msg_str2": msg_str2, "msg_str3": msg_str3, "record_use": record_use, "init_time": init_time, "init_date": init_date, "r-list": r_list_list, "s-rezlin": s_rezlin_list, "t-l-artikel": t_l_artikel_list, "t-h-rezept": t_h_rezept_list}

    def create_rezlin():

        nonlocal h_bezeich, katbezeich, katnr, portion, price_type, amount, msg_str, msg_str2, msg_str3, record_use, init_time, init_date, r_list_list, s_rezlin_list, t_l_artikel_list, t_h_rezept_list, curr_i, flag_ok, lvcarea, h_rezept, l_artikel, htparam, h_rezlin
        nonlocal hrecipe, h_recipe, h_rezln


        nonlocal r_list, t_h_rezept, t_l_artikel, s_rezlin, hrecipe, h_recipe, h_rezln
        nonlocal r_list_list, t_h_rezept_list, t_l_artikel_list, s_rezlin_list

        cost:decimal = 0
        H_recipe = H_rezept
        s_rezlin = S_rezlin()
        s_rezlin_list.append(s_rezlin)

        s_rezlin.h_recid = h_rezlin._recid
        s_rezlin.artnr = h_rezlin.artnrlager
        s_rezlin.bezeich = description
        s_rezlin.menge = h_rezlin.menge
        s_rezlin.lostfact = h_rezlin.lostfact
        s_rezlin.recipe_flag = h_rezlin.recipe_flag

        if h_rezlin.recipe_flag == False:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == h_rezlin.artnrlager)).first()
            s_rezlin.bezeich = l_artikel.bezeich
            s_rezlin.masseinheit = to_string(l_artikel.masseinheit, "x(3)")
            s_rezlin.s_unit = entry(1, l_artikel.herkunft, ";")
            s_rezlin.inhalt = l_artikel.inhalt

            if s_rezlin.s_unit == "" and s_rezlin.inhalt == 1:
                s_rezlin.s_unit = s_rezlin.masseinheit

            if price_type == 0 or l_artikel.ek_aktuell == 0:
                s_rezlin.vk_preis = l_artikel.vk_preis
            else:
                s_rezlin.vk_preis = l_artikel.ek_aktuell
            s_rezlin.lostfact = h_rezlin.lostfact

            if price_type == 0 or l_artikel.ek_aktuell == 0:
                s_rezlin.cost = h_rezlin.menge / l_artikel.inhalt * l_artikel.vk_preis / (1 - h_rezlin.lostfact / 100)
            else:
                s_rezlin.cost = h_rezlin.menge / l_artikel.inhalt * l_artikel.ek_aktuell / (1 - h_rezlin.lostfact / 100)

            if s_rezlin.cost == 0:
                msg_str = msg_str + chr(2) + translateExtended ("Article content or price not yet defined: ", lvcarea, "") + chr(10) + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich

        elif h_rezlin.recipe_flag :

            h_recipe = db_session.query(H_recipe).filter(
                    (H_recipe.artnrrezept == h_rezlin.artnrlager)).first()
            s_rezlin.bezeich = to_string(h_recipe.bezeich, "x(24)")
            s_rezlin.recipe_flag = True
            s_rezlin.inhalt = 1
            cost = 0
            cost = cal_cost(h_recipe.artnr, 1, cost)
            s_rezlin.cost = cost / h_recipe.portion

            if s_rezlin.cost == 0:
                msg_str2 = msg_str2 + chr(2) + translateExtended ("Recipe cost  ==  0; cost calculation not possible:", lvcarea, "") + chr(10) + to_string(h_recipe.artnrrezept) + " - " + h_recipe.bezeich
        amount = amount + s_rezlin.cost

    def cal_cost(p_artnr:int, menge:decimal, cost:decimal):

        nonlocal h_bezeich, katbezeich, katnr, portion, price_type, amount, msg_str, msg_str2, msg_str3, record_use, init_time, init_date, r_list_list, s_rezlin_list, t_l_artikel_list, t_h_rezept_list, curr_i, flag_ok, lvcarea, h_rezept, l_artikel, htparam, h_rezlin
        nonlocal hrecipe, h_recipe, h_rezln


        nonlocal r_list, t_h_rezept, t_l_artikel, s_rezlin, hrecipe, h_recipe, h_rezln
        nonlocal r_list_list, t_h_rezept_list, t_l_artikel_list, s_rezlin_list

        inh:decimal = 0
        i:int = 0
        H_rezln = H_rezlin
        Hrecipe = H_rezept
        for i in range(1,curr_i + 1) :

            if r_list.recipe_nr[i - 1] == p_artnr:
                pass
        curr_i = curr_i + 1
        r_list.recipe_nr[curr_i - 1] = p_artnr

        for h_rezln in db_session.query(H_rezln).filter(
                (H_rezln.artnrrezept == p_artnr)).all():

            if not h_rezln.recipe_flag:
                inh = menge * h_rezln.menge / (1 - h_rezln.lostfact / 100)
            else:

                hrecipe = db_session.query(Hrecipe).filter(
                        (Hrecipe.artnrrezept == h_rezln.artnrlager)).first()

                if hrecipe.portion > 1:
                    inh = menge * h_rezln.menge / hrecipe.portion


                else:
                    inh = menge * h_rezln.menge

            if h_rezln.recipe_flag :
                cost = cal_cost(h_rezln.artnrlager, inh, cost)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezln.artnrlager)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost = cost + inh / l_artikel.inhalt * l_artikel.vk_preis
                else:
                    cost = cost + inh / l_artikel.inhalt * l_artikel.ek_aktuell

    flag_ok, init_time, init_date = get_output(check_timebl(1, h_artnr, None, "h_rezept", None, None))

    if not flag_ok:
        record_use = True

        return generate_output()
    r_list = R_list()
    r_list_list.append(r_list)


    h_rezept = db_session.query(H_rezept).filter(
            (H_rezept.artnrrezept == h_artnr)).first()
    h_bezeich = substring(h_rezept.bezeich, 0, 24)
    katnr = h_rezept.kategorie
    katbezeich = substring(h_rezept.bezeich, 24, 24)
    portion = h_rezept.portion
    t_h_rezept = T_h_rezept()
    t_h_rezept_list.append(t_h_rezept)

    buffer_copy(h_rezept, t_h_rezept)
    t_h_rezept.rec_id = h_rezept._recid

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1024)).first()
    price_type = htparam.finteger

    for h_rezlin in db_session.query(H_rezlin).filter(
            (H_rezlin.artnrrezept == h_artnr)).all():
        create_rezlin()

    for l_artikel in db_session.query(L_artikel).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)

    return generate_output()