# using conversion tools version: 1.0.0.117
"""_yusufwijasena_30/12/2025

        remark: - added validation to except when zimkateg is None
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_rm_limitbl import check_rm_limitbl
from models import Zimmer, Htparam, Zimkateg


def prepare_room_adminbl():

    prepare_cache([Htparam, Zimkateg])

    zikatnr = 0
    rmcatbez = ""
    room_limit = 0
    curr_anz = 0
    ci_date = None
    t_zimmer_data = []
    zimmer = htparam = zimkateg = None

    t_zimmer = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal zikatnr, rmcatbez, room_limit, curr_anz, ci_date, t_zimmer_data, zimmer, htparam, zimkateg
        nonlocal t_zimmer
        nonlocal t_zimmer_data

        return {
            "zikatnr": zikatnr,
            "rmcatbez": rmcatbez,
            "room_limit": room_limit,
            "curr_anz": curr_anz,
            "ci_date": ci_date,
            "t-zimmer": t_zimmer_data
        }

    room_limit, curr_anz = get_output(check_rm_limitbl())

    htparam = get_cache(Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    zimkateg = db_session.query(Zimkateg).first()

    if zimkateg:
        zikatnr = zimkateg.zikatnr
        rmcatbez = zimkateg.kurzbez

    for zimmer in db_session.query(Zimmer).order_by(Zimmer.zinr).all():
        t_zimmer = T_zimmer()
        t_zimmer_data.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)

    return generate_output()
