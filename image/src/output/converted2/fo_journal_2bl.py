#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from functions.calc_servvat import calc_servvat
from models import Guest, Htparam, Bill, Bill_line, Res_line, Reservation, Segment, Artikel, Genstat, Hoteldpt, Billjournal, H_bill, Bk_veran, Arrangement, Argt_line

def fo_journal_2bl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, sorttype:int, exclude_artrans:bool, long_digit:bool, foreign_flag:bool, mi_onlyjournal:bool, mi_excljournal:bool, mi_post:bool, mi_showrelease:bool, mi_break:bool):

    prepare_cache ([Guest, Htparam, Bill, Res_line, Reservation, Segment, Artikel, Genstat, Hoteldpt, Billjournal, H_bill, Bk_veran])

    gtot = to_decimal("0.0")
    output_list_list = []
    curr_date:date = None
    descr1:string = ""
    voucher_no:string = ""
    ind:int = 0
    indexing:int = 0
    gdelimiter:string = ""
    roomnumber:string = ""
    zinrdate:date = None
    billnumber:int = 0
    curr_str:string = ""
    curr_resnr:int = 0
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    temp_str:string = ""
    hoteldept:int = 0
    guest = htparam = bill = bill_line = res_line = reservation = segment = artikel = genstat = hoteldpt = billjournal = h_bill = bk_veran = arrangement = argt_line = None

    output_list = buffguest = None

    output_list_list, Output_list = create_model("Output_list", {"bezeich":string, "c":string, "ns":string, "mb":string, "shift":string, "dept":string, "str":string, "remark":string, "gname":string, "descr":string, "voucher":string, "checkin":date, "checkout":date, "guestname":string, "segcode":string, "amt_nett":Decimal, "service":Decimal, "vat":Decimal, "zinr":string, "deptno":int})

    Buffguest = create_buffer("Buffguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gtot, output_list_list, curr_date, descr1, voucher_no, ind, indexing, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, serv, vat, netto, temp_str, hoteldept, guest, htparam, bill, bill_line, res_line, reservation, segment, artikel, genstat, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break
        nonlocal buffguest


        nonlocal output_list, buffguest
        nonlocal output_list_list

        return {"gtot": gtot, "output-list": output_list_list}

    def custom_record():

        nonlocal gtot, output_list_list, curr_date, descr1, voucher_no, ind, indexing, gdelimiter, serv, vat, netto, temp_str, hoteldept, guest, htparam, bill, bill_line, res_line, reservation, segment, artikel, genstat, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break
        nonlocal buffguest


        nonlocal output_list, buffguest
        nonlocal output_list_list

        roomnumber:string = ""
        zinrdate:date = None
        billnumber:int = 0
        curr_str:string = ""
        curr_resnr:int = 0
        journdate:date = None
        temp_resnr:int = 0
        temp_descr:string = ""
        artikelnr:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

        if htparam:
            journdate = htparam.fdate

        for output_list in query(output_list_list):
            roomnumber = substring(output_list.str, 8, 6)
            zinrdate = date_mdy(substring(output_list.str, 0, 8))
            billnumber = to_int(substring(output_list.str, 14, 9))
            artikelnr = to_int(substring(STR, 23, 4))
            curr_str = " "
            curr_resnr = 0

            if output_list.mb.lower()  == ("*").lower() :

                bill = get_cache (Bill, {"rechnr": [(eq, billnumber)]})

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"zinr": [(eq, roomnumber)]})

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, roomnumber)],"ankunft": [(le, zinrdate)],"abreise": [(ge, zinrdate)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:
                    output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.checkin = res_line.ankunft
                    output_list.checkout = res_line.abreise
                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    output_list.segcode = segment.bezeich
                else:
                    output_list.segcode = ""

            if matches(substring(STR, 77, 12),r"*T O T A L*"):
                output_list.guestname = ""
                output_list.segcode = ""
                output_list.checkin = None
                output_list.checkout = None
                output_list.str = substring(output_list.str, 0, 122)

            if matches(substring(STR, 77, 12),r"*Grand TOTAL*"):
                output_list.guestname = ""
                output_list.segcode = ""
                output_list.checkin = None
                output_list.checkout = None
                output_list.str = substring(output_list.str, 0, 122)

            if num_entries(output_list.gname, "|") >= 2:
                output_list.gname = entry(0, output_list.gname, "|")
                output_list.guestname = entry(0, output_list.gname, "|")

            if matches(output_list.descr,r"*[*"):
                temp_resnr = 0
                temp_descr = entry(0, output_list.descr, "]")

                if num_entries(temp_descr, "#") >= 2:
                    temp_resnr = to_int(entry(0, entry(1, temp_descr, "#") , " "))

                elif num_entries(output_list.descr, "[") > 1:

                    if num_entries(entry(0, output_list.descr, "[") , "/") <= 1:

                        artikel = get_cache (Artikel, {"artnr": [(eq, artikelnr)]})
                        temp_resnr = to_int(substring(entry(0, output_list.descr, "[") , length(artikel.bezeich) + 2 - 1))

                if temp_resnr != 0:

                    res_line = get_cache (Res_line, {"resnr": [(eq, temp_resnr)],"reslinnr": [(eq, 1)],"ankunft": [(le, zinrdate)],"abreise": [(ge, zinrdate)]})

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if guest:
                        output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.checkin = res_line.ankunft
                        output_list.checkout = res_line.abreise
                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        output_list.segcode = segment.bezeich
                    else:
                        output_list.segcode = ""

            elif matches(output_list.descr,r"*#*"):
                temp_descr = entry(0, output_list.descr, "]")

                if num_entries(temp_descr, "#") >= 2:
                    temp_resnr = to_int(entry(0, entry(1, temp_descr, "#") , " "))

                elif num_entries(output_list.descr, "[") > 1:

                    artikel = get_cache (Artikel, {"artnr": [(eq, artikelnr)]})
                    temp_resnr = to_int(substring(entry(0, output_list.descr, "[") , length(artikel.bezeich) + 2 - 1))

                if temp_resnr != 0:

                    res_line = get_cache (Res_line, {"resnr": [(eq, temp_resnr)],"reslinnr": [(eq, 1)],"ankunft": [(le, zinrdate)],"abreise": [(ge, zinrdate)]})

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if guest:
                        output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.checkin = res_line.ankunft
                        output_list.checkout = res_line.abreise
                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        output_list.segcode = segment.bezeich
                    else:
                        output_list.segcode = ""

            if roomnumber != "" and billnumber == 0:

                if zinrdate >= journdate:

                    res_line = get_cache (Res_line, {"zinr": [(eq, roomnumber)],"ankunft": [(eq, zinrdate)]})

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if guest:
                        output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.checkin = res_line.ankunft
                        output_list.checkout = res_line.abreise
                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        output_list.segcode = segment.bezeich
                    else:
                        output_list.segcode = ""

                elif zinrdate < journdate:

                    genstat = get_cache (Genstat, {"datum": [(eq, zinrdate)],"zinr": [(eq, roomnumber)]})

                    if genstat:

                        reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                        buffguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

                        guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                        if guest:
                            output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                            output_list.checkin = genstat.res_date[0]
                            output_list.checkout = genstat.res_date[1]
                            output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                            output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment:
                            output_list.segcode = segment.bezeich
                        else:
                            output_list.segcode = ""
            roomnumber = ""


    def journal_list():

        nonlocal gtot, output_list_list, descr1, voucher_no, ind, indexing, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, serv, vat, netto, temp_str, hoteldept, guest, htparam, bill, bill_line, res_line, reservation, segment, artikel, genstat, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break
        nonlocal buffguest


        nonlocal output_list, buffguest
        nonlocal output_list_list

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        lviresnr:int = -1
        lvcs:string = ""
        amount:Decimal = to_decimal("0.0")
        s:string = ""
        cnt:int = 0
        i:int = 0
        gqty:int = 0
        do_it:bool = True
        deptname:string = ""
        t_amt:Decimal = to_decimal("0.0")
        t_vat:Decimal = to_decimal("0.0")
        t_service:Decimal = to_decimal("0.0")
        tot_amt:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        loopind:int = 0
        gbuff = None
        Gbuff =  create_buffer("Gbuff",Guest)
        output_list_list.clear()

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement >= from_dept) & (Artikel.departement <= to_dept)).order_by((Artikel.departement * 10000 + Artikel.artnr)).all():

            if last_dept != artikel.departement:

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, artikel.departement)]})
            last_dept = artikel.departement
            sub_tot =  to_decimal("0")
            it_exist = False
            qty = 0
            for curr_date in date_range(from_date,to_date) :

                if sorttype == 0:

                    for billjournal in db_session.query(Billjournal).filter(
                             (Billjournal.artnr == artikel.artnr) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == curr_date) & (Billjournal.anzahl != 0)).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():
                        it_exist = True
                        do_it = True

                        if (mi_onlyjournal  and billjournal.bediener_nr == 0) or (mi_excljournal  and billjournal.bediener_nr != 0):
                            do_it = False

                        if exclude_artrans and billjournal.kassarapport:
                            do_it = False

                        if not mi_showrelease and billjournal.betrag == 0:
                            do_it = False

                        if do_it:
                            output_list = Output_list()
                            output_list_list.append(output_list)


                            if (billjournal.bediener_nr == 0 and mi_onlyjournal == False) or (billjournal.bediener_nr != 0 and mi_excljournal == False):
                                output_list.remark = billjournal.stornogrund

                            if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                                if billjournal.rechnr > 0:

                                    if billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                        bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                                        if bill and billjournal.zinr != "":

                                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, bill.zinr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                                            buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                                            if guest:
                                                output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                output_list.checkin = res_line.ankunft
                                                output_list.checkout = res_line.abreise
                                                output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                                                if segment:
                                                    output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.segcode = ""

                                        elif bill:

                                            if bill.resnr == 0 and bill.bilname != "":
                                                output_list.gname = bill.bilname
                                                output_list.guestname = bill.bilname
                                            else:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif billjournal.bediener_nr != 0 and mi_excljournal == False:

                                        h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                                        if h_bill:

                                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                                if res_line:

                                                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                    output_list.checkin = res_line.ankunft


                                                    output_list.checkout = res_line.abreise
                                                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                    output_list.gname = h_bill.bilname

                                                    if h_bill.bilname == "":

                                                        buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                                                        if buffguest:
                                                            output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                                                            output_list.guestname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                                                    genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})

                                                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                                                    if not segment:
                                                        output_list.segcode = ""
                                                    else:
                                                        output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                            elif h_bill.resnr > 0:

                                                guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                                if guest:
                                                    output_list.guestname = guest.name + "," + guest.vorname1
                                                    output_list.gname = h_bill.bilname


                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                                segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif h_bill.resnr == 0 and h_bill.bilname != "":
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                                segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif billjournal.betriebsnr == 0:

                                                bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                                                if bill:

                                                    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                                    if res_line:

                                                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                        output_list.checkin = res_line.ankunft


                                                        output_list.checkout = res_line.abreise
                                                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                        output_list.gname = bill.name

                                                        genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})

                                                        segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                                                        if not segment:
                                                            output_list.segcode = ""
                                                        else:
                                                            output_list.segcode = segment.bezeich
                                else:

                                    if get_index(billjournal.bezeich, " *BQT") > 0:

                                        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, to_int(substring(billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5  - 1)))]})

                                        if bk_veran:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                                        lviresnr = -1
                                        lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, "[#") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, " "))

                                        reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                        if reservation:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif get_index(billjournal.bezeich, " #") > 0 and billjournal.departement == 0:
                                        lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, " #") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, "]"))

                                        reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                        if reservation:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:

                                arrangement = get_cache (Arrangement, {"artnr_logis": [(eq, artikel.artnr)],"intervall": [(eq, artikel.departement)]})

                                if arrangement:

                                    h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.departement)]})

                                    if h_bill:

                                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                            if res_line:
                                                output_list.guestname = res_line.name
                                                output_list.gname = h_bill.bilname

                                                genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})

                                                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich
                                            else:
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                        elif h_bill.resnr > 0:

                                            guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                            if guest:
                                                output_list.guestname = guest.name + "," + guest.vorname1
                                                output_list.gname = h_bill.bilname


                                            else:
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                            segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                            if not segment:
                                                output_list.segcode = ""
                                            else:
                                                output_list.segcode = segment.bezeich

                                        elif h_bill.resnr == 0:
                                            output_list.guestname = h_bill.bilname
                                            output_list.gname = h_bill.bilname

                                            segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                            if not segment:
                                                output_list.segcode = ""
                                            else:
                                                output_list.segcode = segment.bezeich
                                else:

                                    argt_line = get_cache (Argt_line, {"argt_artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)]})

                                    if argt_line:
                                        hoteldept = billjournal.departement

                                        if matches(billjournal.bezeich, ("*<*")) and matches(billjournal.bezeich, ("*>*")):
                                            hoteldept = to_int(substring(billjournal.bezeich, get_index(billjournal.bezeich, "<") + 1 - 1, get_index(billjournal.bezeich, ">") - get_index(billjournal.bezeich, "<") - 1))

                                        h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, hoteldept)]})

                                        if h_bill:

                                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                                if res_line:

                                                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                    output_list.checkin = res_line.ankunft


                                                    output_list.checkout = res_line.abreise
                                                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                    output_list.gname = h_bill.bilname

                                                    genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})

                                                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                                                    if not segment:
                                                        output_list.segcode = ""
                                                    else:
                                                        output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                            elif h_bill.resnr > 0:

                                                guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                                if guest:
                                                    output_list.guestname = guest.name + "," + guest.vorname1
                                                    output_list.gname = h_bill.bilname


                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                                segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif h_bill.resnr == 0:
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                                segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                            if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                output_list.bezeich = artikel.bezeich

                            if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                output_list.c = to_string(billjournal.betriebsnr, "99")
                                output_list.shift = to_string(billjournal.betriebsnr, "99")

                            elif billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                if bill:

                                    if bill.reslinnr == 1 and bill.zinr == "":
                                        output_list.c = "N"
                                        output_list.ns = "*"

                                    elif bill.reslinnr == 0:
                                        output_list.c = "M"
                                        output_list.mb = "*"

                            if foreign_flag:
                                amount =  to_decimal(billjournal.fremdwaehrng)
                            else:
                                amount =  to_decimal(billjournal.betrag)

                            if mi_break :
                                serv =  to_decimal("0")
                                vat =  to_decimal("0")


                                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))
                                output_list.amt_nett =  to_decimal(amount) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                                output_list.service =  to_decimal(output_list.amt_nett) * to_decimal(serv)
                                output_list.vat =  to_decimal(output_list.amt_nett) * to_decimal(vat)
                                t_amt =  to_decimal(t_amt) + to_decimal(output_list.amt_nett)
                                t_vat =  to_decimal(t_vat) + to_decimal(output_list.vat)
                                t_service =  to_decimal(t_service) + to_decimal(output_list.service)
                                tot_amt =  to_decimal(tot_amt) + to_decimal(output_list.amt_nett)
                                tot_vat =  to_decimal(tot_vat) + to_decimal(output_list.vat)
                                tot_service =  to_decimal(tot_service) + to_decimal(output_list.service)


                            descr1 = ""
                            voucher_no = ""

                            if substring(billjournal.bezeich, 0, 1) == ("*").lower()  or billjournal.kassarapport:
                                descr1 = billjournal.bezeich
                                voucher_no = ""


                            else:

                                if not artikel.bezaendern:
                                    ind = num_entries(billjournal.bezeich, "]")

                                    if ind >= 2:
                                        gdelimiter = "]"
                                    else:
                                        ind = num_entries(billjournal.bezeich, "/")

                                        if ind >= 2 and length(artikel.bezeich) <= get_index(billjournal.bezeich, "/") and billjournal.betrag != 0:
                                            gdelimiter = "/"
                                        else:
                                            ind = num_entries(billjournal.bezeich, "|")

                                            if ind >= 2:
                                                gdelimiter = "|"

                                    if ind != 0:

                                        if ind == 1:
                                            descr1 = billjournal.bezeich
                                            voucher_no = ""

                                        elif ind == 2:
                                            descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                            voucher_no = entry(1, billjournal.bezeich, gdelimiter)

                                            if gdelimiter.lower()  == ("]").lower() :
                                                descr1 = descr1 + gdelimiter

                                        elif ind > 2:
                                            voucher_no = ""
                                            descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                            for loopind in range(2,ind + 1) :
                                                voucher_no = voucher_no + entry(loopind - 1, billjournal.bezeich, gdelimiter) + gdelimiter
                                            voucher_no = substring(voucher_no, 0, length(voucher_no) - 1)
                                    else:
                                        descr1 = billjournal.bezeich
                                else:
                                    ind = num_entries(billjournal.bezeich, "/")

                                    if ind == 1:
                                        descr1 = billjournal.bezeich
                                        voucher_no = ""

                                    elif ind == 2:
                                        descr1 = entry(0, billjournal.bezeich, "/")
                                        voucher_no = entry(1, billjournal.bezeich, "/")

                                    elif ind > 2:
                                        descr1 = entry(0, billjournal.bezeich, "/")
                                        for loopind in range(2,ind + 1) :
                                            voucher_no = voucher_no + entry(loopind - 1, billjournal.bezeich, "/") + "/"
                                        voucher_no = substring(voucher_no, 0, length(voucher_no) - 1)
                                    else:
                                        descr1 = billjournal.bezeich

                            if output_list:
                                output_list.descr = to_string(descr1, "x(100)")
                                output_list.voucher = to_string(voucher_no, "x(40)")

                            if billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})

                                if hoteldpt:
                                    deptname = hoteldpt.depart
                                output_list.zinr = billjournal.zinr
                                output_list.deptno = billjournal.departement

                                if not long_digit:
                                    str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(deptname, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(50)") + to_string(deptname, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + billjournal.anzahl
                                gqty = gqty + billjournal.anzahl

                                if foreign_flag:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.fremdwaehrng)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.fremdwaehrng)
                                else:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

                            elif billjournal.bediener_nr != 0 and mi_excljournal == False:

                                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})

                                if hoteldpt:
                                    deptname = hoteldpt.depart
                                output_list.zinr = billjournal.zinr
                                output_list.deptno = billjournal.departement

                                if not long_digit:
                                    str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(deptname, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(50)") + to_string(deptname, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + billjournal.anzahl
                                gqty = gqty + billjournal.anzahl

                                if foreign_flag:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.fremdwaehrng)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.fremdwaehrng)
                                else:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

                            elif mi_excljournal:

                                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})

                                if hoteldpt:
                                    deptname = hoteldpt.depart
                                output_list.zinr = billjournal.zinr
                                output_list.deptno = billjournal.departement

                                if not long_digit:
                                    str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(deptname, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(50)") + to_string(deptname, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + billjournal.anzahl
                                gqty = gqty + billjournal.anzahl

                                if foreign_flag:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.fremdwaehrng)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.fremdwaehrng)
                                else:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

                            if res_line and res_line.ankunft == res_line.abreise and artikel.departement > 0:
                                qty = qty - billjournal.anzahl + res_line.erwachs
                                gqty = gqty - billjournal.anzahl + res_line.erwachs
                                temp_str = substring(STR, 100)
                                str = substring(STR, 0, 95)
                                str = str + to_string(res_line.erwachs, "-9999") + temp_str
                                temp_str = ""


                elif sorttype == 1:

                    for billjournal in db_session.query(Billjournal).filter(
                             (Billjournal.artnr == artikel.artnr) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == curr_date)).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():
                        it_exist = True
                        do_it = True

                        if (mi_onlyjournal  and billjournal.bediener_nr == 0) or (mi_excljournal  and billjournal.bediener_nr != 0):
                            do_it = False

                        if exclude_artrans and billjournal.kassarapport:
                            do_it = False

                        if not mi_showrelease and billjournal.betrag == 0:
                            do_it = False

                        if do_it:
                            output_list = Output_list()
                            output_list_list.append(output_list)


                            if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                output_list.remark = billjournal.stornogrund

                            if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                                if billjournal.rechnr > 0:

                                    if billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                        bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                                        if bill and billjournal.zinr != "":

                                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, bill.zinr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                                            buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                                            if guest:
                                                output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                output_list.checkin = res_line.ankunft
                                                output_list.checkout = res_line.abreise
                                                output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                                                if segment:
                                                    output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.segcode = ""

                                        elif bill:

                                            if bill.resnr == 0 and bill.bilname != "":
                                                output_list.gname = bill.bilname
                                                output_list.guestname = bill.bilname
                                            else:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif billjournal.bediener_nr != 0 and mi_excljournal == False:

                                        h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                                        if h_bill:

                                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                                if res_line:

                                                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                    output_list.checkin = res_line.ankunft


                                                    output_list.checkout = res_line.abreise
                                                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                    output_list.gname = h_bill.bilname

                                                    if h_bill.bilname == "":

                                                        buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                                                        if buffguest:
                                                            output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                                                            output_list.guestname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                                                    genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})

                                                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                                                    if not segment:
                                                        output_list.segcode = ""
                                                    else:
                                                        output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                            elif h_bill.resnr > 0:

                                                guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                                if guest:
                                                    output_list.guestname = guest.name + "," + guest.vorname1
                                                    output_list.gname = h_bill.bilname


                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                                segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif h_bill.resnr == 0 and h_bill.bilname != "":
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                                segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif billjournal.betriebsnr == 0:

                                                bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                                                if bill:

                                                    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                                    if res_line:

                                                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                        output_list.checkin = res_line.ankunft


                                                        output_list.checkout = res_line.abreise
                                                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                        output_list.gname = bill.name

                                                        genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})

                                                        segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                                                        if not segment:
                                                            output_list.segcode = ""
                                                        else:
                                                            output_list.segcode = segment.bezeich
                                else:

                                    if artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                                        lviresnr = -1
                                        lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, "[#") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, " "))

                                        reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                        if reservation:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif get_index(billjournal.bezeich, " #") > 0 and billjournal.departement == 0:
                                        lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, " #") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, "]"))

                                        reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                        if reservation:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:

                                arrangement = get_cache (Arrangement, {"artnr_logis": [(eq, artikel.artnr)],"intervall": [(eq, artikel.departement)]})

                                if arrangement:

                                    h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.departement)]})

                                    if h_bill:

                                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                            if res_line:
                                                output_list.guestname = res_line.name
                                                output_list.gname = h_bill.bilname

                                                genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})

                                                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich
                                            else:
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                        elif h_bill.resnr > 0:

                                            guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                            if guest:
                                                output_list.guestname = guest.name + "," + guest.vorname1
                                                output_list.gname = h_bill.bilname


                                            else:
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                            segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                            if not segment:
                                                output_list.segcode = ""
                                            else:
                                                output_list.segcode = segment.bezeich

                                        elif h_bill.resnr == 0:
                                            output_list.guestname = h_bill.bilname
                                            output_list.gname = h_bill.bilname

                                            segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                            if not segment:
                                                output_list.segcode = ""
                                            else:
                                                output_list.segcode = segment.bezeich
                                else:

                                    argt_line = get_cache (Argt_line, {"argt_artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)]})

                                    if argt_line:
                                        hoteldept = billjournal.departement

                                        if matches(billjournal.bezeich, ("*<*")) and matches(billjournal.bezeich, ("*>*")):
                                            hoteldept = to_int(substring(billjournal.bezeich, get_index(billjournal.bezeich, "<") + 1 - 1, get_index(billjournal.bezeich, ">") - get_index(billjournal.bezeich, "<") - 1))

                                        h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, hoteldept)]})

                                        if h_bill:

                                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                                if res_line:

                                                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                    output_list.checkin = res_line.ankunft


                                                    output_list.checkout = res_line.abreise
                                                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                    output_list.gname = h_bill.bilname

                                                    genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})

                                                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                                                    if not segment:
                                                        output_list.segcode = ""
                                                    else:
                                                        output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                            elif h_bill.resnr > 0:

                                                guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                                if guest:
                                                    output_list.guestname = guest.name + "," + guest.vorname1
                                                    output_list.gname = h_bill.bilname


                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                                segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif h_bill.resnr == 0:
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                                segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                            if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                output_list.bezeich = artikel.bezeich

                            if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                output_list.shift = to_string(billjournal.betriebsnr, "99")
                                output_list.c = to_string(billjournal.betriebsnr, "99")

                            elif billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                if bill:

                                    if bill.reslinnr == 1 and bill.zinr == "":
                                        output_list.c = "N"
                                        output_list.ns = "*"

                                    elif bill.reslinnr == 0:
                                        output_list.c = "M"
                                        output_list.mb = "*"

                            if foreign_flag:
                                amount =  to_decimal(billjournal.fremdwaehrng)
                            else:
                                amount =  to_decimal(billjournal.betrag)

                            if mi_break :
                                serv =  to_decimal("0")
                                vat =  to_decimal("0")


                                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))
                                output_list.amt_nett =  to_decimal(amount) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                                output_list.service =  to_decimal(output_list.amt_nett) * to_decimal(serv)
                                output_list.vat =  to_decimal(output_list.amt_nett) * to_decimal(vat)
                                t_amt =  to_decimal(t_amt) + to_decimal(output_list.amt_nett)
                                t_vat =  to_decimal(t_vat) + to_decimal(output_list.vat)
                                t_service =  to_decimal(t_service) + to_decimal(output_list.service)
                                tot_amt =  to_decimal(tot_amt) + to_decimal(output_list.amt_nett)
                                tot_vat =  to_decimal(tot_vat) + to_decimal(output_list.vat)
                                tot_service =  to_decimal(tot_service) + to_decimal(output_list.service)


                            descr1 = ""
                            voucher_no = ""

                            if substring(billjournal.bezeich, 0, 1) == ("*").lower()  or billjournal.kassarapport:
                                descr1 = billjournal.bezeich
                                voucher_no = ""


                            else:

                                if not artikel.bezaendern:
                                    ind = num_entries(billjournal.bezeich, "]")

                                    if ind >= 2:
                                        gdelimiter = "]"
                                    else:
                                        ind = num_entries(billjournal.bezeich, "/")

                                        if ind >= 2 and length(artikel.bezeich) <= get_index(billjournal.bezeich, "/") and billjournal.betrag != 0:
                                            gdelimiter = "/"
                                        else:
                                            ind = num_entries(billjournal.bezeich, "|")

                                            if ind >= 2:
                                                gdelimiter = "|"

                                    if ind != 0:

                                        if ind == 1:
                                            descr1 = billjournal.bezeich
                                            voucher_no = ""

                                        elif ind == 2:
                                            descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                            voucher_no = entry(1, billjournal.bezeich, gdelimiter)

                                            if gdelimiter.lower()  == ("]").lower() :
                                                descr1 = descr1 + gdelimiter

                                        elif ind > 2:
                                            voucher_no = ""
                                            descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                            for loopind in range(2,ind + 1) :
                                                voucher_no = voucher_no + entry(loopind - 1, billjournal.bezeich, gdelimiter) + gdelimiter
                                            voucher_no = substring(voucher_no, 0, length(voucher_no) - 1)
                                    else:
                                        descr1 = billjournal.bezeich
                                else:
                                    ind = num_entries(billjournal.bezeich, "/")

                                    if ind == 1:
                                        descr1 = billjournal.bezeich
                                        voucher_no = ""

                                    elif ind == 2:
                                        descr1 = entry(0, billjournal.bezeich, "/")
                                        voucher_no = entry(1, billjournal.bezeich, "/")

                                    elif ind > 2:
                                        descr1 = entry(0, billjournal.bezeich, "/")
                                        for loopind in range(2,ind + 1) :
                                            voucher_no = voucher_no + entry(loopind - 1, billjournal.bezeich, "/") + "/"
                                        voucher_no = substring(voucher_no, 0, length(voucher_no) - 1)
                                    else:
                                        descr1 = billjournal.bezeich

                            if output_list:
                                output_list.descr = to_string(descr1, "x(100)")
                                output_list.voucher = to_string(voucher_no, "x(40)")

                            if billjournal.bediener_nr == 0 and mi_onlyjournal == False:
                                output_list.zinr = billjournal.zinr
                                output_list.deptno = billjournal.departement

                                if not long_digit:
                                    str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + billjournal.anzahl
                                gqty = gqty + billjournal.anzahl

                                if foreign_flag:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.fremdwaehrng)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.fremdwaehrng)
                                else:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

                            elif billjournal.bediener_nr != 0 and mi_excljournal == False:
                                output_list.zinr = billjournal.zinr
                                output_list.deptno = billjournal.departement

                                if not long_digit:
                                    str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + billjournal.anzahl
                                gqty = gqty + billjournal.anzahl

                                if foreign_flag:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.fremdwaehrng)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.fremdwaehrng)
                                else:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

                            if res_line and res_line.ankunft == res_line.abreise and artikel.departement > 0:
                                qty = qty - billjournal.anzahl + res_line.erwachs
                                gqty = gqty - billjournal.anzahl + res_line.erwachs
                                temp_str = substring(STR, 100)
                                str = substring(STR, 0, 95)
                                str = str + to_string(res_line.erwachs, "-9999") + temp_str
                                temp_str = ""


                elif sorttype == 2:

                    if mi_post :

                        for billjournal in db_session.query(Billjournal).filter(
                                 (Billjournal.artnr == artikel.artnr) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == curr_date) & (Billjournal.anzahl == 0)).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():
                            it_exist = True
                            do_it = True

                            if (mi_onlyjournal  and billjournal.bediener_nr == 0) or (mi_excljournal  and billjournal.bediener_nr != 0):
                                do_it = False

                            if exclude_artrans and billjournal.kassarapport:
                                do_it = False

                            if not mi_showrelease and billjournal.betrag == 0:
                                do_it = False

                            if do_it:
                                output_list = Output_list()
                                output_list_list.append(output_list)


                                if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                    output_list.remark = billjournal.stornogrund

                                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                                    if billjournal.rechnr > 0:

                                        bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                                        if bill and billjournal.zinr != "":

                                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, bill.zinr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                                            buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                                            if guest:
                                                output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                output_list.checkin = res_line.ankunft
                                                output_list.checkout = res_line.abreise
                                                output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                                                if segment:
                                                    output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.segcode = ""

                                        elif bill:

                                            if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):

                                                if bill.resnr == 0 and bill.bilname != "":
                                                    output_list.gname = bill.bilname
                                                    output_list.guestname = bill.bilname
                                                else:

                                                    gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                                    if gbuff:
                                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                        output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                    else:

                                        if artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                                            lviresnr = -1
                                            lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, "[#") + 2 - 1)
                                            lviresnr = to_int(entry(0, lvcs, " "))

                                            reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                            if reservation:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                        elif get_index(billjournal.bezeich, " #") > 0 and billjournal.departement == 0:
                                            lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, " #") + 2 - 1)
                                            lviresnr = to_int(entry(0, lvcs, "]"))

                                            reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                            if reservation:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                else:
                                    pass

                                if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                    output_list.bezeich = artikel.bezeich

                                if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                    output_list.shift = to_string(billjournal.betriebsnr, "99")
                                    output_list.c = to_string(billjournal.betriebsnr, "99")

                                elif billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                    if bill:

                                        if bill.reslinnr == 1 and bill.zinr == "":
                                            output_list.c = "N"
                                            output_list.ns = "*"

                                        elif bill.reslinnr == 0:
                                            output_list.c = "M"
                                            output_list.mb = "*"

                                if foreign_flag:
                                    amount =  to_decimal(billjournal.fremdwaehrng)
                                else:
                                    amount =  to_decimal(billjournal.betrag)

                                if mi_break :
                                    serv =  to_decimal("0")
                                    vat =  to_decimal("0")


                                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))
                                    output_list.amt_nett =  to_decimal(amount) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                                    output_list.service =  to_decimal(output_list.amt_nett) * to_decimal(serv)
                                    output_list.vat =  to_decimal(output_list.amt_nett) * to_decimal(vat)
                                    t_amt =  to_decimal(t_amt) + to_decimal(output_list.amt_nett)
                                    t_vat =  to_decimal(t_vat) + to_decimal(output_list.vat)
                                    t_service =  to_decimal(t_service) + to_decimal(output_list.service)
                                    tot_amt =  to_decimal(tot_amt) + to_decimal(output_list.amt_nett)
                                    tot_vat =  to_decimal(tot_vat) + to_decimal(output_list.vat)
                                    tot_service =  to_decimal(tot_service) + to_decimal(output_list.service)


                                descr1 = ""
                                voucher_no = ""

                                if substring(billjournal.bezeich, 0, 1) == ("*").lower()  or billjournal.kassarapport:
                                    descr1 = billjournal.bezeich
                                    voucher_no = ""


                                else:

                                    if not artikel.bezaendern:
                                        ind = num_entries(billjournal.bezeich, "]")

                                        if ind >= 2:
                                            gdelimiter = "]"
                                        else:
                                            ind = num_entries(billjournal.bezeich, "/")

                                            if ind >= 2 and length(artikel.bezeich) <= get_index(billjournal.bezeich, "/") and billjournal.betrag != 0:
                                                gdelimiter = "/"
                                            else:
                                                ind = num_entries(billjournal.bezeich, "|")

                                                if ind >= 2:
                                                    gdelimiter = "|"

                                        if ind != 0:

                                            if ind == 1:
                                                descr1 = billjournal.bezeich
                                                voucher_no = ""

                                            elif ind == 2:
                                                descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                                voucher_no = entry(1, billjournal.bezeich, gdelimiter)

                                                if gdelimiter.lower()  == ("]").lower() :
                                                    descr1 = descr1 + gdelimiter

                                            elif ind > 2:
                                                voucher_no = ""
                                                descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                                for loopind in range(2,ind + 1) :
                                                    voucher_no = voucher_no + entry(loopind - 1, billjournal.bezeich, gdelimiter) + gdelimiter
                                                voucher_no = substring(voucher_no, 0, length(voucher_no) - 1)
                                        else:
                                            descr1 = billjournal.bezeich
                                    else:
                                        ind = num_entries(billjournal.bezeich, "/")

                                        if ind == 1:
                                            descr1 = billjournal.bezeich
                                            voucher_no = ""

                                        elif ind == 2:
                                            descr1 = entry(0, billjournal.bezeich, "/")
                                            voucher_no = entry(1, billjournal.bezeich, "/")

                                        elif ind > 2:
                                            descr1 = entry(0, billjournal.bezeich, "/")
                                            for loopind in range(2,ind + 1) :
                                                voucher_no = voucher_no + entry(loopind - 1, billjournal.bezeich, "/") + "/"
                                            voucher_no = substring(voucher_no, 0, length(voucher_no) - 1)
                                        else:
                                            descr1 = billjournal.bezeich

                                if output_list:
                                    output_list.descr = to_string(descr1, "x(100)")
                                    output_list.voucher = to_string(voucher_no, "x(40)")

                                if billjournal.bediener_nr == 0 and mi_onlyjournal == False:
                                    output_list.zinr = billjournal.zinr
                                    output_list.deptno = billjournal.departement

                                    if not long_digit:
                                        str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    else:
                                        str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    qty = qty + billjournal.anzahl
                                    gqty = gqty + billjournal.anzahl

                                    if foreign_flag:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.fremdwaehrng)
                                        tot =  to_decimal(tot) + to_decimal(billjournal.fremdwaehrng)
                                    else:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                                        tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

                                elif billjournal.bediener_nr != 0 and mi_excljournal == False:
                                    output_list.zinr = billjournal.zinr
                                    output_list.deptno = billjournal.departement

                                    if not long_digit:
                                        str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    else:
                                        str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    qty = qty + billjournal.anzahl
                                    gqty = gqty + billjournal.anzahl

                                    if foreign_flag:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.fremdwaehrng)
                                        tot =  to_decimal(tot) + to_decimal(billjournal.fremdwaehrng)
                                    else:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                                        tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

                                if res_line and res_line.ankunft == res_line.abreise and artikel.departement > 0:
                                    qty = qty - billjournal.anzahl + res_line.erwachs
                                    gqty = gqty - billjournal.anzahl + res_line.erwachs
                                    temp_str = substring(STR, 100)
                                    str = substring(STR, 0, 95)
                                    str = str + to_string(res_line.erwachs, "-9999") + temp_str
                                    temp_str = ""

                    else:

                        for billjournal in db_session.query(Billjournal).filter(
                                 (Billjournal.artnr == artikel.artnr) & (Billjournal.departement == artikel.departement) & (Billjournal.sysdate == curr_date) & (Billjournal.anzahl == 0)).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():
                            it_exist = True
                            do_it = True

                            if (mi_onlyjournal  and billjournal.bediener_nr == 0) or (mi_excljournal  and billjournal.bediener_nr != 0):
                                do_it = False

                            if exclude_artrans and billjournal.kassarapport:
                                do_it = False

                            if not mi_showrelease and billjournal.betrag == 0:
                                do_it = False

                            if do_it:
                                output_list = Output_list()
                                output_list_list.append(output_list)


                                if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                    output_list.remark = billjournal.stornogrund

                                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                                    bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                                    if bill and billjournal.zinr != "":

                                        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, bill.zinr)],"ankunft": [(le, billjournal.bill_datum)],"abreise": [(ge, billjournal.bill_datum)]})

                                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                                        buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                                        if guest:
                                            output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                            output_list.checkin = res_line.ankunft
                                            output_list.checkout = res_line.abreise
                                            output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                            output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                                            if segment:
                                                output_list.segcode = segment.bezeich
                                            else:
                                                output_list.segcode = ""

                                    elif bill:

                                        if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):

                                            if bill.resnr == 0 and bill.bilname != "":
                                                output_list.gname = bill.bilname
                                                output_list.guestname = bill.bilname
                                            else:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                    output_list.bezeich = artikel.bezeich

                                if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                    output_list.shift = to_string(billjournal.betriebsnr, "99")
                                    output_list.c = to_string(billjournal.betriebsnr, "99")

                                elif billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                    if bill:

                                        if bill.reslinnr == 1 and bill.zinr == "":
                                            output_list.ns = "*"
                                            output_list.c = "N"

                                        elif bill.reslinnr == 0:
                                            output_list.c = "M"
                                            output_list.mb = "*"

                                if foreign_flag:
                                    amount =  to_decimal(billjournal.fremdwaehrng)
                                else:
                                    amount =  to_decimal(billjournal.betrag)

                                if mi_break :
                                    serv =  to_decimal("0")
                                    vat =  to_decimal("0")


                                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))
                                    output_list.amt_nett =  to_decimal(amount) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                                    output_list.service =  to_decimal(output_list.amt_nett) * to_decimal(serv)
                                    output_list.vat =  to_decimal(output_list.amt_nett) * to_decimal(vat)
                                    t_amt =  to_decimal(t_amt) + to_decimal(output_list.amt_nett)
                                    t_vat =  to_decimal(t_vat) + to_decimal(output_list.vat)
                                    t_service =  to_decimal(t_service) + to_decimal(output_list.service)
                                    tot_amt =  to_decimal(tot_amt) + to_decimal(output_list.amt_nett)
                                    tot_vat =  to_decimal(tot_vat) + to_decimal(output_list.vat)
                                    tot_service =  to_decimal(tot_service) + to_decimal(output_list.service)


                                descr1 = ""
                                voucher_no = ""

                                if substring(billjournal.bezeich, 0, 1) == ("*").lower()  or billjournal.kassarapport:
                                    descr1 = billjournal.bezeich
                                    voucher_no = ""


                                else:

                                    if not artikel.bezaendern:
                                        ind = num_entries(billjournal.bezeich, "]")

                                        if ind >= 2:
                                            gdelimiter = "]"
                                        else:
                                            ind = num_entries(billjournal.bezeich, "/")

                                            if ind >= 2 and length(artikel.bezeich) <= get_index(billjournal.bezeich, "/") and billjournal.betrag != 0:
                                                gdelimiter = "/"
                                            else:
                                                ind = num_entries(billjournal.bezeich, "|")

                                                if ind >= 2:
                                                    gdelimiter = "|"

                                        if ind != 0:

                                            if ind == 1:
                                                descr1 = billjournal.bezeich
                                                voucher_no = ""

                                            elif ind == 2:
                                                descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                                voucher_no = entry(1, billjournal.bezeich, gdelimiter)

                                                if gdelimiter.lower()  == ("]").lower() :
                                                    descr1 = descr1 + gdelimiter

                                            elif ind > 2:
                                                voucher_no = ""
                                                descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                                for loopind in range(2,ind + 1) :
                                                    voucher_no = voucher_no + entry(loopind - 1, billjournal.bezeich, gdelimiter) + gdelimiter
                                                voucher_no = substring(voucher_no, 0, length(voucher_no) - 1)
                                        else:
                                            descr1 = billjournal.bezeich
                                    else:
                                        ind = num_entries(billjournal.bezeich, "/")

                                        if ind == 1:
                                            descr1 = billjournal.bezeich
                                            voucher_no = ""

                                        elif ind == 2:
                                            descr1 = entry(0, billjournal.bezeich, "/")
                                            voucher_no = entry(1, billjournal.bezeich, "/")

                                        elif ind > 2:
                                            descr1 = entry(0, billjournal.bezeich, "/")
                                            for loopind in range(2,ind + 1) :
                                                voucher_no = voucher_no + entry(loopind - 1, billjournal.bezeich, "/") + "/"
                                            voucher_no = substring(voucher_no, 0, length(voucher_no) - 1)
                                        else:
                                            descr1 = billjournal.bezeich

                                if output_list:
                                    output_list.descr = to_string(descr1, "x(100)")
                                    output_list.voucher = to_string(voucher_no, "x(40)")

                                if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                    output_list.zinr = billjournal.zinr
                                    output_list.deptno = billjournal.departement

                                    if not long_digit:
                                        str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                                    else:
                                        str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                                    qty = qty + billjournal.anzahl
                                    gqty = gqty + billjournal.anzahl

                                    if foreign_flag:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.fremdwaehrng)
                                        tot =  to_decimal(tot) + to_decimal(billjournal.fremdwaehrng)
                                    else:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                                        tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

                                elif billjournal.bediener_nr != 0 and mi_excljournal == False:
                                    output_list.zinr = billjournal.zinr
                                    output_list.deptno = billjournal.departement

                                    if not long_digit:
                                        str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                                    else:
                                        str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                                    qty = qty + billjournal.anzahl
                                    gqty = gqty + billjournal.anzahl

                                    if foreign_flag:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.fremdwaehrng)
                                        tot =  to_decimal(tot) + to_decimal(billjournal.fremdwaehrng)
                                    else:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                                        tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

                                if res_line and res_line.ankunft == res_line.abreise and artikel.departement > 0:
                                    qty = qty - billjournal.anzahl + res_line.erwachs
                                    gqty = gqty - billjournal.anzahl + res_line.erwachs
                                    temp_str = substring(STR, 100)
                                    str = substring(STR, 0, 95)
                                    str = str + to_string(res_line.erwachs, "-9999") + temp_str
                                    temp_str = ""


            if it_exist and qty != 0:
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    str = to_string("", "x(77)") + to_string("T O T A L ", "x(12)") + to_string("", "x(6)") + to_string(qty, "-9999") + to_string(sub_tot, "->>,>>>,>>>,>>>,>>9.99")
                    output_list.amt_nett =  to_decimal(t_amt)
                    output_list.service =  to_decimal(t_service)
                    output_list.vat =  to_decimal(t_vat)
                    t_amt =  to_decimal("0")
                    t_service =  to_decimal("0")
                    t_vat =  to_decimal("0")
                else:
                    str = to_string("", "x(77)") + to_string("T O T A L ", "x(12)") + to_string("", "x(6)") + to_string(qty, "-9999") + to_string(sub_tot, "->,>>>,>>>,>>>,>>>,>>9")
                    output_list.amt_nett =  to_decimal(t_amt)
                    output_list.service =  to_decimal(t_service)
                    output_list.vat =  to_decimal(t_vat)
                    t_amt =  to_decimal("0")
                    t_service =  to_decimal("0")
                    t_vat =  to_decimal("0")
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            str = to_string("", "x(77)") +\
                    to_string("Grand TOTAL ", "x(12)") +\
                    to_string("", "x(6)") +\
                    to_string(gqty, "-9999") +\
                    to_string(tot, "->>,>>>,>>>,>>>,>>9.99")
            output_list.amt_nett =  to_decimal(tot_amt)
            output_list.service =  to_decimal(tot_service)
            output_list.vat =  to_decimal(tot_vat)


        else:
            str = to_string("", "x(77)") +\
                    to_string("Grand TOTAL ", "x(12)") +\
                    to_string("", "x(6)") +\
                    to_string(gqty, "-9999") +\
                    to_string(tot, "->,>>>,>>>,>>>,>>>,>>9")
            output_list.amt_nett =  to_decimal(tot_amt)
            output_list.service =  to_decimal(tot_service)
            output_list.vat =  to_decimal(tot_vat)


        gtot =  to_decimal(tot)


    if from_date == None:

        return generate_output()

    if to_date == None:

        return generate_output()
    journal_list()
    custom_record()

    return generate_output()