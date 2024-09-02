from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Hoteldpt, Waehrung

def prepare_hmcoup_listbl():
    billdate = None
    from_date = None
    to_date = None
    from_art = 0
    to_art = 0
    from_dept = 0
    to_dept = 0
    depname1 = ""
    depname2 = ""
    double_currency = False
    foreign_nr = 0
    exchg_rate = 0
    t_hoteldpt_list = []
    min_dept:int = 99
    max_dept:int = 0
    min_art:int = 9999
    max_art:int = 0
    htparam = hoteldpt = waehrung = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int, "depart":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, from_date, to_date, from_art, to_art, from_dept, to_dept, depname1, depname2, double_currency, foreign_nr, exchg_rate, t_hoteldpt_list, min_dept, max_dept, min_art, max_art, htparam, hoteldpt, waehrung


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"billdate": billdate, "from_date": from_date, "to_date": to_date, "from_art": from_art, "to_art": to_art, "from_dept": from_dept, "to_dept": to_dept, "depname1": depname1, "depname2": depname2, "double_currency": double_currency, "foreign_nr": foreign_nr, "exchg_rate": exchg_rate, "t-hoteldpt": t_hoteldpt_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate
    from_date = htparam.fdate - 1
    to_date = htparam.fdate - 1
    min_art = 0
    max_art = 99999
    from_art = min_art
    to_art = max_art
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
            (Htparam.paramnr == 240)).first()

    if htparam.flogical:
        double_currency = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr
            exchg_rate = waehrung.ankauf / waehrung.einheit
        else:
            exchg_rate = 1

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num
        t_hoteldpt.depart = hoteldpt.depart

    return generate_output()