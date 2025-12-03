#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_artikel, L_lager, L_bestand, Htparam

def close_inventory1bl(inv_type:int, m_endkum:int, user_init:string, closedate:date, todate:date):

    prepare_cache ([L_op, L_artikel, L_lager, Htparam])

    l_op = l_artikel = l_lager = l_bestand = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op, l_artikel, l_lager, l_bestand, htparam
        nonlocal inv_type, m_endkum, user_init, closedate, todate

        return {}

    def update_onhand():

        nonlocal l_op, l_artikel, l_lager, l_bestand, htparam
        nonlocal inv_type, m_endkum, user_init, closedate, todate

        s_artnr:int = 0
        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        transdate:date = None
        curr_lager:int = 0
        tot_anz:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        s_artnr = l_op.artnr
        anzahl =  to_decimal(l_op.anzahl)
        wert =  to_decimal(l_op.warenwert)
        transdate = l_op.datum
        curr_lager = l_op.lager_nr

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == 0) & (L_bestand.artnr == s_artnr)).with_for_update().first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = transdate

        if l_op.op_art <= 2:
            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
        else:
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)

        pass

        if l_op.herkunftflag != 2:
            tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
            tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

            if tot_anz != 0:
                db_session.refresh(l_artikel, with_for_update=True)

                avrg_price =  to_decimal(tot_wert) / to_decimal(tot_anz)
                l_artikel.vk_preis =  to_decimal(avrg_price)

                db_session.flush()

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == curr_lager) & (L_bestand.artnr == s_artnr)).with_for_update().first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.lager_nr = curr_lager
            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = transdate

        if l_op.op_art <= 2:
            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
        else:
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)
        

    for l_op in db_session.query(L_op).filter(
             (L_op.op_art <= 4) & (L_op.loeschflag < 2) & (L_op.datum > closedate) & (L_op.datum <= todate)).order_by(L_op._recid).all():

        if l_op.op_art == 1 or (l_op.op_art == 2 and l_op.herkunftflag == 3) or l_op.op_art == 3 or l_op.op_art == 4:

            l_artikel = db_session.query(L_artikel).filter(
                 (L_artikel.artnr == l_op.artnr)).first()

            if l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):
                update_onhand()

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == l_lager.lager_nr) & ((L_bestand.anf_best_dat <= closedate) | (L_bestand.anf_best_dat == None))).first()
        while None != l_bestand:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_bestand.artnr)]})

            if not l_artikel:
                db_session.refresh(l_bestand, with_for_update=True)
                db_session.delete(l_bestand)
                db_session.flush()

            elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):

                if (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang) == 0:
                    db_session.refresh(l_bestand, with_for_update=True)
                    db_session.delete(l_bestand)
                    db_session.flush()

            curr_recid = l_bestand._recid
            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr) & ((L_bestand.anf_best_dat <= closedate) | (L_bestand.anf_best_dat == None)) & (L_bestand._recid > curr_recid)).first()

    l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == 0) & ((L_bestand.anf_best_dat <= closedate) | (L_bestand.anf_best_dat == None))).first()
    while None != l_bestand:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_bestand.artnr)]})

        if not l_artikel:
            db_session.refresh(l_bestand, with_for_update=True)
            db_session.delete(l_bestand)
            db_session.flush()

        elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):

            if l_bestand.anz_anf_best == 0 and l_bestand.anz_eingang == 0 and l_bestand.anz_ausgang == 0:
                db_session.refresh(l_bestand, with_for_update=True)
                db_session.delete(l_bestand)
                db_session.flush()

        curr_recid = l_bestand._recid
        l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == 0) & ((L_bestand.anf_best_dat <= closedate) | (L_bestand.anf_best_dat == None)) & (L_bestand._recid > curr_recid)).first()

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == l_lager.lager_nr) & ((L_bestand.anf_best_dat <= closedate) | (L_bestand.anf_best_dat == None))).first()
        while None != l_bestand:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_bestand.artnr)]})

            if not l_artikel:
                db_session.refresh(l_bestand, with_for_update=True)
                db_session.delete(l_bestand)
                db_session.flush()

            elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):

                if l_bestand.anz_anf_best == 0 and l_bestand.anz_eingang == 0 and l_bestand.anz_ausgang == 0:
                    db_session.refresh(l_bestand, with_for_update=True)
                    db_session.delete(l_bestand)
                    db_session.flush()

            curr_recid = l_bestand._recid
            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr) & ((L_bestand.anf_best_dat <= closedate) | (L_bestand.anf_best_dat == None)) & (L_bestand._recid > curr_recid)).first()

    if inv_type == 1:

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 224).with_for_update().first()
        htparam.fdate = todate
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    elif inv_type == 2:

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 221).with_for_update().first()
        htparam.fdate = todate
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    elif inv_type == 3:

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 221).with_for_update().first()
        htparam.fdate = todate

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 224).with_for_update().first()
        htparam.fdate = todate
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 232).with_for_update().first()
    htparam.flogical = False
    htparam.lupdate = get_current_date()
    htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    return generate_output()