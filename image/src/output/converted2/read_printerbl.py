#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Printer

def read_printerbl(prno:int):
    t_printer_list = []
    printer = None

    t_printer = None

    t_printer_list, T_printer = create_model_like(Printer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_printer_list, printer
        nonlocal prno


        nonlocal t_printer
        nonlocal t_printer_list

        return {"t-printer": t_printer_list}

    printer = get_cache (Printer, {"nr": [(eq, prno)]})

    if printer:
        t_printer = T_printer()
        t_printer_list.append(t_printer)

        buffer_copy(printer, t_printer)

    return generate_output()