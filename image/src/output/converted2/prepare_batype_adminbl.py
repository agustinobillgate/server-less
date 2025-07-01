#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Ba_typ

def prepare_batype_adminbl():
    t_ba_typ_list = []
    ba_typ = None

    t_ba_typ = None

    t_ba_typ_list, T_ba_typ = create_model_like(Ba_typ, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_ba_typ_list, ba_typ


        nonlocal t_ba_typ
        nonlocal t_ba_typ_list

        return {"t-ba-typ": t_ba_typ_list}

    for ba_typ in db_session.query(Ba_typ).order_by(Ba_typ.typ_id).all():
        t_ba_typ = T_ba_typ()
        t_ba_typ_list.append(t_ba_typ)

        buffer_copy(ba_typ, t_ba_typ)
        t_ba_typ.rec_id = ba_typ._recid

    return generate_output()