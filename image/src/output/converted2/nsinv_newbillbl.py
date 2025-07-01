#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Guest, Htparam, Hoteldpt, Bediener, Res_history

def nsinv_newbillbl(gastnr:int, curr_dept:int, transdate:date, user_init:string):

    prepare_cache ([Guest, Htparam, Hoteldpt, Bediener, Res_history])

    gname = ""
    t_bill_list = []
    dept:string = ""
    bill = guest = htparam = hoteldpt = bediener = res_history = None

    t_bill = None

    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, t_bill_list, dept, bill, guest, htparam, hoteldpt, bediener, res_history
        nonlocal gastnr, curr_dept, transdate, user_init


        nonlocal t_bill
        nonlocal t_bill_list

        return {"gname": gname, "t-bill": t_bill_list}

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})
    bill = Bill()
    db_session.add(bill)


    if transdate != None:
        bill.datum = transdate
    else:
        bill.datum = htparam.fdate
    bill.gastnr = gastnr
    bill.billtyp = curr_dept
    bill.name = guest.name + ", " + guest.vorname1 +\
            guest.anredefirma
    bill.bilname = bill.name
    bill.reslinnr = 1
    bill.rgdruck = 1
    gname = bill.name
    dept = hoteldpt.depart


    pass
    t_bill = T_bill()
    t_bill_list.append(t_bill)

    buffer_copy(bill, t_bill)
    t_bill.bl_recid = to_int(bill._recid)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.action = "Nonstay Bill"
    res_history.aenderung = "Create new non stay bill, Department : " + dept + " BillNo : " + to_string(bill.rechnr) + " BillName : " + gname

    pass

    return generate_output()