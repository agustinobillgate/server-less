#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg, Zimmer

def read_zimkategbl(case_type:int, zikatNo:int, shortBez:string):
    t_zimkateg_data = []
    zimkateg = zimmer = None

    t_zimkateg = None

    t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimkateg_data, zimkateg, zimmer
        nonlocal case_type, zikatNo, shortBez


        nonlocal t_zimkateg
        nonlocal t_zimkateg_data

        return {"t-zimkateg": t_zimkateg_data}

    if case_type == 1:

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zikatNo)]})

        if zimkateg:
            t_zimkateg = T_zimkateg()
            t_zimkateg_data.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 2:

        # zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, shortBez)]})
        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.kurzbez == shortBez)).first()

        if zimkateg:
            t_zimkateg = T_zimkateg()
            t_zimkateg_data.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 3:

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.kurzbez).all():

            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)]})

            if zimmer:
                t_zimkateg = T_zimkateg()
                t_zimkateg_data.append(t_zimkateg)

                buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 4:

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            t_zimkateg = T_zimkateg()
            t_zimkateg_data.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 5:

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, shortBez)],"zikatnr": [(ne, zikatNo)]})

        if zimkateg:
            t_zimkateg = T_zimkateg()
            t_zimkateg_data.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 6:

        for zimkateg in db_session.query(Zimkateg).filter(
                 (Zimkateg.typ == zikatNo)).order_by(Zimkateg._recid).all():
            t_zimkateg = T_zimkateg()
            t_zimkateg_data.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)

    return generate_output()