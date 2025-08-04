#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 4/8/2025
# gitlab: 
# 
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Gl_jouhdr

def gl_batchjou_btn_gltransbl(rec_id:int):

    prepare_cache ([Gl_jouhdr])

    gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr
        nonlocal rec_id

        return {}


    gl_jouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, rec_id)]})
    # Bala
    if gl_jouhdr is None:
        return generate_output()
    
    gl_jouhdr.batch = False
    pass

    return generate_output()