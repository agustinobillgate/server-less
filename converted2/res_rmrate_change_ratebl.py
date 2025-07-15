#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from functions.ratecode_rate import ratecode_rate
from models import Res_line, Arrangement

def res_rmrate_change_ratebl(resnr:int, reslinnr:int, curr_code:string, argt:string, datum:date):

    prepare_cache ([Res_line, Arrangement])

    rmrate = to_decimal("0.0")
    ebdisc_flag:bool = False
    kbdisc_flag:bool = False
    rate_found:bool = False
    early_flag:bool = False
    kback_flag:bool = False
    rm_rate:Decimal = to_decimal("0.0")
    res_line = arrangement = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmrate, ebdisc_flag, kbdisc_flag, rate_found, early_flag, kback_flag, rm_rate, res_line, arrangement
        nonlocal resnr, reslinnr, curr_code, argt, datum

        return {"rmrate": rmrate}


    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if res_line:

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, argt)]})

        if arrangement:
            ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
            kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))


            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, curr_code, None, datum, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, res_line.zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

            if rate_found :
                rmrate =  to_decimal(rm_rate)

    return generate_output()