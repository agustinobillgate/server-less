from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Paramtext, Nightaudit, Billjournal, Artikel, Bediener, Nitestor

def nt_fkas():
    long_digit:bool = False
    n:int = 0
    progname:str = "nt-fkas.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 82
    p_length:int = 56
    curr_date:date = None
    from_dept:int = 0
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    htparam = paramtext = nightaudit = billjournal = artikel = bediener = nitestor = None

    user_list = None

    user_list_list, User_list = create_model("User_list", {"userinit":str, "name":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, billjournal, artikel, bediener, nitestor


        nonlocal user_list
        nonlocal user_list_list

        return {}

    def journal_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, billjournal, artikel, bediener, nitestor


        nonlocal user_list
        nonlocal user_list_list

        i:int = 0
        it_exist:bool = False
        curr_artnr:int = 0
        t_amt:decimal = to_decimal("0.0")
        curr_userinit:str = ""
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
        line = "Front-office Cashiers Payment Report"
        add_line(line)
        line = ""
        for i in range(1,82 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.departement >= 0) & (Billjournal.bill_datum == curr_date)).order_by(Billjournal._recid).all():

            artikel = db_session.query(Artikel).filter(
                     (Artikel.departement == billjournal.departement) & (Artikel.artnr == billjournal.artnr)).first()

            if artikel and (artikel.artart == 2 or artikel.artart == 4 or artikel.artart == 6 or artikel.artart == 7):

                user_list = query(user_list_list, filters=(lambda user_list: user_list.userinit == billjournal.userinit), first=True)

                if not user_list:
                    it_exist = True
                    user_list = User_list()
                    user_list_list.append(user_list)

                    user_list.userinit = billjournal.userinit

                    bediener = db_session.query(Bediener).filter(
                             (Bediener.userinit == billjournal.userinit)).first()

                    if bediener:
                        user_list.name = bediener.username
                    else:
                        user_list.name = billjournal.userinit

        for user_list in query(user_list_list, sort_by=[("name",False)]):

            if curr_userinit == "":
                curr_userinit = user_list.userinit
            add_line(" ")
            line = "##en+" + to_string(user_list.userinit, "x(2)") + " - " + user_list.name + "##en-"
            add_line(line)
            add_line(" ")
            line = "Dep RmNo BillNo ArtNo Qty Description Balance Time ID"
            add_line(line)
            line = ""
            for i in range(1,84 + 1) :
                line = line + "-"
            add_line(line)
            t_amt =  to_decimal("0")
            curr_artnr = 0

            for billjournal in db_session.query(Billjournal).filter(
                     (Billjournal.departement >= 0) & (Billjournal.bill_datum == curr_date) & (Billjournal.anzahl != 0) & (Billjournal.userinit == user_list.userinit)).order_by(Billjournal.artnr).all():

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == billjournal.artnr) & (Artikel.departement == billjournal.departement)).first()

                if artikel and (artikel.artart == 2 or artikel.artart == 6 or artikel.artart == 7):

                    if curr_artnr == 0:
                        curr_artnr = artikel.artnr

                    if curr_artnr != artikel.artnr or curr_userinit != billjournal.userinit:
                        line = ""
                        for i in range(1,43 + 1) :
                            line = line + " "
                        for i in range(1,28 + 1) :
                            line = line + "-"
                        add_line(line)
                        line = ""
                        for i in range(1,43 + 1) :
                            line = line + " "

                        if not long_digit:
                            line = line + "T o t a l = " + to_string(t_amt, " ->>>,>>>,>>9.99")
                        else:
                            line = line + "T o t a l = " + to_string(t_amt, "->>>,>>>,>>>,>>9")
                        add_line(line)
                        add_line(" ")
                        t_amt =  to_decimal("0")
                        curr_artnr = billjournal.artnr
                        curr_userinit = billjournal.userinit
                    t_amt =  to_decimal(t_amt) + to_decimal(billjournal.betrag)

                    if not long_digit:
                        line = to_string(billjournal.departement, ">>9") + " " + to_string(billjournal.zinr) + " " + to_string(rechnr, ">,>>>,>>9") + " " + to_string(billjournal.artnr, ">>>>9") + " " + to_string(billjournal.anzahl, "->>9") + " " + to_string(billjournal.bezeich, "x(24)") + " " + to_string(betrag, " ->>>,>>>,>>9.99") + " " + to_string(zeit, "HH:MM") + " " + to_string(billjournal.userinit, "x(2)")
                    else:
                        line = to_string(billjournal.departement, ">>9") + " " + to_string(billjournal.zinr) + " " + to_string(rechnr, ">,>>>,>>9") + " " + to_string(billjournal.artnr, ">>>>9") + " " + to_string(billjournal.anzahl, "->>9") + " " + to_string(billjournal.bezeich, "x(24)") + " " + to_string(betrag, "->>>,>>>,>>>,>>9") + " " + to_string(zeit, "HH:MM") + " " + to_string(billjournal.userinit, "x(2)")
                    add_line(line)
        line = ""
        for i in range(1,43 + 1) :
            line = line + " "
        for i in range(1,28 + 1) :
            line = line + "-"
        add_line(line)
        line = ""
        for i in range(1,43 + 1) :
            line = line + " "

        if not long_digit:
            line = line + "T o t a l = " + to_string(t_amt, " ->>>,>>>,>>9.99")
        else:
            line = line + "T o t a l = " + to_string(t_amt, "->>>,>>>,>>>,>>9")
        add_line(line)
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, billjournal, artikel, bediener, nitestor


        nonlocal user_list
        nonlocal user_list_list

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