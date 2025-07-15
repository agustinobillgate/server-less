#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_printcod1bl import read_printcod1bl
from models import Printcod

def printer_admin_get_emul_webbl():
    emulation_list_data = []
    emul:string = ""
    printcod = None

    emulation_list = t_printcod = None

    emulation_list_data, Emulation_list = create_model("Emulation_list", {"emul_code":string})
    t_printcod_data, T_printcod = create_model_like(Printcod)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal emulation_list_data, emul, printcod


        nonlocal emulation_list, t_printcod
        nonlocal emulation_list_data, t_printcod_data

        return {"emulation-list": emulation_list_data}

    t_printcod_data = get_output(read_printcod1bl(2, "", "", ""))

    for t_printcod in query(t_printcod_data, sort_by=[("emu",False)]):

        if emul != t_printcod.emu:
            emulation_list = Emulation_list()
            emulation_list_data.append(emulation_list)

            emulation_list.emul_code = t_printcod.emu


            emul = t_printcod.emu

    return generate_output()