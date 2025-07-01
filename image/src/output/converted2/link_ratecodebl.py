#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Ratecode, Prtable, Htparam, Queasy

def link_ratecodebl(child_code:string, parent_code:string, tb1_char3:string, in_percent:bool, adjust_value:Decimal):

    prepare_cache ([Ratecode, Prtable, Htparam, Queasy])

    ci_date:date = None
    round_betrag:int = 0
    round_method:int = 0
    length_round:int = 0
    curr_i:int = 0
    rate_str:string = ""
    rounded_rate:Decimal = to_decimal("0.0")
    found_flag:bool = False
    ratecode = prtable = htparam = queasy = None

    product_list = rbuff = prbuff = None

    product_list_list, Product_list = create_model("Product_list", {"market":int, "i_product":int})

    Rbuff = create_buffer("Rbuff",Ratecode)
    Prbuff = create_buffer("Prbuff",Prtable)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, round_betrag, round_method, length_round, curr_i, rate_str, rounded_rate, found_flag, ratecode, prtable, htparam, queasy
        nonlocal child_code, parent_code, tb1_char3, in_percent, adjust_value
        nonlocal rbuff, prbuff


        nonlocal product_list, rbuff, prbuff
        nonlocal product_list_list

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
             (Ratecode.code == (child_code).lower())).order_by(Ratecode._recid).all():

        rbuff = get_cache (Ratecode, {"code": [(eq, parent_code)],"marknr": [(eq, ratecode.marknr)],"zikatnr": [(eq, ratecode.zikatnr)],"argtnr": [(eq, ratecode.argtnr)]})

        if rbuff:
            db_session.delete(ratecode)

    for prtable in db_session.query(Prtable).filter(
             (Prtable.prcode == (child_code).lower())).order_by(Prtable._recid).yield_per(100):
        for curr_i in range(1,99 + 1) :

            if prtable.product[curr_i - 1] == 0:
                break

            if prtable.product[curr_i - 1] >= 90001:

                rbuff = get_cache (Ratecode, {"code": [(eq, prtable.prcode)],"marknr": [(eq, prtable.marknr)],"argtnr ": [(eq, prtable.product[curr_i - 1])]})

            elif prtable.product[curr_i - 1] >= 10001:

                rbuff = get_cache (Ratecode, {"code": [(eq, prtable.prcode)],"marknr": [(eq, prtable.marknr)],"argtnr ": [(eq, prtable.product[curr_i - 1])]})
            else:

                rbuff = get_cache (Ratecode, {"code": [(eq, prtable.prcode)],"marknr": [(eq, prtable.marknr)],"argtnr ": [(eq, prtable.product[curr_i - 1])]})

            if rbuff:
                product_list = Product_list()
                product_list_list.append(product_list)

                product_list.market = prtable.marknr
                product_list.i_product = prtable.product[curr_i - 1]


        db_session.delete(prtable)

    for ratecode in db_session.query(Ratecode).filter(
             (Ratecode.code == (parent_code).lower()) & (Ratecode.endperiode >= ci_date)).order_by(Ratecode._recid).all():
        rbuff = Ratecode()
        db_session.add(rbuff)

        buffer_copy(ratecode, rbuff,except_fields=["CODE"])
        rbuff.code = child_code

        if in_percent:
            rbuff.zipreis =  to_decimal(rbuff.zipreis) * to_decimal((1) + to_decimal(adjust_value) * to_decimal(0.01))

            if round_betrag != 0 and rbuff.zipreis >= (round_betrag * 10):
                rounded_rate = round_it(round_method, round_betrag, rbuff.zipreis)
                rbuff.zipreis =  to_decimal(rounded_rate)


        else:
            rbuff.zipreis =  to_decimal(rbuff.zipreis) + to_decimal(adjust_value)

    for prtable in db_session.query(Prtable).filter(
             (Prtable.prcode == (parent_code).lower())).order_by(Prtable._recid).all():
        prbuff = Prtable()
        db_session.add(prbuff)

        buffer_copy(prtable, prbuff,except_fields=["prcode"])
        prbuff.prcode = child_code

        for product_list in query(product_list_list, filters=(lambda product_list: product_list.market == prbuff.marknr)):
            for curr_i in range(1,99 + 1) :

                if prbuff.product[curr_i - 1] == 0:
                    prbuff.product[curr_i - 1] = product_list.i_product


                    product_list_list.remove(product_list)
                    curr_i = 9999

    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, child_code)]})
    queasy.char3 = tb1_char3


    pass

    return generate_output()