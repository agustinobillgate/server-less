#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_code

def mk_aktline_input_aktionbl(t_aktion:string):

    prepare_cache ([Akt_code])

    t_aktionscode = 0
    akt_code = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_aktionscode, akt_code
        nonlocal t_aktion

        return {"t_aktionscode": t_aktionscode}


    akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, 1)],"bezeich": [(eq, t_aktion)]})
    t_aktionscode = akt_code.aktionscode

    return generate_output()