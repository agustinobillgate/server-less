from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Htparam, Hoteldpt, Bill, Bill_line, H_bill

def rest_rsvplan_btn_gobl(from_date:date, to_date:date, from_time:str, to_time:str, curr_dept:int, sorttype:int):
    rsv_table_list_list = []
    tot_pax:int = 0
    tot_table:int = 0
    ns_billno:int = 0
    gastno:int = 0
    tot_depoamt:decimal = 0
    tot_depopay:decimal = 0
    depname:str = ""
    depoart:int = 0
    queasy = htparam = hoteldpt = bill = bill_line = h_bill = None

    rsv_table_list = q251 = None

    rsv_table_list_list, Rsv_table_list = create_model("Rsv_table_list", {"rec_id":int, "dept_no":int, "dept_name":str, "table_no":int, "guest_name":str, "telepon":str, "pax":int, "rsv_date":date, "f_time":str, "t_time":str, "deposit_amt":decimal, "deposit_pay":decimal, "depopay_date":date, "depopay_art":str, "remark":str, "usr_id":str, "ns_billno":str, "is_refund":str, "bill_no":str, "rsv_stat":str})

    Q251 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rsv_table_list_list, tot_pax, tot_table, ns_billno, gastno, tot_depoamt, tot_depopay, depname, depoart, queasy, htparam, hoteldpt, bill, bill_line, h_bill
        nonlocal q251


        nonlocal rsv_table_list, q251
        nonlocal rsv_table_list_list
        return {"rsv-table-list": rsv_table_list_list}

    def create_rsv_table():

        nonlocal rsv_table_list_list, tot_pax, tot_table, ns_billno, gastno, tot_depoamt, tot_depopay, depname, depoart, queasy, htparam, hoteldpt, bill, bill_line, h_bill
        nonlocal q251


        nonlocal rsv_table_list, q251
        nonlocal rsv_table_list_list

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == curr_dept)).first()

        if hoteldpt:
            depname = hoteldpt.depart
        rsv_table_list = Rsv_table_list()
        rsv_table_list_list.append(rsv_table_list)

        rsv_table_list.rec_id = queasy._recid
        rsv_table_list.dept_no = queasy.number1
        rsv_table_list.dept_name = depname
        rsv_table_list.table_no = queasy.number2
        rsv_table_list.guest_name = entry(0, queasy.char2, "&&")
        rsv_table_list.telepon = entry(1, queasy.char1, ";")
        rsv_table_list.pax = queasy.number3
        rsv_table_list.rsv_date = queasy.date1
        rsv_table_list.f_time = substring(queasy.char1, 0, 4)
        rsv_table_list.t_time = substring(queasy.char1, 4, 4)
        rsv_table_list.deposit_amt = queasy.deci1
        rsv_table_list.remark = entry(1, queasy.char3, ";")
        rsv_table_list.usr_id = entry(0, queasy.char3, ";")
        rsv_table_list.ns_billno = to_string(queasy.deci2, ">>>>>>>")


        ns_billno = to_int(queasy.deci2)
        gastno = to_int(entry(2, queasy.char2, "&&"))

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == ns_billno) &  (Bill.gastnr == gastno) &  (Bill.resnr == 0) &  (Bill.reslinnr == 1) &  (Billtyp == curr_dept) &  (Bill.flag == 1)).first()

        if bill:

            bill_line = db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill.rechnr) &  (Bill_line.artnr != depoart)).first()

            if bill_line:
                rsv_table_list.deposit_pay = bill_line.betrag
                rsv_table_list.depopay_date = bill_line.bill_datum
                rsv_table_list.depopay_art = bill_line.bezeich


                tot_depopay = tot_depopay + rsv_table_list.deposit_pay

        q251 = db_session.query(Q251).filter(
                (Q251.key == 251) &  (Q251.number2 == to_int(queasy._recid))).first()

        if q251:

            h_bill = db_session.query(H_bill).filter(
                    (H_bill._recid == q251.number1)).first()

            if h_bill:
                rsv_table_list.bill_no = to_string(h_bill.rechnr, ">>>>>>>")

        if sorttype == 0:
            rsv_table_list.rsv_stat = "Open"

        elif sorttype == 1:
            rsv_table_list.rsv_stat = "Close"

        elif sorttype == 2:
            rsv_table_list.rsv_stat = "Cancel"

        elif sorttype == 3:
            rsv_table_list.rsv_stat = "Expired"

        elif sorttype == 4:

            if queasy.logi3 and queasy.betriebsnr == 0:
                rsv_table_list.rsv_stat = "Open"

            elif queasy.logi3 and queasy.betriebsnr == 1:
                rsv_table_list.rsv_stat = "Close"

            elif not queasy.logi3 and queasy.betriebsnr == 2:
                rsv_table_list.rsv_stat = "Cancel"

            elif not queasy.logi3 and queasy.betriebsnr == 3:
                rsv_table_list.rsv_stat = "Expired"
        tot_pax = tot_pax + queasy.number3
        tot_table = tot_table + 1
        tot_depoamt = tot_depoamt + queasy.deci1


    rsv_table_list_list.clear()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1361)).first()

    if htparam:
        depoart = htparam.finteger

    if sorttype == 0:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 33) &  (Queasy.number1 == curr_dept) &  (Queasy.date1 >= from_date) &  (Queasy.date1 <= to_date) &  (to_int(substring(Queasy.char1, 0, 4)) < to_int(to_time)) &  (to_int(substring(Queasy.char1, 4, 4)) > to_int(from_time)) &  (Queasy.logi3) &  (Queasy.betriebsnr == 0)).all():
            create_rsv_table()

    elif sorttype == 1:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 33) &  (Queasy.number1 == curr_dept) &  (Queasy.date1 >= from_date) &  (Queasy.date1 <= to_date) &  (to_int(substring(Queasy.char1, 0, 4)) < to_int(to_time)) &  (to_int(substring(Queasy.char1, 4, 4)) > to_int(from_time)) &  (Queasy.logi3) &  (Queasy.betriebsnr == 1)).all():
            create_rsv_table()

    elif sorttype == 2:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 33) &  (Queasy.number1 == curr_dept) &  (Queasy.date1 >= from_date) &  (Queasy.date1 <= to_date) &  (to_int(substring(Queasy.char1, 0, 4)) < to_int(to_time)) &  (to_int(substring(Queasy.char1, 4, 4)) > to_int(from_time)) &  (not Queasy.logi3) &  (Queasy.betriebsnr == 2)).all():
            create_rsv_table()

    elif sorttype == 3:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 33) &  (Queasy.number1 == curr_dept) &  (Queasy.date1 >= from_date) &  (Queasy.date1 <= to_date) &  (to_int(substring(Queasy.char1, 0, 4)) < to_int(to_time)) &  (to_int(substring(Queasy.char1, 4, 4)) > to_int(from_time)) &  (not Queasy.logi3) &  (Queasy.betriebsnr == 3)).all():
            create_rsv_table()

    elif sorttype == 4:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 33) &  (Queasy.number1 == curr_dept) &  (Queasy.date1 >= from_date) &  (Queasy.date1 <= to_date) &  (to_int(substring(Queasy.char1, 0, 4)) < to_int(to_time)) &  (to_int(substring(Queasy.char1, 4, 4)) > to_int(from_time))).all():
            create_rsv_table()

    rsv_table_list = query(rsv_table_list_list, first=True)

    if rsv_table_list:
        rsv_table_list = Rsv_table_list()
        rsv_table_list_list.append(rsv_table_list)

        rsv_table_list.dept_name = "T O T A L"
        rsv_table_list.table_no = tot_table
        rsv_table_list.pax = tot_pax
        rsv_table_list.deposit_amt = tot_depoamt
        rsv_table_list.deposit_pay = tot_depopay

    return generate_output()