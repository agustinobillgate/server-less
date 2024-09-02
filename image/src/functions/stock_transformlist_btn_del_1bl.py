from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, L_bestand, L_verbrauch

def stock_transformlist_btn_del_1bl(t_list_datum:date, t_list_lscheinnr:str):
    successflag = False
    l_op = l_bestand = l_verbrauch = None

    l_op1 = None

    L_op1 = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, l_op, l_bestand, l_verbrauch
        nonlocal l_op1


        nonlocal l_op1
        return {"successflag": successflag}


    for l_op in db_session.query(L_op).filter(
                (L_op.datum == t_list_datum) &  ((L_op.op_art == 2) |  (L_op.op_art == 4)) &  (func.lower(L_op.lscheinnr) == (t_list_lscheinnr).lower()) &  (L_op.loeschflag <= 1)).all():

        if l_op.op_art == 2:

            l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == l_op.lager_nr)).first()

            if l_bestand:
                l_bestand.anz_eingang = l_bestand.anz_eingang - l_op.anzahl
                l_bestand.wert_eingang = l_bestand.wert_eingang - l_op.warenwert

                l_bestand = db_session.query(L_bestand).first()

            l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == 0)).first()

            if l_bestand:
                l_bestand.anz_eingang = l_bestand.anz_eingang - l_op.anzahl
                l_bestand.wert_eingang = l_bestand.wert_eingang - l_op.warenwert

                l_bestand = db_session.query(L_bestand).first()

        elif l_op.op_art == 4:

            l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == l_op.lager_nr)).first()

            if l_bestand:
                l_bestand.anz_ausgang = l_bestand.anz_ausgang + l_op.anzahl
                l_bestand.wert_ausgang = l_bestand.wert_ausgang + l_op.warenwert

                l_bestand = db_session.query(L_bestand).first()

            l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == l_op.artnr and L_bestand.lager_nr == 0)).first()

            if l_bestand:
                l_bestand.anz_ausgang = l_bestand.anz_ausgang + l_op.anzahl
                l_bestand.wert_ausgang = l_bestand.wert_ausgang + l_op.warenwert

                l_bestand = db_session.query(L_bestand).first()

            l_verbrauch = db_session.query(L_verbrauch).filter(
                        (L_verbrauch.artnr == l_op.artnr) &  (L_verbrauch.datum == l_op.datum)).first()

            if l_verbrauch:
                l_verbrauch.anz_verbrau = l_verbrauch.anz_verbrau - l_op.anzahl
                l_verbrauch.wert_verbrau = l_verbrauch.wert_verbrau - l_op.warenwert

                l_verbrauch = db_session.query(L_verbrauch).first()

        l_op1 = db_session.query(L_op1).filter(
                    (L_op1._recid == l_op._recid)).first()

        if l_op1:
            l_op1.loeschflag = 2


            successflag = True

            l_op1 = db_session.query(L_op1).first()
        else:
            successflag = False


    return generate_output()