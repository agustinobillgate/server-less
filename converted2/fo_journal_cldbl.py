#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from models import Billjournal, Guest, Artikel, Hoteldpt, Bill, H_bill, Bk_veran, Reservation, Arrangement, Res_line, Genstat, Segment, Argt_line

def fo_journal_cldbl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, sorttype:int, exclude_artrans:bool, long_digit:bool, foreign_flag:bool, mi_onlyjournal:bool, mi_excljournal:bool, mi_post:bool, mi_showrelease:bool):

    prepare_cache ([Guest, Artikel, Hoteldpt, Bill, H_bill, Bk_veran, Reservation, Res_line, Genstat, Segment])

    gtot = to_decimal("0.0")
    output_list_data = []
    curr_date:date = None
    descr1:string = ""
    voucher_no:string = ""
    ind:int = 0
    gdelimiter:string = ""
    roomnumber:string = ""
    zinrdate:date = None
    billnumber:int = 0
    curr_str:string = ""
    curr_resnr:int = 0
    lvcs:string = ""
    billjournal = guest = artikel = hoteldpt = bill = h_bill = bk_veran = reservation = arrangement = res_line = genstat = segment = argt_line = None

    output_list = t_billjournal = None

    output_list_data, Output_list = create_model("Output_list", {"bezeich":string, "c":string, "ns":string, "mb":string, "shift":string, "dept":string, "str":string, "remark":string, "gname":string, "descr":string, "voucher":string, "checkin":date, "checkout":date, "guestname":string, "segcode":string})
    t_billjournal_data, T_billjournal = create_model_like(Billjournal)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gtot, output_list_data, curr_date, descr1, voucher_no, ind, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, lvcs, billjournal, guest, artikel, hoteldpt, bill, h_bill, bk_veran, reservation, arrangement, res_line, genstat, segment, argt_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease


        nonlocal output_list, t_billjournal
        nonlocal output_list_data, t_billjournal_data

        return {"gtot": gtot, "output-list": output_list_data}

    def journal_list():

        nonlocal gtot, output_list_data, descr1, voucher_no, ind, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, billjournal, guest, artikel, hoteldpt, bill, h_bill, bk_veran, reservation, arrangement, res_line, genstat, segment, argt_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease


        nonlocal output_list, t_billjournal
        nonlocal output_list_data, t_billjournal_data

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
        gbuff = None
        Gbuff =  create_buffer("Gbuff",Guest)
        output_list_data.clear()

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

                    for t_billjournal in query(t_billjournal_data, filters=(lambda t_billjournal: t_billjournal.artnr == artikel.artnr and t_billjournal.departement == artikel.departement and bill_datum == curr_date and t_billjournal.anzahl != 0), sort_by=[("sysdate",False),("zeit",False),("zinr",False)]):
                        it_exist = True
                        do_it = True

                        if exclude_artrans and t_billjournal.kassarapport:
                            do_it = False

                        if not mi_showrelease and t_billjournal.betrag == 0:
                            do_it = False

                        if do_it:

                            if (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False) or (t_billjournal.bediener_nr != 0 and mi_excljournal == False):
                                output_list = Output_list()
                                output_list_data.append(output_list)

                                output_list.remark = t_billjournal.stornogrund

                            if not matches(t_billjournal.bezeich, ("*<*")) and not matches(t_billjournal.bezeich, ("*>*")):

                                if t_billjournal.rechnr > 0:

                                    if t_billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                        bill = get_cache (Bill, {"rechnr": [(eq, t_billjournal.rechnr)]})

                                        if bill:

                                            if bill.resnr == 0 and bill.bilname != "":
                                                output_list.gname = bill.bilname
                                            else:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif t_billjournal.bediener_nr != 0 and mi_excljournal == False:

                                        h_bill = get_cache (H_bill, {"rechnr": [(eq, t_billjournal.rechnr)],"departement": [(eq, t_billjournal.betriebsnr)]})

                                        if h_bill:
                                            output_list.gname = h_bill.bilname
                                else:

                                    if get_index(t_billjournal.bezeich, " *BQT") > 0:

                                        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, to_int(substring(t_billjournal.bezeich, get_index(t_billjournal.bezeich, " *bqt") + 5  - 1)))]})

                                        if bk_veran:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif artikel.artart == 5 and get_index(t_billjournal.bezeich, " [#") > 0 and t_billjournal.departement == 0:
                                        lviresnr = -1
                                        lvcs = substring(t_billjournal.bezeich, get_index(t_billjournal.bezeich, "[#") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, " "))

                                        reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                        if reservation:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif get_index(t_billjournal.bezeich, " #") > 0 and t_billjournal.departement == 0:
                                        lvcs = substring(t_billjournal.bezeich, get_index(t_billjournal.bezeich, " #") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, "]"))

                                        reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                        if reservation:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:

                                arrangement = get_cache (Arrangement, {"artnr_logis": [(eq, artikel.artnr)],"intervall": [(eq, artikel.departement)]})

                                if arrangement:

                                    h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.departement)]})

                                    if h_bill:

                                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                            if res_line:
                                                output_list.guestname = res_line.name
                                                output_list.gname = h_bill.bilname

                                                genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})

                                                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                        elif h_bill.resnr > 0:

                                            guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                            if guest:
                                                output_list.guestname = guest.name + "," + guest.vorname1
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

                                        h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.departement)]})

                                        if h_bill:

                                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                                if res_line:
                                                    output_list.guestname = res_line.name
                                                    output_list.gname = h_bill.bilname

                                                    genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})

                                                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                                                    if not segment:
                                                        output_list.segcode = ""
                                                    else:
                                                        output_list.segcode = segment.bezeich

                                            elif h_bill.resnr > 0:

                                                guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                                if guest:
                                                    output_list.guestname = guest.name + "," + guest.vorname1
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

                            if (t_billjournal.bediener_nr != 0 and mi_excljournal == False and t_billjournal.anzahl == 0) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False and t_billjournal.anzahl == 0):
                                output_list.bezeich = artikel.bezeich

                            if t_billjournal.bediener_nr != 0 and mi_excljournal == False:
                                output_list.c = to_string(t_billjournal.betriebsnr, "99")
                                output_list.shift = to_string(t_billjournal.betriebsnr, "99")

                            elif t_billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                if bill:

                                    if bill.reslinnr == 1 and bill.zinr == "":
                                        output_list.c = "N"
                                        output_list.ns = "*"

                                    elif bill.reslinnr == 0:
                                        output_list.c = "M"
                                        output_list.mb = "*"

                            if foreign_flag:
                                amount =  to_decimal(t_billjournal.fremdwaehrng)
                            else:
                                amount =  to_decimal(t_billjournal.betrag)
                            descr1 = ""
                            voucher_no = ""

                            if substring(t_billjournal.bezeich, 0, 1) == ("*").lower()  or t_billjournal.kassarapport:
                                descr1 = t_billjournal.bezeich
                                voucher_no = ""


                            else:

                                if not artikel.bezaendern:
                                    ind = get_index(t_billjournal.bezeich, "/")

                                    if ind != 0:
                                        gdelimiter = "/"
                                    else:
                                        ind = get_index(t_billjournal.bezeich, "]")

                                        if ind != 0:
                                            gdelimiter = "]"

                                    if ind != 0:

                                        if ind > length(artikel.bezeich):
                                            descr1 = entry(0, t_billjournal.bezeich, gdelimiter)
                                            voucher_no = substring(t_billjournal.bezeich, (ind + 1) - 1)


                                        else:
                                            cnt = num_entries(artikel.bezeich, gdelimiter)
                                            for i in range(1,cnt + 1) :

                                                if descr1 == "":
                                                    descr1 = entry(i - 1, t_billjournal.bezeich, gdelimiter)
                                                else:
                                                    descr1 = descr1 + "/" + entry(i - 1, t_billjournal.bezeich, gdelimiter)
                                            voucher_no = substring(t_billjournal.bezeich, length(descr1) + 2 - 1)

                                        if gdelimiter.lower()  == ("]").lower() :
                                            descr1 = descr1 + gdelimiter
                                    else:
                                        descr1 = t_billjournal.bezeich
                                else:
                                    ind = get_index(t_billjournal.bezeich, "/")

                                    if ind != 0:
                                        gdelimiter = "/"
                                    else:
                                        ind = get_index(t_billjournal.bezeich, "]")

                                        if ind != 0:
                                            gdelimiter = "]"

                                    if ind != 0:

                                        if ind > length(artikel.bezeich):
                                            descr1 = entry(0, t_billjournal.bezeich, gdelimiter)
                                            voucher_no = substring(t_billjournal.bezeich, (ind + 1) - 1)


                                        else:
                                            cnt = num_entries(artikel.bezeich, gdelimiter)

                                            if cnt > num_entries(t_billjournal.bezeich, gdelimiter):

                                                if num_entries(t_billjournal.bezeich, gdelimiter) > 1:
                                                    cnt = num_entries(t_billjournal.bezeich, gdelimiter) - 1
                                                else:
                                                    cnt = num_entries(t_billjournal.bezeich, gdelimiter)
                                            for i in range(1,cnt + 1) :

                                                if descr1 == "":
                                                    descr1 = entry(i - 1, t_billjournal.bezeich, gdelimiter)
                                                else:
                                                    descr1 = descr1 + "/" + entry(i - 1, t_billjournal.bezeich, gdelimiter)
                                            voucher_no = substring(t_billjournal.bezeich, length(descr1) + 2 - 1)

                                        if gdelimiter.lower()  == ("]").lower() :
                                            descr1 = descr1 + gdelimiter
                                    else:
                                        descr1 = t_billjournal.bezeich

                            if output_list:
                                output_list.descr = to_string(descr1, "x(100)")
                                output_list.voucher = to_string(voucher_no, "x(20)")

                            if t_billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, t_billjournal.departement)]})

                                if hoteldpt:
                                    deptname = hoteldpt.depart

                                if not long_digit:
                                    str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(deptname, "x(12)") + to_string("", "x(6)") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(t_billjournal.bezeich, "x(50)") + to_string(deptname, "x(12)") + to_string("", "x(6)") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + t_billjournal.anzahl
                                gqty = gqty + t_billjournal.anzahl

                                if foreign_flag:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.fremdwaehrng)
                                    tot =  to_decimal(tot) + to_decimal(t_billjournal.fremdwaehrng)
                                else:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.betrag)
                                    tot =  to_decimal(tot) + to_decimal(t_billjournal.betrag)

                            elif t_billjournal.bediener_nr != 0 and mi_excljournal == False:

                                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, t_billjournal.departement)]})

                                if hoteldpt:
                                    deptname = hoteldpt.depart

                                if not long_digit:
                                    str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(deptname, "x(12)") + to_string(t_billjournal.betriebsnr, ">>>>>>") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(t_billjournal.bezeich, "x(50)") + to_string(deptname, "x(12)") + to_string(t_billjournal.betriebsnr, ">>>>>>") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + t_billjournal.anzahl
                                gqty = gqty + t_billjournal.anzahl

                                if foreign_flag:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.fremdwaehrng)
                                    tot =  to_decimal(tot) + to_decimal(t_billjournal.fremdwaehrng)
                                else:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.betrag)
                                    tot =  to_decimal(tot) + to_decimal(t_billjournal.betrag)
                        add_field()


                elif sorttype == 1:

                    for t_billjournal in query(t_billjournal_data, filters=(lambda t_billjournal: t_billjournal.artnr == artikel.artnr and t_billjournal.departement == artikel.departement and t_billjournal.bill_datum == curr_date), sort_by=[("sysdate",False),("zeit",False),("zinr",False)]):
                        it_exist = True
                        do_it = True

                        if exclude_artrans and t_billjournal.kassarapport:
                            do_it = False

                        if not mi_showrelease and t_billjournal.betrag == 0:
                            do_it = False

                        if do_it:

                            if (t_billjournal.bediener_nr != 0 and mi_excljournal == False) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                output_list = Output_list()
                                output_list_data.append(output_list)

                                output_list.remark = t_billjournal.stornogrund

                            if not matches(t_billjournal.bezeich, ("*<*")) and not matches(t_billjournal.bezeich, ("*>*")):

                                if t_billjournal.rechnr > 0:

                                    bill = get_cache (Bill, {"rechnr": [(eq, t_billjournal.rechnr)]})

                                    if bill:

                                        if (t_billjournal.bediener_nr != 0 and mi_excljournal == False) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False):

                                            if bill.resnr == 0 and bill.bilname != "":
                                                output_list.gname = bill.bilname
                                            else:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                else:

                                    if artikel.artart == 5 and get_index(t_billjournal.bezeich, " [#") > 0 and t_billjournal.departement == 0:
                                        lviresnr = -1
                                        lvcs = substring(t_billjournal.bezeich, get_index(t_billjournal.bezeich, "[#") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, " "))

                                        reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                        if reservation:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                    elif get_index(t_billjournal.bezeich, " #") > 0 and t_billjournal.departement == 0:
                                        lvcs = substring(t_billjournal.bezeich, get_index(t_billjournal.bezeich, " #") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, "]"))

                                        reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                        if reservation:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                pass

                            if (t_billjournal.bediener_nr != 0 and mi_excljournal == False and t_billjournal.anzahl == 0) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False and t_billjournal.anzahl == 0):
                                output_list.bezeich = artikel.bezeich

                            if t_billjournal.bediener_nr != 0 and mi_excljournal == False:
                                output_list.shift = to_string(t_billjournal.betriebsnr, "99")
                                output_list.c = to_string(t_billjournal.betriebsnr, "99")

                            elif t_billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                if bill:

                                    if bill.reslinnr == 1 and bill.zinr == "":
                                        output_list.c = "N"
                                        output_list.ns = "*"

                                    elif bill.reslinnr == 0:
                                        output_list.c = "M"
                                        output_list.mb = "*"

                            if foreign_flag:
                                amount =  to_decimal(t_billjournal.fremdwaehrng)
                            else:
                                amount =  to_decimal(t_billjournal.betrag)
                            descr1 = ""
                            voucher_no = ""

                            if substring(t_billjournal.bezeich, 0, 1) == ("*").lower()  or t_billjournal.kassarapport:
                                descr1 = t_billjournal.bezeich
                                voucher_no = ""


                            else:

                                if not artikel.bezaendern:
                                    ind = get_index(t_billjournal.bezeich, "/")

                                    if ind != 0:
                                        gdelimiter = "/"
                                    else:
                                        ind = get_index(t_billjournal.bezeich, "]")

                                        if ind != 0:
                                            gdelimiter = "]"

                                    if ind != 0:

                                        if ind > length(artikel.bezeich):
                                            descr1 = entry(0, t_billjournal.bezeich, gdelimiter)
                                            voucher_no = substring(t_billjournal.bezeich, (ind + 1) - 1)


                                        else:
                                            cnt = num_entries(artikel.bezeich, gdelimiter)
                                            for i in range(1,cnt + 1) :

                                                if descr1 == "":
                                                    descr1 = entry(i - 1, t_billjournal.bezeich, gdelimiter)
                                                else:
                                                    descr1 = descr1 + "/" + entry(i - 1, t_billjournal.bezeich, gdelimiter)
                                            voucher_no = substring(t_billjournal.bezeich, length(descr1) + 2 - 1)

                                        if gdelimiter.lower()  == ("]").lower() :
                                            descr1 = descr1 + gdelimiter
                                    else:
                                        descr1 = t_billjournal.bezeich
                                else:
                                    ind = num_entries(t_billjournal.bezeich, "/")

                                    if ind <= 1:
                                        descr1 = t_billjournal.bezeich
                                        voucher_no = ""


                                    else:
                                        descr1 = entry(0, t_billjournal.bezeich, "/")
                                        voucher_no = entry(1, t_billjournal.bezeich, "/")

                                    if descr1 == "" or descr1 == " ":
                                        descr1 = artikel.bezeich

                            if output_list:
                                output_list.descr = to_string(descr1, "x(100)")
                                output_list.voucher = to_string(voucher_no, "x(20)")

                            if t_billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                if not long_digit:
                                    str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + t_billjournal.anzahl
                                gqty = gqty + t_billjournal.anzahl

                                if foreign_flag:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.fremdwaehrng)
                                    tot =  to_decimal(tot) + to_decimal(t_billjournal.fremdwaehrng)
                                else:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.betrag)
                                    tot =  to_decimal(tot) + to_decimal(t_billjournal.betrag)

                            elif t_billjournal.bediener_nr != 0 and mi_excljournal == False:

                                if not long_digit:
                                    str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(t_billjournal.betriebsnr, ">>>>>>") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                else:
                                    str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(t_billjournal.betriebsnr, ">>>>>>") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>>,>>9") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                qty = qty + t_billjournal.anzahl
                                gqty = gqty + t_billjournal.anzahl

                                if foreign_flag:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.fremdwaehrng)
                                    tot =  to_decimal(tot) + to_decimal(t_billjournal.fremdwaehrng)
                                else:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.betrag)
                                    tot =  to_decimal(tot) + to_decimal(t_billjournal.betrag)
                        add_field()


                elif sorttype == 2:

                    if mi_post :

                        for t_billjournal in query(t_billjournal_data, filters=(lambda t_billjournal: t_billjournal.artnr == artikel.artnr and t_billjournal.departement == artikel.departement and t_billjournal.bill_datum == curr_date and t_billjournal.anzahl == 0), sort_by=[("sysdate",False),("zeit",False),("zinr",False)]):
                            it_exist = True
                            do_it = True

                            if exclude_artrans and t_billjournal.kassarapport:
                                do_it = False

                            if not mi_showrelease and t_billjournal.betrag == 0:
                                do_it = False

                            if do_it:

                                if (t_billjournal.bediener_nr != 0 and mi_excljournal == False) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                    output_list = Output_list()
                                    output_list_data.append(output_list)

                                    output_list.remark = t_billjournal.stornogrund

                                if not matches(t_billjournal.bezeich, ("*<*")) and not matches(t_billjournal.bezeich, ("*>*")):

                                    if t_billjournal.rechnr > 0:

                                        bill = get_cache (Bill, {"rechnr": [(eq, t_billjournal.rechnr)]})

                                        if bill:

                                            if (t_billjournal.bediener_nr != 0 and mi_excljournal == False) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False):

                                                if bill.resnr == 0 and bill.bilname != "":
                                                    output_list.gname = bill.bilname
                                                else:

                                                    gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                                    if gbuff:
                                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                    else:

                                        if artikel.artart == 5 and get_index(t_billjournal.bezeich, " [#") > 0 and t_billjournal.departement == 0:
                                            lviresnr = -1
                                            lvcs = substring(t_billjournal.bezeich, get_index(t_billjournal.bezeich, "[#") + 2 - 1)
                                            lviresnr = to_int(entry(0, lvcs, " "))

                                            reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                            if reservation:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                        elif get_index(t_billjournal.bezeich, " #") > 0 and t_billjournal.departement == 0:
                                            lvcs = substring(t_billjournal.bezeich, get_index(t_billjournal.bezeich, " #") + 2 - 1)
                                            lviresnr = to_int(entry(0, lvcs, "]"))

                                            reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                            if reservation:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                else:
                                    pass

                                if (t_billjournal.bediener_nr != 0 and mi_excljournal == False and t_billjournal.anzahl == 0) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False and t_billjournal.anzahl == 0):
                                    output_list.bezeich = artikel.bezeich

                                if t_billjournal.bediener_nr != 0 and mi_excljournal == False:
                                    output_list.shift = to_string(t_billjournal.betriebsnr, "99")
                                    output_list.c = to_string(t_billjournal.betriebsnr, "99")

                                elif t_billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                    if bill:

                                        if bill.reslinnr == 1 and bill.zinr == "":
                                            output_list.c = "N"
                                            output_list.ns = "*"

                                        elif bill.reslinnr == 0:
                                            output_list.c = "M"
                                            output_list.mb = "*"

                                if foreign_flag:
                                    amount =  to_decimal(t_billjournal.fremdwaehrng)
                                else:
                                    amount =  to_decimal(t_billjournal.betrag)
                                descr1 = ""
                                voucher_no = ""

                                if substring(t_billjournal.bezeich, 0, 1) == ("*").lower()  or t_billjournal.kassarapport:
                                    descr1 = t_billjournal.bezeich
                                    voucher_no = ""


                                else:

                                    if not artikel.bezaendern:
                                        ind = get_index(t_billjournal.bezeich, "/")

                                        if ind != 0:
                                            gdelimiter = "/"
                                        else:
                                            ind = get_index(t_billjournal.bezeich, "]")

                                            if ind != 0:
                                                gdelimiter = "]"

                                        if ind != 0:

                                            if ind > length(artikel.bezeich):
                                                descr1 = entry(0, t_billjournal.bezeich, gdelimiter)
                                                voucher_no = substring(t_billjournal.bezeich, (ind + 1) - 1)


                                            else:
                                                cnt = num_entries(artikel.bezeich, gdelimiter)
                                                for i in range(1,cnt + 1) :

                                                    if descr1 == "":
                                                        descr1 = entry(i - 1, t_billjournal.bezeich, gdelimiter)
                                                    else:
                                                        descr1 = descr1 + "/" + entry(i - 1, t_billjournal.bezeich, gdelimiter)
                                                voucher_no = substring(t_billjournal.bezeich, length(descr1) + 2 - 1)

                                            if gdelimiter.lower()  == ("]").lower() :
                                                descr1 = descr1 + gdelimiter
                                        else:
                                            descr1 = t_billjournal.bezeich
                                    else:
                                        ind = num_entries(t_billjournal.bezeich, "/")

                                        if ind <= 1:
                                            descr1 = t_billjournal.bezeich
                                            voucher_no = ""


                                        else:
                                            descr1 = entry(0, t_billjournal.bezeich, "/")
                                            voucher_no = entry(1, t_billjournal.bezeich, "/")

                                        if descr1 == "" or descr1 == " ":
                                            descr1 = artikel.bezeich

                                if output_list:
                                    output_list.descr = to_string(descr1, "x(100)")
                                    output_list.voucher = to_string(voucher_no, "x(20)")

                                if t_billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                    if not long_digit:
                                        str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    else:
                                        str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    qty = qty + t_billjournal.anzahl
                                    gqty = gqty + t_billjournal.anzahl

                                    if foreign_flag:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.fremdwaehrng)
                                        tot =  to_decimal(tot) + to_decimal(t_billjournal.fremdwaehrng)
                                    else:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.betrag)
                                        tot =  to_decimal(tot) + to_decimal(t_billjournal.betrag)

                                elif t_billjournal.bediener_nr != 0 and mi_excljournal == False:

                                    if not long_digit:
                                        str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(t_billjournal.betriebsnr, ">>>>>>") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    else:
                                        str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(descr1, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(t_billjournal.betriebsnr, ">>>>>>") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate) + to_string(voucher_no, "x(24)")
                                    qty = qty + t_billjournal.anzahl
                                    gqty = gqty + t_billjournal.anzahl

                                    if foreign_flag:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.fremdwaehrng)
                                        tot =  to_decimal(tot) + to_decimal(t_billjournal.fremdwaehrng)
                                    else:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.betrag)
                                        tot =  to_decimal(tot) + to_decimal(t_billjournal.betrag)
                            add_field()

                    else:

                        for t_billjournal in query(t_billjournal_data, filters=(lambda t_billjournal: t_billjournal.artnr == artikel.artnr and t_billjournal.departement == artikel.departement and t_billjournal.sysdate == curr_date and t_billjournal.anzahl == 0), sort_by=[("sysdate",False),("zeit",False),("zinr",False)]):
                            it_exist = True
                            do_it = True

                            if exclude_artrans and t_billjournal.kassarapport:
                                do_it = False

                            if not mi_showrelease and t_billjournal.betrag == 0:
                                do_it = False

                            if do_it:

                                if (t_billjournal.bediener_nr != 0 and mi_excljournal == False) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                    output_list = Output_list()
                                    output_list_data.append(output_list)

                                    output_list.remark = t_billjournal.stornogrund

                                if not matches(t_billjournal.bezeich, ("*<*")) and not matches(t_billjournal.bezeich, ("*>*")):

                                    bill = get_cache (Bill, {"rechnr": [(eq, t_billjournal.rechnr)]})

                                    if bill:

                                        if (t_billjournal.bediener_nr != 0 and mi_excljournal == False) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False):

                                            if bill.resnr == 0 and bill.bilname != "":
                                                output_list.gname = bill.bilname
                                            else:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                else:
                                    pass

                                if (t_billjournal.bediener_nr != 0 and mi_excljournal == False and t_billjournal.anzahl == 0) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False and t_billjournal.anzahl == 0):
                                    output_list.bezeich = artikel.bezeich

                                if t_billjournal.bediener_nr != 0 and mi_excljournal == False:
                                    output_list.shift = to_string(t_billjournal.betriebsnr, "99")
                                    output_list.c = to_string(t_billjournal.betriebsnr, "99")

                                elif t_billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                    if bill:

                                        if bill.reslinnr == 1 and bill.zinr == "":
                                            output_list.ns = "*"
                                            output_list.c = "N"

                                        elif bill.reslinnr == 0:
                                            output_list.c = "M"
                                            output_list.mb = "*"

                                if foreign_flag:
                                    amount =  to_decimal(t_billjournal.fremdwaehrng)
                                else:
                                    amount =  to_decimal(t_billjournal.betrag)
                                descr1 = ""
                                voucher_no = ""

                                if substring(t_billjournal.bezeich, 0, 1) == ("*").lower()  or t_billjournal.kassarapport:
                                    descr1 = t_billjournal.bezeich
                                    voucher_no = ""


                                else:

                                    if not artikel.bezaendern:
                                        ind = get_index(t_billjournal.bezeich, "/")

                                        if ind != 0:
                                            gdelimiter = "/"
                                        else:
                                            ind = get_index(t_billjournal.bezeich, "]")

                                            if ind != 0:
                                                gdelimiter = "]"

                                        if ind != 0:

                                            if ind > length(artikel.bezeich):
                                                descr1 = entry(0, t_billjournal.bezeich, gdelimiter)
                                                voucher_no = substring(t_billjournal.bezeich, (ind + 1) - 1)


                                            else:
                                                cnt = num_entries(artikel.bezeich, gdelimiter)
                                                for i in range(1,cnt + 1) :

                                                    if descr1 == "":
                                                        descr1 = entry(i - 1, t_billjournal.bezeich, gdelimiter)
                                                    else:
                                                        descr1 = descr1 + "/" + entry(i - 1, t_billjournal.bezeich, gdelimiter)
                                                voucher_no = substring(t_billjournal.bezeich, length(descr1) + 2 - 1)

                                            if gdelimiter.lower()  == ("]").lower() :
                                                descr1 = descr1 + gdelimiter
                                        else:
                                            descr1 = t_billjournal.bezeich
                                    else:
                                        ind = num_entries(t_billjournal.bezeich, "/")

                                        if ind <= 1:
                                            descr1 = t_billjournal.bezeich
                                            voucher_no = ""


                                        else:
                                            descr1 = entry(0, t_billjournal.bezeich, "/")
                                            voucher_no = entry(1, t_billjournal.bezeich, "/")

                                        if descr1 == "" or descr1 == " ":
                                            descr1 = artikel.bezeich

                                if output_list:
                                    output_list.descr = to_string(descr1, "x(100)")
                                    output_list.voucher = to_string(voucher_no, "x(20)")

                                if (t_billjournal.bediener_nr != 0 and mi_excljournal == False) or (t_billjournal.bediener_nr == 0 and mi_onlyjournal == False):

                                    if not long_digit:
                                        str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(t_billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate)
                                    else:
                                        str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(t_billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string("", "x(6)") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate)
                                    qty = qty + t_billjournal.anzahl
                                    gqty = gqty + t_billjournal.anzahl

                                    if foreign_flag:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.fremdwaehrng)
                                        tot =  to_decimal(tot) + to_decimal(t_billjournal.fremdwaehrng)
                                    else:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.betrag)
                                        tot =  to_decimal(tot) + to_decimal(t_billjournal.betrag)

                                elif t_billjournal.bediener_nr != 0 and mi_excljournal == False:

                                    if not long_digit:
                                        str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(t_billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(t_billjournal.betriebsnr, ">>>>>>") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate)
                                    else:
                                        str = to_string(t_billjournal.bill_datum) + to_string(t_billjournal.zinr, "x(6)") + to_string(t_billjournal.rechnr, "999999999") + to_string(t_billjournal.artnr, "9999") + to_string(t_billjournal.bezeich, "x(50)") + to_string(hoteldpt.depart, "x(12)") + to_string(t_billjournal.betriebsnr, ">>>>>>") + to_string(t_billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(t_billjournal.zeit, "HH:MM:SS") + to_string(t_billjournal.userinit, "x(4)") + to_string(t_billjournal.sysdate)
                                    qty = qty + t_billjournal.anzahl
                                    gqty = gqty + t_billjournal.anzahl

                                    if foreign_flag:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.fremdwaehrng)
                                        tot =  to_decimal(tot) + to_decimal(t_billjournal.fremdwaehrng)
                                    else:
                                        sub_tot =  to_decimal(sub_tot) + to_decimal(t_billjournal.betrag)
                                        tot =  to_decimal(tot) + to_decimal(t_billjournal.betrag)
                            add_field()


            if it_exist:
                output_list = Output_list()
                output_list_data.append(output_list)


                if not long_digit:
                    str = to_string("", "x(77)") + to_string("T O T A L ", "x(12)") + to_string("", "x(6)") + to_string(qty, "-9999") + to_string(sub_tot, "->>,>>>,>>>,>>>,>>9.99")
                else:
                    str = to_string("", "x(77)") + to_string("T O T A L ", "x(12)") + to_string("", "x(6)") + to_string(qty, "-9999") + to_string(sub_tot, "->,>>>,>>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)


        if not long_digit:
            str = to_string("", "x(77)") + to_string("Grand TOTAL ", "x(12)") + to_string("", "x(6)") + to_string(gqty, "-9999") + to_string(tot, "->>,>>>,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(77)") + to_string("Grand TOTAL ", "x(12)") + to_string("", "x(6)") + to_string(gqty, "-9999") + to_string(tot, "->,>>>,>>>,>>>,>>>,>>9")
        gtot =  to_decimal(tot)


    def add_field():

        nonlocal gtot, output_list_data, curr_date, descr1, voucher_no, ind, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, lvcs, billjournal, guest, artikel, hoteldpt, bill, h_bill, bk_veran, reservation, arrangement, res_line, genstat, segment, argt_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease


        nonlocal output_list, t_billjournal
        nonlocal output_list_data, t_billjournal_data


        roomnumber = substring(output_list.str, 8, 6)

        if t_billjournal.rechnr > 0:

            bill = get_cache (Bill, {"rechnr": [(eq, t_billjournal.rechnr)]})

            if bill:

                if bill.resnr != 0:

                    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, roomnumber)]})

                    if res_line:

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                        output_list.checkin = res_line.ankunft
                        output_list.checkout = res_line.abreise
                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    else:

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                            output_list.checkin = res_line.ankunft
                            output_list.checkout = res_line.abreise
                            output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
        else:

            if get_index(output_list.descr, "[#") > 0:
                curr_str = substring(output_list.descr, get_index(output_list.descr, "[#") + 2 - 1)
                curr_resnr = to_int(entry(0, curr_str, " "))

            elif get_index(output_list.descr, " #") > 0:
                curr_str = substring(output_list.descr, get_index(output_list.descr, " #") + 2 - 1)
                curr_resnr = to_int(entry(0, curr_str, "]"))

            res_line = get_cache (Res_line, {"resnr": [(eq, curr_resnr)]})

            if res_line:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                output_list.checkin = res_line.ankunft
                output_list.checkout = res_line.abreise
                output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

    if from_date == None:

        return generate_output()

    if to_date == None:

        return generate_output()

    for billjournal in db_session.query(Billjournal).filter(
             (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.bill_datum >= from_date) & (Billjournal.bill_datum <= to_date) & (Billjournal.anzahl != 0)).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():
        t_billjournal = T_billjournal()
        t_billjournal_data.append(t_billjournal)

        buffer_copy(billjournal, t_billjournal)
    journal_list()

    output_list = query(output_list_data, first=True)
    while None != output_list:

        if output_list.MB.lower()  == ("*").lower()  and roomnumber == "":
            output_list.guestname = ""
            output_list.segcode = ""

        elif output_list.shift != "":
            output_list.checkin = None
            output_list.checkout = None
            output_list.guestname = ""
            output_list.segcode = ""

        output_list = query(output_list_data, next=True)

    return generate_output()