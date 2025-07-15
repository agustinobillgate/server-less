#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Hoteldpt, Bill, Bill_line, H_bill

def rest_rsvplan_btn_gobl(from_date:date, to_date:date, from_time:string, to_time:string, curr_dept:int, sorttype:int):

    prepare_cache ([Queasy, Htparam, Hoteldpt, Bill, Bill_line, H_bill])

    rsv_table_list_data = []
    tot_pax:int = 0
    tot_table:int = 0
    ns_billno:int = 0
    gastno:int = 0
    tot_depoamt:Decimal = to_decimal("0.0")
    tot_depopay:Decimal = to_decimal("0.0")
    depname:string = ""
    depoart:int = 0
    queasy = htparam = hoteldpt = bill = bill_line = h_bill = None

    rsv_table_list = q251 = None

    rsv_table_list_data, Rsv_table_list = create_model("Rsv_table_list", {"rec_id":int, "dept_no":int, "dept_name":string, "table_no":int, "guest_name":string, "telepon":string, "pax":int, "rsv_date":date, "f_time":string, "t_time":string, "deposit_amt":Decimal, "deposit_pay":Decimal, "depopay_date":date, "depopay_art":string, "remark":string, "usr_id":string, "ns_billno":string, "is_refund":string, "bill_no":string, "rsv_stat":string})

    Q251 = create_buffer("Q251",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rsv_table_list_data, tot_pax, tot_table, ns_billno, gastno, tot_depoamt, tot_depopay, depname, depoart, queasy, htparam, hoteldpt, bill, bill_line, h_bill
        nonlocal from_date, to_date, from_time, to_time, curr_dept, sorttype
        nonlocal q251


        nonlocal rsv_table_list, q251
        nonlocal rsv_table_list_data

        return {"rsv-table-list": rsv_table_list_data}

    def create_rsv_table():

        nonlocal rsv_table_list_data, tot_pax, tot_table, ns_billno, gastno, tot_depoamt, tot_depopay, depname, depoart, queasy, htparam, hoteldpt, bill, bill_line, h_bill
        nonlocal from_date, to_date, from_time, to_time, curr_dept, sorttype
        nonlocal q251


        nonlocal rsv_table_list, q251
        nonlocal rsv_table_list_data

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

        if hoteldpt:
            depname = hoteldpt.depart
        rsv_table_list = Rsv_table_list()
        rsv_table_list_data.append(rsv_table_list)

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
        rsv_table_list.deposit_amt =  to_decimal(queasy.deci1)
        rsv_table_list.remark = entry(1, queasy.char3, ";")
        rsv_table_list.usr_id = entry(0, queasy.char3, ";")
        rsv_table_list.ns_billno = to_string(queasy.deci2, ">>>>>>>")


        ns_billno = to_int(queasy.deci2)
        gastno = to_int(entry(2, queasy.char2, "&&"))

        bill = get_cache (Bill, {"rechnr": [(eq, ns_billno)],"gastnr": [(eq, gastno)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"billtyp": [(eq, curr_dept)],"flag": [(eq, 1)]})

        if bill:

            bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(ne, depoart)]})

            if bill_line:
                rsv_table_list.deposit_pay =  to_decimal(bill_line.betrag)
                rsv_table_list.depopay_date = bill_line.bill_datum
                rsv_table_list.depopay_art = bill_line.bezeich


                tot_depopay =  to_decimal(tot_depopay) + to_decimal(rsv_table_list.deposit_pay)

        q251 = get_cache (Queasy, {"key": [(eq, 251)],"number2": [(eq, to_int(queasy._recid))]})

        if q251:

            h_bill = get_cache (H_bill, {"_recid": [(eq, q251.number1)]})

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
        tot_depoamt =  to_decimal(tot_depoamt) + to_decimal(queasy.deci1)

    rsv_table_list_data.clear()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:
        depoart = htparam.finteger

    if sorttype == 0:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 33) & (Queasy.number1 == curr_dept) & (Queasy.date1 >= from_date) & (Queasy.date1 <= to_date) & (to_int(substring(Queasy.char1, 0, 4)) < to_int(to_time)) & (to_int(substring(Queasy.char1, 4, 4)) > to_int(from_time)) & (Queasy.logi3) & (Queasy.betriebsnr == 0)).order_by(Queasy.date1, Queasy.number1).all():
            create_rsv_table()

    elif sorttype == 1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 33) & (Queasy.number1 == curr_dept) & (Queasy.date1 >= from_date) & (Queasy.date1 <= to_date) & (to_int(substring(Queasy.char1, 0, 4)) < to_int(to_time)) & (to_int(substring(Queasy.char1, 4, 4)) > to_int(from_time)) & (Queasy.logi3) & (Queasy.betriebsnr == 1)).order_by(Queasy.date1, Queasy.number1).all():
            create_rsv_table()

    elif sorttype == 2:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 33) & (Queasy.number1 == curr_dept) & (Queasy.date1 >= from_date) & (Queasy.date1 <= to_date) & (to_int(substring(Queasy.char1, 0, 4)) < to_int(to_time)) & (to_int(substring(Queasy.char1, 4, 4)) > to_int(from_time)) & not_ (Queasy.logi3) & (Queasy.betriebsnr == 2)).order_by(Queasy.date1, Queasy.number1).all():
            create_rsv_table()

    elif sorttype == 3:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 33) & (Queasy.number1 == curr_dept) & (Queasy.date1 >= from_date) & (Queasy.date1 <= to_date) & (to_int(substring(Queasy.char1, 0, 4)) < to_int(to_time)) & (to_int(substring(Queasy.char1, 4, 4)) > to_int(from_time)) & not_ (Queasy.logi3) & (Queasy.betriebsnr == 3)).order_by(Queasy.date1, Queasy.number1).all():
            create_rsv_table()

    elif sorttype == 4:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 33) & (Queasy.number1 == curr_dept) & (Queasy.date1 >= from_date) & (Queasy.date1 <= to_date) & (to_int(substring(Queasy.char1, 0, 4)) < to_int(to_time)) & (to_int(substring(Queasy.char1, 4, 4)) > to_int(from_time))).order_by(Queasy.date1, Queasy.number1).all():
            create_rsv_table()

    rsv_table_list = query(rsv_table_list_data, first=True)

    if rsv_table_list:
        rsv_table_list = Rsv_table_list()
        rsv_table_list_data.append(rsv_table_list)

        rsv_table_list.dept_name = "T O T A L"
        rsv_table_list.table_no = tot_table
        rsv_table_list.pax = tot_pax
        rsv_table_list.deposit_amt =  to_decimal(tot_depoamt)
        rsv_table_list.deposit_pay =  to_decimal(tot_depopay)

    return generate_output()