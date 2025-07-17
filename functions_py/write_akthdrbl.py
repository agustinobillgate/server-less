#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akthdr

t_akthdr1_data, T_akthdr1 = create_model_like(Akthdr)

def write_akthdrbl(case_type:int, t_akthdr1_data:[T_akthdr1]):
    success_flag = False
    akthdr = None

    T_akthdr1 = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, akthdr
        nonlocal case_type
        nonlocal t_akthdr1
        print("Output:", success_flag)
        return {"success_flag": success_flag}

    t_akthdr1 = query(t_akthdr1_data, first=True)

    if not t_akthdr1:

        return generate_output()

    if case_type == 1:
        akthdr = Akthdr()
        db_session.add(akthdr)

        buffer_copy(t_akthdr1, akthdr)
        success_flag = True
        pass
    elif case_type == 2:

        akthdr = get_cache (Akthdr, {"aktnr": [(eq, t_akthdr1.aktnr)]})

        if akthdr:
            buffer_copy(t_akthdr1, akthdr)
            success_flag = True
        pass

    return generate_output()