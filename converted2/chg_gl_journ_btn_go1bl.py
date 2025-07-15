#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_jouhdr

def chg_gl_journ_btn_go1bl(t_refno:string, t_bezeich:string, t_recid:int):

    prepare_cache ([Gl_jouhdr])

    gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr
        nonlocal t_refno, t_bezeich, t_recid

        return {}


    gl_jouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, t_recid)]})

    if t_refno != "":
        pass
        gl_jouhdr.refno = t_refno


        pass

    if t_bezeich != "":
        pass
        gl_jouhdr.bezeich = t_bezeich


        pass

    return generate_output()