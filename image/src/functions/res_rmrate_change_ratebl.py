from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from functions.ratecode_rate import ratecode_rate
from models import Res_line, Arrangement

def res_rmrate_change_ratebl(resnr:int, reslinnr:int, curr_code:str, argt:str, datum:date):
    rmrate = 0
    ebdisc_flag:bool = False
    kbdisc_flag:bool = False
    rate_found:bool = False
    early_flag:bool = False
    kback_flag:bool = False
    rm_rate:decimal = 0
    res_line = arrangement = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmrate, ebdisc_flag, kbdisc_flag, rate_found, early_flag, kback_flag, rm_rate, res_line, arrangement


        return {"rmrate": rmrate}


    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if res_line:

        arrangement = db_session.query(Arrangement).filter(
                (func.lower(Arrangement) == (argt).lower())).first()

        if arrangement:
            ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
            kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)


            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, curr_code, None, datum, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, res_line.zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

            if rate_found :
                rmrate = rm_rate

    return generate_output()