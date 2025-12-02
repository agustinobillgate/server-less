#using conversion tools version: 1.0.0.117
#--------------------------------------------------------------------
# Rd 4/8/2025
# gitlab: 
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#--------------------------------------------------------------------
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

    # Rd, 24/11/2025, get gl_jouhdr dengan for update
    # gl_jouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, rec_id)]})
    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr._recid == rec_id)).with_for_update().first()
    # Bala
    if gl_jouhdr is None:
        return generate_output()
    
    gl_jouhdr.batch = False
    pass

    return generate_output()