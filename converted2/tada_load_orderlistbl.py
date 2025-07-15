#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, H_bill

def tada_load_orderlistbl(deptno:int):

    prepare_cache ([Queasy, H_bill])

    order_list_data = []
    order_detail_data = []
    tableno:int = 0
    tada_deptno:int = 0
    vhp_deptno:int = 0
    get_date_str:string = ""
    get_date:date = None
    nr:int = 0
    queasy = h_bill = None

    order_list = order_detail = crd_list = orderhdr = orderline = None

    order_list_data, Order_list = create_model("Order_list", {"outlet_no":int, "order_id":int, "guest_name":string, "guest_email":string, "guest_phone":string, "bill_number":string, "order_date":string, "order_type":string, "status_order":string, "posted":bool, "billrecid":int, "table_no":string, "vhp_bill":int, "courier_mtd":string, "payment":string, "payment_amt":Decimal, "payment_art":int, "allow_completed":bool, "trans_date":date})
    order_detail_data, Order_detail = create_model("Order_detail", {"nr":int, "outlet_no":int, "order_id":int, "bezeich":string, "qty":int, "sp_req":string, "confirm":bool, "remarks":string, "order_date":string, "art_nr":int, "posted":bool, "table_no":string, "payment":string, "payment_amt":Decimal, "payment_art":int})
    crd_list_data, Crd_list = create_model("Crd_list", {"deptno":int, "uname":string, "pass":string, "tada_outlet_id":int})

    Orderhdr = create_buffer("Orderhdr",Queasy)
    Orderline = create_buffer("Orderline",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal order_list_data, order_detail_data, tableno, tada_deptno, vhp_deptno, get_date_str, get_date, nr, queasy, h_bill
        nonlocal deptno
        nonlocal orderhdr, orderline


        nonlocal order_list, order_detail, crd_list, orderhdr, orderline
        nonlocal order_list_data, order_detail_data, crd_list_data

        return {"order-list": order_list_data, "order-detail": order_detail_data}


    vhp_deptno = deptno

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 1)).order_by(Queasy.betriebsnr, Queasy.number2).all():

        if (queasy.number2 == 27 or queasy.number2 == 28 or queasy.number2 == 29 or queasy.number2 == 30):

            if num_entries(queasy.char2, ";") >= 2:
                crd_list = Crd_list()
                crd_list_data.append(crd_list)

                crd_list.deptno = to_int(entry(0, queasy.char2, ";"))
                crd_list.uname = entry(1, queasy.char2, ";")
                crd_list.pass = entry(2, queasy.char2, ";")
                crd_list.tada_outlet_id = to_int(entry(3, queasy.char2, ";"))

        if queasy.number2 == 5:
            tableno = to_int(queasy.char2)

    crd_list = query(crd_list_data, filters=(lambda crd_list: crd_list.deptno == deptno), first=True)

    if crd_list:
        deptno = crd_list.tada_outlet_id

    for orderhdr in db_session.query(Orderhdr).filter(
             (Orderhdr.key == 271) & (Orderhdr.betriebsnr == 1) & (Orderhdr.number1 == deptno)).order_by(Orderhdr._recid).all():
        order_list = Order_list()
        order_list_data.append(order_list)

        order_list.outlet_no = orderhdr.number1
        order_list.order_id = orderhdr.number2
        order_list.guest_name = entry(2, orderhdr.char2, "|").upper()
        order_list.guest_email = entry(4, orderhdr.char2, "|").upper()
        order_list.guest_phone = entry(5, orderhdr.char2, "|").upper()
        order_list.bill_number = entry(3, orderhdr.char2, "|")
        order_list.order_date = entry(0, orderhdr.char2, "|")
        order_list.order_type = entry(0, orderhdr.char1, "|")
        order_list.status_order = entry(1, orderhdr.char1, "|")
        order_list.posted = orderhdr.logi1
        order_list.table_no = entry(1, orderhdr.char2, "|")
        order_list.vhp_bill = orderhdr.number3
        order_list.courier_mtd = entry(2, orderhdr.char1, "|")


        get_date_str = entry(0, order_list.order_date, " ")
        get_date = date_mdy(to_int(entry(1, get_date_str, "-")) , to_int(entry(2, get_date_str, "-")) , to_int(entry(0, get_date_str, "-")))
        order_list.trans_date = get_date

        if order_list.table_no.lower()  == ("null").lower() :
            order_list.table_no = ""

        elif matches(order_list.table_no,r"*room*"):
            order_list.table_no = entry(1, order_list.table_no, " ")
        nr = 0

        for orderline in db_session.query(Orderline).filter(
                 (Orderline.key == 271) & (Orderline.betriebsnr == 2) & (Orderline.number2 == orderhdr.number2)).order_by(Orderline._recid).all():
            nr = nr + 1
            order_detail = Order_detail()
            order_detail_data.append(order_detail)

            order_detail.nr = nr
            order_detail.outlet_no = deptno
            order_detail.order_id = orderline.number2
            order_detail.bezeich = entry(1, orderline.char1, "|").upper()
            order_detail.qty = to_int(entry(0, orderline.char1, "|"))
            order_detail.sp_req = entry(1, orderline.char2, "|").upper()
            order_detail.remarks = entry(2, orderline.char2, "|")
            order_detail.order_date = entry(0, orderline.char2, "|")
            order_detail.art_nr = orderline.number1
            order_detail.posted = orderline.logi1
            order_detail.payment = entry(2, orderline.char1, "|").upper()
            order_detail.payment_amt =  to_decimal(to_decimal(entry(3 , orderline.char1 , "|")) )
            order_detail.payment_art = to_int(entry(4, orderline.char1, "|"))

            if order_detail.sp_req.lower()  == ("null").lower() :
                order_detail.sp_req = ""

    for order_list in query(order_list_data):

        if order_list.status_order.lower()  == ("EXPIRED").lower() :
            order_list_data.remove(order_list)

        elif order_list.status_order.lower()  == ("HAVE_ISSUE").lower() :
            order_list_data.remove(order_list)

        elif order_list.status_order.lower()  == ("NEW").lower()  and order_list.trans_date < get_current_date():
            order_list_data.remove(order_list)

        elif order_list.status_order.lower()  == ("UNPAID").lower() :
            order_list_data.remove(order_list)

        elif order_list.status_order.lower()  == ("COMPLETED").lower() :
            order_list_data.remove(order_list)
        else:

            order_detail = query(order_detail_data, filters=(lambda order_detail: order_detail.order_id == order_list.order_id), first=True)

            if order_detail:
                order_list.payment = order_detail.payment
                order_list.payment_amt =  to_decimal(order_detail.payment_amt)
                order_list.payment_art = order_detail.payment_art

            h_bill = get_cache (H_bill, {"departement": [(eq, vhp_deptno)],"rechnr": [(eq, order_list.vhp_bill)]})

            if h_bill:

                if h_bill.flag == 1:
                    order_list.allow_completed = True
                else:
                    order_list.allow_completed = False

    return generate_output()