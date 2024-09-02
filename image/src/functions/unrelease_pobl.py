from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_orderhdr

def unrelease_pobl(docu_nr:str):
    flag = 0
    l_orderhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_orderhdr


        return {"flag": flag}


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()

    if not l_orderhdr:
        flag = 1

        return generate_output()
    else:

        if l_orderhdr.gedruckt == None:
            flag = 2

            return generate_output()
        else:
            flag = 3

            return generate_output()