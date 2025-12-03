#using conversion tools version: 1.0.0.119

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

        queasy = db_session.query(Queasy).filter((Queasy.key == 340) & (Queasy.char1 == lscheinnr) & (Queasy.number1 == artnr) & (Queasy.deci1 == einzelpreis)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 340
            queasy.char1 = lscheinnr
            queasy.number1 = artnr
            queasy.char2 = remark
            queasy.deci1 =  to_decimal(einzelpreis)
        else:
            db_session.refresh(queasy, with_for_update=True)
            queasy.char2 = remark
            db_session.flush()

    return generate_output()