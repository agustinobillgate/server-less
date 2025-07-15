#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line, Bediener, Res_history

t_argt_line_data, T_argt_line = create_model_like(Argt_line)

def delete_argt_line_1bl(case_type:int, int1:int, user_init:string, t_argt_line_data:[T_argt_line]):

    prepare_cache ([Bediener, Res_history])

    success_flag = False
    proz:Decimal = to_decimal("0.0")
    betrag:Decimal = to_decimal("0.0")
    argt_line = bediener = res_history = None

    t_argt_line = temp_bediener = None

    Temp_bediener = create_buffer("Temp_bediener",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, proz, betrag, argt_line, bediener, res_history
        nonlocal case_type, int1, user_init
        nonlocal temp_bediener


        nonlocal t_argt_line, temp_bediener

        return {"success_flag": success_flag}

    if case_type == 1:

        t_argt_line = query(t_argt_line_data, first=True)

        if not t_argt_line:

            return generate_output()

        argt_line = get_cache (Argt_line, {"argtnr": [(eq, t_argt_line.argtnr)],"argt_artnr": [(eq, t_argt_line.argt_artnr)],"departement": [(eq, t_argt_line.departement)],"fakt_modus": [(eq, t_argt_line.fakt_modus)],"intervall": [(eq, t_argt_line.intervall)],"kind1": [(eq, t_argt_line.kind1)],"kind2": [(eq, t_argt_line.kind2)],"betrag": [(eq, t_argt_line.betrag)],"betriebsnr": [(eq, t_argt_line.betriebsnr)],"vt_percnt": [(eq, t_argt_line.vt_percnt)]})

        if argt_line:
            db_session.delete(argt_line)
            pass
            success_flag = True
            betrag =  to_decimal(t_argt_line.betrag)

            temp_bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if t_argt_line.betrag <= 0:
                proz =  to_decimal(t_argt_line.betrag)
                betrag =  to_decimal("0")
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = temp_bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Arrangement Lines Setup"
            res_history.aenderung = "Delete => " + "No: " + to_string(t_argt_line.argtnr) + " | " +\
                    "Dept: " + to_string(t_argt_line.departement) + " | " +\
                    "ArtNo: " + to_string(t_argt_line.argt_artnr) + " | " +\
                    "Amt: " + to_string(betrag) + " | " +\
                    "In %: " + to_string(proz) + " | " +\
                    "Type: " + to_string(t_argt_line.fakt_modus) + " | " +\
                    "Incl: " + to_string(t_argt_line.kind1) + " | " +\
                    "Fix: " + to_string(t_argt_line.kind2)


    elif case_type == 2:

        argt_line = get_cache (Argt_line, {"_recid": [(eq, int1)]})

        if argt_line:
            db_session.delete(argt_line)
            pass
            success_flag = True

    return generate_output()