#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Guest_pr, Queasy

def chg_prcodebl(gastnr:int):

    prepare_cache ([Guest_pr])

    q1_list_data = []
    q2_list_data = []
    res_line = guest_pr = queasy = None

    q1_list = q2_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"char1":string, "char2":string, "logi2":bool, "number3":int, "selected":bool})
    q2_list_data, Q2_list = create_model("Q2_list", {"char1":string, "char2":string, "logi2":bool, "number3":int, "selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, q2_list_data, res_line, guest_pr, queasy
        nonlocal gastnr


        nonlocal q1_list, q2_list
        nonlocal q1_list_data, q2_list_data

        return {"q1-list": q1_list_data, "q2-list": q2_list_data}

    def check_resline():

        nonlocal q1_list_data, q2_list_data, res_line, guest_pr, queasy
        nonlocal gastnr


        nonlocal q1_list, q2_list
        nonlocal q1_list_data, q2_list_data

        rline = None
        Rline =  create_buffer("Rline",Res_line)

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, gastnr)]})

        if not guest_pr:

            return

        res_line = get_cache (Res_line, {"gastnr": [(eq, gastnr)],"active_flag": [(le, 1)]})

        if not res_line:

            return

        res_line = get_cache (Res_line, {"gastnr": [(eq, gastnr)],"active_flag": [(le, 1)]})
        while None != res_line:

            if not matches(res_line.zimmer_wunsch,r"*$CODE$*"):

                rline = db_session.query(Rline).filter(
                         (Rline._recid == res_line._recid)).with_for_update().first()
                rline.zimmer_wunsch = rline.zimmer_wunsch + "$CODE$" + guest_pr.code + ";"
                pass
                pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.gastnr == gastnr) & (Res_line.active_flag <= 1) & (Res_line._recid > curr_recid)).first()


    def create_list():

        nonlocal q1_list_data, q2_list_data, res_line, guest_pr, queasy
        nonlocal gastnr


        nonlocal q1_list, q2_list
        nonlocal q1_list_data, q2_list_data

        for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == gastnr)).order_by(Guest_pr._recid).all():

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})

            if queasy:
                q2_list = Q2_list()
                q2_list_data.append(q2_list)

                buffer_copy(queasy, q2_list)

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2)).order_by(Queasy._recid).all():
            q1_list = Q1_list()
            q1_list_data.append(q1_list)

            buffer_copy(queasy, q1_list)

            q2_list = query(q2_list_data, filters=(lambda q2_list: q2_list.char1 == q1_list.char1), first=True)

            if q2_list:
                q1_list.selected = True


    check_resline()
    create_list()

    return generate_output()