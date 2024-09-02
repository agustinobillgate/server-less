from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, H_bill

def pos_dashboard_load_orderbl(dept:int):
    order_list_list = []
    order_item_list = []
    mess_str:str = ""
    i_str:int = 0
    mess_token:str = ""
    mess_keyword:str = ""
    mess_value:str = ""
    pax:int = 0
    orderdatetime:str = ""
    gname:str = ""
    room:str = ""
    gastnr:int = 0
    resnr:int = 0
    reslinnr:int = 0
    billnumber:int = 0
    doit:bool = False
    posted_flag:bool = False
    queasy = h_bill = None

    order_list = order_item = orderhdr = None

    order_list_list, Order_list = create_model("Order_list", {"table_nr":int, "pax":int, "order_nr":int, "guest_name":str, "room_no":str, "order_date":str, "posted":bool, "guest_nr":int, "resnr":int, "reslinnr":int, "sessionprm":str, "billrecid":int})
    order_item_list, Order_item = create_model("Order_item", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":str, "qty":int, "sp_req":str, "confirm":bool, "remarks":str, "order_date":str, "art_nr":int, "posted":bool})

    Orderhdr = Order_list
    orderhdr_list = order_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal order_list_list, order_item_list, mess_str, i_str, mess_token, mess_keyword, mess_value, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, billnumber, doit, posted_flag, queasy, h_bill
        nonlocal orderhdr


        nonlocal order_list, order_item, orderhdr
        nonlocal order_list_list, order_item_list
        return {"order-list": order_list_list, "order-item": order_item_list}


    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 225) &  (Queasy.number1 == dept) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.logi1)).all():
        mess_str = queasy.char2
        for i_str in range(1,num_entries(mess_str, "|")  + 1) :
            mess_token = entry(i_str - 1, mess_str, "|")
            mess_keyword = entry(0, mess_token, " == ")
            mess_value = entry(1, mess_token, " == ")

            if mess_keyword.lower()  == "RN":
                room = mess_value

            elif mess_keyword.lower()  == "PX":
                pax = to_int(mess_value)

            elif mess_keyword.lower()  == "NM":
                gname = mess_value

            elif mess_keyword.lower()  == "DT":
                orderdatetime = mess_value

            elif mess_keyword.lower()  == "GN":
                gastnr = to_int(mess_value)

            elif mess_keyword.lower()  == "RS":
                resnr = to_int(mess_value)

            elif mess_keyword.lower()  == "RL":
                reslinnr = to_int(mess_value)

            elif mess_keyword.lower()  == "BL":
                billnumber = to_int(mess_value)

        if billnumber != 0:

            h_bill = db_session.query(H_bill).filter(
                    (H_bill.rechnr == billnumber) &  (H_bill.departement == dept)).first()

            if h_bill and h_bill.flag == 0:
                doit = True

                if doit:
                    order_list = Order_list()
                    order_list_list.append(order_list)

                    order_list.table_nr = queasy.number2
                    order_list.pax = pax
                    order_list.order_nr = queasy.number3
                    order_list.guest_name = gname
                    order_list.room_no = room
                    order_list.order_date = orderdatetime
                    order_list.guest_nr = gastnr
                    order_list.resnr = resnr
                    order_list.reslinnr = reslinnr
                    order_list.sessionprm = queasy.char3
                    order_list.posted = queasy.logi3
                    order_list.billrecid = queasy.betriebsnr


                doit = False
        else:
            order_list = Order_list()
            order_list_list.append(order_list)

            order_list.table_nr = queasy.number2
            order_list.pax = pax
            order_list.order_nr = queasy.number3
            order_list.guest_name = gname
            order_list.room_no = room
            order_list.order_date = orderdatetime
            order_list.guest_nr = gastnr
            order_list.resnr = resnr
            order_list.reslinnr = reslinnr
            order_list.sessionprm = queasy.char3
            order_list.posted = queasy.logi3
            order_list.billrecid = queasy.betriebsnr


        room = ""
        pax = 0
        gname = ""
        orderdatetime = ""
        gastnr = 0
        resnr = 0
        reslinnr = 0
        billnumber = 0

    order_list = query(order_list_list, first=True)

    if order_list:

        for order_list in query(order_list_list):

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 225) &  (func.lower(Queasy.char1) == "orderbill_line") &  (Queasy.number2 == order_list.table_nr) &  (Queasy.number1 == order_list.order_nr) &  (entry(2, Queasy.char2, "|Queasy.") == order_list.order_date)).all():
                mess_str = queasy.char3
                order_item = Order_item()
                order_item_list.append(order_item)

                order_item.table_nr = order_list.table_nr
                order_item.order_nr = order_list.order_nr
                order_item.bezeich = entry(2, mess_str, "|")
                order_item.qty = to_int(entry(3, mess_str, "|"))
                order_item.sp_req = entry(5, mess_str, "|")
                order_item.confirm = queasy.logi2
                order_item.remarks = ""
                order_item.order_date = entry(2, queasy.char2, "|")
                order_item.nr = queasy.number3
                order_item.art_nr = to_int(entry(1, mess_str, "|"))
                order_item.posted = queasy.logi3

    for orderhdr in query(orderhdr_list, filters=(lambda orderhdr :orderhdr.billrecid != 0)):

        order_list = query(order_list_list, filters=(lambda order_list :order_list.sessionprm == orderhdr.sessionprm and order_list.billrecid == 0), first=True)

        if order_list:
            order_list.billrecid = orderhdr.billrecid

    return generate_output()