#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_bestand, L_besthis, L_lager

def close_inventory1_step1bl(pvilanguage:int, inv_type:int, m_endkum:int, begindate:date, closedate:date):

    prepare_cache ([L_artikel, L_bestand, L_besthis, L_lager])

    t_its_ok = False
    msg_str = ""
    msg_str2 = ""
    its_ok:bool = False
    anzahl:Decimal = to_decimal("0.0")
    lvcarea:string = "close-inventory"
    l_artikel = l_bestand = l_besthis = l_lager = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_its_ok, msg_str, msg_str2, its_ok, anzahl, lvcarea, l_artikel, l_bestand, l_besthis, l_lager
        nonlocal pvilanguage, inv_type, m_endkum, begindate, closedate

        return {"t_its_ok": t_its_ok, "msg_str": msg_str, "msg_str2": msg_str2}

    def create_lbesthis():

        nonlocal t_its_ok, msg_str, msg_str2, its_ok, anzahl, lvcarea, l_artikel, l_bestand, l_besthis, l_lager
        nonlocal pvilanguage, inv_type, m_endkum, begindate, closedate

        lart = None
        Lart =  create_buffer("Lart",L_artikel)

        for l_bestand in db_session.query(L_bestand).order_by(L_bestand.artnr).all():

            if not lart:

                lart = get_cache (L_artikel, {"artnr": [(eq, l_bestand.artnr)]})

            elif lart and lart.artnr != l_bestand.artnr:

                lart = get_cache (L_artikel, {"artnr": [(eq, l_bestand.artnr)]})

            if (inv_type == 1 and lart.endkum < m_endkum) or (inv_type == 2 and lart.endkum >= m_endkum) or (inv_type == 3):

                # l_besthis = get_cache (L_besthis, {"anf_best_dat": [(eq, begindate)],"lager_nr": [(eq, l_bestand.lager_nr)],"artnr": [(eq, l_bestand.artnr)]})
                l_besthis = db_session.query(L_besthis).filter(
                         (L_besthis.anf_best_dat == begindate) & (L_besthis.lager_nr == l_bestand.lager_nr) & (L_besthis.artnr == l_bestand.artnr)).with_for_update().first()

                if not l_besthis:
                    l_besthis = L_besthis()
                    db_session.add(l_besthis)

                buffer_copy(l_bestand, l_besthis,except_fields=["l_bestand.anf_best_dat"])
                l_besthis.anf_best_dat = begindate


                pass
                pass


    def close_onhand():

        nonlocal t_its_ok, msg_str, msg_str2, its_ok, anzahl, lvcarea, l_artikel, l_bestand, l_besthis, l_lager
        nonlocal pvilanguage, inv_type, m_endkum, begindate, closedate

        l_onhand = None
        t_qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        L_onhand =  create_buffer("L_onhand",L_bestand)

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == 0) & ((L_bestand.anf_best_dat <= closedate) | (L_bestand.anf_best_dat == None) | (L_bestand.anf_best_dat >= closedate))).first()
        
        while None != l_bestand:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_bestand.artnr)]})

            if not l_artikel:
                msg_str2 = msg_str2 + chr_unicode(2) + "&W" + translateExtended ("Article not found for stock onhand", lvcarea, "") + " " + to_string(l_bestand.artnr, "9999999")

            elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):
                t_qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
                anzahl = close_onhand2(l_bestand.artnr, t_qty, wert)
                
                db_session.refresh(l_bestand, with_for_update=True)

                l_bestand.anz_anf_best =  to_decimal(anzahl)
                l_bestand.val_anf_best =  to_decimal(wert)
                l_bestand.anz_eingang =  to_decimal("0")
                l_bestand.wert_eingang =  to_decimal("0")
                l_bestand.anz_ausgang =  to_decimal("0")
                l_bestand.wert_ausgang =  to_decimal("0")
                l_bestand.anf_best_dat = closedate + timedelta(days=1)
                
                db_session.flush()

                if anzahl != 0:
                    avrg_price =  to_decimal(wert) / to_decimal(anzahl)

                    l_artikel = db_session.query(L_artikel).filter(
                             (L_artikel.artnr == l_bestand.artnr)).with_for_update().first()

                    if l_artikel:
                        l_artikel.vk_preis =  to_decimal(avrg_price)

            curr_recid = l_bestand._recid
            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == 0) & ((L_bestand.anf_best_dat <= closedate) | (L_bestand.anf_best_dat == None) | (L_bestand.anf_best_dat >= closedate)) & (L_bestand._recid > curr_recid)).first()


    def check_onhand():

        nonlocal t_its_ok, msg_str, msg_str2, its_ok, anzahl, lvcarea, l_artikel, l_bestand, l_besthis, l_lager
        nonlocal pvilanguage, inv_type, m_endkum, begindate, closedate

        its_ok = True

        def generate_inner_output():
            return (its_ok)


        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == 0) & ((L_bestand.anf_best_dat <= closedate) | (L_bestand.anf_best_dat == None))).first()
        while None != l_bestand:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_bestand.artnr)]})

            if l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Not updated Stock Onhand found for article :", lvcarea, "") + chr_unicode(10) + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr_unicode(10) + translateExtended ("Last Closing Date = ", lvcarea, "") + to_string(l_bestand.anf_best_dat) + chr_unicode(10) + translateExtended ("Fix the possible errors, THEN restart the program.", lvcarea, "")
                its_ok = False

                return generate_inner_output()

            curr_recid = l_bestand._recid
            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == 0) & ((L_bestand.anf_best_dat <= closedate) | (L_bestand.anf_best_dat == None)) & (L_bestand._recid > curr_recid)).first()

        return generate_inner_output()


    def close_onhand2(artnr:int, t_qty:Decimal, t_wert:Decimal):

        nonlocal t_its_ok, msg_str, msg_str2, its_ok, lvcarea, l_artikel, l_bestand, l_besthis, l_lager
        nonlocal pvilanguage, inv_type, m_endkum, begindate, closedate

        t_anz = to_decimal("0.0")
        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        l_onhand = None
        store = None

        def generate_inner_output():
            return (t_anz)

        L_onhand =  create_buffer("L_onhand",L_bestand)
        Store =  create_buffer("Store",L_lager)

        for store in db_session.query(Store).order_by(Store._recid).all():

            l_onhand = db_session.query(L_onhand).filter(
                     (L_onhand.artnr == artnr) & (L_onhand.lager_nr == store.lager_nr)).first()

            if l_onhand:
                anzahl = ( to_decimal(l_onhand.anz_anf_best) + to_decimal(l_onhand.anz_eingang) - to_decimal(l_onhand.anz_ausgang))
                t_anz =  to_decimal(t_anz) + to_decimal(anzahl)

                if t_qty != 0:
                    wert =  to_decimal(t_wert) * to_decimal(anzahl) / to_decimal(t_qty)
                else:
                    wert =  to_decimal("0")
                
                db_session.refresh(l_onhand, with_for_update=True)

                l_onhand.anz_anf_best =  to_decimal(anzahl)
                l_onhand.val_anf_best =  to_decimal(wert)
                l_onhand.anz_eingang =  to_decimal("0")
                l_onhand.wert_eingang =  to_decimal("0")
                l_onhand.anz_ausgang =  to_decimal("0")
                l_onhand.wert_ausgang =  to_decimal("0")
                l_onhand.anf_best_dat = closedate + timedelta(days=1)
                
                db_session.flush()

        return generate_inner_output()


    create_lbesthis()
    close_onhand()
    its_ok = check_onhand()
    t_its_ok = its_ok

    return generate_output()