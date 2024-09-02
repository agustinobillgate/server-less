from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_order, L_orderhdr

def mk_po_check_lief_nrbl(docu_nr:str, lief_nr:int):
    l_order = l_orderhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order, l_orderhdr


        return {}


    for l_order in db_session.query(L_order).filter(
            (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower())).all():
        l_order.lief_nr = lief_nr

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()

    if l_orderhdr:
        l_orderhdr.lief_nr = lief_nr

    return generate_output()