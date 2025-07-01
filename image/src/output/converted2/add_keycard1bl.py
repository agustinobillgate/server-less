#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def add_keycard1bl(resno:int, reslinno:int):

    prepare_cache ([Res_line])

    card_type = ""
    res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal card_type, res_line
        nonlocal resno, reslinno

        return {"card_type": card_type}


    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})
    pass
    res_line.betrieb_gast = res_line.betrieb_gast + 1
    pass
    card_type = "cardtype=2"

    return generate_output()