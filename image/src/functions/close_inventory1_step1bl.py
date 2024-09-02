from functions.additional_functions import *
import decimal
from datetime import date
from models import L_artikel, L_bestand, L_besthis, L_lager

def close_inventory1_step1bl(pvilanguage:int, inv_type:int, m_endkum:int, begindate:date, closedate:date):
    t_its_ok = False
    msg_str = ""
    msg_str2 = ""
    its_ok:bool = False
    anzahl:decimal = 0
    lvcarea:str = "close_inventory"
    l_artikel = l_bestand = l_besthis = l_lager = None

    lart = l_onhand = store = None

    Lart = L_artikel
    L_onhand = L_bestand
    Store = L_lager

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_its_ok, msg_str, msg_str2, its_ok, anzahl, lvcarea, l_artikel, l_bestand, l_besthis, l_lager
        nonlocal lart, l_onhand, store


        nonlocal lart, l_onhand, store
        return {"t_its_ok": t_its_ok, "msg_str": msg_str, "msg_str2": msg_str2}

    def create_lbesthis():

        nonlocal t_its_ok, msg_str, msg_str2, its_ok, anzahl, lvcarea, l_artikel, l_bestand, l_besthis, l_lager
        nonlocal lart, l_onhand, store


        nonlocal lart, l_onhand, store


        Lart = L_artikel

        for l_bestand in db_session.query(L_bestand).all():

            if not lart:

                lart = db_session.query(Lart).filter(
                        (Lart.artnr == l_bestand.artnr)).first()

            elif lart and lart.artnr != l_bestand.artnr:

                lart = db_session.query(Lart).filter(
                        (Lart.artnr == l_bestand.artnr)).first()

            if (inv_type == 1 and lart.l_artikel.endkum < m_endkum) or (inv_type == 2 and lart.l_artikel.endkum >= m_endkum) or (inv_type == 3):

                l_besthis = db_session.query(L_besthis).filter(
                        (L_besthis.anf_best_dat == begindate) &  (L_besthis.lager_nr == l_bestand.lager_nr) &  (L_besthis.artnr == l_bestand.artnr)).first()

                if not l_besthis:
                    l_besthis = L_besthis()
                db_session.add(l_besthis)

                buffer_copy(l_bestand, l_besthis,except_fields=["l_bestand.anf_best_dat"])
                l_besthis.anf_best_dat = begindate

                l_besthis = db_session.query(L_besthis).first()


    def close_onhand():

        nonlocal t_its_ok, msg_str, msg_str2, its_ok, anzahl, lvcarea, l_artikel, l_bestand, l_besthis, l_lager
        nonlocal lart, l_onhand, store


        nonlocal lart, l_onhand, store

        t_qty:decimal = 0
        wert:decimal = 0
        avrg_price:decimal = 0
        L_onhand = L_bestand

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  ((L_bestand.anf_best_dat <= closedate) |  (L_bestand.anf_best_dat == None) |  (L_bestand.anf_best_dat >= closedate))).first()
        while None != l_bestand:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_bestand.artnr)).first()

            if not l_artikel:
                msg_str2 = msg_str2 + chr(2) + "&W" + translateExtended ("Article not found for stock onhand", lvcarea, "") + " " + to_string(l_bestand.artnr, "9999999")

            elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):
                t_qty = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
                wert = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang
                anzahl = close_onhand2(l_bestand.artnr, t_qty, wert)

                l_bestand = db_session.query(L_bestand).first()
                l_bestand.anz_anf_best = anzahl
                l_bestand.val_anf_best = wert
                l_bestand.anz_eingang = 0
                l_bestand.wert_eingang = 0
                l_bestand.anz_ausgang = 0
                l_bestand.wert_ausgang = 0
                l_bestand.anf_best_dat = closedate + 1

                l_bestand = db_session.query(L_bestand).first()

                if anzahl != 0:
                    avrg_price = wert / anzahl

                    l_artikel = db_session.query(L_artikel).filter(
                            (L_artikel.artnr == l_bestand.artnr)).first()

                    if l_artikel:
                        l_artikel.vk_preis = avrg_price

                        l_artikel = db_session.query(L_artikel).first()

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0) &  ((L_bestand.anf_best_dat <= closedate) |  (L_bestand.anf_best_dat == None) |  (L_bestand.anf_best_dat >= closedate))).first()

    def check_onhand():

        nonlocal t_its_ok, msg_str, msg_str2, its_ok, anzahl, lvcarea, l_artikel, l_bestand, l_besthis, l_lager
        nonlocal lart, l_onhand, store


        nonlocal lart, l_onhand, store

        its_ok = False

        def generate_inner_output():
            return its_ok

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  ((L_bestand.anf_best_dat <= closedate) |  (L_bestand.anf_best_dat == None))).first()
        while None != l_bestand:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_bestand.artnr)).first()

            if l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):
                msg_str = msg_str + chr(2) + translateExtended ("Not updated Stock Onhand found for article :", lvcarea, "") + chr(10) + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr(10) + translateExtended ("Last Closing Date  ==  ", lvcarea, "") + to_string(l_bestand.anf_best_dat) + chr(10) + translateExtended ("Fix the possible errors, then restart the program.", lvcarea, "")
                its_ok = False

                return generate_inner_output()

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0) &  ((L_bestand.anf_best_dat <= closedate) |  (L_bestand.anf_best_dat == None))).first()


        return generate_inner_output()

    def close_onhand2(artnr:int, t_qty:decimal, t_wert:decimal):

        nonlocal t_its_ok, msg_str, msg_str2, its_ok, anzahl, lvcarea, l_artikel, l_bestand, l_besthis, l_lager
        nonlocal lart, l_onhand, store


        nonlocal lart, l_onhand, store

        t_anz = 0
        anzahl:decimal = 0
        wert:decimal = 0

        def generate_inner_output():
            return t_anz
        L_onhand = L_bestand
        Store = L_lager

        for store in db_session.query(Store).all():

            l_onhand = db_session.query(L_onhand).filter(
                    (L_onhand.artnr == artnr) &  (L_onhand.lager_nr == store.lager_nr)).first()

            if l_onhand:
                anzahl = (l_onhand.anz_anf_best + l_onhand.anz_eingang - l_onhand.anz_ausgang)
                t_anz = t_anz + anzahl

                if t_qty != 0:
                    wert = t_wert * anzahl / t_qty
                else:
                    wert = 0

                l_onhand = db_session.query(L_onhand).first()
                l_onhand.anz_anf_best = anzahl
                l_onhand.val_anf_best = wert
                l_onhand.anz_eingang = 0
                l_onhand.wert_eingang = 0
                l_onhand.anz_ausgang = 0
                l_onhand.wert_ausgang = 0
                l_onhand.anf_best_dat = closedate + 1

                l_onhand = db_session.query(L_onhand).first()


        return generate_inner_output()

    create_lbesthis()
    close_onhand()
    its_ok = check_onhand()
    t_its_ok = its_ok

    return generate_output()