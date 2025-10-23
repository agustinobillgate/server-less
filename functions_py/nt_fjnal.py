#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 22-10-2025 
# Issue : 
# - New compile program
# - Fix space in string
# - Fix missing table "billjournal"
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Paramtext, Nightaudit, Hoteldpt, Billjournal, Nitestor

def nt_fjnal():

    prepare_cache ([Htparam, Paramtext, Nightaudit, Hoteldpt, Billjournal, Nitestor])

    long_digit:bool = False
    n:int = 0
    progname:string = "nt-fjnal.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:string = ""
    p_width:int = 80
    p_length:int = 56
    curr_date:date = None
    from_dept:int = 0
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    htparam = paramtext = nightaudit = hoteldpt = billjournal = nitestor = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, billjournal, nitestor


        nonlocal output_list
        nonlocal output_list_data

        return {}

    def journal_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, billjournal, nitestor


        nonlocal output_list
        nonlocal output_list_data

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,7 + 1) :
            line = line + " "
                            
        # Rulita,
        # - Fix space in string
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + "  " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,7 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,7 + 1) :
            line = line + " "
                                        
        # Rulita,
        # - Fix space in string
        line = line + "Page      :" + " " + "##page"
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

            billjournal = get_cache (Billjournal, {"departement": [(eq, hoteldpt.num)],"bill_datum": [(eq, curr_date)],"stornogrund": [(eq, "")]})

            if billjournal:
                it_exist = True
                add_line(" ")
                line = to_string(hoteldpt.num) + " " + hoteldpt.depart
                add_line(line)
                add_line(" ")
                                                        
                # Rulita,
                # - Fix space in string
                line = "RmNo      BillNo ArtNo  Qty Description                    Balance  Time ID"
                add_line(line)
                line = ""
                for i in range(1,76 + 1) :
                    line = line + "-"
                add_line(line)

                for billjournal in db_session.query(Billjournal).filter(
                         (Billjournal.departement == hoteldpt.num) & (Billjournal.bill_datum == curr_date) & (Billjournal.stornogrund == "")).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():

                    # Rulita,
                    # Issue :
                    # - Fix missing table "billjournal"
                    if long_digit:
                        line = to_string(billjournal.zinr) + " " + to_string(billjournal.rechnr, ">,>>>,>>9") + " " + to_string(billjournal.artnr, ">>>>9") + " " + to_string(billjournal.anzahl, "->>9") + " " + to_string(billjournal.bezeich, "x(23)") + " " + to_string(billjournal.betrag, "->,>>>,>>>,>>9") + " " + to_string(billjournal.zeit, "HH:MM") + " " + to_string(billjournal.userinit, "x(2)")

                    elif billjournal.betrag > 99999999 or billjournal.betrag < -99999999:
                        line = to_string(billjournal.zinr) + " " + to_string(billjournal.rechnr, ">,>>>,>>9") + " " + to_string(billjournal.artnr, ">>>>9") + " " + to_string(billjournal.anzahl, "->>9") + " " + to_string(billjournal.bezeich, "x(23)") + " " + to_string(billjournal.betrag, "->,>>>,>>>,>>9") + " " + to_string(billjournal.zeit, "HH:MM") + " " + to_string(billjournal.userinit, "x(2)")
                    else:
                        line = to_string(billjournal.zinr) + " " + to_string(billjournal.rechnr, ">,>>>,>>9") + " " + to_string(billjournal.artnr, ">>>>9") + " " + to_string(billjournal.anzahl, "->>9") + " " + to_string(billjournal.bezeich, "x(23)") + " " + to_string(billjournal.betrag, "->>,>>>,>>9.99") + " " + to_string(billjournal.zeit, "HH:MM") + " " + to_string(billjournal.userinit, "x(2)")
                    add_line(line)

        if not it_exist:
            add_line("***** " + "No Bookings found" + " *****")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, billjournal, nitestor


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
    from_dept = 0

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        journal_list()

    return generate_output()