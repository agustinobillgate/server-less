#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 20/10/2025
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Nightaudit

def reprint_nabl():

    prepare_cache ([Nightaudit])

    b1_list_data = []
    nightaudit = None

    b1_list = None

    b1_list_data, B1_list = create_model("B1_list", {"reihenfolge":int, "hogarest":int, "bezeichnun":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_data, nightaudit


        nonlocal b1_list
        nonlocal b1_list_data

        return {"b1-list": b1_list_data}

    for nightaudit in db_session.query(Nightaudit).filter(
             (Nightaudit.selektion)).order_by((1 - Nightaudit.hogarest), Nightaudit.reihenfolge).all():
        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.reihenfolge = nightaudit.reihenfolge
        b1_list.hogarest = nightaudit.hogarest
        b1_list.bezeichnun = nightaudit.bezeichnung
        b1_list.rec_id = nightaudit._recid

    return generate_output()