from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Paramtext, Nightaudit, Artikel, Debitor, Bediener, Guest, Nitestor

def nt_debt():
    long_digit:bool = False
    n:int = 0
    progname:str = "nt-debt.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 80
    p_length:int = 56
    curr_date:date = None
    from_dept:int = 0
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    htparam = paramtext = nightaudit = artikel = debitor = bediener = guest = nitestor = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, artikel, debitor, bediener, guest, nitestor

        return {}

    def journal_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, artikel, debitor, bediener, guest, nitestor

        i:int = 0
        it_exist:bool = False
        curr_artnr:int = 0
        t_amt:decimal = to_decimal("0.0")
        tot_amt:decimal = to_decimal("0.0")
        guestname:str = ""
        userinit:str = ""
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,20 + 1) :
            line = line + " "
        line = line + "Page :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "List of transferred debts"
        add_line(line)
        line = ""
        for i in range(1,80 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        debitor_obj_list = []
        for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == Debitor.departement)).filter(
                 (Debitor.rgdatum == curr_date) & (Debitor.zahlkonto == 0)).order_by(Artikel.artart, Artikel.artnr, Debitor.name).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)

            bediener = db_session.query(Bediener).filter(
                     (Bediener.nr == debitor.bediener_nr)).first()

            if bediener:
                userinit = bediener.userinit
            else:
                userinit = ""

            if curr_artnr != debitor.artnr:

                if curr_artnr != 0:
                    line = ""
                    for i in range(1,46 + 1) :
                        line = line + " "
                    for i in range(1,29 + 1) :
                        line = line + "-"
                    add_line(line)
                    line = ""
                    for i in range(1,46 + 1) :
                        line = line + " "

                    if not long_digit:
                        line = line + "T o t a l = " + to_string(t_amt, "->>,>>>,>>9.99")
                    else:
                        line = line + "T o t a l = " + to_string(t_amt, "->,>>>,>>>,>>9")
                    add_line(line)
                    add_line(" ")
                curr_artnr = debitor.artnr
                add_line(" ")
                line = "##en+" + to_string(artikel.artnr) + " - " + artikel.bezeich + "##en-"
                add_line(line)
                add_line(" ")
                line = "Bill Receiver guestname BillNo RmNo Balance ID"
                add_line(line)
                line = ""
                for i in range(1,78 + 1) :
                    line = line + "-"
                add_line(line)
                t_amt =  to_decimal("0")
            t_amt =  to_decimal(t_amt) + to_decimal(debitor.saldo)
            tot_amt =  to_decimal(tot_amt) + to_decimal(debitor.saldo)

            if debitor.gastnr != debitor.gastnrmember:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == debitor.gastnrmember)).first()
                guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
            else:
                guestname = ""

            if not long_digit:
                line = to_string(debitor.name, "x(24)") + " " + to_string(guestname, "x(20)") + " " + to_string(debitor.rechnr, ">,>>>,>>9") + " " + to_string(debitor.zinr) + " " + to_string(debitor.saldo, "->>,>>>,>>9.99") + " " + to_string(userinit, "x(2)")
            else:
                line = to_string(debitor.name, "x(24)") + " " + to_string(guestname, "x(20)") + " " + to_string(debitor.rechnr, ">,>>>,>>9") + " " + to_string(debitor.zinr) + " " + to_string(debitor.saldo, "->,>>>,>>>,>>9") + " " + to_string(userinit, "x(2)")
            add_line(line)
        line = ""
        for i in range(1,46 + 1) :
            line = line + " "
        for i in range(1,29 + 1) :
            line = line + "-"
        add_line(line)
        line = ""
        for i in range(1,44 + 1) :
            line = line + " "

        if not long_digit:
            line = line + "T o t a l = " + to_string(t_amt, " ->>>,>>>,>>9.99")
        else:
            line = line + "T o t a l = " + to_string(t_amt, "->>>,>>>,>>>,>>9")
        add_line(line)
        add_line(" ")
        line = ""
        for i in range(1,46 + 1) :
            line = line + " "
        for i in range(1,29 + 1) :
            line = line + "="
        add_line(line)
        line = ""
        for i in range(1,44 + 1) :
            line = line + " "

        if not long_digit:
            line = line + "Total Debts = " + to_string(tot_amt, "->,>>>,>>>,>>9.99")
        else:
            line = line + "Total Debts = " + to_string(tot_amt, "->>>>,>>>,>>>,>>9")
        add_line(line)
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, artikel, debitor, bediener, guest, nitestor

        nitestor = db_session.query(Nitestor).filter(
                 (Nitestor.night_type == night_type) & (Nitestor.reihenfolge == reihenfolge) & (Nitestor.line_nr == line_nr)).first()

        if not nitestor:
            nitestor = Nitestor()
            db_session.add(nitestor)

            nitestor.night_type = night_type
            nitestor.reihenfolge = reihenfolge
            nitestor.line_nr = line_nr
        nitestor.line = s
        line_nr = line_nr + 1

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 200)).first()
    htl_name = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 201)).first()
    htl_adr = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 204)).first()
    htl_tel = paramtext.ptexte

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    curr_date = htparam.fdate
    from_dept = 0

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        journal_list()

    return generate_output()