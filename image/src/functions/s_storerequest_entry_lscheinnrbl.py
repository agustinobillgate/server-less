from functions.additional_functions import *
import decimal
from models import L_ophdr

def s_storerequest_entry_lscheinnrbl(recid_l_ophdr:int, lscheinnr:str):
    l_ophdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr


        return {}


    l_ophdr = db_session.query(L_ophdr).filter(
            (L_ophdr._recid == recid_l_ophdr)).first()

    l_ophdr = db_session.query(L_ophdr).first()
    l_ophdr.docu_nr = lscheinnr
    l_ophdr.lscheinnr = lscheinnr

    l_ophdr = db_session.query(L_ophdr).first()

    return generate_output()