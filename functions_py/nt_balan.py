#using conversion tools version: 1.0.0.117

# ============================
# Rulita, 22-10-2025 
# Issue : New compile program
# ============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Paramtext, Nightaudit, Nitestor, Bill, Bill_line, Guest, Res_line

def nt_balan():

    prepare_cache ([Htparam, Paramtext, Nightaudit, Nitestor, Bill, Bill_line, Guest, Res_line])

    long_digit:bool = False
    n:int = 0
    progname:string = "nt-balan.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:string = ""
    p_width:int = 115
    p_length:int = 56
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    curr_date:date = None
    htparam = paramtext = nightaudit = nitestor = bill = bill_line = guest = res_line = None

    output_list = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":string, "zinr":string, "zipreis":Decimal, "rechnr":int, "receiver":string, "ankunft":string, "abreise":string, "saldo":Decimal, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, htparam, paramtext, nightaudit, nitestor, bill, bill_line, guest, res_line


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        return {}

    def balance_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, htparam, paramtext, nightaudit, nitestor, bill, bill_line, guest, res_line


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,30 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(get_current_time_in_seconds(), "HH:MM")
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

        for cl_list in query(cl_list_data):
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
                for i in range(1,62 + 1) :
                    line = line + " "

                if not long_digit:
                    line = line + "GRAND T O T A L " + to_string(cl_list.saldo, "->>>,>>>,>>>,>>9.99")
                else:
                    line = line + "GRAND T O T A L " + to_string(cl_list.saldo, " ->,>>>,>>>,>>>,>>9")
                add_line(line)
            else:

                if not long_digit:
                    line = to_string(cl_list.flag, "x(2)") + " " + to_string(cl_list.zinr) + " " + to_string(cl_list.zipreis, ">>,>>>,>>9.99") + " " + to_string(cl_list.rechnr, ">>>,>>>,>>9") + " " + to_string(cl_list.name, "x(30)") + " " + to_string(cl_list.ankunft) + " " + to_string(cl_list.abreise) + " " + to_string(cl_list.saldo, "->,>>>,>>>,>>9.99") + " " + to_string(cl_list.receiver, "x(24)")
                else:

                    if cl_list.zipreis <= 9999999:
                        line = to_string(cl_list.flag, "x(2)") + " " + to_string(cl_list.zinr) + " " + to_string(cl_list.zipreis, ">>,>>>,>>9.99") + " " + to_string(cl_list.rechnr, ">>>,>>>,>>9") + " " + to_string(cl_list.name, "x(30)") + " " + to_string(cl_list.ankunft) + " " + to_string(cl_list.abreise) + " " + to_string(cl_list.saldo, " ->>>,>>>,>>>,>>9") + " " + to_string(cl_list.receiver, "x(24)")
                    else:
                        line = to_string(cl_list.flag, "x(2)") + " " + to_string(cl_list.zinr) + " " + to_string(cl_list.zipreis, " >>>,>>>,>>9") + " " + to_string(cl_list.rechnr, ">>>,>>>,>>9") + " " + to_string(cl_list.name, "x(30)") + " " + to_string(cl_list.ankunft) + " " + to_string(cl_list.abreise) + " " + to_string(cl_list.saldo, " ->>>,>>>,>>>,>>9") + " " + to_string(cl_list.receiver, "x(24)")
                add_line(line)

        if not it_exist:
            add_line("***** No Bookings found *****")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, htparam, paramtext, nightaudit, nitestor, bill, bill_line, guest, res_line


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


    def create_billbalance():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, htparam, paramtext, nightaudit, nitestor, bill, bill_line, guest, res_line


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        tot_val:Decimal = to_decimal("0.0")
        total_val:Decimal = to_decimal("0.0")
        g_saldo:Decimal = to_decimal("0.0")
        tot_val =  to_decimal("0")
        total_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr == 0)).order_by(Bill.name).all():
            g_saldo =  to_decimal(bill.saldo)

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum > curr_date)).order_by(Bill_line._recid).all():
                g_saldo =  to_decimal(g_saldo) - to_decimal(bill_line.betrag)

            if g_saldo != 0:

                guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.flag = "NS"
                cl_list.receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                cl_list.name = ""
                cl_list.rechnr = bill.rechnr
                cl_list.saldo =  to_decimal(g_saldo)
                tot_val =  to_decimal(tot_val) + to_decimal(g_saldo)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "**"
        cl_list.name = "T O T A L"
        cl_list.saldo =  to_decimal(tot_val)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        tot_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.zinr == "")).order_by(Bill.name).all():

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, 1)]})

            guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
            g_saldo =  to_decimal(bill.saldo)

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum > curr_date)).order_by(Bill_line._recid).all():
                g_saldo =  to_decimal(g_saldo) - to_decimal(bill_line.betrag)

            if g_saldo != 0:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

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
        cl_list_data.append(cl_list)

        cl_list.flag = "**"
        cl_list.name = "T O T A L"
        cl_list.saldo =  to_decimal(tot_val)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        tot_val =  to_decimal("0")

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.zinr != "")).order_by(Bill.name).all():

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
            g_saldo =  to_decimal(bill.saldo)

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum > curr_date)).order_by(Bill_line._recid).all():
                g_saldo =  to_decimal(g_saldo) - to_decimal(bill_line.betrag)

            if g_saldo != 0:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

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
        cl_list_data.append(cl_list)

        cl_list.flag = "**"
        cl_list.name = "T O T A L"
        cl_list.saldo =  to_decimal(tot_val)
        total_val =  to_decimal(total_val) + to_decimal(tot_val)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "*"
        cl_list.name = "T O T A L"
        cl_list.saldo =  to_decimal(total_val)

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

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        create_billbalance()
        balance_list()

    return generate_output()