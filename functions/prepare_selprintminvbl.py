#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Printer, Htparam, Brief

def prepare_selprintminvbl(printer_nr:int, briefnr:int):

    prepare_cache ([Printer, Htparam, Brief])

    n1 = 0
    rate = True
    usr_pr_defined = False
    found = False
    briefnr2 = 0
    flag = False
    b1_list_data = []
    s_list_data = []
    printer = htparam = brief = None

    user_printers = s_list = b1_list = None

    user_printers_data, User_printers = create_model("User_printers", {"nr":int, "selected":bool}, {"selected": True})
    s_list_data, S_list = create_model("S_list", {"ind":int, "nr":int, "bezeich":string}, {"ind": 1})
    b1_list_data, B1_list = create_model("B1_list", {"nr":int, "position":string, "path":string, "make":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal n1, rate, usr_pr_defined, found, briefnr2, flag, b1_list_data, s_list_data, printer, htparam, brief
        nonlocal printer_nr, briefnr


        nonlocal user_printers, s_list, b1_list
        nonlocal user_printers_data, s_list_data, b1_list_data

        return {"printer_nr": printer_nr, "briefnr": briefnr, "n1": n1, "rate": rate, "usr_pr_defined": usr_pr_defined, "found": found, "briefnr2": briefnr2, "flag": flag, "b1-list": b1_list_data, "s-list": s_list_data}

    def selected_printers():

        nonlocal n1, rate, usr_pr_defined, found, briefnr2, flag, b1_list_data, s_list_data, printer, htparam, brief
        nonlocal printer_nr, briefnr


        nonlocal user_printers, s_list, b1_list
        nonlocal user_printers_data, s_list_data, b1_list_data

        i:int = 0
        s1:string = ""
        s2:string = ""

        for printer in db_session.query(Printer).filter(
                 (Printer.bondrucker == False) & (Printer.opsysname == ("DOS").lower())).order_by(Printer._recid).all():
            user_printers = User_printers()
            user_printers_data.append(user_printers)

            user_printers.nr = printer.nr

    selected_printers()

    printer_obj_list = {}
    for printer in db_session.query(Printer).filter(
             (Printer.bondrucker == False) & (Printer.opsysname == ("DOS").lower())).order_by(Printer._recid).all():
        user_printers = query(user_printers_data, (lambda user_printers: user_printers.nr == printer.nr and user_printers.selected), first=True)
        if not user_printers:
            continue

        if printer_obj_list.get(printer._recid):
            continue
        else:
            printer_obj_list[printer._recid] = True


        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.nr = printer.nr
        b1_list.position = printer.position
        b1_list.path = printer.path
        b1_list.make = printer.make

    htparam = get_cache (Htparam, {"paramnr": [(eq, 137)]})
    rate = htparam.flogical

    if printer_nr != 0 and printer and not usr_pr_defined:

        if printer.nr == printer_nr:
            found = True
        else:
            found = False
            n1 = 0

            printer = get_cache (Printer, {"bondrucker": [(eq, False)],"opsysname": [(eq, "dos")]})
            while not found and printer:
                n1 = n1 + 1

                if printer.nr == printer_nr:
                    found = True
                else:

                    curr_recid = printer._recid
                    printer = db_session.query(Printer).filter(
                             (Printer.bondrucker == False) & (Printer.opsysname == ("DOS").lower()) & (Printer._recid > curr_recid)).first()
            flag = True

    brief = get_cache (Brief, {"briefnr": [(eq, briefnr)]})
    s_list = S_list()
    s_list_data.append(s_list)

    s_list.ind = 1
    s_list.nr = briefnr
    s_list.bezeich = brief.briefbezeich

    htparam = get_cache (Htparam, {"paramnr": [(eq, 415)]})
    briefnr2 = htparam.finteger

    if briefnr2 != 0:

        brief = get_cache (Brief, {"briefnr": [(eq, briefnr2)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.ind = 2
        s_list.nr = briefnr2
        s_list.bezeich = brief.briefbezeich

    if printer:
        printer_nr = printer.nr

    return generate_output()