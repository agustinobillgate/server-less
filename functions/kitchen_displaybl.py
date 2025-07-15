#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.kitchen_display_getdata_cld_1bl import kitchen_display_getdata_cld_1bl
from models import H_artikel, Wgrpdep, Hoteldpt

def kitchen_displaybl(casetype:int, dept_number:int, kp_number:int):

    prepare_cache ([H_artikel, Wgrpdep, Hoteldpt])

    header_list_data = []
    orderlist_data = []
    summary_list_data = []
    subgrp:int = 0
    qheadrecid:int = 0
    tbno:int = 0
    billno:int = 0
    h_artikel = wgrpdep = hoteldpt = None

    kds_list = summary_artlist = summ_list = header_list = order_list = done_list = summary_list = orderlist = hdr_list = bsumlist = bsummary_list = order = None

    kds_list_data, Kds_list = create_model("Kds_list", {"count_pos":int, "curr_flag":string, "qhead_recid":int, "qline_recid":int, "recid_hbline":int, "bill_no":int, "dept_no":int, "table_no":int, "user_post_id":string, "user_name":string, "artikel_no":int, "artikel_qty":int, "artikel_name":string, "sp_request":string, "post_date":date, "post_time":int, "post_timestr":string, "status_order":string, "void_menu":bool, "remain_qty":int, "dept_name":string, "system_date":date, "served_time":string})
    summary_artlist_data, Summary_artlist = create_model("Summary_artlist", {"artikel_no":int, "artikel_qty":int, "artikel_name":string, "artikel_dept":int, "subgroup_no":int, "subgroup_name":string, "void_menu":bool})
    summ_list_data, Summ_list = create_model("Summ_list", {"artikel_no":int, "artikel_qty":int, "artikel_name":string, "artikel_dept":int, "subgroup_no":int, "subgroup_name":string})
    header_list_data, Header_list = create_model("Header_list", {"rechnr":int, "tablenr":int, "zeit":int, "waiters":string, "datum":date, "rec_id":int, "status_no":int, "dept_no":int, "dept_name":string, "sysdate":date, "sysdatetime":datetime})
    order_list_data, Order_list = create_model("Order_list", {"rechnr":int, "tablenr":int, "zeit":int, "datum":date, "prod":string, "note":string, "qty":int, "flag":bool, "status_no":int, "subgrpno":int, "artno":int, "rec_id":int, "header_recid":int, "sysdate":date, "served_time":string, "dept_no":int})
    done_list_data, Done_list = create_model_like(Summary_artlist)
    summary_list_data, Summary_list = create_model_like(Summary_artlist)
    orderlist_data, Orderlist = create_model_like(Order_list)
    hdr_list_data, Hdr_list = create_model_like(Header_list)

    Bsumlist = Summary_artlist
    bsumlist_data = summary_artlist_data

    Bsummary_list = Summary_artlist
    bsummary_list_data = summary_artlist_data

    Order = Order_list
    order_data = order_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal header_list_data, orderlist_data, summary_list_data, subgrp, qheadrecid, tbno, billno, h_artikel, wgrpdep, hoteldpt
        nonlocal casetype, dept_number, kp_number
        nonlocal bsumlist, bsummary_list, order


        nonlocal kds_list, summary_artlist, summ_list, header_list, order_list, done_list, summary_list, orderlist, hdr_list, bsumlist, bsummary_list, order
        nonlocal kds_list_data, summary_artlist_data, summ_list_data, header_list_data, order_list_data, done_list_data, summary_list_data, orderlist_data, hdr_list_data

        return {"header-list": header_list_data, "orderlist": orderlist_data, "summary-list": summary_list_data}


    kds_list_data, summary_artlist_data, done_list_data = get_output(kitchen_display_getdata_cld_1bl(1, kp_number))

    for bsummary_list in query(bsummary_list_data, filters=(lambda bsummary_list: bsummary_list.void_menu == False), sort_by=[("subgroup_name",False)]):

        if subgrp != bsummary_list.subgroup_no:
            subgrp = bsummary_list.subgroup_no

        summary_list = query(summary_list_data, filters=(lambda summary_list: summary_list.subgroup_no == subgrp), first=True)

        if not summary_list:
            summary_list = Summary_list()
            summary_list_data.append(summary_list)

            summary_list.artikel_name = bsummary_list.subgroup_name.upper()

        for bsumlist in query(bsumlist_data, filters=(lambda bsumlist: bsumlist.subgroup_no == subgrp and bsumlist.void_menu == False), sort_by=[("artikel_qty",True)]):

            summary_list = query(summary_list_data, filters=(lambda summary_list: summary_list.artikel_no == bsumlist.artikel_no), first=True)

            if not summary_list:
                summary_list = Summary_list()
                summary_list_data.append(summary_list)

                buffer_copy(bsumlist, summary_list)

    for kds_list in query(kds_list_data):

        if kds_list.curr_flag.lower()  == ("kds-header").lower() :
            header_list = Header_list()
            header_list_data.append(header_list)

            header_list.rechnr = kds_list.bill_no
            header_list.tablenr = kds_list.table_no
            header_list.zeit = kds_list.post_time
            header_list.waiters = kds_list.user_name
            header_list.datum = kds_list.post_date
            header_list.rec_id = kds_list.qhead_recid
            header_list.dept_no = kds_list.dept_no
            header_list.dept_name = kds_list.dept_name
            header_list.sysdate = kds_list.system_date

            if kds_list.status_order.lower()  == ("NEW").lower() :
                header_list.status_no = 0

            elif kds_list.status_order.lower()  == ("COOKING").lower() :
                header_list.status_no = 1

            elif kds_list.status_order.lower()  == ("DONE").lower() :
                header_list.status_no = 2

            elif kds_list.status_order.lower()  == ("SERVED").lower() :
                header_list.status_no = 3

            elif kds_list.status_order.lower()  == ("SERVEDBYSYSTEM").lower() :
                header_list.status_no = 4

        elif kds_list.curr_flag.lower()  == ("kds-line").lower() :
            order_list = Order_list()
            order_list_data.append(order_list)

            order_list.rechnr = kds_list.bill_no
            order_list.tablenr = kds_list.table_no
            order_list.zeit = kds_list.post_time
            order_list.datum = kds_list.post_date
            order_list.prod = kds_list.artikel_name
            order_list.note = kds_list.sp_request
            order_list.qty = kds_list.artikel_qty
            order_list.flag = False
            order_list.artno = kds_list.artikel_no
            order_list.rec_id = kds_list.qline_recid
            order_list.header_recid = kds_list.qhead_recid
            order_list.sysdate = kds_list.system_date
            order_list.served_time = kds_list.served_time
            order_list.dept_no = kds_list.dept_no

            if kds_list.status_order.lower()  == ("NEW").lower() :
                order_list.status_no = 0

            elif kds_list.status_order.lower()  == ("COOKING").lower() :
                order_list.status_no = 1

            elif kds_list.status_order.lower()  == ("DONE").lower() :
                order_list.status_no = 2

            elif kds_list.status_order.lower()  == ("SERVED").lower() :
                order_list.status_no = 3

            elif kds_list.status_order.lower()  == ("SERVEDBYSYSTEM").lower() :
                order_list.status_no = 4

            h_artikel = get_cache (H_artikel, {"departement": [(eq, kds_list.dept_no)],"artnr": [(eq, order_list.artno)],"bondruckernr[0]": [(eq, kp_number)]})

            if h_artikel:
                order_list.subgrpno = h_artikel.zwkum
    subgrp = 0
    billno = 0
    tbno = 0

    for order_list in query(order_list_data, sort_by=[("subgrp",False),("status_no",False)]):

        if subgrp != order_list.subgrpno:
            billno = order_list.rechnr
            tbno = order_list.tablenr
            subgrp = order_list.subgrpno

        orderlist = query(orderlist_data, filters=(lambda orderlist: orderlist.header_recid == order_list.header_recid and orderlist.subgrp == subgrp), first=True)

        if not orderlist:

            wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, order_list.dept_no)],"zknr": [(eq, subgrp)]})
            orderlist = Orderlist()
            orderlist_data.append(orderlist)

            orderlist.prod = wgrpdep.bezeich.upper()
            orderlist.subgrpno = wgrpdep.zknr
            orderlist.flag = True
            orderlist.rechnr = billno
            orderlist.header_recid = order_list.header_recid
            orderlist.note = ""
        orderlist = Orderlist()
        orderlist_data.append(orderlist)

        buffer_copy(order_list, orderlist)
        order_list_data.remove(order_list)

    for header_list in query(header_list_data, sort_by=[("sysdate",True),("zeit",False)]):

        orderlist = query(orderlist_data, filters=(lambda orderlist: orderlist.header_recid == header_list.rec_id and orderlist.artno != 0), first=True)

        if orderlist:
            header_list.sysdate = orderlist.sysdate

        if header_list.dept_name == "":

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, header_list.dept_no)]})

            if hoteldpt:
                header_list.dept_name = hoteldpt.depart
        hdr_list = Hdr_list()
        hdr_list_data.append(hdr_list)

        buffer_copy(header_list, hdr_list)
        hdr_list.sysdatetime = to_datetime(to_string(hdr_list.sysdate) + " " + to_string(hdr_list.zeit, "HH:MM"))
    header_list_data.clear()

    for hdr_list in query(hdr_list_data, sort_by=[("sysdatetime",False)]):
        header_list = Header_list()
        header_list_data.append(header_list)

        buffer_copy(hdr_list, header_list)

    return generate_output()