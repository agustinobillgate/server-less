from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def fa_artlist_fibukontobl(fibukonto:str):
    do_it = False
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, gl_acct


        return {"do_it": do_it}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.(fibukonto).lower()) == (fibukonto).lower())).first()

    if not gl_acct and to_int(fibukonto) != 0:
        do_it = True

    return generate_output()