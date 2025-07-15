#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Argt_line, Reslin_queasy

p_list_data, P_list = create_model_like(Argt_line)

def argt_frate_fill_rate_1bl(icase:int, s_recid:int, argtnr:int, resnr:int, reslinnr:int, ch1_betrag:Decimal, ch2_betrag:Decimal, from_date:date, to_date:date, vt_percnt:int, p_list_data:[P_list]):
    argt_line = reslin_queasy = None

    p_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal argt_line, reslin_queasy
        nonlocal icase, s_recid, argtnr, resnr, reslinnr, ch1_betrag, ch2_betrag, from_date, to_date, vt_percnt


        nonlocal p_list

        return {"s_recid": s_recid}

    def add_argt():

        nonlocal argt_line, reslin_queasy
        nonlocal icase, s_recid, argtnr, resnr, reslinnr, ch1_betrag, ch2_betrag, from_date, to_date, vt_percnt


        nonlocal p_list


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


    def chg_argt():

        nonlocal argt_line, reslin_queasy
        nonlocal icase, s_recid, argtnr, resnr, reslinnr, ch1_betrag, ch2_betrag, from_date, to_date, vt_percnt


        nonlocal p_list

        reslin_queasy = get_cache (Reslin_queasy, {"_recid": [(eq, s_recid)]})

        if reslin_queasy:
            pass
            reslin_queasy.deci1 =  to_decimal(p_list.betrag)
            reslin_queasy.deci2 =  to_decimal(ch1_betrag)
            reslin_queasy.deci3 =  to_decimal(ch2_betrag)
            reslin_queasy.date1 = from_date
            reslin_queasy.date2 = to_date
            reslin_queasy.char2 = to_string(p_list.vt_percnt)


            pass
            pass


    def del_argt():

        nonlocal argt_line, reslin_queasy
        nonlocal icase, s_recid, argtnr, resnr, reslinnr, ch1_betrag, ch2_betrag, from_date, to_date, vt_percnt


        nonlocal p_list

        reslin_queasy = get_cache (Reslin_queasy, {"_recid": [(eq, s_recid)]})

        if reslin_queasy:
            pass
            db_session.delete(reslin_queasy)
            pass

    p_list = query(p_list_data, first=True)

    if icase == 1:
        add_argt()
    elif icase == 2:
        chg_argt()
    elif icase == 3:
        del_argt()

    return generate_output()