#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line, Bediener, Res_history

argtlinebuff_data, Argtlinebuff = create_model_like(Argt_line)
t_argt_line_data, T_argt_line = create_model_like(Argt_line)

def write_argt_line_1bl(user_init:string, argtlinebuff_data:[Argtlinebuff], t_argt_line_data:[T_argt_line]):

    prepare_cache ([Argt_line, Bediener, Res_history])

    success_flag = False
    proz:Decimal = to_decimal("0.0")
    betrag:Decimal = to_decimal("0.0")
    bezeich:string = ""
    argt_line = bediener = res_history = None

    t_argt_line = argtlinebuff = temp_bediener = None

    Temp_bediener = create_buffer("Temp_bediener",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, proz, betrag, bezeich, argt_line, bediener, res_history
        nonlocal user_init
        nonlocal temp_bediener


        nonlocal t_argt_line, argtlinebuff, temp_bediener

        return {"success_flag": success_flag}


    argtlinebuff = query(argtlinebuff_data, first=True)

    t_argt_line = query(t_argt_line_data, first=True)

    if argtlinebuff and t_argt_line:

        argt_line = get_cache (Argt_line, {"argtnr": [(eq, argtlinebuff.argtnr)],"argt_artnr": [(eq, argtlinebuff.argt_artnr)],"departement": [(eq, argtlinebuff.departement)],"fakt_modus": [(eq, argtlinebuff.fakt_modus)],"intervall": [(eq, argtlinebuff.intervall)],"kind1": [(eq, argtlinebuff.kind1)],"kind2": [(eq, argtlinebuff.kind2)],"betrag": [(eq, argtlinebuff.betrag)],"betriebsnr": [(eq, argtlinebuff.betriebsnr)],"vt_percnt": [(eq, argtlinebuff.vt_percnt)]})

        if argt_line:
            betrag =  to_decimal(t_argt_line.betrag)

            if t_argt_line.betrag <= 0:
                proz =  to_decimal(t_argt_line.betrag)
                betrag =  to_decimal("0")

            temp_bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = temp_bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Arrangement Lines Setup"


            bezeich = "Change => " + "No: " + to_string(t_argt_line.argtnr) + " | " + "Dept: " + to_string(argt_line.departement) + " - " + "Art: " + to_string(argt_line.argt_artnr)

            if argt_line.departement != t_argt_line.departement:
                bezeich = bezeich + " | " + "DeptNo: " + to_string(argt_line.departement) + " to: " + to_string(t_argt_line.departement)

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
            pass
            success_flag = True

    return generate_output()