from functions.additional_functions import *
import decimal
from datetime import date
from models import Argt_line, Reslin_queasy

def argt_frate_fill_rate_1bl(icase:int, s_recid:int, argtnr:int, resnr:int, reslinnr:int, ch1_betrag:decimal, ch2_betrag:decimal, from_date:date, to_date:date, vt_percnt:int, p_list:[P_list]):
    argt_line = reslin_queasy = None

    p_list = None

    p_list_list, P_list = create_model_like(Argt_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal argt_line, reslin_queasy


        nonlocal p_list
        nonlocal p_list_list
        return {}

    def add_argt():

        nonlocal argt_line, reslin_queasy


        nonlocal p_list
        nonlocal p_list_list


        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "fargt_line"
        reslin_queasy.number1 = p_list.departement
        reslin_queasy.number2 = argtnr
        reslin_queasy.number3 = p_list.argt_artnr
        reslin_queasy.resnr = resnr
        reslin_queasy.reslinnr = reslinnr
        reslin_queasy.deci1 = p_list.betrag
        reslin_queasy.deci2 = ch1_betrag
        reslin_queasy.deci3 = ch2_betrag
        reslin_queasy.date1 = from_date
        reslin_queasy.date2 = to_date
        reslin_queasy.char2 = to_string(p_list.vt_percnt)

        reslin_queasy = db_session.query(Reslin_queasy).first()
        s_recid = to_int(reslin_queasy._recid)

    def chg_argt():

        nonlocal argt_line, reslin_queasy


        nonlocal p_list
        nonlocal p_list_list

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (Reslin_queasy._recid == s_recid)).first()

        if reslin_queasy:

            reslin_queasy = db_session.query(Reslin_queasy).first()
            reslin_queasy.deci1 = p_list.betrag
            reslin_queasy.deci2 = ch1_betrag
            reslin_queasy.deci3 = ch2_betrag
            reslin_queasy.date1 = from_date
            reslin_queasy.date2 = to_date
            reslin_queasy.char2 = to_string(p_list.vt_percnt)

            reslin_queasy = db_session.query(Reslin_queasy).first()


    def del_argt():

        nonlocal argt_line, reslin_queasy


        nonlocal p_list
        nonlocal p_list_list

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (Reslin_queasy._recid == s_recid)).first()

        if reslin_queasy:

            reslin_queasy = db_session.query(Reslin_queasy).first()
            db_session.delete(reslin_queasy)


    pass


    p_list = query(p_list_list, first=True)

    if icase == 1:
        add_argt()
    elif icase == 2:
        chg_argt()
    elif icase == 3:
        del_argt()

    return generate_output()