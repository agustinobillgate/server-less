from functions.additional_functions import *
import decimal
from models import Queasy

def write_queasy1bl(case_type:int, t_queasy:[T_queasy]):
    success_flag = False
    queasy = None

    t_queasy = buf_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})

    Buf_queasy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal buf_queasy


        nonlocal t_queasy, buf_queasy
        nonlocal t_queasy_list
        return {"success_flag": success_flag}

    t_queasy = query(t_queasy_list, first=True)

    if not t_queasy:

        return generate_output()

    if case_type == 1:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == t_Queasy.rec_id)).first()

        if queasy:
            queasy.deci1 = t_queasy.deci1
            queasy.deci2 = t_queasy.deci2

            success_flag = True


    elif case_type == 2:

        t_queasy = query(t_queasy_list, first=True)
        while None != t_queasy:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == t_Queasy.key) &  (Queasy.number1 == t_Queasy.number1) &  (Queasy.number2 == t_Queasy.number2) &  (Queasy.char1 == t_Queasy.char1) &  ((Queasy.deci1 != t_Queasy.deci1) |  (Queasy.deci2 != t_Queasy.deci2))).first()

            if queasy:

                queasy = db_session.query(Queasy).first()
                queasy.deci1 = t_queasy.deci1
                queasy.deci2 = t_queasy.deci2

                queasy = db_session.query(Queasy).first()

                success_flag = True

            t_queasy = query(t_queasy_list, next=True)

    return generate_output()