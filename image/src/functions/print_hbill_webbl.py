from functions.additional_functions import *
import decimal
from functions.print_hbilllnl_cldbl import print_hbilllnl_cldbl
import re
from models import Printer, Queasy, Htparam, Artikel, Wgrpgen, H_artikel, Bill, Bill_line, H_bill

def print_hbill_webbl(pvilanguage:int, user_init:str, print_all:bool, printnr:int, hbrecid:int, use_h_queasy:bool):
    msg_str = ""
    room_no = ""
    guest_name = ""
    t_print_head_list = []
    t_print_line_list = []
    lvcarea:str = "print_hbill1"
    session_parameter:str = ""
    winprinterflag:bool = False
    filename:str = ""
    table_no:str = ""
    usr_id:str = ""
    counter:int = 0
    gs:str = ""
    pay_str:str = ""
    depopay_str:str = ""
    pay_amount:str = ""
    curr_amount:str = ""
    curr_pay:str = ""
    rechnr_str:str = ""
    flag_change:bool = False
    flag_pay:bool = False
    flag_vat:bool = False
    foot_note:str = ""
    guest_addr:str = ""
    guest_addr1:str = ""
    count_i:int = 0
    gs_1:str = ""
    fo_depoart:int = 0
    fo_depobez:str = ""
    fb_depoart:int = 0
    fb_depobez:str = ""
    voucher_depo:str = ""
    gastno:int = 0
    ns_billno:int = 0
    curr_dept:int = 0
    str1:str = ""
    printer = queasy = htparam = artikel = wgrpgen = h_artikel = bill = bill_line = h_bill = None

    t_print_head = t_print_line = output_list2 = t_printer = print_list = paylist = q_33 = None

    t_print_head_list, T_print_head = create_model("T_print_head", {"str_date":str, "str_time":str, "bill_no":str, "resto_name":str, "table_usr_id":str, "curr_time":str, "guest_member":str, "od_taker":str}, {"str_date": "", "str_time": "", "bill_no": "", "resto_name": "", "table_usr_id": "", "curr_time": "", "guest_member": "", "od_taker": ""})
    t_print_line_list, T_print_line = create_model("T_print_line", {"str_qty":str, "descrip":str, "str_price":str, "foot_note1":str, "foot_note2":str}, {"str_qty": "", "descrip": "", "str_price": "", "foot_note1": "", "foot_note2": ""})
    output_list2_list, Output_list2 = create_model("Output_list2", {"str":str, "str_pos":int, "pos":int, "flag_popup":bool, "npause":int, "sort_i":int})
    t_printer_list, T_printer = create_model_like(Printer)

    Print_list = Output_list2
    print_list_list = output_list2_list

    Paylist = Output_list2
    paylist_list = output_list2_list

    Q_33 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_no, guest_name, t_print_head_list, t_print_line_list, lvcarea, session_parameter, winprinterflag, filename, table_no, usr_id, counter, gs, pay_str, depopay_str, pay_amount, curr_amount, curr_pay, rechnr_str, flag_change, flag_pay, flag_vat, foot_note, guest_addr, guest_addr1, count_i, gs_1, fo_depoart, fo_depobez, fb_depoart, fb_depobez, voucher_depo, gastno, ns_billno, curr_dept, str1, printer, queasy, htparam, artikel, wgrpgen, h_artikel, bill, bill_line, h_bill
        nonlocal print_list, paylist, q_33


        nonlocal t_print_head, t_print_line, output_list2, t_printer, print_list, paylist, q_33
        nonlocal t_print_head_list, t_print_line_list, output_list2_list, t_printer_list
        return {"msg_str": msg_str, "room_no": room_no, "guest_name": guest_name, "t-print-head": t_print_head_list, "t-print-line": t_print_line_list}

    print_all, filename, msg_str, winprinterflag, output_list2_list, t_printer_list = get_output(print_hbilllnl_cldbl(pvilanguage, session_parameter, user_init, hbrecid, printnr, use_h_queasy, print_all))

    if msg_str != "":

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1361)).first()

    if htparam:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

        if artikel:
            fo_depoart = artikel.artnr
            fo_depobez = artikel.bezeich

    wgrpgen = db_session.query(Wgrpgen).filter(
            (Wgrpgen.bezeich.op("~")(".*deposit.*"))).first()

    if wgrpgen:

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.endkum == wgrpgen.eknr) &  (H_artikel.activeflag)).first()

        if h_artikel:
            fb_depoart = h_artikel.artnr
            fb_depobez = h_artikel.bezeich

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 251) &  (Queasy.number1 == hbrecid)).first()

    if queasy:

        q_33 = db_session.query(Q_33).filter(
                (Q_33._recid == queasy.number2)).first()

        if q_33:
            ns_billno = to_int(q_33.deci2)
            gastno = to_int(entry(2, q_33.char2, "&&"))
            curr_dept = q_33.number1

            bill = db_session.query(Bill).filter(
                    (Bill.rechnr == ns_billno) &  (Bill.gastnr == gastno) &  (Bill.resnr == 0) &  (Bill.reslinnr == 1) &  (Billtyp == curr_dept) &  (Bill.flag == 1)).first()

            if bill:

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.rechnr == bill.rechnr) &  (Bill_line.artnr == fo_depoart)).first()

                if bill_line:
                    str1 = entry(0, bill_line.bezeich, "[")
                    voucher_depo = trim(entry(1, str1, "/"))
    t_print_head = T_print_head()
    t_print_head_list.append(t_print_head)


    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 1), first=True)

    if not print_list:
        msg_str = translateExtended ("No Data Available.", lvcarea, "")

        return generate_output()
    else:
        t_print_head.str_date = trim(entry(0, print_list.str, "|"))
        t_print_head.str_time = trim(entry(1, print_list.str, "|"))
        t_print_head.bill_no = trim(entry(3, print_list.str, "|"))
        t_print_head.curr_time = to_string(get_current_time_in_seconds(), "HH:MM:SS")
        rechnr_str = t_print_head.bill_no

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 2), first=True)

    if print_list:
        t_print_head.resto_name = print_list.str

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 3), first=True)

    if print_list:
        table_no = trim(entry(1, print_list.str, "|"))
        usr_id = trim(entry(2, print_list.str, "|")) + " " + trim(entry(3, print_list.str, "|"))

        if trim(entry(4, print_list.str, "|")) != "":
            t_print_head.od_taker = trim(entry(4, print_list.str, "|"))
        t_print_head.table_usr_id = translateExtended ("Table", lvcarea, "") + " " + table_no + " / " + usr_id.upper()

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 8), first=True)

    if print_list:
        t_print_head.guest_member = trim(print_list.str)

    for print_list in query(print_list_list, filters=(lambda print_list :print_list.str_pos == 10)):
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.str_qty = trim(entry(0, print_list.str, "|"))
        t_print_line.descrip = trim(entry(1, print_list.str, "|"))
        t_print_line.str_price = trim(entry(2, print_list.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 11), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = trim(entry(0, print_list.str, "|"))
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))


    t_print_line = T_print_line()
    t_print_line_list.append(t_print_line)

    t_print_line.descrip = fill("-", 42)
    t_print_line.str_price = fill("-", 19)

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 12 and re.match(".*Service.*",print_list.str)), first=True)

    if print_list:
        flag_vat = True
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 12 and re.match(".*gov.*",print_list.str)), first=True)

    if print_list:
        flag_vat = True
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    if flag_vat:
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = fill("-", 42)
        t_print_line.str_price = fill("-", 19)

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 13), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended ("TOTAL", lvcarea, "")


        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 18), first=True)

    if print_list:
        gs = trim(substring(print_list.str, 1, 64))
        gs_1 = substring(print_list.str, 1, 64)
        guest_addr = trim(substring(print_list.str, 66, 48))
        guest_addr1 = substring(print_list.str, 66, 48)
        guest_name = gs

        if gs == None:
            gs = ""

        if guest_name == None:
            guest_name = ""

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 14), first=True)

    if print_list:
        flag_pay = True

        for paylist in query(paylist_list, filters=(lambda paylist :paylist.str_pos == 14)):
            t_print_line = T_print_line()
            t_print_line_list.append(t_print_line)


            if gs != "":

                if paylist.str MATCHES '*' + gs + '*':
                    t_print_line.descrip = translateExtended (trim(entry(0, paylist.str, "|")) , lvcarea, "")
                    t_print_line.descrip = trim(substring(t_print_line.descrip, len(gs) + 1 - 1))


                else:
                    t_print_line.descrip = translateExtended (trim(entry(0, paylist.str, "|")) , lvcarea, "")
            else:
                t_print_line.descrip = translateExtended (trim(entry(0, paylist.str, "|")) , lvcarea, "")
            t_print_line.str_price = trim(entry(1, paylist.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 16), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))


    gs = ""
    pay_str = ""
    pay_amount = ""

    if not flag_change and flag_pay:
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = fill("-", 42)
        t_print_line.str_price = fill("-", 19)

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 15), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 17), first=True)

    if print_list:

        if num_entries(print_list.str, ":") > 1:
            room_no = trim(entry(1, substring(print_list.str, 5, 25) , ":"))
        else:
            room_no = ""

    for print_list in query(print_list_list, filters=(lambda print_list :print_list.str_pos == 19)):
        foot_note = foot_note + trim(print_list.str) + ";"

    if foot_note != "":
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.foot_note1 = entry(0, foot_note, ";")
        t_print_line.foot_note2 = entry(1, foot_note, ";")

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == hbrecid)).first()

    h_bill = db_session.query(H_bill).first()
    h_bill.rgdruck = 1

    h_bill = db_session.query(H_bill).first()

    return generate_output()