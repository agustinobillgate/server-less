#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Argt_line, Reslin_queasy, Bediener, Res_history, Artikel, Arrangement

p_list_data, P_list = create_model_like(Argt_line)

def argt_frate_fill_rate_1_webbl(icase:int, s_recid:int, argtnr:int, resnr:int, reslinnr:int, ch1_betrag:Decimal, ch2_betrag:Decimal, from_date:date, to_date:date, vt_percnt:int, user_init:string, p_list_data:[P_list]):

    prepare_cache ([Bediener, Res_history, Artikel, Arrangement])

    argt_line = reslin_queasy = bediener = res_history = artikel = arrangement = None

    p_list = t_reslin_queasy = None

    t_reslin_queasy_data, T_reslin_queasy = create_model_like(Reslin_queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal argt_line, reslin_queasy, bediener, res_history, artikel, arrangement
        nonlocal icase, s_recid, argtnr, resnr, reslinnr, ch1_betrag, ch2_betrag, from_date, to_date, vt_percnt, user_init


        nonlocal p_list, t_reslin_queasy
        nonlocal t_reslin_queasy_data

        return {"s_recid": s_recid}

    def add_argt():

        nonlocal argt_line, reslin_queasy, bediener, res_history, artikel, arrangement
        nonlocal icase, s_recid, argtnr, resnr, reslinnr, ch1_betrag, ch2_betrag, from_date, to_date, vt_percnt, user_init


        nonlocal p_list, t_reslin_queasy
        nonlocal t_reslin_queasy_data


        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "fargt-line"
        reslin_queasy.number1 = p_list.departement
        reslin_queasy.number2 = argtnr
        reslin_queasy.number3 = p_list.argt_artnr
        reslin_queasy.resnr = resnr
        reslin_queasy.reslinnr = reslinnr
        reslin_queasy.deci1 =  to_decimal(p_list.betrag)
        reslin_queasy.deci2 =  to_decimal(ch1_betrag)
        reslin_queasy.deci3 =  to_decimal(ch2_betrag)
        reslin_queasy.date1 = from_date
        reslin_queasy.date2 = to_date
        reslin_queasy.char2 = to_string(p_list.vt_percnt)

        pass
        s_recid = to_int(reslin_queasy._recid)

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Arrangement Line"
            res_history.aenderung = "Create a new arrangement line for reservation no " + to_string(resnr) + "/" + to_string(reslinnr) + ", arrangement no: " + to_string(p_list.argt_artnr) + ", outlet no: " + to_string(p_list.departement)

            artikel = get_cache (Artikel, {"artnr": [(eq, p_list.argt_artnr)],"departement": [(eq, p_list.departement)]})

            if artikel:
                res_history.aenderung = res_history.aenderung + " - " + artikel.bezeich

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, p_list.argtnr)]})

            if arrangement:
                res_history.aenderung = res_history.aenderung + " in " + arrangement.arrangement
            pass


    def chg_argt():

        nonlocal argt_line, reslin_queasy, bediener, res_history, artikel, arrangement
        nonlocal icase, s_recid, argtnr, resnr, reslinnr, ch1_betrag, ch2_betrag, from_date, to_date, vt_percnt, user_init


        nonlocal p_list, t_reslin_queasy
        nonlocal t_reslin_queasy_data

        reslin_queasy = get_cache (Reslin_queasy, {"_recid": [(eq, s_recid)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
            pass
            reslin_queasy.deci1 =  to_decimal(p_list.betrag)
            reslin_queasy.deci2 =  to_decimal(ch1_betrag)
            reslin_queasy.deci3 =  to_decimal(ch2_betrag)
            reslin_queasy.date1 = from_date
            reslin_queasy.date2 = to_date
            reslin_queasy.char2 = to_string(p_list.vt_percnt)

            pass
            pass

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        t_reslin_queasy = query(t_reslin_queasy_data, first=True)

        if bediener and t_reslin_queasy:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Arrangement Line"
            res_history.aenderung = "Modify arrangement line for reservation no " + to_string(resnr) + "/" + to_string(reslinnr) + ", arrangement no: " + to_string(p_list.argt_artnr) + ", outlet no: " + to_string(p_list.departement) + " of "

            if t_reslin_queasy.deci1 != p_list.betrag:
                res_history.aenderung = res_history.aenderung + "adult amount from " + trim(to_string(t_reslin_queasy.deci1, "->>>,>>>,>>>,>>9.99")) + " to " + trim(to_string(p_list.betrag, "->>>,>>>,>>>,>>9.99")) + ", "

            if t_reslin_queasy.deci2 != ch1_betrag:
                res_history.aenderung = res_history.aenderung + "child amount from " + trim(to_string(t_reslin_queasy.deci2, "->>>,>>>,>>>,>>9.99")) + " to " + trim(to_string(ch1_betrag, "->>>,>>>,>>>,>>9.99")) + ", "

            if t_reslin_queasy.deci3 != ch2_betrag:
                res_history.aenderung = res_history.aenderung + "infant amount from " + trim(to_string(t_reslin_queasy.deci3, "->>>,>>>,>>>,>>9.99")) + " to " + trim(to_string(ch2_betrag, "->>>,>>>,>>>,>>9.99")) + ", "

            if (t_reslin_queasy.date1 != from_date) or (t_reslin_queasy.date2 != to_date):
                res_history.aenderung = res_history.aenderung + "period date from " + trim(to_string(t_reslin_queasy.date1, "99/99/9999")) + " - " + trim(to_string(t_reslin_queasy.date2, "99/99/9999")) + " to " + trim(to_string(from_date, "99/99/9999")) + " - " + trim(to_string(to_date, "99/99/9999")) + ", "

            if t_reslin_queasy.char2 != to_string(p_list.vt_percnt):
                res_history.aenderung = res_history.aenderung + "in % from" + t_reslin_queasy.char2 + " to " + to_string(p_list.vt_percnt)

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, p_list.argtnr)]})

            if arrangement:
                res_history.aenderung = res_history.aenderung + " in " + arrangement.arrangement

            t_reslin_queasy_data.clear()
            pass


    def del_argt():

        nonlocal argt_line, reslin_queasy, bediener, res_history, artikel, arrangement
        nonlocal icase, s_recid, argtnr, resnr, reslinnr, ch1_betrag, ch2_betrag, from_date, to_date, vt_percnt, user_init


        nonlocal p_list, t_reslin_queasy
        nonlocal t_reslin_queasy_data

        argt_artnr:int = 0
        dpt:int = 0

        reslin_queasy = get_cache (Reslin_queasy, {"_recid": [(eq, s_recid)]})

        if reslin_queasy:
            argt_artnr = reslin_queasy.number3
            dpt = reslin_queasy.number1

            pass
            db_session.delete(reslin_queasy)
            pass

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Arrangement Line"
            res_history.aenderung = "Delete arrangement line for reservation no " + to_string(resnr) + "/" + to_string(reslinnr) + ", arrangement no: " + to_string(argt_artnr) + ", outlet no: " + to_string(dpt)

            artikel = get_cache (Artikel, {"artnr": [(eq, argt_artnr)],"departement": [(eq, dpt)]})

            if artikel:
                res_history.aenderung = res_history.aenderung + " - " + artikel.bezeich

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, argtnr)]})

            if arrangement:
                res_history.aenderung = res_history.aenderung + " in " + arrangement.arrangement
            pass


    p_list = query(p_list_data, first=True)

    if icase == 1:
        add_argt()
    elif icase == 2:
        chg_argt()
    elif icase == 3:
        del_argt()

    return generate_output()