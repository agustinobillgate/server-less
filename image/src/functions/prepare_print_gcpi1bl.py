from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Gc_pi, Gc_pitype, Printer

def prepare_print_gcpi1bl(docu_nr:str, user_init:str, printer_nr:int):
    outstanding = 0
    path = ""
    output_list_list = []
    i:int = 0
    bediener = gc_pi = gc_pitype = printer = None

    output_list = ubuff = pibuff = None

    output_list_list, Output_list = create_model("Output_list", {"docu_nr":str, "bemerk":str, "betrag":decimal, "amount_array":[decimal], "bez_array":[str], "b_username":str, "u_username":str, "bezeich":str, "avail_gc_pitype":bool})

    Ubuff = Bediener
    Pibuff = Gc_pi

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outstanding, path, output_list_list, i, bediener, gc_pi, gc_pitype, printer
        nonlocal ubuff, pibuff


        nonlocal output_list, ubuff, pibuff
        nonlocal output_list_list
        return {"outstanding": outstanding, "path": path, "output-list": output_list_list}

    gc_pi = db_session.query(Gc_pi).filter(
            (func.lower(Gc_pi.(docu_nr).lower()) == (docu_nr).lower())).first()

    gc_pitype = db_session.query(Gc_pitype).filter(
            (Gc_pitype.nr == gc_pi.pi_type)).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    ubuff = db_session.query(Ubuff).filter(
            (Ubuff.userinit == gc_pi.rcvID)).first()

    for pibuff in db_session.query(Pibuff).filter(
            (Pibuff.rcvID == gc_pi.rcvID) &  (Pibuff.pi_status == 1)).all():
        outstanding = outstanding + pibuff.betrag
    output_list = Output_list()
    output_list_list.append(output_list)

    output_list.docu_nr = gc_pi.docu_nr
    output_list.bemerk = gc_pi.bemerk
    output_list.betrag = gc_pi.betrag
    output_list.b_username = bediener.username
    output_list.u_username = ubuff.username
    output_list.bezeich = gc_pitype.bezeich


    for i in range(1,10 + 1) :
        output_list.amount_array[i - 1] = gc_pi.amount_array[i - 1]
        output_list.bez_array[i - 1] = gc_pi.bez_array[i - 1]

    if gc_pitype:
        output_list.avail_gc_pitype = True
    else:
        output_list.avail_gc_pitype = False

    printer = db_session.query(Printer).filter(
            (Printer.nr == printer_nr)).first()
    path = printer.path

    return generate_output()