#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Fixleist

def read_fixleistbl(case_type:int, resno:int, reslinno:int, fixnum:int):
    t_fixleist_list = []
    fixleist = None

    t_fixleist = None

    t_fixleist_list, T_fixleist = create_model_like(Fixleist)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_fixleist_list, fixleist
        nonlocal case_type, resno, reslinno, fixnum


        nonlocal t_fixleist
        nonlocal t_fixleist_list

        return {"t-fixleist": t_fixleist_list}

    if case_type == 1:

        for fixleist in db_session.query(Fixleist).filter(
                 (Fixleist.resnr == resno) & (Fixleist.reslinnr == reslinno) & (Fixleist.number >= fixnum)).order_by(Fixleist._recid).all():
            t_fixleist = T_fixleist()
            t_fixleist_list.append(t_fixleist)

            buffer_copy(fixleist, t_fixleist)

    elif case_type == 2:
        pass

    return generate_output()