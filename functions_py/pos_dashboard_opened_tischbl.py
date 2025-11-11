#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, H_bill, Hoteldpt, Tisch, Kellner, Res_line

def pos_dashboard_opened_tischbl(dept:int):

    prepare_cache ([Queasy, H_bill, Hoteldpt, Tisch, Kellner, Res_line])

    t_list_data = []
    pick_table_data = []
    tot_saldo:Decimal = to_decimal("0.0")
    pax:int = 0
    orderdatetime:string = ""
    gname:string = ""
    room:string = ""
    gastnr:int = 0
    resnr:int = 0
    reslinnr:int = 0
    mess_str:string = ""
    i_str:int = 0
    mess_token:string = ""
    mess_keyword:string = ""
    mess_value:string = ""
    table_no:int = 0
    dtime:datetime = None
    dynamic_qr:bool = False
    asroom_service:bool = False
    validate_room:string = ""
    validate_name:string = ""
    validate_rechnr:int = 0
    found_it:bool = False
    session_params:string = ""
    billnumber:int = 0
    queasy = h_bill = hoteldpt = tisch = kellner = res_line = None

    t_list = pick_table = qsy230 = session_table = posted_item = queasy223 = orderbill = None

    t_list_data, T_list = create_model("T_list", {"dept":int, "tischnr":int, "bezeich":string, "normalbeleg":int, "name":string, "occupied":bool, "belegung":int, "balance":Decimal, "zinr":string, "gname":string, "ask_bill":bool, "bill_print":bool, "platform":string, "allow_ctr":string, "bill_number":int, "pay_status":string})
    pick_table_data, Pick_table = create_model("Pick_table", {"dept":int, "tableno":int, "pax":int, "gname":string, "occupied":bool, "session_parameter":string, "gemail":string, "active_session":bool, "dataqr":string, "date_time":datetime})

    Qsy230 = create_buffer("Qsy230",Queasy)
    Session_table = create_buffer("Session_table",Queasy)
    Posted_item = create_buffer("Posted_item",Queasy)
    Queasy223 = create_buffer("Queasy223",Queasy)
    Orderbill = create_buffer("Orderbill",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_data, pick_table_data, tot_saldo, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, dynamic_qr, asroom_service, validate_room, validate_name, validate_rechnr, found_it, session_params, billnumber, queasy, h_bill, hoteldpt, tisch, kellner, res_line
        nonlocal dept
        nonlocal qsy230, session_table, posted_item, queasy223, orderbill


        nonlocal t_list, pick_table, qsy230, session_table, posted_item, queasy223, orderbill
        nonlocal t_list_data, pick_table_data

        return {"t-list": t_list_data, "pick-table": pick_table_data}

    def create_list():

        nonlocal t_list_data, pick_table_data, tot_saldo, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, dynamic_qr, asroom_service, validate_room, validate_name, validate_rechnr, found_it, session_params, billnumber, queasy, h_bill, hoteldpt, tisch, kellner, res_line
        nonlocal dept
        nonlocal qsy230, session_table, posted_item, queasy223, orderbill


        nonlocal t_list, pick_table, qsy230, session_table, posted_item, queasy223, orderbill
        nonlocal t_list_data, pick_table_data


        mess_str = queasy.char2
        for i_str in range(1,num_entries(mess_str, "|")  + 1) :
            mess_token = entry(i_str - 1, mess_str, "|")
            mess_keyword = entry(0, mess_token, "=")
            mess_value = entry(1, mess_token, "=")

            if mess_keyword.lower()  == ("PX").lower() :
                pax = to_int(mess_value)

            elif mess_keyword.lower()  == ("NM").lower() :
                gname = mess_value

            elif mess_keyword.lower()  == ("TB").lower() :
                table_no = int (mess_value)

            elif mess_keyword.lower()  == ("TM").lower() :
                dtime = to_datetime(mess_value)
        pick_table = Pick_table()
        pick_table_data.append(pick_table)

        pick_table.dept = queasy.number1
        pick_table.tableno = queasy.number2
        pick_table.pax = pax
        pick_table.gname = gname
        pick_table.occupied = queasy.logi3
        pick_table.session_parameter = entry(0, queasy.char3, "|")
        pick_table.dataqr = entry(1, queasy.char3, "|")
        pick_table.date_time = dtime


        validate_rechnr = 0

        posted_item = db_session.query(Posted_item).filter(
                 (Posted_item.key == 225) & (Posted_item.char1 == ("orderbill").lower()) & (Posted_item.char3 == entry(0, queasy.char3, "|")) & (Posted_item.number1 == queasy.number1) & (Posted_item.betriebsnr != 0) & (Posted_item.logi1)).first()

        if posted_item:
            validate_rechnr = posted_item.betriebsnr

            if validate_rechnr != 0:
                pick_table.occupied = True
            else:
                pick_table.occupied = False


    def build_list0():

        nonlocal t_list_data, pick_table_data, tot_saldo, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, dynamic_qr, asroom_service, validate_room, validate_name, validate_rechnr, found_it, session_params, billnumber, queasy, h_bill, hoteldpt, tisch, kellner, res_line
        nonlocal dept
        nonlocal qsy230, session_table, posted_item, queasy223, orderbill


        nonlocal t_list, pick_table, qsy230, session_table, posted_item, queasy223, orderbill
        nonlocal t_list_data, pick_table_data

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num > 0)).order_by(Hoteldpt._recid).all():

            tisch_obj_list = {}
            tisch = Tisch()
            h_bill = H_bill()
            for tisch.tischnr, tisch.bezeich, tisch.normalbeleg, tisch._recid, h_bill.belegung, h_bill.bilname, h_bill.saldo, h_bill.rgdruck, h_bill.rechnr, h_bill.kellner_nr, h_bill.resnr, h_bill.reslinnr, h_bill.flag, h_bill._recid in db_session.query(Tisch.tischnr, Tisch.bezeich, Tisch.normalbeleg, Tisch._recid, H_bill.belegung, H_bill.bilname, H_bill.saldo, H_bill.rgdruck, H_bill.rechnr, H_bill.kellner_nr, H_bill.resnr, H_bill.reslinnr, H_bill.flag, H_bill._recid).join(H_bill,(H_bill.departement == hoteldpt.num) & (H_bill.tischnr == Tisch.tischnr) & (H_bill.flag == 0)).filter(
                     (Tisch.departement == hoteldpt.num)).order_by(Tisch.tischnr).all():
                if tisch_obj_list.get(tisch._recid):
                    continue
                else:
                    tisch_obj_list[tisch._recid] = True


                t_list = T_list()
                t_list_data.append(t_list)

                t_list.dept = hoteldpt.num
                t_list.tischnr = tisch.tischnr
                t_list.bezeich = tisch.bezeich
                t_list.normalbeleg = tisch.normalbeleg
                t_list.occupied = True
                t_list.belegung = h_bill.belegung
                t_list.gname = h_bill.bilname
                t_list.balance =  to_decimal(h_bill.saldo)
                t_list.bill_print = logical(h_bill.rgdruck)
                t_list.bill_number = h_bill.rechnr

                kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, dept)]})

                if kellner:
                    t_list.name = kellner.kellnername

                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                if res_line:
                    t_list.zinr = res_line.zinr
                    t_list.gname = res_line.name

                    if res_line.zinr != "":

                        if res_line.code != "":

                            queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code.strip()))]})

                            if queasy and queasy.logi1 :
                                t_list.allow_ctr = "Not Allowed"
                            else:
                                t_list.allow_ctr = "Allowed"
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(h_bill.saldo)


    def build_list():

        nonlocal t_list_data, pick_table_data, tot_saldo, pax, orderdatetime, gname, room, gastnr, resnr, reslinnr, mess_str, i_str, mess_token, mess_keyword, mess_value, table_no, dtime, dynamic_qr, asroom_service, validate_room, validate_name, validate_rechnr, found_it, session_params, billnumber, queasy, h_bill, hoteldpt, tisch, kellner, res_line
        nonlocal dept
        nonlocal qsy230, session_table, posted_item, queasy223, orderbill


        nonlocal t_list, pick_table, qsy230, session_table, posted_item, queasy223, orderbill
        nonlocal t_list_data, pick_table_data

        tisch_obj_list = {}
        tisch = Tisch()
        h_bill = H_bill()
        for tisch.tischnr, tisch.bezeich, tisch.normalbeleg, tisch._recid, h_bill.belegung, h_bill.bilname, h_bill.saldo, h_bill.rgdruck, h_bill.rechnr, h_bill.kellner_nr, h_bill.resnr, h_bill.reslinnr, h_bill.flag, h_bill._recid in db_session.query(Tisch.tischnr, Tisch.bezeich, Tisch.normalbeleg, Tisch._recid, H_bill.belegung, H_bill.bilname, H_bill.saldo, H_bill.rgdruck, H_bill.rechnr, H_bill.kellner_nr, H_bill.resnr, H_bill.reslinnr, H_bill.flag, H_bill._recid).join(H_bill,(H_bill.departement == dept) & (H_bill.tischnr == Tisch.tischnr) & (H_bill.flag == 0)).filter(
                 (Tisch.departement == dept)).order_by(Tisch.tischnr).all():
            if tisch_obj_list.get(tisch._recid):
                continue
            else:
                tisch_obj_list[tisch._recid] = True


            t_list = T_list()
            t_list_data.append(t_list)

            t_list.dept = dept
            t_list.tischnr = tisch.tischnr
            t_list.bezeich = tisch.bezeich
            t_list.normalbeleg = tisch.normalbeleg
            t_list.occupied = True
            t_list.belegung = h_bill.belegung
            t_list.gname = h_bill.bilname
            t_list.balance =  to_decimal(h_bill.saldo)
            t_list.bill_print = logical(h_bill.rgdruck)
            t_list.bill_number = h_bill.rechnr

            kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, dept)]})

            if kellner:
                t_list.name = kellner.kellnername

            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

            if res_line:
                t_list.zinr = res_line.zinr
                t_list.gname = res_line.name

                if res_line.zinr != "":

                    if res_line.code != "":

                        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code.strip()))]})

                        if queasy and queasy.logi1 :
                            t_list.allow_ctr = "Not Allowed"
                        else:
                            t_list.allow_ctr = "Allowed"
            tot_saldo =  to_decimal(tot_saldo) + to_decimal(h_bill.saldo)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.betriebsnr == dept)).order_by(Queasy._recid).all():

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
                 (Queasy.key == 225) & (Queasy.char1 == ("taken-table").lower()) & (Queasy.number1 == dept) & (Queasy.logi1) & (Queasy.logi2) & (length(entry(0, Queasy.char3, "|")) <= 20)).first()
        while None != queasy:
            create_list()

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 225) & (Queasy.char1 == ("taken-table").lower()) & (Queasy.number1 == dept) & (Queasy.logi1) & (Queasy.logi2) & (length(entry(0, Queasy.char3, "|")) <= 20) & (Queasy._recid > curr_recid)).first()
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "taken-table")],"number1": [(eq, dept)],"logi1": [(eq, True)],"logi2": [(eq, False)]})
        while None != queasy:
            create_list()

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 225) & (Queasy.char1 == ("taken-table").lower()) & (Queasy.number1 == dept) & (Queasy.logi1) & (Queasy.logi2 == False) & (Queasy._recid > curr_recid)).first()
        pass

    for t_list in query(t_list_data):

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 225) & (Queasy.number1 == dept) & (Queasy.char1 == ("orderbill").lower()) & (Queasy.number2 == t_list.tischnr) & (Queasy.logi1) & (Queasy.char3 != "") & (Queasy.logi2)).first()

        if queasy:
            pass
            session_params = queasy.char3
            mess_str = queasy.char2
            for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                mess_token = entry(i_str - 1, mess_str, "|")
                mess_keyword = entry(0, mess_token, "=")
                mess_value = entry(1, mess_token, "=")

                if mess_keyword.lower()  == ("BL").lower() :
                    validate_rechnr = to_int(mess_value)

                elif mess_keyword.lower()  == ("RN").lower() :
                    validate_room = mess_value

                elif mess_keyword.lower()  == ("NM").lower() :
                    validate_name = mess_value

            h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"rechnr": [(eq, validate_rechnr)]})

            if h_bill:

                if h_bill.flag != 0:
                    queasy.logi1 = False
            found_it = False

            if (validate_room == t_list.zinr):
                found_it = True

            if not found_it:

                if num_entries(validate_name, ",") >= 1:
                    validate_name = entry(0, validate_name, ",")

                if matches(t_list.gname,r"*" + validate_name + r"*"):
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

            queasy223 = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, dept)],"char3": [(eq, session_params)]})

            if queasy223:
                t_list.pay_status = queasy223.char1

            if t_list.allow_ctr == "":
                t_list.allow_ctr = "Not Allowed"
            pass
            pass
        else:
            t_list_data.remove(t_list)

    if dynamic_qr:

        for pick_table in query(pick_table_data, filters=(lambda pick_table: pick_table.length(pick_table.session_parameter) > 20)):
            pick_table_data.remove(pick_table)
    else:
        pass

    return generate_output()