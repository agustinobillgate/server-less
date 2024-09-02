from functions.additional_functions import *
import decimal
import re
from models import Res_line, Guest_pr, Queasy

def chg_prcodebl(gastnr:int):
    q1_list_list = []
    q2_list_list = []
    res_line = guest_pr = queasy = None

    q1_list = q2_list = rline = None

    q1_list_list, Q1_list = create_model("Q1_list", {"char1":str, "char2":str, "logi2":bool, "number3":int, "selected":bool})
    q2_list_list, Q2_list = create_model("Q2_list", {"char1":str, "char2":str, "logi2":bool, "number3":int, "selected":bool})

    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, q2_list_list, res_line, guest_pr, queasy
        nonlocal rline


        nonlocal q1_list, q2_list, rline
        nonlocal q1_list_list, q2_list_list
        return {"q1-list": q1_list_list, "q2-list": q2_list_list}

    def check_resline():

        nonlocal q1_list_list, q2_list_list, res_line, guest_pr, queasy
        nonlocal rline


        nonlocal q1_list, q2_list, rline
        nonlocal q1_list_list, q2_list_list


        Rline = Res_line

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == gastnr)).first()

        if not guest_pr:

            return

        res_line = db_session.query(Res_line).filter(
                (Res_line.gastnr == gastnr) &  (Res_line.active_flag <= 1)).first()

        if not res_line:

            return

        res_line = db_session.query(Res_line).filter(
                (Res_line.gastnr == gastnr) &  (Res_line.active_flag <= 1)).first()
        while None != res_line:

            if not re.match(".*\$CODE\$.*",res_line.zimmer_wunsch):

                rline = db_session.query(Rline).filter(
                        (Rline._recid == res_line._recid)).first()
                rline.zimmer_wunsch = rline.zimmer_wunsch + "$CODE$" + guest_pr.CODE + ";"

                rline = db_session.query(Rline).first()


            res_line = db_session.query(Res_line).filter(
                    (Res_line.gastnr == gastnr) &  (Res_line.active_flag <= 1)).first()

    def create_list():

        nonlocal q1_list_list, q2_list_list, res_line, guest_pr, queasy
        nonlocal rline


        nonlocal q1_list, q2_list, rline
        nonlocal q1_list_list, q2_list_list

        for guest_pr in db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == gastnr)).all():

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (Queasy.char1 == guest_pr.CODE)).first()

            if queasy:
                q2_list = Q2_list()
                q2_list_list.append(q2_list)

                buffer_copy(queasy, q2_list)

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2)).all():
            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            buffer_copy(queasy, q1_list)

            q2_list = query(q2_list_list, filters=(lambda q2_list :q2_list.char1 == q1_list.char1), first=True)

            if q2_list:
                q1_list.SELECTED = True

    check_resline()
    create_list()

    return generate_output()