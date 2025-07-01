#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.pos_dashboard_getparambl import pos_dashboard_getparambl
from functions.pos_dashboard_expired_sessionbl import pos_dashboard_expired_sessionbl
from functions.pos_dashboard_opened_tischbl import pos_dashboard_opened_tischbl
from functions.pos_dashboard_load_orderbl import pos_dashboard_load_orderbl
from models import Queasy

def pos_dashboard_auto_refresh1_webbl(user_init:string, dept_no:int):

    prepare_cache ([Queasy])

    urlws = ""
    licensenr = 0
    dynamic_qr = False
    interval_time = 0
    asroom_service = False
    cancel_exist = False
    found_new_order = False
    ask_bill_flag = False
    sound_link = ""
    t_dept_list = []
    t_queasy222_list = []
    t_list_list = []
    pick_table_list = []
    order_list_list = []
    order_item_list = []
    check_new_ordered:bool = False
    queasy = None

    t_list = pick_table = order_list = order_item = t_dept = t_queasy222 = None

    t_list_list, T_list = create_model("T_list", {"dept":int, "tischnr":int, "bezeich":string, "normalbeleg":int, "name":string, "occupied":bool, "belegung":int, "balance":Decimal, "zinr":string, "gname":string, "ask_bill":bool, "bill_print":bool, "platform":string, "allow_ctr":string, "bill_number":int, "pay_status":string})
    pick_table_list, Pick_table = create_model("Pick_table", {"dept":int, "tableno":int, "pax":int, "gname":string, "occupied":bool, "session_parameter":string, "gemail":string, "expired_session":bool, "dataqr":string, "date_time":datetime})
    order_list_list, Order_list = create_model("Order_list", {"table_nr":int, "pax":int, "order_nr":int, "guest_name":string, "room_no":string, "order_date":string, "posted":bool, "guest_nr":int, "resnr":int, "reslinnr":int, "sessionprm":string, "billrecid":int})
    order_item_list, Order_item = create_model("Order_item", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":string, "qty":int, "sp_req":string, "confirm":bool, "remarks":string, "order_date":string, "art_nr":int, "posted":bool})
    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":string})
    t_queasy222_list, T_queasy222 = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal urlws, licensenr, dynamic_qr, interval_time, asroom_service, cancel_exist, found_new_order, ask_bill_flag, sound_link, t_dept_list, t_queasy222_list, t_list_list, pick_table_list, order_list_list, order_item_list, check_new_ordered, queasy
        nonlocal user_init, dept_no


        nonlocal t_list, pick_table, order_list, order_item, t_dept, t_queasy222
        nonlocal t_list_list, pick_table_list, order_list_list, order_item_list, t_dept_list, t_queasy222_list

        return {"urlws": urlws, "licensenr": licensenr, "dynamic_qr": dynamic_qr, "interval_time": interval_time, "asroom_service": asroom_service, "cancel_exist": cancel_exist, "found_new_order": found_new_order, "ask_bill_flag": ask_bill_flag, "sound_link": sound_link, "t-dept": t_dept_list, "t-queasy222": t_queasy222_list, "t-list": t_list_list, "pick-table": pick_table_list, "order-list": order_list_list, "order-item": order_item_list}

    t_dept_list, t_queasy222_list, urlws, licensenr, dynamic_qr, interval_time, asroom_service, cancel_exist = get_output(pos_dashboard_getparambl(dept_no))

    t_dept = query(t_dept_list, filters=(lambda t_dept: t_dept.nr == dept_no), first=True)
    get_output(pos_dashboard_expired_sessionbl(t_dept.nr, dynamic_qr))
    t_list_list, pick_table_list = get_output(pos_dashboard_opened_tischbl(t_dept.nr))
    order_list_list, order_item_list = get_output(pos_dashboard_load_orderbl(t_dept.nr))

    t_list = query(t_list_list, filters=(lambda t_list: t_list.ask_bill  and t_list.bill_print == False), first=True)

    if t_list:
        ask_bill_flag = True

    for order_list in query(order_list_list, filters=(lambda order_list: not order_list.posted)):
        check_new_ordered = True

        if check_new_ordered :
            break
    found_new_order = check_new_ordered

    queasy = get_cache (Queasy, {"key": [(eq, 222)],"betriebsnr": [(eq, dept_no)],"number1": [(eq, 1)],"number2": [(eq, 29)],"number3": [(eq, 5)]})

    if queasy:
        sound_link = queasy.char2

    return generate_output()