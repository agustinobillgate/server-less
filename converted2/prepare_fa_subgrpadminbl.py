#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_grup, Fa_artikel

def prepare_fa_subgrpadminbl():
    t_fa_grup_data = []
    t_fa_artikel_data = []
    fa_grup = fa_artikel = None

    t_fa_grup = t_fa_artikel = None

    t_fa_grup_data, T_fa_grup = create_model_like(Fa_grup, {"rec_id":int})
    t_fa_artikel_data, T_fa_artikel = create_model_like(Fa_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_fa_grup_data, t_fa_artikel_data, fa_grup, fa_artikel


        nonlocal t_fa_grup, t_fa_artikel
        nonlocal t_fa_grup_data, t_fa_artikel_data

        return {"t-fa-grup": t_fa_grup_data, "t-fa-artikel": t_fa_artikel_data}


    for fa_grup in db_session.query(Fa_grup).order_by(Fa_grup._recid).all():
        t_fa_grup = T_fa_grup()
        t_fa_grup_data.append(t_fa_grup)

        buffer_copy(fa_grup, t_fa_grup)
        t_fa_grup.rec_id = fa_grup._recid

    for fa_artikel in db_session.query(Fa_artikel).order_by(Fa_artikel._recid).all():
        t_fa_artikel = T_fa_artikel()
        t_fa_artikel_data.append(t_fa_artikel)

        buffer_copy(fa_artikel, t_fa_artikel)

    return generate_output()