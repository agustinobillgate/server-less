from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Guest_pr

def ratecode_adm_memberbl(prcode:str):
    tb11_list = []
    guest = guest_pr = None

    tb11 = None

    tb11_list, Tb11 = create_model("Tb11", {"gastnr":int, "name":str, "code":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tb11_list, guest, guest_pr


        nonlocal tb11
        nonlocal tb11_list
        return {"tb11": tb11_list}

    guest_pr_obj_list = []
    for guest_pr, guest in db_session.query(Guest_pr, Guest).join(Guest,(Guest.gastnr == Guest_pr.gastnr) &  (Guest.karteityp <= 2)).filter(
            (func.lower(Guest_pr.code) == (prcode).lower())).all():
        if guest_pr._recid in guest_pr_obj_list:
            continue
        else:
            guest_pr_obj_list.append(guest_pr._recid)


        tb11 = Tb11()
        tb11_list.append(tb11)

        tb11.gastnr = guest.gastnr
        tb11.name = guest.name
        tb11.CODE = prcode

    return generate_output()