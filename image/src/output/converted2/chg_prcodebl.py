from functions.additional_functions import *
import decimal
from models import Res_line, Guest_pr, Queasy

def chg_prcodebl(gastnr:int):
    q1_list_list = []
    q2_list_list = []
    res_line = guest_pr = queasy = None

    q1_list = q2_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"char1":str, "char2":str, "logi2":bool, "number3":int, "selected":bool})
    q2_list_list, Q2_list = create_model("Q2_list", {"char1":str, "char2":str, "logi2":bool, "number3":int, "selected":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, q2_list_list, res_line, guest_pr, queasy
        nonlocal gastnr


        nonlocal q1_list, q2_list
        nonlocal q1_list_list, q2_list_list
        return {"q1-list": q1_list_list, "q2-list": q2_list_list}

    def check_resline():

        nonlocal q1_list_list, q2_list_list, res_line, guest_pr, queasy
        nonlocal gastnr


        nonlocal q1_list, q2_list
        nonlocal q1_list_list, q2_list_list

        rline = None
        Rline =  create_buffer("Rline",Res_line)

        guest_pr = db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == gastnr)).first()

        if not guest_pr:

            return

        res_line = db_session.query(Res_line).filter(
                 (Res_line.gastnr == gastnr) & (Res_line.active_flag <= 1)).first()

        if not res_line:

            return

        res_line = db_session.query(Res_line).filter(
                 (Res_line.gastnr == gastnr) & (Res_line.active_flag <= 1)).first()
        while None != res_line:

            if re.match(r".*\$CODE\$.*",not res_line.zimmer_wunsch, re.IGNORECASE):

                rline = db_session.query(Rline).filter(
                         (Rline._recid == res_line._recid)).first()
                rline.zimmer_wunsch = rline.zimmer_wunsch + "$CODE$" + guest_pr.code + ";"
                pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.gastnr == gastnr) & (Res_line.active_flag <= 1)).filter(Res_line._recid > curr_recid).first()


    def create_list():

        nonlocal q1_list_list, q2_list_list, res_line, guest_pr, queasy
        nonlocal gastnr


        nonlocal q1_list, q2_list
        nonlocal q1_list_list, q2_list_list

        for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == gastnr)).order_by(Guest_pr._recid).all():

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 2) & (Queasy.char1 == guest_pr.code)).first()

            if queasy:
                q2_list = Q2_list()
                q2_list_list.append(q2_list)

                buffer_copy(queasy, q2_list)

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2)).order_by(Queasy._recid).all():
            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            buffer_copy(queasy, q1_list)

            q2_list = query(q2_list_list, filters=(lambda q2_list: q2_list.char1 == q1_list.char1), first=True)

            if q2_list:
                q1_list.selected = True


    check_resline()
    create_list()

    return generate_output()