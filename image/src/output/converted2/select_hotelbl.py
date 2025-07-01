#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_code

def select_hotelbl():

    prepare_cache ([Akt_code])

    b1_list_list = []
    akt_code = None

    b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"aktionscode":int, "bezeich":string, "bemerkung":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, akt_code


        nonlocal b1_list
        nonlocal b1_list_list

        return {"b1-list": b1_list_list}

    for akt_code in db_session.query(Akt_code).filter(
             (Akt_code.aktiongrup == 4)).order_by(Akt_code.aktionscode).all():
        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.aktionscode = akt_code.aktionscode
        b1_list.bezeich = akt_code.bezeich
        b1_list.bemerkung = akt_code.bemerkung

    return generate_output()