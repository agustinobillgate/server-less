from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Ratecode, Htparam, Queasy

def link_edit_ratecodebl(child_code:str, parent_code:str, tb1_char3:str, in_percent:bool, adjust_value:decimal):
    ci_date:date = None
    round_betrag:int = 0
    round_method:int = 0
    length_round:int = 0
    rounded_rate:decimal = 0
    prefix_str:str = "A"
    ratecode = htparam = queasy = None

    rbuff = None

    Rbuff = Ratecode

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, round_betrag, round_method, length_round, rounded_rate, prefix_str, ratecode, htparam, queasy
        nonlocal rbuff


        nonlocal rbuff
        return {}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1013)).first()

    if htparam.feldtyp == 1:
        round_betrag = htparam.finteger
        length_round = len(to_string(round_betrag))

    elif htparam.feldtyp == 5 and num_entries(htparam.fchar, ";") > 1:
        round_betrag = to_int(entry(0, htparam.fchar, ";"))
        length_round = len(to_string(round_betrag))
        round_method = to_int(entry(1, htparam.fchar, ";"))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    for ratecode in db_session.query(Ratecode).filter(
            (func.lower(Ratecode.code) == (child_code).lower()) &  (Ratecode.endperiode >= ci_date)).all():

        rbuff = db_session.query(Rbuff).filter(
                (Rbuff.marknr == ratecode.marknr) &  (func.lower(Rbuff.code) == (parent_code).lower()) &  (Rbuff.argtnr == ratecode.argtnr) &  (Rbuff.zikatnr == ratecode.zikatnr) &  (Rbuff.erwachs == ratecode.erwachs) &  (Rbuff.kind1 == ratecode.kind1) &  (Rbuff.kind2 == ratecode.kind2) &  (Rbuff.wday == ratecode.wday) &  (Rbuff.startperiode <= ratecode.startperiode) &  (Rbuff.endperiode >= ratecode.endperiode)).first()

        if rbuff:
            ratecode.zipreis = rbuff.zipreis

            if in_percent:
                ratecode.zipreis = ratecode.zipreis * (1 + adjust_value * 0.01)

                if round_betrag != 0 and ratecode.zipreis >= (round_betrag * 10):
                    rounded_rate = round_it(ratecode.zipreis)
                    ratecode.zipreis = rounded_rate


            else:
                ratecode.zipreis = ratecode.zipreis + adjust_value

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (func.lower(Queasy.char1) == (child_code).lower())).first()

    if in_percent:
        prefix_str = "%"
    queasy.char3 = entry(0, tb1_char3, ";") + ";" + entry(1, tb1_char3, ";") + ";" + prefix_str + to_string(adjust_value * 100)

    queasy = db_session.query(Queasy).first()

    return generate_output()