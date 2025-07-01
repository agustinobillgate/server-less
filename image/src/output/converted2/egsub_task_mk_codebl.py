#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_subtask, Queasy

def egsub_task_mk_codebl(subtask_dept_nr:int, subtask_main_nr:int):

    prepare_cache ([Eg_subtask])

    t_sub_code = ""
    eg_subtask = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_sub_code, eg_subtask, queasy
        nonlocal subtask_dept_nr, subtask_main_nr

        return {"t_sub_code": t_sub_code}

    def mk_code():

        nonlocal t_sub_code, eg_subtask, queasy
        nonlocal subtask_dept_nr, subtask_main_nr

        tmp:int = 0
        ctr:int = 0
        ebuff = None
        qbuff = None
        Ebuff =  create_buffer("Ebuff",Eg_subtask)
        Qbuff =  create_buffer("Qbuff",Queasy)

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, subtask_dept_nr)]})

        if not queasy:

            return

        qbuff = db_session.query(Qbuff).filter(
                 (Qbuff.key == 133) & (Qbuff.number1 == subtask_main_nr)).first()

        if not qbuff:

            return
        ctr = 0

        for ebuff in db_session.query(Ebuff).filter(
                 (Ebuff.dept_nr == subtask_dept_nr) & (Ebuff.main_nr == subtask_main_nr)).order_by(Ebuff._recid).all():
            tmp = to_int(substring(ebuff.sub_code, 5, 3))

            if tmp > ctr:
                ctr = to_int(substring(ebuff.sub_code, 5, 3))
        ctr = ctr + 1
        t_sub_code = to_string(subtask_dept_nr, "99") + to_string(subtask_main_nr, "999") + to_string(ctr, "999")


    mk_code()

    return generate_output()