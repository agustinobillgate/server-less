from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Argt_line, Bediener, Res_history

def create_argt_line_1bl(user_init:str, t_argt_line:[T_argt_line]):
    success_flag = False
    proz:decimal = 0
    betrag:decimal = 0
    argt_line = bediener = res_history = None

    t_argt_line = temp_bediener = None

    t_argt_line_list, T_argt_line = create_model_like(Argt_line)

    Temp_bediener = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, proz, betrag, argt_line, bediener, res_history
        nonlocal temp_bediener


        nonlocal t_argt_line, temp_bediener
        nonlocal t_argt_line_list
        return {"success_flag": success_flag}

    t_argt_line = query(t_argt_line_list, first=True)

    if t_argt_line:
        success_flag = True
        betrag = t_argt_line.betrag

        argt_line = db_session.query(Argt_line).filter(
                (Argt_line.argtnr == t_Argt_line.argtnr) &  (Argt_line.argt_artnr == t_Argt_line.argt_artnr) &  (Argt_line.departement == t_Argt_line.departement) &  (Argt_line.fakt_modus == t_Argt_line.fakt_modus) &  (Argt_line.intervall == t_Argt_line.intervall) &  (Argt_line.kind1 == t_Argt_line.kind1) &  (Argt_line.kind2 == t_Argt_line.kind2) &  (Argt_line.betrag == t_Argt_line.betrag) &  (Argt_line.betriebsnr == t_Argt_line.betriebsnr) &  (Argt_line.vt_percnt == t_Argt_line.vt_percnt)).first()

        if not argt_line:
            argt_line = Argt_line()
            db_session.add(argt_line)

            buffer_copy(t_argt_line, argt_line)


        temp_bediener = db_session.query(Temp_bediener).filter(
                (func.lower(Temp_bediener.userinit) == (user_init).lower())).first()

        if t_argt_line.betrag <= 0:
            proz = t_argt_line.betrag
            betrag = 0
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = temp_bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Arrangement Lines Setup"
        res_history.aenderung = "Create  == > " + "No: " + to_string(t_argt_line.argtnr) + " | " +\
                "Dept: " + to_string(t_argt_line.departement) + " | " +\
                "ArtNo: " + to_string(t_argt_line.argt_artnr) + " | " +\
                "Amt: " + to_string(betrag) + " | " +\
                "In %: " + to_string(proz) + " | " +\
                "Type: " + to_string(t_argt_line.fakt_modus) + " | " +\
                "Incl: " + to_string(t_argt_line.kind1) + " | " +\
                "Fixt: " + to_string(t_argt_line.kind2)

    return generate_output()