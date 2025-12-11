#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

htlname_data, Htlname = create_model("Htlname", {"key":int, "number2":int, "number3":int, "date1":date, "date2":date, "date3":date, "deci1":Decimal, "deci2":Decimal, "deci3":Decimal, "logi3":bool, "betriebsnr":int, "number1": int, "char3":string, "char2":string, "char1":string, "logi1":bool, "logi2":bool})

def grphtl_admin_btn_exitbl(htlname_data:[Htlname], case_type:int, rec_id:int):

    prepare_cache ([Queasy])

    rec_id1 = 0
    queasy = None

    htlname = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_id1, queasy
        nonlocal case_type, rec_id


        nonlocal htlname

        return {"rec_id1": rec_id1}

    def fill_new_queasy():

        nonlocal rec_id1, queasy
        nonlocal case_type, rec_id


        nonlocal htlname


        queasy.key = 136
        buffer_copy(htlname, queasy,except_fields=["KEY"])


    htlname = query(htlname_data, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()
        pass
        rec_id1 = queasy._recid

    elif case_type == 2:

        # queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
        queasy = db_session.query(Queasy).filter(Queasy._recid == rec_id).with_for_update().first()
        buffer_copy(htlname, queasy)

    return generate_output()