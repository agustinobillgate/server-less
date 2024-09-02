from functions.additional_functions import *
import decimal
from models import Zimkateg

def write_zimkategbl(case_type:int, t_zimkateg:[T_zimkateg]):
    success_flag = False
    zimkateg = None

    t_zimkateg = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, zimkateg


        nonlocal t_zimkateg
        nonlocal t_zimkateg_list
        return {"success_flag": success_flag}

    t_zimkateg = query(t_zimkateg_list, first=True)

    if not t_zimkateg:

        return generate_output()

    if case_type == 1:
        zimkateg = Zimkateg()
        db_session.add(zimkateg)

        buffer_copy(t_zimkateg, zimkateg)

        success_flag = True


    elif case_type == 2:

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == t_Zimkateg.zikatnr)).first()

        if zimkateg:
            buffer_copy(t_zimkateg, zimkateg)

            success_flag = True

    return generate_output()