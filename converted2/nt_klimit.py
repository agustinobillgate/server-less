from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Paramtext, Nightaudit, Nitestor, Res_line, Bill, Guest

def nt_klimit():
    long_digit:bool = False
    n:int = 0
    progname:str = "nt-klimit.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 92
    p_length:int = 56
    curr_date:date = None
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    htparam = paramtext = nightaudit = nitestor = res_line = bill = guest = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"zinr":str, "rechnr":int, "name":str, "receiver":str, "klimit":int, "saldo":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, res_line, bill, guest


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        return {}

    def klimit_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, res_line, bill, guest


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,20 + 1) :
            line = line + " "
        line = line + "Bill-Date :" + " " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,20 + 1) :
            line = line + " "
        line = line + "Page :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "Over Credit Limit List"
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        line = "RmNo BillNo GuestName Bill Receiver Credit-Limit Bill-Balance"
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "-"
        add_line(line)
        add_line("##end-header")

        for cl_list in query(cl_list_list):
            it_exist = True

            if cl_list.klimit <= 9999999999:
                line = to_string(cl_list.zinr) + " " + to_string(cl_list.rechnr, ">>,>>>,>>9") + " " + to_string(cl_list.name, "x(24)") + " " + to_string(cl_list.receiver, "x(20)") + " " + to_string(cl_list.klimit, ">>>>,>>>,>>9") + " " + to_string(cl_list.saldo, ">>>>,>>>,>>9.99")
            else:
                line = to_string(cl_list.zinr) + " " + to_string(cl_list.rechnr, ">>,>>>,>>9") + " " + to_string(cl_list.name, "x(24)") + " " + to_string(cl_list.receiver, "x(20)") + " " + to_string(cl_list.klimit, ">>>>>>>>>>>9") + " " + to_string(cl_list.saldo, ">>>,>>>,>>>,>>9")
            add_line(line)

        if not it_exist:
            add_line("*** " + "No over credit limits found" + " ***")
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, res_line, bill, guest


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


    def create_klimit():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, res_line, bill, guest


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        tot_val:decimal = to_decimal("0.0")
        total_val:decimal = to_decimal("0.0")
        klimit:decimal = to_decimal("0.0")
        klimit0:decimal = to_decimal("0.0")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 68)).first()

        if htparam.fdecimal != 0:
            klimit0 =  to_decimal(htparam.fdecimal)
        else:
            klimit0 =  to_decimal(htparam.finteger)
        tot_val =  to_decimal("0")
        total_val =  to_decimal("0")

        bill_obj_list = []
        for bill, res_line in db_session.query(Bill, Res_line).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.reslinnr == Bill.reslinnr)).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.zinr != "") & (Bill.saldo != 0)).order_by(Res_line.name).all():
            if bill._recid in bill_obj_list:
                continue
            else:
                bill_obj_list.append(bill._recid)

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrpay)).first()
            klimit =  to_decimal(guest.kreditlimit)

            if klimit == 0:
                klimit =  to_decimal(klimit0)

            if bill.saldo > klimit:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.zinr = bill.zinr
                cl_list.rechnr = bill.rechnr
                cl_list.name = res_line.name

                if res_line.gastnrmember != res_line.gastnrpay:
                    cl_list.receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                cl_list.klimit = klimit
                cl_list.saldo =  to_decimal(bill.saldo)

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
        create_klimit()
        klimit_list()

    return generate_output()