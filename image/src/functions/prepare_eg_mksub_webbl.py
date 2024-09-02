from functions.additional_functions import *
import decimal
from models import Queasy, Eg_subtask

def prepare_eg_mksub_webbl(deptnr:int, mainnr:int):
    fl_code = 0
    subtask = ""
    t_queasy_list = []
    queasy = eg_subtask = None

    t_queasy = qbuff = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"number1":int})

    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, subtask, t_queasy_list, queasy, eg_subtask
        nonlocal qbuff


        nonlocal t_queasy, qbuff
        nonlocal t_queasy_list
        return {"fl_code": fl_code, "subtask": subtask, "t-queasy": t_queasy_list}

    def mk_code():

        nonlocal fl_code, subtask, t_queasy_list, queasy, eg_subtask
        nonlocal qbuff


        nonlocal t_queasy, qbuff
        nonlocal t_queasy_list

        tmp:int = 0
        ctr:int = 0
        Qbuff = Queasy

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 19) &  (Queasy.number1 == deptnr)).first()

        if not queasy:

            return

        qbuff = db_session.query(Qbuff).filter(
                (Qbuff.key == 133) &  (Qbuff.number1 == mainnr)).first()

        if not qbuff:

            return
        ctr = 0

        for eg_subtask in db_session.query(Eg_subtask).filter(
                (Eg_subtask.dept_nr == deptnr) &  (Eg_subtask.main_nr == mainnr)).all():
            tmp = to_int(substring(eg_subtask.sub_code, 5, 3))

            if tmp > ctr:
                ctr = to_int(substring(eg_subtask.sub_code, 5, 3))
        ctr = ctr + 1
        subtask = to_string(deptnr, "99") + to_string(mainnr, "999") + to_string(ctr, "999")


    mk_code()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 19) &  (Queasy.number1 == deptnr)).first()

    if not queasy:
        fl_code = 1

        return generate_output()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 133) &  (Queasy.number1 == mainnr)).first()

    if not queasy:
        fl_code = 1

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.KEY == 131)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        t_queasy.number1 = queasy.number1

    return generate_output()