#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def inventory_vat_listbl(casetype:int, nr:int, bezeich:string, vatvalue:Decimal, fibukonto:string):
    successflag = False
    msg_str = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, msg_str, queasy
        nonlocal casetype, nr, bezeich, vatvalue, fibukonto

        return {"successflag": successflag, "msg_str": msg_str}


    if casetype == 1:

        queasy = get_cache (Queasy, {"key": [(eq, 303)],"number1": [(eq, nr)]})

        if queasy:
            successflag = False
            msg_str = "Tax value with No . " + to_string(nr) + " is already exist."

        elif not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 303
            queasy.number1 = nr
            queasy.char1 = bezeich
            queasy.deci1 =  to_decimal(vatvalue)
            queasy.char2 = fibukonto
            successflag = True

    elif casetype == 2:

        queasy = get_cache (Queasy, {"key": [(eq, 303)],"number1": [(eq, nr)]})

        if queasy:
            pass
            queasy.char1 = bezeich
            queasy.deci1 =  to_decimal(vatvalue)
            queasy.char2 = fibukonto
            successflag = True


            pass
            pass

    elif casetype == 3:

        queasy = get_cache (Queasy, {"key": [(eq, 303)],"number1": [(eq, nr)]})

        if queasy:
            pass
            db_session.delete(queasy)
            pass

    return generate_output()