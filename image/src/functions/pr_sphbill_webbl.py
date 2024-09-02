from functions.additional_functions import *
import decimal
from functions.pr_sphbill1_lnlbl import pr_sphbill1_lnlbl
import re
from models import Printer

def pr_sphbill_webbl(pvilanguage:int, user_init:str, print_all:bool, printnr:int, hbrecid:int, use_h_queasy:bool, bill_nr:int):
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
    pax:str = ""
    counter:int = 0
    gs:str = ""
    pay_str:str = ""
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
    printer = None

    t_print_head = t_print_line = output_list2 = t_printer = print_list = paylist = None

    t_print_head_list, T_print_head = create_model("T_print_head", {"str_date":str, "str_time":str, "bill_no":str, "resto_name":str, "table_usr_id":str, "curr_time":str}, {"str_date": "", "str_time": "", "bill_no": "", "resto_name": "", "table_usr_id": "", "curr_time": ""})
    t_print_line_list, T_print_line = create_model("T_print_line", {"str_qty":str, "descrip":str, "str_price":str, "foot_note1":str, "foot_note2":str}, {"str_qty": "", "descrip": "", "str_price": "", "foot_note1": "", "foot_note2": ""})
    output_list2_list, Output_list2 = create_model("Output_list2", {"str":str, "str_pos":int, "pos":int, "flag_popup":bool, "npause":int, "sort_i":int})
    t_printer_list, T_printer = create_model_like(Printer)

    Print_list = Output_list2
    print_list_list = output_list2_list

    Paylist = Output_list2
    paylist_list = output_list2_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_no, guest_name, t_print_head_list, t_print_line_list, lvcarea, session_parameter, winprinterflag, filename, table_no, usr_id, pax, counter, gs, pay_str, pay_amount, curr_amount, curr_pay, rechnr_str, flag_change, flag_pay, flag_vat, foot_note, guest_addr, guest_addr1, count_i, gs_1, printer
        nonlocal print_list, paylist


        nonlocal t_print_head, t_print_line, output_list2, t_printer, print_list, paylist
        nonlocal t_print_head_list, t_print_line_list, output_list2_list, t_printer_list
        return {"msg_str": msg_str, "room_no": room_no, "guest_name": guest_name, "t-print-head": t_print_head_list, "t-print-line": t_print_line_list}

    print_all, winprinterflag, filename, msg_str, output_list2_list, t_printer_list = get_output(pr_sphbill1_lnlbl(pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, bill_nr, print_all))

    if msg_str != "":

        return generate_output()
    t_print_head = T_print_head()
    t_print_head_list.append(t_print_head)


    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 1), first=True)

    if not print_list:
        msg_str = translateExtended ("No Data Available.", lvcarea, "")

        return generate_output()
    else:
        t_print_head.str_date = trim(substring(print_list.str, 5, 8))
        t_print_head.str_time = trim(substring(print_list.str, 14, 5))
        t_print_head.bill_no = trim(substring(print_list.str, 27, 10))
        t_print_head.curr_time = to_string(get_current_time_in_seconds(), "HH:MM:SS")
        rechnr_str = t_print_head.bill_no

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 2), first=True)

    if print_list:
        t_print_head.resto_name = trim(print_list.str)

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 3), first=True)

    if print_list:
        table_no = trim(substring(print_list.str, 10, 5))
        pax = trim(substring(print_list.str, 16, 13))
        usr_id = trim(substring(print_list.str, 29, 32))
        t_print_head.table_usr_id = translateExtended ("Table", lvcarea, "") + " " + table_no + " / " + pax + " " + usr_id.upper()

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

        t_print_line.descrip = trim(substring(print_list.str, 0, 20))
        t_print_line.str_price = trim(substring(print_list.str, 30, 19))


    t_print_line = T_print_line()
    t_print_line_list.append(t_print_line)

    t_print_line.descrip = fill("-", 42)
    t_print_line.str_price = fill("-", 19)

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 12 and re.match(".*Service.*",print_list.str)), first=True)

    if print_list:
        flag_vat = True
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(substring(print_list.str, 5, 25)) , lvcarea, "")
        t_print_line.str_price = trim(substring(print_list.str, 30, 19))

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 12 and re.match(".*gov.*",print_list.str)), first=True)

    if print_list:
        flag_vat = True
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(substring(print_list.str, 5, 25)) , lvcarea, "")
        t_print_line.str_price = trim(substring(print_list.str, 30, 19))

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


        t_print_line.str_price = trim(substring(print_list.str, 30, 19))

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 18), first=True)

    if print_list:
        gs = trim(substring(print_list.str, 1, 30))
        gs_1 = substring(print_list.str, 1, 30)
        guest_addr = trim(substring(print_list.str, 32, 48))
        guest_addr1 = substring(print_list.str, 32, 48)
        guest_name = gs

        if guest_name == None:
            guest_name = ""

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 14), first=True)

    if print_list:
        flag_pay = True

        for paylist in query(paylist_list, filters=(lambda paylist :paylist.str_pos == 14)):

            if gs != "":

                if guest_addr == "":

                    if paylist.str MATCHES '*' + gs + '*':
                        pay_str = trim(substring(paylist.str, len(gs) + 3 - 1, 36))
                        curr_pay = pay_str
                        curr_amount = trim(substring(paylist.str, len(gs) + 2 - 1, len(paylist.str)))
                        count_i = num_entries(curr_amount, "-")
                        pay_amount = "-" + trim(entry(count_i - 1, curr_amount, "-"))
                        pay_str = replace_str(pay_str, "-", "")
                        t_print_line = T_print_line()
                        t_print_line_list.append(t_print_line)

                        t_print_line.descrip = translateExtended (trim(pay_str) , lvcarea, "")
                        t_print_line.str_price = trim(pay_amount)


                    else:
                        pay_str = trim(substring(paylist.str, 5, 24))
                        curr_pay = pay_str
                        pay_amount = trim(substring(paylist.str, 30, 19))
                        pay_str = replace_str(pay_str, "-", "")
                        t_print_line = T_print_line()
                        t_print_line_list.append(t_print_line)

                        t_print_line.descrip = translateExtended (trim(pay_str) , lvcarea, "")
                        t_print_line.str_price = trim(pay_amount)


                else:

                    if paylist.str MATCHES '*' + gs + '*':
                        pay_str = trim(substring(paylist.str, len(gs_1) + len(guest_addr1) + 3 - 1, 30))
                        curr_amount = trim(substring(paylist.str, len(gs) + 2 - 1, len(paylist.str)))
                        count_i = num_entries(curr_amount, "-")
                        pay_amount = "-" + trim(entry(count_i - 1, curr_amount, "-"))
                        pay_str = replace_str(pay_str, "-", "")
                        t_print_line = T_print_line()
                        t_print_line_list.append(t_print_line)

                        t_print_line.descrip = translateExtended (trim(pay_str) , lvcarea, "")
                        t_print_line.str_price = trim(pay_amount)


                    else:
                        pay_str = trim(substring(paylist.str, 5, 24))
                        curr_pay = pay_str
                        pay_amount = trim(substring(paylist.str, 30, 19))
                        pay_str = replace_str(pay_str, "-", "")
                        t_print_line = T_print_line()
                        t_print_line_list.append(t_print_line)

                        t_print_line.descrip = translateExtended (trim(pay_str) , lvcarea, "")
                        t_print_line.str_price = trim(pay_amount)


            else:

                if not re.match(".*Cash Rp(Change).*",paylist.str):
                    pay_str = trim(substring(paylist.str, 5, 24))
                    curr_pay = pay_str
                    pay_amount = trim(substring(paylist.str, 30, 19))
                    pay_str = replace_str(pay_str, "-", "")
                    t_print_line = T_print_line()
                    t_print_line_list.append(t_print_line)

                    t_print_line.descrip = translateExtended (trim(pay_str) , lvcarea, "")
                    t_print_line.str_price = trim(pay_amount)

    print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 16), first=True)

    if print_list:
        flag_change = True
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = fill("-", 42)
        t_print_line.str_price = fill("-", 19)
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(substring(print_list.str, 5, 25)) , lvcarea, "")
        t_print_line.str_price = trim(substring(print_list.str, 30, 19))


    else:

        for paylist in query(paylist_list, filters=(lambda paylist :paylist.str_pos == 14)):

            if gs != "":

                if not paylist.str MATCHES '*' + gs + '*':
                    pay_str = trim(substring(paylist.str, 5, 24))
                    pay_amount = trim(substring(paylist.str, 30, 19))
            else:

                if re.match(".*Cash Rp(Change).*",paylist.str):
                    pay_str = trim(substring(paylist.str, 5, 24))
                    pay_amount = trim(substring(paylist.str, 30, 19))
            pay_str = replace_str(pay_str, "-", "")

        if re.match(".*Cash Rp(Change).*",pay_str):
            t_print_line = T_print_line()
            t_print_line_list.append(t_print_line)

            t_print_line.descrip = translateExtended (trim(pay_str) , lvcarea, "")
            t_print_line.str_price = trim(pay_amount)


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


        if flag_change or not flag_pay:
            t_print_line.descrip = ""
            t_print_line.str_price = ""


        else:
            t_print_line.descrip = translateExtended (trim(substring(print_list.str, 5, 25)) , lvcarea, "")
            t_print_line.str_price = trim(substring(print_list.str, 30, 19))


    else:
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)


        if flag_change or not flag_pay:
            t_print_line.descrip = ""
            t_print_line.str_price = ""


        else:
            t_print_line.descrip = translateExtended ("BALANCE", lvcarea, "")

            print_list = query(print_list_list, filters=(lambda print_list :print_list.str_pos == 13), first=True)

            if print_list:
                t_print_line.str_price = trim(substring(print_list.str, 30, 19))

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

    return generate_output()