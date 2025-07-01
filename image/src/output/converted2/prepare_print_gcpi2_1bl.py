#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Gc_pibline, Gc_pi, Gc_pitype, Printer

def prepare_print_gcpi2_1bl(docu_nr:string, user_init:string, printer_nr:int):

    prepare_cache ([Bediener, Gc_pi, Gc_pitype, Printer])

    output_list_list = []
    t_gc_pibline_list = []
    bediener = gc_pibline = gc_pi = gc_pitype = printer = None

    ubuff = output_list = t_gc_pibline = None

    output_list_list, Output_list = create_model("Output_list", {"docu_nr":string, "u_username":string, "b_username":string, "bezeich":string, "bemerk":string, "betrag":Decimal, "path":string, "avail_gc_pitype":bool})
    t_gc_pibline_list, T_gc_pibline = create_model_like(Gc_pibline, {"rec_id":int})

    Ubuff = create_buffer("Ubuff",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, t_gc_pibline_list, bediener, gc_pibline, gc_pi, gc_pitype, printer
        nonlocal docu_nr, user_init, printer_nr
        nonlocal ubuff


        nonlocal ubuff, output_list, t_gc_pibline
        nonlocal output_list_list, t_gc_pibline_list

        return {"output-list": output_list_list, "t-gc-PIbline": t_gc_pibline_list}


    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})

    gc_pitype = get_cache (Gc_pitype, {"nr": [(eq, gc_pi.pi_type)]})

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    ubuff = get_cache (Bediener, {"userinit": [(eq, gc_pi.rcvid)]})

    printer = get_cache (Printer, {"nr": [(eq, printer_nr)]})
    output_list = Output_list()
    output_list_list.append(output_list)


    if gc_pitype:
        output_list.avail_gc_pitype = True
        output_list.bezeich = gc_pitype.bezeich


    output_list.docu_nr = gc_pi.docu_nr
    output_list.u_username = ubuff.username
    output_list.b_username = bediener.username
    output_list.bemerk = gc_pi.bemerk
    output_list.betrag =  to_decimal(gc_pi.betrag)
    output_list.path = printer.path

    for gc_pibline in db_session.query(Gc_pibline).filter(
             (gc_pibline.docu_nr == gc_pi.docu_nr)).order_by(Gc_pibline.created, Gc_pibline.zeit).all():
        t_gc_pibline = T_gc_pibline()
        t_gc_pibline_list.append(t_gc_pibline)

        buffer_copy(gc_pibline, t_gc_pibline)

    return generate_output()