from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Paramtext, Htparam, Waehrung, Nightaudit, Nitestor, Guest, Bill, Zimmer, Res_line, Reservation, Segment, Arrangement, Guest_pr, Pricecod, Argt_line, Artikel, Reslin_queasy

def nt_revbdown():
    n:int = 0
    progname:str = "nt-revbdown.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 134
    p_length:int = 56
    curr_date:date = None
    price_decimal:int = 0
    exchg_rate:decimal = 1
    foreign_rate:bool = False
    frate:decimal = to_decimal("0.0")
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    paramtext = htparam = waehrung = nightaudit = nitestor = guest = bill = zimmer = res_line = reservation = segment = arrangement = guest_pr = pricecod = argt_line = artikel = reslin_queasy = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":str, "zinr":str, "argt":str, "zipreis":decimal, "lodging":decimal, "bfast":decimal, "lunch":decimal, "dinner":decimal, "misc":decimal, "pax":int, "rechnr":int, "ankunft":date, "abreise":date, "name":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, price_decimal, exchg_rate, foreign_rate, frate, htl_name, htl_adr, htl_tel, paramtext, htparam, waehrung, nightaudit, nitestor, guest, bill, zimmer, res_line, reservation, segment, arrangement, guest_pr, pricecod, argt_line, artikel, reslin_queasy


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        return {}

    def balance_list():

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, price_decimal, exchg_rate, foreign_rate, frate, htl_name, htl_adr, htl_tel, paramtext, htparam, waehrung, nightaudit, nitestor, guest, bill, zimmer, res_line, reservation, segment, arrangement, guest_pr, pricecod, argt_line, artikel, reslin_queasy


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,60 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,60 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,60 + 1) :
            line = line + " "
        line = line + "Page :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "Room Revenue Breakdown Report"
        add_line(line)
        line = ""
        for i in range(1,134 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        line = "GuestName RmNo Arg Pax Arrival Depart RoomRate Lodging Breakfast Lunch Dinner OtherRev BillNo"
        add_line(line)
        line = ""
        for i in range(1,134 + 1) :
            line = line + "-"
        add_line(line)
        add_line("##end-header")

        for cl_list in query(cl_list_list):
            it_exist = True

            if cl_list.flag.lower()  == ("*").lower() :
                line = ""
                for i in range(1,134 + 1) :
                    line = line + "-"
                add_line(line)
                line = ""
                line = line + "T O T A L"
                for i in range(1,10 + 1) :
                    line = line + " "
                line = line + to_string(to_int(cl_list.zinr) , ">>>>>9 ") + to_string("", "x(4)") + to_string(cl_list.pax, ">>9 ")
                for i in range(1,18 + 1) :
                    line = line + " "

                if price_decimal == 0:
                    line = line + to_string(cl_list.zipreis, " >>>,>>>,>>9 ") + to_string(cl_list.lodging, " >>>,>>>,>>9 ") + to_string(cl_list.bfast, ">>,>>>,>>9 ") + to_string(cl_list.lunch, ">>,>>>,>>9 ") + to_string(cl_list.dinner, ">>,>>>,>>9 ") + to_string(cl_list.misc, ">>,>>>,>>9")
                else:
                    line = line + to_string(cl_list.zipreis, ">>,>>>,>>9.99") + to_string(cl_list.lodging, ">>,>>>,>>9.99") + to_string(cl_list.bfast, ">>>,>>9.99 ") + to_string(cl_list.lunch, ">>>,>>9.99 ") + to_string(cl_list.dinner, ">>>,>>9.99 ") + to_string(cl_list.misc, ">>>,>>9.99")
                add_line(line)
            else:
                line = to_string(cl_list.name, "x(19) ") + to_string(cl_list.zinr, "x(6) ") + to_string(cl_list.argt, "x(3) ") + to_string(cl_list.pax, ">>9 ") + to_string(cl_list.ankunft) + " " + to_string(cl_list.abreise) + " " + to_string(cl_list.zipreis, ">>,>>>,>>9.99") + to_string(cl_list.lodging, ">>,>>>,>>9.99") + to_string(cl_list.bfast, ">>>,>>9.99 ") + to_string(cl_list.lunch, ">>>,>>9.99 ") + to_string(cl_list.dinner, ">>>,>>9.99 ") + to_string(cl_list.misc, ">>>,>>9.99 ") + to_string(cl_list.rechnr, ">>>>>>9 ")
                add_line(line)

        if not it_exist:
            add_line("***** " + "No Bookings found" + " *****")
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, price_decimal, exchg_rate, foreign_rate, frate, htl_name, htl_adr, htl_tel, paramtext, htparam, waehrung, nightaudit, nitestor, guest, bill, zimmer, res_line, reservation, segment, arrangement, guest_pr, pricecod, argt_line, artikel, reslin_queasy


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

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, price_decimal, exchg_rate, foreign_rate, frate, htl_name, htl_adr, htl_tel, paramtext, htparam, waehrung, nightaudit, nitestor, guest, bill, zimmer, res_line, reservation, segment, arrangement, guest_pr, pricecod, argt_line, artikel, reslin_queasy


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        member1 = None
        rguest = None
        mbill = None
        tot_val:decimal = to_decimal("0.0")
        total_val:decimal = to_decimal("0.0")
        tot_pax:int = 0
        tot_rm:int = 0
        tot_rate:decimal = to_decimal("0.0")
        tot_lodging:decimal = to_decimal("0.0")
        tot_bfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_misc:decimal = to_decimal("0.0")
        rate:decimal = to_decimal("0.0")
        curr_resnr:int = 0
        curr_zinr:str = ""
        do_it:bool = False
        bfast_art:int = 0
        lunch_art:int = 0
        dinner_art:int = 0
        lundin_art:int = 0
        fb_dept:int = 0
        argt_betrag:decimal = to_decimal("0.0")
        take_it:bool = False
        prcode:int = 0
        curr_zikatnr:int = 0
        Member1 =  create_buffer("Member1",Guest)
        Rguest =  create_buffer("Rguest",Guest)
        Mbill =  create_buffer("Mbill",Bill)
        tot_val =  to_decimal("0")
        total_val =  to_decimal("0")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 125)).first()
        bfast_art = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 126)).first()
        fb_dept = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 227)).first()
        lunch_art = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 228)).first()
        dinner_art = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 229)).first()
        lundin_art = htparam.finteger

        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr) & (Zimmer.sleeping)).filter(
                 (((Res_line.active_flag == 1) & (Res_line.resstatus != 12)) | ((Res_line.active_flag == 2) & (Res_line.zipreis != 0) & (Res_line.ankunft == curr_date) & (Res_line.abreise == curr_date))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr, Res_line.resnr).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            bill = db_session.query(Bill).filter(
                     (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).first()
            do_it = True

            if res_line.active_flag == 2 and bill.argtumsatz == 0:
                do_it = False

            if do_it:

                if res_line.l_zuordnung[0] != 0:
                    curr_zikatnr = res_line.l_zuordnung[0]
                else:
                    curr_zikatnr = res_line.zikatnr

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnrpay)).first()

                member1 = db_session.query(Member1).filter(
                         (Member1.gastnr == res_line.gastnrmember)).first()

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode)).first()

                mbill = db_session.query(Mbill).filter(
                         (Mbill.resnr == res_line.resnr) & (Mbill.reslinnr == 0)).first()
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.zinr = res_line.zinr
                cl_list.argt = res_line.arrangement
                cl_list.name = res_line.name
                cl_list.rechnr = bill.rechnr
                cl_list.pax = res_line.erwachs + res_line.kind1 + res_line.gratis
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise
                cl_list.zipreis =  to_decimal(res_line.zipreis)
                tot_rate =  to_decimal(tot_rate) + to_decimal(cl_list.zipreis)
                tot_pax = tot_pax + cl_list.pax
                lodging = cl_list.zipreis

                if lodging > 0:
                    prcode = 0

                    rguest = db_session.query(Rguest).filter(
                             (Rguest.gastnr == res_line.gastnr)).first()

                    arrangement = db_session.query(Arrangement).filter(
                             (Arrangement.arrangement == res_line.arrangement)).first()

                    guest_pr = db_session.query(Guest_pr).filter(
                             (Guest_pr.gastnr == rguest.gastnr)).first()

                    if guest_pr:

                        pricecod = db_session.query(Pricecod).filter(
                                 (Pricecod.code == guest_pr.code) & (Pricecod.marknr == res_line.reserve_int) & (Pricecod.argtnr == arrangement.argtnr) & (Pricecod.zikatnr == curr_zikatnr) & (curr_date >= Pricecod.startperiode) & (curr_date <= Pricecod.endperiode)).first()

                    if pricecod:
                        prcode = pricecod._recid

                    for argt_line in db_session.query(Argt_line).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & (not Argt_line.kind2)).order_by(Argt_line._recid).all():

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == argt_line.argt_artnr) & (Artikel.departement == argt_line.departement)).first()
                        take_it, argt_betrag = get_argtline_rate(prcode, argt_line._recid)

                        if take_it:

                            if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                                cl_list.bfast =  to_decimal(cl_list.bfast) + to_decimal(argt_betrag)
                                tot_bfast =  to_decimal(tot_bfast) + to_decimal(argt_betrag)
                                lodging = lodging - argt_betrag

                            elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                                cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(argt_betrag)
                                tot_lunch =  to_decimal(tot_lunch) + to_decimal(argt_betrag)
                                lodging = lodging - argt_betrag

                            elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                                cl_list.dinner =  to_decimal(cl_list.dinner) + to_decimal(argt_betrag)
                                tot_dinner =  to_decimal(tot_dinner) + to_decimal(argt_betrag)
                                lodging = lodging - argt_betrag

                            elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                                cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(argt_betrag)
                                tot_lunch =  to_decimal(tot_lunch) + to_decimal(argt_betrag)
                                lodging = lodging - argt_betrag
                            else:
                                cl_list.misc =  to_decimal(cl_list.misc) + to_decimal(argt_betrag)
                                tot_misc =  to_decimal(tot_misc) + to_decimal(argt_betrag)
                                lodging = lodging - argt_betrag
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(lodging)

                if curr_zinr != res_line.zinr or curr_resnr != res_line.resnr:
                    tot_rm = tot_rm + 1
                curr_zinr = res_line.zinr
                curr_resnr = res_line.resnr
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "*"
        cl_list.name = "T O T A L"
        cl_list.zinr = to_string(tot_rm, ">>>>>9")
        cl_list.pax = tot_pax
        cl_list.zipreis =  to_decimal(tot_rate)
        cl_list.lodging =  to_decimal(tot_lodging)
        cl_list.bfast =  to_decimal(tot_bfast)
        cl_list.lunch =  to_decimal(tot_lunch)
        cl_list.dinner =  to_decimal(tot_dinner)
        cl_list.misc =  to_decimal(tot_misc)


    def get_argtline_rate(code_recid:int, argt_recid:int):

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, price_decimal, exchg_rate, foreign_rate, frate, htl_name, htl_adr, htl_tel, paramtext, htparam, waehrung, nightaudit, nitestor, guest, bill, zimmer, res_line, reservation, segment, arrangement, guest_pr, pricecod, argt_line, artikel, reslin_queasy


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        add_it = False
        argt_betrag = to_decimal("0.0")
        qty:int = 0
        argtline = None

        def generate_inner_output():
            return (add_it, argt_betrag)

        Argtline =  create_buffer("Argtline",Argt_line)

        argtline = db_session.query(Argtline).filter(
                 (Argtline._recid == argt_recid)).first()

        if argt_line.fakt_modus == 1:
            add_it = True

        elif argt_line.fakt_modus == 2:

            if res_line.ankunft == curr_date:
                add_it = True

        elif argt_line.fakt_modus == 3:

            if (res_line.ankunft + 1) == curr_date:
                add_it = True

        elif argt_line.fakt_modus == 4 and get_day(curr_date) == 1:
            add_it = True

        elif argt_line.fakt_modus == 5 and get_day(curr_date + 1) == 1:
            add_it = True

        elif argt_line.fakt_modus == 6:

            if (res_line.ankunft + (argt_line.intervall - 1)) >= curr_date:
                add_it = True

        if add_it:

            if code_recid != 0:

                if argt_line.betriebsnr == 0:
                    qty = res_line.erwachs
                else:
                    qty = argt_line.betriebsnr

                pricecod = db_session.query(Pricecod).filter(
                         (Pricecod._recid == code_recid)).first()

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (Reslin_queasy.char1 == pricecod.code) & (Reslin_queasy.number1 == pricecod.marknr) & (Reslin_queasy.number2 == pricecod.argtnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).first()

                if reslin_queasy:
                    argt_betrag =  to_decimal(reslin_queasy.deci1)
                else:
                    argt_betrag =  to_decimal(argt_line.betrag)
            else:
                argt_betrag =  to_decimal(argt_line.betrag)
        argt_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

        return generate_inner_output()

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

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 143)).first()

    if htparam.flogical:
        foreign_rate = True

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 240)).first()

    if htparam.flogical:
        foreign_rate = True

    if foreign_rate:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        create_billbalance()
        balance_list()

    return generate_output()