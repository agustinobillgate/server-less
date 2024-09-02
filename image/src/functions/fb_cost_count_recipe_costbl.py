from functions.additional_functions import *
import decimal
from models import H_rezept, H_rezlin, L_artikel

def fb_cost_count_recipe_costbl(grid_list_artnrrezept:int, price_type:int, amount:decimal):
    portion:decimal = 1
    vk_preis:decimal = 0
    h_rezept = h_rezlin = l_artikel = None

    s_rezlin = h_recipe = h_rezlin1 = None

    s_rezlin_list, S_rezlin = create_model("S_rezlin", {"h_recid":int, "pos":int, "artnr":int, "bezeich":str, "masseinheit":str, "inhalt":decimal, "vk_preis":decimal, "cost":decimal, "menge":decimal, "lostfact":decimal, "recipe_flag":bool})

    H_recipe = H_rezept
    H_rezlin1 = H_rezlin

    db_session = local_storage.db_session

    def generate_output():
        nonlocal portion, vk_preis, h_rezept, h_rezlin, l_artikel
        nonlocal h_recipe, h_rezlin1


        nonlocal s_rezlin, h_recipe, h_rezlin1
        nonlocal s_rezlin_list
        return {}

    def cal_cost(p_artnr:int, menge:decimal, cost:decimal):

        nonlocal portion, vk_preis, h_rezept, h_rezlin, l_artikel
        nonlocal h_recipe, h_rezlin1


        nonlocal s_rezlin, h_recipe, h_rezlin1
        nonlocal s_rezlin_list

        inh:decimal = 0
        vk_preis:decimal = 0
        H_rezlin1 = H_rezlin

        h_rezept = db_session.query(H_rezept).filter(
                (H_rezept.artnrrezept == p_artnr)).first()

        for h_rezlin1 in db_session.query(H_rezlin1).filter(
                (H_rezlin1.artnrrezept == p_artnr)).all():
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
                cost = cost + inh / l_artikel.inhalt * vk_preis / h_rezept.portion / (1 - h_rezlin1.lostfact / 100)


    if grid_list_artnrrezept != 0:

        h_rezept = db_session.query(H_rezept).filter(
                (H_rezept.artnrrezept == grid_list_artnrrezept)).first()

    if h_rezept:
        portion = h_rezept.portion

    for h_rezlin in db_session.query(H_rezlin).filter(
            (H_rezlin.artnrrezept == grid_list_artnrrezept)).all():
        s_rezlin = S_rezlin()
        s_rezlin_list.append(s_rezlin)

        s_rezlin.artnr = h_rezlin.artnrlager
        s_rezlin.menge = h_rezlin.menge / portion
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
            s_rezlin.cost = h_rezlin.menge / l_artikel.inhalt * vk_preis / portion / (1 - h_rezlin.lostfact / 100)

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

    return generate_output()