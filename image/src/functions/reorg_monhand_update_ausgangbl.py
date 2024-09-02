from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_op, L_artikel, L_bestand

def reorg_monhand_update_ausgangbl(art_type:int):
    main_grp:int = 0
    to_grp:int = 0
    to_date:date = None
    from_date:date = None
    htparam = l_op = l_artikel = l_bestand = None

    bbest = None

    Bbest = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_op, l_artikel, l_bestand
        nonlocal bbest


        nonlocal bbest
        return {}

    def update_ausgang():

        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_op, l_artikel, l_bestand
        nonlocal bbest


        nonlocal bbest

        s_artnr:int = 0
        anzahl:decimal = 0
        wert:decimal = 0
        transdate:date = None
        curr_lager:int = 0
        Bbest = L_bestand
        s_artnr = l_op.artnr
        anzahl = l_op.anzahl
        wert = l_op.warenwert
        transdate = l_op.datum
        curr_lager = l_op.lager_nr

        if l_op.op_art == 3 or (l_op.op_art == 4):

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = transdate
                l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
                l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert


            else:

                bbest = db_session.query(Bbest).filter(
                        (Bbest._recid == l_bestand._recid)).first()
                bbest.anz_ausgang = bbest.anz_ausgang + anzahl
                bbest.wert_ausgang = bbest.wert_ausgang + wert

                bbest = db_session.query(Bbest).first()


        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.lager_nr = curr_lager
            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = transdate
            l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert


        else:

            bbest = db_session.query(Bbest).filter(
                    (Bbest._recid == l_bestand._recid)).first()
            bbest.anz_ausgang = bbest.anz_ausgang + anzahl
            bbest.wert_ausgang = bbest.wert_ausgang + wert

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
            ((L_op.op_art == 3) |  (L_op.op_art == 4)) &  (L_op.loeschflag < 2) &  ((L_op.datum >= from_date) &  (L_op.datum <= to_date)) &  (L_op.pos >= 1) &  (L_op.lager_nr > 0)).all():

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_op.artnr)).first()

        if l_artikel and l_artikel.endkum >= main_grp and l_artikel.endkum <= to_grp:
            update_ausgang()

    return generate_output()