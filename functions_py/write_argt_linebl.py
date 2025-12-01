#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line

argtlinebuff_data, Argtlinebuff = create_model_like(Argt_line)
t_argt_line_data, T_argt_line = create_model_like(Argt_line)

def write_argt_linebl(argtlinebuff_data:[Argtlinebuff], t_argt_line_data:[T_argt_line]):
    success_flag = False
    argt_line = None

    t_argt_line = argtlinebuff = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, argt_line


        nonlocal t_argt_line, argtlinebuff

        return {"success_flag": success_flag}


    argtlinebuff = query(argtlinebuff_data, first=True)

    t_argt_line = query(t_argt_line_data, first=True)

    if argtlinebuff and t_argt_line:

        # argt_line = get_cache (Argt_line, {"argtnr": [(eq, argtlinebuff.argtnr)],"argt_artnr": [(eq, argtlinebuff.argt_artnr)],
        # "departement": [(eq, argtlinebuff.departement)],"fakt_modus": [(eq, argtlinebuff.fakt_modus)],
        # "intervall": [(eq, argtlinebuff.intervall)],"kind1": [(eq, argtlinebuff.kind1)],"kind2": [(eq, argtlinebuff.kind2)],
        # "betrag": [(eq, argtlinebuff.betrag)],"betriebsnr": [(eq, argtlinebuff.betriebsnr)],"vt_percnt": [(eq, argtlinebuff.vt_percnt)]})
        argt_line = db_session.query(Argt_line).filter(
                    (Argt_line.argtnr == argtlinebuff.argtnr) &
                    (Argt_line.argt_artnr == argtlinebuff.argt_artnr) &
                    (Argt_line.departement == argtlinebuff.departement) &
                    (Argt_line.fakt_modus == argtlinebuff.fakt_modus) &
                    (Argt_line.intervall == argtlinebuff.intervall) &
                    (Argt_line.kind1 == argtlinebuff.kind1) &
                    (Argt_line.kind2 == argtlinebuff.kind2) &
                    (Argt_line.betrag == argtlinebuff.betrag) &
                    (Argt_line.betriebsnr == argtlinebuff.betriebsnr) &
                    (Argt_line.vt_percnt == argtlinebuff.vt_percnt)).with_for_update().first()
        if argt_line:
            buffer_copy(t_argt_line, argt_line)
            pass
            success_flag = True

    return generate_output()