#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def bookengine_admin_selectguestbl():

    prepare_cache ([Guest])

    tguest_list = []
    guest = None

    tguest = None

    tguest_list, Tguest = create_model("Tguest", {"gastnr":int, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tguest_list, guest


        nonlocal tguest
        nonlocal tguest_list

        return {"tguest": tguest_list}

    for guest in db_session.query(Guest).filter(
             (Guest.karteityp == 2)).order_by(Guest._recid).all():
        tguest = Tguest()
        tguest_list.append(tguest)

        tguest.gastnr = guest.gastnr
        tguest.name = guest.name

    return generate_output()