from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Zimkateg, Zimmer

def read_zimkategbl(case_type:int, zikatno:int, shortbez:str):
    t_zimkateg_list = []
    zimkateg = zimmer = None

    t_zimkateg = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimkateg_list, zimkateg, zimmer


        nonlocal t_zimkateg
        nonlocal t_zimkateg_list
        return {"t-zimkateg": t_zimkateg_list}

    if case_type == 1:

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == zikatno)).first()

        if zimkateg:
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 2:

        zimkateg = db_session.query(Zimkateg).filter(
                (func.lower(Zimkateg.kurzbez) == (shortbez).lower())).first()

        if zimkateg:
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 3:

        for zimkateg in db_session.query(Zimkateg).all():

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == zimkateg.zikatnr)).first()

            if zimmer:
                t_zimkateg = T_zimkateg()
                t_zimkateg_list.append(t_zimkateg)

                buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 4:

        for zimkateg in db_session.query(Zimkateg).all():
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 5:

        zimkateg = db_session.query(Zimkateg).filter(
                (func.lower(Zimkateg.kurzbez) == (shortbez).lower()) &  (Zimkateg.zikatnr != zikatno)).first()

        if zimkateg:
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)
    elif case_type == 6:

        for zimkateg in db_session.query(Zimkateg).filter(
                (Zimkateg.typ == zikatno)).all():
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)

    return generate_output()