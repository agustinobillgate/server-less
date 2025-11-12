#using conversion tools version: 1.0.0.117

# ========================================================
# Rulita, 21-10-2025 
# Issue :
# - Fixing missing table "h_journal" rechnr, betrag & zeit
# - Fix space in string 
# ========================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Paramtext, Nightaudit, Hoteldpt, H_journal, Nitestor

def nt_rjnal():

    prepare_cache ([Htparam, Paramtext, Nightaudit, Hoteldpt, H_journal, Nitestor])

    long_digit:bool = False
    n:int = 0
    progname:string = "nt-rjnal.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:string = ""
    p_width:int = 82
    p_length:int = 56
    curr_date:date = None
    from_dept:int = 0
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    htparam = paramtext = nightaudit = hoteldpt = h_journal = nitestor = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, h_journal, nitestor


        nonlocal output_list
        nonlocal output_list_data

        return {}

    def journal_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, h_journal, nitestor


        nonlocal output_list
        nonlocal output_list_data

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,20 + 1) :
            line = line + " "

        # Rulita,
        # - Fix space in string 
        line = line + "Page      :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "Restaurant Transaction Journal"
        add_line(line)
        line = ""
        for i in range(1,82 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept)).order_by(Hoteldpt.num).all():

            h_journal = get_cache (H_journal, {"departement": [(eq, hoteldpt.num)],"bill_datum": [(eq, curr_date)],"stornogrund": [(eq, "")]})

            if h_journal:
                it_exist = True
                add_line(" ")
                line = to_string(hoteldpt.num) + " " + hoteldpt.depart
                add_line(line)
                add_line(" ")

                # Rulita,
                # - Fix space in string 
                line = "RmNo   Table    BillNo ArtNo  Qty Description                    Balance  Time  No"
                add_line(line)
                line = ""
                for i in range(1,82 + 1) :
                    line = line + "-"
                add_line(line)

                for h_journal in db_session.query(H_journal).filter(
                         (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_date) & (H_journal.stornogrund == "")).order_by(H_journal.sysdate, H_journal.zeit).all():

                    # Rulita, Fixing missing table "h_journal." variable : 
                    # - rechnr
                    # - betrag
                    # - zeit
                    if not long_digit:
                        line = to_string(h_journal.zinr) + " " + to_string(h_journal.tischnr, ">>>9 ") + " " + to_string(h_journal.rechnr, ">,>>>,>>9") + " " + to_string(h_journal.artnr, ">>>>9") + " " + to_string(h_journal.anzahl, "->>9") + " " + to_string(h_journal.bezeich, "x(23)") + " " + to_string(h_journal.betrag, "->,>>>,>>>,>>9.99") + " " + to_string(h_journal.zeit, "HH:MM") + " " + to_string(h_journal.kellner_nr, ">>>9")
                    else:
                        line = to_string(h_journal.zinr) + " " + to_string(h_journal.tischnr, ">>>9 ") + " " + to_string(h_journal.rechnr, ">,>>>,>>9") + " " + to_string(h_journal.artnr, ">>>>9") + " " + to_string(h_journal.anzahl, "->>9") + " " + to_string(h_journal.bezeich, "x(23)") + " " + to_string(h_journal.betrag, "->>,>>>,>>>,>>9") + " " + to_string(h_journal.zeit, "HH:MM") + " " + to_string(h_journal.kellner_nr, ">>>9")
                    add_line(line)

        if not it_exist:
            add_line("***** " + "No Bookings found" + " *****")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, h_journal, nitestor


        nonlocal output_list
        nonlocal output_list_data

        nitestor = get_cache (Nitestor, {"night_type": [(eq, night_type)],"reihenfolge": [(eq, reihenfolge)],"line_nr": [(eq, line_nr)]})

        if not nitestor:
            nitestor = Nitestor()
            db_session.add(nitestor)

            nitestor.night_type = night_type
            nitestor.reihenfolge = reihenfolge
            nitestor.line_nr = line_nr
        nitestor.line = s
        line_nr = line_nr + 1
        pass


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    htl_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
    htl_adr = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    htl_tel = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    curr_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 852)]})
    from_dept = htparam.finteger

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        journal_list()

    return generate_output()