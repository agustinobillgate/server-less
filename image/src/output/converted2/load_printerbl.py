#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Printer

def load_printerbl(case_type:int, druckmode:bool, osname:string):
    t_printer_list = []
    printer = None

    t_printer = None

    t_printer_list, T_printer = create_model_like(Printer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_printer_list, printer
        nonlocal case_type, druckmode, osname


        nonlocal t_printer
        nonlocal t_printer_list

        return {"t-printer": t_printer_list}

    if case_type == 1:

        for printer in db_session.query(Printer).filter(
                 (Printer.bondrucker == druckmode) & (Printer.opsysname == osname)).order_by(Printer._recid).all():
            t_printer = T_printer()
            t_printer_list.append(t_printer)

            buffer_copy(printer, t_printer)

    elif case_type == 2:

        printer = get_cache (Printer, {"bondrucker": [(eq, druckmode)],"opsysname": [(eq, osname)]})

        if printer:
            t_printer = T_printer()
            t_printer_list.append(t_printer)

            buffer_copy(printer, t_printer)
    elif case_type == 3:

        for printer in db_session.query(Printer).order_by(Printer._recid).all():
            t_printer = T_printer()
            t_printer_list.append(t_printer)

            buffer_copy(printer, t_printer)

    return generate_output()