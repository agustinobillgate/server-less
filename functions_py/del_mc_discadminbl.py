#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Mc_disc

def del_mc_discadminbl(curr_nr:int, rec_id:int):
    hoteldpt = mc_disc = None

    hbuff = None

    Hbuff = create_buffer("Hbuff",Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hoteldpt, mc_disc
        nonlocal curr_nr, rec_id
        nonlocal hbuff


        nonlocal hbuff

        return {}


    # mc_disc = get_cache (Mc_disc, {"nr": [(eq, curr_nr)],"_recid": [(eq, rec_id)]})
    mc_disc = db_session.query(Mc_disc).filter(
             (Mc_disc.nr == curr_nr) &
             (Mc_disc._recid == rec_id)).with_for_update().first()

    if mc_disc:
        pass
        db_session.delete(mc_disc)
        pass

    return generate_output()