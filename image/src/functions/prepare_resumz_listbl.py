from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, Htparam

def prepare_resumz_listbl():
    long_digit = False
    to_date = None
    ldry = 0
    dstore = 0
    from_dept = 0
    to_dept = 0
    depname1 = ""
    depname2 = ""
    t_hoteldpt_list = []
    min_dept:int = 0
    max_dept:int = 0
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, to_date, ldry, dstore, from_dept, to_dept, depname1, depname2, t_hoteldpt_list, min_dept, max_dept, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"long_digit": long_digit, "to_date": to_date, "ldry": ldry, "dstore": dstore, "from_dept": from_dept, "to_dept": to_dept, "depname1": depname1, "depname2": depname2, "t-hoteldpt": t_hoteldpt_list}

    def select_dept():

        nonlocal long_digit, to_date, ldry, dstore, from_dept, to_dept, depname1, depname2, t_hoteldpt_list, min_dept, max_dept, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1081)).first()
        ldry = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1082)).first()
        dstore = finteger
        min_dept = 0

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= 1) &  (Hoteldpt.num != ldry) &  (Hoteldpt.num != dstore)).all():

            if max_dept < hoteldpt.num:
                max_dept = hoteldpt.num
        from_dept = min_dept
        to_dept = max_dept

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == from_dept)).first()

        if hoteldpt:
            depname1 = hoteldpt.depart

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == to_dept)).first()

        if hoteldpt:
            depname2 = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    to_date = get_current_date()
    select_dept()

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()