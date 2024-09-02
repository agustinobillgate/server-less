from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Ratecode, Queasy, Htparam

def insert_child_ratesbl(child_code:str, from_date:date, to_date:date):
    found_flag = False
    parent_code:str = ""
    in_percent:bool = False
    adjust_value:decimal = 0
    round_betrag:int = 0
    round_method:int = 0
    length_round:int = 0
    rounded_rate:decimal = 0
    ratecode = queasy = htparam = None

    child_ratecode = rbuff = None

    child_ratecode_list, Child_ratecode = create_model_like(Ratecode)

    Rbuff = Ratecode

    db_session = local_storage.db_session

    def generate_output():
        nonlocal found_flag, parent_code, in_percent, adjust_value, round_betrag, round_method, length_round, rounded_rate, ratecode, queasy, htparam
        nonlocal rbuff


        nonlocal child_ratecode, rbuff
        nonlocal child_ratecode_list
        return {"found_flag": found_flag}

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (func.lower(Queasy.char1) == (child_code).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1013)).first()

    if htparam.feldtyp == 1:
        round_betrag = htparam.finteger
        length_round = len(to_string(round_betrag))

    elif htparam.feldtyp == 5 and num_entries(htparam.fchar, ";") > 1:
        round_betrag = to_int(entry(0, htparam.fchar, ";"))
        length_round = len(to_string(round_betrag))
        round_method = to_int(entry(1, htparam.fchar, ";"))


    parent_code = entry(1, queasy.char3, ";")
    in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
    adjust_value = decimal.Decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100

    for ratecode in db_session.query(Ratecode).filter(
            (func.lower(Ratecode.code) == (parent_code).lower()) &  (Ratecode.startperiode <= from_date) &  (Ratecode.endperiode >= to_date)).all():
        child_ratecode = Child_ratecode()
        child_ratecode_list.append(child_ratecode)

        buffer_copy(ratecode, child_ratecode,except_fields=["CODE"])
        found_flag = True
        child_ratecode.CODE = child_code
        child_ratecode.startperiode = from_date
        child_ratecode.endperiode = to_date

        if adjust_value != 0:

            if in_percent:
                child_ratecode.zipreis = child_ratecode.zipreis * (1 + adjust_value * 0.01)

                if round_betrag != 0 and child_ratecode.zipreis >= (round_betrag * 10):
                    rounded_rate = round_it(child_ratecode.zipreis)
                    child_ratecode.zipreis = rounded_rate
            else:
                child_ratecode.zipreis = child_ratecode.zipreis + adjust_value

    for child_ratecode in query(child_ratecode_list):

        for ratecode in db_session.query(Ratecode).filter(
                (Ratecode.marknr == child_Ratecode.marknr) &  (func.lower(Ratecode.code) == (child_code).lower()) &  (Ratecode.argtnr == child_Ratecode.argtnr) &  (Ratecode.zikatnr == child_Ratecode.zikatnr) &  (Ratecode.erwachs == child_Ratecode.erwachs) &  (Ratecode.kind1 == child_Ratecode.kind1) &  (Ratecode.kind2 == child_Ratecode.kind2) &  (Ratecode.wday == child_Ratecode.wday) &  (not Ratecode.endperiode < child_Ratecode.startperiode) &  (not Ratecode.startperiode > child_Ratecode.endperiode)).all():

            if ratecode.startperiode < child_ratecode.startperiode:
                ratecode.endperiode = child_ratecode.startperiode - 1

            elif (ratecode.startperiode >= child_ratecode.startperiode) and (ratecode.endperiode <= child_ratecode.endperiode):
                db_session.delete(ratecode)

            elif (ratecode.startperiode >= child_ratecode.startperiode) and (ratecode.endperiode > child_ratecode.endperiode):
                ratecode.startperiode = child_ratecode.endperiode + 1

    for child_ratecode in query(child_ratecode_list):
        rbuff = Rbuff()
        db_session.add(rbuff)

        buffer_copy(child_ratecode, rbuff)

    return generate_output()