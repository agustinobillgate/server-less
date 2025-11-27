#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line

t_argt_line_data, T_argt_line = create_model_like(Argt_line)

def delete_argt_linebl(case_type:int, int1:int, t_argt_line_data:[T_argt_line]):
    success_flag = False
    argt_line = None

    t_argt_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, argt_line
        nonlocal case_type, int1


        nonlocal t_argt_line

        return {"success_flag": success_flag}

    if case_type == 1:

        t_argt_line = query(t_argt_line_data, first=True)

        if not t_argt_line:

            return generate_output()

        # argt_line = get_cache (Argt_line, {"argtnr": [(eq, t_argt_line.argtnr)],"argt_artnr": [(eq, t_argt_line.argt_artnr)],"departement": [(eq, t_argt_line.departement)],"fakt_modus": [(eq, t_argt_line.fakt_modus)],"intervall": [(eq, t_argt_line.intervall)],"kind1": [(eq, t_argt_line.kind1)],"kind2": [(eq, t_argt_line.kind2)],"betrag": [(eq, t_argt_line.betrag)],"betriebsnr": [(eq, t_argt_line.betriebsnr)],"vt_percnt": [(eq, t_argt_line.vt_percnt)]})
        argt_line = db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == t_argt_line.argtnr) &
                 (Argt_line.argt_artnr == t_argt_line.argt_artnr) &
                 (Argt_line.departement == t_argt_line.departement) &
                 (Argt_line.fakt_modus == t_argt_line.fakt_modus) &
                 (Argt_line.intervall == t_argt_line.intervall) &
                 (Argt_line.kind1 == t_argt_line.kind1) &
                 (Argt_line.kind2 == t_argt_line.kind2) &
                 (Argt_line.betrag == t_argt_line.betrag) &
                 (Argt_line.betriebsnr == t_argt_line.betriebsnr) &
                 (Argt_line.vt_percnt == t_argt_line.vt_percnt)).with_for_update().first()
        
        if argt_line:
            db_session.delete(argt_line)
            pass
            success_flag = True
    elif case_type == 2:

        # argt_line = get_cache (Argt_line, {"_recid": [(eq, int1)]})
        argt_line = db_session.query(Argt_line).filter(
                 (Argt_line._recid == int1)).with_for_update().first()

        if argt_line:
            db_session.delete(argt_line)
            pass
            success_flag = True

    return generate_output()