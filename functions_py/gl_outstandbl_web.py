#using conversion tools version: 1.0.0.119
#--------------------------------------------
# Rd, 26/11/2025, with_for_update
#--------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Uebertrag

t_uebertrag_data, T_uebertrag = create_model("T_uebertrag", {"datum":date, "betrag":Decimal, "betriebsnr":int})

def gl_outstandbl_web(t_uebertrag_data:[T_uebertrag]):

    prepare_cache ([Uebertrag])

    uebertrag = None

    t_uebertrag = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal uebertrag


        nonlocal t_uebertrag

        return {}

    for t_uebertrag in query(t_uebertrag_data):

        # uebertrag = get_cache (Uebertrag, {"datum": [(eq, t_uebertrag.datum)],"betriebsnr": [(eq, t_uebertrag.betriebsnr)]})
        uebertrag = db_session.query(Uebertrag).filter(
                 (Uebertrag.datum == t_uebertrag.datum) & (Uebertrag.betriebsnr == t_uebertrag.betriebsnr)).with_for_update().first()

        if uebertrag:
            uebertrag.betrag =  to_decimal(t_uebertrag.betrag)

    return generate_output()