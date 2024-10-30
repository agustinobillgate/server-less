from functions.additional_functions import *
import decimal
from models import Gl_jouhdr

def chg_gl_journ_btn_go1bl(t_refno:str, t_bezeich:str, t_recid:int):
    gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr
        nonlocal t_refno, t_bezeich, t_recid

        return {}


    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr._recid == t_recid)).first()

    if t_refno != "":
        gl_jouhdr.refno = t_refno

    if t_bezeich != "":
        gl_jouhdr.bezeich = t_bezeich

    return generate_output()