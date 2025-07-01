#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Bk_veran, Htparam, Bill, Bk_func, B_history

def ba_plan_res_checkout2bl(mainres_recid:int, t_resnr:int, t_reslinnr:int, user_init:string):

    prepare_cache ([Bk_veran, Htparam, Bill, B_history])

    ci_date:date = None
    bk_reser = bk_veran = htparam = bill = bk_func = b_history = None

    resline = bk_resline = mainres = None

    Resline = create_buffer("Resline",Bk_reser)
    Bk_resline = create_buffer("Bk_resline",Bk_reser)
    Mainres = create_buffer("Mainres",Bk_veran)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, bk_reser, bk_veran, htparam, bill, bk_func, b_history
        nonlocal mainres_recid, t_resnr, t_reslinnr, user_init
        nonlocal resline, bk_resline, mainres


        nonlocal resline, bk_resline, mainres

        return {}

    def create_bahistory():

        nonlocal ci_date, bk_reser, bk_veran, htparam, bill, bk_func, b_history
        nonlocal mainres_recid, t_resnr, t_reslinnr, user_init
        nonlocal resline, bk_resline, mainres


        nonlocal resline, bk_resline, mainres


        b_history = B_history()
        db_session.add(b_history)

        buffer_copy(bk_func, b_history)
        b_history.deposit =  to_decimal(mainres.deposit)
        b_history.limit_date = mainres.limit_date
        b_history.segmentcode = mainres.segmentcode
        b_history.deposit_payment[0] = mainres.deposit_payment[0]
        b_history.deposit_payment[1] = mainres.deposit_payment[1]
        b_history.deposit_payment[2] = mainres.deposit_payment[2]
        b_history.deposit_payment[3] = mainres.deposit_payment[3]
        b_history.deposit_payment[4] = mainres.deposit_payment[4]
        b_history.deposit_payment[5] = mainres.deposit_payment[5]
        b_history.deposit_payment[6] = mainres.deposit_payment[6]
        b_history.deposit_payment[7] = mainres.deposit_payment[7]
        b_history.deposit_payment[8] = mainres.deposit_payment[8]
        b_history.payment_date[0] = mainres.payment_date[0]
        b_history.payment_date[1] = mainres.payment_date[1]
        b_history.payment_date[2] = mainres.payment_date[2]
        b_history.payment_date[3] = mainres.payment_date[3]
        b_history.payment_date[4] = mainres.payment_date[4]
        b_history.payment_date[5] = mainres.payment_date[5]
        b_history.payment_date[6] = mainres.payment_date[6]
        b_history.payment_date[7] = mainres.payment_date[7]
        b_history.payment_date[8] = mainres.payment_date[8]
        b_history.payment_userinit[0] = mainres.payment_userinit[0]
        b_history.payment_userinit[1] = mainres.payment_userinit[1]
        b_history.payment_userinit[2] = mainres.payment_userinit[2]
        b_history.payment_userinit[3] = mainres.payment_userinit[3]
        b_history.payment_userinit[4] = mainres.payment_userinit[4]
        b_history.payment_userinit[5] = mainres.payment_userinit[5]
        b_history.payment_userinit[6] = mainres.payment_userinit[6]
        b_history.payment_userinit[7] = mainres.payment_userinit[7]
        b_history.payment_userinit[8] = mainres.payment_userinit[8]
        b_history.total_paid =  to_decimal(mainres.total_paid)


        pass
        pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    resline = db_session.query(Resline).filter(
             (Resline.veran_nr == t_resnr) & (Resline.veran_resnr == t_reslinnr)).first()

    if resline:

        mainres = get_cache (Bk_veran, {"_recid": [(eq, mainres_recid)]})

        if mainres:

            bill = get_cache (Bill, {"rechnr": [(eq, mainres.rechnr)]})

            if bill:
                pass
                mainres.activeflag = 1
                pass

                bk_resline = db_session.query(Bk_resline).filter(
                             (Bk_resline.veran_nr == resline.veran_nr) & (Bk_resline.resstatus == 1)).first()
                while None != bk_resline:
                    pass
                    bk_resline.resstatus = 8
                    pass

                    curr_recid = bk_resline._recid
                    bk_resline = db_session.query(Bk_resline).filter(
                                 (Bk_resline.veran_nr == resline.veran_nr) & (Bk_resline.resstatus == 1) & (Bk_resline._recid > curr_recid)).first()

                bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resline.veran_nr)],"resstatus": [(eq, 1)]})
                while None != bk_func:
                    create_bahistory()
                    pass
                    bk_func.resstatus = 8
                    bk_func.c_resstatus[0] = "I"
                    bk_func.r_resstatus[0] = 8


                    pass

                    curr_recid = bk_func._recid
                    bk_func = db_session.query(Bk_func).filter(
                                 (Bk_func.veran_nr == resline.veran_nr) & (Bk_func.resstatus == 1) & (Bk_func._recid > curr_recid)).first()

                if mainres.rechnr > 0:
                    pass
                    bill.flag = 1
                    bill.datum = ci_date
                    bill.vesrcod = user_init


                    pass

    return generate_output()