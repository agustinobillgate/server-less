from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Gc_pi, Gc_pitype, Printer

def prepare_print_gcpi1abl(docu_nr:str, user_init:str, printer_nr:int):
    output_list_list = []
    bediener = gc_pi = gc_pitype = printer = None

    output_list = ubuff = None

    output_list_list, Output_list = create_model("Output_list", {"docu_nr":str, "chequeno":str, "pay_datum":date, "username":str, "duedate":date, "bemerk":str, "betrag":decimal, "path":str})

    Ubuff = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, bediener, gc_pi, gc_pitype, printer
        nonlocal ubuff


        nonlocal output_list, ubuff
        nonlocal output_list_list
        return {"output-list": output_list_list}

    gc_pi = db_session.query(Gc_pi).filter(
            (func.lower(Gc_pi.(docu_nr).lower()) == (docu_nr).lower())).first()

    gc_pitype = db_session.query(Gc_pitype).filter(
            (Gc_pitype.nr == gc_pi.pi_type)).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    ubuff = db_session.query(Ubuff).filter(
            (Ubuff.userinit == gc_pi.rcvID)).first()

    printer = db_session.query(Printer).filter(
            (Printer.nr == printer_nr)).first()
    output_list = Output_list()
    output_list_list.append(output_list)

    output_list.docu_nr = gc_pi.docu_nr
    output_list.chequeNo = gc_pi.chequeNo
    output_list.pay_datum = gc_pi.pay_datum
    output_list.username = bediener.username
    output_list.dueDate = gc_pi.dueDate
    output_list.bemerk = gc_pi.bemerk
    output_list.betrag = gc_pi.betrag
    output_list.path = printer.path

    return generate_output()