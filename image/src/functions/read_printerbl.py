from functions.additional_functions import *
import decimal
from models import Printer

def read_printerbl(prno:int):
    t_printer_list = []
    printer = None

    t_printer = None

    t_printer_list, T_printer = create_model_like(Printer)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_printer_list, printer


        nonlocal t_printer
        nonlocal t_printer_list
        return {"t-printer": t_printer_list}

    printer = db_session.query(Printer).filter(
            (Printer.nr == prno)).first()

    if printer:
        t_printer = T_printer()
        t_printer_list.append(t_printer)

        buffer_copy(printer, t_printer)

    return generate_output()