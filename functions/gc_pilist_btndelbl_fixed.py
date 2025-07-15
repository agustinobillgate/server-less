#using conversion tools version: 1.0.0.113

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_pi

def gc_pilist_btndelbl(docu_nr:string, user_init:string):

    prepare_cache ([Gc_pi])

    gc_pi = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_pi
        nonlocal docu_nr, user_init

        return {}


    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})

    if gc_pi is None:
        gc_pi = Gc_pi()
        gc_pi.docu_nr = docu_nr
        db_session.add(gc_pi)

    gc_pi.pi_status = 9
    gc_pi.canceldate = get_current_date()
    gc_pi.cancelid = user_init
    gc_pi.cancelzeit = get_current_time_in_seconds()


    pass

    return generate_output()
