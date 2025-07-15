from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Paramtext, Nightaudit, Hoteldpt, H_journal, Nitestor

def nt_rcjnal():
    long_digit:bool = False
    n:int = 0
    progname:str = "nt-rcjnal.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 105
    p_length:int = 56
    curr_date:date = None
    from_dept:int = 0
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    htparam = paramtext = nightaudit = hoteldpt = h_journal = nitestor = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, h_journal, nitestor


        nonlocal output_list
        nonlocal output_list_list

        return {}

    def journal_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, h_journal, nitestor


        nonlocal output_list
        nonlocal output_list_list

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,40 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,40 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,40 + 1) :
            line = line + " "
        line = line + "Page :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "Restaurant Cancellation Journal"
        add_line(line)
        line = ""
        for i in range(1,105 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept)).order_by(Hoteldpt.num).all():

            h_journal = db_session.query(H_journal).filter(
                     (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_date) & (H_journal.stornogrund != "")).first()

            if h_journal:
                it_exist = True
                add_line(" ")
                line = to_string(hoteldpt.num) + " " + hoteldpt.depart
                add_line(line)
                add_line(" ")
                line = "RmNo Table BillNo ArtNo Qty Description Balance Cancel Reason Time No"
                add_line(line)
                line = ""
                for i in range(1,107 + 1) :
                    line = line + "-"
                add_line(line)

                for h_journal in db_session.query(H_journal).filter(
                         (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_date) & (H_journal.stornogrund != "")).order_by(H_journal.sysdate, H_journal.zeit).all():

                    if not long_digit:
                        line = to_string(h_journal.zinr, "x(6)") + " " + to_string(h_journal.tischnr, ">>>9 ") + " " + to_string(rechnr, ">,>>>,>>9") + " " + to_string(h_journal.artnr, ">>>>9") + " " + to_string(h_journal.anzahl, "->>9") + " " + to_string(h_journal.bezeich, "x(23)") + " " + to_string(betrag, "->>,>>>,>>9.99") + " " + to_string(h_journal.stornogrund, "x(24)") + " " + to_string(zeit, "HH:MM") + " " + to_string(h_journal.kellner_nr, ">>9")
                    else:
                        line = to_string(h_journal.zinr, "x(6)") + " " + to_string(h_journal.tischnr, ">>>9 ") + " " + to_string(rechnr, ">,>>>,>>9") + " " + to_string(h_journal.artnr, ">>>>9") + " " + to_string(h_journal.anzahl, "->>9") + " " + to_string(h_journal.bezeich, "x(23)") + " " + to_string(betrag, "->,>>>,>>>,>>9") + " " + to_string(h_journal.stornogrund, "x(24)") + " " + to_string(zeit, "HH:MM") + " " + to_string(h_journal.kellner_nr, ">>9")
                    add_line(line)

        if not it_exist:
            add_line("***** " + "No Cancel-Bookings found" + " *****")
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, h_journal, nitestor


        nonlocal output_list
        nonlocal output_list_list

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

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 852)).first()
    from_dept = htparam.finteger

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