#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rset

def ba_rmsetup_btndelbl(rset_bezeich:string):
    bk_rset = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_rset
        nonlocal rset_bezeich

        return {}


    bk_rset = get_cache (Bk_rset, {"bezeichnung": [(eq, rset_bezeich)]})

    if bk_rset:
        pass
        db_session.delete(bk_rset)

    return generate_output()