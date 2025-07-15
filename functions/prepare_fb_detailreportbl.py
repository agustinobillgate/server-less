#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.select_deptbl import select_deptbl
from models import Hoteldpt

def prepare_fb_detailreportbl(from_dept:int, to_dept:int):
    to_date = None
    from_date = None
    depname1 = ""
    depname2 = ""
    t_hoteldpt_data = []
    t_htpchar:string = ""
    hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_date, from_date, depname1, depname2, t_hoteldpt_data, t_htpchar, hoteldpt
        nonlocal from_dept, to_dept


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_data

        return {"from_dept": from_dept, "to_dept": to_dept, "to_date": to_date, "from_date": from_date, "depname1": depname1, "depname2": depname2, "t-hoteldpt": t_hoteldpt_data}


    to_date = get_output(htpdate(110))
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
    from_dept, to_dept, depname1, depname2 = get_output(select_deptbl(from_dept, to_dept))

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()