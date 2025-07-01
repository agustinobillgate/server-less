#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, H_bill

input_list_list, Input_list = create_model("Input_list", {"dept":int, "search_type":int, "table_nr":int, "order_nr":int, "order_date":string, "sessionprm":string})

def pos_dashboard_postedorder_list_webbl(input_list_list:[Input_list]):

    prepare_cache ([Queasy, H_bill])

    order_list_list = []
    order_item_list = []
    mess_str:string = ""
    queasy = h_bill = None

    input_list = order_list = order_item = b_queasy = qbill_line = orderhdr = None

    order_list_list, Order_list = create_model("Order_list", {"table_nr":int, "pax":int, "order_nr":int, "guest_name":string, "room_no":string, "order_date":string, "posted":bool, "guest_nr":int, "resnr":int, "reslinnr":int, "sessionprm":string, "billrecid":int})
    order_item_list, Order_item = create_model("Order_item", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":string, "qty":int, "sp_req":string, "confirm":bool, "remarks":string, "order_date":string, "art_nr":int, "posted":bool})

    B_queasy = create_buffer("B_queasy",Queasy)
    Qbill_line = create_buffer("Qbill_line",Queasy)
    Orderhdr = Order_list
    orderhdr_list = order_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal order_list_list, order_item_list, mess_str, queasy, h_bill
        nonlocal b_queasy, qbill_line, orderhdr


        nonlocal input_list, order_list, order_item, b_queasy, qbill_line, orderhdr
        nonlocal order_list_list, order_item_list

        return {"order-list": order_list_list, "order-item": order_item_list}

    def create_list():

        nonlocal order_list_list, order_item_list, mess_str, queasy, h_bill
        nonlocal b_queasy, qbill_line, orderhdr


        nonlocal input_list, order_list, order_item, b_queasy, qbill_line, orderhdr
        nonlocal order_list_list, order_item_list

        i_str:int = 0
        mess_token:string = ""
        mess_keyword:string = ""
        mess_value:string = ""
        pax:int = 0
        orderdatetime:string = ""
        gname:string = ""
        room:string = ""
        gastnr:int = 0
        resnr:int = 0
        reslinnr:int = 0
        billnumber:int = 0
        doit:bool = False
        posted_flag:bool = False

        queasy = get_cache (Queasy, {"key": [(eq, 225)],"number1": [(eq, input_list.dept)],"logi1": [(eq, True)],"char1": [(eq, "orderbill")],"logi3": [(eq, True)]})
        while None != queasy:
            mess_str = queasy.char2
            for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                mess_token = entry(i_str - 1, mess_str, "|")
                mess_keyword = entry(0, mess_token, "=")
                mess_value = entry(1, mess_token, "=")

                if mess_keyword.lower()  == ("RN").lower() :
                    room = mess_value

                elif mess_keyword.lower()  == ("PX").lower() :
                    pax = to_int(mess_value)

                elif mess_keyword.lower()  == ("NM").lower() :
                    gname = mess_value

                elif mess_keyword.lower()  == ("DT").lower() :
                    orderdatetime = mess_value

                elif mess_keyword.lower()  == ("GN").lower() :
                    gastnr = to_int(mess_value)

                elif mess_keyword.lower()  == ("RS").lower() :
                    resnr = to_int(mess_value)

                elif mess_keyword.lower()  == ("RL").lower() :
                    reslinnr = to_int(mess_value)

                elif mess_keyword.lower()  == ("BL").lower() :
                    billnumber = to_int(mess_value)

            if billnumber != 0 or queasy.betriebsnr != 0:

                h_bill = get_cache (H_bill, {"rechnr": [(eq, billnumber)],"departement": [(eq, input_list.dept)]})

                if not h_bill:

                    h_bill = get_cache (H_bill, {"_recid": [(eq, queasy.betriebsnr)]})

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

            qbill_line = db_session.query(Qbill_line).filter(
                     (Qbill_line.key == 225) & (Qbill_line.char1 == ("orderbill-line").lower()) & (Qbill_line.number2 == queasy.number2) & (Qbill_line.number1 == queasy.number3) & (to_int(entry(0, Qbill_line.char2, "|")) == input_list.dept) & (entry(2, Qbill_line.char2, "|") == (orderdatetime).lower()) & (entry(3, Qbill_line.char2, "|") == queasy.char3) & (Qbill_line.logi2)).first()

            if qbill_line:

                b_queasy = get_cache (Queasy, {"key": [(eq, 225)],"number1": [(eq, input_list.dept)],"char1": [(eq, "orderbill")],"betriebsnr": [(eq, queasy.betriebsnr)],"number3": [(eq, queasy.number3)],"number2": [(eq, queasy.number2)],"char3": [(eq, queasy.char3)]})

                if b_queasy:
                    b_queasy.logi3 = True
                    order_list.posted = True
                    pass
                    pass
            room = ""
            pax = 0
            gname = ""
            orderdatetime = ""
            gastnr = 0
            resnr = 0
            reslinnr = 0
            billnumber = 0

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 225) & (Queasy.number1 == input_list.dept) & (Queasy.logi1) & (Queasy.char1 == ("orderbill").lower()) & (Queasy.logi3) & (Queasy._recid > curr_recid)).first()

        for orderhdr in query(orderhdr_list, filters=(lambda orderhdr: orderhdr.billrecid != 0)):

            order_list = query(order_list_list, filters=(lambda order_list: order_list.sessionprm == orderhdr.sessionprm and order_list.billrecid == 0), first=True)

            if order_list:
                order_list.billrecid = orderhdr.billrecid


    def create_detail():

        nonlocal order_list_list, order_item_list, mess_str, queasy, h_bill
        nonlocal b_queasy, qbill_line, orderhdr


        nonlocal input_list, order_list, order_item, b_queasy, qbill_line, orderhdr
        nonlocal order_list_list, order_item_list

        for qbill_line in db_session.query(Qbill_line).filter(
                 (Qbill_line.key == 225) & (Qbill_line.char1 == ("orderbill-line").lower()) & (Qbill_line.number2 == input_list.table_nr) & (Qbill_line.number1 == input_list.order_nr) & (entry(3, Qbill_line.char2, "|") == input_list.sessionprm) & (entry(2, Qbill_line.char2, "|") == input_list.order_date) & (to_int(entry(0, Qbill_line.char2, "|")) == input_list.dept)).order_by(Qbill_line._recid).all():
            mess_str = qbill_line.char3
            order_item = Order_item()
            order_item_list.append(order_item)

            order_item.table_nr = qbill_line.number2
            order_item.order_nr = qbill_line.number1
            order_item.bezeich = entry(2, mess_str, "|")
            order_item.qty = to_int(entry(3, mess_str, "|"))
            order_item.sp_req = entry(5, mess_str, "|")
            order_item.confirm = qbill_line.logi2
            order_item.remarks = ""
            order_item.order_date = entry(2, qbill_line.char2, "|")
            order_item.nr = qbill_line.number3
            order_item.art_nr = to_int(entry(1, mess_str, "|"))
            order_item.posted = qbill_line.logi3


    input_list = query(input_list_list, first=True)

    if not input_list:

        return generate_output()

    if input_list.search_type == 1:
        create_list()

    elif input_list.search_type == 2:
        create_detail()

    return generate_output()