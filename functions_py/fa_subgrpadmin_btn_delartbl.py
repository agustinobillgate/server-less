#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 4/8/2025
# if available
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Fa_grup, Fa_artikel

def fa_subgrpadmin_btn_delartbl(rec_id:int):
    do_it = True
    fa_grup = fa_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, fa_grup, fa_artikel
        nonlocal rec_id

        return {"do_it": do_it}


    fa_grup = get_cache (Fa_grup, {"_recid": [(eq, rec_id)]})
    # Rd 4/8/2025
    # if available
    if fa_grup is None:
        return generate_output()
    
    fa_artikel = get_cache (Fa_artikel, {"gnr": [(eq, fa_grup.gnr)]})

    if fa_artikel:
        do_it = False
    else:
        pass
        db_session.delete(fa_grup)
        pass

    return generate_output()