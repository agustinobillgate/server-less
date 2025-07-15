#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.pr_sphbill1_cldbl import pr_sphbill1_cldbl
from models import Printer, H_bill

def printsplit_hbill_getsection_webbl(pvilanguage:int, user_init:string, print_all:bool, printnr:int, hbrecid:int, use_h_queasy:bool, billnr:int):

    prepare_cache ([H_bill])

    msg_str = ""
    room_no = ""
    guest_name = ""
    outlet_split_bill_data = []
    lvcarea:string = "printsplit-hbill-getsection-web"
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
    split_no:string = ""
    printer = h_bill = None

    t_printer = output_list = print_list = outlet_split_bill = paylist = None

    t_printer_data, T_printer = create_model_like(Printer)
    output_list_data, Output_list = create_model("Output_list", {"str":string, "pos":int, "flag_popup":bool, "npause":int, "sort_i":int})
    print_list_data, Print_list = create_model("Print_list", {"str":string, "str_pos":int, "pos":int, "flag_popup":bool, "npause":int, "sort_i":int})
    outlet_split_bill_data, Outlet_split_bill = create_model("Outlet_split_bill", {"sort_i":int, "str_date":string, "str_time":string, "bill_no":string, "resto_name":string, "table_usr_id":string, "curr_time":string, "guest_name":string, "guest_member":string, "od_taker":string, "str_qty":string, "descrip":string, "str_price":string, "foot_note1":string, "foot_note2":string, "foot_note3":string}, {"str_date": "", "str_time": "", "bill_no": "", "resto_name": "", "table_usr_id": "", "curr_time": "", "guest_name": "", "guest_member": "", "od_taker": "", "str_qty": "", "descrip": "", "str_price": "", "foot_note1": "", "foot_note2": "", "foot_note3": ""})

    Paylist = Print_list
    paylist_data = print_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_no, guest_name, outlet_split_bill_data, lvcarea, winprinterflag, session_parameter, filename, table_no, usr_id, counter, gs, pay_str, depopay_str, pay_amount, curr_amount, curr_pay, rechnr_str, flag_change, flag_pay, flag_vat, foot_note, guest_addr, guest_addr1, count_i, gs_1, fo_depoart, fo_depobez, fb_depoart, fb_depobez, voucher_depo, gastno, ns_billno, curr_dept, str1, split_no, printer, h_bill
        nonlocal pvilanguage, user_init, print_all, printnr, hbrecid, use_h_queasy, billnr
        nonlocal paylist


        nonlocal t_printer, output_list, print_list, outlet_split_bill, paylist
        nonlocal t_printer_data, output_list_data, print_list_data, outlet_split_bill_data

        return {"msg_str": msg_str, "room_no": room_no, "guest_name": guest_name, "outlet-split-bill": outlet_split_bill_data}


    printer = get_cache (Printer, {"nr": [(eq, printnr)]})

    if not printer:
        msg_str = "1-Printer Not Found."

        return generate_output()
    print_all, winprinterflag, filename, msg_str, print_list_data, t_printer_data = get_output(pr_sphbill1_cldbl(pvilanguage, hbrecid, printnr, use_h_queasy, session:parameter, user_init, billnr, print_all))

    if msg_str != "":

        return generate_output()

    for print_list in query(print_list_data, sort_by=[("str_pos",False)]):
        outlet_split_bill = Outlet_split_bill()
        outlet_split_bill_data.append(outlet_split_bill)

        outlet_split_bill.sort_i = print_list.sort_i

        if print_list.str_pos == 1:
            outlet_split_bill.str_date = trim(entry(0, print_list.str, "|"))
            outlet_split_bill.str_time = trim(entry(1, print_list.str, "|"))
            outlet_split_bill.bill_no = trim(entry(3, print_list.str, "|"))
            outlet_split_bill.curr_time = to_string(get_current_time_in_seconds(), "HH:MM:SS")

        elif print_list.str_pos == 2:
            outlet_split_bill.resto_name = trim(print_list.str)

        elif print_list.str_pos == 3:
            table_no = trim(entry(1, print_list.str, "|"))
            usr_id = trim(entry(2, print_list.str, "|")) + " " + trim(entry(4, print_list.str, "|"))
            split_no = trim(entry(3, print_list.str, "|"))


            outlet_split_bill.table_usr_id = translateExtended ("Table", lvcarea, "") + " " + table_no + "/" + usr_id.upper() + split_no

        elif print_list.str_pos == 5:
            outlet_split_bill.guest_name = trim(entry(1, print_list.str, "|"))
            gs = outlet_split_bill.guest_name
            guest_name = outlet_split_bill.guest_name

            if num_entries(print_list.str, "|") > 2 and guest_name != "":
                outlet_split_bill.guest_name = outlet_split_bill.guest_name + " | " + trim(entry(2, print_list.str, "|"))

        elif print_list.str_pos == 8:
            outlet_split_bill.guest_member = trim(print_list.str)

        elif print_list.str_pos == 10:
            outlet_split_bill.str_qty = trim(entry(0, print_list.str, "|"))
            outlet_split_bill.descrip = trim(entry(1, print_list.str, "|"))
            outlet_split_bill.str_price = trim(entry(2, print_list.str, "|"))

        elif print_list.str_pos == 11:
            outlet_split_bill.descrip = trim(entry(0, print_list.str, "|"))
            outlet_split_bill.str_price = trim(entry(1, print_list.str, "|"))


            outlet_split_bill = Outlet_split_bill()
            outlet_split_bill_data.append(outlet_split_bill)

            outlet_split_bill.sort_i = -1
            outlet_split_bill.descrip = fill("-", 42)
            outlet_split_bill.str_price = fill("-", 19)

        elif print_list.str_pos == 12 and matches(print_list.str,r"*Service*"):
            outlet_split_bill.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            outlet_split_bill.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 12 and matches(print_list.str,r"*gov*"):
            outlet_split_bill.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            outlet_split_bill.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 13:
            outlet_split_bill.sort_i = -1
            outlet_split_bill.descrip = fill("-", 42)
            outlet_split_bill.str_price = fill("-", 19)
            outlet_split_bill = Outlet_split_bill()
            outlet_split_bill_data.append(outlet_split_bill)

            outlet_split_bill.sort_i = print_list.sort_i
            outlet_split_bill.descrip = translateExtended ("TOTAL", lvcarea, "")
            outlet_split_bill.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 14:

            if gs != "":

                if matches(print_list.str,'*' + gs + '*'):
                    outlet_split_bill.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
                    outlet_split_bill.descrip = trim(substring(outlet_split_bill.descrip, length(gs) + 1 - 1))


                else:
                    outlet_split_bill.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            else:
                outlet_split_bill.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            outlet_split_bill.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 16:
            outlet_split_bill.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            outlet_split_bill.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 15:
            outlet_split_bill.sort_i = -1
            outlet_split_bill.descrip = fill("-", 42)
            outlet_split_bill.str_price = fill("-", 19)
            outlet_split_bill = Outlet_split_bill()
            outlet_split_bill_data.append(outlet_split_bill)

            outlet_split_bill.sort_i = print_list.sort_i
            outlet_split_bill.descrip = translateExtended (trim(entry(0, print_list.str, "|")) , lvcarea, "")
            outlet_split_bill.str_price = trim(entry(1, print_list.str, "|"))

        elif print_list.str_pos == 17:

            if num_entries(print_list.str, ":") > 1:
                room_no = trim(entry(1, print_list.str, ":"))
            else:
                room_no = ""

        elif print_list.str_pos == 19:

            if print_list.str == None:
                print_list.str = ""
            outlet_split_bill.foot_note1 = trim(print_list.str)

        elif print_list.str_pos == 20:

            if print_list.str == None:
                print_list.str = ""
            outlet_split_bill.foot_note2 = trim(print_list.str)

        elif print_list.str_pos == 21:

            if print_list.str == None:
                print_list.str = ""
            outlet_split_bill.foot_note3 = trim(print_list.str)

    h_bill = get_cache (H_bill, {"_recid": [(eq, hbrecid)]})
    pass
    h_bill.rgdruck = 1
    pass
    msg_str = "0-Success"

    return generate_output()