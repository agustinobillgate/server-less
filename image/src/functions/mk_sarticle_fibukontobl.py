from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def mk_sarticle_fibukontobl(pvilanguage:int, fibukonto:str):
    str_msg = ""
    lvcarea:str = "mk_sarticle"
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, lvcarea, gl_acct


        return {"str_msg": str_msg}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.(fibukonto).lower()) == (fibukonto).lower())).first()

    if not gl_acct and to_int(fibukonto) != 0:
        str_msg = translateExtended ("No such account number", lvcarea, "")

    return generate_output()