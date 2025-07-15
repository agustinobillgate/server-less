#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Ratecode, Htparam, Queasy

def link_edit_ratecodebl(child_code:string, parent_code:string, tb1_char3:string, in_percent:bool, adjust_value:Decimal):

    prepare_cache ([Ratecode, Htparam, Queasy])

    ci_date:date = None
    round_betrag:int = 0
    round_method:int = 0
    length_round:int = 0
    rounded_rate:Decimal = to_decimal("0.0")
    prefix_str:string = "A"
    ratecode = htparam = queasy = None

    rbuff = None

    Rbuff = create_buffer("Rbuff",Ratecode)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, round_betrag, round_method, length_round, rounded_rate, prefix_str, ratecode, htparam, queasy
        nonlocal child_code, parent_code, tb1_char3, in_percent, adjust_value
        nonlocal rbuff


        nonlocal rbuff

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1013)]})

    if htparam.feldtyp == 1:
        round_betrag = htparam.finteger
        length_round = length(to_string(round_betrag))

    elif htparam.feldtyp == 5 and num_entries(htparam.fchar, ";") > 1:
        round_betrag = to_int(entry(0, htparam.fchar, ";"))
        length_round = length(to_string(round_betrag))
        round_method = to_int(entry(1, htparam.fchar, ";"))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    for ratecode in db_session.query(Ratecode).filter(
             (Ratecode.code == (child_code).lower()) & (Ratecode.endperiode >= ci_date)).order_by(Ratecode._recid).all():

        rbuff = get_cache (Ratecode, {"marknr": [(eq, ratecode.marknr)],"code": [(eq, parent_code)],"argtnr": [(eq, ratecode.argtnr)],"zikatnr": [(eq, ratecode.zikatnr)],"erwachs": [(eq, ratecode.erwachs)],"kind1": [(eq, ratecode.kind1)],"kind2": [(eq, ratecode.kind2)],"wday": [(eq, ratecode.wday)],"startperiode": [(le, ratecode.startperiode)],"endperiode": [(ge, ratecode.endperiode)]})

        if rbuff:
            ratecode.zipreis =  to_decimal(rbuff.zipreis)

            if in_percent:
                ratecode.zipreis =  to_decimal(ratecode.zipreis) * to_decimal((1) + to_decimal(adjust_value) * to_decimal(0.01))

                if round_betrag != 0 and ratecode.zipreis >= (round_betrag * 10):
                    rounded_rate = round_it(round_method, round_betrag, ratecode.zipreis)
                    ratecode.zipreis =  to_decimal(rounded_rate)


            else:
                ratecode.zipreis =  to_decimal(ratecode.zipreis) + to_decimal(adjust_value)

    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, child_code)]})

    if in_percent:
        prefix_str = "%"
    queasy.char3 = entry(0, tb1_char3, ";") + ";" + entry(1, tb1_char3, ";") + ";" + prefix_str + to_string(adjust_value * 100)
    pass

    return generate_output()