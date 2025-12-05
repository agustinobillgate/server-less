#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import B_storno
from sqlalchemy.orm.attributes import flag_modified

def sales_activity_list_btnchgbl(resnr:int, str:string, outnr:int):

    prepare_cache ([B_storno])

    b_storno = None

    db_session = local_storage.db_session
    str = str.strip()

    def generate_output():
        nonlocal b_storno
        nonlocal resnr, str, outnr

        return {}


    # b_storno = get_cache (B_storno, {"bankettnr": [(eq, resnr)]})
    b_storno = db_session.query(B_storno).filter(B_storno.bankettnr == resnr).with_for_update().first()
    pass
    b_storno.grund[outnr - 1] = str
    flag_modified(b_storno, "grund")
    

    return generate_output()