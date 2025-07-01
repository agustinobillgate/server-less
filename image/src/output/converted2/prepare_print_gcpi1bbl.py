#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Gc_pi, Gc_pitype, Printer

def prepare_print_gcpi1bbl(docu_nr:string, user_init:string, printer_nr:int):

    prepare_cache ([Bediener, Gc_pi, Printer])

    output_list_list = []
    i:int = 0
    bediener = gc_pi = gc_pitype = printer = None

    output_list = ubuff = None

    output_list_list, Output_list = create_model("Output_list", {"docu_nr":string, "chequeno":string, "pay_datum":date, "username":string, "duedate":date, "bemerk":string, "betrag":Decimal, "path":string, "amount_array":[Decimal,10], "bez_array":[string,10], "amtreturn":Decimal, "grand_tot":Decimal})

    Ubuff = create_buffer("Ubuff",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, i, bediener, gc_pi, gc_pitype, printer
        nonlocal docu_nr, user_init, printer_nr
        nonlocal ubuff


        nonlocal output_list, ubuff
        nonlocal output_list_list

        return {"output-list": output_list_list}

    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})

    gc_pitype = get_cache (Gc_pitype, {"nr": [(eq, gc_pi.pi_type)]})

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    ubuff = get_cache (Bediener, {"userinit": [(eq, gc_pi.rcvid)]})

    printer = get_cache (Printer, {"nr": [(eq, printer_nr)]})
    output_list = Output_list()
    output_list_list.append(output_list)

    output_list.docu_nr = gc_pi.docu_nr
    output_list.chequeno = gc_pi.chequeno
    output_list.pay_datum = gc_pi.pay_datum
    output_list.username = bediener.username
    output_list.duedate = gc_pi.dueDate
    output_list.bemerk = gc_pi.bemerk
    output_list.betrag =  to_decimal(gc_pi.betrag)
    output_list.path = printer.path
    output_list.amtreturn =  to_decimal(gc_pi.returnamt)
    output_list.grand_tot =  to_decimal(gc_pi.betrag) - to_decimal(gc_pi.returnamt)


    for i in range(1,10 + 1) :
        output_list.amount_array[i - 1] = gc_pi.amount_array[i - 1]
        output_list.bez_array[i - 1] = gc_pi.bez_array[i - 1]

    return generate_output()