from functions.additional_functions import *
import decimal
from models import Nightaudit

def write_nightauditbl(case_type:int, t_nightaudit:[T_nightaudit]):
    success_flag = False
    nightaudit = None

    t_nightaudit = None

    t_nightaudit_list, T_nightaudit = create_model_like(Nightaudit, {"n_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, nightaudit


        nonlocal t_nightaudit
        nonlocal t_nightaudit_list
        return {"success_flag": success_flag}

    t_nightaudit = query(t_nightaudit_list, first=True)

    if not t_nightaudit:

        return generate_output()

    if case_type == 1:
        nightaudit = Nightaudit()
        db_session.add(nightaudit)

        buffer_copy(t_nightaudit, nightaudit)

        success_flag = True
    elif case_type == 2:

        nightaudit = db_session.query(Nightaudit).filter(
                (Nightaudit._recid == t_Nightaudit.n_recid)).first()

        if nightaudit:
            buffer_copy(t_nightaudit, nightaudit)

            success_flag = True

    return generate_output()