from functions.additional_functions import *
import decimal
from models import Zimmer
t_zimmer_list, T_zimmer = create_model_like(Zimmer)
def write_zimmerbl(t_zimmer:[T_zimmer]):
    success_flag = False
    zimmer = None

    t_zimmer = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, zimmer


        nonlocal t_zimmer
        global t_zimmer_list
        return {"success_flag": success_flag}

    t_zimmer = query(t_zimmer_list, first=True)

    if t_zimmer:

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == t_zimmer.zinr)).first()

        if zimmer:
            buffer_copy(t_zimmer, zimmer)

            success_flag = True

    return generate_output()