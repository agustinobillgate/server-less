#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line, Bediener, Res_history

t_argt_line_list, T_argt_line = create_model_like(Argt_line)

def create_argt_line_1bl(user_init:string, t_argt_line_list:[T_argt_line]):

    prepare_cache ([Bediener, Res_history])

    success_flag = False
    proz:Decimal = to_decimal("0.0")
    betrag:Decimal = to_decimal("0.0")
    force_qty_stats:bool = False
    argt_line = bediener = res_history = None

    t_argt_line = temp_bediener = None

    Temp_bediener = create_buffer("Temp_bediener",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, proz, betrag, force_qty_stats, argt_line, bediener, res_history
        nonlocal user_init
        nonlocal temp_bediener


        nonlocal t_argt_line, temp_bediener

        return {"success_flag": success_flag}

    t_argt_line = query(t_argt_line_list, first=True)

    if t_argt_line:
        success_flag = True
        betrag =  to_decimal(t_argt_line.betrag)

        argt_line = get_cache (Argt_line, {"argtnr": [(eq, t_argt_line.argtnr)],"argt_artnr": [(eq, t_argt_line.argt_artnr)],"departement": [(eq, t_argt_line.departement)],"fakt_modus": [(eq, t_argt_line.fakt_modus)],"intervall": [(eq, t_argt_line.intervall)],"kind1": [(eq, t_argt_line.kind1)],"kind2": [(eq, t_argt_line.kind2)],"betrag": [(eq, t_argt_line.betrag)],"betriebsnr": [(eq, t_argt_line.betriebsnr)],"vt_percnt": [(eq, t_argt_line.vt_percnt)]})

        if not argt_line:
            argt_line = Argt_line()
            db_session.add(argt_line)

            buffer_copy(t_argt_line, argt_line)
            pass

        temp_bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if t_argt_line.betrag <= 0:
            proz =  to_decimal(t_argt_line.betrag)
            betrag =  to_decimal("0")

        if t_argt_line.betriebsnr == 1:
            force_qty_stats = True
        else:
            force_qty_stats = False
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = temp_bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Arrangement Lines Setup"
        res_history.aenderung = "Create => " + "No: " + to_string(t_argt_line.argtnr) + " | " +\
                "Dept: " + to_string(t_argt_line.departement) + " | " +\
                "ArtNo: " + to_string(t_argt_line.argt_artnr) + " | " +\
                "Amt: " + to_string(betrag) + " | " +\
                "In %: " + to_string(proz) + " | " +\
                "Type: " + to_string(t_argt_line.fakt_modus) + " | " +\
                "Incl: " + to_string(t_argt_line.kind1) + " | " +\
                "Fixt: " + to_string(t_argt_line.kind2) + " | " +\
                "Force One Qty: " + to_string(force_qty_stats)

    return generate_output()