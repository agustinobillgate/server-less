#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 15-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_queasy_data, T_queasy = create_model("T_queasy", {"rec_id":int})

def if_ecsys_realtime_trx_successbl(t_queasy_data:[T_queasy]):

    prepare_cache ([Queasy])

    queasy = None

    t_queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal t_queasy

        return {}

    for t_queasy in query(t_queasy_data):

        queasy = get_cache (Queasy, {"_recid": [(eq, t_queasy.rec_id)]})

        if queasy:
            pass
            queasy.logi1 = False
            queasy.logi2 = True


            pass
            pass

    return generate_output()