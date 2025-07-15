#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import L_artikel, Gl_acct, L_untergrup, Gl_jouhdr, Gl_journal

def s_stockout_check_artnrbl(pvilanguage:int, out_type:int, s_artnr:int, transdate:date):

    prepare_cache ([L_artikel, Gl_acct, L_untergrup, Gl_jouhdr])

    accepted = True
    msg_str = ""
    lvcarea:string = "s-stockout"
    l_artikel = gl_acct = l_untergrup = gl_jouhdr = gl_journal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal accepted, msg_str, lvcarea, l_artikel, gl_acct, l_untergrup, gl_jouhdr, gl_journal
        nonlocal pvilanguage, out_type, s_artnr, transdate

        return {"accepted": accepted, "msg_str": msg_str}

    def check_artnr():

        nonlocal accepted, msg_str, lvcarea, l_artikel, gl_acct, l_untergrup, gl_jouhdr, gl_journal
        nonlocal pvilanguage, out_type, s_artnr, transdate

        l_art = None
        L_art =  create_buffer("L_art",L_artikel)

        if out_type == 1:

            return

        l_art = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_art.fibukonto)]})

        if not gl_acct:

            l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_art.zwkum)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

            if not gl_acct:

                return

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.BATCH) & (Gl_jouhdr.jtype == 3) & (Gl_jouhdr.datum >= transdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal = db_session.query(Gl_journal).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr) & (Gl_journal.fibukonto == gl_acct.fibukonto) & (matches(Gl_journal.bemerk,("*;&&5;")))).first()

            if gl_journal:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Journal Transfer to G/L found on", lvcarea, "") + " " + to_string(gl_jouhdr.datum)
                accepted = False

                return


    check_artnr()

    return generate_output()