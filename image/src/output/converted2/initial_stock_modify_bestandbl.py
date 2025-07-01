#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand, L_artikel

def initial_stock_modify_bestandbl(s_artnr:int, qty:Decimal, old_qty:Decimal, amount:Decimal, old_amount:Decimal, curr_lager:int, s_recid:int, t_amount:Decimal):

    prepare_cache ([L_bestand, L_artikel])

    suc_flg = False
    anzahl = to_decimal("0.0")
    wert = to_decimal("0.0")
    avrg_price:Decimal = to_decimal("0.0")
    l_bestand = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal suc_flg, anzahl, wert, avrg_price, l_bestand, l_artikel
        nonlocal s_artnr, qty, old_qty, amount, old_amount, curr_lager, s_recid, t_amount

        return {"t_amount": t_amount, "suc_flg": suc_flg, "anzahl": anzahl, "wert": wert}

    def modify_bestand():

        nonlocal suc_flg, anzahl, wert, avrg_price, l_bestand, l_artikel
        nonlocal s_artnr, qty, old_qty, amount, old_amount, curr_lager, s_recid, t_amount

        curr_pos:int = 0
        tot_anz:Decimal = to_decimal("0.0")
        anzahl =  to_decimal(qty)
        wert =  to_decimal(amount)
        t_amount =  to_decimal(t_amount) + to_decimal(wert) - to_decimal(old_amount)

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, s_artnr)]})
        l_bestand.anz_anf_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(anzahl) - to_decimal(old_qty)
        l_bestand.val_anf_best =  to_decimal(l_bestand.val_anf_best) + to_decimal(wert) - to_decimal(old_amount)
        pass
        tot_anz = ( to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang))

        if tot_anz != 0:
            avrg_price = ( to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)) / to_decimal(tot_anz)

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
            l_artikel.vk_preis =  to_decimal(avrg_price)
            pass

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})
        l_bestand.anz_anf_best =  to_decimal(anzahl)
        l_bestand.val_anf_best =  to_decimal(wert)
        pass
        suc_flg = True


    modify_bestand()

    return generate_output()