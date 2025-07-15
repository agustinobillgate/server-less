#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.pos_dashboard_post_menubl import pos_dashboard_post_menubl
from models import Queasy, H_bill, H_artikel, H_bill_line, Tisch, Res_line

menu_list_data, Menu_list = create_model("Menu_list", {"nr":int, "rec_id":int, "art_number":int, "art_description":string, "art_qty":int, "art_price":Decimal, "special_request":string})

def selforder_post_itembl(outlet_number:int, table_nr:int, room_number:string, guest_name:string, pax:int, guest_number:int, res_number:int, resline_number:int, order_datetime:datetime, active_order:bool, session_parameter:string, menu_list_data:[Menu_list]):

    prepare_cache ([Queasy, H_bill, Tisch, Res_line])

    mess_result = ""
    orderbill_number:int = 0
    orderbill_line_number:int = 0
    direct_post:bool = False
    count_i:int = 0
    alpha_flag:bool = False
    room_no:string = ""
    rm_no:string = ""
    str1:string = ""
    dynamic_qr:bool = False
    room_serviceflag:bool = False
    pay_flag:bool = False
    found_menu:bool = False
    sclose_time:int = 0
    eclose_time:int = 0
    scurr_time:int = 0
    ecurr_time:int = 0
    curr_time:int = 0
    time_str:string = ""
    shour:int = 0
    sminute:int = 0
    ehour:int = 0
    eminute:int = 0
    recid_hbill:int = 0
    found_soldout:bool = False
    queasy = h_bill = h_artikel = h_bill_line = tisch = res_line = None

    menu_list = post_menu_list = new_order = buff_hbill = q_orderbill = q_takentable = sosqsy = h_order = None

    post_menu_list_data, Post_menu_list = create_model("Post_menu_list", {"rec_id":int, "description":string, "qty":int, "price":Decimal, "special_request":string})

    New_order = create_buffer("New_order",Queasy)
    Buff_hbill = create_buffer("Buff_hbill",H_bill)
    Q_orderbill = create_buffer("Q_orderbill",Queasy)
    Q_takentable = create_buffer("Q_takentable",Queasy)
    Sosqsy = create_buffer("Sosqsy",Queasy)
    H_order = create_buffer("H_order",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, orderbill_number, orderbill_line_number, direct_post, count_i, alpha_flag, room_no, rm_no, str1, dynamic_qr, room_serviceflag, pay_flag, found_menu, sclose_time, eclose_time, scurr_time, ecurr_time, curr_time, time_str, shour, sminute, ehour, eminute, recid_hbill, found_soldout, queasy, h_bill, h_artikel, h_bill_line, tisch, res_line
        nonlocal outlet_number, table_nr, room_number, guest_name, pax, guest_number, res_number, resline_number, order_datetime, active_order, session_parameter
        nonlocal new_order, buff_hbill, q_orderbill, q_takentable, sosqsy, h_order


        nonlocal menu_list, post_menu_list, new_order, buff_hbill, q_orderbill, q_takentable, sosqsy, h_order
        nonlocal post_menu_list_data

        return {"mess_result": mess_result}

    def post_to_outlet():

        nonlocal mess_result, orderbill_number, orderbill_line_number, direct_post, count_i, alpha_flag, room_no, rm_no, str1, dynamic_qr, room_serviceflag, pay_flag, found_menu, sclose_time, eclose_time, scurr_time, ecurr_time, curr_time, time_str, shour, sminute, ehour, eminute, recid_hbill, found_soldout, queasy, h_bill, h_artikel, h_bill_line, tisch, res_line
        nonlocal outlet_number, table_nr, room_number, guest_name, pax, guest_number, res_number, resline_number, order_datetime, active_order, session_parameter
        nonlocal new_order, buff_hbill, q_orderbill, q_takentable, sosqsy, h_order


        nonlocal menu_list, post_menu_list, new_order, buff_hbill, q_orderbill, q_takentable, sosqsy, h_order
        nonlocal post_menu_list_data

        post_language_code:int = 0
        post_rec_id:int = 0
        post_tischnr:int = 0
        post_curr_dept:int = 0
        post_gname:string = ""
        post_pax:int = 0
        post_guestnr:int = 0
        post_curr_room:string = ""
        post_resnr:int = 0
        post_reslinnr:int = 0
        post_table_no:int = 0
        post_order_no:int = 0
        post_bill_number:int = 0
        post_session_param:string = ""
        post_bill_recid:int = 0
        post_mess_str:string = ""
        user_init:string = ""
        mergequeasy = None
        getrec_id = None

        queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 1)],"number2": [(eq, 9)]})

        if queasy:
            user_init = queasy.char2
        Mergequeasy =  create_buffer("Mergequeasy",Queasy)

        mergequeasy = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "orderbill")],"char3": [(eq, session_parameter)],"betriebsnr": [(ne, 0)]})

        if mergequeasy:

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 225) & (Queasy.char1 == ("orderbill").lower()) & (Queasy.char3 == mergequeasy.char3)).order_by(Queasy._recid).all():
                queasy.betriebsnr = mergequeasy.betriebsnr
            pass
        Getrec_id =  create_buffer("Getrec_id",Queasy)

        getrec_id = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "orderbill")],"char3": [(eq, session_parameter)]})

        if getrec_id:
            post_bill_recid = getrec_id.betriebsnr
        else:
            post_bill_recid = 0
        post_menu_list_data.clear()

        for menu_list in query(menu_list_data):
            post_menu_list = Post_menu_list()
            post_menu_list_data.append(post_menu_list)

            post_menu_list.rec_id = menu_list.art_number
            post_menu_list.description = menu_list.art_description
            post_menu_list.qty = menu_list.art_qty
            post_menu_list.price =  to_decimal(menu_list.art_price)
            post_menu_list.special_request = menu_list.special_request


        post_table_no = table_nr
        post_order_no = orderbill_number
        post_tischnr = table_nr
        post_curr_dept = outlet_number
        post_gname = guest_name
        post_pax = pax
        post_guestnr = guest_number
        post_curr_room = room_number
        post_resnr = res_number
        post_reslinnr = resline_number
        post_session_param = session_parameter


        post_bill_number, post_mess_str = get_output(pos_dashboard_post_menubl(1, post_bill_recid, post_tischnr, post_curr_dept, user_init, post_gname, post_pax, post_guestnr, post_curr_room, post_resnr, post_reslinnr, post_session_param, post_order_no, post_menu_list_data))

        if post_mess_str.lower()  == ("Order Posted Success").lower() :
            mess_result = "0-Posting Item Success"
        else:
            mess_result = "9-" + post_mess_str

    if outlet_number == None or outlet_number == 0:
        mess_result = "1-Outlet number can't be null!"

        return generate_output()

    if table_nr == None or table_nr == 0:
        mess_result = "2-Table number can't be null!"

        return generate_output()

    if guest_name == None or guest_name == "":
        mess_result = "3-Guest Name can't be null!"

        return generate_output()

    if pax == None or pax == 0:
        mess_result = "4-Number of pax can't be null!"

        return generate_output()

    if order_datetime == None:
        mess_result = "5-Order Date and Time can't be null!"

        return generate_output()

    menu_list = query(menu_list_data, first=True)

    if not menu_list:
        mess_result = "7-Request is not complete. Menu List not available."

        return generate_output()

    queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 1)],"number2": [(eq, 25)],"number3": [(eq, 5)],"betriebsnr": [(eq, outlet_number)],"char2": [(ne, "")]})

    if queasy:
        shour = to_int(substring(trim(entry(0, queasy.char2, "|")) , 0, 2))
        sminute = to_int(substring(trim(entry(0, queasy.char2, "|")) , 3, 2))
        ehour = to_int(substring(trim(entry(1, queasy.char2, "|")) , 0, 2))
        eminute = to_int(substring(trim(entry(1, queasy.char2, "|")) , 3, 2))
        sclose_time = shour * 3600 + sminute * 60
        eclose_time = ehour * 3600 + eminute * 60
        curr_time = get_current_time_in_seconds()
        time_str = to_string(get_current_time_in_seconds(), "HH:MM")
        scurr_time = to_int(entry(0, time_str, ":"))
        ecurr_time = to_int(entry(1, time_str, ":"))

        if ehour - shour < 0:

            if scurr_time >= shour:

                if curr_time >= sclose_time and eclose_time <= curr_time:
                    mess_result = "4-Closing Time periode! Order not possible."

                    return generate_output()

            elif scurr_time <= ehour:

                if curr_time <= eclose_time:
                    mess_result = "4-Closing Time periode! Order not possible."

                    return generate_output()
        else:

            if curr_time >= sclose_time and curr_time <= eclose_time:
                mess_result = "4-Closing Time periode! Order not possible."

                return generate_output()
    active_order = True
    direct_post = False

    queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 1)],"number2": [(eq, 15)],"betriebsnr": [(eq, outlet_number)]})

    if queasy:
        direct_post = queasy.logi1

    if direct_post:

        h_bill = get_cache (H_bill, {"tischnr": [(eq, table_nr)],"departement": [(eq, outlet_number)],"flag": [(eq, 0)],"saldo": [(eq, 0)]})

        if h_bill:

            h_bill_line_obj_list = {}
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart != 0)).filter(
                     (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True


                pay_flag = True
                break

            if pay_flag:
                mess_result = "91-Bill on this table has been paid and balance is zero. Please come back at the moment or contact the cashier."

                return generate_output()

    if room_number == None:
        room_number = ""

    if guest_number == None:
        guest_number = 0

    if res_number == None:
        res_number = 0

    if resline_number == None:
        resline_number = 0

    for menu_list in query(menu_list_data):

        queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, menu_list.art_number)],"number3": [(eq, outlet_number)]})

        if queasy:

            if queasy.logi2 :
                found_soldout = True
                break

    if found_soldout:
        mess_result = "6-One of Item Has SoldOut!"

        return generate_output()

    for sosqsy in db_session.query(Sosqsy).filter(
             (Sosqsy.key == 222) & (Sosqsy.number1 == 1) & (Sosqsy.betriebsnr == outlet_number)).order_by(Sosqsy._recid).all():

        if sosqsy.number2 == 14:
            dynamic_qr = sosqsy.logi1

        if sosqsy.number2 == 21:
            room_serviceflag = sosqsy.logi1
    recid_hbill = 0

    for buff_hbill in db_session.query(Buff_hbill).filter(
             (Buff_hbill.tischnr == table_nr) & (Buff_hbill.departement == outlet_number) & (Buff_hbill.flag == 1)).order_by(Buff_hbill.rechnr.desc()).yield_per(100):
        recid_hbill = buff_hbill._recid

        if recid_hbill != 0:
            break

    q_orderbill = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "orderbill")],"number1": [(eq, outlet_number)],"number2": [(eq, table_nr)],"number3": [(eq, 0)],"char3": [(eq, session_parameter)],"betriebsnr": [(eq, recid_hbill)]})

    if q_orderbill:
        pass
        db_session.delete(q_orderbill)
        pass

    if room_serviceflag:

        q_takentable = db_session.query(Q_takentable).filter(
                 (Q_takentable.key == 225) & (Q_takentable.char1 == ("taken-table").lower()) & (Q_takentable.number2 == table_nr) & (entry(0, Q_takentable.char3, "|") == (session_parameter).lower()) & (num_entries(Q_takentable.char3, "|") == 3)).first()

        if q_takentable:
            str1 = entry(2, q_takentable.char3, "|")
            rm_no = entry(0, str1, "$")

        if rm_no != "":
            for count_i in range(65,90 + 1) :

                if matches(rm_no,r"*" + chr_unicode(count_i) + r"*"):
                    alpha_flag = True

            if not alpha_flag:
                count_i = 0
                for count_i in range(97,122 + 1) :

                    if matches(rm_no,r"*" + chr_unicode(count_i) + r"*"):
                        alpha_flag = True

    if alpha_flag:

        tisch = get_cache (Tisch, {"departement": [(eq, outlet_number)],"tischnr": [(eq, table_nr)]})

        if tisch:
            room_no = substring(tisch.bezeich, 5)

        res_line = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, room_no)]})
    else:

        res_line = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, to_string(table_nr))]})

    if res_line:
        res_number = res_line.resnr
        resline_number = res_line.reslinnr

    queasy = get_cache (Queasy, {"key": [(eq, 225)],"number1": [(eq, outlet_number)],"char1": [(eq, "orderbill")],"number2": [(eq, table_nr)],"logi1": [(eq, active_order)]})

    if queasy:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 225) & (Queasy.number1 == outlet_number) & (Queasy.char1 == ("orderbill").lower()) & (Queasy.number2 == table_nr) & (Queasy.logi1 == active_order)).order_by(Queasy.number3.desc()).yield_per(100):
            orderbill_number = queasy.number3 + 1
            break
    else:
        orderbill_number = 1

    queasy = get_cache (Queasy, {"key": [(eq, 225)],"number1": [(eq, outlet_number)],"char1": [(eq, "orderbill")],"number2": [(eq, table_nr)],"number3": [(eq, orderbill_number)],"date1": [(eq, date_mdy(order_datetime))],"logi1": [(eq, active_order)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 225
        queasy.number1 = outlet_number
        queasy.number2 = table_nr
        queasy.number3 = orderbill_number
        queasy.char1 = "orderbill"
        queasy.char2 = "RN=" + room_number +\
                "|NM=" + guest_name +\
                "|DT=" + to_string(order_datetime) +\
                "|PX=" + to_string(pax) +\
                "|GN=" + to_string(guest_number) +\
                "|RS=" + to_string(res_number) +\
                "|RL=" + to_string(resline_number)
        queasy.date1 = date_mdy(order_datetime)
        queasy.logi1 = active_order
        queasy.logi3 = False
        queasy.char3 = session_parameter


        queasy.betriebsnr = 0

        for menu_list in query(menu_list_data):
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 225
            queasy.number1 = orderbill_number
            queasy.number2 = table_nr
            queasy.number3 = menu_list.nr
            queasy.char1 = "orderbill-line"
            queasy.char2 = to_string(outlet_number) + "|" + to_string(table_nr) + "|" + to_string(order_datetime) + "|" + session_parameter
            queasy.char3 = to_string(menu_list.nr) + "|" +\
                    to_string(menu_list.art_number) + "|" +\
                    to_string(menu_list.art_description) + "|" +\
                    to_string(menu_list.art_qty) + "|" +\
                    to_string(menu_list.art_price) + "|" +\
                    to_string(menu_list.special_request)
            queasy.date1 = date_mdy(order_datetime)
            queasy.logi2 = False
            queasy.logi3 = False

        if direct_post:
            post_to_outlet()
        else:
            mess_result = "0-Posting Item Success"
    else:

        for menu_list in query(menu_list_data):
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 225
            queasy.number1 = orderbill_number
            queasy.number2 = table_nr
            queasy.number3 = menu_list.nr
            queasy.char1 = "orderbill-line"
            queasy.char2 = to_string(outlet_number) + "|" + to_string(table_nr) + "|" + to_string(order_datetime) + "|" + session_parameter
            queasy.char3 = to_string(menu_list.nr) + "|" +\
                    to_string(menu_list.art_number) + "|" +\
                    to_string(menu_list.art_description) + "|" +\
                    to_string(menu_list.art_qty) + "|" +\
                    to_string(menu_list.art_price) + "|" +\
                    to_string(menu_list.special_request)
            queasy.date1 = date_mdy(order_datetime)
            queasy.logi2 = False
            queasy.logi3 = False

        if direct_post:
            post_to_outlet()
        else:
            mess_result = "0-RePosting Item Success"

    return generate_output()