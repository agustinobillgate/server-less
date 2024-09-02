from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, L_kredit, L_artikel, L_untergrup, Gl_acct, Gl_jouhdr, Gl_journal, Htparam, L_bestand

def supply_inlist_btn_deletebl(pvilanguage:int, str_list_billdate:date, str_list_lief_nr:int, str_list_docu_nr:str, str_list_lscheinnr:str, str_list_l_recid:int, str_list_artnr:int):
    may_delete = False
    msg_str = ""
    msg_str1 = ""
    msg_str2 = ""
    art_fibu:str = ""
    lvcarea:str = "supply_inlist"
    l_op = l_kredit = l_artikel = l_untergrup = gl_acct = gl_jouhdr = gl_journal = htparam = l_bestand = None

    incoming_op = l_op = None

    Incoming_op = L_op
    L_op = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal may_delete, msg_str, msg_str1, msg_str2, art_fibu, lvcarea, l_op, l_kredit, l_artikel, l_untergrup, gl_acct, gl_jouhdr, gl_journal, htparam, l_bestand
        nonlocal incoming_op, l_op


        nonlocal incoming_op, l_op
        return {"may_delete": may_delete, "msg_str": msg_str, "msg_str1": msg_str1, "msg_str2": msg_str2}

    def check_onhand_after_cancel_receiving():

        nonlocal may_delete, msg_str, msg_str1, msg_str2, art_fibu, lvcarea, l_op, l_kredit, l_artikel, l_untergrup, gl_acct, gl_jouhdr, gl_journal, htparam, l_bestand
        nonlocal incoming_op, l_op


        nonlocal incoming_op, l_op

        f_endkum:int = 0
        b_endkum:int = 0
        m_endkum:int = 0
        billdate:date = None
        fb_closedate:date = None
        m_closedate:date = None
        qty:decimal = 0
        trf_gl:date = None

        if str_list_l_recid == 0:
            msg_str1 = msg_str1 + chr(2) + translateExtended ("Old record(s) can not be deleted,", lvcarea, "") + translateExtended ("Cancel Receiving not possible.", lvcarea, "")

            return

        l_op = db_session.query(L_op).filter(
                (L_op._recid == str_list_l_recid)).first()

        if l_op.flag:
            may_delete = True

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 269)).first()

        if htparam:
            trf_gl = htparam.fdate

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

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and str_list_billdate > fb_closedate) or (l_artikel.endkum >= m_endkum and str_list_billdate > m_closedate):
            may_delete = True

            return

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == l_op.lager_nr)).first()
        qty = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang - l_op.anzahl

        if qty < 0:
            msg_str1 = msg_str1 + chr(2) + translateExtended ("Onhand qty in Store ", lvcarea, "") + to_string(l_op.lager_nr, "99") + " " + translateExtended ("would become (-)  == ", lvcarea, "") + " " + trim(to_string(qty, "->,>>>,>>>,>>9.99")) + chr(10) + translateExtended ("Cancel Receiving not possible.", lvcarea, "")

            return
        may_delete = True

        if str_list_billdate <= trf_gl:
            may_delete = False
            msg_str1 = msg_str1 + chr(2) + translateExtended ("Receiving have been transfered to the G/L, ", lvcarea, "") + translateExtended ("cancel Receiving not possible.", lvcarea, "")

            return


    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit.lief_nr == str_list_lief_nr) &  (func.lower(L_kredit.name) == (str_list_docu_nr).lower()) &  (func.lower(L_kredit.lscheinnr) == (str_list_lscheinnr).lower()) &  (L_kredit.opart >= 1) &  (L_kredit.zahlkonto > 0)).first()

    if l_kredit:
        msg_str = msg_str + chr(2) + translateExtended ("The A/P Payment record found.", lvcarea, "") + chr(10) + translateExtended ("Cancel Receiving is no longer possible.", lvcarea, "")

        return generate_output()

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == str_list_artnr)).first()

    l_untergrup = db_session.query(L_untergrup).filter(
            (L_untergrup.zwkum == l_artikel.zwkum)).first()

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

    if not gl_acct:

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == l_artikel.fibukonto)).first()

    if gl_acct:
        art_fibu = gl_acct.fibukonto

    if art_fibu != "":

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.datum >= str_list_billdate) &  (Gl_jouhdr.jtyp == 6) &  (Gl_jouhdr.refno.op("~")("RCV.*"))).all():

            gl_journal = db_session.query(Gl_journal).filter(
                    (Gl_journal.jnr == gl_jouhdr.jnr) &  (func.lower(Gl_journal.fibukonto) == (art_fibu).lower())).first()

            if gl_journal:
                msg_str = msg_str + chr(2) + translateExtended ("Stock receiving records have been transfered to the G/L.", lvcarea, "") + chr(10) + translateExtended ("Cancel Receiving is no longer possible.", lvcarea, "")
                break

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.datum >= str_list_billdate) &  (Gl_jouhdr.jtyp == 3) &  (Gl_jouhdr.refno.op("~")("OUT.*"))).all():

            gl_journal = db_session.query(Gl_journal).filter(
                    (Gl_journal.jnr == gl_jouhdr.jnr) &  (func.lower(Gl_journal.fibukonto) == (art_fibu).lower())).first()

            if gl_journal:
                msg_str = msg_str + chr(2) + translateExtended ("Stock outgoing records have been transfered to the G/L.", lvcarea, "") + chr(10) + translateExtended ("Cancel outgoing is no longer possible.", lvcarea, "")
                break

    if msg_str != "":

        return generate_output()
    check_onhand_after_cancel_receiving()

    if not may_delete:

        return generate_output()

    l_op = db_session.query(L_op).filter(
            (L_op.datum >= str_list_billdate) &  (L_op.artnr == str_list_artnr) &  (L_op.op_art >= 2) &  (L_op.op_art <= 4) &  (not L_op.flag)).first()

    if l_op:
        msg_str2 = "&W" + translateExtended ("Stock receiving record(s) exist for this article.", lvcarea, "") + chr(10) + translateExtended ("The stock receiving amount will be adjusted. ", lvcarea, "")

    return generate_output()