from functions.additional_functions import *
import decimal
from models import Reslin_queasy

def write_reslin_queasybl(case_type:int, old_rqbuff:[Old_rqbuff], new_rqbuff:[New_rqbuff]):
    success_flag = False
    i_pos:int = 0
    ct:str = ""
    reslin_queasy = None

    old_rqbuff = new_rqbuff = rqbuff = None

    old_rqbuff_list, Old_rqbuff = create_model_like(Reslin_queasy)
    new_rqbuff_list, New_rqbuff = create_model_like(Reslin_queasy)

    Rqbuff = Reslin_queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, i_pos, ct, reslin_queasy
        nonlocal rqbuff


        nonlocal old_rqbuff, new_rqbuff, rqbuff
        nonlocal old_rqbuff_list, new_rqbuff_list
        return {"success_flag": success_flag}


    if case_type == 1:

        new_rqbuff = query(new_rqbuff_list, first=True)

        if not new_rqBuff:

            return generate_output()
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        buffer_copy(new_rQbuff, reslin_queasy)

        reslin_queasy = db_session.query(Reslin_queasy).first()

        success_flag = True
    elif case_type == 2:

        old_rqbuff = query(old_rqbuff_list, first=True)

        new_rqbuff = query(new_rqbuff_list, first=True)

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == old_rqBuff.key) &  (Reslin_queasy.resnr == old_rqBuff.resnr) &  (Reslin_queasy.reslinnr == old_rqBuff.reslinnr) &  (Reslin_queasy.number1 == old_rqBuff.number1) &  (Reslin_queasy.number2 == old_rqBuff.number2) &  (Reslin_queasy.number3 == old_rqBuff.number3) &  (Reslin_queasy.date1 == old_rqBuff.date1) &  (Reslin_queasy.date2 == old_rqBuff.date2) &  (Reslin_queasy.date3 == old_rqBuff.date3) &  (Reslin_queasy.char1 == old_rqBuff.char1) &  (Reslin_queasy.char2 == old_rqBuff.char2) &  (Reslin_queasy.char3 == old_rqBuff.char3) &  (Reslin_queasy.deci1 == old_rqBuff.deci1) &  (Reslin_queasy.deci2 == old_rqBuff.deci2) &  (Reslin_queasy.deci3 == old_rqBuff.deci3) &  (Reslin_queasy.logi1 == old_rqBuff.logi1) &  (Reslin_queasy.logi2 == old_rqBuff.logi2) &  (Reslin_queasy.logi3 == old_rqBuff.logi3)).first()

        if reslin_queasy:
            buffer_copy(new_rqBuff, reslin_queasy)

            reslin_queasy = db_session.query(Reslin_queasy).first()

            success_flag = True
    elif case_type == 3:

        old_rqbuff = query(old_rqbuff_list, first=True)

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == old_rqBuff.key) &  (Reslin_queasy.resnr == old_rqBuff.resnr) &  (Reslin_queasy.reslinnr == old_rqBuff.reslinnr) &  (Reslin_queasy.number1 == old_rqBuff.number1) &  (Reslin_queasy.number2 == old_rqBuff.number2) &  (Reslin_queasy.number3 == old_rqBuff.number3) &  (Reslin_queasy.date1 == old_rqBuff.date1) &  (Reslin_queasy.date2 == old_rqBuff.date2) &  (Reslin_queasy.date3 == old_rqBuff.date3) &  (Reslin_queasy.char1 == old_rqBuff.char1) &  (Reslin_queasy.char2 == old_rqBuff.char2) &  (Reslin_queasy.char3 == old_rqBuff.char3) &  (Reslin_queasy.deci1 == old_rqBuff.deci1) &  (Reslin_queasy.deci2 == old_rqBuff.deci2) &  (Reslin_queasy.deci3 == old_rqBuff.deci3) &  (Reslin_queasy.logi1 == old_rqBuff.logi1) &  (Reslin_queasy.logi2 == old_rqBuff.logi2) &  (Reslin_queasy.logi3 == old_rqBuff.logi3)).first()

        if reslin_queasy:
            db_session.delete(reslin_queasy)

            success_flag = True
    elif case_type == 4:

        new_rqbuff = query(new_rqbuff_list, first=True)

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == new_rqbuff.key) &  (Reslin_queasy.resnr == new_rqbuff.resnr) &  (Reslin_queasy.reslinnr == new_rqbuff.reslinnr)).first()

        if reslin_queasy:
            reslin_queasy.date2 = new_rqbuff.date1
            reslin_queasy.number2 = new_rqbuff.number1
            reslin_queasy.char2 = new_rqbuff.char1
            reslin_queasy.char3 = new_rqbuff.char3

            reslin_queasy = db_session.query(Reslin_queasy).first()
        else:
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            buffer_copy(new_rqbuff, reslin_queasy)

            reslin_queasy = db_session.query(Reslin_queasy).first()

    return generate_output()