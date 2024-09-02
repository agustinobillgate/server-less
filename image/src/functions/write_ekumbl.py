from functions.additional_functions import *
import decimal
from models import Ekum

def write_ekumbl(case_type:int, t_ekum:[T_ekum]):
    success_flag = False
    ekum = None

    t_ekum = None

    t_ekum_list, T_ekum = create_model_like(Ekum)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, ekum


        nonlocal t_ekum
        nonlocal t_ekum_list
        return {"success_flag": success_flag}

    t_ekum = query(t_ekum_list, first=True)

    if not t_ekum:

        return generate_output()

    if case_type == 1:
        ekum = Ekum()
        db_session.add(ekum)

        buffer_copy(t_ekum, ekum)

        success_flag = True
    elif case_type == 2:

        ekum = db_session.query(Ekum).filter(
                (Ekum.eknr == t_Ekum.eknr)).first()

        if ekum:
            buffer_copy(t_ekum, ekum)

            success_flag = True

    return generate_output()