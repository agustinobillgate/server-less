#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Gc_pi, Gc_pitype, Printer

def prepare_print_gcpi1bl(docu_nr:string, user_init:string, printer_nr:int):

    prepare_cache ([Bediener, Gc_pi, Gc_pitype, Printer])

    outstanding = to_decimal("0.0")
    path = ""
    output_list_data = []
    i:int = 0
    bediener = gc_pi = gc_pitype = printer = None

    output_list = ubuff = pibuff = None

    output_list_data, Output_list = create_model("Output_list", {"docu_nr":string, "bemerk":string, "betrag":Decimal, "amount_array":[Decimal,10], "bez_array":[string,10], "b_username":string, "u_username":string, "bezeich":string, "avail_gc_pitype":bool})

    Ubuff = create_buffer("Ubuff",Bediener)
    Pibuff = create_buffer("Pibuff",Gc_pi)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal outstanding, path, output_list_data, i, bediener, gc_pi, gc_pitype, printer
        nonlocal docu_nr, user_init, printer_nr
        nonlocal ubuff, pibuff


        nonlocal output_list, ubuff, pibuff
        nonlocal output_list_data

        return {"outstanding": outstanding, "path": path, "output-list": output_list_data}

    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})

    gc_pitype = get_cache (Gc_pitype, {"nr": [(eq, gc_pi.pi_type)]})

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    ubuff = get_cache (Bediener, {"userinit": [(eq, gc_pi.rcvid)]})

    for pibuff in db_session.query(Pibuff).filter(
             (Pibuff.rcvID == gc_pi.rcvid) & (Pibuff.pi_status == 1)).order_by(Pibuff._recid).all():
        outstanding =  to_decimal(outstanding) + to_decimal(pibuff.betrag)
    output_list = Output_list()
    output_list_data.append(output_list)

    output_list.docu_nr = gc_pi.docu_nr
    output_list.bemerk = gc_pi.bemerk
    output_list.betrag =  to_decimal(gc_pi.betrag)
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

    printer = get_cache (Printer, {"nr": [(eq, printer_nr)]})
    path = printer.path

    return generate_output()