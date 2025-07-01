#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Hoteldpt, Paramtext

def tada_dashboard_getparambl(dept:int):

    prepare_cache ([Hoteldpt, Paramtext])

    t_dept_list = []
    t_queasy270_list = []
    licensenr = ""
    interval_time = 0
    cancel_exist = False
    t_status_list = []
    pax:int = 0
    orderdatetime:string = ""
    gname:string = ""
    room:string = ""
    gastnr:int = 0
    resnr:int = 0
    reslinnr:int = 0
    mess_str:string = ""
    i_str:int = 0
    mess_token:string = ""
    mess_keyword:string = ""
    mess_value:string = ""
    table_no:int = 0
    dtime:datetime = None
    queasy = hoteldpt = paramtext = None

    t_dept = t_status = t_queasy270 = qsy230 = session_table = posted_item = None

    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":string})
    t_status_list, T_status = create_model("T_status", {"nr":int, "status_str":string})
    t_queasy270_list, T_queasy270 = create_model_like(Queasy)

    Qsy230 = create_buffer("Qsy230",Queasy)
    Session_table = create_buffer("Session_table",Queasy)
    Posted_item = create_buffer("Posted_item",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_dept_list, t_queasy270_list, licensenr, interval_time, cancel_exist, t_status_list, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, queasy, hoteldpt, paramtext
        nonlocal dept
        nonlocal qsy230, session_table, posted_item


        nonlocal t_dept, t_status, t_queasy270, qsy230, session_table, posted_item
        nonlocal t_dept_list, t_status_list, t_queasy270_list

        return {"t-dept": t_dept_list, "t-queasy270": t_queasy270_list, "licensenr": licensenr, "interval_time": interval_time, "cancel_exist": cancel_exist, "t-status": t_status_list}

    def decode_string(in_str:string):

        nonlocal t_dept_list, t_queasy270_list, licensenr, interval_time, cancel_exist, t_status_list, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, queasy, hoteldpt, paramtext
        nonlocal dept
        nonlocal qsy230, session_table, posted_item


        nonlocal t_dept, t_status, t_queasy270, qsy230, session_table, posted_item
        nonlocal t_dept_list, t_status_list, t_queasy270_list

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    queasy = get_cache (Queasy, {"key": [(eq, 11)]})
    cancel_exist = None != queasy

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num > 0)).order_by(Hoteldpt._recid).all():
        t_dept = T_dept()
        t_dept_list.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 1) & (Queasy.betriebsnr == dept)).order_by(Queasy._recid).all():

        if queasy.number2 == 3:
            interval_time = to_int(queasy.char2)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 1)).order_by(Queasy.betriebsnr, Queasy.number2).all():
        t_queasy270 = T_queasy270()
        t_queasy270_list.append(t_queasy270)

        buffer_copy(queasy, t_queasy270)

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)
    t_status = T_status()
    t_status_list.append(t_status)

    t_status.nr = 1
    t_status.status_str = "NEW"


    t_status = T_status()
    t_status_list.append(t_status)

    t_status.nr = 2
    t_status.status_str = "ON PROCESS"


    t_status = T_status()
    t_status_list.append(t_status)

    t_status.nr = 3
    t_status.status_str = "READY"


    t_status = T_status()
    t_status_list.append(t_status)

    t_status.nr = 4
    t_status.status_str = "COMPLETED"


    t_status = T_status()
    t_status_list.append(t_status)

    t_status.nr = 5
    t_status.status_str = "DECLINED"


    t_status = T_status()
    t_status_list.append(t_status)

    t_status.nr = 6
    t_status.status_str = "UNPAID"


    t_status = T_status()
    t_status_list.append(t_status)

    t_status.nr = 7
    t_status.status_str = "ON DELIVERY"


    t_status = T_status()
    t_status_list.append(t_status)

    t_status.nr = 8
    t_status.status_str = "DELIVERED"

    return generate_output()