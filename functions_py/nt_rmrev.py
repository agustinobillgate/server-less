#using conversion tools version: 1.0.0.117

# ==============================
# Rulita, 22-10-2025 
# Issue : 
# - Fix missing table Zimkateg
# - added find firt zimkateg
# - Fix space in string
# ==============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Paramtext, Waehrung, Nightaudit, Nitestor, Guest, Bill, Zimmer, Res_line, Guest_pr, Arrangement, Reservation, Segment, Fixleist, Artikel, Reslin_queasy, Zimkateg

def nt_rmrev():

    prepare_cache ([Htparam, Paramtext, Waehrung, Nightaudit, Nitestor, Guest, Bill, Res_line, Guest_pr, Arrangement, Reservation, Segment, Fixleist, Reslin_queasy, Zimkateg])

    long_digit:bool = False
    n:int = 0
    progname:string = "nt-rmrev.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:string = ""
    p_width:int = 135
    p_length:int = 56
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    ct:string = ""
    contcode:string = ""
    bill_date:date = None
    price_decimal:int = 0
    exchg_rate:Decimal = 1
    frate:Decimal = to_decimal("0.0")
    foreign_rate:bool = False
    htparam = paramtext = waehrung = nightaudit = nitestor = guest = bill = zimmer = res_line = guest_pr = arrangement = reservation = segment = fixleist = artikel = reslin_queasy = None

    output_list = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":string, "gastnr":int, "zinr":string, "zipreis1":Decimal, "zipreis":Decimal, "fbrate":Decimal, "pax":int, "nat":string, "segm":string, "bemerk":string, "rechnr":int, "mrechnr":int, "receiver":string, "ankunft":date, "abreise":date, "name":string, "curr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, ct, contcode, bill_date, price_decimal, exchg_rate, frate, foreign_rate, htparam, paramtext, waehrung, nightaudit, nitestor, guest, bill, zimmer, res_line, guest_pr, arrangement, reservation, segment, fixleist, artikel, reslin_queasy


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        return {}

    def balance_list():

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, ct, contcode, bill_date, price_decimal, exchg_rate, frate, foreign_rate, htparam, paramtext, waehrung, nightaudit, nitestor, guest, bill, zimmer, res_line, guest_pr, arrangement, reservation, segment, fixleist, artikel, reslin_queasy


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,60 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string
        line = line + "Date/Time :" + "  " + to_string(get_current_date()) + " " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,60 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(bill_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,60 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string
        line = line + "Page      :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "Room Revenue and Occupancy Report"
        add_line(line)
        line = ""
        line = fill("_", 141)
        add_line(line)
        add_line(" ")

        # Rulita,
        # - Fix space in string
        line = "GuestName                Company / TA             RmNo   Pax Arrival  Depart   Nat Segment           RmRate  RateLocal Curr   BillNo  MBillNo"
        add_line(line)
        line = ""
        line = fill("-", 141)
        add_line(line)
        add_line("##end-header")

        for cl_list in query(cl_list_data):
            it_exist = True

            if cl_list.flag.lower()  == ("*").lower() :
                line = ""
                line = fill("_", 141)
                add_line(line)
                line = ""
                for i in range(1,21 + 1) :
                    line = line + " "
                line = line + "T O T A L"
                for i in range(1,19 + 1) :
                    line = line + " "
                line = line + to_string(to_int(cl_list.zinr) , ">>>>>9 ") + to_string(cl_list.pax, ">>9")
                for i in range(1,33 + 1) :
                    line = line + " "
                line = line + to_string(cl_list.zipreis, ">>>,>>>,>>9.99 ") + to_string(cl_list.zipreis1, ">>>,>>>,>>9.99")
                add_line(line)
            else:
                line = to_string(cl_list.name, "x(24)") + " " + to_string(cl_list.receiver, "x(24)") + " " + to_string(cl_list.zinr) + " " + to_string(cl_list.pax, ">>9 ") + to_string(cl_list.ankunft) + " " + to_string(cl_list.abreise) + " " + to_string(cl_list.nat, "x(3)") + " " + to_string(cl_list.segm, "x(10)") + " " + to_string(cl_list.zipreis, ">>,>>>,>>9.99 ")

                if price_decimal == 0:
                    line = line + to_string(cl_list.zipreis1, ">>,>>>,>>9 ")
                else:
                    line = line + to_string(cl_list.zipreis1, ">>>,>>>.99 ")
                line = line + to_string(cl_list.curr, "x(4) ") + to_string(cl_list.rechnr, ">>>>>>>9 ") + to_string(cl_list.mrechnr, ">>>>>>>9")
                add_line(line)

        if not it_exist:
            add_line("***** " + "No Bookings found" + " *****")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal long_digit, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, ct, contcode, bill_date, price_decimal, exchg_rate, frate, foreign_rate, htparam, paramtext, waehrung, nightaudit, nitestor, guest, bill, zimmer, res_line, guest_pr, arrangement, reservation, segment, fixleist, artikel, reslin_queasy


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

        nonlocal long_digit, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, ct, contcode, bill_date, price_decimal, exchg_rate, frate, foreign_rate, htparam, paramtext, waehrung, nightaudit, nitestor, guest, bill, zimmer, res_line, guest_pr, arrangement, reservation, segment, fixleist, artikel, reslin_queasy


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        member1 = None
        mbill = None
        tot_val:Decimal = to_decimal("0.0")
        total_val:Decimal = to_decimal("0.0")
        tot_rate:Decimal = to_decimal("0.0")
        tot_rate1:Decimal = to_decimal("0.0")
        argt_rate:Decimal = to_decimal("0.0")
        foreign_amt:Decimal = to_decimal("0.0")
        curr_resnr:int = 0
        resno:int = 0
        i:int = 0
        tot_pax:int = 0
        tot_rm:int = 0
        curr_zinr:string = ""
        do_it:bool = False
        fixed_rate:bool = False
        add_it:bool = False
        n:int = 0
        Member1 =  create_buffer("Member1",Guest)
        Mbill =  create_buffer("Mbill",Bill)
        tot_val =  to_decimal("0")
        total_val =  to_decimal("0")

        res_line_obj_list = {}
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                 (((Res_line.active_flag == 1) & (Res_line.resstatus != 12)) | ((Res_line.active_flag == 2) & (Res_line.zipreis != 0) & (Res_line.resstatus == 8) & (Res_line.ankunft == bill_date) & (Res_line.abreise == bill_date))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr, Res_line.name).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            contcode = ""

            guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

            if guest_pr:
                contcode = guest_pr.code
                ct = res_line.zimmer_wunsch

                if matches(ct,r"*$CODE$*"):
                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                    contcode = substring(ct, 0, get_index(ct, ";") - 1)

            if res_line.reserve_dec != 0:
                frate =  to_decimal(res_line.reserve_dec)
            else:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})
                frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            fixed_rate = False

            if res_line.was_status == 1:
                fixed_rate = True

            bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
            do_it = True

            if res_line.active_flag == 2 and bill.argtumsatz == 0:
                do_it = False

            if do_it:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

                member1 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                mbill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)]})

                # Rulita, 
                # Issue : Fix missing query zimkateg 
                zimkateg = get_cache (Zimkateg, {"zimkateg": [(eq, res_line.zikatnr)]})

                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.zinr = res_line.zinr

                if guest.karteityp > 0:
                    cl_list.receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                cl_list.name = res_line.name
                cl_list.rechnr = bill.rechnr
                cl_list.pax = res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis + res_line.l_zuordnung[3]
                cl_list.nat = member1.nation1
                for i in range(1,14 + 1) :

                    if i <= length(res_line.bemerk):

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(res_line.bemerk, i - 1, 1)
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if mbill:
                    cl_list.mrechnr = mbill.rechnr

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz
                cl_list.zipreis =  to_decimal(res_line.zipreis)
                cl_list.zipreis1 = to_decimal(round(res_line.zipreis * frate , price_decimal))

                if foreign_rate and price_decimal == 0:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

                    if htparam.finteger != 0:
                        n = 1
                        for i in range(1,htparam.finteger + 1) :
                            n = n * 10
                        cl_list.zipreis1 = to_decimal(round(cl_list.zipreis1 / n , 0) * n)
                tot_rate =  to_decimal(tot_rate) + to_decimal(cl_list.zipreis)
                tot_rate1 =  to_decimal(tot_rate1) + to_decimal(cl_list.zipreis1)

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                    add_it = False

                    if fixleist.sequenz == 1:
                        add_it = True

                    elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                        if res_line.ankunft == bill_date:
                            add_it = True

                    elif fixleist.sequenz == 4 and get_day(bill_date) == 1:
                        add_it = True

                    elif fixleist.sequenz == 5 and get_day(bill_date + 1) == 1:
                        add_it = True

                    elif fixleist.sequenz == 6:

                        if bill_date <= (res_line.ankunft + fixleist.dekade - 1):
                            add_it = True

                    if add_it:

                        artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                        argt_rate =  to_decimal(fixleist.betrag)

                        if not fixed_rate and guest_pr:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, zimkateg.zikatnr)],"number3": [(eq, fixleist.artnr)],"resnr": [(eq, fixleist.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                            if reslin_queasy:
                                argt_rate =  to_decimal(reslin_queasy.deci1)
                        cl_list.zipreis1 = to_decimal(cl_list.zipreis1 + round(argt_rate * frate , price_decimal))
                        tot_rate1 = to_decimal(tot_rate1 + round(argt_rate * frate , price_decimal))
                        cl_list.zipreis =  to_decimal(cl_list.zipreis) + to_decimal(argt_rate)
                        tot_rate =  to_decimal(tot_rate) + to_decimal(argt_rate)
                tot_pax = tot_pax + cl_list.pax

                if curr_zinr != res_line.zinr or curr_resnr != res_line.resnr:
                    tot_rm = tot_rm + 1
                curr_zinr = res_line.zinr
                curr_resnr = res_line.resnr
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "*"
        cl_list.receiver = "T O T A L"
        cl_list.zinr = to_string(tot_rm, ">>>>>9")
        cl_list.pax = tot_pax
        cl_list.zipreis1 =  to_decimal(tot_rate1)
        cl_list.zipreis =  to_decimal(tot_rate)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    htl_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
    htl_adr = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    htl_tel = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam.flogical:
        foreign_rate = True

    if not foreign_rate:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})

        if htparam.flogical:
            foreign_rate = True

    if foreign_rate:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

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