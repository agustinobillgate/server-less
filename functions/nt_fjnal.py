from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Paramtext, Nightaudit, Hoteldpt, Billjournal, Nitestor

def nt_fjnal():
    long_digit:bool = False
    n:int = 0
    progname:str = "nt-fjnal.p"
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
    htparam = paramtext = nightaudit = hoteldpt = billjournal = nitestor = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, billjournal, nitestor


        nonlocal output_list
        nonlocal output_list_list

        return {}

    def journal_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, billjournal, nitestor


        nonlocal output_list
        nonlocal output_list_list

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,7 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,7 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,7 + 1) :
            line = line + " "
        line = line + "Page :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "Front-office Transaction Journal"
        add_line(line)
        line = ""
        for i in range(1,74 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept)).order_by(Hoteldpt.num).all():

            billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.departement == hoteldpt.num) & (Billjournal.bill_datum == curr_date) & (Billjournal.stornogrund == "")).first()

            if billjournal:
                it_exist = True
                add_line(" ")
                line = to_string(hoteldpt.num) + " " + hoteldpt.depart
                add_line(line)
                add_line(" ")
                line = "RmNo BillNo ArtNo Qty Description Balance Time ID"
                add_line(line)
                line = ""
                for i in range(1,76 + 1) :
                    line = line + "-"
                add_line(line)

                for billjournal in db_session.query(Billjournal).filter(
                         (Billjournal.departement == hoteldpt.num) & (Billjournal.bill_datum == curr_date) & (Billjournal.stornogrund == "")).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():

                    if long_digit:
                        line = to_string(billjournal.zinr) + " " + to_string(rechnr, ">,>>>,>>9") + " " + to_string(billjournal.artnr, ">>>>9") + " " + to_string(billjournal.anzahl, "->>9") + " " + to_string(billjournal.bezeich, "x(23)") + " " + to_string(billjournal.betrag, "->,>>>,>>>,>>9") + " " + to_string(billjournal.zeit, "HH:MM") + " " + to_string(billjournal.userinit, "x(2)")

                    elif billjournal.betrag > 99999999 or billjournal.betrag < -99999999:
                        line = to_string(billjournal.zinr) + " " + to_string(rechnr, ">,>>>,>>9") + " " + to_string(billjournal.artnr, ">>>>9") + " " + to_string(billjournal.anzahl, "->>9") + " " + to_string(billjournal.bezeich, "x(23)") + " " + to_string(billjournal.betrag, "->,>>>,>>>,>>9") + " " + to_string(billjournal.zeit, "HH:MM") + " " + to_string(billjournal.userinit, "x(2)")
                    else:
                        line = to_string(billjournal.zinr) + " " + to_string(rechnr, ">,>>>,>>9") + " " + to_string(billjournal.artnr, ">>>>9") + " " + to_string(billjournal.anzahl, "->>9") + " " + to_string(billjournal.bezeich, "x(23)") + " " + to_string(billjournal.betrag, "->>,>>>,>>9.99") + " " + to_string(billjournal.zeit, "HH:MM") + " " + to_string(billjournal.userinit, "x(2)")
                    add_line(line)

        if not it_exist:
            add_line("***** " + "No Bookings found" + " *****")
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, billjournal, nitestor


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