from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, Htparam

def prepare_fb_statisticbl(fdept:int, tdept:int):
    price_decimal = 0
    ci_date = None
    fdpt_str = ""
    tdpt_str = ""
    t_hoteldpt_list = []
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, ci_date, fdpt_str, tdpt_str, t_hoteldpt_list, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"price_decimal": price_decimal, "ci_date": ci_date, "fdpt_str": fdpt_str, "tdpt_str": tdpt_str, "t-hoteldpt": t_hoteldpt_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0) &  (Hoteldpt.num == fdept)).first()

    if hoteldpt:
        fdpt_str = hoteldpt.depart

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0) &  (Hoteldpt.num == tdept)).first()

    if hoteldpt:
        tdpt_str = hoteldpt.depart

    for hoteldpt in db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0)).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()