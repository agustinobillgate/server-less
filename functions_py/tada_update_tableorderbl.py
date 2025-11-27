#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def tada_update_tableorderbl(orderid:string, tischnr:int):

    prepare_cache ([Queasy])

    param1:string = ""
    param3:string = ""
    param4:string = ""
    param5:string = ""
    param6:string = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal param1, param3, param4, param5, param6, queasy
        nonlocal orderid, tischnr

        return {}


    # queasy = get_cache (Queasy, {"key": [(eq, 271)],"betriebsnr": [(eq, 1)],"number2": [(eq, to_int(orderid))]})
    queasy = db_session.query(Queasy).filter(
        Queasy.key == 271,
        Queasy.betriebsnr == 1,
        Queasy.number2 == to_int(orderid)
    ).with_for_update().first()

    if queasy:
        pass
        param1 = entry(0, queasy.char2, "|")
        param3 = entry(2, queasy.char2, "|")
        param4 = entry(3, queasy.char2, "|")
        param5 = entry(4, queasy.char2, "|")
        param6 = entry(5, queasy.char2, "|")
        queasy.char2 = param1 + "|" + to_string(tischnr) + "|" + param3 + "|" + param4 + "|" + param5 + "|" + param6
        pass
        pass

    return generate_output()