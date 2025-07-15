#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Hoteldpt, Paramtext

def pos_dashboard_getparambl(dept:int):

    prepare_cache ([Hoteldpt, Paramtext])

    t_dept_data = []
    t_queasy222_data = []
    urlws = ""
    licensenr = 0
    dynamic_qr = False
    interval_time = 0
    asroom_service = False
    cancel_exist = False
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
    zeit:int = 0
    queasy = hoteldpt = paramtext = None

    t_dept = pick_table = t_queasy222 = qsy230 = session_table = posted_item = None

    t_dept_data, T_dept = create_model("T_dept", {"nr":int, "dept":string})
    pick_table_data, Pick_table = create_model("Pick_table", {"dept":int, "tableno":int, "pax":int, "gname":string, "occupied":bool, "session_parameter":string, "gemail":string, "active_session":bool, "dataqr":string, "date_time":datetime})
    t_queasy222_data, T_queasy222 = create_model_like(Queasy)

    Qsy230 = create_buffer("Qsy230",Queasy)
    Session_table = create_buffer("Session_table",Queasy)
    Posted_item = create_buffer("Posted_item",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_dept_data, t_queasy222_data, urlws, licensenr, dynamic_qr, interval_time, asroom_service, cancel_exist, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, zeit, queasy, hoteldpt, paramtext
        nonlocal dept
        nonlocal qsy230, session_table, posted_item


        nonlocal t_dept, pick_table, t_queasy222, qsy230, session_table, posted_item
        nonlocal t_dept_data, pick_table_data, t_queasy222_data

        return {"t-dept": t_dept_data, "t-queasy222": t_queasy222_data, "urlws": urlws, "licensenr": licensenr, "dynamic_qr": dynamic_qr, "interval_time": interval_time, "asroom_service": asroom_service, "cancel_exist": cancel_exist}

    def decode_string(in_str:string):

        nonlocal t_dept_data, t_queasy222_data, urlws, licensenr, dynamic_qr, interval_time, asroom_service, cancel_exist, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, zeit, queasy, hoteldpt, paramtext
        nonlocal dept
        nonlocal qsy230, session_table, posted_item


        nonlocal t_dept, pick_table, t_queasy222, qsy230, session_table, posted_item
        nonlocal t_dept_data, pick_table_data, t_queasy222_data

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
        t_dept_data.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept)]})
    while None != queasy:

        if queasy.number2 == 6:
            urlws = queasy.char2

        if queasy.number2 == 13:
            interval_time = to_int(queasy.char2)

        if queasy.number2 == 14:
            dynamic_qr = queasy.logi1

        if queasy.number2 == 21:
            asroom_service = queasy.logi1

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.betriebsnr == dept) & (Queasy._recid > curr_recid)).first()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 222) & (Queasy.number1 == 1)).order_by(Queasy.betriebsnr, Queasy.number2).all():
        t_queasy222 = T_queasy222()
        t_queasy222_data.append(t_queasy222)

        buffer_copy(queasy, t_queasy222)

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)

    return generate_output()