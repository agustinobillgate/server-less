#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def add_crmlicense():

    prepare_cache ([Htparam])

    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1459)]})

    if htparam.paramgruppe != 99:
        pass
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License FOR CRM Module"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 1073

    return generate_output()