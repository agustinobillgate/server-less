from functions.additional_functions import *
import decimal
from models import Zimmer

def read_zimmerbl(case_type:int, rmno:str, zikatno:int, setupno:int):
    t_zimmer_list = []
    zimmer = None

    t_zimmer = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimmer_list, zimmer


        nonlocal t_zimmer
        nonlocal t_zimmer_list
        return {"t-zimmer": t_zimmer_list}

    if case_type == 1:

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == rmno)).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 2:

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zikatnr == zikatno) &  (Zimmer.setup == setupno)).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 3:

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.zikatnr == zikatno)).all():
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)

    elif case_type == 4:

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.house_status != 0)).all():
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)

    elif case_type == 5:

        zimmer = db_session.query(Zimmer).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 6:

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zikatnr == zikatno) &  (Zimmer.sleeping)).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 7:

        for zimmer in db_session.query(Zimmer).all():
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 8:

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.zistatus >= 2) &  (Zimmer.zistatus <= 4)).all():
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 9:

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.typ == zikatno)).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 10:

        zimmer = db_session.query(Zimmer).filter(
                ((Zimmer.setup + 9200) == setupno)).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 11:

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.nebenstelle != "")).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)

    return generate_output()