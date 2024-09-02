from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Hoteldpt, Waehrung

def prepare_ktrans_reportbl(min_dept:int, max_dept:int):
    billdate = None
    from_date = None
    to_date = None
    long_digit = False
    min_art = 0
    max_art = 0
    from_art = 0
    to_art = 0
    from_dept = 0
    to_dept = 0
    depname1 = ""
    depname2 = ""
    double_currency = False
    exchg_rate = 0
    t_hoteldpt_list = []
    htparam = hoteldpt = waehrung = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int, "depart":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, from_date, to_date, long_digit, min_art, max_art, from_art, to_art, from_dept, to_dept, depname1, depname2, double_currency, exchg_rate, t_hoteldpt_list, htparam, hoteldpt, waehrung


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"billdate": billdate, "from_date": from_date, "to_date": to_date, "long_digit": long_digit, "min_art": min_art, "max_art": max_art, "from_art": from_art, "to_art": to_art, "from_dept": from_dept, "to_dept": to_dept, "depname1": depname1, "depname2": depname2, "double_currency": double_currency, "exchg_rate": exchg_rate, "t-hoteldpt": t_hoteldpt_list}

    def select_dept():

        nonlocal billdate, from_date, to_date, long_digit, min_art, max_art, from_art, to_art, from_dept, to_dept, depname1, depname2, double_currency, exchg_rate, t_hoteldpt_list, htparam, hoteldpt, waehrung


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        ldry:int = 0
        dstore:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1081)).first()
        ldry = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1082)).first()
        dstore = finteger
        min_dept = 1

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= 1) &  (Hoteldpt.num != ldry) &  (Hoteldpt.num != dstore)).all():

            if max_dept < hoteldpt.num:
                max_dept = hoteldpt.num

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate
    from_date = htparam.fdate - 1
    to_date = htparam.fdate - 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    select_dept()
    min_art = 0
    max_art = 99999
    from_art = min_art
    to_art = max_art
    from_dept = min_dept
    to_dept = max_dept

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == from_dept)).first()
    depname1 = hoteldpt.depart

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == to_dept)).first()
    depname2 = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam.flogical:
        double_currency = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit
        else:
            exchg_rate = 1

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num
        t_hoteldpt.depart = hoteldpt.depart

    return generate_output()