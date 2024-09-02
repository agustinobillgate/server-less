from functions.additional_functions import *
import decimal
from datetime import date
from functions.check_rm_limitbl import check_rm_limitbl
from models import Zimmer, Htparam, Zimkateg

def prepare_room_adminbl():
    zikatnr = 0
    rmcatbez = ""
    room_limit = 0
    curr_anz = 0
    ci_date = None
    t_zimmer_list = []
    zimmer = htparam = zimkateg = None

    t_zimmer = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zikatnr, rmcatbez, room_limit, curr_anz, ci_date, t_zimmer_list, zimmer, htparam, zimkateg


        nonlocal t_zimmer
        nonlocal t_zimmer_list
        return {"zikatnr": zikatnr, "rmcatbez": rmcatbez, "room_limit": room_limit, "curr_anz": curr_anz, "ci_date": ci_date, "t-zimmer": t_zimmer_list}


    room_limit, curr_anz = get_output(check_rm_limitbl())

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    zimkateg = db_session.query(Zimkateg).first()
    zikatnr = zimkateg.zikatnr
    rmcatbez = zimkateg.kurzbez

    for zimmer in db_session.query(Zimmer).all():
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)

    return generate_output()