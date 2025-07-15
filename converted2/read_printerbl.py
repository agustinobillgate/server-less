#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Printer

def read_printerbl(prno:int):
    t_printer_data = []
    printer = None

    t_printer = None

    t_printer_data, T_printer = create_model_like(Printer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_printer_data, printer
        nonlocal prno


        nonlocal t_printer
        nonlocal t_printer_data

        return {"t-printer": t_printer_data}

    printer = get_cache (Printer, {"nr": [(eq, prno)]})

    if printer:
        t_printer = T_printer()
        t_printer_data.append(t_printer)

        buffer_copy(printer, t_printer)

    return generate_output()