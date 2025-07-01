#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

def prepare_mp_event_package_linebl(package_nr:int):
    t_bkqueasy_list = []

    t_bkqueasy = None

    t_bkqueasy_list, T_bkqueasy = create_model("T_bkqueasy", {"key":int, "number1":int, "number2":int, "number3":int, "date1":date, "date2":date, "date3":date, "char1":string, "char2":string, "char3":string, "deci1":Decimal, "deci2":Decimal, "deci3":Decimal, "logi1":bool, "logi2":bool, "logi3":bool, "betriebsnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bkqueasy_list
        nonlocal package_nr


        nonlocal t_bkqueasy
        nonlocal t_bkqueasy_list

        return {"t-bkqueasy": t_bkqueasy_list}

    for bk_queasy in query(bk_queasy_list, filters=(lambda bk_queasy: bk_queasy.key == 11 and bk_queasy.number2 == package_nr)):
        t_bkqueasy = T_bkqueasy()
        t_bkqueasy_list.append(t_bkqueasy)

        t_bkqueasy.key = bk_queasy.key
        t_bkqueasy.number1 = bk_queasy.number1
        t_bkqueasy.number2 = bk_queasy.number2
        t_bkqueasy.number3 = bk_queasy.number3
        t_bkqueasy.char1 = bk_queasy.char1
        t_bkqueasy.char2 = bk_queasy.char2
        t_bkqueasy.char3 = bk_queasy.char3
        t_bkqueasy.deci1 =  to_decimal(bk_queasy.deci1)
        t_bkqueasy.deci2 =  to_decimal(bk_queasy.deci2)
        t_bkqueasy.deci3 =  to_decimal(bk_queasy.deci3)

    return generate_output()