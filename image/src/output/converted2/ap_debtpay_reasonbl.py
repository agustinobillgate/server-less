#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, Queasy

def ap_debtpay_reasonbl(curr_mode:string, docu_nr:string, bill_date:date, comments:string):

    prepare_cache ([L_kredit, Queasy])

    l_kredit = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_kredit, queasy
        nonlocal curr_mode, docu_nr, bill_date, comments

        return {"comments": comments}

    def create_queasy():

        nonlocal l_kredit, queasy
        nonlocal curr_mode, docu_nr, bill_date, comments

        l_kredit = get_cache (L_kredit, {"rgdatum": [(eq, bill_date)],"opart": [(lt, 2)],"counter": [(ge, 0)],"name": [(eq, docu_nr)]})

        queasy = get_cache (Queasy, {"key": [(eq, 263)],"char1": [(eq, l_kredit.name)]})

        if queasy:
            queasy.char2 = comments


        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 263
            queasy.char1 = l_kredit.name
            queasy.char2 = comments


    def load_queasy():

        nonlocal l_kredit, queasy
        nonlocal curr_mode, docu_nr, bill_date, comments

        l_kredit = get_cache (L_kredit, {"rgdatum": [(eq, bill_date)],"opart": [(lt, 2)],"counter": [(ge, 0)],"name": [(eq, docu_nr)]})

        queasy = get_cache (Queasy, {"key": [(eq, 263)],"char1": [(eq, l_kredit.name)]})

        if queasy:
            comments = queasy.char2


        else:
            comments = " "

    if curr_mode.lower()  == ("save").lower() :
        create_queasy()
    else:
        load_queasy()

    return generate_output()