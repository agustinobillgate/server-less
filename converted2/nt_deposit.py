from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Paramtext, Nightaudit, Nitestor, Bill, Res_line, Billjournal, Guest, Reservation

def nt_deposit():
    long_digit:bool = False
    n:int = 0
    progname:str = "nt-deposit.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 80
    p_length:int = 56
    curr_date:date = None
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    htparam = paramtext = nightaudit = nitestor = bill = res_line = billjournal = guest = reservation = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":str, "zinr":str, "rechnr":int, "name":str, "receiver":str, "saldo":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, bill, res_line, billjournal, guest, reservation


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        return {}

    def deposit_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, bill, res_line, billjournal, guest, reservation


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,9 + 1) :
            line = line + " "
        line = line + "Date/Time : " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,9 + 1) :
            line = line + " "
        line = line + "Bill-Date : " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,9 + 1) :
            line = line + " "
        line = line + "Page : " + "##page"
        add_line(line)
        add_line(" ")
        line = "List of transferred deposits"
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        line = "RmNo BillNo GuestName Bill Receiver Deposit-Amount"
        add_line(line)
        line = fill("-", p_width)
        add_line(line)
        add_line("##end-header")

        for cl_list in query(cl_list_list):
            it_exist = True

            if cl_list.flag == "":
                line = to_string(cl_list.zinr) + " " + to_string(cl_list.rechnr, ">>>,>>>,>>9") + " " + to_string(cl_list.name, "x(24)") + " " + to_string(cl_list.receiver, "x(20)") + " " + to_string(cl_list.saldo, "->>>,>>>,>>9.99")
                add_line(line)

            elif cl_list.flag.lower()  == ("*").lower() :
                line = fill("-", 78)
                add_line(line)
                line = fill("-", 42)
                line = line + "T O T A L " + to_string(cl_list.saldo, "->>>,>>>,>>9.99")
                add_line(line)

            elif cl_list.flag.lower()  == ("**").lower() :
                line = fill("=", 78)
                add_line(line)
                line = ""
                add_line(line)
                line = cl_list.name + " " + trim(to_string(cl_list.saldo, "->>,>>>,>>>,>>9.99"))
                add_line(line)
                line = fill("=", 78)
                add_line(line)
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, bill, res_line, billjournal, guest, reservation


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


    def create_deposit():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, bill, res_line, billjournal, guest, reservation


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        tot_val:decimal = to_decimal("0.0")
        total_val:decimal = to_decimal("0.0")
        artnr:int = 0
        tot_deposit:decimal = to_decimal("0.0")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 120)).first()
        artnr = htparam.finteger
        tot_val =  to_decimal("0")

        billjournal_obj_list = []
        for billjournal, bill, res_line in db_session.query(Billjournal, Bill, Res_line).join(Bill,(Bill.rechnr == Billjournal.rechnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.reslinnr == Bill.reslinnr)).filter(
                 (Billjournal.bill_datum == curr_date) & (Billjournal.artnr == artnr) & (Billjournal.departement == 0) & (substring(Billjournal.bezeich, 0, 1) != ("*").lower())).order_by(Res_line.name).all():
            if billjournal._recid in billjournal_obj_list:
                continue
            else:
                billjournal_obj_list.append(billjournal._recid)


            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.zinr = bill.zinr
            cl_list.rechnr = bill.rechnr
            cl_list.name = res_line.name
            cl_list.receiver = res_line.name
            cl_list.saldo =  to_decimal(billjournal.betrag)

            if res_line.gastnrmember != res_line.gastnrpay:

                guest = db_session.query(Guest).filter(
                             (Guest.gastnr == res_line.gastnrpay)).first()
                cl_list.receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
            tot_val =  to_decimal(tot_val) + to_decimal(billjournal.betrag)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "*"
        cl_list.receiver = "T O T A L"
        cl_list.saldo =  to_decimal(tot_val)

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.activeflag == 0) & ((Reservation.depositbez != 0) | (Reservation.depositbez2 != 0))).order_by(Reservation._recid).all():

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == reservation.resnr) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 8))).first()

            if not res_line:
                tot_deposit =  to_decimal(tot_deposit) + to_decimal(reservation.depositbez) + to_decimal(reservation.depositbez2)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "**"
        cl_list.name = "Total Opened Paid Hotel Guest Deposit:"


        cl_list.saldo =  to_decimal(tot_deposit)

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

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        create_deposit()
        deposit_list()

    return generate_output()