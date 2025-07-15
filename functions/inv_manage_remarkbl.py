#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

payload_list_data, Payload_list = create_model("Payload_list", {"artnr":int, "lscheinnr":string, "remark":string, "einzelpreis":Decimal})

def inv_manage_remarkbl(payload_list_data:[Payload_list]):

    prepare_cache ([Queasy])

    valid_input:bool = False
    artnr:int = 0
    lscheinnr:string = ""
    remark:string = ""
    einzelpreis:Decimal = to_decimal("0.0")
    queasy = None

    payload_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal valid_input, artnr, lscheinnr, remark, einzelpreis, queasy


        nonlocal payload_list

        return {}

    payload_list = query(payload_list_data, first=True)

    if payload_list:
        artnr = payload_list.artnr
        lscheinnr = payload_list.lscheinnr
        remark = payload_list.remark
        einzelpreis =  to_decimal(payload_list.einzelpreis)

        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, lscheinnr)],"number1": [(eq, artnr)],"deci1": [(eq, einzelpreis)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 340
            queasy.char1 = lscheinnr
            queasy.number1 = artnr
            queasy.char2 = remark
            queasy.deci1 =  to_decimal(einzelpreis)


        else:
            pass
            queasy.char2 = remark


            pass

    return generate_output()