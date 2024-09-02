from functions.additional_functions import *
import decimal
from datetime import date
from models import L_bestand, L_artikel

def initial_stock_create_bestandbl(s_artnr:int, m_endkum:int, m_date:date, fb_date:date, qty:decimal, amount:decimal, old_amount:decimal, curr_lager:int, t_amount:decimal):
    best_list_list = []
    avrg_price:decimal = 0
    l_bestand = l_artikel = None

    best_list = t_best_list = l_art1 = None

    best_list_list, Best_list = create_model_like(L_bestand, {"rec_id":int})
    t_best_list_list, T_best_list = create_model_like(Best_list)

    L_art1 = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal best_list_list, avrg_price, l_bestand, l_artikel
        nonlocal l_art1


        nonlocal best_list, t_best_list, l_art1
        nonlocal best_list_list, t_best_list_list
        return {"best-list": best_list_list}

    def create_bestand():

        nonlocal best_list_list, avrg_price, l_bestand, l_artikel
        nonlocal l_art1


        nonlocal best_list, t_best_list, l_art1
        nonlocal best_list_list, t_best_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        curr_pos:int = 0
        init_date:date = None
        tot_anz:decimal = 0
        L_art1 = L_artikel

        l_art1 = db_session.query(L_art1).filter(
                (L_art1.artnr == s_artnr)).first()

        if l_art1.endkum >= m_endkum:
            init_date = m_date
        else:
            init_date = fb_date
        anzahl = qty
        wert = amount
        t_amount = t_amount + wert - old_amount

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = init_date
        l_bestand.anz_anf_best = l_bestand.anz_anf_best + anzahl
        l_bestand.val_anf_best = l_bestand.val_anf_best + wert

        l_bestand = db_session.query(L_bestand).first()
        tot_anz = (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang)

        if tot_anz != 0:
            avrg_price = (l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang) / tot_anz

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == s_artnr)).first()
            l_artikel.vk_preis = avrg_price

            l_artikel = db_session.query(L_artikel).first()

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr
            l_bestand.lager_nr = curr_lager
            l_bestand.anf_best_dat = init_date
        l_bestand.anz_anf_best = l_bestand.anz_anf_best + anzahl
        l_bestand.val_anf_best = l_bestand.val_anf_best + wert

        l_bestand = db_session.query(L_bestand).first()
        best_list = Best_list()
        best_list_list.append(best_list)

        best_list.artnr = s_artnr
        best_list.anf_best_dat = init_date
        best_list.lager_nr = curr_lager
        best_list.anz_anf_best = anzahl
        best_list.val_anf_best = wert
        best_list.rec_id = l_bestand._recid

    create_bestand()

    return generate_output()