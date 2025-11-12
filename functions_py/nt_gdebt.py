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
from models import Paramtext, Htparam, Nightaudit, Nitestor, Umsatz, Debitor, Bill, Reservation, Artikel

def nt_gdebt():

    prepare_cache ([Paramtext, Htparam, Nightaudit, Nitestor, Debitor, Bill, Reservation, Artikel])

    n:int = 0
    progname:string = "nt-gdebt.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:string = ""
    p_width:int = 70
    p_length:int = 56
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    bill_date:date = None
    paramtext = htparam = nightaudit = nitestor = umsatz = debitor = bill = reservation = artikel = None

    output_list = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":string, "bezeich":string, "saldo":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, bill_date, paramtext, htparam, nightaudit, nitestor, umsatz, debitor, bill, reservation, artikel


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        return {}

    def balance_list():

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, bill_date, paramtext, htparam, nightaudit, nitestor, umsatz, debitor, bill, reservation, artikel


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,10 + 1) :
            line = line + " "

        # Rulita,
        # - Fix space in string
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + "  " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,10 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(bill_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,10 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string
        line = line + "Page      :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "List of Debts Balance"
        add_line(line)
        add_line(" ")
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "-"
        add_line(line)
        
        # Rulita,
        # - Fix space in string
        line = "Debts Account                               Balance"
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "-"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        for cl_list in query(cl_list_data):
            it_exist = True

            if cl_list.flag.lower()  == ("*").lower() :
                add_line(" ")

            elif cl_list.flag.lower()  == ("**").lower() :
                add_line(" ")
                line = to_string(cl_list.bezeich, "x(30)") + " : " + to_string(cl_list.saldo, "->>>,>>>,>>>,>>9.99")
                add_line(line)
            else:
                line = to_string(cl_list.bezeich, "x(30)") + " : " + to_string(cl_list.saldo, "->>>,>>>,>>>,>>9.99")
                add_line(line)
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, bill_date, paramtext, htparam, nightaudit, nitestor, umsatz, debitor, bill, reservation, artikel


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

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


    def create_debtbalance():

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, bill_date, paramtext, htparam, nightaudit, nitestor, umsatz, debitor, bill, reservation, artikel


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        tot_val:Decimal = to_decimal("0.0")
        total_val:Decimal = to_decimal("0.0")
        datum:date = None
        umsatz1 = None
        umsatz2 = None
        debt = None
        tot_balance:Decimal = to_decimal("0.0")
        artnr:int = 0
        curr_bezeich:string = ""
        Umsatz1 =  create_buffer("Umsatz1",Umsatz)
        Umsatz2 =  create_buffer("Umsatz2",Umsatz)
        Debt =  create_buffer("Debt",Debitor)
        total_val =  to_decimal("0")
        tot_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.zinr != "") & (Bill.saldo != 0)).order_by(Bill._recid).all():
            tot_val =  to_decimal(tot_val) + to_decimal(bill.saldo)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Resident Guests"
        cl_list.saldo =  to_decimal(tot_val)
        tot_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr == 0) & (Bill.saldo != 0)).order_by(Bill._recid).all():
            tot_val =  to_decimal(tot_val) + to_decimal(bill.saldo)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Non Stay Guests"
        cl_list.saldo =  to_decimal(tot_val)
        tot_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.zinr == "") & (Bill.saldo != 0)).order_by(Bill._recid).all():
            tot_val =  to_decimal(tot_val) + to_decimal(bill.saldo)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Master Bills"
        cl_list.saldo =  to_decimal(tot_val)
        tot_val =  to_decimal("0")

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.depositbez != 0) & (Reservation.bestat_datum == None)).order_by(Reservation._recid).all():
            tot_val =  to_decimal(tot_val) - to_decimal(reservation.depositbez) - to_decimal(reservation.depositbez2)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Deposits"
        cl_list.saldo =  to_decimal(tot_val)
        tot_val =  to_decimal("0")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Outlet Cashier's Outstandings"
        cl_list.saldo =  to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "*"
        artnr = 0
        tot_val =  to_decimal("0")
        curr_bezeich = ""

        debitor_obj_list = {}
        debitor = Debitor()
        artikel = Artikel()
        for debitor.saldo, debitor.counter, debitor._recid, artikel.artnr, artikel.bezeich, artikel._recid in db_session.query(Debitor.saldo, Debitor.counter, Debitor._recid, Artikel.artnr, Artikel.bezeich, Artikel._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).filter(
                 (Debitor.opart == 0) & (Debitor.zahlkonto == 0)).order_by(Artikel.artart, Artikel.bezeich).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            if artnr == 0:
                artnr = artikel.artnr
                curr_bezeich = artikel.bezeich

            if artnr != artikel.artnr:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.bezeich = curr_bezeich
                cl_list.saldo =  to_decimal(tot_val)
                total_val =  to_decimal(total_val) + to_decimal(tot_val)
                artnr = artikel.artnr
                curr_bezeich = artikel.bezeich
                tot_val =  to_decimal("0")
            tot_val =  to_decimal(tot_val) + to_decimal(debitor.saldo)

            if debitor.counter != 0:

                for debt in db_session.query(Debt).filter(
                         (Debt.counter == debitor.counter) & (Debt.opart == 1)).order_by(Debt._recid).all():
                    tot_val =  to_decimal(tot_val) + to_decimal(debt.saldo)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = curr_bezeich
        cl_list.saldo =  to_decimal(tot_val)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "**"
        cl_list.bezeich = "Total Debts"
        cl_list.saldo =  to_decimal(total_val)

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    htl_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
    htl_adr = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    htl_tel = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        create_debtbalance()
        balance_list()

    return generate_output()