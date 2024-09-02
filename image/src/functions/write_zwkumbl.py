from functions.additional_functions import *
import decimal
from models import Zwkum

def write_zwkumbl(case_type:int, t_zwkum:[T_zwkum]):
    success_flag = False
    zwkum = None

    t_zwkum = None

    t_zwkum_list, T_zwkum = create_model_like(Zwkum)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, zwkum


        nonlocal t_zwkum
        nonlocal t_zwkum_list
        return {"success_flag": success_flag}

    t_zwkum = query(t_zwkum_list, first=True)

    if not t_zwkum:

        return generate_output()

    if case_type == 1:
        zwkum = Zwkum()
        db_session.add(zwkum)

        buffer_copy(t_zwkum, zwkum)

        success_flag = True
    elif case_type == 2:

        zwkum = db_session.query(Zwkum).filter(
                (Zwkum.zknr == t_Zwkum.zknr) &  (Zwkum.departement == t_Zwkum.departement)).first()

        if zwkum:
            buffer_copy(t_zwkum, zwkum)

            success_flag = True
    elif case_type == 3:

        zwkum = db_session.query(Zwkum).filter(
                (Zwkum.zknr == t_Zwkum.zknr) &  (Zwkum.departement == t_Zwkum.departement)).first()

        if zwkum:
            db_session.delete(zwkum)

            success_flag = True

    return generate_output()