from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Prtable, Ratecode, Queasy, Waehrung

def ratecode_adm_update_listbl(pvilanguage:int, select_mode:int, prcode:str, market_no:int, prbuff:[Prbuff], pr_list:[Pr_list]):
    msg_str = ""
    error_flag = False
    lvcarea:str = "ratecode_admin"
    chcode:str = ""
    prtable = ratecode = queasy = waehrung = None

    pr_list = prbuff = t_prtable = prtable0 = qbuff18 = wbuff = None

    pr_list_list, Pr_list = create_model("Pr_list", {"cstr":str, "prcode":str, "rmcat":str, "argt":str, "zikatnr":int, "argtnr":int, "i_typ":int, "flag":int})
    prbuff_list, Prbuff = create_model_like(Pr_list)
    t_prtable_list, T_prtable = create_model_like(Prtable)

    Prtable0 = Prtable
    Qbuff18 = Queasy
    Wbuff = Waehrung

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, lvcarea, chcode, prtable, ratecode, queasy, waehrung
        nonlocal prtable0, qbuff18, wbuff


        nonlocal pr_list, prbuff, t_prtable, prtable0, qbuff18, wbuff
        nonlocal pr_list_list, prbuff_list, t_prtable_list
        return {"msg_str": msg_str, "error_flag": error_flag}

    def check_deselect():

        nonlocal msg_str, error_flag, lvcarea, chcode, prtable, ratecode, queasy, waehrung
        nonlocal prtable0, qbuff18, wbuff


        nonlocal pr_list, prbuff, t_prtable, prtable0, qbuff18, wbuff
        nonlocal pr_list_list, prbuff_list, t_prtable_list

        if prbuff.flag == 0:
            msg_str = translateExtended ("Product was not selected", lvcarea, "")

            return

        ratecode = db_session.query(Ratecode).filter(
                (Ratecode.argtnr == prbuff.argtnr) &  (Ratecode.zikatnr == prbuff.zikatnr) &  (Ratecode.code == prbuff.prcode) &  (Ratecode.marknr == market_no)).first()

        if ratecode:
            msg_str = translateExtended ("Rates exist with Code  ==  ", lvcarea, "") + ratecode.code + ", deselecting not possible."

            return

        pr_list = query(pr_list_list, filters=(lambda pr_list :pr_list.zikatnr == prbuff.zikatnr and pr_list.argtnr == prbuff.argtnr), first=True)
        pr_list.flag = 0

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (not Queasy.logi2) &  (num_entries(Queasy.char3, ";") > 2) &  (entry(1, Queasy.char3, ";") == (prcode).lower())).all():

            pr_list = query(pr_list_list, filters=(lambda pr_list :pr_list.zikatnr == prbuff.zikatnr and pr_list.argtnr == prbuff.argtnr), first=True)
            pr_list.flag = 0


        error_flag = False

    def check_select():

        nonlocal msg_str, error_flag, lvcarea, chcode, prtable, ratecode, queasy, waehrung
        nonlocal prtable0, qbuff18, wbuff


        nonlocal pr_list, prbuff, t_prtable, prtable0, qbuff18, wbuff
        nonlocal pr_list_list, prbuff_list, t_prtable_list

        if prbuff.flag == 1:
            msg_str = translateExtended ("Product has been selected", lvcarea, "")

            return

        pr_list = query(pr_list_list, filters=(lambda pr_list :pr_list.zikatnr == prbuff.zikatnr and pr_list.argtnr == prbuff.argtnr), first=True)
        pr_list.flag = 1

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (not Queasy.logi2) &  (num_entries(Queasy.char3, ";") > 2) &  (entry(1, Queasy.char3, ";") == (prcode).lower())).all():

            pr_list = query(pr_list_list, filters=(lambda pr_list :pr_list.zikatnr == prbuff.zikatnr and pr_list.argtnr == prbuff.argtnr), first=True)
            pr_list.flag = 1


        error_flag = False

    def update_select_list():

        nonlocal msg_str, error_flag, lvcarea, chcode, prtable, ratecode, queasy, waehrung
        nonlocal prtable0, qbuff18, wbuff


        nonlocal pr_list, prbuff, t_prtable, prtable0, qbuff18, wbuff
        nonlocal pr_list_list, prbuff_list, t_prtable_list

        i:int = 0
        i_fact:int = 0
        Prtable0 = Prtable
        Qbuff18 = Queasy
        Wbuff = Waehrung

        prtable0 = db_session.query(Prtable0).filter(
                (Prtable0.marknr == market_no) &  (Prtable0.prcode == "")).first()

        if not prtable0:
            msg_str = translateExtended ("prtable record not available for market segment", lvcarea, "") + " " + to_string(market_no)
            error_flag = True

            return

        prtable = db_session.query(Prtable).filter(
                (func.lower(Prtable.(prcode).lower()) == (prcode).lower()) &  (Prtable.marknr == market_no)).first()

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

        for pr_list in query(pr_list_list, filters=(lambda pr_list :pr_list.flag == 1)):
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

        prtable = db_session.query(Prtable).first()

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (not Queasy.logi2) &  (num_entries(Queasy.char3, ";") > 2) &  (entry(1, Queasy.char3, ";") == (prcode).lower())).all():

            prtable = db_session.query(Prtable).filter(
                    (Prtable.prcode == queasy.char1) &  (Prtable.marknr == market_no)).first()

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

            for pr_list in query(pr_list_list, filters=(lambda pr_list :pr_list.flag == 1)):
                i = i + 1
                i_fact = 0

                if pr_list.zikatnr < 10:
                    i_fact = 90
                prtable.product[i - 1] = (i_fact + pr_list.zikatnr) * 1000 + pr_list.argtnr

            prtable = db_session.query(Prtable).first()

        qbuff18 = db_session.query(Qbuff18).filter(
                (Qbuff18.key == 18) &  (Qbuff18.number1 == prtable.nr) &  (Qbuff18.char3 != "")).first()

        if qbuff18:

            wbuff = db_session.query(Wbuff).filter(
                    (Wbuff.wabkurz == qbuff18.char3)).first()

            if wbuff:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 2) &  (func.lower(Queasy.char1) == (prcode).lower())).first()
                queasy.number1 = wbuff.waehrungsnr

                queasy = db_session.query(Queasy).first()

    prbuff = query(prbuff_list, first=True)

    if select_mode == 0:
        check_deselect()
    else:
        check_select()

    if error_flag:

        return generate_output()
    update_select_list()

    return generate_output()