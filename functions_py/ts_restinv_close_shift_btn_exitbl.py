#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill_line, H_journal, H_bill, Bediener, Res_history

shift_list_data, Shift_list = create_model("Shift_list", {"rechnr":int, "tischnr":int, "selectflag":bool, "bstr":string})

def ts_restinv_close_shift_btn_exitbl(pvilanguage:int, shift_list_data:[Shift_list], all_user:bool, 
                                      curr_dept:int, billdate:date, kellner_kellner_nr:int, shift:int, user_init:string):

    prepare_cache ([H_bill_line, H_journal, Bediener, Res_history])

    flag = 0
    lvcarea:string = "TS-restinv"
    do_it:bool = False
    h_bill_line = h_journal = h_bill = bediener = res_history = None

    shift_list = user_list = sbuff = hbline = None

    user_list_data, User_list = create_model("User_list", {"kellner_nr":int})

    Sbuff = Shift_list
    sbuff_data = shift_list_data

    Hbline = create_buffer("Hbline",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, lvcarea, do_it, h_bill_line, h_journal, h_bill, bediener, res_history
        nonlocal pvilanguage, all_user, curr_dept, billdate, kellner_kellner_nr, shift, user_init
        nonlocal sbuff, hbline


        nonlocal shift_list, user_list, sbuff, hbline
        nonlocal user_list_data

        return {"shift-list": shift_list_data, "flag": flag}

    user_list_data.clear()

    if all_user:

        for h_journal in db_session.query(H_journal).filter(
                 (H_journal.departement == curr_dept) & (H_journal.bill_datum == billdate)).order_by(H_journal._recid).all():

            user_list = query(user_list_data, filters=(lambda user_list: user_list.kellner_nr == h_journal.kellner_nr), first=True)

            if not user_list:
                user_list = User_list()
                user_list_data.append(user_list)

                user_list.kellner_nr = h_journal.kellner_nr


    else:
        user_list = User_list()
        user_list_data.append(user_list)

        user_list.kellner_nr = kellner_kellner_nr

    for user_list in query(user_list_data):

        for h_bill in db_session.query(H_bill).filter(
                 (H_bill.flag == 1) & (H_bill.departement == curr_dept) & (H_bill.kellner_nr == user_list.kellner_nr)).order_by(H_bill._recid).all():

            if all_user:
                do_it = True
            else:

                sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff.rechnr == h_bill.rechnr and sbuff.selectflag), first=True)
                do_it = None != sbuff

            if do_it:

                h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(eq, billdate)],"departement": [(eq, curr_dept)],"zeit": [(ge, 0)],"betriebsnr": [(eq, 0)]})
                while None != h_bill_line:

                    # hbline = get_cache (H_bill_line, {"_recid": [(eq, h_bill_line._recid)]})
                    hbline = db_session.query(H_bill_line).filter(
                             (H_bill_line._recid == h_bill_line._recid)).with_for_update().first()
                    hbline.betriebsnr = shift


                    curr_recid = h_bill_line._recid
                    h_bill_line = db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum == billdate) & (H_bill_line.departement == curr_dept) & (H_bill_line.zeit >= 0) & (H_bill_line.betriebsnr == 0) & (H_bill_line._recid > curr_recid)).first()

    if all_user:

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Close shift(ALL)"
        res_history.action = "POS Cashier"

        flag = 1
    else:

        sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff.selectflag == False), first=True)

        if not sbuff:
            flag = 2
        else:
            flag = 3

    return generate_output()