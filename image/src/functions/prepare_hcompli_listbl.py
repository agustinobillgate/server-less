from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, Htparam, Queasy, Waehrung

def prepare_hcompli_listbl():
    from_dept = 0
    to_dept = 0
    billdate = None
    avail_queasy = False
    min_dept = 0
    max_dept = 0
    depname1 = ""
    depname2 = ""
    double_currency = False
    exchg_rate = 0
    foreign_nr = 0
    min_art = 0
    max_art = 0
    from_art = 0
    to_art = 0
    t_hoteldpt_list = []
    ldry:int = 0
    dstore:int = 0
    hoteldpt = htparam = queasy = waehrung = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int, "depart":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_dept, to_dept, billdate, avail_queasy, min_dept, max_dept, depname1, depname2, double_currency, exchg_rate, foreign_nr, min_art, max_art, from_art, to_art, t_hoteldpt_list, ldry, dstore, hoteldpt, htparam, queasy, waehrung


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"from_dept": from_dept, "to_dept": to_dept, "billdate": billdate, "avail_queasy": avail_queasy, "min_dept": min_dept, "max_dept": max_dept, "depname1": depname1, "depname2": depname2, "double_currency": double_currency, "exchg_rate": exchg_rate, "foreign_nr": foreign_nr, "min_art": min_art, "max_art": max_art, "from_art": from_art, "to_art": to_art, "t-hoteldpt": t_hoteldpt_list}

    def select_dept():

        nonlocal from_dept, to_dept, billdate, avail_queasy, min_dept, max_dept, depname1, depname2, double_currency, exchg_rate, foreign_nr, min_art, max_art, from_art, to_art, t_hoteldpt_list, ldry, dstore, hoteldpt, htparam, queasy, waehrung


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1081)).first()
        ldry = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1082)).first()
        dstore = finteger
        min_dept = 999
        max_dept = 1

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= 1) &  (Hoteldpt.num != ldry) &  (Hoteldpt.num != dstore)).all():

            if min_dept > hoteldpt.num:
                min_dept = hoteldpt.num

            if max_dept < hoteldpt.num:
                max_dept = hoteldpt.num

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0)).first()

    if not hoteldpt:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate
    select_dept()
    min_art = 0
    max_art = 99999
    from_art = min_art
    to_art = max_art

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 105)).first()

    if queasy:
        avail_queasy = True
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

    if htparam.fchar != "":

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit
            foreign_nr = waehrungsnr
        else:
            exchg_rate = 1

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num
        t_hoteldpt.depart = hoteldpt.depart

    return generate_output()