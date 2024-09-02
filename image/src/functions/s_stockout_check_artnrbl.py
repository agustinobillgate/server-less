from functions.additional_functions import *
import decimal
from datetime import date
from models import L_artikel, Gl_acct, L_untergrup, Gl_jouhdr, Gl_journal

def s_stockout_check_artnrbl(pvilanguage:int, out_type:int, s_artnr:int, transdate:date):
    accepted = False
    msg_str = ""
    lvcarea:str = "s_stockout"
    l_artikel = gl_acct = l_untergrup = gl_jouhdr = gl_journal = None

    l_art = None

    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal accepted, msg_str, lvcarea, l_artikel, gl_acct, l_untergrup, gl_jouhdr, gl_journal
        nonlocal l_art


        nonlocal l_art
        return {"accepted": accepted, "msg_str": msg_str}

    def check_artnr():

        nonlocal accepted, msg_str, lvcarea, l_artikel, gl_acct, l_untergrup, gl_jouhdr, gl_journal
        nonlocal l_art


        nonlocal l_art


        L_art = L_artikel

        if out_type == 1:

            return

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

                return

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.activeflag == 0) &  (Gl_jouhdr.BATCH) &  (Gl_jouhdr.jtype == 3) &  (Gl_jouhdr.datum >= transdate)).all():

            gl_journal = db_session.query(Gl_journal).filter(
                    (Gl_journal.jnr == gl_jouhdr.jnr) &  (Gl_journal.fibukonto == gl_acct.fibukonto) &  (Gl_journal.bemerk.op("~")(".*;&&5;"))).first()

            if gl_journal:
                msg_str = msg_str + chr(2) + translateExtended ("Journal Transfer to G/L found on", lvcarea, "") + " " + to_string(gl_jouhdr.datum)
                accepted = False

                return

    check_artnr()

    return generate_output()