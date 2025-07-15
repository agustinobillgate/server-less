#using conversion tools version: 1.0.0.117

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

        argt_line = get_cache (Argt_line, {"argtnr": [(eq, argtlinebuff.argtnr)],"argt_artnr": [(eq, argtlinebuff.argt_artnr)],"departement": [(eq, argtlinebuff.departement)],"fakt_modus": [(eq, argtlinebuff.fakt_modus)],"intervall": [(eq, argtlinebuff.intervall)],"kind1": [(eq, argtlinebuff.kind1)],"kind2": [(eq, argtlinebuff.kind2)],"betrag": [(eq, argtlinebuff.betrag)],"betriebsnr": [(eq, argtlinebuff.betriebsnr)],"vt_percnt": [(eq, argtlinebuff.vt_percnt)]})

        if argt_line:
            buffer_copy(t_argt_line, argt_line)
            pass
            success_flag = True

    return generate_output()