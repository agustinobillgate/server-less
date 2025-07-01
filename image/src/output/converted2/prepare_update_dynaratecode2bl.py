#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from models import Queasy, Zimkateg

def prepare_update_dynaratecode2bl():

    prepare_cache ([Queasy, Zimkateg])

    ci_date = None
    i_param439 = 0
    queasy2_list = []
    t_zimkateg_list = []
    queasy = zimkateg = None

    t_zimkateg = queasy2 = None

    t_zimkateg_list, T_zimkateg = create_model("T_zimkateg", {"kurzbez":string})
    queasy2_list, Queasy2 = create_model("Queasy2", {"char1":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, i_param439, queasy2_list, t_zimkateg_list, queasy, zimkateg


        nonlocal t_zimkateg, queasy2
        nonlocal t_zimkateg_list, queasy2_list

        return {"ci_date": ci_date, "i_param439": i_param439, "queasy2": queasy2_list, "t-zimkateg": t_zimkateg_list}

    ci_date = get_output(htpdate(87))
    i_param439 = get_output(htpint(439))

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2) & (Queasy.logi2)).order_by(Queasy.char1).all():
        queasy2 = Queasy2()
        queasy2_list.append(queasy2)

        queasy2.char1 = queasy.char1

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_list.append(t_zimkateg)

        t_zimkateg.kurzbez = zimkateg.kurzbez

    return generate_output()