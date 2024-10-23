from functions.additional_functions import *
import decimal
from models import Queasy

htlname_list, Htlname = create_model("Htlname")

def grphtl_admin_btn_exitbl(htlname_list:[Htlname], case_type:int, rec_id:int):
    rec_id1 = 0
    queasy = None

    htlname = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_id1, queasy
        nonlocal case_type, rec_id


        nonlocal htlname
        nonlocal htlname_list
        return {"rec_id1": rec_id1}

    def fill_new_queasy():

        nonlocal rec_id1, queasy
        nonlocal case_type, rec_id


        nonlocal htlname
        nonlocal htlname_list


        queasy.key = 136
        buffer_copy(htlname, queasy,except_fields=["KEY"])


    htlname = query(htlname_list, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()
        rec_id1 = queasy._recid

    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                 (Queasy._recid == rec_id)).first()
        buffer_copy(htlname, queasy)

    return generate_output()