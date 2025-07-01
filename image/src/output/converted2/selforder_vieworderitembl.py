#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill, Bediener, H_bill_line, Res_line, Htparam, H_journal

def selforder_vieworderitembl(inp_outlet_num:int, inp_table_num:int):

    prepare_cache ([H_bill, Bediener, H_bill_line, Res_line, Htparam, H_journal])

    record_id = 0
    user_init = ""
    language_code = 0
    outlet_number = 0
    order_number = 0
    table_number = 0
    post_datetime = ""
    guest_number = 0
    guest_name = ""
    pax = 0
    room_number = ""
    res_number = 0
    reslin_numnber = 0
    subtotal = to_decimal("0.0")
    mess_result = ""
    selected_menu_list = []
    h_bill = bediener = h_bill_line = res_line = htparam = h_journal = None

    selected_menu = None

    selected_menu_list, Selected_menu = create_model("Selected_menu", {"rec_id":int, "article_name":string, "quantity":int, "price":Decimal, "post_date":date, "post_time":string, "tax":Decimal, "service":Decimal, "subtotal":Decimal, "special_req":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal record_id, user_init, language_code, outlet_number, order_number, table_number, post_datetime, guest_number, guest_name, pax, room_number, res_number, reslin_numnber, subtotal, mess_result, selected_menu_list, h_bill, bediener, h_bill_line, res_line, htparam, h_journal
        nonlocal inp_outlet_num, inp_table_num


        nonlocal selected_menu
        nonlocal selected_menu_list

        return {"record_id": record_id, "user_init": user_init, "language_code": language_code, "outlet_number": outlet_number, "order_number": order_number, "table_number": table_number, "post_datetime": post_datetime, "guest_number": guest_number, "guest_name": guest_name, "pax": pax, "room_number": room_number, "res_number": res_number, "reslin_numnber": reslin_numnber, "subtotal": subtotal, "mess_result": mess_result, "selected-menu": selected_menu_list}


    selected_menu_list.clear()

    h_bill = get_cache (H_bill, {"departement": [(eq, inp_outlet_num)],"flag": [(eq, 0)],"saldo": [(ne, 0)],"tischnr": [(eq, inp_table_num)]})

    if h_bill:
        record_id = h_bill._recid
        order_number = h_bill.rechnr
        outlet_number = inp_outlet_num
        table_number = inp_table_num
        pax = h_bill.belegung
        res_number = h_bill.resnr
        reslin_numnber = h_bill.reslinnr

        bediener = get_cache (Bediener, {"userinit": [(eq, "so")]})

        if bediener:
            user_init = bediener.userinit

        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)],"tischnr": [(eq, h_bill.tischnr)]})

        if h_bill_line:
            post_datetime = to_string(h_bill_line.bill_datum) + " - " + to_string(h_bill_line.zeit, "HH:MM:SS")

        if h_bill.resnr > 0:

            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

            if res_line:
                guest_number = res_line.gastnrmember
                guest_name = res_line.name
                room_number = res_line.zinr


        else:
            guest_name = h_bill.bilname
            room_number = ""

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.tischnr == h_bill.tischnr)).order_by(H_bill_line.bill_datum.desc(), H_bill_line.zeit.desc()).all():
            selected_menu = Selected_menu()
            selected_menu_list.append(selected_menu)

            selected_menu.rec_id = h_bill_line._recid
            selected_menu.article_name = h_bill_line.bezeich
            selected_menu.quantity = h_bill_line.anzahl
            selected_menu.price =  to_decimal(h_bill_line.betrag)
            selected_menu.post_date = h_bill_line.bill_datum
            selected_menu.post_time = to_string(h_bill_line.zeit, "HH:MM:SS")
            subtotal =  to_decimal(subtotal) + to_decimal(h_bill_line.betrag)

            htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

            h_journal = get_cache (H_journal, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)],"rechnr": [(eq, h_bill_line.rechnr)],"bill_datum": [(eq, h_bill_line.bill_datum)]})

            if h_journal and h_journal.artnr != htparam.finteger:
                selected_menu.special_req = h_journal.aendertext
            else:
                selected_menu.special_req = ""
        mess_result = "Success load data"
    else:
        mess_result = "Bill status is closed!"

    return generate_output()