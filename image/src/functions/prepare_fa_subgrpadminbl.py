from functions.additional_functions import *
import decimal
from models import Fa_grup, Fa_artikel

def prepare_fa_subgrpadminbl():
    t_fa_grup_list = []
    t_fa_artikel_list = []
    fa_grup = fa_artikel = None

    t_fa_grup = t_fa_artikel = None

    t_fa_grup_list, T_fa_grup = create_model_like(Fa_grup, {"rec_id":int})
    t_fa_artikel_list, T_fa_artikel = create_model_like(Fa_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_fa_grup_list, t_fa_artikel_list, fa_grup, fa_artikel


        nonlocal t_fa_grup, t_fa_artikel
        nonlocal t_fa_grup_list, t_fa_artikel_list
        return {"t-fa-grup": t_fa_grup_list, "t-fa-artikel": t_fa_artikel_list}


    for fa_grup in db_session.query(Fa_grup).all():
        t_fa_grup = T_fa_grup()
        t_fa_grup_list.append(t_fa_grup)

        buffer_copy(fa_grup, t_fa_grup)
        t_fa_grup.rec_id = fa_grup._recid

    for fa_artikel in db_session.query(Fa_artikel).all():
        t_fa_artikel = T_fa_artikel()
        t_fa_artikel_list.append(t_fa_artikel)

        buffer_copy(fa_artikel, t_fa_artikel)

    return generate_output()