from functions.additional_functions import *
import decimal
from models import Sourccod

def correct_statistic_disp_sourcebl():
    t_sourccod_list = []
    sourccod = None

    t_sourccod = None

    t_sourccod_list, T_sourccod = create_model("T_sourccod", {"source_code":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_sourccod_list, sourccod


        nonlocal t_sourccod
        nonlocal t_sourccod_list
        return {"t-Sourccod": t_sourccod_list}

    for sourccod in db_session.query(Sourccod).all():
        t_sourccod = T_sourccod()
        t_sourccod_list.append(t_sourccod)

        t_Sourccod.source_code = Sourccod.source_code
        t_Sourccod.bezeich = Sourccod.bezeich

    return generate_output()