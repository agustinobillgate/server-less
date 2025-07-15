from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Paramtext, Nightaudit, Nitestor, Bill, Bill_line, Guest, Res_line

def nt_balanrm():
    long_digit:bool = False
    n:int = 0
    progname:str = "nt-balanRm.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 115
    p_length:int = 56
    curr_date:date = None
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    htparam = paramtext = nightaudit = nitestor = bill = bill_line = guest = res_line = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":str, "zinr":str, "zipreis":decimal, "rechnr":int, "receiver":str, "ankunft":str, "abreise":str, "saldo":decimal, "name":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, bill, bill_line, guest, res_line


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        return {}

    def balance_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, bill, bill_line, guest, res_line


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,30 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,30 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,30 + 1) :
            line = line + " "
        line = line + "Page : " + "##page"
        add_line(line)
        add_line(" ")
        line = "Guest Account Balance"
        add_line(line)
        line = ""
        for i in range(1,115 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        line = "** " + "RmNo RoomRate BillNo GuestName Arrival Depart BillBalance BillReceiver"
        add_line(line)
        line = ""
        for i in range(1,115 + 1) :
            line = line + "-"
        add_line(line)
        add_line("##end-header")

        for cl_list in query(cl_list_list):
            it_exist = True

            if cl_list.flag.lower()  == ("**").lower() :
                line = ""
                for i in range(1,115 + 1) :
                    line = line + "-"
                add_line(line)
                line = ""
                for i in range(1,68 + 1) :
                    line = line + " "

                if not long_digit:
                    line = line + "T O T A L " + to_string(cl_list.saldo, "->>>,>>>,>>>,>>9.99")
                else:
                    line = line + "T O T A L " + to_string(cl_list.saldo, " ->,>>>,>>>,>>>,>>9")
                add_line(line)

                if cl_list.flag.lower()  == ("**").lower() :
                    add_line(" ")
                    add_line(" ")

            elif cl_list.flag.lower()  == ("*").lower() :
                line = ""
                for i in range(1,66 + 1) :
                    line = line + " "

                if not long_digit:
                    line = line + "GRAND T O T A L " + to_string(cl_list.saldo, "->,>>>,>>>,>>9.99")
                else:
                    line = line + "GRAND T O T A L " + to_string(cl_list.saldo, " ->>>,>>>,>>>,>>9")
                add_line(line)
            else:

                if not long_digit:
                    line = to_string(cl_list.flag, "x(2)") + " " + to_string(cl_list.zinr) + " " + to_string(cl_list.zipreis, ">,>>>,>>9.99") + " " + to_string(cl_list.rechnr, ">>>,>>>,>>9") + " " + to_string(cl_list.name, "x(30)") + " " + to_string(cl_list.ankunft) + " " + to_string(cl_list.abreise) + " " + to_string(cl_list.saldo, "->,>>>,>>>,>>9.99") + " " + to_string(cl_list.receiver, "x(24)")
                else:

                    if cl_list.zipreis <= 9999999:
                        line = to_string(cl_list.flag, "x(2)") + " " + to_string(cl_list.zinr) + " " + to_string(cl_list.zipreis, ">,>>>,>>9.99") + " " + to_string(cl_list.rechnr, ">>>,>>>,>>9") + " " + to_string(cl_list.name, "x(30)") + " " + to_string(cl_list.ankunft) + " " + to_string(cl_list.abreise) + " " + to_string(cl_list.saldo, " ->>>,>>>,>>>,>>9") + " " + to_string(cl_list.receiver, "x(24)")
                    else:
                        line = to_string(cl_list.flag, "x(2)") + " " + to_string(cl_list.zinr) + " " + to_string(cl_list.zipreis, " >>>,>>>,>>9") + " " + to_string(cl_list.rechnr, ">>>,>>>,>>9") + " " + to_string(cl_list.name, "x(30)") + " " + to_string(cl_list.ankunft) + " " + to_string(cl_list.abreise) + " " + to_string(cl_list.saldo, " ->>>,>>>,>>>,>>9") + " " + to_string(cl_list.receiver, "x(24)")
                add_line(line)

        if not it_exist:
            add_line("***** No Bookings found *****")
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, bill, bill_line, guest, res_line


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


    def create_billbalance():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, bill, bill_line, guest, res_line


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        tot_val:decimal = to_decimal("0.0")
        total_val:decimal = to_decimal("0.0")
        g_saldo:decimal = to_decimal("0.0")
        tot_val =  to_decimal("0")
        total_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr == 0)).order_by(Bill.name).all():
            g_saldo =  to_decimal(bill.saldo)

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum > curr_date)).order_by(Bill_line._recid).all():
                g_saldo =  to_decimal(g_saldo) - to_decimal(bill_line.betrag)

            if g_saldo != 0:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == bill.gastnr)).first()
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.flag = "NS"
                cl_list.receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                cl_list.name = ""
                cl_list.rechnr = bill.rechnr
                cl_list.saldo =  to_decimal(g_saldo)
                tot_val =  to_decimal(tot_val) + to_decimal(g_saldo)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "**"
        cl_list.name = "T O T A L"
        cl_list.saldo =  to_decimal(tot_val)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        tot_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.zinr == "")).order_by(Bill.name).all():

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == 1)).first()

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == bill.gastnr)).first()
            g_saldo =  to_decimal(bill.saldo)

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum > curr_date)).order_by(Bill_line._recid).all():
                g_saldo =  to_decimal(g_saldo) - to_decimal(bill_line.betrag)

            if g_saldo != 0:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.flag = "M"
                cl_list.receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                cl_list.name = ""
                cl_list.rechnr = bill.rechnr
                cl_list.saldo =  to_decimal(g_saldo)

                if res_line:
                    cl_list.ankunft = to_string(res_line.ankunft, "99/99/99")
                    cl_list.abreise = to_string(res_line.abreise, "99/99/99")
                tot_val =  to_decimal(tot_val) + to_decimal(g_saldo)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "**"
        cl_list.name = "T O T A L"
        cl_list.saldo =  to_decimal(tot_val)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        tot_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.zinr != "")).order_by(Bill.zinr).all():

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.reslinnr)).first()

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == bill.gastnr)).first()
            g_saldo =  to_decimal(bill.saldo)

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum > curr_date)).order_by(Bill_line._recid).all():
                g_saldo =  to_decimal(g_saldo) - to_decimal(bill_line.betrag)

            if g_saldo != 0:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.zinr = bill.zinr
                cl_list.receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if res_line:
                    cl_list.name = res_line.name
                    cl_list.zipreis =  to_decimal(res_line.zipreis)
                    cl_list.ankunft = to_string(res_line.ankunft, "99/99/99")
                    cl_list.abreise = to_string(res_line.abreise, "99/99/99")
                cl_list.rechnr = bill.rechnr
                cl_list.saldo =  to_decimal(g_saldo)
                tot_val =  to_decimal(tot_val) + to_decimal(g_saldo)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "**"
        cl_list.name = "T O T A L"
        cl_list.saldo =  to_decimal(tot_val)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "*"
        cl_list.name = "T O T A L"
        cl_list.saldo =  to_decimal(total_val)

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

    if not nightaudit:
        pass
    else:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        create_billbalance()
        balance_list()

    return generate_output()