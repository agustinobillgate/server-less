#using conversion tools version: 1.0.0.117

# =========================================
# Rulita, 23-10-2025 
# Issue : 
# - New compile program
# - Fix space in string
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Paramtext, Nightaudit, Artikel, Debitor, Bediener, Guest, Nitestor

def nt_debtbl():

    prepare_cache ([Htparam, Paramtext, Nightaudit, Artikel, Debitor, Bediener, Guest, Nitestor])

    pvilanguage:int = 0
    lvcarea:string = "nt-debt"
    long_digit:bool = False
    n:int = 0
    progname:string = "nt-debt.p"
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
    htparam = paramtext = nightaudit = artikel = debitor = bediener = guest = nitestor = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pvilanguage, lvcarea, long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, artikel, debitor, bediener, guest, nitestor

        return {}

    def journal_list():

        nonlocal pvilanguage, lvcarea, long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, artikel, debitor, bediener, guest, nitestor

        i:int = 0
        it_exist:bool = False
        curr_artnr:int = 0
        t_amt:Decimal = to_decimal("0.0")
        tot_amt:Decimal = to_decimal("0.0")
        guestname:string = ""
        userinit:string = ""
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string
        line = line + translateExtended ("Date/Time :", lvcarea, "") + " " + to_string(get_current_date()) + "  " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        line = line + translateExtended ("Bill.Date :", lvcarea, "") + " " + to_string(curr_date)
        add_line(line)
        line = translateExtended ("Tel", lvcarea, "") + " " + to_string(htl_tel, "x(36)")
        for i in range(1,20 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string
        line = line + translateExtended ("Page      :", lvcarea, "") + " " + "##page"
        add_line(line)
        add_line(" ")
        line = translateExtended ("List of transferred debts", lvcarea, "")
        add_line(line)
        line = ""
        for i in range(1,80 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        debitor_obj_list = {}
        debitor = Debitor()
        artikel = Artikel()
        for debitor.bediener_nr, debitor.artnr, debitor.saldo, debitor.gastnrmember, debitor.name, debitor.rechnr, debitor.zinr, debitor.gastnr, debitor._recid, artikel.artnr, artikel.bezeich, artikel._recid in db_session.query(Debitor.bediener_nr, Debitor.artnr, Debitor.saldo, Debitor.gastnrmember, Debitor.name, Debitor.rechnr, Debitor.zinr, Debitor.gastnr, Debitor._recid, Artikel.artnr, Artikel.bezeich, Artikel._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == Debitor.departement)).filter(
                 (Debitor.rgdatum == curr_date) & (Debitor.zahlkonto == 0)).order_by(Artikel.artart, Artikel.artnr, Debitor.name).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

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

                    # Rulita,
                    # - Fix space in string
                    if not long_digit:
                        line = line + "T o t a l   =  " + to_string(t_amt, "->>,>>>,>>9.99")
                    else:
                        line = line + "T o t a l   =  " + to_string(t_amt, "->,>>>,>>>,>>9")
                    add_line(line)
                    add_line(" ")
                curr_artnr = debitor.artnr
                add_line(" ")
                line = "##en+" + to_string(artikel.artnr) + " - " + artikel.bezeich + "##en-"
                add_line(line)
                add_line(" ")

                # Rulita,
                # - Fix space in string
                line = translateExtended ("Bill Receiver            GuestName               BillNo RmNo        Balance ID", lvcarea, "")
                add_line(line)
                line = ""
                for i in range(1,78 + 1) :
                    line = line + "-"
                add_line(line)
                t_amt =  to_decimal("0")
            t_amt =  to_decimal(t_amt) + to_decimal(debitor.saldo)
            tot_amt =  to_decimal(tot_amt) + to_decimal(debitor.saldo)

            if debitor.gastnr != debitor.gastnrmember:

                guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})
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

        # Rulita,
        # - Fix space in string
        if not long_digit:
            line = line + "T o t a l   =  " + to_string(t_amt, " ->>>,>>>,>>9.99")
        else:
            line = line + "T o t a l   =  " + to_string(t_amt, "->>>,>>>,>>>,>>9")
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


    def add_line(s:string):

        nonlocal pvilanguage, lvcarea, long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, artikel, debitor, bediener, guest, nitestor

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