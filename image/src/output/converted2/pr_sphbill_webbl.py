#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.pr_sphbill1_lnlbl import pr_sphbill1_lnlbl
from models import Printer

def pr_sphbill_webbl(pvilanguage:int, user_init:string, print_all:bool, printnr:int, hbrecid:int, use_h_queasy:bool, bill_nr:int):
    msg_str = ""
    room_no = ""
    guest_name = ""
    t_print_head_list = []
    t_print_line_list = []
    lvcarea:string = "print-hbill1"
    session_parameter:string = ""
    winprinterflag:bool = False
    filename:string = ""
    table_no:string = ""
    usr_id:string = ""
    pax:string = ""
    counter:int = 0
    gs:string = ""
    pay_str:string = ""
    pay_amount:string = ""
    curr_amount:string = ""
    curr_pay:string = ""
    rechnr_str:string = ""
    flag_change:bool = False
    flag_pay:bool = False
    flag_vat:bool = False
    foot_note:string = ""
    guest_addr:string = ""
    guest_addr1:string = ""
    count_i:int = 0
    gs_1:string = ""
    split_no:string = ""
    printer = None

    t_print_head = t_print_line = output_list2 = t_printer = print_list = paylist = None

    t_print_head_list, T_print_head = create_model("T_print_head", {"str_date":string, "str_time":string, "bill_no":string, "resto_name":string, "table_usr_id":string, "curr_time":string, "guest_member":string}, {"str_date": "", "str_time": "", "bill_no": "", "resto_name": "", "table_usr_id": "", "curr_time": "", "guest_member": ""})
    t_print_line_list, T_print_line = create_model("T_print_line", {"str_qty":string, "descrip":string, "str_price":string, "foot_note1":string, "foot_note2":string, "foot_note3":string}, {"str_qty": "", "descrip": "", "str_price": "", "foot_note1": "", "foot_note2": "", "foot_note3": ""})
    output_list2_list, Output_list2 = create_model("Output_list2", {"str":string, "str_pos":int, "pos":int, "flag_popup":bool, "npause":int, "sort_i":int})
    t_printer_list, T_printer = create_model_like(Printer)

    Print_list = Output_list2
    print_list_list = output_list2_list

    Paylist = Output_list2
    paylist_list = output_list2_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_no, guest_name, t_print_head_list, t_print_line_list, lvcarea, session_parameter, winprinterflag, filename, table_no, usr_id, pax, counter, gs, pay_str, pay_amount, curr_amount, curr_pay, rechnr_str, flag_change, flag_pay, flag_vat, foot_note, guest_addr, guest_addr1, count_i, gs_1, split_no, printer
        nonlocal pvilanguage, user_init, print_all, printnr, hbrecid, use_h_queasy, bill_nr
        nonlocal print_list, paylist


        nonlocal t_print_head, t_print_line, output_list2, t_printer, print_list, paylist
        nonlocal t_print_head_list, t_print_line_list, output_list2_list, t_printer_list

        return {"msg_str": msg_str, "room_no": room_no, "guest_name": guest_name, "t-print-head": t_print_head_list, "t-print-line": t_print_line_list}

    print_all, winprinterflag, filename, msg_str, output_list2_list, t_printer_list = get_output(pr_sphbill1_lnlbl(pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, bill_nr, print_all))

    if msg_str != "":

        return generate_output()
    t_print_head = T_print_head()
    t_print_head_list.append(t_print_head)


    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 1), first=True)

    if not print_list:
        msg_str = translateExtended ("No Data Available.", lvcarea, "")

        return generate_output()
    else:
        t_print_head.str_date = trim(entry(0, print_list.str, "|"))
        t_print_head.str_time = trim(entry(1, print_list.str, "|"))
        t_print_head.bill_no = trim(entry(3, print_list.str, "|"))
        t_print_head.curr_time = to_string(get_current_time_in_seconds(), "HH:MM:SS")
        rechnr_str = t_print_head.bill_no

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 2), first=True)

    if print_list:
        t_print_head.resto_name = trim(print_list.str)

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 3), first=True)

    if print_list:
        table_no = trim(entry(1, print_list.str, "|"))
        usr_id = trim(entry(2, print_list.str, "|")) + " " + trim(entry(4, print_list.str, "|"))
        split_no = trim(entry(3, print_list.str, "|"))


        t_print_head.table_usr_id = translateExtended ("Table", lvcarea, "") + " " + table_no + "/" + usr_id.upper() + split_no

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 5), first=True)

    if print_list:
        guest_name = trim(entry(1, print_list.str, "|"))


        gs = guest_name

        if num_entries(print_list.str, "|") > 2 and gs != "":
            guest_name = guest_name + " | " + trim(entry(2, print_list.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 8), first=True)

    if print_list:
        t_print_head.guest_member = trim(print_list.str)

    for print_list in query(print_list_list, filters=(lambda print_list: print_list.str_pos == 10)):
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.str_qty = trim(entry(0, print_list.str, "|"))
        t_print_line.descrip = trim(entry(1, print_list.str, "|"))
        t_print_line.str_price = trim(entry(2, print_list.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 11), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = trim(entry(0, print_list.str, "|"))
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))


    t_print_line = T_print_line()
    t_print_line_list.append(t_print_line)

    t_print_line.descrip = fill("-", 42)
    t_print_line.str_price = fill("-", 19)

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 12 and matches(print_list.str,r"*Service*")), first=True)

    if print_list:
        flag_vat = True
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 12 and matches(print_list.str,r"*gov*")), first=True)

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

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 13), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended ("TOTAL", lvcarea, "")


        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 14), first=True)

    if print_list:
        flag_pay = True

        for paylist in query(paylist_list, filters=(lambda paylist: paylist.str_pos == 14)):
            t_print_line = T_print_line()
            t_print_line_list.append(t_print_line)


            if gs != "":

                if matches(paylist.str,'*' + gs + '*'):
                    t_print_line.descrip = translateExtended (trim(entry(0, paylist.str, "|")) , lvcarea, "")
                    t_print_line.descrip = trim(substring(t_print_line.descrip, length(gs) + 1 - 1))


                else:
                    t_print_line.descrip = translateExtended (trim(entry(0, paylist.str, "|")) , lvcarea, "")
            else:
                t_print_line.descrip = translateExtended (trim(entry(0, paylist.str, "|")) , lvcarea, "")
            t_print_line.str_price = trim(entry(1, paylist.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 16), first=True)

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

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 15), first=True)

    if print_list:
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)

        t_print_line.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
        t_print_line.str_price = trim(entry(1, print_list.str, "|"))

    print_list = query(print_list_list, filters=(lambda print_list: print_list.str_pos == 17), first=True)

    if print_list:

        if num_entries(print_list.str, ":") > 1:
            room_no = trim(entry(1, substring(print_list.str, 5, 25) , ":"))
        else:
            room_no = ""

    for print_list in query(print_list_list, filters=(lambda print_list: print_list.str_pos == 19)):

        if print_list.str == None:
            print_list.str = ""
        print_list.str = replace_str(print_list.str, ";", " ")
        foot_note = foot_note + trim(print_list.str) + ";"
    foot_note = substring(foot_note, 0, length(foot_note) - 1)

    if foot_note != "":
        t_print_line = T_print_line()
        t_print_line_list.append(t_print_line)


        if num_entries(foot_note, ";") <= 1:
            t_print_line.foot_note1 = entry(0, foot_note, ";")

        elif num_entries(foot_note, ";") <= 2:
            t_print_line.foot_note1 = entry(0, foot_note, ";")
            t_print_line.foot_note2 = entry(1, foot_note, ";")

        elif num_entries(foot_note, ";") <= 3:
            t_print_line.foot_note1 = entry(0, foot_note, ";")
            t_print_line.foot_note2 = entry(1, foot_note, ";")
            t_print_line.foot_note3 = entry(2, foot_note, ";")

    return generate_output()