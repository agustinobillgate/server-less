from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, L_op, L_artikel, Bediener, L_bestand

def reorg_monhand_update_eingang_1bl(art_type:int, user_init:str):
    main_grp:int = 0
    to_grp:int = 0
    to_date:date = None
    from_date:date = None
    htparam = l_op = l_artikel = bediener = l_bestand = None

    l_op1 = bbest = None

    L_op1 = L_op
    Bbest = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_op, l_artikel, bediener, l_bestand
        nonlocal l_op1, bbest


        nonlocal l_op1, bbest
        return {}

    def checkin_outgoing():

        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_op, l_artikel, bediener, l_bestand
        nonlocal l_op1, bbest


        nonlocal l_op1, bbest


        L_op1 = L_op

        l_op1 = db_session.query(L_op1).filter(
                (L_op1.artnr == l_op.artnr) &  (L_op1.op_art == 3) &  (L_op1.lief_nr == l_op.lief_nr) &  (L_op1.lscheinnr == l_op.lscheinnr) &  (L_op1.herkunftflag == 2) &  (L_op1.lager_nr == l_op.lager_nr)).first()

        if l_op1:

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            l_op1.loeschflag = 2
            l_op1.betriebsnr = bediener.nr

            l_op1 = db_session.query(L_op1).first()

    def update_eingang():

        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_op, l_artikel, bediener, l_bestand
        nonlocal l_op1, bbest


        nonlocal l_op1, bbest

        s_artnr:int = 0
        anzahl:decimal = 0
        wert:decimal = 0
        transdate:date = None
        curr_lager:int = 0
        tot_anz:decimal = 0
        tot_wert:decimal = 0
        avrg_price:decimal = 0
        Bbest = L_bestand
        s_artnr = l_op.artnr
        anzahl = l_op.anzahl
        wert = l_op.warenwert
        transdate = l_op.datum
        curr_lager = l_op.lager_nr

        if l_op.op_art == 1 or (l_op.op_art == 2):

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = transdate
                l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
                l_bestand.wert_eingang = l_bestand.wert_eingang + wert


            else:

                bbest = db_session.query(Bbest).filter(
                        (Bbest._recid == l_bestand._recid)).first()
                bbest.anz_eingang = bbest.anz_eingang + anzahl
                bbest.wert_eingang = bbest.wert_eingang + wert

                bbest = db_session.query(Bbest).first()


        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.lager_nr = curr_lager
            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = transdate
            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert


        else:

            bbest = db_session.query(Bbest).filter(
                    (Bbest._recid == l_bestand._recid)).first()
            bbest.anz_eingang = bbest.anz_eingang + anzahl
            bbest.wert_eingang = bbest.wert_eingang + wert

            bbest = db_session.query(Bbest).first()

    if art_type == 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 257)).first()
        main_grp = htparam.finteger
        to_grp = main_grp

    elif art_type == 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 258)).first()
        main_grp = htparam.finteger
        to_grp = main_grp

    elif art_type == 3:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 268)).first()
        main_grp = htparam.finteger
        to_grp = 9

    if art_type <= 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
    to_date = fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    for l_op in db_session.query(L_op).filter(
            ((L_op.op_art == 1) |  (L_op.op_art == 2)) &  (L_op.loeschflag < 2) &  ((L_op.datum >= from_date) &  (L_op.datum <= to_date)) &  (L_op.pos >= 1) &  (L_op.lager_nr > 0)).all():

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_op.artnr)).first()

        if l_artikel and l_artikel.endkum >= main_grp and l_artikel.endkum <= to_grp:
            update_eingang()

    for l_op in db_session.query(L_op).filter(
            ((L_op.op_art == 1) |  (L_op.op_art == 2)) &  (L_op.loeschflag == 2) &  ((L_op.datum >= from_date) &  (L_op.datum <= to_date)) &  (L_op.pos >= 1) &  (L_op.lager_nr > 0)).all():

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_op.artnr)).first()

        if l_artikel and l_artikel.endkum >= main_grp and l_artikel.endkum <= to_grp and l_op.flag :
            checkin_outgoing()

    return generate_output()