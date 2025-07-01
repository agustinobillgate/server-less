#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def mp_select_instructionbl(dept_nr:int):
    t_queasy_list = []
    queasy = None

    t_queasy = buffqueasy = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"instruct_no":int, "dept_no":int, "department":string, "instruction":string})

    Buffqueasy = create_buffer("Buffqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy
        nonlocal dept_nr
        nonlocal buffqueasy


        nonlocal t_queasy, buffqueasy
        nonlocal t_queasy_list

        return {"t-queasy": t_queasy_list}

    for bk_queasy in query(bk_queasy_list, filters=(lambda bk_queasy: bk_queasy.key == 13)):

        buffqueasy = db_session.query(Buffqueasy).filter(
                 (buffQueasy.key == 148) & (buffQueasy.number1 == bk_queasy.number2) & (buffQueasy.number1 == dept_nr)).first()

        if buffQueasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            t_queasy.instruct_no = bk_queasy.number1
            t_queasy.dept_no = buffQueasy.number1
            t_queasy.department = buffQueasy.char3
            t_queasy.instruction = bk_queasy.char1

    return generate_output()