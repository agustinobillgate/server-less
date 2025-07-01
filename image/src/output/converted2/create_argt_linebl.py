#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line

t_argt_line_list, T_argt_line = create_model_like(Argt_line)

def create_argt_linebl(t_argt_line_list:[T_argt_line]):
    success_flag = False
    argt_line = None

    t_argt_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, argt_line


        nonlocal t_argt_line

        return {"success_flag": success_flag}

    t_argt_line = query(t_argt_line_list, first=True)

    if t_argt_line:
        success_flag = True

        argt_line = get_cache (Argt_line, {"argtnr": [(eq, t_argt_line.argtnr)],"argt_artnr": [(eq, t_argt_line.argt_artnr)],"departement": [(eq, t_argt_line.departement)],"fakt_modus": [(eq, t_argt_line.fakt_modus)],"intervall": [(eq, t_argt_line.intervall)],"kind1": [(eq, t_argt_line.kind1)],"kind2": [(eq, t_argt_line.kind2)],"betrag": [(eq, t_argt_line.betrag)],"betriebsnr": [(eq, t_argt_line.betriebsnr)],"vt_percnt": [(eq, t_argt_line.vt_percnt)]})

        if not argt_line:
            argt_line = Argt_line()
            db_session.add(argt_line)

            buffer_copy(t_argt_line, argt_line)
            pass

    return generate_output()