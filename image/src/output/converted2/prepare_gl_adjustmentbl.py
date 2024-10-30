from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jouhdr, Htparam, Gl_journal, Gl_acct

def prepare_gl_adjustmentbl(sorttype:int):
    from_date = None
    param_983 = False
    t_gl_jouhdr_list = []
    b2_list_list = []
    to_date:date = None
    gl_jouhdr = htparam = gl_journal = gl_acct = None

    t_gl_jouhdr = b2_list = None

    t_gl_jouhdr_list, T_gl_jouhdr = create_model_like(Gl_jouhdr)
    b2_list_list, B2_list = create_model("B2_list", {"jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, param_983, t_gl_jouhdr_list, b2_list_list, to_date, gl_jouhdr, htparam, gl_journal, gl_acct
        nonlocal sorttype


        nonlocal t_gl_jouhdr, b2_list
        nonlocal t_gl_jouhdr_list, b2_list_list

        return {"from_date": from_date, "param_983": param_983, "t-gl-jouhdr": t_gl_jouhdr_list, "b2-list": b2_list_list}

    def display_it0():

        nonlocal from_date, param_983, t_gl_jouhdr_list, b2_list_list, to_date, gl_jouhdr, htparam, gl_journal, gl_acct
        nonlocal sorttype


        nonlocal t_gl_jouhdr, b2_list
        nonlocal t_gl_jouhdr_list, b2_list_list

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.activeflag == sorttype) & (Gl_jouhdr.batch == False) & (Gl_jouhdr.datum == to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_list.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)

            for gl_journal in db_session.query(Gl_journal).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal.sysdate, Gl_journal.zeit).all():

                gl_acct = db_session.query(Gl_acct).filter(
                         (Gl_acct.fibukonto == gl_journal.fibukonto)).first()
                b2_list = B2_list()
                b2_list_list.append(b2_list)

                buffer_copy(gl_journal, b2_list)
                b2_list.bezeich = gl_acct.bezeich

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 795)).first()
    from_date = htparam.fdate
    to_date = from_date
    display_it0()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 983)).first()
    param_983 = htparam.flogical

    return generate_output()