#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

htlname_list, Htlname = create_model("Htlname")

def grphtl_admin_btn_exitbl(htlname_list:[Htlname], case_type:int, rec_id:int):

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


    htlname = query(htlname_list, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()
        pass
        rec_id1 = queasy._recid

    elif case_type == 2:

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
        pass
        buffer_copy(htlname, queasy)

    return generate_output()