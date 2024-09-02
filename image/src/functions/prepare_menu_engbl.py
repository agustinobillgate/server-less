from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from functions.select_deptbl import select_deptbl
from functions.htpint import htpint
from functions.htpchar import htpchar
from sqlalchemy import func
from models import Hoteldpt, Wgrpdep, Waehrung

def prepare_menu_engbl(from_dept:int, to_dept:int):
    to_date = None
    from_date = None
    vat_included = False
    depname1 = ""
    depname2 = ""
    ldry_dept = 0
    double_currency = False
    exchg_rate = 0
    t_hoteldpt_list = []
    t_wgrpdep_list = []
    t_htpchar:str = ""
    hoteldpt = wgrpdep = waehrung = None

    t_hoteldpt = t_wgrpdep = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)
    t_wgrpdep_list, T_wgrpdep = create_model_like(Wgrpdep)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_date, from_date, vat_included, depname1, depname2, ldry_dept, double_currency, exchg_rate, t_hoteldpt_list, t_wgrpdep_list, t_htpchar, hoteldpt, wgrpdep, waehrung


        nonlocal t_hoteldpt, t_wgrpdep
        nonlocal t_hoteldpt_list, t_wgrpdep_list
        return {"to_date": to_date, "from_date": from_date, "vat_included": vat_included, "depname1": depname1, "depname2": depname2, "ldry_dept": ldry_dept, "double_currency": double_currency, "exchg_rate": exchg_rate, "t-hoteldpt": t_hoteldpt_list, "t-wgrpdep": t_wgrpdep_list}

    to_date = get_output(htpdate(110))
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
    vat_included = get_output(htplogic(134))
    from_dept, to_dept, depname1, depname2 = get_output(select_deptbl(from_dept, to_dept))
    ldry_dept = get_output(htpint(1081))
    double_currency = get_output(htplogic(240))

    if double_currency:
        t_htpchar = get_output(htpchar(144))

        waehrung = db_session.query(Waehrung).filter(
                (func.lower(Waehrung.wabkurz) == (t_htpchar).lower())).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    for wgrpdep in db_session.query(Wgrpdep).all():
        t_wgrpdep = T_wgrpdep()
        t_wgrpdep_list.append(t_wgrpdep)

        buffer_copy(wgrpdep, t_wgrpdep)

    return generate_output()