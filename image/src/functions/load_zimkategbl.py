from functions.additional_functions import *
import decimal
from models import Zimkateg, Zimmer

def load_zimkategbl(room_exist_only:bool, sleeping_only:bool):
    t_zimkateg_list = []
    do_it:bool = False
    zimkateg = zimmer = None

    t_zimkateg = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimkateg_list, do_it, zimkateg, zimmer


        nonlocal t_zimkateg
        nonlocal t_zimkateg_list
        return {"t-zimkateg": t_zimkateg_list}

    for zimkateg in db_session.query(Zimkateg).all():

        if sleeping_only:

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.sleeping)).first()

        if not zimmer and room_exist_only:

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == zimkateg.zikatnr)).first()
        do_it = (not room_exist_only and not sleeping_only) or None != zimmer

        if do_it:
            t_zimkateg = T_zimkateg()
            t_zimkateg_list.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)

    return generate_output()