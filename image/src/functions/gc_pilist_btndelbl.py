from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gc_pi

def gc_pilist_btndelbl(docu_nr:str, user_init:str):
    gc_pi = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_pi


        return {}


    gc_pi = db_session.query(Gc_pi).filter(
                (func.lower(Gc_pi.(docu_nr).lower()) == (docu_nr).lower())).first()
    gc_pi.pi_status = 9
    gc_pi.cancelDate = get_current_date()
    gc_pi.cancelID = user_init
    gc_pi.cancelZeit = get_current_time_in_seconds()

    gc_pi = db_session.query(Gc_pi).first()


    return generate_output()