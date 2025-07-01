#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Printer

def delete_printerbl(case_type:int, int1:int):
    success_flag = False
    printer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, printer
        nonlocal case_type, int1

        return {"success_flag": success_flag}


    if case_type == 1:

        printer = get_cache (Printer, {"nr": [(eq, int1)]})

        if printer:
            db_session.delete(printer)
            pass
            success_flag = True

    return generate_output()