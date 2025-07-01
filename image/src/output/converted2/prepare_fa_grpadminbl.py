#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_grup

def prepare_fa_grpadminbl():
    t_fa_grup_list = []
    fa_grup = None

    t_fa_grup = None

    t_fa_grup_list, T_fa_grup = create_model_like(Fa_grup, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_fa_grup_list, fa_grup


        nonlocal t_fa_grup
        nonlocal t_fa_grup_list

        return {"t-fa-grup": t_fa_grup_list}

    for fa_grup in db_session.query(Fa_grup).order_by(Fa_grup._recid).all():
        t_fa_grup = T_fa_grup()
        t_fa_grup_list.append(t_fa_grup)

        buffer_copy(fa_grup, t_fa_grup)
        t_fa_grup.rec_id = fa_grup._recid

    return generate_output()