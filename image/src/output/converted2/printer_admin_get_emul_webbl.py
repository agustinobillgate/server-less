#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.read_printcod1bl import read_printcod1bl
from models import Printcod

def printer_admin_get_emul_webbl():
    emulation_list_list = []
    emul:string = ""
    printcod = None

    emulation_list = t_printcod = None

    emulation_list_list, Emulation_list = create_model("Emulation_list", {"emul_code":string})
    t_printcod_list, T_printcod = create_model_like(Printcod)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal emulation_list_list, emul, printcod


        nonlocal emulation_list, t_printcod
        nonlocal emulation_list_list, t_printcod_list

        return {"emulation-list": emulation_list_list}

    t_printcod_list = get_output(read_printcod1bl(2, "", "", ""))

    for t_printcod in query(t_printcod_list, sort_by=[("emu",False)]):

        if emul != t_printcod.emu:
            emulation_list = Emulation_list()
            emulation_list_list.append(emulation_list)

            emulation_list.emul_code = t_printcod.emu


            emul = t_printcod.emu

    return generate_output()