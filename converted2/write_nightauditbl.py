#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nightaudit

t_nightaudit_data, T_nightaudit = create_model_like(Nightaudit, {"n_recid":int})

def write_nightauditbl(case_type:int, t_nightaudit_data:[T_nightaudit]):
    success_flag = False
    nightaudit = None

    t_nightaudit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, nightaudit
        nonlocal case_type


        nonlocal t_nightaudit

        return {"success_flag": success_flag}

    t_nightaudit = query(t_nightaudit_data, first=True)

    if not t_nightaudit:

        return generate_output()

    if case_type == 1:
        nightaudit = Nightaudit()
        db_session.add(nightaudit)

        buffer_copy(t_nightaudit, nightaudit)
        pass
        success_flag = True
    elif case_type == 2:

        nightaudit = get_cache (Nightaudit, {"_recid": [(eq, t_nightaudit.n_recid)]})

        if nightaudit:
            buffer_copy(t_nightaudit, nightaudit)
            pass
            success_flag = True

    return generate_output()