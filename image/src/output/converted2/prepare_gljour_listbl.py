from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jouhdr, Htparam

def prepare_gljour_listbl(sorttype:int):
    from_date = None
    to_date = None
    t_gl_jouhdr_list = []
    gl_jouhdr = htparam = None

    t_gl_jouhdr = None

    t_gl_jouhdr_list, T_gl_jouhdr = create_model_like(Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, t_gl_jouhdr_list, gl_jouhdr, htparam
        nonlocal sorttype


        nonlocal t_gl_jouhdr
        nonlocal t_gl_jouhdr_list

        return {"from_date": from_date, "to_date": to_date, "t-gl-jouhdr": t_gl_jouhdr_list}

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 558)).first()
    from_date = htparam.fdate + timedelta(days=1)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 597)).first()
    to_date = get_current_date()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.activeflag == sorttype) & (Gl_jouhdr.batch == False) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
        t_gl_jouhdr = T_gl_jouhdr()
        t_gl_jouhdr_list.append(t_gl_jouhdr)

        buffer_copy(gl_jouhdr, t_gl_jouhdr)

    return generate_output()