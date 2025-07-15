#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_line

def akt_sales1_btn_del2bl(recid_aktline:int):
    akt_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal akt_line
        nonlocal recid_aktline

        return {}


    akt_line = get_cache (Akt_line, {"_recid": [(eq, recid_aktline)]})
    pass
    db_session.delete(akt_line)

    return generate_output()