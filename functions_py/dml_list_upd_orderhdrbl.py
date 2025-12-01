#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Andika 04/08/2025
# gitlab: -
# Rd, 01/12/2025, with_for_update added
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr
from sqlalchemy.orm import flag_modified

def dml_list_upd_orderhdrbl(case_type:int, rec_id:int, dept:int, comments_screen_value:string, datum:date):
    l_orderhdr = None

    db_session = local_storage.db_session
    comments_screen_value = comments_screen_value.strip()

    def generate_output():
        nonlocal l_orderhdr
        nonlocal case_type, rec_id, dept, comments_screen_value, datum

        return {}


    # l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})
    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr._recid == rec_id)).with_for_update().first()
    
    if l_orderhdr:
        if case_type == 1:
            pass
            l_orderhdr.angebot_lief[0] = dept
            pass

        elif case_type == 2:
            pass
            l_orderhdr.lief_fax[2] = comments_screen_value
            pass

        elif case_type == 3:
            pass
            l_orderhdr.lieferdatum = datum
            pass

        elif case_type == 4:
            pass
            db_session.delete(l_orderhdr)
        flag_modified(l_orderhdr, "angebot_lief")
        flag_modified(l_orderhdr, "lief_fax")
        return generate_output()