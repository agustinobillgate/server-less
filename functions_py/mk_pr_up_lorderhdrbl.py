#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr
from sqlalchemy.orm.attributes import flag_modified

def mk_pr_up_lorderhdrbl(case_type:int, rec_id:int, dept:int, datum:date):

    prepare_cache ([L_orderhdr])

    l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr
        nonlocal case_type, rec_id, dept, datum

        return {}


    # l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})
    l_orderhdr = db_session.query(L_orderhdr).filter(
                 (L_orderhdr._recid == rec_id)).with_for_update().first()

    if case_type == 1:
        pass
        l_orderhdr.angebot_lief[0] = dept

    elif case_type == 2:
        pass
        l_orderhdr.lieferdatum = datum
    pass
    flag_modified(l_orderhdr, "angebot_lief")

    return generate_output()