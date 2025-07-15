#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_besthis, L_bestand, L_ophis, L_artikel

def close_inventory_step3bl(inv_type:int, m_endkum:int, closedate:date):

    prepare_cache ([L_besthis, L_bestand, L_ophis, L_artikel])

    startdate:date = None
    next_fdate:date = None
    curr_artnr:int = 0
    l_besthis = l_bestand = l_ophis = l_artikel = None

    lbuff = ltrans = l_bestand1 = None

    Lbuff = create_buffer("Lbuff",L_besthis)
    Ltrans = create_buffer("Ltrans",L_besthis)
    L_bestand1 = create_buffer("L_bestand1",L_bestand)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal startdate, next_fdate, curr_artnr, l_besthis, l_bestand, l_ophis, l_artikel
        nonlocal inv_type, m_endkum, closedate
        nonlocal lbuff, ltrans, l_bestand1


        nonlocal lbuff, ltrans, l_bestand1

        return {}

    startdate = date_mdy(get_month(closedate) , 1, get_year(closedate))
    next_fdate = closedate + timedelta(days=1)

    for l_ophis in db_session.query(L_ophis).filter(
             (L_ophis.datum >= startdate) & (L_ophis.datum <= closedate) & ((L_ophis.op_art >= 1) & (L_ophis.op_art <= 4))).order_by(L_ophis.artnr, L_ophis.datum, L_ophis.op_art).all():

        if curr_artnr != l_ophis.artnr:
            curr_artnr = l_ophis.artnr

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_ophis.artnr)]})

        if (inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or (inv_type == 3):

            l_besthis = get_cache (L_besthis, {"anf_best_dat": [(ge, startdate),(le, closedate)],"artnr": [(eq, l_ophis.artnr)],"lager_nr": [(eq, l_ophis.lager_nr)]})

            if not l_besthis:
                l_besthis = L_besthis()
                db_session.add(l_besthis)

                l_besthis.artnr = l_ophis.artnr
                l_besthis.anf_best_dat = startdate
                l_besthis.lager_nr = l_ophis.lager_nr

            lbuff = get_cache (L_besthis, {"anf_best_dat": [(ge, startdate),(le, closedate)],"artnr": [(eq, l_ophis.artnr)],"lager_nr": [(eq, 0)]})

            if not lbuff:
                lbuff = L_besthis()
                db_session.add(lbuff)

                lbuff.artnr = l_ophis.artnr
                lbuff.anf_best_dat = startdate
                lbuff.lager_nr = 0

            if l_ophis.op_art == 1:
                l_besthis.anz_eingang =  to_decimal(l_besthis.anz_eingang) + to_decimal(l_ophis.anzahl)
                lbuff.anz_eingang =  to_decimal(lbuff.anz_eingang) + to_decimal(l_ophis.anzahl)
                lbuff.wert_eingang =  to_decimal(lbuff.wert_eingang) + to_decimal(l_ophis.warenwert)

            elif l_ophis.op_art == 2:

                ltrans = get_cache (L_besthis, {"anf_best_dat": [(ge, startdate),(le, closedate)],"artnr": [(eq, l_ophis.artnr)],"lager_nr": [(eq, l_ophis.lief_nr)]})

                if not ltrans:
                    ltrans = L_besthis()
                    db_session.add(ltrans)

                    ltrans.artnr = l_ophis.artnr
                    ltrans.anf_best_dat = startdate
                    ltrans.lager_nr = l_ophis.lief_nr


                l_besthis.anz_eingang =  to_decimal(l_besthis.anz_eingang) + to_decimal(l_ophis.anzahl)
                ltrans.anz_ausgang =  to_decimal(ltrans.anz_ausgang) + to_decimal(l_ophis.anzahl)

            elif l_ophis.op_art == 3:
                l_besthis.anz_ausgang =  to_decimal(l_besthis.anz_ausgang) + to_decimal(l_ophis.anzahl)
                lbuff.anz_ausgang =  to_decimal(lbuff.anz_ausgang) + to_decimal(l_ophis.anzahl)
                lbuff.wert_ausgang =  to_decimal(lbuff.wert_ausgang) + to_decimal(l_ophis.warenwert)

            elif l_ophis.op_art == 4:
                lbuff.anz_ausgang =  to_decimal(lbuff.anz_ausgang) + to_decimal(l_ophis.anzahl)

    for l_besthis in db_session.query(L_besthis).filter(
                 (L_besthis.anf_best_dat >= startdate) & (L_besthis.anf_best_dat <= closedate) & (L_besthis.lager_nr == 0) & (L_besthis.anz_anf_best == 0)).order_by(L_besthis._recid).all():

        for lbuff in db_session.query(Lbuff).filter(
                     (Lbuff.artnr == l_besthis.artnr) & (Lbuff.anf_best_dat == l_besthis.anf_best_dat)).order_by(Lbuff._recid).all():
            lbuff.anz_anf_best =  to_decimal("0")
            lbuff.val_anf_best =  to_decimal("0")


    curr_artnr = 0

    for l_besthis in db_session.query(L_besthis).filter(
             (L_besthis.anf_best_dat >= startdate) & (L_besthis.anf_best_dat <= closedate)).order_by(L_besthis.artnr, L_besthis.lager_nr).all():

        if curr_artnr != l_besthis.artnr:
            curr_artnr = l_besthis.artnr

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, curr_artnr)]})

        if (inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or (inv_type == 3):

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_besthis.artnr)],"lager_nr": [(eq, l_besthis.lager_nr)],"anf_best_dat": [(eq, next_fdate)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

            l_bestand.artnr = l_besthis.artnr
            l_bestand.anf_best_dat = next_fdate
            l_bestand.lager_nr = l_besthis.lager_nr
            l_bestand.anz_anf_best =  to_decimal(l_besthis.anz_anf_best) +\
                    l_besthis.anz_eingang - to_decimal(l_besthis.anz_ausgang)
            l_bestand.val_anf_best =  to_decimal(l_besthis.val_anf_best) +\
                    l_besthis.wert_eingang - to_decimal(l_besthis.wert_ausgang)

            if l_bestand.lager_nr > 0 and l_bestand.anz_anf_best != 0:

                l_bestand1 = get_cache (L_bestand, {"artnr": [(eq, l_bestand.artnr)],"anf_best_dat": [(eq, l_bestand.anf_best_dat)],"lager_nr": [(eq, 0)]})

                if l_bestand1.anz_anf_best != 0:
                    l_bestand.val_anf_best =  to_decimal(l_bestand1.val_anf_best) *\
                        l_bestand.anz_anf_best / to_decimal(l_bestand1.anz_anf_best)


            pass
            pass

    return generate_output()