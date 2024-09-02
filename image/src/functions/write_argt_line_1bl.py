from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Argt_line, Bediener, Res_history

def write_argt_line_1bl(user_init:str, argtlinebuff:[Argtlinebuff], t_argt_line:[T_argt_line]):
    success_flag = False
    proz:decimal = 0
    betrag:decimal = 0
    bezeich:str = ""
    argt_line = bediener = res_history = None

    t_argt_line = argtlinebuff = temp_bediener = None

    t_argt_line_list, T_argt_line = create_model_like(Argt_line)
    argtlinebuff_list, Argtlinebuff = create_model_like(Argt_line)

    Temp_bediener = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, proz, betrag, bezeich, argt_line, bediener, res_history
        nonlocal temp_bediener


        nonlocal t_argt_line, argtlinebuff, temp_bediener
        nonlocal t_argt_line_list, argtlinebuff_list
        return {"success_flag": success_flag}


    argtlinebuff = query(argtlinebuff_list, first=True)

    t_argt_line = query(t_argt_line_list, first=True)

    if argtlineBuff and t_argt_line:

        argt_line = db_session.query(Argt_line).filter(
                (Argt_line.argtnr == argtlineBuff.argtnr) &  (Argt_line.argt_artnr == argtlineBuff.argt_artnr) &  (Argt_line.departement == argtlineBuff.departement) &  (Argt_line.fakt_modus == argtlineBuff.fakt_modus) &  (Argt_line.intervall == argtlineBuff.intervall) &  (Argt_line.kind1 == argtlineBuff.kind1) &  (Argt_line.kind2 == argtlineBuff.kind2) &  (Argt_line.betrag == argtlineBuff.betrag) &  (Argt_line.betriebsnr == argtlineBuff.betriebsnr) &  (Argt_line.vt_percnt == argtlineBuff.vt_percnt)).first()

        if argt_line:
            betrag = t_argt_line.betrag

            if t_argt_line.betrag <= 0:
                proz = t_argt_line.betrag
                betrag = 0

            temp_bediener = db_session.query(Temp_bediener).filter(
                    (func.lower(Temp_bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = temp_bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Arrangement Lines Setup"


            bezeich = "Change  == > " + "No: " + to_string(t_argt_line.argtnr)

            if argt_line.departement != t_argt_line.departement:
                bezeich = bezeich + " | " + "Dept: " + to_string(argt_line.departement) + " to: " + to_string(t_argt_line.departement)

            if argt_line.argt_artnr != t_argt_line.argt_artnr:
                bezeich = bezeich + " | " + "ArtNo: " + to_string(argt_line.argt_artnr) + " to: " + to_string(t_argt_line.argt_artnr)

            if argt_line.betrag > 0 and argt_line.betrag != betrag:
                bezeich = bezeich + " | " + "Amt: " + to_string(argt_line.betrag) + " to: " + to_string(betrag)

                if t_argt_line.betrag <= 0:
                    bezeich = bezeich + " | " + "In %: " + to_string(betrag) + " to: " + to_string(proz)

            if argt_line.betrag <= 0 and argt_line.betrag != proz:
                bezeich = bezeich + " | " + "In %: " + to_string(argt_line.betrag) + " to: " + to_string(proz)

                if t_argt_line.betrag > 0:
                    bezeich = bezeich + " | " + "Amt: " + to_string(proz) + " to: " + to_string(betrag)

            if argt_line.fakt_modus != t_argt_line.fakt_modus:
                bezeich = bezeich + " | " + "Type: " + to_string(argt_line.fakt_modus) + " to: " + to_string(t_argt_line.fakt_modus)

            if argt_line.kind1 != t_argt_line.kind1:
                bezeich = bezeich + " | " + "Incl: " + to_string(argt_line.kind1) + " to: " + to_string(t_argt_line.kind1)

            if argt_line.kind2 != t_argt_line.kind2:
                bezeich = bezeich + " | " + "Fix: " + to_string(argt_line.kind2) + " to: " + to_string(t_argt_line.kind2)
            res_history.aenderung = bezeich
            buffer_copy(t_argt_line, argt_line)

            success_flag = True

    return generate_output()