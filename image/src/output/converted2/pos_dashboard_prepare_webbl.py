#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.pos_dashboard_check_waiteraccountbl import pos_dashboard_check_waiteraccountbl
from functions.pos_dashboard_getparambl import pos_dashboard_getparambl
from functions.pos_dashboard_opened_tischbl import pos_dashboard_opened_tischbl
from functions.pos_dashboard_load_orderbl import pos_dashboard_load_orderbl
from models import Queasy

def pos_dashboard_prepare_webbl(user_init:string, init_posdept:int, bedi_username:string):
    result_msg = ""
    urlws = ""
    licensenr = 0
    dynamic_qr = False
    interval_time = 0
    asroom_service = False
    cancel_exist = False
    t_dept_list = []
    t_queasy222_list = []
    t_list_list = []
    pick_table_list = []
    order_list_list = []
    order_item_list = []
    active_waiter:bool = False
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
        nonlocal result_msg, urlws, licensenr, dynamic_qr, interval_time, asroom_service, cancel_exist, t_dept_list, t_queasy222_list, t_list_list, pick_table_list, order_list_list, order_item_list, active_waiter, queasy
        nonlocal user_init, init_posdept, bedi_username


        nonlocal t_list, pick_table, order_list, order_item, t_dept, t_queasy222
        nonlocal t_list_list, pick_table_list, order_list_list, order_item_list, t_dept_list, t_queasy222_list

        return {"result_msg": result_msg, "urlws": urlws, "licensenr": licensenr, "dynamic_qr": dynamic_qr, "interval_time": interval_time, "asroom_service": asroom_service, "cancel_exist": cancel_exist, "t-dept": t_dept_list, "t-queasy222": t_queasy222_list, "t-list": t_list_list, "pick-table": pick_table_list, "order-list": order_list_list, "order-item": order_item_list}


    if bedi_username == None:
        bedi_username = ""
    active_waiter = get_output(pos_dashboard_check_waiteraccountbl(user_init, 1, bedi_username))

    if not active_waiter:
        result_msg = "Waiter / Cashier Account not defined."

        return generate_output()
    t_dept_list, t_queasy222_list, urlws, licensenr, dynamic_qr, interval_time, asroom_service, cancel_exist = get_output(pos_dashboard_getparambl(1))

    t_dept = query(t_dept_list, filters=(lambda t_dept: t_dept.nr == 1), first=True)
    t_list_list, pick_table_list = get_output(pos_dashboard_opened_tischbl(t_dept.nr))
    order_list_list, order_item_list = get_output(pos_dashboard_load_orderbl(t_dept.nr))

    return generate_output()