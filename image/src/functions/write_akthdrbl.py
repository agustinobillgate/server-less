from functions.additional_functions import *
import decimal
from models import Akthdr

def write_akthdrbl(case_type:int, t_akthdr:[T_akthdr]):
    success_flag = False
    akthdr = None

    t_akthdr = None

    t_akthdr_list, T_akthdr = create_model_like(Akthdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, akthdr


        nonlocal t_akthdr
        nonlocal t_akthdr_list
        return {"success_flag": success_flag}

    t_akthdr = query(t_akthdr_list, first=True)

    if not t_akthdr:

        return generate_output()

    if case_type == 1:
        akthdr = Akthdr()
        db_session.add(akthdr)

        buffer_copy(t_akthdr, akthdr)
        success_flag = True

        akthdr = db_session.query(Akthdr).first()
    elif case_type == 2:

        akthdr = db_session.query(Akthdr).filter(
                (Akthdr.aktnr == t_Akthdr.aktnr)).first()

        if akthdr:
            buffer_copy(t_akthdr, akthdr)
            success_flag = True

        akthdr = db_session.query(Akthdr).first()

    return generate_output()