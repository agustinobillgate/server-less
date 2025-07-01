#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Prtable, Ratecode, Queasy, Waehrung

pr_list_list, Pr_list = create_model("Pr_list", {"cstr":[string,2], "prcode":string, "rmcat":string, "argt":string, "zikatnr":int, "argtnr":int, "i_typ":int, "flag":int})
prbuff_list, Prbuff = create_model_like(Pr_list)

def ratecode_adm_update_listbl(pvilanguage:int, select_mode:int, prcode:string, market_no:int, prbuff_list:[Prbuff], pr_list_list:[Pr_list]):

    prepare_cache ([Prtable, Ratecode, Queasy, Waehrung])

    pr_list_list = []
    msg_str = ""
    error_flag = True
    lvcarea:string = "ratecode-admin"
    chcode:string = ""
    prtable = ratecode = queasy = waehrung = None

    pr_list = prbuff = t_prtable = None

    t_prtable_list, T_prtable = create_model_like(Prtable)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pr_list_list, msg_str, error_flag, lvcarea, chcode, prtable, ratecode, queasy, waehrung
        nonlocal pvilanguage, select_mode, prcode, market_no


        nonlocal pr_list, prbuff, t_prtable
        nonlocal pr_list_list, t_prtable_list

        return {"msg_str": msg_str, "error_flag": error_flag}

    def check_deselect():

        nonlocal pr_list_list, msg_str, error_flag, lvcarea, chcode, prtable, ratecode, queasy, waehrung
        nonlocal pvilanguage, select_mode, prcode, market_no


        nonlocal pr_list, prbuff, t_prtable
        nonlocal pr_list_list, t_prtable_list

        if prbuff.flag == 0:
            msg_str = translateExtended ("Product was not selected", lvcarea, "")

            return

        ratecode = get_cache (Ratecode, {"argtnr": [(eq, prbuff.argtnr)],"zikatnr": [(eq, prbuff.zikatnr)],"code": [(eq, prbuff.prcode)],"marknr": [(eq, market_no)]})

        if ratecode:
            msg_str = translateExtended ("Rates exist with Code = ", lvcarea, "") + ratecode.code + ", deselecting not possible."

            return

        pr_list = query(pr_list_list, filters=(lambda pr_list: pr_list.zikatnr == prbuff.zikatnr and pr_list.argtnr == prbuff.argtnr), first=True)

        if pr_list:
            pr_list.flag = 0

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2) & not_ (Queasy.logi2) & (num_entries(Queasy.char3, ";") > 2) & (entry(1, Queasy.char3, ";") == (prcode).lower())).order_by(Queasy._recid).all():

            pr_list = query(pr_list_list, filters=(lambda pr_list: pr_list.zikatnr == prbuff.zikatnr and pr_list.argtnr == prbuff.argtnr), first=True)

            if pr_list:
                pr_list.flag = 0


        error_flag = False


    def check_select():

        nonlocal pr_list_list, msg_str, error_flag, lvcarea, chcode, prtable, ratecode, queasy, waehrung
        nonlocal pvilanguage, select_mode, prcode, market_no


        nonlocal pr_list, prbuff, t_prtable
        nonlocal pr_list_list, t_prtable_list

        if prbuff.flag == 1:
            msg_str = translateExtended ("Product has been selected", lvcarea, "")

            return

        pr_list = query(pr_list_list, filters=(lambda pr_list: pr_list.zikatnr == prbuff.zikatnr and pr_list.argtnr == prbuff.argtnr), first=True)

        if pr_list:
            pr_list.flag = 1

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2) & not_ (Queasy.logi2) & (num_entries(Queasy.char3, ";") > 2) & (entry(1, Queasy.char3, ";") == (prcode).lower())).order_by(Queasy._recid).all():

            pr_list = query(pr_list_list, filters=(lambda pr_list: pr_list.zikatnr == prbuff.zikatnr and pr_list.argtnr == prbuff.argtnr), first=True)
            pr_list.flag = 1


        error_flag = False


    def update_select_list():

        nonlocal pr_list_list, msg_str, error_flag, lvcarea, chcode, prtable, ratecode, queasy, waehrung
        nonlocal pvilanguage, select_mode, prcode, market_no


        nonlocal pr_list, prbuff, t_prtable
        nonlocal pr_list_list, t_prtable_list

        i:int = 0
        i_fact:int = 0
        prtable0 = None
        qbuff18 = None
        wbuff = None
        Prtable0 =  create_buffer("Prtable0",Prtable)
        Qbuff18 =  create_buffer("Qbuff18",Queasy)
        Wbuff =  create_buffer("Wbuff",Waehrung)

        prtable0 = get_cache (Prtable, {"marknr": [(eq, market_no)],"prcode": [(eq, "")]})

        if not prtable0:
            msg_str = translateExtended ("prtable record not available for market segment", lvcarea, "") + " " + to_string(market_no)
            error_flag = True

            return

        prtable = get_cache (Prtable, {"prcode": [(eq, prcode)],"marknr": [(eq, market_no)]})

        if not prtable:
            prtable = Prtable()
            db_session.add(prtable)

            prtable.prcode = prcode
            prtable.nr = market_no
            prtable.marknr = market_no


        for i in range(1,99 + 1) :
            prtable.product[i - 1] = 0
            prtable.zikatnr[i - 1] = prtable0.zikatnr[i - 1]
            prtable.argtnr[i - 1] = prtable0.argtnr[i - 1]


        i = 0

        for pr_list in query(pr_list_list, filters=(lambda pr_list: pr_list.flag == 1), sort_by=[("argtnr",False)]):
            i = i + 1
            i_fact = 0

            if pr_list.argtnr <= 999:

                if pr_list.zikatnr < 10:
                    i_fact = 90
                prtable.product[i - 1] = (i_fact + pr_list.zikatnr) * 1000 + pr_list.argtnr
            else:

                if pr_list.zikatnr < 10:
                    i_fact = 90
                prtable.product[i - 1] = (i_fact + pr_list.zikatnr) * 10000 + pr_list.argtnr
        pass
        pass

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2) & not_ (Queasy.logi2) & (num_entries(Queasy.char3, ";") > 2) & (entry(1, Queasy.char3, ";") == (prcode).lower())).order_by(Queasy._recid).all():

            prtable = get_cache (Prtable, {"prcode": [(eq, queasy.char1)],"marknr": [(eq, market_no)]})

            if not prtable:
                prtable = Prtable()
                db_session.add(prtable)

                prtable.prcode = queasy.char1
                prtable.nr = market_no
                prtable.marknr = market_no


            for i in range(1,99 + 1) :
                prtable.product[i - 1] = 0
                prtable.zikatnr[i - 1] = prtable0.zikatnr[i - 1]
                prtable.argtnr[i - 1] = prtable0.argtnr[i - 1]


            i = 0

            for pr_list in query(pr_list_list, filters=(lambda pr_list: pr_list.flag == 1), sort_by=[("argtnr",False)]):
                i = i + 1
                i_fact = 0

                if pr_list.zikatnr < 10:
                    i_fact = 90
                prtable.product[i - 1] = (i_fact + pr_list.zikatnr) * 1000 + pr_list.argtnr
            pass
            pass

        qbuff18 = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, prtable.nr)],"char3": [(ne, "")]})

        if qbuff18:

            wbuff = get_cache (Waehrung, {"wabkurz": [(eq, qbuff18.char3)]})

            if wbuff:

                queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, prcode)]})
                queasy.number1 = wbuff.waehrungsnr


                pass
                pass


    prbuff = query(prbuff_list, first=True)

    if select_mode == 0:
        check_deselect()
    else:
        check_select()

    if error_flag:

        return generate_output()
    update_select_list()

    return generate_output()