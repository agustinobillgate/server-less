#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Nightaudit, Nitehist

def if_read_onlinetax_mbl(datum_rech:date):

    prepare_cache ([Nightaudit, Nitehist])

    reihenfolge:int = 0
    nightaudit = nitehist = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal reihenfolge, nightaudit, nitehist
        nonlocal datum_rech

        return {}


    nightaudit = get_cache (Nightaudit, {"programm": [(eq, "nt-onlinetax.p")]})
    reihenfolge = nightaudit.reihenfolge

    nitehist = db_session.query(Nitehist).filter(
             (Nitehist.datum == datum_rech) & (Nitehist.reihenfolge == reihenfolge) & (Nitehist.line == ("END-OF-RECORD").lower())).order_by(Nitehist._recid.desc()).first()

    if not nitehist:

        return generate_output()
    else:
        nitehist.line_nr = 99999998

    return generate_output()