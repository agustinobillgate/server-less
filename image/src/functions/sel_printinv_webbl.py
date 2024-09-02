from functions.additional_functions import *
import decimal
from sqlalchemy import func
import re
from models import Printer

def sel_printinv_webbl(session_param:str):
    t_printer_list = []
    s1:str = ""
    s2:str = ""
    i:int = 0
    usr_pr_defined:bool = False
    printer = None

    t_printer = user_printers = None

    t_printer_list, T_printer = create_model_like(Printer)
    user_printers_list, User_printers = create_model("User_printers", {"nr":int, "selected":bool}, {"selected": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_printer_list, s1, s2, i, usr_pr_defined, printer


        nonlocal t_printer, user_printers
        nonlocal t_printer_list, user_printers_list
        return {"t-printer": t_printer_list}


    for printer in db_session.query(Printer).filter(
            (Printer.bondrucker == False) &  (func.lower(Printer.opsysname) == "DOS")).all():
        t_printer = T_printer()
        t_printer_list.append(t_printer)

        buffer_copy(printer, t_printer)

    for t_printer in query(t_printer_list):
        user_printers = User_printers()
        user_printers_list.append(user_printers)

        user_printers.nr = t_printer.nr

    if re.match(".*printerS ==.*",session_param):

        for user_printers in query(user_printers_list):
            user_printers.selected = False
        s1 = session_param
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

                return generate_output()

            if substring(s2, i - 1, 1) == ",":

                user_printers = query(user_printers_list, filters=(lambda user_printers :user_printers.nr == to_int(s1)), first=True)

                if user_printers:
                    user_printers.selected = True
                s1 = ""

            elif substring(s2, i - 1, 1) >= "0" and substring(s2, i - 1, 1) <= "9":
                s1 = s1 + substring(s2, i - 1, 1)
        usr_pr_defined = True

    for t_printer in query(t_printer_list):

        user_printers = query(user_printers_list, filters=(lambda user_printers :user_printers.nr == t_printer.nr and user_printers.selected), first=True)

        if not user_printers:
            t_printer_list.remove(t_printer)

    return generate_output()