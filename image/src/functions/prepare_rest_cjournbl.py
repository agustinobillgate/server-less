from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, Htparam

def prepare_rest_cjournbl():
    from_date = None
    to_date = None
    long_digit = False
    depname1 = ""
    depname2 = ""
    t_hoteldpt_list = []
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, long_digit, depname1, depname2, t_hoteldpt_list, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"from_date": from_date, "to_date": to_date, "long_digit": long_digit, "depname1": depname1, "depname2": depname2, "t-hoteldpt": t_hoteldpt_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    from_date = htparam.fdate
    to_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == 1)).first()

    if hoteldpt:
        depname1 = hoteldpt.depart
        depname2 = hoteldpt.depart

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()