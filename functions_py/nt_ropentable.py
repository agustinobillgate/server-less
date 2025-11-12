#using conversion tools version: 1.0.0.117

# ==================================================
# Rulita, 21-10-2025 
# Issue :
# - Fixing missing table "h_bill_line" betrag & zeit
# - Fix space in string 
# ==================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Paramtext, Nightaudit, H_bill, Hoteldpt, H_bill_line, Kellner, Nitestor

def nt_ropentable():

    prepare_cache ([Htparam, Paramtext, Nightaudit, H_bill, Hoteldpt, H_bill_line, Kellner, Nitestor])

    long_digit:bool = False
    n:int = 0
    progname:string = "nt-ropentable.p"
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
    htparam = paramtext = nightaudit = h_bill = hoteldpt = h_bill_line = kellner = nitestor = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, from_dept, htparam, paramtext, nightaudit, h_bill, hoteldpt, h_bill_line, kellner, nitestor


        nonlocal output_list
        nonlocal output_list_data

        return {}

    def create_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, from_dept, htparam, paramtext, nightaudit, h_bill, hoteldpt, h_bill_line, kellner, nitestor


        nonlocal output_list
        nonlocal output_list_data

        i:int = 0
        curr_dept:int = -1
        it_exist:bool = False
        saldo:Decimal = to_decimal("0.0")
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
        line = "POS Opened Tables Report"
        add_line(line)
        line = ""
        for i in range(1,80 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        for h_bill in db_session.query(H_bill).filter(
                 (H_bill.flag == 0) & (H_bill.departement >= from_dept)).order_by(H_bill.departement, H_bill.rechnr).all():
            saldo =  to_decimal("0")

            if not it_exist:
                it_exist = True
                add_line(" ")

                # Rulita,
                # - Fix space in string 
                line = "Table    BillNo  ArtNo  Description                Qty          Amount   Time"
                add_line(line)
                line = ""
                for i in range(1,80 + 1) :
                    line = line + "-"
                add_line(line)

            if curr_dept != h_bill.departement:
                curr_dept = h_bill.departement

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_bill.departement)]})
                add_line(" ")
                line = " " + to_string(hoteldpt.num, "99") + " - " + hoteldpt.depart
                add_line(line)
                add_line(" ")

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departement == h_bill.departement) & (H_bill_line.rechnr == h_bill.rechnr)).order_by(H_bill_line.sysdate, H_bill_line.zeit).all():
                saldo =  to_decimal(saldo) + to_decimal(h_bill_line.betrag)
                
                # Rulita, Fixing missing table "h_bill_line" variable : 
                # - betrag
                # - zeit
                if not long_digit:
                    line = to_string(h_bill_line.tischnr, ">>>>9 ") + to_string(h_bill_line.rechnr, ">>>>>>>9 ") + to_string(h_bill_line.artnr, ">>>>9 ") + to_string(h_bill_line.bezeich, "x(24) ") + to_string(h_bill_line.anzahl, "->>9 ") + to_string(h_bill_line.betrag, "->>,>>>,>>9.99 ") + to_string(h_bill_line.zeit, "HH:MM")
                else:
                    line = to_string(h_bill_line.tischnr, ">>>>9 ") + to_string(h_bill_line.rechnr, ">>>>>>>9 ") + to_string(h_bill_line.artnr, ">>>>9 ") + to_string(h_bill_line.bezeich, "x(24) ") + to_string(h_bill_line.anzahl, "->>9 ") + to_string(h_bill_line.betrag, "->,>>>,>>>,>>9 ") + to_string(h_bill_line.zeit, "HH:MM")
                add_line(line)
            line = ""
            for i in range(1,24 + 1) :
                line = line + " "
            for i in range(1,53 + 1) :
                line = line + "-"
            add_line(line)
            line = ""
            for i in range(1,24 + 1) :
                line = line + " "

            kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})

            if kellner:
                line = line + to_string(kellner.kellnername, "x(24) ")
            else:
                line = line + to_string("", "x(32)")

            if not long_digit:
                line = line + to_string(saldo, "->>,>>>,>>9.99")
            else:
                line = line + to_string(saldo, "->,>>>,>>>,>>9")
            add_line(line)
            add_line(" ")

        if not it_exist:
            add_line("***** " + "No Opened Table found" + " *****")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, from_dept, htparam, paramtext, nightaudit, h_bill, hoteldpt, h_bill_line, kellner, nitestor


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
        create_list()

    return generate_output()