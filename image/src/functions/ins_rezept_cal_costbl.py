from functions.additional_functions import *
import decimal
from models import H_rezlin, L_artikel

def ins_rezept_cal_costbl(p_artnr:int, menge:decimal, price_type:int, cost:decimal):
    h_rezlin = l_artikel = None

    h_rezlin1 = None

    H_rezlin1 = H_rezlin

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezlin, l_artikel
        nonlocal h_rezlin1


        nonlocal h_rezlin1
        return {}

    def cal_cost():

        nonlocal h_rezlin, l_artikel
        nonlocal h_rezlin1


        nonlocal h_rezlin1

        inh:decimal = 0
        vk_preis:decimal = 0
        H_rezlin1 = H_rezlin

        for h_rezlin1 in db_session.query(H_rezlin1).filter(
                (H_rezlin1.artnrrezept == p_artnr)).all():
            inh = menge * h_rezlin1.menge

            if h_rezlin1.recipe_flag :
                cost = cal_cost2(h_rezlin1.artnrlager, inh, cost)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin1.artnrlager)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis = l_artikel.vk_preis
                else:
                    vk_preis = l_artikel.ek_aktuell
                cost = cost + inh / l_artikel.inhalt * vk_preis / (1 - h_rezlin1.lostfact / 100)

    def cal_cost2():

        nonlocal h_rezlin, l_artikel
        nonlocal h_rezlin1


        nonlocal h_rezlin1

        inh:decimal = 0
        vk_preis:decimal = 0
        H_rezlin1 = H_rezlin

        for h_rezlin1 in db_session.query(H_rezlin1).filter(
                (H_rezlin1.artnrrezept == p_artnr)).all():
            inh = menge * h_rezlin1.menge

            if h_rezlin1.recipe_flag :
                cost = cal_cost2(h_rezlin1.artnrlager, inh, cost)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin1.artnrlager)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis = l_artikel.vk_preis
                else:
                    vk_preis = l_artikel.ek_aktuell
                cost = cost + inh / l_artikel.inhalt * vk_preis / (1 - h_rezlin1.lostfact / 100)

    cal_cost()

    return generate_output()