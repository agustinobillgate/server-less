from functions.additional_functions import *
import decimal
from datetime import date
from models import L_bestand, L_artikel, L_besthis

def close_inventory_step1bl(pvilanguage:int, closedate:date, inv_type:int, m_endkum:int):
    its_ok = False
    msg_str = ""
    msg_str2 = ""
    lvcarea:str = "close_inventory"
    anzahl:decimal = 0
    startdate:date = None
    l_bestand = l_artikel = l_besthis = None

    l_onhand = None

    L_onhand = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, msg_str2, lvcarea, anzahl, startdate, l_bestand, l_artikel, l_besthis
        nonlocal l_onhand


        nonlocal l_onhand
        return {"its_ok": its_ok, "msg_str": msg_str, "msg_str2": msg_str2}

    startdate = date_mdy(get_month(closedate) , 1, get_year(closedate))

    l_bestand = db_session.query(L_bestand).filter(
            ((L_bestand.anf_best_dat <= closedate)) |  ((L_bestand.anf_best_dat >= closedate)) |  ((L_bestand.anf_best_dat == None))).first()
    while None != l_bestand:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_bestand.artnr)).first()

        if not l_artikel:
            msg_str2 = msg_str2 + chr(2) + "&W" + translateExtended ("Article not found for stock onhand", lvcarea, "") + " " + to_string(l_bestand.artnr, "9999999")

        elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):

            l_besthis = db_session.query(L_besthis).filter(
                    (L_besthis.artnr == l_bestand.artnr) &  (L_besthis.lager_nr == l_bestand.lager_nr) &  (L_besthis.anf_best_dat == l_bestand.anf_best_dat)).first()

            if not l_besthis:
                l_besthis = L_besthis()
            db_session.add(l_besthis)

            buffer_copy(l_bestand, l_besthis,except_fields=["anz_eingang","anz_ausgang","wert_eingang","wert_ausgang"])
            l_besthis.anf_best_dat = startdate

            l_onhand = db_session.query(L_onhand).filter(
                    (L_onhand._recid == l_bestand._recid)).first()
            db_session.delete(l_onhand)


        l_bestand = db_session.query(L_bestand).filter(
                ((L_bestand.anf_best_dat <= closedate)) |  ((L_bestand.anf_best_dat >= closedate)) |  ((L_bestand.anf_best_dat == None))).first()

    return generate_output()