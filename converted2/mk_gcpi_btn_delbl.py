#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_pibline

def mk_gcpi_btn_delbl(s_recid:int):
    gc_pibline = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_pibline
        nonlocal s_recid

        return {}


    gc_pibline = get_cache (Gc_pibline, {"_recid": [(eq, s_recid)]})
    db_session.delete(gc_pibline)

    return generate_output()