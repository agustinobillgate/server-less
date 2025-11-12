#using conversion tools version: 1.0.0.117

# =========================================
# Rulita, 22-10-2025 
# Issue : 
# - New compile program
# - Fix space in string
# - Fix missing table "billjournal" rechnr
# - Fix missing table "billjournal" betrag
# - Fix missing table "billjournal" zeit
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Paramtext, Nightaudit, Billjournal, Artikel, Bediener, Nitestor

def nt_fkasbl():

    prepare_cache ([Htparam, Paramtext, Nightaudit, Billjournal, Artikel, Bediener, Nitestor])

    pvilanguage:int = 0
    lvcarea:string = "nt-fkas"
    long_digit:bool = False
    n:int = 0
    progname:string = "nt-fkas.p"
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
    htparam = paramtext = nightaudit = billjournal = artikel = bediener = nitestor = None

    user_list = None

    user_list_data, User_list = create_model("User_list", {"userinit":string, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pvilanguage, lvcarea, long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, billjournal, artikel, bediener, nitestor


        nonlocal user_list
        nonlocal user_list_data

        return {}

    def journal_list():

        nonlocal pvilanguage, lvcarea, long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, billjournal, artikel, bediener, nitestor


        nonlocal user_list
        nonlocal user_list_data

        i:int = 0
        it_exist:bool = False
        curr_artnr:int = 0
        t_amt:Decimal = to_decimal("0.0")
        curr_userinit:string = ""
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string
        line = line + translateExtended ("Date/Time :", lvcarea, "") + "  " + to_string(get_current_date()) + "  " + to_string(get_current_time_in_seconds(), "HH:MM")
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
        line = translateExtended ("Front-office Cashiers Payment Report", lvcarea, "")
        add_line(line)
        line = ""
        for i in range(1,82 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.departement >= 0) & (Billjournal.bill_datum == curr_date)).order_by(Billjournal._recid).all():

            artikel = get_cache (Artikel, {"departement": [(eq, billjournal.departement)],"artnr": [(eq, billjournal.artnr)]})

            if artikel and (artikel.artart == 2 or artikel.artart == 4 or artikel.artart == 6 or artikel.artart == 7):

                user_list = query(user_list_data, filters=(lambda user_list: user_list.userinit == billjournal.userinit), first=True)

                if not user_list:
                    it_exist = True
                    user_list = User_list()
                    user_list_data.append(user_list)

                    user_list.userinit = billjournal.userinit

                    bediener = get_cache (Bediener, {"userinit": [(eq, billjournal.userinit)]})

                    if bediener:
                        user_list.name = bediener.username
                    else:
                        user_list.name = billjournal.userinit

        for user_list in query(user_list_data, sort_by=[("name",False)]):

            if curr_userinit == "":
                curr_userinit = user_list.userinit
            add_line(" ")
            line = "##en+" + to_string(user_list.userinit, "x(2)") + " - " + user_list.name + "##en-"
            add_line(line)
            add_line(" ")

            # Rulita,
            # - Fix space in string
            line = translateExtended ("Dep RmNo      BillNo ArtNo  Qty Description                       Balance  Time ID", lvcarea, "")
            add_line(line)
            line = ""
            for i in range(1,84 + 1) :
                line = line + "-"
            add_line(line)
            t_amt =  to_decimal("0")
            curr_artnr = 0

            for billjournal in db_session.query(Billjournal).filter(
                     (Billjournal.departement >= 0) & (Billjournal.bill_datum == curr_date) & (Billjournal.anzahl != 0) & (Billjournal.userinit == user_list.userinit)).order_by(Billjournal.artnr).all():

                artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.departement)]})

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

                    # Rulita,
                    # Issue :
                    # - Fix missing table "billjournal" rechnr
                    # - Fix missing table "billjournal" betrag
                    # - Fix missing table "billjournal" zeit
                    if not long_digit:
                        line = to_string(billjournal.departement, ">>9") + " " + to_string(billjournal.zinr) + " " + to_string(billjournal.rechnr, ">,>>>,>>9") + " " + to_string(billjournal.artnr, ">>>>9") + " " + to_string(billjournal.anzahl, "->>9") + " " + to_string(billjournal.bezeich, "x(24)") + " " + to_string(billjournal.betrag, " ->>>,>>>,>>9.99") + " " + to_string(billjournal.zeit, "HH:MM") + " " + to_string(billjournal.userinit, "x(2)")
                    else:
                        line = to_string(billjournal.departement, ">>9") + " " + to_string(billjournal.zinr) + " " + to_string(billjournal.rechnr, ">,>>>,>>9") + " " + to_string(billjournal.artnr, ">>>>9") + " " + to_string(billjournal.anzahl, "->>9") + " " + to_string(billjournal.bezeich, "x(24)") + " " + to_string(billjournal.betrag, "->>>,>>>,>>>,>>9") + " " + to_string(billjournal.zeit, "HH:MM") + " " + to_string(billjournal.userinit, "x(2)")
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


    def add_line(s:string):

        nonlocal pvilanguage, lvcarea, long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, from_dept, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, billjournal, artikel, bediener, nitestor


        nonlocal user_list
        nonlocal user_list_data

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