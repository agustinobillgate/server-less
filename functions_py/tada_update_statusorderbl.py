#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def tada_update_statusorderbl(orderid:string, changestatusto:string):

    prepare_cache ([Queasy])

    param1:string = ""
    param2:string = ""
    param3:string = ""
    queasy = None

    db_session = local_storage.db_session
    orderid = orderid.strip()
    changestatusto = changestatusto.strip()

    def generate_output():
        nonlocal param1, param2, param3, queasy
        nonlocal orderid, changestatusto

        return {}


    # queasy = get_cache (Queasy, {"key": [(eq, 271)],"betriebsnr": [(eq, 1)],"number2": [(eq, to_int(orderid))]})
    queasy = db_session.query(Queasy).filter(
        Queasy.key == 271,
        Queasy.betriebsnr == 1,
        Queasy.number2 == to_int(orderid)
    ).with_for_update().first()

    if queasy:
        pass
        param1 = entry(0, queasy.char1, "|")
        param2 = entry(1, queasy.char1, "|")
        param3 = entry(2, queasy.char1, "|")
        queasy.char1 = param1 + "|" + changestatusto + "|" + param3
        pass
        pass

    return generate_output()