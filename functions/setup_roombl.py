#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Paramtext

def setup_roombl(rmtype:int, bed_setup:int):

    prepare_cache ([Paramtext])

    t_zimmer_data = []
    zimmer = paramtext = None

    t_zimmer = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer, {"outlook":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimmer_data, zimmer, paramtext
        nonlocal rmtype, bed_setup


        nonlocal t_zimmer
        nonlocal t_zimmer_data

        return {"t-zimmer": t_zimmer_data}

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.zikatnr == rmtype)).order_by(Zimmer._recid).all():
        t_zimmer = T_zimmer()
        t_zimmer_data.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 230)],"ptexte": [(ne, "")],"sprachcode": [(eq, zimmer.typ)]})

        if paramtext:
            t_zimmer.outlook = paramtext.ptexte

    return generate_output()