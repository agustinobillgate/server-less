#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 28/7/2025
#
#-----------------------------------------
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


    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})\
    
    # Rd, 28/7/2025
    # if availbale
    if gc_pi:
        gc_pi.pi_status = 9
        gc_pi.canceldate = get_current_date()
        gc_pi.cancelid = user_init
        gc_pi.cancelzeit = get_current_time_in_seconds()


    pass

    return generate_output()