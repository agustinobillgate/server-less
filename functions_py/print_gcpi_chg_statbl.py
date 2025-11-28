#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 28-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_pi

def print_gcpi_chg_statbl(docu_nr:string, flag:int):

    prepare_cache ([Gc_pi])

    gc_pi = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_pi
        nonlocal docu_nr, flag

        return {}


    # gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})
    gc_pi = db_session.query(Gc_pi).filter(
             (Gc_pi.docu_nr == docu_nr)).with_for_update().first()

    if gc_pi:
        # pass

        if flag == 1:
            gc_pi.printed1 = True

        elif flag == 2:
            gc_pi.printed1a = True

        db_session.refresh(gc_pi,with_for_update=True)
        # pass
        # pass

    return generate_output()
