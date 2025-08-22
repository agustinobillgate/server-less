#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 4/8/2025
# if available
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Mc_disc, Mc_types

def mc_typeadmin_btn_delnamebl(nr:int, rec_id:int):
    mc_disc = mc_types = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mc_disc, mc_types
        nonlocal nr, rec_id

        return {}


    for mc_disc in db_session.query(Mc_disc).filter(
             (Mc_disc.nr == nr)).order_by(Mc_disc._recid).all():
        db_session.delete(mc_disc)

    mc_types = get_cache (Mc_types, {"_recid": [(eq, rec_id)]})
    # Rd 4/8/2025
    # if available
    if mc_types:
        db_session.delete(mc_types)

    return generate_output()