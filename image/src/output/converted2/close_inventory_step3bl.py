from functions.additional_functions import *
import decimal
from datetime import date
from models import L_besthis, L_bestand, L_ophis, L_artikel

def close_inventory_step3bl(inv_type:int, m_endkum:int, closedate:date):
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

            l_artikel = db_session.query(L_artikel).filter(
                     (L_artikel.artnr == l_ophis.artnr)).first()

        if (inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or (inv_type == 3):

            l_besthis = db_session.query(L_besthis).filter(
                     (L_besthis.anf_best_dat >= startdate) & (L_besthis.anf_best_dat <= closedate) & (L_besthis.artnr == l_ophis.artnr) & (L_besthis.lager_nr == l_ophis.lager_nr)).first()

            if not l_besthis:
                l_besthis = L_besthis()
                db_session.add(l_besthis)

                l_besthis.artnr = l_ophis.artnr
                l_besthis.anf_best_dat = startdate
                l_besthis.lager_nr = l_ophis.lager_nr

        lbuff = db_session.query(Lbuff).filter(
                 (Lbuff.anf_best_dat >= startdate) & (Lbuff.anf_best_dat <= closedate) & (Lbuff.artnr == l_ophis.artnr) & (Lbuff.lager_nr == 0)).first()

        if not lbuff:
            lbuff = Lbuff()
            db_session.add(lbuff)

            lbuff.artnr = l_ophis.artnr
            lbuff.anf_best_dat = startdate
            lbuff.lager_nr = 0

        if l_ophis.op_art == 1:
            l_besthis.anz_eingang =  to_decimal(l_besthis.anz_eingang) + to_decimal(l_ophis.anzahl)
            lbuff.anz_eingang =  to_decimal(lbuff.anz_eingang) + to_decimal(l_ophis.anzahl)
            lbuff.wert_eingang =  to_decimal(lbuff.wert_eingang) + to_decimal(l_ophis.warenwert)

        elif l_ophis.op_art == 2:

            ltrans = db_session.query(Ltrans).filter(
                     (Ltrans.anf_best_dat >= startdate) & (Ltrans.anf_best_dat <= closedate) & (Ltrans.artnr == l_ophis.artnr) & (Ltrans.lager_nr == l_ophis.lief_nr)).first()

            if not ltrans:
                ltrans = Ltrans()
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

            l_artikel = db_session.query(L_artikel).filter(
                     (L_artikel.artnr == curr_artnr)).first()

        if (inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or (inv_type == 3):

            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.artnr == l_besthis.artnr) & (L_bestand.lager_nr == l_besthis.lager_nr) & (L_bestand.anf_best_dat == next_fdate)).first()

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

                l_bestand1 = db_session.query(L_bestand1).filter(
                         (L_bestand1.artnr == l_bestand.artnr) & (L_bestand1.anf_best_dat == l_bestand.anf_best_dat) & (L_bestand1.lager_nr == 0)).first()

                if l_bestand1.anz_anf_best != 0:
                    l_bestand.val_anf_best =  to_decimal(l_bestand1.val_anf_best) *\
                        l_bestand.anz_anf_best / to_decimal(l_bestand1.anz_anf_best)


        pass

    return generate_output()