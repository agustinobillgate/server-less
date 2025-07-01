#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Printcod

def printer_admin_get_emul_web1bl():

    prepare_cache ([Printcod])

    emulation_list_list = []
    emul:string = ""
    printcod = None

    emulation_list = t_printcod = None

    emulation_list_list, Emulation_list = create_model("Emulation_list", {"emul_code":string, "rec_id":int})
    t_printcod_list, T_printcod = create_model_like(Printcod)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal emulation_list_list, emul, printcod


        nonlocal emulation_list, t_printcod
        nonlocal emulation_list_list, t_printcod_list

        return {"emulation-list": emulation_list_list}


    for printcod in db_session.query(Printcod).order_by(Printcod.emu).all():

        if emul != printcod.emu:
            emulation_list = Emulation_list()
            emulation_list_list.append(emulation_list)

            emulation_list.emul_code = printcod.emu
            emulation_list.rec_id = printcod._recid
            emul = printcod.emu

    return generate_output()