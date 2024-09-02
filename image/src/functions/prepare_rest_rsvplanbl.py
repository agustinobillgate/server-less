from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, Htparam

def prepare_rest_rsvplanbl():
    from_date = None
    to_date = None
    min_dept = 0
    max_dept = 0
    from_dept = 0
    to_dept = 0
    curr_dept = 0
    depname1 = ""
    depname2 = ""
    depname3 = ""
    t_hoteldpt_list = []
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, min_dept, max_dept, from_dept, to_dept, curr_dept, depname1, depname2, depname3, t_hoteldpt_list, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"from_date": from_date, "to_date": to_date, "min_dept": min_dept, "max_dept": max_dept, "from_dept": from_dept, "to_dept": to_dept, "curr_dept": curr_dept, "depname1": depname1, "depname2": depname2, "depname3": depname3, "t-hoteldpt": t_hoteldpt_list}

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0)).first()

    if not hoteldpt:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    from_date = htparam.fdate
    to_date = htparam.fdate
    min_dept = 999
    max_dept = 1

    for hoteldpt in db_session.query(Hoteldpt).filter(
            (Hoteldpt.num >= 1)).all():

        if min_dept > hoteldpt.num:
            min_dept = hoteldpt.num

        if max_dept < hoteldpt.num:
            max_dept = hoteldpt.num
    curr_dept = min_dept
    from_dept = min_dept
    to_dept = max_dept

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == from_dept)).first()
    depname1 = hoteldpt.depart

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == to_dept)).first()
    depname2 = hoteldpt.depart

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_dept)).first()
    depname3 = hoteldpt.depart

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()