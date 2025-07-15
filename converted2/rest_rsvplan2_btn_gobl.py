#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Hoteldpt, Guest

def rest_rsvplan2_btn_gobl(from_date:date, to_date:date, sorttype:int):

    prepare_cache ([Queasy, Hoteldpt, Guest])

    rsv_table_list_data = []
    doit:bool = False
    rstatus:List[string] = create_empty_list(4,"")
    queasy = hoteldpt = guest = None

    rsv_table_list = bqueasy = None

    rsv_table_list_data, Rsv_table_list = create_model("Rsv_table_list", {"rec_id":int, "bookingdate":date, "reservationno":int, "guestid":int, "guestname":string, "guestemail":string, "guestphone":string, "depositamount":Decimal, "paymentamount":Decimal, "statusrsv":string, "pax":int, "dept_no":int, "dept_name":string, "table_no":int, "f_time":string, "t_time":string, "remark":string, "usr_id":string, "bill_no":string})

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rsv_table_list_data, doit, rstatus, queasy, hoteldpt, guest
        nonlocal from_date, to_date, sorttype
        nonlocal bqueasy


        nonlocal rsv_table_list, bqueasy
        nonlocal rsv_table_list_data

        return {"rsv-table-list": rsv_table_list_data}


    rstatus[0] = "OPEN"
    rstatus[1] = "CLOSE"
    rstatus[2] = "CANCEL"
    rstatus[3] = "EXPIRED"

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 311) & (Queasy.date1 >= from_date) & (Queasy.date1 <= to_date)).order_by(Queasy._recid).all():
        doit = True

        if sorttype > 0:

            if sorttype == 1 and queasy.betriebsnr != 0:
                doit = False

            elif sorttype == 2 and queasy.betriebsnr != 1:
                doit = False

            elif sorttype == 3 and queasy.betriebsnr != 2:
                doit = False

            elif sorttype == 4 and queasy.betriebsnr != 3:
                doit = False

        if doit:
            rsv_table_list = Rsv_table_list()
            rsv_table_list_data.append(rsv_table_list)

            rsv_table_list.rec_id = queasy._recid
            rsv_table_list.bookingdate = queasy.date1
            rsv_table_list.reservationno = queasy.number1
            rsv_table_list.guestid = to_int(entry(0, queasy.char2, "|"))
            rsv_table_list.statusrsv = rstatus[queasy.betriebsnr + 1 - 1]
            rsv_table_list.pax = queasy.number2

            if queasy.char1 != "" and queasy.char1 != None:
                rsv_table_list.bill_no = entry(0, queasy.char1, "|")
                rsv_table_list.dept_no = to_int(entry(1, queasy.char1, "|"))

                if num_entries(queasy.char1, "|") >= 3:
                    rsv_table_list.table_no = to_int(entry(2, queasy.char1, "|"))

            if queasy.char3 != "" and queasy.char3 != None:
                rsv_table_list.remark = entry(1, queasy.char3, "|")
                rsv_table_list.usr_id = entry(0, queasy.char3, "|")

            if rsv_table_list.dept_no > 0:

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, rsv_table_list.dept_no)]})

                if hoteldpt:
                    rsv_table_list.dept_name = hoteldpt.depart

            guest = get_cache (Guest, {"gastnr": [(eq, rsv_table_list.guestid)]})

            if guest:
                rsv_table_list.guestname = guest.name + "," + guest.vorname1
                rsv_table_list.guestphone = guest.mobil_telefon
                rsv_table_list.guestemail = guest.email_adr

            for bqueasy in db_session.query(Bqueasy).filter(
                     (Bqueasy.key == 312) & (Bqueasy.number1 == queasy.number1)).order_by(Bqueasy._recid).all():
                rsv_table_list.depositamount =  to_decimal(rsv_table_list.depositamount) + to_decimal(bqueasy.deci1)
                rsv_table_list.paymentamount =  to_decimal(rsv_table_list.paymentamount) + to_decimal(bqueasy.deci2)

    return generate_output()