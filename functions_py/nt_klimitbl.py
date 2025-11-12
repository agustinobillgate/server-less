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
from models import Htparam, Paramtext, Nightaudit, Nitestor, Res_line, Bill, Guest

def nt_klimitbl():

    prepare_cache ([Htparam, Paramtext, Nightaudit, Nitestor, Res_line, Bill, Guest])

    pvilanguage:int = 0
    lvcarea:string = "nt-klimit"
    long_digit:bool = False
    n:int = 0
    progname:string = "nt-klimit.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:string = ""
    p_width:int = 92
    p_length:int = 56
    curr_date:date = None
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    htparam = paramtext = nightaudit = nitestor = res_line = bill = guest = None

    output_list = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"zinr":string, "rechnr":int, "name":string, "receiver":string, "klimit":int, "saldo":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pvilanguage, lvcarea, long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, res_line, bill, guest


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        return {}

    def klimit_list():

        nonlocal pvilanguage, lvcarea, long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, res_line, bill, guest


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        i:int = 0
        it_exist:bool = False
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
        line = line + translateExtended ("Bill-Date :", lvcarea, "") + " " + to_string(curr_date)
        add_line(line)
        line = translateExtended ("Tel", lvcarea, "") + " " + to_string(htl_tel, "x(36)")
        for i in range(1,20 + 1) :
            line = line + " "

        # Rulita,
        # - Fix space in string
        line = line + translateExtended ("Page      :", lvcarea, "") + " " + "##page"
        add_line(line)
        add_line(" ")
        line = translateExtended ("Over Credit Limit List", lvcarea, "")
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")

        # Rulita,
        # - Fix space in string
        line = translateExtended ("RmNo       BillNo GuestName                Bill Receiver        Credit-Limit    Bill-Balance", lvcarea, "")
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "-"
        add_line(line)
        add_line("##end-header")

        for cl_list in query(cl_list_data):
            it_exist = True

            if cl_list.klimit <= 9999999999:
                line = to_string(cl_list.zinr) + " " + to_string(cl_list.rechnr, ">>,>>>,>>9") + " " + to_string(cl_list.name, "x(24)") + " " + to_string(cl_list.receiver, "x(20)") + " " + to_string(cl_list.klimit, ">>>>,>>>,>>9") + " " + to_string(cl_list.saldo, ">>>>,>>>,>>9.99")
            else:
                line = to_string(cl_list.zinr) + " " + to_string(cl_list.rechnr, ">>,>>>,>>9") + " " + to_string(cl_list.name, "x(24)") + " " + to_string(cl_list.receiver, "x(20)") + " " + to_string(cl_list.klimit, ">>>>>>>>>>>9") + " " + to_string(cl_list.saldo, ">>>,>>>,>>>,>>9")
            add_line(line)

        if not it_exist:
            add_line("*** " + translateExtended ("No over credit limits found", lvcarea, "") + " ***")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal pvilanguage, lvcarea, long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, res_line, bill, guest


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


    def create_klimit():

        nonlocal pvilanguage, lvcarea, long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, htparam, paramtext, nightaudit, nitestor, res_line, bill, guest


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        tot_val:Decimal = to_decimal("0.0")
        total_val:Decimal = to_decimal("0.0")
        klimit:Decimal = to_decimal("0.0")
        klimit0:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 68)]})

        if htparam.fdecimal != 0:
            klimit0 =  to_decimal(htparam.fdecimal)
        else:
            klimit0 =  to_decimal(htparam.finteger)
        tot_val =  to_decimal("0")
        total_val =  to_decimal("0")

        bill_obj_list = {}
        bill = Bill()
        res_line = Res_line()
        for bill.zinr, bill.rechnr, bill.saldo, bill._recid, res_line.gastnrpay, res_line.name, res_line.gastnrmember, res_line._recid in db_session.query(Bill.zinr, Bill.rechnr, Bill.saldo, Bill._recid, Res_line.gastnrpay, Res_line.name, Res_line.gastnrmember, Res_line._recid).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.reslinnr == Bill.reslinnr)).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.zinr != "") & (Bill.saldo != 0)).order_by(Res_line.name).all():
            if bill_obj_list.get(bill._recid):
                continue
            else:
                bill_obj_list[bill._recid] = True

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
            klimit =  to_decimal(guest.kreditlimit)

            if klimit == 0:
                klimit =  to_decimal(klimit0)

            if bill.saldo > klimit:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.zinr = bill.zinr
                cl_list.rechnr = bill.rechnr
                cl_list.name = res_line.name

                if res_line.gastnrmember != res_line.gastnrpay:
                    cl_list.receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                cl_list.klimit = klimit
                cl_list.saldo =  to_decimal(bill.saldo)

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
        create_klimit()
        klimit_list()

    return generate_output()