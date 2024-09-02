from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bill, Guest, Htparam, Bediener, Res_history

def nsinv_newbillbl(gastnr:int, curr_dept:int, transdate:date, user_init:str):
    gname = ""
    t_bill_list = []
    bill = guest = htparam = bediener = res_history = None

    t_bill = None

    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, t_bill_list, bill, guest, htparam, bediener, res_history


        nonlocal t_bill
        nonlocal t_bill_list
        return {"gname": gname, "t-bill": t_bill_list}

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill = Bill()
    db_session.add(bill)


    if transdate != None:
        bill.datum = transdate
    else:
        bill.datum = htparam.fdate
    bill.gastnr = gastnr
    billtyp = curr_dept
    bill.name = guest.name + ", " + guest.vorname1 +\
            guest.anredefirma
    bill.bilname = bill.name
    bill.reslinnr = 1
    bill.rgdruck = 1
    gname = bill.name

    bill = db_session.query(Bill).first()
    t_bill = T_bill()
    t_bill_list.append(t_bill)

    buffer_copy(bill, t_bill)
    t_bill.bl_recid = to_int(bill._recid)

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.action = "Nonstay Bill"
    res_history.aenderung = "Create new non stay bill, BillNo : " + to_string(bill.rechnr) + " BillName : " + gname


    pass

    res_history = db_session.query(Res_history).first()

    return generate_output()