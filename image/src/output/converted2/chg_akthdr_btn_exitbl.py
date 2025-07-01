#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Akthdr

akthdr1_list, Akthdr1 = create_model_like(Akthdr)

def chg_akthdr_btn_exitbl(akthdr1_list:[Akthdr1]):
    akthdr = None

    akthdr1 = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal akthdr
        nonlocal akthdr1_list


        nonlocal akthdr1

        return {}

    akthdr1 = query(akthdr1_list, first=True)

    akthdr = get_cache (Akthdr, {"aktnr": [(eq, akthdr1.aktnr)]})
    buffer_copy(akthdr1, akthdr)
    pass

    return generate_output()