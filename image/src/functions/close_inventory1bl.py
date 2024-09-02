from functions.additional_functions import *
import decimal
from datetime import date
from models import L_op, L_artikel, L_lager, L_bestand, Htparam

def close_inventory1bl(inv_type:int, m_endkum:int, user_init:str, closedate:date, todate:date):
    l_op = l_artikel = l_lager = l_bestand = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op, l_artikel, l_lager, l_bestand, htparam


        return {}

    def update_onhand():

        nonlocal l_op, l_artikel, l_lager, l_bestand, htparam

        s_artnr:int = 0
        anzahl:decimal = 0
        wert:decimal = 0
        transdate:date = None
        curr_lager:int = 0
        tot_anz:decimal = 0
        tot_wert:decimal = 0
        avrg_price:decimal = 0
        s_artnr = l_op.artnr
        anzahl = l_op.anzahl
        wert = l_op.warenwert
        transdate = l_op.datum
        curr_lager = l_op.lager_nr

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = transdate

        if l_op.op_art <= 2:
            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert
        else:
            l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

        l_bestand = db_session.query(L_bestand).first()

        if l_op.herkunftflag != 2:
            tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
            tot_wert = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

            if tot_anz != 0:
                avrg_price = tot_wert / tot_anz

                l_artikel = db_session.query(L_artikel).first()
                l_artikel.vk_preis = avrg_price

                l_artikel = db_session.query(L_artikel).first()

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.lager_nr = curr_lager
            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = transdate

        if l_op.op_art <= 2:
            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert
        else:
            l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

        l_bestand = db_session.query(L_bestand).first()


    for l_op in db_session.query(L_op).filter(
            (L_op.op_art <= 4) &  (L_op.loeschflag < 2) &  (L_op.datum > closedate) &  (L_op.datum <= todate)).all():

        if l_op.op_art == 1 or (l_op.op_art == 2 and l_op.herkunftflag == 3) or l_op.op_art == 3 or l_op.op_art == 4:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_op.artnr)).first()

            if l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):
                update_onhand()

    for l_lager in db_session.query(L_lager).all():

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == l_lager.lager_nr) &  ((L_bestand.anf_best_dat <= closedate) |  (L_bestand.anf_best_dat == None))).first()
        while None != l_bestand:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_bestand.artnr)).first()

            if not l_artikel:

                l_bestand = db_session.query(L_bestand).first()
                db_session.delete(l_bestand)

            elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):

                if (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang) == 0:

                    l_bestand = db_session.query(L_bestand).first()
                    db_session.delete(l_bestand)

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr) &  ((L_bestand.anf_best_dat <= closedate) |  (L_bestand.anf_best_dat == None))).first()

    l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  ((L_bestand.anf_best_dat <= closedate) |  (L_bestand.anf_best_dat == None))).first()
    while None != l_bestand:

        l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_bestand.artnr)).first()

        if not l_artikel:

            l_bestand = db_session.query(L_bestand).first()
            db_session.delete(l_bestand)

        elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):

            if l_bestand.anz_anf_best == 0 and l_bestand.anz_eingang == 0 and l_bestand.anz_ausgang == 0:

                l_bestand = db_session.query(L_bestand).first()
                db_session.delete(l_bestand)

        l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0) &  ((L_bestand.anf_best_dat <= closedate) |  (L_bestand.anf_best_dat == None))).first()

    for l_lager in db_session.query(L_lager).all():

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == l_lager.lager_nr) &  ((L_bestand.anf_best_dat <= closedate) |  (L_bestand.anf_best_dat == None))).first()
        while None != l_bestand:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_bestand.artnr)).first()

            if not l_artikel:

                l_bestand = db_session.query(L_bestand).first()
                db_session.delete(l_bestand)

            elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):

                if l_bestand.anz_anf_best == 0 and l_bestand.anz_eingang == 0 and l_bestand.anz_ausgang == 0:

                    l_bestand = db_session.query(L_bestand).first()
                    db_session.delete(l_bestand)

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr) &  ((L_bestand.anf_best_dat <= closedate) |  (L_bestand.anf_best_dat == None))).first()

    if inv_type == 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
        htparam.fdate = todate
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        htparam = db_session.query(Htparam).first()

    elif inv_type == 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
        htparam.fdate = todate
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        htparam = db_session.query(Htparam).first()

    elif inv_type == 3:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
        htparam.fdate = todate

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
        htparam.fdate = todate
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 232)).first()
    htparam.flogical = False
    htparam.lupdate = get_current_date()
    htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    htparam = db_session.query(Htparam).first()


    return generate_output()