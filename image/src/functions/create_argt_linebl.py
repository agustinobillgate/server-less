from functions.additional_functions import *
import decimal
from models import Argt_line

def create_argt_linebl(t_argt_line:[T_argt_line]):
    success_flag = False
    argt_line = None

    t_argt_line = None

    t_argt_line_list, T_argt_line = create_model_like(Argt_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, argt_line


        nonlocal t_argt_line
        nonlocal t_argt_line_list
        return {"success_flag": success_flag}

    t_argt_line = query(t_argt_line_list, first=True)

    if t_argt_line:
        success_flag = True

        argt_line = db_session.query(Argt_line).filter(
                (Argt_line.argtnr == t_Argt_line.argtnr) &  (Argt_line.argt_artnr == t_Argt_line.argt_artnr) &  (Argt_line.departement == t_Argt_line.departement) &  (Argt_line.fakt_modus == t_Argt_line.fakt_modus) &  (Argt_line.intervall == t_Argt_line.intervall) &  (Argt_line.kind1 == t_Argt_line.kind1) &  (Argt_line.kind2 == t_Argt_line.kind2) &  (Argt_line.betrag == t_Argt_line.betrag) &  (Argt_line.betriebsnr == t_Argt_line.betriebsnr) &  (Argt_line.vt_percnt == t_Argt_line.vt_percnt)).first()

        if not argt_line:
            argt_line = Argt_line()
            db_session.add(argt_line)

            buffer_copy(t_argt_line, argt_line)


    return generate_output()