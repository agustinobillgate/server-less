#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Printer

t_printer_data, T_printer = create_model_like(Printer)

def write_printer_webbl(case_type:int, emu:string, t_printer_data:[T_printer]):
    success_flag = False
    printer = None

    t_printer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, printer
        nonlocal case_type, emu


        nonlocal t_printer

        return {"success_flag": success_flag}

    t_printer = query(t_printer_data, first=True)

    if not t_printer:

        return generate_output()

    if case_type == 1:
        printer = Printer()
        db_session.add(printer)

        buffer_copy(t_printer, printer)
        pass
        success_flag = True
    elif case_type == 2:

        # printer = get_cache (Printer, {"nr": [(eq, t_printer.nr)]})
        printer = db_session.query(Printer).filter(
                 (Printer.nr == t_printer.nr)).with_for_update().first()    

        if printer:
            buffer_copy(t_printer, printer)
            pass
            success_flag = True

    return generate_output()