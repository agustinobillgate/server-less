#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Ratecode, Reslin_queasy, Queasy

pr_list_list, Pr_list = create_model("Pr_list", {"cstr":[string,2], "prcode":string, "rmcat":string, "argt":string, "zikatnr":int, "argtnr":int, "i_typ":int, "flag":int})

def ratecode_adm_copy_rate_1bl(pvilanguage:int, argtnr1:int, zikatnr1:int, market_nr:int, prcode:string, market:string, user_init:string, adj_value:Decimal, adj_type:string, pr_list_list:[Pr_list]):

    prepare_cache ([Reslin_queasy, Queasy])

    msg_str = ""
    lvcarea:string = "ratecode-admin"
    ratecode = reslin_queasy = queasy = None

    pr_list = child_list = None

    child_list_list, Child_list = create_model("Child_list", {"child_code":string, "true_child":bool, "in_percent":bool, "adjust_value":Decimal}, {"true_child": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, ratecode, reslin_queasy, queasy
        nonlocal pvilanguage, argtnr1, zikatnr1, market_nr, prcode, market, user_init, adj_value, adj_type


        nonlocal pr_list, child_list
        nonlocal child_list_list

        return {"msg_str": msg_str}

    def copy_rates():

        nonlocal msg_str, lvcarea, ratecode, reslin_queasy, queasy
        nonlocal pvilanguage, argtnr1, zikatnr1, market_nr, prcode, market, user_init, adj_value, adj_type


        nonlocal pr_list, child_list
        nonlocal child_list_list

        it_is:bool = False
        ratecode1 = None
        reslin_qsy = None
        child_code = None
        Ratecode1 =  create_buffer("Ratecode1",Ratecode)
        Reslin_qsy =  create_buffer("Reslin_qsy",Reslin_queasy)
        Child_code =  create_buffer("Child_code",Ratecode)

        pr_list = query(pr_list_list, first=True)
        create_child_list()

        for ratecode1 in db_session.query(Ratecode1).filter(
                 (Ratecode1.marknr == market_nr) & (Ratecode1.code == (prcode).lower()) & (Ratecode1.argtnr == argtnr1) & (Ratecode1.zikatnr == zikatnr1)).order_by(Ratecode1.startperiode).all():
            it_is = check_overlapping("copy-rate", ratecode1.startperiode, ratecode1.endperiode, ratecode1.wday, ratecode1.erwachs, ratecode1.kind1, ratecode1.kind2, prcode, market, pr_list.zikatnr, pr_list.argtnr)

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

                if adj_type.lower()  == ("In Amount").lower() :
                    ratecode.zipreis =  to_decimal(ratecode.zipreis) + to_decimal(adj_value)
                else:
                    ratecode.zipreis =  to_decimal(ratecode.zipreis) * to_decimal((1) + to_decimal(adj_value) * to_decimal(0.01))
            pass
            pass

            for child_list in query(child_list_list):

                child_code = db_session.query(Child_code).filter(
                         (Child_code.code == child_list.child_code) & (Child_code.startperiode == ratecode1.startperiode) & (Child_code.endperiode == ratecode1.endperiode) & (Child_code.erwachs == ratecode1.erwachs) & (Child_code.zikatnr == pr_list.zikatnr)).first()

                if child_code:
                    msg_str = translateExtended ("Child overlapping found: ", lvcarea, "") + to_string(ratecode1.startperiode) + " - " + to_string(ratecode1.endperiode)
                else:
                    child_code = Ratecode()
                    db_session.add(child_code)

                    buffer_copy(ratecode1, child_code,except_fields=["ratecode1.code","ratecode1.argtnr","ratecode1.zikatnr"])
                    child_code.code = child_list.child_code
                    child_code.argtnr = pr_list.argtnr
                    child_code.zikatnr = pr_list.zikatnr
                    child_code.char1[4] = user_init

                    if adj_value != 0:

                        if adj_type.lower()  == ("In Amount").lower() :

                            if child_list.in_percent:
                                child_code.zipreis = ( to_decimal(child_code.zipreis) + to_decimal(adj_value)) * to_decimal((1) + to_decimal(child_list.adjust_value) * to_decimal(0.01))
                            else:
                                child_code.zipreis = ( to_decimal(child_code.zipreis) + to_decimal(adj_value)) + to_decimal(child_list.adjust_value)
                        else:

                            if child_list.in_percent:
                                child_code.zipreis = ( to_decimal(child_code.zipreis) * to_decimal((1) + to_decimal(adj_value) * to_decimal(0.01))) * to_decimal((1) + to_decimal(child_list.adjust_value) * to_decimal(0.01))
                            else:
                                child_code.zipreis = ( to_decimal(child_code.zipreis) * to_decimal((1) + to_decimal(adj_value) * to_decimal(0.01))) + to_decimal(child_list.adjust_value)
                    pass
                    pass

        if argtnr1 != pr_list.argtnr:
            msg_str = "&W" + translateExtended ("Nocopy of argt-lines for different arrangement", lvcarea, "")
        else:

            for reslin_qsy in db_session.query(Reslin_qsy).filter(
                     (Reslin_qsy.key == ("argt-line").lower()) & (Reslin_qsy.number1 == market_nr) & (Reslin_qsy.number2 == argtnr1) & (Reslin_qsy.char1 == (prcode).lower()) & (Reslin_qsy.reslinnr == zikatnr1)).order_by(Reslin_qsy.resnr, Reslin_qsy.number3, Reslin_qsy.date1).all():
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "argt-line"
                reslin_queasy.char1 = prcode
                reslin_queasy.number1 = market_nr
                reslin_queasy.number2 = pr_list.argtnr
                reslin_queasy.number3 = reslin_qsy.number3
                reslin_queasy.resnr = reslin_qsy.resnr
                reslin_queasy.reslinnr = pr_list.zikatnr
                reslin_queasy.deci1 =  to_decimal(reslin_qsy.deci1)
                reslin_queasy.date1 = reslin_qsy.date1
                reslin_queasy.date2 = reslin_qsy.date2


                pass

    def check_overlapping(curr_mode:string, f_date:date, t_date:date, w_day:int, adult:int, child1:int, child2:int, prcode:string, market:string, zikatnr:int, argtnr:int):

        nonlocal msg_str, lvcarea, ratecode, reslin_queasy, queasy
        nonlocal pvilanguage, argtnr1, zikatnr1, market_nr, user_init, adj_value, adj_type


        nonlocal pr_list, child_list
        nonlocal child_list_list

        it_is = False
        found:bool = False
        ratecode1 = None

        def generate_inner_output():
            return (it_is)

        Ratecode1 =  create_buffer("Ratecode1",Ratecode)

        if curr_mode.lower()  == ("add-rate").lower()  or curr_mode.lower()  == ("copy-rate").lower() :

            ratecode1 = db_session.query(Ratecode1).filter(
                     (Ratecode1.marknr == market_nr) & (Ratecode1.code == (prcode).lower()) & (Ratecode1.argtnr == argtnr) & (Ratecode1.zikatnr == zikatnr) & (Ratecode1.erwachs == adult) & (Ratecode1.kind1 == child1) & (Ratecode1.kind2 == child2) & (Ratecode1.wday == w_day) & not_ (Ratecode1.startperiod >= t_date) & not_ (Ratecode1.endperiod <= f_date)).first()

        elif curr_mode.lower()  == ("chg-rate").lower() :

            ratecode1 = db_session.query(Ratecode1).filter(
                     (Ratecode1.marknr == prmarket.nr) & (Ratecode1.code == (prcode).lower()) & (Ratecode1.argtnr == argtnr) & (Ratecode1.zikatnr == zikatnr) & (Ratecode1._recid != ratecode._recid) & (Ratecode1.erwachs == adult) & (Ratecode1.kind1 == child1) & (Ratecode1.kind2 == child2) & (Ratecode1.wday == w_day) & not_ (Ratecode1.startperiod >= t_date) & not_ (Ratecode1.endperiod <= f_date)).first()
        it_is = None != ratecode1

        return generate_inner_output()


    def create_child_list():

        nonlocal msg_str, lvcarea, ratecode, reslin_queasy, queasy
        nonlocal pvilanguage, argtnr1, zikatnr1, market_nr, prcode, market, user_init, adj_value, adj_type


        nonlocal pr_list, child_list
        nonlocal child_list_list

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2) & not_ (Queasy.logi2) & (num_entries(Queasy.char3, ";") > 2) & (entry(1, Queasy.char3, ";") == (prcode).lower())).order_by(Queasy._recid).all():
            child_list = Child_list()
            child_list_list.append(child_list)

            child_list.child_code = queasy.char1
            child_list.in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
            child_list.adjust_value = to_decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100


    copy_rates()

    return generate_output()