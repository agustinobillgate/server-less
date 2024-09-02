from functions.additional_functions import *
import decimal
from sqlalchemy import func
import re
from functions.pos_dashboard_post_menubl import pos_dashboard_post_menubl
from models import Queasy, H_bill, Tisch, Res_line

def selforder_post_itembl(outlet_number:int, table_nr:int, room_number:str, guest_name:str, pax:int, guest_number:int, res_number:int, resline_number:int, order_datetime:, active_order:bool, session_parameter:str, menu_list:[Menu_list]):
    mess_result = ""
    orderbill_number:int = 0
    orderbill_line_number:int = 0
    direct_post:bool = False
    count_i:int = 0
    alpha_flag:bool = False
    room_no:str = ""
    rm_no:str = ""
    str1:str = ""
    dynamic_qr:bool = False
    room_serviceflag:bool = False
    recid_hbill:int = 0
    found_soldout:bool = False
    queasy = h_bill = tisch = res_line = None

    menu_list = post_menu_list = new_order = buff_hbill = q_orderbill = q_takentable = sosqsy = mergequeasy = getrec_id = None

    menu_list_list, Menu_list = create_model("Menu_list", {"nr":int, "rec_id":int, "art_number":int, "art_description":str, "art_qty":int, "art_price":decimal, "special_request":str})
    post_menu_list_list, Post_menu_list = create_model("Post_menu_list", {"rec_id":int, "description":str, "qty":int, "price":decimal, "special_request":str})

    New_order = Queasy
    Buff_hbill = H_bill
    Q_orderbill = Queasy
    Q_takentable = Queasy
    Sosqsy = Queasy
    Mergequeasy = Queasy
    Getrec_id = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, orderbill_number, orderbill_line_number, direct_post, count_i, alpha_flag, room_no, rm_no, str1, dynamic_qr, room_serviceflag, recid_hbill, found_soldout, queasy, h_bill, tisch, res_line
        nonlocal new_order, buff_hbill, q_orderbill, q_takentable, sosqsy, mergequeasy, getrec_id


        nonlocal menu_list, post_menu_list, new_order, buff_hbill, q_orderbill, q_takentable, sosqsy, mergequeasy, getrec_id
        nonlocal menu_list_list, post_menu_list_list
        return {"mess_result": mess_result}

    def post_to_outlet():

        nonlocal mess_result, orderbill_number, orderbill_line_number, direct_post, count_i, alpha_flag, room_no, rm_no, str1, dynamic_qr, room_serviceflag, recid_hbill, found_soldout, queasy, h_bill, tisch, res_line
        nonlocal new_order, buff_hbill, q_orderbill, q_takentable, sosqsy, mergequeasy, getrec_id


        nonlocal menu_list, post_menu_list, new_order, buff_hbill, q_orderbill, q_takentable, sosqsy, mergequeasy, getrec_id
        nonlocal menu_list_list, post_menu_list_list

        post_language_code:int = 0
        post_rec_id:int = 0
        post_tischnr:int = 0
        post_curr_dept:int = 0
        post_gname:str = ""
        post_pax:int = 0
        post_guestnr:int = 0
        post_curr_room:str = ""
        post_resnr:int = 0
        post_reslinnr:int = 0
        post_table_no:int = 0
        post_order_no:int = 0
        post_bill_number:int = 0
        post_session_param:str = ""
        post_bill_recid:int = 0
        post_mess_str:str = ""
        user_init:str = ""

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 222) &  (Queasy.number1 == 1) &  (Queasy.number2 == 9)).first()

        if queasy:
            user_init = queasy.char2
        Mergequeasy = Queasy

        mergequeasy = db_session.query(Mergequeasy).filter(
                (Mergequeasy.key == 225) &  (func.lower(Mergequeasy.char1) == "orderbill") &  (func.lower(Mergequeasy.char3) == (session_parameter).lower()) &  (Mergequeasy.betriebsnr != 0)).first()

        if mergequeasy:

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 225) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.char3 == mergeQueasy.char3)).all():
                queasy.betriebsnr = mergequeasy.betriebsnr
        Getrec_id = Queasy

        getrec_id = db_session.query(Getrec_id).filter(
                (Getrec_id.key == 225) &  (func.lower(Getrec_id.char1) == "orderbill") &  (func.lower(Getrec_id.char3) == (session_parameter).lower())).first()

        if getrec_id:
            post_bill_recid = getrec_id.betriebsnr
        else:
            post_bill_recid = 0
        post_menu_list._list.clear()

        for menu_list in query(menu_list_list):
            post_menu_list = Post_menu_list()
            post_menu_list_list.append(post_menu_list)

            post_menu_list.rec_id = menu_list.art_number
            post_menu_list.DESCRIPTION = menu_list.art_description
            post_menu_list.qty = menu_list.art_qty
            post_menu_list.price = menu_list.art_price
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


        post_bill_number, post_mess_str = get_output(pos_dashboard_post_menubl(1, post_bill_recid, post_tischnr, post_curr_dept, user_init, post_gname, post_pax, post_guestnr, post_curr_room, post_resnr, post_reslinnr, post_session_param, post_order_no, post_menu_list))

        if post_mess_str.lower()  == "Order Posted Success":
            mess_result = "0_Posting Item Success"
        else:
            mess_result = "9-" + post_mess_str


    if outlet_number == None or outlet_number == 0:
        mess_result = "1_Outlet number can't be null!"

        return generate_output()

    if table_nr == None or table_nr == 0:
        mess_result = "2_Table number can't be null!"

        return generate_output()

    if guest_name == None or guest_name == "":
        mess_result = "3_Guest Name can't be null!"

        return generate_output()

    if pax == None or pax == 0:
        mess_result = "4_Number of pax can't be null!"

        return generate_output()

    if order_datetime == None:
        mess_result = "5_Order Date and Time can't be null!"

        return generate_output()
    active_order = True
    direct_post = False

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 222) &  (Queasy.number1 == 1) &  (Queasy.number2 == 15) &  (Queasy.betriebsnr == outlet_number)).first()

    if queasy:
        direct_post = queasy.logi1

    if room_number == None:
        room_number = ""

    if guest_number == None:
        guest_number = 0

    if res_number == None:
        res_number = 0

    if resline_number == None:
        resline_number = 0

    for menu_list in query(menu_list_list):

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 222) &  (Queasy.number1 == 2) &  (Queasy.number2 == menu_list.art_number) &  (Queasy.number3 == outlet_number)).first()

        if queasy:

            if queasy.logi2 :
                found_soldout = True
                break

    if found_soldout:
        mess_result = "6_One of Item Has SoldOut!"

        return generate_output()

    for sosqsy in db_session.query(Sosqsy).filter(
            (Sosqsy.key == 222) &  (Sosqsy.number1 == 1) &  (Sosqsy.betriebsnr == outlet_number)).all():

        if sosqsy.number2 == 14:
            dynamic_qr = sosqsy.logi1

        if sosqsy.number2 == 21:
            room_serviceflag = sosqsy.logi1
    recid_hbill = 0

    for buff_hbill in db_session.query(Buff_hbill).filter(
            (Buff_hbill.tischnr == table_nr) &  (Buff_hbill.departement == outlet_number) &  (Buff_hbill.flag == 1)).all():
        recid_hbill = buff_hbill._recid

        if recid_hbill != 0:
            break

    q_orderbill = db_session.query(Q_orderbill).filter(
            (Q_orderbill.key == 225) &  (func.lower(Q_orderbill.char1) == "orderbill") &  (Q_orderbill.number1 == outlet_number) &  (Q_orderbill.number2 == table_nr) &  (Q_orderbill.number3 == 0) &  (func.lower(Q_orderbill.char3) == (session_parameter).lower()) &  (Q_orderbill.betriebsnr == recid_hbill)).first()

    if q_orderbill:

        q_orderbill = db_session.query(Q_orderbill).first()
        db_session.delete(q_orderbill)


    if room_serviceflag:

        q_takentable = db_session.query(Q_takentable).filter(
                (Q_takentable.key == 225) &  (func.lower(Q_takentable.char1) == "taken_table") &  (Q_takentable.number2 == table_nr) &  (entry(0, Q_takentable.char3, "|Q_takentable.Q_takentable.") == (session_parameter).lower()) &  (num_entries(Q_takentable.char3, "|Q_takentable.Q_takentable.") == 3)).first()

        if q_takentable:
            str1 = entry(2, q_takentable.char3, "|")
            rm_no = entry(0, str1, "$")

        if rm_no != "":
            for count_i in range(65,90 + 1) :

                if re.match(".*" + chr(count_i,rm_no) + "*"):
                    alpha_flag = True

            if not alpha_flag:
                count_i = 0
                for count_i in range(97,122 + 1) :

                    if re.match(".*" + chr(count_i,rm_no) + "*"):
                        alpha_flag = True

    if alpha_flag:

        tisch = db_session.query(Tisch).filter(
                (Tisch.departement == outlet_number) &  (Tischnr == table_nr)).first()

        if tisch:
            room_no = substring(tisch.bezeich, 5)

        res_line = db_session.query(Res_line).filter(
                (Res_line.resstatus == 6) &  (func.lower(Res_line.zinr) == (room_no).lower())).first()
    else:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resstatus == 6) &  (Res_line.zinr == to_string(table_nr))).first()

    if res_line:
        res_number = res_line.resnr
        resline_number = res_line.reslinnr

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 225) &  (Queasy.number1 == outlet_number) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.number2 == table_nr) &  (Queasy.logi1 == active_order)).first()

    if queasy:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (Queasy.number1 == outlet_number) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.number2 == table_nr) &  (Queasy.logi1 == active_order)).all():
            orderbill_number = queasy.number3 + 1
            break
    else:
        orderbill_number = 1

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 225) &  (Queasy.number1 == outlet_number) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.number2 == table_nr) &  (Queasy.number3 == orderbill_number) &  (Queasy.date1 == date_mdy(order_datetime)) &  (Queasy.logi1 == active_order)).first()

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 225
        queasy.number1 = outlet_number
        queasy.number2 = table_nr
        queasy.number3 = orderbill_number
        queasy.char1 = "orderbill"
        queasy.char2 = "RN == " + room_number +\
                "|NM == " + guest_name +\
                "|DT == " + to_string(order_datetime) +\
                "|PX == " + to_string(pax) +\
                "|GN == " + to_string(guest_number) +\
                "|RS == " + to_string(res_number) +\
                "|RL == " + to_string(resline_number)
        queasy.date1 = date_mdy(order_datetime)
        queasy.logi1 = active_order
        queasy.logi3 = False
        queasy.char3 = session_parameter

        h_bill = db_session.query(H_bill).filter(
                (H_bill.flag == 0) &  (H_bill.tischnr == table_nr) &  (H_bill.departement == outlet_number)).first()

        if h_bill:
            queasy.betriebsnr = h_bill._recid
        else:
            queasy.betriebsnr = 0

        for menu_list in query(menu_list_list):
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 225
            queasy.number1 = orderbill_number
            queasy.number2 = table_nr
            queasy.number3 = menu_list.nr
            queasy.char1 = "orderbill_line"
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
            mess_result = "0_Posting Item Success"
    else:

        for menu_list in query(menu_list_list):
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 225
            queasy.number1 = orderbill_number
            queasy.number2 = table_nr
            queasy.number3 = menu_list.nr
            queasy.char1 = "orderbill_line"
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
            mess_result = "0_RePosting Item Success"

    return generate_output()