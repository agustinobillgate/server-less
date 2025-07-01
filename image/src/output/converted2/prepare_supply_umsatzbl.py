#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_liefumsatz

def prepare_supply_umsatzbl(lief_nr:int):
    umsatz_list_list = []
    l_liefumsatz = None

    umsatz_list = None

    umsatz_list_list, Umsatz_list = create_model("Umsatz_list", {"lief_nr":int, "datum":date, "gesamtumsatz":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal umsatz_list_list, l_liefumsatz
        nonlocal lief_nr


        nonlocal umsatz_list
        nonlocal umsatz_list_list

        return {"umsatz-list": umsatz_list_list}

    for l_liefumsatz in db_session.query(L_liefumsatz).filter(
             (L_liefumsatz.lief_nr == lief_nr)).order_by(L_liefumsatz.datum).all():
        umsatz_list = Umsatz_list()
        umsatz_list_list.append(umsatz_list)

        buffer_copy(l_liefumsatz, umsatz_list)

    return generate_output()