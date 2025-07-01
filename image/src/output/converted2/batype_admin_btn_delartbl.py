#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Ba_typ

def batype_admin_btn_delartbl(rec_id:int):
    ba_typ = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ba_typ
        nonlocal rec_id

        return {}


    ba_typ = get_cache (Ba_typ, {"_recid": [(eq, rec_id)]})

    if ba_typ:
        db_session.delete(ba_typ)

    return generate_output()