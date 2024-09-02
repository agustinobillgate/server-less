from functions.additional_functions import *
import decimal
from sqlalchemy import func
from functions.create_lartjob import create_lartjob
from models import L_ophdr, L_op, L_bestand, L_artikel, L_verbrauch

def stock_outlist_del_opbl(str_list_op_recid:int, bediener_nr:int):
    l_ophdr = l_op = l_bestand = l_artikel = l_verbrauch = None

    l_oph = None

    L_oph = L_ophdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr, l_op, l_bestand, l_artikel, l_verbrauch
        nonlocal l_oph


        nonlocal l_oph
        return {}

    def del_op():

        nonlocal l_ophdr, l_op, l_bestand, l_artikel, l_verbrauch
        nonlocal l_oph


        nonlocal l_oph

        qty:decimal = 0
        val:decimal = 0
        L_oph = L_ophdr

        l_op = db_session.query(L_op).filter(
                (L_op._recid == str_list_op_recid)).first()
        l_op.loeschflag = 2
        l_op.fuellflag = bediener_nr

        l_op = db_session.query(L_op).first()

        l_oph = db_session.query(L_oph).filter(
                (L_oph.lscheinnr == l_op.lscheinnr) &  (func.lower(L_oph.op_typ) == "STT")).first()

        if l_oph and l_oph.betriebsnr != 0:
            get_output(create_lartjob(l_oph._recid, l_op.artnr, - l_op.anzahl, - l_op.warenwert, l_op.datum, False))

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == 0)).first()

        if l_bestand:
            l_bestand.anz_ausgang = l_bestand.anz_ausgang - l_op.anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang - l_op.warenwert

            l_bestand = db_session.query(L_bestand).first()
            qty = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
            val = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

        if qty != 0:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_op.artnr)).first()
            l_artikel.vk_preis = val / qty

            l_artikel = db_session.query(L_artikel).first()

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == l_op.lager_nr)).first()

        if l_bestand:
            l_bestand.anz_ausgang = l_bestand.anz_ausgang - l_op.anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang - l_op.warenwert

            l_bestand = db_session.query(L_bestand).first()

        l_verbrauch = db_session.query(L_verbrauch).filter(
                (L_verbrauch.artnr == l_op.artnr) &  (L_verbrauch.datum == l_op.datum)).first()

        if l_verbrauch:
            l_verbrauch.anz_verbrau = l_verbrauch.anz_verbrau - l_op.anzahl
            l_verbrauch.wert_verbrau = l_verbrauch.wert_verbrau + l_op.warenwert

            l_verbrauch = db_session.query(L_verbrauch).first()

    del_op()

    return generate_output()