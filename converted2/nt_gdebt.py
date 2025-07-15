from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Paramtext, Htparam, Nightaudit, Nitestor, Umsatz, Debitor, Bill, Reservation, Artikel

def nt_gdebt():
    n:int = 0
    progname:str = "nt-gdebt.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 70
    p_length:int = 56
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    bill_date:date = None
    paramtext = htparam = nightaudit = nitestor = umsatz = debitor = bill = reservation = artikel = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":str, "bezeich":str, "saldo":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, bill_date, paramtext, htparam, nightaudit, nitestor, umsatz, debitor, bill, reservation, artikel


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        return {}

    def balance_list():

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, bill_date, paramtext, htparam, nightaudit, nitestor, umsatz, debitor, bill, reservation, artikel


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,10 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,10 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(bill_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,10 + 1) :
            line = line + " "
        line = line + "Page :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "List of Debts Balance"
        add_line(line)
        add_line(" ")
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "-"
        add_line(line)
        line = "Debts Account Balance"
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "-"
        add_line(line)
        add_line(" ")
        add_line("##end-header")

        for cl_list in query(cl_list_list):
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


    def add_line(s:str):

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, bill_date, paramtext, htparam, nightaudit, nitestor, umsatz, debitor, bill, reservation, artikel


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

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


    def create_debtbalance():

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, bill_date, paramtext, htparam, nightaudit, nitestor, umsatz, debitor, bill, reservation, artikel


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        tot_val:decimal = to_decimal("0.0")
        total_val:decimal = to_decimal("0.0")
        datum:date = None
        umsatz1 = None
        umsatz2 = None
        debt = None
        tot_balance:decimal = to_decimal("0.0")
        artnr:int = 0
        curr_bezeich:str = ""
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
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Resident Guests"
        cl_list.saldo =  to_decimal(tot_val)
        tot_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr == 0) & (Bill.saldo != 0)).order_by(Bill._recid).all():
            tot_val =  to_decimal(tot_val) + to_decimal(bill.saldo)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Non Stay Guests"
        cl_list.saldo =  to_decimal(tot_val)
        tot_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.zinr == "") & (Bill.saldo != 0)).order_by(Bill._recid).all():
            tot_val =  to_decimal(tot_val) + to_decimal(bill.saldo)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Master Bills"
        cl_list.saldo =  to_decimal(tot_val)
        tot_val =  to_decimal("0")

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.depositbez != 0) & (Reservation.bestat_datum == None)).order_by(Reservation._recid).all():
            tot_val =  to_decimal(tot_val) - to_decimal(reservation.depositbez) - to_decimal(reservation.depositbez2)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Deposits"
        cl_list.saldo =  to_decimal(tot_val)
        tot_val =  to_decimal("0")
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Outlet Cashier's Outstandings"
        cl_list.saldo =  to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "*"
        artnr = 0
        tot_val =  to_decimal("0")
        curr_bezeich = ""

        debitor_obj_list = []
        for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).filter(
                 (Debitor.opart == 0) & (Debitor.zahlkonto == 0)).order_by(Artikel.artart, Artikel.bezeich).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)

            if artnr == 0:
                artnr = artikel.artnr
                curr_bezeich = artikel.bezeich

            if artnr != artikel.artnr:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

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
        cl_list_list.append(cl_list)

        cl_list.bezeich = curr_bezeich
        cl_list.saldo =  to_decimal(tot_val)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "**"
        cl_list.bezeich = "Total Debts"
        cl_list.saldo =  to_decimal(total_val)

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
    bill_date = htparam.fdate

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        create_debtbalance()
        balance_list()

    return generate_output()