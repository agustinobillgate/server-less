from functions.additional_functions import *
import decimal
from models import Eg_subtask

def egsub_task_btn_exitbl(subtask:[Subtask], case_type:int, user_init:str, rec_id:int):
    fl_code = 0
    eg_subtask = None

    subtask = subbuff = None

    subtask_list, Subtask = create_model_like(Eg_subtask)

    Subbuff = Eg_subtask

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_subtask
        nonlocal subbuff


        nonlocal subtask, subbuff
        nonlocal subtask_list
        return {"fl_code": fl_code}

    subtask = query(subtask_list, first=True)

    if case_type == 1:
        eg_subtask = Eg_subtask()
        db_session.add(eg_subtask)

        subtask.create_DATE = get_current_date()
        subtask.create_TIME = get_current_time_in_seconds()
        subtask.create_by = user_init
        subtask.sourceForm = "0"


        buffer_copy(subtask, eg_subtask)

    elif case_type == 2:

        subbuff = db_session.query(Subbuff).filter(
                (subBuff.main_nr == subtask.main_nr) &  (subBuff.bezeich == subtask.bezeich) &  (Subbuff.sub_code != subtask.sub_code)).first()

        if subBuff:
            fl_code = 1
        else:

            eg_subtask = db_session.query(Eg_subtask).filter(
                    (Eg_subtask.dept_nr == subtask.dept_nr) &  (Eg_subtask.main_nr == subtask.main_nr) &  (Eg_subtask.sub_code == subtask.sub_code)).first()

            if eg_subtask:

                if eg_subtask.othersflag != subtask.othersflag:

                    if subtask.othersflag :

                        eg_subtask = db_session.query(Eg_subtask).filter(
                                (Eg_subtask.dept_nr == subtask.dept_nr) &  (Eg_subtask.main_nr == subtask.main_nr) &  (Eg_subtask.sub_code != subtask.sub_code) &  (Eg_subtask.othersflag)).first()

                        if eg_subtask:
                            fl_code = 2
                        else:

                            eg_subtask = db_session.query(Eg_subtask).filter(
                                    (Eg_subtask._recid == rec_id)).first()

                            eg_subtask = db_session.query(Eg_subtask).first()
                            buffer_copy(subtask, eg_subtask)

                            eg_subtask = db_session.query(Eg_subtask).first()

                            fl_code = 3
                    else:

                        eg_subtask = db_session.query(Eg_subtask).filter(
                                (Eg_subtask._recid == rec_id)).first()

                        eg_subtask = db_session.query(Eg_subtask).first()
                        buffer_copy(subtask, eg_subtask)

                        eg_subtask = db_session.query(Eg_subtask).first()

                        fl_code = 3
                else:

                    eg_subtask = db_session.query(Eg_subtask).filter(
                            (Eg_subtask._recid == rec_id)).first()

                    eg_subtask = db_session.query(Eg_subtask).first()
                    buffer_copy(subtask, eg_subtask)

                    eg_subtask = db_session.query(Eg_subtask).first()

                    fl_code = 3

    return generate_output()