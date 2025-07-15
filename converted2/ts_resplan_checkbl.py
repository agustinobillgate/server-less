#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, H_bill

def ts_resplan_checkbl(v_key:int, s_recid:int, curr_dept:int, table_no:int):

    prepare_cache ([H_bill])

    msg_str = ""
    queasy = h_bill = None

    queasy251 = None

    Queasy251 = create_buffer("Queasy251",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, queasy, h_bill
        nonlocal v_key, s_recid, curr_dept, table_no
        nonlocal queasy251


        nonlocal queasy251

        return {"msg_str": msg_str}


    if v_key == 1:

        h_bill = get_cache (H_bill, {"flag": [(eq, 0)],"tischnr": [(eq, table_no)],"departement": [(eq, curr_dept)]})

        if h_bill:

            if h_bill.rechnr != 0:

                queasy251 = db_session.query(Queasy251).filter(
                         (Queasy251.key == 251) & (Queasy251.number1 == to_int(h_bill._recid)) & (Queasy251.number2 == s_recid)).first()

                if queasy251:
                    msg_str = "Bill already open for this table."

                    return generate_output()

    return generate_output()