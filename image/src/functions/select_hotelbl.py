from functions.additional_functions import *
import decimal
from models import Akt_code

def select_hotelbl():
    b1_list_list = []
    akt_code = None

    b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"aktionscode":int, "bezeich":str, "bemerkung":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, akt_code


        nonlocal b1_list
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    for akt_code in db_session.query(Akt_code).filter(
            (Akt_code.aktiongrup == 4)).all():
        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.aktionscode = akt_code.aktionscode
        b1_list.bezeich = akt_code.bezeich
        b1_list.bemerkung = akt_code.bemerkung

    return generate_output()