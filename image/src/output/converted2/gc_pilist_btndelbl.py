from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gc_pi

def gc_pilist_btndelbl(docu_nr:str, user_init:str):
    gc_pi = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_pi
        nonlocal docu_nr, user_init


        return {}


    gc_pi = db_session.query(Gc_pi).filter(
                 (func.lower(Gc_pi.docu_nr) == (docu_nr).lower())).first()
    gc_pi.pi_status = 9
    gc_pi.canceldate = get_current_date()
    gc_pi.cancelid = user_init
    gc_pi.cancelzeit = get_current_time_in_seconds()


    return generate_output()