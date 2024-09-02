from functions.additional_functions import *
import decimal
from sqlalchemy import func
from datetime import date
from models import Ratecode, Reslin_queasy, Queasy

def ratecode_adm_copy_rate_1bl(pvilanguage:int, argtnr1:int, zikatnr1:int, market_nr:int, prcode:str, market:str, user_init:str, adj_value:decimal, adj_type:str, pr_list:[Pr_list]):
    msg_str = ""
    lvcarea:str = "ratecode_admin"
    ratecode = reslin_queasy = queasy = None

    pr_list = child_list = ratecode1 = reslin_qsy = child_code = None

    pr_list_list, Pr_list = create_model("Pr_list", {"cstr":str, "prcode":str, "rmcat":str, "argt":str, "zikatnr":int, "argtnr":int, "i_typ":int, "flag":int})
    child_list_list, Child_list = create_model("Child_list", {"child_code":str, "true_child":bool, "in_percent":bool, "adjust_value":decimal}, {"true_child": True})

    Ratecode1 = Ratecode
    Reslin_qsy = Reslin_queasy
    Child_code = Ratecode

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, ratecode, reslin_queasy, queasy
        nonlocal ratecode1, reslin_qsy, child_code


        nonlocal pr_list, child_list, ratecode1, reslin_qsy, child_code
        nonlocal pr_list_list, child_list_list
        return {"msg_str": msg_str}

    def copy_rates():

        nonlocal msg_str, lvcarea, ratecode, reslin_queasy, queasy
        nonlocal ratecode1, reslin_qsy, child_code


        nonlocal pr_list, child_list, ratecode1, reslin_qsy, child_code
        nonlocal pr_list_list, child_list_list

        it_is:bool = False
        Ratecode1 = Ratecode
        Reslin_qsy = Reslin_queasy
        Child_code = Ratecode

        pr_list = query(pr_list_list, first=True)
        create_child_list()

        for ratecode1 in db_session.query(Ratecode1).filter(
                (Ratecode1.marknr == market_nr) &  (func.lower(Ratecode1.code) == (prcode).lower()) &  (Ratecode1.argtnr == argtnr1) &  (Ratecode1.zikatnr == zikatnr1)).all():
            it_is = check_overlapping("copy_rate", ratecode1.startperiode, ratecode1.endperiode, ratecode1.wday, ratecode1.erwachs, ratecode1.kind1, ratecode1.kind2, prcode, market, pr_list.zikatnr, pr_list.argtnr)

            if it_is:
                msg_str = translateExtended ("Overlapping found: ", lvcarea, "") + to_string(ratecode1.startperiode) + " - " + to_string(ratecode1.endperiode)

                return
            ratecode = Ratecode()
            db_session.add(ratecode)

            buffer_copy(ratecode1, ratecode,except_fields=["ratecode1.argtnr","ratecode1.zikatnr"])
            ratecode.argtnr = pr_list.argtnr
            ratecode.zikatnr = pr_list.zikatnr
            ratecode.char1[4] = user_init

            if adj_value != 0:

                if adj_type.lower()  == "In Amount":
                    ratecode.zipreis = ratecode.zipreis + adj_value
                else:
                    ratecode.zipreis = ratecode.zipreis * (1 + adj_value * 0.01)

            ratecode = db_session.query(Ratecode).first()

            for child_list in query(child_list_list):

                child_code = db_session.query(Child_code).filter(
                        (Child_code.CODE == child_list.child_code) &  (Child_code.startperiode == ratecode1.startperiode) &  (Child_code.endperiode == ratecode1.endperiode) &  (Child_code.erwachs == ratecode1.erwachs) &  (Child_code.zikatnr == pr_list.zikatnr)).first()

                if child_code:
                    msg_str = translateExtended ("Child overlapping found: ", lvcarea, "") + to_string(ratecode1.startperiode) + " - " + to_string(ratecode1.endperiode)
                else:
                    child_code = Child_code()
                    db_session.add(child_code)

                    buffer_copy(ratecode1, child_code,except_fields=["ratecode1.CODE","ratecode1.argtnr","ratecode1.zikatnr"])
                    child_code.CODE = child_list.child_code
                    child_code.argtnr = pr_list.argtnr
                    child_code.zikatnr = pr_list.zikatnr
                    child_code.char1[4] = user_init

                    if adj_value != 0:

                        if adj_type.lower()  == "In Amount":

                            if child_list.in_percent:
                                child_code.zipreis = (child_code.zipreis + adj_value) * (1 + child_list.adjust_value * 0.01)
                            else:
                                child_code.zipreis = (child_code.zipreis + adj_value) + child_list.adjust_value
                        else:

                            if child_list.in_percent:
                                child_code.zipreis = (child_code.zipreis * (1 + adj_value * 0.01)) * (1 + child_list.adjust_value * 0.01)
                            else:
                                child_code.zipreis = (child_code.zipreis * (1 + adj_value * 0.01)) + child_list.adjust_value

                    child_code = db_session.query(Child_code).first()


        if argtnr1 != pr_list.argtnr:
            msg_str = "&W" + translateExtended ("Nocopy of argt_lines for different arrangement", lvcarea, "")
        else:

            for reslin_qsy in db_session.query(Reslin_qsy).filter(
                    (func.lower(Reslin_qsy.key) == "argt_line") &  (Reslin_qsy.number1 == market_nr) &  (Reslin_qsy.number2 == argtnr1) &  (func.lower(Reslin_qsy.char1) == (prcode).lower()) &  (Reslin_qsy.reslinnr == zikatnr1)).all():
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "argt_line"
                reslin_queasy.char1 = prcode
                reslin_queasy.number1 = market_nr
                reslin_queasy.number2 = pr_list.argtnr
                reslin_queasy.number3 = reslin_qsy.number3
                reslin_queasy.resnr = reslin_qsy.resnr
                reslin_queasy.reslinnr = pr_list.zikatnr
                reslin_queasy.deci1 = reslin_qsy.deci1
                reslin_queasy.date1 = reslin_qsy.date1
                reslin_queasy.date2 = reslin_qsy.date2

                reslin_queasy = db_session.query(Reslin_queasy).first()


    def check_overlapping(curr_mode:str, f_date:date, t_date:date, w_day:int, adult:int, child1:int, child2:int, prcode:str, market:str, zikatnr:int, argtnr:int):

        nonlocal msg_str, lvcarea, ratecode, reslin_queasy, queasy
        nonlocal ratecode1, reslin_qsy, child_code


        nonlocal pr_list, child_list, ratecode1, reslin_qsy, child_code
        nonlocal pr_list_list, child_list_list

        it_is = False
        found:bool = False

        def generate_inner_output():
            return it_is
        Ratecode1 = Ratecode

        if curr_mode.lower()  == "add_rate" or curr_mode.lower()  == "copy_rate":

            ratecode1 = db_session.query(Ratecode1).filter(
                    (Ratecode1.marknr == market_nr) &  (func.lower(Ratecode1.code) == (prcode).lower()) &  (Ratecode1.argtnr == argtnr) &  (Ratecode1.zikatnr == zikatnr) &  (Ratecode1.erwachs == adult) &  (Ratecode1.kind1 == child1) &  (Ratecode1.kind2 == child2) &  (Ratecode1.wday == w_day) &  (not Ratecode1.startperiod >= t_date) &  (not Ratecode1.endperiod <= f_date)).first()

        elif curr_mode.lower()  == "chg_rate":

            ratecode1 = db_session.query(Ratecode1).filter(
                    (Ratecode1.marknr == prmarket.nr) &  (func.lower(Ratecode1.code) == (prcode).lower()) &  (Ratecode1.argtnr == argtnr) &  (Ratecode1.zikatnr == zikatnr) &  (Ratecode1._recid != ratecode._recid) &  (Ratecode1.erwachs == adult) &  (Ratecode1.kind1 == child1) &  (Ratecode1.kind2 == child2) &  (Ratecode1.wday == w_day) &  (not Ratecode1.startperiod >= t_date) &  (not Ratecode1.endperiod <= f_date)).first()
        it_is = None != ratecode1


        return generate_inner_output()

    def create_child_list():

        nonlocal msg_str, lvcarea, ratecode, reslin_queasy, queasy
        nonlocal ratecode1, reslin_qsy, child_code


        nonlocal pr_list, child_list, ratecode1, reslin_qsy, child_code
        nonlocal pr_list_list, child_list_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (not Queasy.logi2) &  (num_entries(Queasy.char3, ";") > 2) &  (entry(1, Queasy.char3, ";") == (prcode).lower())).all():
            child_list = Child_list()
            child_list_list.append(child_list)

            child_list.child_code = queasy.char1
            child_list.in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
            child_list.adjust_value = decimal.Decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100

    copy_rates()

    return generate_output()