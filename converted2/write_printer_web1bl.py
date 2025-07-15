#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Printer, Printcod

t_printer_data, T_printer = create_model("T_printer", {"nr":int, "path":string, "copies":int, "make":string, "emu":string, "position":string, "pglen":int, "spooled":bool, "bondrucker":bool, "opsysname":string})

def write_printer_web1bl(case_type:int, recid_emu:int, t_printer_data:[T_printer]):

    prepare_cache ([Printer, Printcod])

    success_flag = False
    printer = printcod = None

    t_printer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, printer, printcod
        nonlocal case_type, recid_emu


        nonlocal t_printer

        return {"success_flag": success_flag}

    t_printer = query(t_printer_data, first=True)

    if not t_printer:

        return generate_output()

    if case_type == 1:
        printer = Printer()
        db_session.add(printer)

        buffer_copy(t_printer, printer)

        printcod = get_cache (Printcod, {"_recid": [(eq, recid_emu)]})

        if printcod:
            printer.emu = printcod.emu
        pass
        success_flag = True
    elif case_type == 2:

        printer = get_cache (Printer, {"nr": [(eq, t_printer.nr)]})

        if printer:
            buffer_copy(t_printer, printer,except_fields=["emu"])

            printcod = get_cache (Printcod, {"_recid": [(eq, recid_emu)]})

            if printcod:
                printer.emu = printcod.emu
            pass
            success_flag = True

    return generate_output()