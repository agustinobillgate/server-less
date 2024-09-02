from functions.additional_functions import *
import decimal
from models import H_rezept, H_rezlin, L_artikel

def mk_rezept_cal_costbl(p_artnr:int, menge:decimal, cost:decimal, price_type:int):
    h_rezept = h_rezlin = l_artikel = None

    hrecipe = None

    Hrecipe = H_rezept

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal hrecipe


        nonlocal hrecipe
        return {}

    def cal_cost():

        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal hrecipe


        nonlocal hrecipe

        inh:decimal = 0
        vk_preis:decimal = 0

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == p_artnr)).all():

            if not h_rezlin.recipe_flag:
                inh = menge * h_rezlin.menge / (1 - h_rezlin.lostfact / 100)
            else:

                hrecipe = db_session.query(Hrecipe).filter(
                        (Hrecipe.artnrrezept == h_rezlin.artnrlager)).first()

                if hrecipe.portion > 1:
                    inh = menge * h_rezlin.menge / hrecipe.portion


                else:
                    inh = menge * h_rezlin.menge

            if h_rezlin.recipe_flag :
                cost = cal_cost2(h_rezlin.artnrlager, inh, cost)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis = l_artikel.vk_preis
                else:
                    vk_preis = l_artikel.ek_aktuell
                cost = cost + inh / l_artikel.inhalt * vk_preis

    def cal_cost2(p_artnr:int, menge:decimal, cost:decimal):

        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal hrecipe


        nonlocal hrecipe

        inh:decimal = 0
        vk_preis:decimal = 0

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == p_artnr)).all():

            if not h_rezlin.recipe_flag:
                inh = menge * h_rezlin.menge / (1 - h_rezlin.lostfact / 100)
            else:

                hrecipe = db_session.query(Hrecipe).filter(
                        (Hrecipe.artnrrezept == h_rezlin.artnrlager)).first()

                if hrecipe.portion > 1:
                    inh = menge * h_rezlin.menge / hrecipe.portion


                else:
                    inh = menge * h_rezlin.menge

            if h_rezlin.recipe_flag :
                cost = cal_cost3(h_rezlin.artnrlager, inh, cost)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis = l_artikel.vk_preis
                else:
                    vk_preis = l_artikel.ek_aktuell
                cost = cost + inh / l_artikel.inhalt * vk_preis

    def cal_cost3(p_artnr:int, menge:decimal, cost:decimal):

        nonlocal h_rezept, h_rezlin, l_artikel
        nonlocal hrecipe


        nonlocal hrecipe

        inh:decimal = 0
        vk_preis:decimal = 0

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == p_artnr)).all():

            if not h_rezlin.recipe_flag:
                inh = menge * h_rezlin.menge / (1 - h_rezlin.lostfact / 100)
            else:

                hrecipe = db_session.query(Hrecipe).filter(
                        (Hrecipe.artnrrezept == h_rezlin.artnrlager)).first()

                if hrecipe.portion > 1:
                    inh = menge * h_rezlin.menge / hrecipe.portion


                else:
                    inh = menge * h_rezlin.menge

            if h_rezlin.recipe_flag :
                cost = cal_cost3(h_rezlin.artnrlager, inh, cost)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis = l_artikel.vk_preis
                else:
                    vk_preis = l_artikel.ek_aktuell
                cost = cost + inh / l_artikel.inhalt * vk_preis

    cal_cost()

    return generate_output()