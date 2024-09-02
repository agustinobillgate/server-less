from functions.additional_functions import *
import decimal
from sqlalchemy import func
import re
from models import Queasy, H_bill, Hoteldpt, Tisch, Kellner, Res_line

def pos_dashboard_opened_tischbl(dept:int):
    t_list_list = []
    pick_table_list = []
    tot_saldo:decimal = 0
    pax:int = 0
    orderdatetime:str = ""
    gname:str = ""
    room:str = ""
    gastnr:int = 0
    resnr:int = 0
    reslinnr:int = 0
    mess_str:str = ""
    i_str:int = 0
    mess_token:str = ""
    mess_keyword:str = ""
    mess_value:str = ""
    table_no:int = 0
    dtime: = None
    dynamic_qr:bool = False
    asroom_service:bool = False
    validate_room:str = ""
    validate_name:str = ""
    validate_rechnr:int = 0
    found_it:bool = False
    session_params:str = ""
    billnumber:int = 0
    queasy = h_bill = hoteldpt = tisch = kellner = res_line = None

    t_list = pick_table = qsy230 = session_table = posted_item = queasy223 = orderbill = None

    t_list_list, T_list = create_model("T_list", {"dept":int, "tischnr":int, "bezeich":str, "normalbeleg":int, "name":str, "occupied":bool, "belegung":int, "balance":decimal, "zinr":str, "gname":str, "ask_bill":bool, "bill_print":bool, "platform":str, "allow_ctr":str, "bill_number":int, "pay_status":str})
    pick_table_list, Pick_table = create_model("Pick_table", {"dept":int, "tableno":int, "pax":int, "gname":str, "occupied":bool, "session_parameter":str, "gemail":str, "active_session":bool, "dataqr":str, "date_time":})

    Qsy230 = Queasy
    Session_table = Queasy
    Posted_item = Queasy
    Queasy223 = Queasy
    Orderbill = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, pick_table_list, tot_saldo, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, dynamic_qr, asroom_service, validate_room, validate_name, validate_rechnr, found_it, session_params, billnumber, queasy, h_bill, hoteldpt, tisch, kellner, res_line
        nonlocal qsy230, session_table, posted_item, queasy223, orderbill


        nonlocal t_list, pick_table, qsy230, session_table, posted_item, queasy223, orderbill
        nonlocal t_list_list, pick_table_list
        return {"t-list": t_list_list, "pick-table": pick_table_list}

    def create_list():

        nonlocal t_list_list, pick_table_list, tot_saldo, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, dynamic_qr, asroom_service, validate_room, validate_name, validate_rechnr, found_it, session_params, billnumber, queasy, h_bill, hoteldpt, tisch, kellner, res_line
        nonlocal qsy230, session_table, posted_item, queasy223, orderbill


        nonlocal t_list, pick_table, qsy230, session_table, posted_item, queasy223, orderbill
        nonlocal t_list_list, pick_table_list


        mess_str = queasy.char2
        for i_str in range(1,num_entries(mess_str, "|")  + 1) :
            mess_token = entry(i_str - 1, mess_str, "|")
            mess_keyword = entry(0, mess_token, " == ")
            mess_value = entry(1, mess_token, " == ")

            if mess_keyword.lower()  == "PX":
                pax = to_int(mess_value)

            elif mess_keyword.lower()  == "NM":
                gname = mess_value

            elif mess_keyword.lower()  == "TB":
                table_no = int (mess_value)

            elif mess_keyword.lower()  == "TM":
                dtime = DATETIME (mess_value)
        pick_table = Pick_table()
        pick_table_list.append(pick_table)

        pick_table.dept = queasy.number1
        pick_table.tableno = queasy.number2
        pick_table.pax = pax
        pick_table.gname = gname
        pick_table.occupied = queasy.logi3
        pick_table.session_parameter = entry(0, queasy.char3, "|")
        pick_table.dataQr = entry(1, queasy.char3, "|")
        pick_table.date_time = dtime


        validate_rechnr = 0

        posted_item = db_session.query(Posted_item).filter(
                (Posted_item.key == 225) &  (func.lower(Posted_item.char1) == "orderbill") &  (Posted_item.char3 == entry(0, queasy.char3, "|"))).first()
        while None != posted_item:
            mess_str = posted_item.char2
            for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                mess_token = entry(i_str - 1, mess_str, "|")
                mess_keyword = entry(0, mess_token, " == ")
                mess_value = entry(1, mess_token, " == ")

                if mess_keyword.lower()  == "BL":
                    validate_rechnr = to_int(mess_value)

                if validate_rechnr != 0:
                    return

            posted_item = db_session.query(Posted_item).filter(
                    (Posted_item.key == 225) &  (func.lower(Posted_item.char1) == "orderbill") &  (Posted_item.char3 == entry(0, queasy.char3, "|"))).first()

        if validate_rechnr != 0:
            pick_table.occupied = True
        else:
            pick_table.occupied = False

        session_table = db_session.query(Session_table).filter(
                (Session_table.key == 230) &  (Session_table.char1 == entry(0, queasy.char3, "|"))).first()

        if session_table:
            pick_table.gemail = entry(1, session_table.char2, "|")
            pick_table.active_session = session_table.logi1

    def build_list0():

        nonlocal t_list_list, pick_table_list, tot_saldo, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, dynamic_qr, asroom_service, validate_room, validate_name, validate_rechnr, found_it, session_params, billnumber, queasy, h_bill, hoteldpt, tisch, kellner, res_line
        nonlocal qsy230, session_table, posted_item, queasy223, orderbill


        nonlocal t_list, pick_table, qsy230, session_table, posted_item, queasy223, orderbill
        nonlocal t_list_list, pick_table_list

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num > 0)).all():

            tisch_obj_list = []
            for tisch, h_bill in db_session.query(Tisch, H_bill).join(H_bill,(H_bill.departement == hoteldpt.num) &  (H_bill.tisch == Tischnr) &  (H_bill.flag == 0)).filter(
                    (Tisch.departement == hoteldpt.num)).all():
                if tisch._recid in tisch_obj_list:
                    continue
                else:
                    tisch_obj_list.append(tisch._recid)


                t_list = T_list()
                t_list_list.append(t_list)

                t_list.dept = hoteldpt.num
                t_list.tischnr = tischnr
                t_list.bezeich = tisch.bezeich
                t_list.normalbeleg = tisch.normalbeleg
                t_list.occupied = True
                t_list.belegung = h_bill.belegung
                t_list.gname = h_bill.bilname
                t_list.balance = h_bill.saldo
                t_list.bill_print = logical(h_bill.rgdruck)
                t_list.bill_number = h_bill.rechnr

                kellner = db_session.query(Kellner).filter(
                        (Kellner_nr == h_bill.kellner_nr) &  (Kellner.departement == dept)).first()

                if kellner:
                    t_list.name = kellnername

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

                if res_line:
                    t_list.zinr = res_line.zinr
                    t_list.gname = res_line.name

                    if res_line.zinr != "":

                        if res_line.CODE != "":

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                            if queasy and queasy.logi1 :
                                t_list.allow_ctr = "Not Allowed"
                            else:
                                t_list.allow_ctr = "Allowed"
                tot_saldo = tot_saldo + h_bill.saldo

    def build_list():

        nonlocal t_list_list, pick_table_list, tot_saldo, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, dynamic_qr, asroom_service, validate_room, validate_name, validate_rechnr, found_it, session_params, billnumber, queasy, h_bill, hoteldpt, tisch, kellner, res_line
        nonlocal qsy230, session_table, posted_item, queasy223, orderbill


        nonlocal t_list, pick_table, qsy230, session_table, posted_item, queasy223, orderbill
        nonlocal t_list_list, pick_table_list

        tisch_obj_list = []
        for tisch, h_bill in db_session.query(Tisch, H_bill).join(H_bill,(H_bill.departement == dept) &  (H_bill.tisch == Tischnr) &  (H_bill.flag == 0)).filter(
                (Tisch.departement == dept)).all():
            if tisch._recid in tisch_obj_list:
                continue
            else:
                tisch_obj_list.append(tisch._recid)


            t_list = T_list()
            t_list_list.append(t_list)

            t_list.dept = dept
            t_list.tischnr = tischnr
            t_list.bezeich = tisch.bezeich
            t_list.normalbeleg = tisch.normalbeleg
            t_list.occupied = True
            t_list.belegung = h_bill.belegung
            t_list.gname = h_bill.bilname
            t_list.balance = h_bill.saldo
            t_list.bill_print = logical(h_bill.rgdruck)
            t_list.bill_number = h_bill.rechnr

            kellner = db_session.query(Kellner).filter(
                    (Kellner_nr == h_bill.kellner_nr) &  (Kellner.departement == dept)).first()

            if kellner:
                t_list.name = kellnername

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

            if res_line:
                t_list.zinr = res_line.zinr
                t_list.gname = res_line.name

                if res_line.zinr != "":

                    if res_line.CODE != "":

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                        if queasy and queasy.logi1 :
                            t_list.allow_ctr = "Not Allowed"
                        else:
                            t_list.allow_ctr = "Allowed"
            tot_saldo = tot_saldo + h_bill.saldo


    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 222) &  (Queasy.number1 == 1) &  (Queasy.betriebsnr == dept)).all():

        if queasy.number2 == 14:
            dynamic_qr = queasy.logi1

        if queasy.number2 == 21:
            asroom_service = queasy.logi1

    if dept > 0:
        build_list()
    else:
        build_list0()

    if dynamic_qr:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (func.lower(Queasy.char1) == "taken_table") &  (Queasy.number1 == dept) &  (Queasy.logi1) &  (Queasy.logi2)).first()
        while None != queasy:
            create_list()

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 225) &  (func.lower(Queasy.char1) == "taken_table") &  (Queasy.number1 == dept) &  (Queasy.logi1) &  (Queasy.logi2)).first()
    else:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (func.lower(Queasy.char1) == "taken_table") &  (Queasy.number1 == dept) &  (Queasy.logi1) &  (Queasy.logi2 == False)).first()
        while None != queasy:
            create_list()

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 225) &  (func.lower(Queasy.char1) == "taken_table") &  (Queasy.number1 == dept) &  (Queasy.logi1) &  (Queasy.logi2 == False)).first()

    for t_list in query(t_list_list):

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (Queasy.number1 == dept) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.number2 == t_list.tischnr) &  (Queasy.logi1) &  (Queasy.char3 != "")).first()

        if queasy:
            session_params = queasy.char3
            mess_str = queasy.char2
            for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                mess_token = entry(i_str - 1, mess_str, "|")
                mess_keyword = entry(0, mess_token, " == ")
                mess_value = entry(1, mess_token, " == ")

                if mess_keyword.lower()  == "BL":
                    validate_rechnr = to_int(mess_value)

                elif mess_keyword.lower()  == "RN":
                    validate_room = mess_value

                elif mess_keyword.lower()  == "NM":
                    validate_name = mess_value

            h_bill = db_session.query(H_bill).filter(
                    (H_bill.departement == dept) &  (H_bill.rechnr == validate_rechnr)).first()

            if h_bill:

                if h_bill.flag != 0:
                    queasy.logi1 = False
            found_it = False

            if (validate_room == t_list.zinr):
                found_it = True

            if not found_it:

                if num_entries(validate_name, ",") >= 1:
                    validate_name = entry(0, validate_name, ",")

                if re.match(".*" + validate_name + ".*",t_list.gname):
                    found_it = True

            if not found_it:
                validate_room = to_string(queasy.number2)

                if (validate_room == t_list.zinr):
                    found_it = True

            if found_it:
                t_list.platform = "Self Order"
                t_list.ask_bill = queasy.logi2
            else:
                t_list.platform = "Waiter Order"

            queasy223 = db_session.query(Queasy223).filter(
                    (Queasy223.key == 223) &  (Queasy223.number1 == dept) &  (func.lower(Queasy223.char3) == (session_params).lower())).first()

            if queasy223:
                t_list.pay_status = queasy223.char1
        else:
            t_list.platform = "Waiter Order"

        if t_list.allow_ctr == "":
            t_list.allow_ctr = "Not Allowed"

    for pick_table in query(pick_table_list):

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (Queasy.number1 == pick_table.dept) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.char3 == pick_table.session_parameter)).first()

        if queasy:

            if queasy.betriebsnr != 0:

                for orderbill in db_session.query(Orderbill).filter(
                        (Orderbill.key == 225) &  (func.lower(Orderbill.char1) == "orderbill") &  (Orderbill.number1 == queasy.number1) &  (Orderbill.char3 == queasy.char3) &  (Orderbill.betriebsnr != 0)).all():
                    mess_str = orderbill.char2
                    for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                        mess_token = entry(i_str - 1, mess_str, "|")
                        mess_keyword = entry(0, mess_token, " == ")
                        mess_value = entry(1, mess_token, " == ")

                        if mess_keyword.lower()  == "BL":
                            billnumber = to_int(mess_value)
                            break

                    if billnumber != 0:
                        break

                h_bill = db_session.query(H_bill).filter(
                        (H_bill.rechnr == billnumber) &  (H_bill.departement == dept)).first()

                if h_bill and h_bill.flag == 1:
                    pick_table_list.remove(pick_table)
                billnumber = 0
            else:

                if not queasy.logi1:
                    pick_table_list.remove(pick_table)
        else:

            if dynamic_qr:

                if num_entries(pick_table.session_parameter, ";") > 1:
                    pick_table_list.remove(pick_table)
                else:

                    if len(pick_table.session_parameter) > 20:
                        pick_table_list.remove(pick_table)

    return generate_output()