#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.check_oth_rl_sts import check_oth_rl_sts
from models import Bk_func, Bk_reser, Bediener, Res_history

def ba_plan_btn_stat2_1bl(answer2:bool, t_resnr:int, t_reslinnr:int, c_status:string, r_status:int, recid_rl:int, bk_reser_resstatus:int, user_init:string):

    prepare_cache ([Bk_func, Bk_reser, Bediener, Res_history])

    new_status:string = ""
    old_status:string = ""
    bk_func = bk_reser = bediener = res_history = None

    bf = rl = None

    Bf = create_buffer("Bf",Bk_func)
    Rl = create_buffer("Rl",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_status, old_status, bk_func, bk_reser, bediener, res_history
        nonlocal answer2, t_resnr, t_reslinnr, c_status, r_status, recid_rl, bk_reser_resstatus, user_init
        nonlocal bf, rl


        nonlocal bf, rl

        return {}


    if bk_reser_resstatus == 1:
        old_status = "Fix Reservation"

    elif bk_reser_resstatus == 2:
        old_status = "Tentative"

    if r_status == 1:
        new_status = "Fix Reservation"

    elif r_status == 2:
        new_status = "Tentative"

    rl = get_cache (Bk_reser, {"_recid": [(eq, recid_rl)]})

    if answer2:

        for bf in db_session.query(Bf).filter(
                 (Bf.veran_nr == t_resnr)).order_by(Bf._recid).all():

            if bf and c_status != "":
                bf.c_resstatus[0] = c_status
                bf.r_resstatus[0] = r_status
                bf.resstatus = r_status
                pass
                rl.resstatus = r_status
                pass
                get_output(check_oth_rl_sts(bf.veran_nr, bf.veran_seite, bf.resstatus))

                if bk_reser_resstatus != r_status:

                    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Status Changes From " + old_status + " To " + new_status
                    res_history.action = "Banquet"


                    pass
                    pass
    else:

        bf = get_cache (Bk_func, {"veran_nr": [(eq, t_resnr)],"veran_seite": [(eq, t_reslinnr)]})

        if bf and c_status != "":
            pass
            bf.c_resstatus[0] = c_status
            bf.r_resstatus[0] = r_status
            bf.resstatus = r_status
            pass
            pass
            rl.resstatus = r_status
            pass
            get_output(check_oth_rl_sts(bf.veran_nr, bf.veran_seite, bf.resstatus))

            if bk_reser_resstatus != r_status:

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Status Changes From " + old_status + " To " + new_status
                res_history.action = "Banquet"


                pass
                pass

    return generate_output()