#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_bestand, L_artikel

def initial_stock_create_bestandbl(s_artnr:int, m_endkum:int, m_date:date, fb_date:date, qty:Decimal, amount:Decimal, old_amount:Decimal, curr_lager:int, t_amount:Decimal):

    prepare_cache ([L_bestand, L_artikel])

    best_list_data = []
    avrg_price:Decimal = to_decimal("0.0")
    l_bestand = l_artikel = None

    best_list = t_best_list = None

    best_list_data, Best_list = create_model_like(L_bestand, {"rec_id":int})
    t_best_list_data, T_best_list = create_model_like(Best_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal best_list_data, avrg_price, l_bestand, l_artikel
        nonlocal s_artnr, m_endkum, m_date, fb_date, qty, amount, old_amount, curr_lager, t_amount


        nonlocal best_list, t_best_list
        nonlocal best_list_data, t_best_list_data

        return {"t_amount": t_amount, "best-list": best_list_data}

    def create_bestand():

        nonlocal best_list_data, avrg_price, l_bestand, l_artikel
        nonlocal s_artnr, m_endkum, m_date, fb_date, qty, amount, old_amount, curr_lager, t_amount


        nonlocal best_list, t_best_list
        nonlocal best_list_data, t_best_list_data

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        curr_pos:int = 0
        init_date:date = None
        l_art1 = None
        tot_anz:Decimal = to_decimal("0.0")
        L_art1 =  create_buffer("L_art1",L_artikel)

        l_art1 = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

        if l_art1.endkum >= m_endkum:
            init_date = m_date
        else:
            init_date = fb_date
        anzahl =  to_decimal(qty)
        wert =  to_decimal(amount)
        t_amount =  to_decimal(t_amount) + to_decimal(wert) - to_decimal(old_amount)

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, s_artnr)]})

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = init_date
        l_bestand.anz_anf_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(anzahl)
        l_bestand.val_anf_best =  to_decimal(l_bestand.val_anf_best) + to_decimal(wert)
        pass
        tot_anz = ( to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang))

        if tot_anz != 0:
            avrg_price = ( to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)) / to_decimal(tot_anz)

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
            l_artikel.vk_preis =  to_decimal(avrg_price)
            pass

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr
            l_bestand.lager_nr = curr_lager
            l_bestand.anf_best_dat = init_date
        l_bestand.anz_anf_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(anzahl)
        l_bestand.val_anf_best =  to_decimal(l_bestand.val_anf_best) + to_decimal(wert)
        pass
        best_list = Best_list()
        best_list_data.append(best_list)

        best_list.artnr = s_artnr
        best_list.anf_best_dat = init_date
        best_list.lager_nr = curr_lager
        best_list.anz_anf_best =  to_decimal(anzahl)
        best_list.val_anf_best =  to_decimal(wert)
        best_list.rec_id = l_bestand._recid


    create_bestand()

    return generate_output()