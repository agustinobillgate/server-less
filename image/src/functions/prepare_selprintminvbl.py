from functions.additional_functions import *
import decimal
from sqlalchemy import func
import re
from models import Printer, Htparam, Brief

def prepare_selprintminvbl(printer_nr:int, briefnr:int):
    n1 = 0
    rate = False
    usr_pr_defined = False
    found = False
    briefnr2 = 0
    flag = False
    b1_list_list = []
    s_list_list = []
    printer = htparam = brief = None

    user_printers = s_list = b1_list = None

    user_printers_list, User_printers = create_model("User_printers", {"nr":int, "selected":bool}, {"selected": True})
    s_list_list, S_list = create_model("S_list", {"ind":int, "nr":int, "bezeich":str}, {"ind": 1})
    b1_list_list, B1_list = create_model("B1_list", {"nr":int, "position":str, "path":str, "make":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal n1, rate, usr_pr_defined, found, briefnr2, flag, b1_list_list, s_list_list, printer, htparam, brief


        nonlocal user_printers, s_list, b1_list
        nonlocal user_printers_list, s_list_list, b1_list_list
        return {"n1": n1, "rate": rate, "usr_pr_defined": usr_pr_defined, "found": found, "briefnr2": briefnr2, "flag": flag, "b1-list": b1_list_list, "s-list": s_list_list}

    def selected_printers():

        nonlocal n1, rate, usr_pr_defined, found, briefnr2, flag, b1_list_list, s_list_list, printer, htparam, brief


        nonlocal user_printers, s_list, b1_list
        nonlocal user_printers_list, s_list_list, b1_list_list

        i:int = 0
        s1:str = ""
        s2:str = ""

        for printer in db_session.query(Printer).filter(
                (Printer.bondrucker == False) &  (func.lower(Printer.opsysname) == "DOS")).all():
            user_printers = User_printers()
            user_printers_list.append(user_printers)

            user_printers.nr = printer.nr

        if SESSION:re.match(".*printerS ==.*",PARAMETER):

            for user_printers in query(user_printers_list):
                user_printers.selected = False
            s1 = SESSION:PARAMETER
            for i in range(1,len(s1)  + 1) :

                if substring(s1, i - 1, 9) == "printerS == ":
                    s2 = substring(s1, (i + 9) - 1, len(s1))
                    i = 999
            s1 = ""
            for i in range(1,len(s2)  + 1) :

                if substring(s2, i - 1, 1) == ";":

                    user_printers = query(user_printers_list, filters=(lambda user_printers :user_printers.nr == to_int(s1)), first=True)

                    if user_printers:
                        user_printers.selected = True
                    usr_pr_defined = True

                    return

                if substring(s2, i - 1, 1) == ",":

                    user_printers = query(user_printers_list, filters=(lambda user_printers :user_printers.nr == to_int(s1)), first=True)

                    if user_printers:
                        user_printers.selected = True
                    s1 = ""

                elif substring(s2, i - 1, 1) >= "0" and substring(s2, i - 1, 1) <= "9":
                    s1 = s1 + substring(s2, i - 1, 1)
            usr_pr_defined = True


    selected_printers()

    printer_obj_list = []
    for printer, user_printers in db_session.query(Printer, User_printers).join(User_printers,(User_printers.nr == Printer.nr) &  (User_printers.selected)).filter(
            (Printer.bondrucker == False) &  (func.lower(Printer.opsysname) == "DOS")).all():
        if printer._recid in printer_obj_list:
            continue
        else:
            printer_obj_list.append(printer._recid)


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.nr = printer.nr
        b1_list.position = printer.position
        b1_list.path = printer.path
        b1_list.make = printer.make

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 137)).first()
    rate = htparam.flogical

    if printer_nr != 0 and printer and not usr_pr_defined:

        if printer.nr == printer_nr:
            found = True
        else:
            found = False
            n1 = 0

            printer = db_session.query(Printer).filter(
                    (Printer.bondrucker == False) &  (func.lower(Printer.opsysname) == "DOS")).first()
            while not found and printer:
                n1 = n1 + 1

                if printer.nr == printer_nr:
                    found = True
                else:

                    printer = db_session.query(Printer).filter(
                            (Printer.bondrucker == False) &  (func.lower(Printer.opsysname) == "DOS")).first()
            flag = True

    brief = db_session.query(Brief).filter(
            (briefnr == briefnr)).first()
    s_list = S_list()
    s_list_list.append(s_list)

    s_list.ind = 1
    s_list.nr = briefnr
    s_list.bezeich = briefbezeich

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 415)).first()
    briefnr2 = htparam.finteger

    if briefnr2 != 0:

        brief = db_session.query(Brief).filter(
                (briefnr == briefnr2)).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.ind = 2
        s_list.nr = briefnr2
        s_list.bezeich = briefbezeich

    if printer:
        printer_nr = printer.nr

    return generate_output()