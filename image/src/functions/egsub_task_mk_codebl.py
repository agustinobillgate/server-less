from functions.additional_functions import *
import decimal
from models import Eg_subtask, Queasy

def egsub_task_mk_codebl(subtask_dept_nr:int, subtask_main_nr:int):
    t_sub_code = ""
    eg_subtask = queasy = None

    ebuff = qbuff = None

    Ebuff = Eg_subtask
    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_sub_code, eg_subtask, queasy
        nonlocal ebuff, qbuff


        nonlocal ebuff, qbuff
        return {"t_sub_code": t_sub_code}

    def mk_code():

        nonlocal t_sub_code, eg_subtask, queasy
        nonlocal ebuff, qbuff


        nonlocal ebuff, qbuff

        tmp:int = 0
        ctr:int = 0
        Ebuff = Eg_subtask
        Qbuff = Queasy

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 19) &  (Queasy.number1 == subtask_dept_nr)).first()

        if not queasy:

            return

        qbuff = db_session.query(Qbuff).filter(
                (Qbuff.key == 133) &  (Qbuff.number1 == subtask_main_nr)).first()

        if not qbuff:

            return
        ctr = 0

        for ebuff in db_session.query(Ebuff).filter(
                (Ebuff.dept_nr == subtask_dept_nr) &  (Ebuff.main_nr == subtask_main_nr)).all():
            tmp = to_int(substring(ebuff.sub_code, 5, 3))

            if tmp > ctr:
                ctr = to_int(substring(ebuff.sub_code, 5, 3))
        ctr = ctr + 1
        t_sub_code = to_string(subtask_dept_nr, "99") + to_string(subtask_main_nr, "999") + to_string(ctr, "999")

    mk_code()

    return generate_output()