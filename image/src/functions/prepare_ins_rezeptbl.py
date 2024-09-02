from functions.additional_functions import *
import decimal
from models import L_artikel, H_rezept, Htparam, H_rezlin

def prepare_ins_rezeptbl(fr_artnr:int, to_artnr:int, h_artnr:int):
    katnr = 0
    katbezeich = ""
    h_bezeich = ""
    portion = 0
    price_type = 0
    amount = 0
    t_l_artikel_list = []
    t_h_rezept_list = []
    s_rezlin_list = []
    curr_pos:int = 0
    l_artikel = h_rezept = htparam = h_rezlin = None

    t_l_artikel = t_h_rezept = s_rezlin = h_recipe = h_rezlin1 = hrecipe = None

    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)
    t_h_rezept_list, T_h_rezept = create_model_like(H_rezept)
    s_rezlin_list, S_rezlin = create_model("S_rezlin", {"new_created":bool, "h_recid":int, "pos":int, "artnr":int, "bezeich":str, "masseinheit":str, "inhalt":decimal, "vk_preis":decimal, "cost":decimal, "menge":decimal, "lostfact":decimal, "recipe_flag":bool, "s_unit":str})

    H_recipe = H_rezept
    H_rezlin1 = H_rezlin
    Hrecipe = H_rezept

    db_session = local_storage.db_session

    def generate_output():
        nonlocal katnr, katbezeich, h_bezeich, portion, price_type, amount, t_l_artikel_list, t_h_rezept_list, s_rezlin_list, curr_pos, l_artikel, h_rezept, htparam, h_rezlin
        nonlocal h_recipe, h_rezlin1, hrecipe


        nonlocal t_l_artikel, t_h_rezept, s_rezlin, h_recipe, h_rezlin1, hrecipe
        nonlocal t_l_artikel_list, t_h_rezept_list, s_rezlin_list
        return {"katnr": katnr, "katbezeich": katbezeich, "h_bezeich": h_bezeich, "portion": portion, "price_type": price_type, "amount": amount, "t-l-artikel": t_l_artikel_list, "t-h-rezept": t_h_rezept_list, "s-rezlin": s_rezlin_list}

    def create_list():

        nonlocal katnr, katbezeich, h_bezeich, portion, price_type, amount, t_l_artikel_list, t_h_rezept_list, s_rezlin_list, curr_pos, l_artikel, h_rezept, htparam, h_rezlin
        nonlocal h_recipe, h_rezlin1, hrecipe


        nonlocal t_l_artikel, t_h_rezept, s_rezlin, h_recipe, h_rezlin1, hrecipe
        nonlocal t_l_artikel_list, t_h_rezept_list, s_rezlin_list

        cost:decimal = 0
        vk_preis:decimal = 0
        H_recipe = H_rezept

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == h_artnr)).all():
            curr_pos = curr_pos + 1
            s_rezlin = S_rezlin()
            s_rezlin_list.append(s_rezlin)

            s_rezlin.pos = curr_pos
            s_rezlin.artnr = h_rezlin.artnrlager
            s_rezlin.menge = h_rezlin.menge
            s_rezlin.lostfact = h_rezlin.lostfact

            if h_rezlin.recipe_flag == False:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis = l_artikel.vk_preis
                else:
                    vk_preis = l_artikel.ek_aktuell
                s_rezlin.bezeich = l_artikel.bezeich
                s_rezlin.masseinheit = to_string(l_artikel.masseinheit, "x(3)")
                s_rezlin.inhalt = l_artikel.inhalt
                s_rezlin.vk_preis = vk_preis
                s_rezlin.cost = h_rezlin.menge / l_artikel.inhalt * vk_preis / (1 - h_rezlin.lostfact / 100)

                if num_entries(l_artikel.herkunft, ";") > 1:
                    s_rezlin.s_unit = entry(1, l_artikel.herkunft, ";")

                if s_rezlin.s_unit == " ":
                    s_rezlin.s_unit = l_artikel.masseinheit

            elif h_rezlin.recipe_flag :

                h_recipe = db_session.query(H_recipe).filter(
                        (H_recipe.artnrrezept == h_rezlin.artnrlager)).first()
                s_rezlin.bezeich = h_recipe.bezeich
                s_rezlin.recipe_flag = True
                s_rezlin.inhalt = 1
                cost = 0
                cost = cal_cost(h_rezlin.artnrlager, 1, cost)
                s_rezlin.cost = h_rezlin.menge * cost
            amount = amount + s_rezlin.cost

    def cal_cost(p_artnr:int, menge:decimal, cost:decimal):

        nonlocal katnr, katbezeich, h_bezeich, portion, price_type, amount, t_l_artikel_list, t_h_rezept_list, s_rezlin_list, curr_pos, l_artikel, h_rezept, htparam, h_rezlin
        nonlocal h_recipe, h_rezlin1, hrecipe


        nonlocal t_l_artikel, t_h_rezept, s_rezlin, h_recipe, h_rezlin1, hrecipe
        nonlocal t_l_artikel_list, t_h_rezept_list, s_rezlin_list

        inh:decimal = 0
        vk_preis:decimal = 0
        H_rezlin1 = H_rezlin
        Hrecipe = H_rezept

        for h_rezlin1 in db_session.query(H_rezlin1).filter(
                (H_rezlin1.artnrrezept == p_artnr)).all():

            hrecipe = db_session.query(Hrecipe).filter(
                    (Hrecipe.artnrrezept == h_rezlin1.artnrrezept)).first()

            if hrecipe.portion > 1:
                inh = menge * h_rezlin1.menge / hrecipe.portion


            else:
                inh = menge * h_rezlin1.menge

            if h_rezlin1.recipe_flag :
                cost = cal_cost(h_rezlin1.artnrlager, inh, cost)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin1.artnrlager)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis = l_artikel.vk_preis
                else:
                    vk_preis = l_artikel.ek_aktuell
                cost = cost + inh / l_artikel.inhalt * vk_preis / (1 - h_rezlin1.lostfact / 100)

    h_rezept = db_session.query(H_rezept).filter(
            (H_rezept.artnrrezept == h_artnr)).first()
    katnr = h_rezept.kategorie
    katbezeich = substring(h_rezept.bezeich, 24, 24)
    h_bezeich = substring(h_rezept.bezeich, 0, 24)
    portion = h_rezept.portion
    amount = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1024)).first()
    price_type = htparam.finteger
    create_list()

    for l_artikel in db_session.query(L_artikel).filter(
            (L_artikel.artnr >= fr_artnr) &  (L_artikel.artnr <= to_artnr)).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)

    for h_rezept in db_session.query(H_rezept).all():
        t_h_rezept = T_h_rezept()
        t_h_rezept_list.append(t_h_rezept)

        buffer_copy(h_rezept, t_h_rezept)

    return generate_output()