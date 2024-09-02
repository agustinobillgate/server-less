from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gc_pi

def print_gcpi_chg_statbl(docu_nr:str, flag:int):
    gc_pi = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_pi


        return {}


    gc_pi = db_session.query(Gc_pi).filter(
            (func.lower(Gc_pi.(docu_nr).lower()) == (docu_nr).lower())).first()

    if flag == 1:
        gc_pi.printed1 = True

    elif flag == 2:
        gc_pi.printed1A = True

    gc_pi = db_session.query(Gc_pi).first()

    return generate_output()