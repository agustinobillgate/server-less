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
from models import Htparam, Paramtext, Nightaudit, Hoteldpt, Artikel, Bill_line, Bill, Guest, Nitestor

def nt_outbill():

    prepare_cache ([Htparam, Paramtext, Nightaudit, Hoteldpt, Bill_line, Bill, Guest, Nitestor])

    long_digit:bool = False
    n:int = 0
    progname:string = "nt-outbill.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:string = ""
    p_width:int = 102
    p_length:int = 56
    curr_date:date = None
    from_dept:int = 0
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    htparam = paramtext = nightaudit = hoteldpt = artikel = bill_line = bill = guest = nitestor = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, artikel, bill_line, bill, guest, nitestor


        nonlocal output_list
        nonlocal output_list_data

        return {}

    def journal_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, artikel, bill_line, bill, guest, nitestor


        nonlocal output_list
        nonlocal output_list_data

        i:int = 0
        it_exist:bool = False
        do_it:bool = False
        gname:string = ""
        tot_val:Decimal = to_decimal("0.0")
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,27 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + "  " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,27 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,27 + 1) :
            line = line + " "
                 
        # Rulita,
        # - Fix space in string
        line = line + "Page      :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "Front-office Payment Journal"
        add_line(line)
        line = ""
        for i in range(1,102 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept)).order_by(Hoteldpt.num).all():
            do_it = True
            tot_val =  to_decimal("0")

            bill_line_obj_list = {}
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & ((Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7))).filter(
                     (Bill_line.departement == hoteldpt.num) & (Bill_line.bill_datum == curr_date)).order_by(Bill_line.zinr, Bill_line.sysdate, Bill_line.zeit).all():
                if bill_line_obj_list.get(bill_line._recid):
                    continue
                else:
                    bill_line_obj_list[bill_line._recid] = True

                if do_it:
                    add_line(" ")

                    if it_exist:
                        add_line(" ")
                    it_exist = True
                    line = to_string(hoteldpt.num) + " " + hoteldpt.depart
                    add_line(line)
                    add_line(" ")
                    
                    # Rulita,
                    # - Fix space in string
                    line = "RmNo      BillNo Guestname                        ArtNo Description                      Amount  Time ID"
                    add_line(line)
                    line = ""
                    for i in range(1,104 + 1) :
                        line = line + "-"
                    add_line(line)
                    do_it = False
                tot_val =  to_decimal(tot_val) + to_decimal(bill_line.betrag)

                bill = get_cache (Bill, {"rechnr": [(eq, bill_line.rechnr)]})

                guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
                gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if not long_digit:
                    line = to_string(bill_line.zinr) + " " + to_string(bill_line.rechnr, ">,>>>,>>9") + " " + to_string(gname, "x(32)") + " " + to_string(bill_line.artnr, ">>>>9") + " " + to_string(bill_line.bezeich, "x(22)") + " " + to_string(bill_line.betrag, " ->>>,>>>,>>9.99") + " " + to_string(bill_line.zeit, "HH:MM") + " " + to_string(bill_line.userinit, "x(2)")
                else:
                    line = to_string(bill_line.zinr) + " " + to_string(bill_line.rechnr, ">,>>>,>>9") + " " + to_string(gname, "x(32)") + " " + to_string(bill_line.artnr, ">>>>9") + " " + to_string(bill_line.bezeich, "x(22)") + " " + to_string(bill_line.betrag, "->>>,>>>,>>>,>>9") + " " + to_string(bill_line.zeit, "HH:MM") + " " + to_string(bill_line.userinit, "x(2)")
                add_line(line)

            if not do_it:
                add_line(" ")
                line = ""
                for i in range(1,54 + 1) :
                    line = line + " "

                if not long_digit:
                    line = line + "T O T A L             " + to_string(tot_val, "->,>>>,>>>,>>9.99")
                else:
                    line = line + ("T O T A L            ") + to_string(tot_val, "->,>>>,>>>,>>>,>>9")
                add_line(line)

        if not it_exist:
            add_line("***** " + "No Bookings found" + " *****")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, hoteldpt, artikel, bill_line, bill, guest, nitestor


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