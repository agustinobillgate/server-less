#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Kellner

def select_husr_disp_itbl(curr_dept:int, kname:string):
    t_hoteldpt_list = []
    t_kellner_list = []
    hoteldpt = kellner = None

    t_hoteldpt = t_kellner = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)
    t_kellner_list, T_kellner = create_model_like(Kellner, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_hoteldpt_list, t_kellner_list, hoteldpt, kellner
        nonlocal curr_dept, kname


        nonlocal t_hoteldpt, t_kellner
        nonlocal t_hoteldpt_list, t_kellner_list

        return {"t-hoteldpt": t_hoteldpt_list, "t-kellner": t_kellner_list}


    for kellner in db_session.query(Kellner).order_by(Kellner._recid).all():
        t_kellner = T_kellner()
        t_kellner_list.append(t_kellner)

        buffer_copy(kellner, t_kellner)
        t_kellner.rec_id = kellner._recid

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()