#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Htparam

def prepare_gljour_listbl(sorttype:int):

    prepare_cache ([Htparam])

    from_date = None
    to_date = None
    t_gl_jouhdr_data = []
    gl_jouhdr = htparam = None

    t_gl_jouhdr = None

    t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, t_gl_jouhdr_data, gl_jouhdr, htparam
        nonlocal sorttype


        nonlocal t_gl_jouhdr
        nonlocal t_gl_jouhdr_data

        return {"from_date": from_date, "to_date": to_date, "t-gl-jouhdr": t_gl_jouhdr_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    from_date = htparam.fdate + timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    to_date = get_current_date()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.activeflag == sorttype) & (Gl_jouhdr.batch == False) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
        t_gl_jouhdr = T_gl_jouhdr()
        t_gl_jouhdr_data.append(t_gl_jouhdr)

        buffer_copy(gl_jouhdr, t_gl_jouhdr)

    return generate_output()