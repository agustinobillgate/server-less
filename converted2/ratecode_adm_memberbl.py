#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Guest_pr

def ratecode_adm_memberbl(prcode:string):

    prepare_cache ([Guest])

    tb11_data = []
    guest = guest_pr = None

    tb11 = None

    tb11_data, Tb11 = create_model("Tb11", {"gastnr":int, "name":string, "code":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tb11_data, guest, guest_pr
        nonlocal prcode


        nonlocal tb11
        nonlocal tb11_data

        return {"tb11": tb11_data}

    guest_pr_obj_list = {}
    for guest_pr, guest in db_session.query(Guest_pr, Guest).join(Guest,(Guest.gastnr == Guest_pr.gastnr) & (Guest.karteityp <= 2)).filter(
             (Guest_pr.code == (prcode).lower())).order_by(Guest.name).all():
        if guest_pr_obj_list.get(guest_pr._recid):
            continue
        else:
            guest_pr_obj_list[guest_pr._recid] = True


        tb11 = Tb11()
        tb11_data.append(tb11)

        tb11.gastnr = guest.gastnr
        tb11.name = guest.name
        tb11.code = prcode

    return generate_output()