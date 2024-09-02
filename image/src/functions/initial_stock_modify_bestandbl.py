from functions.additional_functions import *
import decimal
from models import L_bestand, L_artikel

def initial_stock_modify_bestandbl(s_artnr:int, qty:decimal, old_qty:decimal, amount:decimal, old_amount:decimal, curr_lager:int, s_recid:int, t_amount:decimal):
    suc_flg = False
    anzahl = 0
    wert = 0
    avrg_price:decimal = 0
    l_bestand = l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal suc_flg, anzahl, wert, avrg_price, l_bestand, l_artikel


        return {"suc_flg": suc_flg, "anzahl": anzahl, "wert": wert}

    def modify_bestand():

        nonlocal suc_flg, anzahl, wert, avrg_price, l_bestand, l_artikel

        curr_pos:int = 0
        tot_anz:decimal = 0
        anzahl = qty
        wert = amount
        t_amount = t_amount + wert - old_amount

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr)).first()
        l_bestand.anz_anf_best = l_bestand.anz_anf_best + anzahl - old_qty
        l_bestand.val_anf_best = l_bestand.val_anf_best + wert - old_amount

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
        l_bestand.anz_anf_best = anzahl
        l_bestand.val_anf_best = wert

        l_bestand = db_session.query(L_bestand).first()
        suc_flg = True

    modify_bestand()

    return generate_output()