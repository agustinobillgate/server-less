from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Hoteldpt, Paramtext

def pos_dashboard_getparambl(dept:int):
    t_dept_list = []
    t_queasy222_list = []
    urlws = ""
    licensenr = 0
    static_qr = False
    interval_time = 0
    asroom_service = False
    cancel_exist = False
    pax:int = 0
    orderdatetime:str = ""
    gname:str = ""
    room:str = ""
    gastnr:int = 0
    resnr:int = 0
    reslinnr:int = 0
    mess_str:str = ""
    i_str:int = 0
    mess_token:str = ""
    mess_keyword:str = ""
    mess_value:str = ""
    table_no:int = 0
    dtime: = None
    queasy = hoteldpt = paramtext = None

    t_dept = pick_table = t_queasy222 = qsy230 = session_table = posted_item = None

    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":str})
    pick_table_list, Pick_table = create_model("Pick_table", {"dept":int, "tableno":int, "pax":int, "gname":str, "occupied":bool, "session_parameter":str, "gemail":str, "active_session":bool, "dataqr":str, "date_time":})
    t_queasy222_list, T_queasy222 = create_model_like(Queasy)

    Qsy230 = Queasy
    Session_table = Queasy
    Posted_item = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_dept_list, t_queasy222_list, urlws, licensenr, static_qr, interval_time, asroom_service, cancel_exist, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, queasy, hoteldpt, paramtext
        nonlocal qsy230, session_table, posted_item


        nonlocal t_dept, pick_table, t_queasy222, qsy230, session_table, posted_item
        nonlocal t_dept_list, pick_table_list, t_queasy222_list
        return {"t-dept": t_dept_list, "t-queasy222": t_queasy222_list, "urlws": urlws, "licensenr": licensenr, "static_qr": static_qr, "interval_time": interval_time, "asroom_service": asroom_service, "cancel_exist": cancel_exist}

    def decode_string(in_str:str):

        nonlocal t_dept_list, t_queasy222_list, urlws, licensenr, static_qr, interval_time, asroom_service, cancel_exist, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, queasy, hoteldpt, paramtext
        nonlocal qsy230, session_table, posted_item


        nonlocal t_dept, pick_table, t_queasy222, qsy230, session_table, posted_item
        nonlocal t_dept_list, pick_table_list, t_queasy222_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 11)).first()
    cancel_exist = None != queasy

    for hoteldpt in db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0)).all():
        t_dept = T_dept()
        t_dept_list.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 222) &  (Queasy.number1 == 1) &  (Queasy.betriebsnr == dept)).first()
    while None != queasy:

        if queasy.number2 == 6:
            urlws = queasy.char2

        if queasy.number2 == 13:
            interval_time = to_int(queasy.char2)

        if queasy.number2 == 14:
            static_qr = queasy.logi1

        if queasy.number2 == 21:
            asroom_service = queasy.logi1

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 222) &  (Queasy.number1 == 1) &  (Queasy.betriebsnr == dept)).first()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 222) &  (Queasy.number1 == 1)).all():
        t_queasy222 = T_queasy222()
        t_queasy222_list.append(t_queasy222)

        buffer_copy(queasy, t_queasy222)

    if not static_qr:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (func.lower(Queasy.char1) == "taken_table") &  (Queasy.number1 == dept) &  (Queasy.logi1) &  (Queasy.logi2) &  (len(entry(0, Queasy.char3, "|Queasy.")) <= 20)).first()
        while None != queasy:

            posted_item = db_session.query(Posted_item).filter(
                    (Posted_item.key == 225) &  (func.lower(Posted_item.char1) == "orderbill") &  (Posted_item.char3 == entry(0, queasy.char3, "|"))).first()

            if posted_item:
                queasy.number3 = posted_item.number3

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 225) &  (func.lower(Queasy.char1) == "taken_table") &  (Queasy.number1 == dept) &  (Queasy.logi1) &  (Queasy.logi2) &  (len(entry(0, Queasy.char3, "|Queasy.")) <= 20)).first()
    else:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (func.lower(Queasy.char1) == "taken_table") &  (Queasy.logi1) &  (Queasy.logi2 == False)).first()
        while None != queasy:

            posted_item = db_session.query(Posted_item).filter(
                    (Posted_item.key == 225) &  (func.lower(Posted_item.char1) == "orderbill") &  (Posted_item.char3 == entry(0, queasy.char3, "|"))).first()

            if posted_item:
                queasy.number3 = posted_item.number3

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 225) &  (func.lower(Queasy.char1) == "taken_table") &  (Queasy.logi1) &  (Queasy.logi2 == False)).first()


    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(ptexte)

    return generate_output()