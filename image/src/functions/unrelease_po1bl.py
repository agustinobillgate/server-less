from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_orderhdr

def unrelease_po1bl(docu_nr:str):
    l_orderhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr


        return {}


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()

    l_orderhdr = db_session.query(L_orderhdr).first()
    l_orderhdr.gedruckt = None

    l_orderhdr = db_session.query(L_orderhdr).first()

    return generate_output()