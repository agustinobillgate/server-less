#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 28-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_giro

def delete_gc_girobl(case_type:int, int1:int):
    successflag = False
    gc_giro = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, gc_giro
        nonlocal case_type, int1

        return {"successflag": successflag}


    if case_type == 1:

        # gc_giro = get_cache (Gc_giro, {"_recid": [(eq, int1)]})
        gc_giro = db_session.query(Gc_giro).filter(
                 (Gc_giro._recid == int1)).with_for_update().first()

        if gc_giro:
            db_session.delete(gc_giro)
            successflag = True

    return generate_output()
