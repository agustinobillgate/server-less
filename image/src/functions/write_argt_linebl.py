from functions.additional_functions import *
import decimal
from models import Argt_line

def write_argt_linebl(argtlinebuff:[Argtlinebuff], t_argt_line:[T_argt_line]):
    success_flag = False
    argt_line = None

    t_argt_line = argtlinebuff = None

    t_argt_line_list, T_argt_line = create_model_like(Argt_line)
    argtlinebuff_list, Argtlinebuff = create_model_like(Argt_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, argt_line


        nonlocal t_argt_line, argtlinebuff
        nonlocal t_argt_line_list, argtlinebuff_list
        return {"success_flag": success_flag}


    argtlinebuff = query(argtlinebuff_list, first=True)

    t_argt_line = query(t_argt_line_list, first=True)

    if argtlineBuff and t_argt_line:

        argt_line = db_session.query(Argt_line).filter(
                (Argt_line.argtnr == argtlineBuff.argtnr) &  (Argt_line.argt_artnr == argtlineBuff.argt_artnr) &  (Argt_line.departement == argtlineBuff.departement) &  (Argt_line.fakt_modus == argtlineBuff.fakt_modus) &  (Argt_line.intervall == argtlineBuff.intervall) &  (Argt_line.kind1 == argtlineBuff.kind1) &  (Argt_line.kind2 == argtlineBuff.kind2) &  (Argt_line.betrag == argtlineBuff.betrag) &  (Argt_line.betriebsnr == argtlineBuff.betriebsnr) &  (Argt_line.vt_percnt == argtlineBuff.vt_percnt)).first()

        if argt_line:
            buffer_copy(t_argt_line, argt_line)

            success_flag = True

    return generate_output()