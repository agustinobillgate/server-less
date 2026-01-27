#using conversion tools version: 1.0.0.119
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added

# Rulita, 14-01-2026
# Added fitur Sub Menu
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from functions.print_hbilllnl_cldbl import print_hbilllnl_cldbl
from sqlalchemy import func
from models import Printer, Queasy, Htparam, Artikel, Wgrpgen, H_artikel, Bill, Bill_line, H_bill

def print_hbill_webbl(pvilanguage:int, user_init:string, print_all:bool, printnr:int, hbrecid:int, use_h_queasy:bool):

    prepare_cache ([Queasy, Htparam, Artikel, Wgrpgen, H_artikel, Bill, Bill_line, H_bill])

    msg_str = ""
    room_no = ""
    guest_name = ""
    t_print_head_data = []
    t_print_line_data = []
    lvcarea:string = "print-hbill1"
    session_parameter:string = ""
    winprinterflag:bool = False
    filename:string = ""
    table_no:string = ""
    usr_id:string = ""
    counter:int = 0
    gs:string = ""
    pay_str:string = ""
    depopay_str:string = ""
    pay_amount:string = ""
    curr_amount:string = ""
    curr_pay:string = ""
    rechnr_str:string = ""
    flag_change:bool = False
    flag_pay:bool = False
    flag_vat:bool = False
    foot_note:string = ""
    curr_footnote:string = ""
    guest_addr:string = ""
    guest_addr1:string = ""
    count_i:int = 0
    gs_1:string = ""
    fo_depoart:int = 0
    fo_depobez:string = ""
    fb_depoart:int = 0
    fb_depobez:string = ""
    voucher_depo:string = ""
    gastno:int = 0
    ns_billno:int = 0
    curr_dept:int = 0
    str1:string = ""
    printer = queasy = htparam = artikel = wgrpgen = h_artikel = bill = bill_line = h_bill = None

    t_print_head = t_print_line = output_list2 = t_printer = print_list = paylist = q_33 = None

    t_print_head_data, T_print_head = create_model("T_print_head", {"str_date":string, "str_time":string, "bill_no":string, "resto_name":string, "table_usr_id":string, "curr_time":string, "guest_member":string, "od_taker":string, "table_desc":string}, {"str_date": "", "str_time": "", "bill_no": "", "resto_name": "", "table_usr_id": "", "curr_time": "", "guest_member": "", "od_taker": "", "table_desc": ""})
    t_print_line_data, T_print_line = create_model("T_print_line", {"str_qty":string, "descrip":string, "str_price":string, "foot_note1":string, "foot_note2":string, "foot_note3":string, "ismain":bool}, {"str_qty": "", "descrip": "", "str_price": "", "foot_note1": "", "foot_note2": "", "foot_note3": "", "ismain": True})
    output_list2_data, Output_list2 = create_model("Output_list2", {"str":string, "str_pos":int, "pos":int, "flag_popup":bool, "npause":int, "sort_i":int})
    t_printer_data, T_printer = create_model_like(Printer)

    Print_list = Output_list2
    print_list_data = output_list2_data

    Paylist = Output_list2
    paylist_data = output_list2_data

    Q_33 = create_buffer("Q_33",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_no, guest_name, t_print_head_data, t_print_line_data, lvcarea, session_parameter, winprinterflag, filename, table_no, usr_id, counter, gs, pay_str, depopay_str, pay_amount, curr_amount, curr_pay, rechnr_str, flag_change, flag_pay, flag_vat, foot_note, curr_footnote, guest_addr, guest_addr1, count_i, gs_1, fo_depoart, fo_depobez, fb_depoart, fb_depobez, voucher_depo, gastno, ns_billno, curr_dept, str1, printer, queasy, htparam, artikel, wgrpgen, h_artikel, bill, bill_line, h_bill
        nonlocal pvilanguage, user_init, print_all, printnr, hbrecid, use_h_queasy
        nonlocal print_list, paylist, q_33


        nonlocal t_print_head, t_print_line, output_list2, t_printer, print_list, paylist, q_33
        nonlocal t_print_head_data, t_print_line_data, output_list2_data, t_printer_data

        return {"msg_str": msg_str, "room_no": room_no, "guest_name": guest_name, "t-print-head": t_print_head_data, "t-print-line": t_print_line_data}

    print_all, filename, msg_str, winprinterflag, output_list2_data, t_printer_data = get_output(print_hbilllnl_cldbl(pvilanguage, session_parameter, user_init, hbrecid, printnr, use_h_queasy, print_all))

    if msg_str != "":

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if artikel:
            fo_depoart = artikel.artnr
            fo_depobez = artikel.bezeich

    wgrpgen = db_session.query(Wgrpgen).filter(
             (matches(Wgrpgen.bezeich,"*deposit*"))).first()

    if wgrpgen:

        h_artikel = db_session.query(H_artikel).filter(
                 (H_artikel.endkum == wgrpgen.eknr) & (H_artikel.activeflag)).first()

        if h_artikel:
            fb_depoart = h_artikel.artnr
            fb_depobez = h_artikel.bezeich

    queasy = get_cache (Queasy, {"key": [(eq, 251)],"number1": [(eq, hbrecid)]})

    if queasy:

        q_33 = get_cache (Queasy, {"_recid": [(eq, queasy.number2)]})

        if q_33:
            ns_billno = to_int(q_33.deci2)
            gastno = to_int(entry(2, q_33.char2, "&&"))
            curr_dept = q_33.number1

            bill = get_cache (Bill, {"rechnr": [(eq, ns_billno)],"gastnr": [(eq, gastno)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"billtyp": [(eq, curr_dept)],"flag": [(eq, 1)]})

            if bill:

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(eq, fo_depoart)]})

                if bill_line:
                    str1 = entry(0, bill_line.bezeich, "[")
                    voucher_depo = trim(entry(1, str1, "/"))
    t_print_head = T_print_head()
    t_print_head_data.append(t_print_head)


    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 1), first=True)

    if not print_list:
        msg_str = translateExtended ("No Data Available.", lvcarea, "")

        return generate_output()
    else:
        t_print_head.str_date = trim(entry(0, print_list.str, "|"))
        t_print_head.str_time = trim(entry(1, print_list.str, "|"))
        t_print_head.bill_no = trim(entry(3, print_list.str, "|"))
        t_print_head.curr_time = to_string(get_current_time_in_seconds(), "HH:MM:SS")
        rechnr_str = t_print_head.bill_no

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 2), first=True)

    if print_list:
        t_print_head.resto_name = print_list.str

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 3), first=True)

    if print_list:
        table_no = trim(entry(1, print_list.str, "|"))
        usr_id = trim(entry(2, print_list.str, "|")) + " " + trim(entry(3, print_list.str, "|"))

        if trim(entry(4, print_list.str, "|")) != "":
            t_print_head.od_taker = trim(entry(4, print_list.str, "|"))

        if trim(entry(5, print_list.str, "|")) != "":
            t_print_head.table_desc = trim(entry(5, print_list.str, "|"))
        t_print_head.table_usr_id = translateExtended (t_print_head.table_desc, lvcarea, "") + " / " + usr_id.upper()

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 8), first=True)

    if print_list:
        t_print_head.guest_member = trim(print_list.str)

    for print_list in query(print_list_data, filters=(lambda print_list: print_list.str_pos == 10)):
        t_print_line = T_print_line()
        t_print_line_data.append(t_print_line)

        t_print_line.str_qty = trim(entry(0, print_list.str, "|"))
        t_print_line.descrip = trim(entry(1, print_list.str, "|"))
        t_print_line.str_price = trim(entry(2, print_list.str, "|"))

        if trim(entry(3, print_list.str, "|")) == ("1").lower() :
            t_print_line.ismain = True

        elif trim(entry(3, print_list.str, "|")) == ("2").lower() :
            t_print_line.ismain = False

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 11), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_data.append(t_print_line)

        t_print_line.descrip = trim(entry(0, print_list.str, "|"))
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))


    t_print_line = T_print_line()
    t_print_line_data.append(t_print_line)

    t_print_line.descrip = fill("-", 42)
    t_print_line.str_price = fill("-", 19)

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 12 and matches(print_list.str,r"*Service*")), first=True)

    if print_list:
        flag_vat = True
        t_print_line = T_print_line()
        t_print_line_data.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 12 and matches(print_list.str,r"*gov*")), first=True)

    if print_list:
        flag_vat = True
        t_print_line = T_print_line()
        t_print_line_data.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    if flag_vat:
        t_print_line = T_print_line()
        t_print_line_data.append(t_print_line)

        t_print_line.descrip = fill("-", 42)
        t_print_line.str_price = fill("-", 19)

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 13), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_data.append(t_print_line)

        t_print_line.descrip = translateExtended ("TOTAL", lvcarea, "")


        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 18), first=True)

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

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 14), first=True)

    if print_list:
        flag_pay = True

        for paylist in query(paylist_data, filters=(lambda paylist: paylist.str_pos == 14)):
            t_print_line = T_print_line()
            t_print_line_data.append(t_print_line)


            if gs != "":

                if matches(paylist.str,'*' + gs + '*'):

                    if (gs.lower()  == ("Compl").lower()  or gs.lower()  == ("Compliment").lower()  or gs.lower()  == ("A&G").lower()  or gs.lower()  == ("Eng").lower()  or gs.lower()  == ("FB").lower()  or gs.lower()  == ("FO").lower()  or gs.lower()  == ("HK").lower()  or gs.lower()  == ("HRD").lower()  or gs.lower()  == ("Owner").lower()  or gs.lower()  == ("Sales").lower()) and (matches(paylist.str,("*Compliment*")) or matches(paylist.str,r"*Compl*") or matches(paylist.str,r"*Entertaint*") or matches(paylist.str,r"*Officer Check*")):
                        t_print_line.descrip = trim(substring(translateExtended (entry(0, paylist.str, "|") , lvcarea, "") , length(gs) - 1))
                    else:
                        t_print_line.descrip = translateExtended (trim(entry(0, paylist.str, "|")) , lvcarea, "")
                        t_print_line.descrip = trim(substring(t_print_line.descrip, length(gs) + 1 - 1))


                else:
                    t_print_line.descrip = translateExtended (trim(entry(0, paylist.str, "|")) , lvcarea, "")
            else:
                t_print_line.descrip = translateExtended (trim(entry(0, paylist.str, "|")) , lvcarea, "")
            t_print_line.str_price = trim(entry(1, paylist.str, "|"))

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 16), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_data.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))


    gs = ""
    pay_str = ""
    pay_amount = ""

    if not flag_change and flag_pay:
        t_print_line = T_print_line()
        t_print_line_data.append(t_print_line)

        t_print_line.descrip = fill("-", 42)
        t_print_line.str_price = fill("-", 19)

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 15), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_data.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    print_list = query(print_list_data, filters=(lambda print_list: print_list.str_pos == 17), first=True)

    if print_list:

        if num_entries(print_list.str, ":") > 1:
            room_no = trim(entry(1, substring(print_list.str, 5, 25) , ":"))
        else:
            room_no = ""

    for print_list in query(print_list_data, filters=(lambda print_list: print_list.str_pos == 19)):

        if print_list.str == None:
            print_list.str = ""
        print_list.str = replace_str(print_list.str, ";", " ")
        foot_note = foot_note + trim(print_list.str) + ";"
    foot_note = substring(foot_note, 0, length(foot_note) - 1)

    if foot_note != "":
        t_print_line = T_print_line()
        t_print_line_data.append(t_print_line)


        if num_entries(foot_note, ";") <= 1:
            t_print_line.foot_note1 = entry(0, foot_note, ";")

        elif num_entries(foot_note, ";") <= 2:
            t_print_line.foot_note1 = entry(0, foot_note, ";")
            t_print_line.foot_note2 = entry(1, foot_note, ";")

        elif num_entries(foot_note, ";") <= 3:
            t_print_line.foot_note1 = entry(0, foot_note, ";")
            t_print_line.foot_note2 = entry(1, foot_note, ";")
            t_print_line.foot_note3 = entry(2, foot_note, ";")

    # h_bill = get_cache (H_bill, {"_recid": [(eq, hbrecid)]})
    h_bill = db_session.query(H_bill).filter(
             (H_bill._recid == hbrecid)).with_for_update().first()
    h_bill.rgdruck = 1

    return generate_output()