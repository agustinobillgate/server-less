#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.print_hbill1_cldbl import print_hbill1_cldbl
from models import Printer, H_bill, Res_line, Guest

def print_hbill_getpartial_webbl(pvilanguage:int, user_init:string, print_all:bool, printnr:int, hbrecid:int, use_h_queasy:bool):

    prepare_cache ([H_bill, Res_line, Guest])

    msg_str = ""
    room_no = ""
    guest_name = ""
    outlet_print_list_data = []
    lvcarea:string = "print-hbill-getsection-web"
    winprinterflag:bool = False
    session_parameter:string = ""
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
    printer = h_bill = res_line = guest = None

    t_printer = output_list = print_list = outlet_print_list = paylist = None

    t_printer_data, T_printer = create_model_like(Printer)
    output_list_data, Output_list = create_model("Output_list", {"str":string, "pos":int, "flag_popup":bool, "npause":int, "sort_i":int})
    print_list_data, Print_list = create_model("Print_list", {"str":string, "str_pos":int, "pos":int, "flag_popup":bool, "npause":int, "sort_i":int})
    outlet_print_list_data, Outlet_print_list = create_model("Outlet_print_list", {"sort_i":int, "flag_popup":bool, "str_date":string, "str_time":string, "bill_no":string, "resto_name":string, "table_usr_id":string, "curr_time":string, "guest_name":string, "guest_member":string, "od_taker":string, "str_qty":string, "descrip":string, "str_price":string, "foot_note1":string, "foot_note2":string}, {"str_date": "", "str_time": "", "bill_no": "", "resto_name": "", "table_usr_id": "", "curr_time": "", "guest_name": "", "guest_member": "", "od_taker": "", "str_qty": "", "descrip": "", "str_price": "", "foot_note1": "", "foot_note2": ""})

    Paylist = Print_list
    paylist_data = print_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_no, guest_name, outlet_print_list_data, lvcarea, winprinterflag, session_parameter, filename, table_no, usr_id, counter, gs, pay_str, depopay_str, pay_amount, curr_amount, curr_pay, rechnr_str, flag_change, flag_pay, flag_vat, foot_note, guest_addr, guest_addr1, count_i, gs_1, fo_depoart, fo_depobez, fb_depoart, fb_depobez, voucher_depo, gastno, ns_billno, curr_dept, str1, printer, h_bill, res_line, guest
        nonlocal pvilanguage, user_init, print_all, printnr, hbrecid, use_h_queasy
        nonlocal paylist


        nonlocal t_printer, output_list, print_list, outlet_print_list, paylist
        nonlocal t_printer_data, output_list_data, print_list_data, outlet_print_list_data

        return {"msg_str": msg_str, "room_no": room_no, "guest_name": guest_name, "outlet-print-list": outlet_print_list_data}


    printer = get_cache (Printer, {"nr": [(eq, printnr)]})

    if not printer:
        msg_str = "1-Printer Not Found."

        return generate_output()
    print_all, filename, msg_str, winprinterflag, print_list_data, t_printer_data = get_output(print_hbill1_cldbl(pvilanguage, session_parameter, user_init, hbrecid, printnr, use_h_queasy, print_all))

    if msg_str != "":

        return generate_output()

    for print_list in query(print_list_data, sort_by=[("sort_i",False)]):
        outlet_print_list = Outlet_print_list()
        outlet_print_list_data.append(outlet_print_list)

        outlet_print_list.sort_i = print_list.sort_i
        outlet_print_list.flag_popup = print_list.flag_popup

        if print_list.str_pos == 1:
            outlet_print_list.str_date = trim(entry(0, print_list.str, "|"))
            outlet_print_list.str_time = trim(entry(1, print_list.str, "|"))
            outlet_print_list.bill_no = trim(entry(3, print_list.str, "|"))
            outlet_print_list.curr_time = to_string(get_current_time_in_seconds(), "HH:MM:SS")

        elif print_list.str_pos == 2:
            outlet_print_list.resto_name = trim(print_list.str)

        elif print_list.str_pos == 3:
            table_no = trim(entry(1, print_list.str, "|"))
            usr_id = trim(entry(2, print_list.str, "|")) + " " + trim(entry(3, print_list.str, "|"))

            if trim(entry(4, print_list.str, "|")) != "":
                outlet_print_list.od_taker = trim(entry(4, print_list.str, "|"))
            outlet_print_list.table_usr_id = translateExtended ("Table", lvcarea, "") + " " + table_no + " / " + usr_id.upper()

        elif print_list.str_pos == 5:
            outlet_print_list.guest_name = trim(entry(1, print_list.str, "|"))
            gs = outlet_print_list.guest_name
            guest_name = outlet_print_list.guest_name

            h_bill = get_cache (H_bill, {"_recid": [(eq, hbrecid)]})

            if h_bill:

                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                    if res_line:
                        gs = res_line.name
                        guest_name = res_line.name
                        outlet_print_list.guest_name = res_line.name

                elif h_bill.resnr > 0:

                    guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                    if guest:
                        gs = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        guest_name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        outlet_print_list.guest_name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

        elif print_list.str_pos == 8:
            outlet_print_list.guest_member = trim(print_list.str)

        elif print_list.str_pos == 10:
            outlet_print_list.str_qty = trim(entry(0, print_list.str, "|"))
            outlet_print_list.descrip = trim(entry(1, print_list.str, "|"))
            outlet_print_list.str_price = trim(entry(2, print_list.str, "|"))

        elif print_list.str_pos == 11:
            outlet_print_list.descrip = trim(entry(0, print_list.str, "|"))
            outlet_print_list.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 12 and matches(print_list.str,r"*Service*"):
            outlet_print_list.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            outlet_print_list.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 12 and matches(print_list.str,r"*gov*"):
            outlet_print_list.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            outlet_print_list.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 13:
            outlet_print_list.descrip = translateExtended ("TOTAL", lvcarea, "")
            outlet_print_list.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 14:

            if gs != "":

                if matches(print_list.str,'*' + gs + '*'):
                    outlet_print_list.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
                    outlet_print_list.descrip = trim(substring(outlet_print_list.descrip, length(gs) + 1 - 1))


                else:
                    outlet_print_list.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            else:
                outlet_print_list.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            outlet_print_list.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 16:
            outlet_print_list.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            outlet_print_list.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 15:
            outlet_print_list.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            outlet_print_list.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 17:

            if num_entries(print_list.str, ":") > 1:
                room_no = trim(entry(1, print_list.str, ":"))
            else:
                room_no = ""

        elif print_list.str_pos == 19:
            outlet_print_list.foot_note1 = trim(print_list.str)

        elif print_list.str_pos == 20:
            outlet_print_list.foot_note1 = trim(print_list.str)

    h_bill = get_cache (H_bill, {"_recid": [(eq, hbrecid)]})
    pass
    h_bill.rgdruck = 1
    pass
    msg_str = "0-Success"

    return generate_output()