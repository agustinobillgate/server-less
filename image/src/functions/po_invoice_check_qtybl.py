from functions.additional_functions import *
import decimal
from datetime import date
from models import L_artikel, L_op, Htparam, L_bestand

def po_invoice_check_qtybl(pvilanguage:int, qty:decimal, s_list_s_recid:int, s_list_artnr:int):
    msg_str = ""
    may_chg = False
    lvcarea:str = "po_invoice"
    l_artikel = l_op = htparam = l_bestand = None

    l_art = None

    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, may_chg, lvcarea, l_artikel, l_op, htparam, l_bestand
        nonlocal l_art


        nonlocal l_art
        return {"msg_str": msg_str, "may_chg": may_chg}

    def check_qty():

        nonlocal msg_str, may_chg, lvcarea, l_artikel, l_op, htparam, l_bestand
        nonlocal l_art


        nonlocal l_art

        f_endkum:int = 0
        b_endkum:int = 0
        m_endkum:int = 0
        billdate:date = None
        fb_closedate:date = None
        m_closedate:date = None
        qty1:decimal = 0
        L_art = L_artikel

        l_op = db_session.query(L_op).filter(
                (L_op._recid == s_list_s_recid)).first()

        if l_op.flag:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 257)).first()
        f_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 258)).first()
        b_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 268)).first()
        m_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
        fb_closedate = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
        m_closedate = htparam.fdate

        l_art = db_session.query(L_art).filter(
                (L_art.artnr == s_list_artnr)).first()

        if ((l_art.endkum == f_endkum or l_art.endkum == b_endkum) and l_op.datum > fb_closedate) or (l_art.endkum >= m_endkum and l_op.datum > m_closedate):

            return

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == l_op.lager_nr)).first()
        qty1 = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang + qty - l_op.anzahl

        if qty1 < 0:
            msg_str = msg_str + chr(2) + translateExtended ("Onhand qty in Store ", lvcarea, "") + to_string(l_op.lager_nr, "99") + " " + translateExtended ("would become negative", lvcarea, "") + "  ==  " + trim(to_string(qty1, "->>>,>>>,>>9.99")) + chr(10) + translateExtended ("The entered qty is therefore not possible.", lvcarea, "")
            may_chg = False

    check_qty()

    return generate_output()