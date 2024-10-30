from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Gl_jouhdr

def prepare_gl_jourefbl():
    from_date = None
    to_date = None
    from_refno = ""
    ref_bez = ""
    htparam = gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, from_refno, ref_bez, htparam, gl_jouhdr

        return {"from_date": from_date, "to_date": to_date, "from_refno": from_refno, "ref_bez": ref_bez}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 558)).first()
    from_date = htparam.fdate + timedelta(days=1)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 597)).first()
    to_date = get_current_date()

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.datum == from_date)).first()

    if gl_jouhdr:
        from_refno = gl_jouhdr.refno
        ref_bez = gl_jouhdr.bezeich

    return generate_output()