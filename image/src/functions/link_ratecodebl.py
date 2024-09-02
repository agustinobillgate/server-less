from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Ratecode, Prtable, Htparam, Queasy

def link_ratecodebl(child_code:str, parent_code:str, tb1_char3:str, in_percent:bool, adjust_value:decimal):
    ci_date:date = None
    round_betrag:int = 0
    round_method:int = 0
    length_round:int = 0
    curr_i:int = 0
    rate_str:str = ""
    rounded_rate:decimal = 0
    found_flag:bool = False
    ratecode = prtable = htparam = queasy = None

    product_list = rbuff = prbuff = None

    product_list_list, Product_list = create_model("Product_list", {"market":int, "i_product":int})

    Rbuff = Ratecode
    Prbuff = Prtable

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, round_betrag, round_method, length_round, curr_i, rate_str, rounded_rate, found_flag, ratecode, prtable, htparam, queasy
        nonlocal rbuff, prbuff


        nonlocal product_list, rbuff, prbuff
        nonlocal product_list_list
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
            (func.lower(Ratecode.code) == (child_code).lower())).all():

        rbuff = db_session.query(Rbuff).filter(
                (func.lower(Rbuff.code) == (parent_code).lower()) &  (Rbuff.marknr == ratecode.marknr) &  (Rbuff.zikatnr == ratecode.zikatnr) &  (Rbuff.argtnr == ratecode.argtnr)).first()

        if rbuff:
            db_session.delete(ratecode)

    for prtable in db_session.query(Prtable).filter(
            (func.lower(Prtable.prcode) == (child_code).lower())).all():
        for curr_i in range(1,99 + 1) :

            if prtable.product[curr_i - 1] == 0:
                break

            if prtable.product[curr_i - 1] >= 90001:

                rbuff = db_session.query(Rbuff).filter(
                        (Rbuff.CODE == prtable.prcode) &  (Rbuff.marknr == prtable.marknr) &  (((90 + Rbuff.zikatnr) * 1000 + Rbuff.argtnr) == prtable.product[curr_i - 1])).first()

            elif prtable.product[curr_i - 1] >= 10001:

                rbuff = db_session.query(Rbuff).filter(
                        (Rbuff.CODE == prtable.prcode) &  (Rbuff.marknr == prtable.marknr) &  ((Rbuff.zikatnr * 1000 + Rbuff.argtnr) == prtable.product[curr_i - 1])).first()
            else:

                rbuff = db_session.query(Rbuff).filter(
                        (Rbuff.CODE == prtable.prcode) &  (Rbuff.marknr == prtable.marknr) &  ((Rbuff.zikatnr * 100 + Rbuff.argtnr) == prtable.product[curr_i - 1])).first()

            if rbuff:
                product_list = Product_list()
                product_list_list.append(product_list)

                product_list.market = prtable.marknr
                product_list.i_product = prtable.product[curr_i - 1]


        db_session.delete(prtable)

    for ratecode in db_session.query(Ratecode).filter(
            (func.lower(Ratecode.code) == (parent_code).lower()) &  (Ratecode.endperiode >= ci_date)).all():
        rbuff = Rbuff()
        db_session.add(rbuff)

        buffer_copy(ratecode, rbuff,except_fields=["CODE"])
        rbuff.CODE = child_code

        if in_percent:
            rbuff.zipreis = rbuff.zipreis * (1 + adjust_value * 0.01)

            if round_betrag != 0 and rbuff.zipreis >= (round_betrag * 10):
                rounded_rate = round_it(rbuff.zipreis)
                rbuff.zipreis = rounded_rate


        else:
            rbuff.zipreis = rbuff.zipreis + adjust_value

    for prtable in db_session.query(Prtable).filter(
            (func.lower(Prtable.prcode) == (parent_code).lower())).all():
        prbuff = Prbuff()
        db_session.add(prbuff)

        buffer_copy(prtable, prbuff,except_fields=["prcode"])
        prbuff.prcode = child_code

        for product_list in query(product_list_list, filters=(lambda product_list :product_list.market == prbuff.marknr)):
            for curr_i in range(1,99 + 1) :

                if prbuff.product[curr_i - 1] == 0:
                    prbuff.product[curr_i - 1] = product_list.i_product


                    product_list_list.remove(product_list)
                    curr_i = 9999

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (func.lower(Queasy.char1) == (child_code).lower())).first()
    queasy.char3 = tb1_char3

    queasy = db_session.query(Queasy).first()

    return generate_output()