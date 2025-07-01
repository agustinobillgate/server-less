#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Eg_subtask

def prepare_eg_mksub_webbl(deptnr:int, mainnr:int):

    prepare_cache ([Queasy, Eg_subtask])

    fl_code = 0
    subtask = ""
    t_queasy_list = []
    queasy = eg_subtask = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"number1":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, subtask, t_queasy_list, queasy, eg_subtask
        nonlocal deptnr, mainnr


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"fl_code": fl_code, "subtask": subtask, "t-queasy": t_queasy_list}

    def mk_code():

        nonlocal fl_code, subtask, t_queasy_list, queasy, eg_subtask
        nonlocal deptnr, mainnr


        nonlocal t_queasy
        nonlocal t_queasy_list

        tmp:int = 0
        ctr:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, deptnr)]})

        if not queasy:

            return

        qbuff = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, mainnr)]})

        if not qbuff:

            return
        ctr = 0

        for eg_subtask in db_session.query(Eg_subtask).filter(
                 (Eg_subtask.dept_nr == deptnr) & (Eg_subtask.main_nr == mainnr)).order_by(Eg_subtask._recid).all():
            tmp = to_int(substring(eg_subtask.sub_code, 5, 3))

            if tmp > ctr:
                ctr = to_int(substring(eg_subtask.sub_code, 5, 3))
        ctr = ctr + 1
        subtask = to_string(deptnr, "99") + to_string(mainnr, "999") + to_string(ctr, "999")

    mk_code()

    queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, deptnr)]})

    if not queasy:
        fl_code = 1

        return generate_output()

    queasy = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, mainnr)]})

    if not queasy:
        fl_code = 1

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 131)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        t_queasy.number1 = queasy.number1

    return generate_output()