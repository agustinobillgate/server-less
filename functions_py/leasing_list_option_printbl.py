#using conversion tools version: 1.0.0.119
"""_yusufwijasena_05/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - convert only
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

tlist_data, Tlist = create_model(
"Tlist",
{
    "due_date":date,
    "show_tax":bool,
    "show_package":bool,
    "installment":int
})

def leasing_list_option_printbl(resnr:int, tlist_data:Tlist):

    prepare_cache ([Queasy])

    queasy = None
    tlist = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal resnr
        nonlocal tlist

        return {}

    queasy = get_cache (
        Queasy, {"key": [(eq, 346)],"number1": [(eq, resnr)]})

    if not queasy:
        queasy = Queasy()

        queasy.key = 346
        queasy.number1 = resnr

        db_session.add(queasy)

        tlist = query(tlist_data, first=True)

        if tlist:
            queasy.date1 = tlist.due_date
            queasy.logi1 = tlist.show_tax
            queasy.logi2 = tlist.show_package
            queasy.number2 = tlist.installment

    else:
        tlist = query(tlist_data, first=True)

        if tlist:
            queasy.date1 = tlist.due_date
            queasy.logi1 = tlist.show_tax
            queasy.logi2 = tlist.show_package

            if tlist.installment > 1:
                queasy.number2 = tlist.installment
    return generate_output()