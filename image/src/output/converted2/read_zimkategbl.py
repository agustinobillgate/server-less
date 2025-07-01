#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg, Zimmer

def read_zimkategbl(case_type:int, zikatno:int, shortbez:string):
    t_zimkateg_list = []
    zimkateg = zimmer = None

    t_zimkateg = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimkateg_list, zimkateg, zimmer
        nonlocal case_type, zikatno, shortbez


        nonlocal t_zimkateg
        nonlocal t_zimkateg_list

        return {"t-zimkateg": t_zimkateg_list}

    if case_type == 1:

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zikatno)]})

        if zimkateg:
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 2:

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, shortbez)]})

        if zimkateg:
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 3:

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.kurzbez).all():

            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)]})

            if zimmer:
                t_zimkateg = T_zimkateg()
                t_zimkateg_list.append(t_zimkateg)

                buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 4:

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 5:

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, shortbez)],"zikatnr": [(ne, zikatno)]})

        if zimkateg:
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 6:

        for zimkateg in db_session.query(Zimkateg).filter(
                 (Zimkateg.typ == zikatno)).order_by(Zimkateg._recid).all():
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)

    return generate_output()