#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Eg_subtask

def eg_mksub_mk_codebl(deptnr:int, mainnr:int):

    prepare_cache ([Eg_subtask])

    subtask = ""
    queasy = eg_subtask = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal subtask, queasy, eg_subtask
        nonlocal deptnr, mainnr

        return {"subtask": subtask}

    def mk_code():

        nonlocal subtask, queasy, eg_subtask
        nonlocal deptnr, mainnr

        tmp:int = 0
        ctr:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, deptnr)]})

        if not queasy:

            return

        qbuff = db_session.query(Qbuff).filter(
                 (Qbuff.key == 133) & (Qbuff.number1 == mainnr)).first()

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

    return generate_output()