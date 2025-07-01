#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from models import Guest_pr, Queasy, Zimkateg

def prepare_update_dynaratecode_webbl(booken_selected:int):

    prepare_cache ([Zimkateg])

    ci_date = None
    i_param439 = 0
    cusername = ""
    cpassword = ""
    vcwsagent = ""
    htl_code = ""
    pushrate = False
    queasy2_list = []
    t_zimkateg_list = []
    t_guest_pr_list = []
    t_queasy159_list = []
    t_queasy160_list = []
    t_queasy201_list = []
    gastnr:int = 0
    guest_pr = queasy = zimkateg = None

    t_zimkateg = queasy2 = t_guest_pr = t_queasy159 = t_queasy160 = t_queasy201 = None

    t_zimkateg_list, T_zimkateg = create_model("T_zimkateg", {"kurzbez":string})
    queasy2_list, Queasy2 = create_model("Queasy2", {"char1":string})
    t_guest_pr_list, T_guest_pr = create_model_like(Guest_pr)
    t_queasy159_list, T_queasy159 = create_model_like(Queasy)
    t_queasy160_list, T_queasy160 = create_model_like(Queasy)
    t_queasy201_list, T_queasy201 = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, i_param439, cusername, cpassword, vcwsagent, htl_code, pushrate, queasy2_list, t_zimkateg_list, t_guest_pr_list, t_queasy159_list, t_queasy160_list, t_queasy201_list, gastnr, guest_pr, queasy, zimkateg
        nonlocal booken_selected


        nonlocal t_zimkateg, queasy2, t_guest_pr, t_queasy159, t_queasy160, t_queasy201
        nonlocal t_zimkateg_list, queasy2_list, t_guest_pr_list, t_queasy159_list, t_queasy160_list, t_queasy201_list

        return {"ci_date": ci_date, "i_param439": i_param439, "cusername": cusername, "cpassword": cpassword, "vcwsagent": vcwsagent, "htl_code": htl_code, "pushrate": pushrate, "queasy2": queasy2_list, "t-zimkateg": t_zimkateg_list, "t-guest-pr": t_guest_pr_list, "t-queasy159": t_queasy159_list, "t-queasy160": t_queasy160_list, "t-queasy201": t_queasy201_list}

    ci_date = get_output(htpdate(87))
    i_param439 = get_output(htpint(439))

    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, booken_selected)]})

    if queasy:
        gastnr = queasy.number2

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2) & (Queasy.logi2)).order_by(Queasy.char1).all():
        queasy2 = Queasy2()
        queasy2_list.append(queasy2)

        queasy2.char1 = queasy.char1

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_list.append(t_zimkateg)

        t_zimkateg.kurzbez = zimkateg.kurzbez

    for guest_pr in db_session.query(Guest_pr).filter(
             (Guest_pr.gastnr == gastnr)).order_by(Guest_pr._recid).all():
        t_guest_pr = T_guest_pr()
        t_guest_pr_list.append(t_guest_pr)

        buffer_copy(guest_pr, t_guest_pr)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 159)).order_by(Queasy._recid).all():
        t_queasy159 = T_queasy159()
        t_queasy159_list.append(t_queasy159)

        buffer_copy(queasy, t_queasy159)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 160)).order_by(Queasy._recid).all():
        t_queasy160 = T_queasy160()
        t_queasy160_list.append(t_queasy160)

        buffer_copy(queasy, t_queasy160)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 201)).order_by(Queasy._recid).all():
        t_queasy201 = T_queasy201()
        t_queasy201_list.append(t_queasy201)

        buffer_copy(queasy, t_queasy201)

    t_queasy160 = query(t_queasy160_list, filters=(lambda t_queasy160: t_queasy160.number1 == 3), first=True)

    if t_queasy160:
        cusername = entry(2, entry(8, t_queasy160.char1, ";") , "$")
        cpassword = entry(2, entry(9, t_queasy160.char1, ";") , "$")
        vcwsagent = entry(17, entry(6, t_queasy160.char1, ";") , "=")
        htl_code = entry(2, entry(7, t_queasy160.char1, ";") , "$")
        pushrate = logical(entry(2, entry(10, t_queasy160.char1, ";") , "$"))

    return generate_output()