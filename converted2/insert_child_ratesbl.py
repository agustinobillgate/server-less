#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Ratecode, Queasy, Htparam

def insert_child_ratesbl(child_code:string, from_date:date, to_date:date):

    prepare_cache ([Queasy, Htparam])

    found_flag = False
    parent_code:string = ""
    in_percent:bool = False
    adjust_value:Decimal = to_decimal("0.0")
    round_betrag:int = 0
    round_method:int = 0
    length_round:int = 0
    rounded_rate:Decimal = to_decimal("0.0")
    ratecode = queasy = htparam = None

    child_ratecode = rbuff = None

    child_ratecode_data, Child_ratecode = create_model_like(Ratecode)

    Rbuff = create_buffer("Rbuff",Ratecode)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal found_flag, parent_code, in_percent, adjust_value, round_betrag, round_method, length_round, rounded_rate, ratecode, queasy, htparam
        nonlocal child_code, from_date, to_date
        nonlocal rbuff


        nonlocal child_ratecode, rbuff
        nonlocal child_ratecode_data

        return {"found_flag": found_flag}

    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, child_code)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1013)]})

    if htparam.feldtyp == 1:
        round_betrag = htparam.finteger
        length_round = length(to_string(round_betrag))

    elif htparam.feldtyp == 5 and num_entries(htparam.fchar, ";") > 1:
        round_betrag = to_int(entry(0, htparam.fchar, ";"))
        length_round = length(to_string(round_betrag))
        round_method = to_int(entry(1, htparam.fchar, ";"))


    parent_code = entry(1, queasy.char3, ";")
    in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
    adjust_value = to_decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100

    for ratecode in db_session.query(Ratecode).filter(
             (Ratecode.code == (parent_code).lower()) & (Ratecode.startperiode <= from_date) & (Ratecode.endperiode >= to_date)).order_by(Ratecode._recid).all():
        child_ratecode = Child_ratecode()
        child_ratecode_data.append(child_ratecode)

        buffer_copy(ratecode, child_ratecode,except_fields=["CODE"])
        found_flag = True
        child_ratecode.code = child_code
        child_ratecode.startperiode = from_date
        child_ratecode.endperiode = to_date

        if adjust_value != 0:

            if in_percent:
                child_ratecode.zipreis =  to_decimal(child_ratecode.zipreis) * to_decimal((1) + to_decimal(adjust_value) * to_decimal(0.01))

                if round_betrag != 0 and child_ratecode.zipreis >= (round_betrag * 10):
                    rounded_rate = round_it(round_method, round_betrag, child_ratecode.zipreis)
                    child_ratecode.zipreis =  to_decimal(rounded_rate)
            else:
                child_ratecode.zipreis =  to_decimal(child_ratecode.zipreis) + to_decimal(adjust_value)

    for child_ratecode in query(child_ratecode_data):

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.marknr == child_ratecode.marknr) & (Ratecode.code == (child_code).lower()) & (Ratecode.argtnr == child_ratecode.argtnr) & (Ratecode.zikatnr == child_ratecode.zikatnr) & (Ratecode.erwachs == child_ratecode.erwachs) & (Ratecode.kind1 == child_ratecode.kind1) & (Ratecode.kind2 == child_ratecode.kind2) & (Ratecode.wday == child_ratecode.wday) & not_ (Ratecode.endperiode < child_ratecode.startperiode) & not_ (Ratecode.startperiode > child_ratecode.endperiode)).order_by(Ratecode._recid).all():

            if ratecode.startperiode < child_ratecode.startperiode:
                ratecode.endperiode = child_ratecode.startperiode - timedelta(days=1)

            elif (ratecode.startperiode >= child_ratecode.startperiode) and (ratecode.endperiode <= child_ratecode.endperiode):
                db_session.delete(ratecode)

            elif (ratecode.startperiode >= child_ratecode.startperiode) and (ratecode.endperiode > child_ratecode.endperiode):
                ratecode.startperiode = child_ratecode.endperiode + timedelta(days=1)
    pass

    for child_ratecode in query(child_ratecode_data):
        rbuff = Ratecode()
        db_session.add(rbuff)

        buffer_copy(child_ratecode, rbuff)

    return generate_output()