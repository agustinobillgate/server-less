from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Paramtext, Nightaudit, Kellner, Bediener, H_journal, H_artikel, Nitestor

def nt_rkas():
    long_digit:bool = False
    n:int = 0
    progname:str = "nt-rkas.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 80
    p_length:int = 56
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    curr_dept:int = 0
    curr_date:date = None
    from_dept:int = 0
    htparam = paramtext = nightaudit = kellner = bediener = h_journal = h_artikel = nitestor = None

    user_list = None

    user_list_list, User_list = create_model("User_list", {"kellner_nr":int, "dept":int, "userinit":str, "name":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_dept, curr_date, from_dept, htparam, paramtext, nightaudit, kellner, bediener, h_journal, h_artikel, nitestor


        nonlocal user_list
        nonlocal user_list_list

        return {}

    def journal_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_dept, curr_date, from_dept, htparam, paramtext, nightaudit, kellner, bediener, h_journal, h_artikel, nitestor


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
        line = "F&B-Cashiers Payment Report"
        add_line(line)
        line = ""
        for i in range(1,80 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        h_journal_obj_list = []
        for h_journal, kellner, bediener in db_session.query(H_journal, Kellner, Bediener).join(Kellner,(Kellner.kellner_nr == H_journal.kellner_nr)).join(Bediener,(Bediener.userinit == to_string(Kellner.kellner_nr, "99"))).filter(
                 (H_journal.departement >= 1) & (H_journal.bill_datum == curr_date) & ((H_journal.artart == 2) | (H_journal.artart == 6) | (H_journal.artart == 7))).order_by(H_journal.departement, Bediener.username).all():
            if h_journal._recid in h_journal_obj_list:
                continue
            else:
                h_journal_obj_list.append(h_journal._recid)

            user_list = query(user_list_list, filters=(lambda user_list: user_list.userinit == bediener.userinit and user_list.dept == h_journal.departement), first=True)

            if not user_list:
                it_exist = True
                user_list = User_list()
                user_list_list.append(user_list)

                user_list.kellner_nr = h_journal.kellner_nr
                user_list.dept = h_journal.departement
                user_list.userinit = bediener.userinit
                user_list.name = bediener.username

        for user_list in query(user_list_list, sort_by=[("dept",False),("name",False)]):

            if curr_userinit == "":
                curr_userinit = user_list.userinit
            add_line(" ")
            line = "##en+" + to_string(user_list.userinit, "x(2)") + " - " + user_list.name + "##en-"
            add_line(line)
            add_line(" ")
            line = "Dep TbNo BillNo ArtNo Qty Description Balance Time ID"
            add_line(line)
            line = ""
            for i in range(1,78 + 1) :
                line = line + "-"
            add_line(line)
            t_amt =  to_decimal("0")
            curr_artnr = 0

            h_journal_obj_list = []
            for h_journal, h_artikel in db_session.query(H_journal, H_artikel).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement)).filter(
                     (H_journal.departement >= 0) & (H_journal.bill_datum == curr_date) & (H_journal.kellner_nr == user_list.kellner_nr) & (H_journal.departement == user_list.dept) & ((H_journal.artart == 2) | (H_journal.artart == 6) | (H_journal.artart == 7))).order_by(H_artikel.artnr).all():
                if h_journal._recid in h_journal_obj_list:
                    continue
                else:
                    h_journal_obj_list.append(h_journal._recid)

                if curr_artnr == 0:
                    curr_artnr = h_artikel.artnr

                if curr_artnr != h_artikel.artnr or curr_userinit != user_list.userinit:
                    line = ""
                    for i in range(1,43 + 1) :
                        line = line + " "
                    for i in range(1,26 + 1) :
                        line = line + "-"
                    add_line(line)
                    line = ""
                    for i in range(1,43 + 1) :
                        line = line + " "

                    if not long_digit:
                        line = line + "T o t a l = " + to_string(t_amt, "->>,>>>,>>9.99")
                    else:
                        line = line + "T o t a l = " + to_string(t_amt, "->,>>>,>>>,>>9")
                    add_line(line)
                    add_line(" ")
                    t_amt =  to_decimal("0")
                    curr_artnr = h_journal.artnr
                    curr_userinit = user_list.userinit
                t_amt =  to_decimal(t_amt) + to_decimal(h_journal.betrag)

                if not long_digit:
                    line = to_string(h_journal.departement, ">>9") + " " + to_string(h_journal.tischnr, ">>>9") + " " + to_string(rechnr, ">,>>>,>>9") + " " + to_string(h_journal.artnr, ">>>>9") + " " + to_string(h_journal.anzahl, "->>9") + " " + to_string(h_journal.bezeich, "x(24)") + " " + to_string(betrag, "->>,>>>,>>9.99") + " " + to_string(zeit, "HH:MM") + " " + to_string(user_list.userinit, "x(2)")
                else:
                    line = to_string(h_journal.departement, ">>9") + " " + to_string(h_journal.tischnr, ">>>9") + " " + to_string(rechnr, ">,>>>,>>9") + " " + to_string(h_journal.artnr, ">>>>9") + " " + to_string(h_journal.anzahl, "->>9") + " " + to_string(h_journal.bezeich, "x(24)") + " " + to_string(betrag, "->,>>>,>>>,>>9") + " " + to_string(zeit, "HH:MM") + " " + to_string(user_list.userinit, "x(2)")
                add_line(line)
            line = ""
            for i in range(1,43 + 1) :
                line = line + " "
            for i in range(1,26 + 1) :
                line = line + "-"
            add_line(line)
            line = ""
            for i in range(1,43 + 1) :
                line = line + " "

            if not long_digit:
                line = line + "T o t a l = " + to_string(t_amt, "->>,>>>,>>9.99")
            else:
                line = line + "T o t a l = " + to_string(t_amt, "->,>>>,>>>,>>9")
            add_line(line)
            add_line(" ")
            t_amt =  to_decimal("0")
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_dept, curr_date, from_dept, htparam, paramtext, nightaudit, kellner, bediener, h_journal, h_artikel, nitestor


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