#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def gcf_ccard_btn_exitbl(gastnr:int, ausweis_nr2:string):

    prepare_cache ([Guest])

    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest
        nonlocal gastnr, ausweis_nr2

        return {}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
    guest.ausweis_nr2 = ausweis_nr2


    pass

    return generate_output()