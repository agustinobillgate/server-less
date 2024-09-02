from functions.additional_functions import *
import decimal
from models import H_rezept, H_rezlin, L_artikel

def recipe_list_cal_costbl(p_artnr:int, menge:decimal, cost:decimal, price_type:int):
    h_rezept = h_rezlin = l_artikel = None

    h_recipe = hrecipe = None

    H_recipe = H_rezept
    Hrecipe = H_rezept

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal h_recipe, hrecipe


        nonlocal h_recipe, hrecipe
        return {}

    def cal_cost(p_artnr:int, menge:decimal, cost:decimal):

        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal h_recipe, hrecipe


        nonlocal h_recipe, hrecipe

        inh:decimal = 0
        i:int = 0
        H_recipe = H_rezept
        Hrecipe = H_rezept

        h_recipe = db_session.query(H_recipe).filter(
                (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == p_artnr)).all():

            if h_rezlin.recipe_flag :

                hrecipe = db_session.query(Hrecipe).filter(
                        (Hrecipe.artnrrezept == h_rezlin.artnrlager)).first()

                if hrecipe.portion > 1:
                    inh = menge * h_rezlin.menge / hrecipe.portion


                else:
                    inh = menge * h_rezlin.menge
                cost = cal_cost(h_rezlin.artnrlager, inh, cost)
            else:
                inh = menge * h_rezlin.menge

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost = cost + inh / l_artikel.inhalt * l_artikel.vk_preis / (1 - h_rezlin.lostfact / 100)
                else:
                    cost = cost + inh / l_artikel.inhalt * l_artikel.ek_aktuell / (1 - h_rezlin.lostfact / 100)

    cost = cal_cost(p_artnr, menge, cost)

    return generate_output()