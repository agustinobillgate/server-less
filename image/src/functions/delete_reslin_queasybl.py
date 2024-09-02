from functions.additional_functions import *
import decimal
from models import Reslin_queasy

def delete_reslin_queasybl(t_reslin_queasy:[T_reslin_queasy]):
    success_flag = False
    reslin_queasy = None

    t_reslin_queasy = None

    t_reslin_queasy_list, T_reslin_queasy = create_model_like(Reslin_queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, reslin_queasy


        nonlocal t_reslin_queasy
        nonlocal t_reslin_queasy_list
        return {"success_flag": success_flag}

    t_reslin_queasy = query(t_reslin_queasy_list, first=True)

    if t_reslin_queasy:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == t_Reslin_queasy.key) &  (Reslin_queasy.resnr == t_Reslin_queasy.resnr) &  (Reslin_queasy.reslinnr == t_Reslin_queasy.reslinnr) &  (Reslin_queasy.number1 == t_Reslin_queasy.number1) &  (Reslin_queasy.number2 == t_Reslin_queasy.number2) &  (Reslin_queasy.number3 == t_Reslin_queasy.number3) &  (Reslin_queasy.date1 == t_Reslin_queasy.date1) &  (Reslin_queasy.date2 == t_Reslin_queasy.date2) &  (Reslin_queasy.date3 == t_Reslin_queasy.date3) &  (Reslin_queasy.char1 == t_Reslin_queasy.char1) &  (Reslin_queasy.char2 == t_Reslin_queasy.char2) &  (Reslin_queasy.char3 == t_Reslin_queasy.char3) &  (Reslin_queasy.deci1 == t_Reslin_queasy.deci1) &  (Reslin_queasy.deci2 == t_Reslin_queasy.deci2) &  (Reslin_queasy.deci3 == t_Reslin_queasy.deci3) &  (Reslin_queasy.logi1 == t_Reslin_queasy.logi1) &  (Reslin_queasy.logi2 == t_Reslin_queasy.logi2) &  (Reslin_queasy.logi3 == t_Reslin_queasy.logi3)).first()

    if reslin_queasy:
        db_session.delete(reslin_queasy)

        success_flag = True

    return generate_output()