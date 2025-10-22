#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 22-10-2025 
# Issue : 
# - New compile program
# - Fix space in string
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Paramtext, Htparam, Nightaudit, Bill_line, Nitestor

def nt_calls():

    prepare_cache ([Paramtext, Htparam, Nightaudit, Bill_line, Nitestor])

    n:int = 0
    progname:string = "nt-calls.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:string = ""
    p_width:int = 80
    p_length:int = 56
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    curr_date:date = None
    from_dept:int = 0
    paramtext = htparam = nightaudit = bill_line = nitestor = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, from_dept, paramtext, htparam, nightaudit, bill_line, nitestor


        nonlocal output_list
        nonlocal output_list_data

        return {}

    def journal_list():

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, from_dept, paramtext, htparam, nightaudit, bill_line, nitestor


        nonlocal output_list
        nonlocal output_list_data

        i:int = 0
        it_exist:bool = False
        art1:int = 0
        art2:int = 0
        art3:int = 0
        tot_val:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 113)]})
        art1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 114)]})
        art2 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 115)]})
        art3 = htparam.finteger
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string
        line = line + "Date/Time : " + to_string(get_current_date()) + "  " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        line = line + "Bill.Date : " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,20 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string
        line = line + "Page      : " + "##page"
        add_line(line)
        add_line(" ")
        line = "Journal of Posted Calls"
        add_line(line)
        line = ""
        for i in range(1,80 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.departement == 0) & (Bill_line.bill_datum == curr_date) & ((Bill_line.artnr == art1) | (Bill_line.artnr == art2) | (Bill_line.artnr == art3))).order_by(Bill_line.sysdate, Bill_line.zeit, Bill_line.zinr).all():

            if not it_exist:
                it_exist = True
                add_line(" ")
                
                # Rulita,
                # - Fix space in string
                line = "RmNo    BillNo ArtNo  Qty Description                    Balance  Time ID"
                add_line(line)
                line = ""
                for i in range(1,74 + 1) :
                    line = line + "-"
                add_line(line)
            tot_val =  to_decimal(tot_val) + to_decimal(bill_line.betrag)

            # Rulita,
            # Issue :
            # - Fix missing table "bill_line"
            line = to_string(bill_line.zinr) + " " + to_string(bill_line.rechnr, ">,>>>,>>9") + " " + to_string(bill_line.artnr, ">>>>9") + " " + to_string(bill_line.anzahl, "->>9") + " " + to_string(bill_line.bezeich, "x(24)") + " " + to_string(bill_line.betrag, "->,>>>,>>9.99") + " " + to_string(bill_line.zeit, "HH:MM") + " " + to_string(bill_line.userinit, "x(2)")
            add_line(line)

        if it_exist:
            add_line(" ")
            
            # Rulita,
            # - Fix space in string
            line = "                                   " + "T O T A L" + "      " + to_string(tot_val, "->>,>>>,>>9.99")
            add_line(line)
        else:
            add_line("***** " + "No Bookings found" + " *****")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, from_dept, paramtext, htparam, nightaudit, bill_line, nitestor


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