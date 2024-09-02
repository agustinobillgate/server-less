from functions.additional_functions import *
import decimal
from models import Nightaudit

def reprint_nabl():
    b1_list_list = []
    nightaudit = None

    b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"reihenfolge":int, "hogarest":int, "bezeichnun":str, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, nightaudit


        nonlocal b1_list
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    for nightaudit in db_session.query(Nightaudit).filter(
            (selektion)).all():
        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.reihenfolge = nightaudit.reihenfolge
        b1_list.hogarest = nightaudit.hogarest
        b1_list.bezeichnun = nightaudit.bezeichnung
        b1_list.rec_id = nightaudit._recid

    return generate_output()