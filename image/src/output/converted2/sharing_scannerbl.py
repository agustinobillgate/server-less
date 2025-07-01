#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def sharing_scannerbl(usersession:string, command_string:string, gastnr:int, scanner_number:int):

    prepare_cache ([Queasy])

    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal usersession, command_string, gastnr, scanner_number

        return {}


    queasy = get_cache (Queasy, {"key": [(eq, 284)],"char1": [(eq, usersession)],"number2": [(eq, scanner_number)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 284
        queasy.char1 = usersession
        queasy.char2 = command_string
        queasy.logi1 = False
        queasy.number1 = gastnr
        queasy.number2 = scanner_number


        pass
    else:
        pass
        queasy.char2 = command_string
        queasy.logi1 = False


        pass
        pass

    return generate_output()