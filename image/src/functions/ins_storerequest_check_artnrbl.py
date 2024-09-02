from functions.additional_functions import *
import decimal
from datetime import date
from models import L_artikel, Gl_acct, L_untergrup, Gl_jouhdr, Gl_journal

def ins_storerequest_check_artnrbl(pvilanguage:int, s_artnr:int, transdate:date):
    msg_str = ""
    lvcarea:str = "ins_storerequest"
    l_artikel = gl_acct = l_untergrup = gl_jouhdr = gl_journal = None

    l_art = None

    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, l_artikel, gl_acct, l_untergrup, gl_jouhdr, gl_journal
        nonlocal l_art


        nonlocal l_art
        return {"msg_str": msg_str}


    l_art = db_session.query(L_art).filter(
            (L_art.artnr == s_artnr)).first()

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == l_art.fibukonto)).first()

    if not gl_acct:

        l_untergrup = db_session.query(L_untergrup).filter(
                (L_untergrup.zwkum == l_art.zwkum)).first()

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

        if not gl_acct:

            return generate_output()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.activeflag == 0) &  (Gl_jouhdr.BATCH) &  (Gl_jouhdr.jtype == 3) &  (Gl_jouhdr.datum >= transdate)).all():

        gl_journal = db_session.query(Gl_journal).filter(
                (Gl_journal.jnr == gl_jouhdr.jnr) &  (Gl_journal.fibukonto == gl_acct.fibukonto) &  (Gl_journal.bemerk.op("~")(".*;&&5;"))).first()

        if gl_journal:
            msg_str = translateExtended ("Journal Transfer to G/L found on", lvcarea, "") + " " + to_string(gl_jouhdr.datum)
            s_artnr = 0

            return generate_output()