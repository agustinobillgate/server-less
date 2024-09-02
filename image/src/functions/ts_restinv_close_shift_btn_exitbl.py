from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import H_bill_line, H_journal, H_bill, Bediener, Res_history

def ts_restinv_close_shift_btn_exitbl(pvilanguage:int, shift_list:[Shift_list], all_user:bool, curr_dept:int, billdate:date, kellner_kellner_nr:int, shift:int, user_init:str):
    flag = 0
    lvcarea:str = "TS_restinv"
    do_it:bool = False
    h_bill_line = h_journal = h_bill = bediener = res_history = None

    shift_list = user_list = sbuff = hbline = None

    shift_list_list, Shift_list = create_model("Shift_list", {"rechnr":int, "tischnr":int, "selectflag":bool, "bstr":str})
    user_list_list, User_list = create_model("User_list", {"kellner_nr":int})

    Sbuff = Shift_list
    sbuff_list = shift_list_list

    Hbline = H_bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, lvcarea, do_it, h_bill_line, h_journal, h_bill, bediener, res_history
        nonlocal sbuff, hbline


        nonlocal shift_list, user_list, sbuff, hbline
        nonlocal shift_list_list, user_list_list
        return {"flag": flag}

    user_list_list.clear()

    if all_user:

        for h_journal in db_session.query(H_journal).filter(
                (H_journal.departement == curr_dept) &  (H_journal.bill_datum == billdate)).all():

            user_list = query(user_list_list, filters=(lambda user_list :user_list.kellner_nr == h_journal.kellner_nr), first=True)

            if not user_list:
                user_list = User_list()
                user_list_list.append(user_list)

                user_list.kellner_nr = h_journal.kellner_nr


    else:
        user_list = User_list()
        user_list_list.append(user_list)

        user_list.kellner_nr = kellner_kellner_nr

    for user_list in query(user_list_list):

        for h_bill in db_session.query(H_bill).filter(
                (H_bill.flag == 1) &  (H_bill.departement == curr_dept) &  (H_bill.kellner_nr == user_list.kellner_nr)).all():

            if all_user:
                do_it = True
            else:

                sbuff = query(sbuff_list, filters=(lambda sbuff :sbuff.rechnr == h_bill.rechnr and sbuff.selectFlag), first=True)
                do_it = None != sbuff

            if do_it:

                h_bill_line = db_session.query(H_bill_line).filter(
                        (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.bill_datum == billdate) &  (H_bill_line.departement == curr_dept) &  (H_bill_line.zeit >= 0) &  (H_bill_line.betriebsnr == 0)).first()
                while None != h_bill_line:

                    hbline = db_session.query(Hbline).filter(
                            (Hbline._recid == h_bill_line._recid)).first()
                    hbline.betriebsnr = shift

                    hbline = db_session.query(Hbline).first()


                    h_bill_line = db_session.query(H_bill_line).filter(
                            (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.bill_datum == billdate) &  (H_bill_line.departement == curr_dept) &  (H_bill_line.zeit >= 0) &  (H_bill_line.betriebsnr == 0)).first()

    if all_user:

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Close shift(ALL)"
        res_history.action = "POS Cashier"

        res_history = db_session.query(Res_history).first()

    flag = 1
    else:

        sbuff = query(sbuff_list, filters=(lambda sbuff :sbuff.selectFLag == False), first=True)

        if not sbuff:
            flag = 2
        else:
            flag = 3

    return generate_output()