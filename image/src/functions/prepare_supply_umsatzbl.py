from functions.additional_functions import *
import decimal
from models import L_liefumsatz

def prepare_supply_umsatzbl(lief_nr:int):
    umsatz_list_list = []
    l_liefumsatz = None

    umsatz_list = None

    umsatz_list_list, Umsatz_list = create_model("Umsatz_list", {"lief_nr":int, "datum":date, "gesamtumsatz":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal umsatz_list_list, l_liefumsatz


        nonlocal umsatz_list
        nonlocal umsatz_list_list
        return {"umsatz-list": umsatz_list_list}

    for l_liefumsatz in db_session.query(L_liefumsatz).filter(
            (L_liefumsatz.lief_nr == lief_nr)).all():
        umsatz_list = Umsatz_list()
        umsatz_list_list.append(umsatz_list)

        buffer_copy(l_liefumsatz, umsatz_list)

    return generate_output()