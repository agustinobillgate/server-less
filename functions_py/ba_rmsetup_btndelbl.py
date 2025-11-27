#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rset

def ba_rmsetup_btndelbl(rset_bezeich:string):
    bk_rset = None

    db_session = local_storage.db_session
    rset_bezeich = rset_bezeich.strip()

    def generate_output():
        nonlocal bk_rset
        nonlocal rset_bezeich

        return {}


    # bk_rset = get_cache (Bk_rset, {"bezeichnung": [(eq, rset_bezeich)]})
    bk_rset = db_session.query(Bk_rset).filter(
             (Bk_rset.bezeichnung == rset_bezeich)).with_for_update().first()

    if bk_rset:
        pass
        db_session.delete(bk_rset)

    return generate_output()