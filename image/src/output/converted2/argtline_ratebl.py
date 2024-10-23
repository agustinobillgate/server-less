from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Argt_line, Zimkateg, Artikel, Reslin_queasy

def argtline_ratebl(prcode:str, marknr:int, argtnr:int, zikatnr:int):
    t_argtline_rate_list = []
    argt_line = zimkateg = artikel = reslin_queasy = None

    t_argtline_rate = None

    t_argtline_rate_list, T_argtline_rate = create_model("T_argtline_rate", {"argt_artnr":int, "bezeich":str, "deci1":decimal, "deci2":decimal, "deci3":decimal, "date1":date, "date2":date, "departement":int, "fakt_modus":int, "key":str, "char1":str, "number1":int, "number2":int, "number3":int, "resnr":int, "reslinnr":int, "artnr":int, "s_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_argtline_rate_list, argt_line, zimkateg, artikel, reslin_queasy
        nonlocal prcode, marknr, argtnr, zikatnr


        nonlocal t_argtline_rate
        nonlocal t_argtline_rate_list
        return {"t-argtline-rate": t_argtline_rate_list}

    reslin_queasy_obj_list = []
    for reslin_queasy, argt_line, zimkateg, artikel in db_session.query(Reslin_queasy, Argt_line, Zimkateg, Artikel).join(Argt_line,(Argt_line.argtnr == Reslin_queasy.number2) & (Argt_line.argt_artnr == Reslin_queasy.number3) & (Argt_line.departement == Reslin_queasy.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Reslin_queasy.reslinnr)).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
             (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (prcode).lower()) & (Reslin_queasy.number1 == marknr) & (Reslin_queasy.number2 == argtnr) & (Reslin_queasy.reslinnr == zikatnr)).order_by(Argt_line.argt_artnr, Reslin_queasy.date1).all():
        if reslin_queasy._recid in reslin_queasy_obj_list:
            continue
        else:
            reslin_queasy_obj_list.append(reslin_queasy._recid)


        t_argtline_rate = T_argtline_rate()
        t_argtline_rate_list.append(t_argtline_rate)

        t_argtline_rate.argt_artnr = argt_line.argt_artnr
        t_argtline_rate.bezeich = artikel.bezeich
        t_argtline_rate.deci1 =  to_decimal(reslin_queasy.deci1)
        t_argtline_rate.deci2 =  to_decimal(reslin_queasy.deci2)
        t_argtline_rate.deci3 =  to_decimal(reslin_queasy.deci3)
        t_argtline_rate.date1 = reslin_queasy.date1
        t_argtline_rate.date2 = reslin_queasy.date2
        t_argtline_rate.departement = argt_line.departement
        t_argtline_rate.fakt_modus = argt_line.fakt_modus
        t_argtline_rate.key = reslin_queasy.key
        t_argtline_rate.char1 = reslin_queasy.char1
        t_argtline_rate.number1 = reslin_queasy.number1
        t_argtline_rate.number2 = reslin_queasy.number2
        t_argtline_rate.number3 = reslin_queasy.number3
        t_argtline_rate.resnr = reslin_queasy.resnr
        t_argtline_rate.reslinnr = reslin_queasy.reslinnr
        t_argtline_rate.artnr = artikel.artnr
        t_argtline_rate.s_recid = argt_line._recid

    return generate_output()