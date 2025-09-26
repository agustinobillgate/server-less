#using conversion tools version: 1.0.0.105
#-----------------------------------------
# 17-July-25, update INT64() -> int(), 
# if available res_line
#-----------------------------------------

from functions.additional_functions import *
from sqlalchemy import func
from decimal import Decimal
from datetime import date
import re
from functions.calc_servvat import calc_servvat
from models import Guest, Artikel, Queasy, Htparam, Bill, Bill_line, Res_line, Reservation, Sourccod, Segment, Genstat, Guestseg, Debitor, Hoteldpt, Billjournal, H_bill, Bk_veran, Arrangement, Argt_line, H_journal

def format_fixed_length(text: str, length: int) -> str:
        if len(text) > length:
            return text[:length]   # trim
        else:
            return text.ljust(length)

def fo_journal_cld_3bl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, sorttype:int, exclude_artrans:bool, long_digit:bool, foreign_flag:bool, mi_onlyjournal:bool, mi_excljournal:bool, mi_post:bool, mi_showrelease:bool, mi_break:bool, id_flag:string):

    prepare_cache ([Guest, Artikel, Queasy, Htparam, Bill, Res_line, Reservation, Sourccod, Segment, Genstat, Guestseg, Debitor, Hoteldpt, Billjournal, H_bill, Bk_veran, H_journal])

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
    shift:int = 0
    temp1:string = ""
    temp2:string = ""
    counter:int = 0
    isoutletshift:bool = False
    guest = artikel = queasy = htparam = bill = bill_line = res_line = reservation = sourccod = segment = genstat = guestseg = debitor = hoteldpt = billjournal = h_bill = bk_veran = arrangement = argt_line = h_journal = None

    output_list = shift_list = buffguest = gbuff = shift_buff = b_artikel = None

    output_list_list, Output_list = create_model("Output_list", {"bezeich":string, "c":string, "ns":string, "mb":string, "shift":string, "dept":string, "str":string, "sstr":string, "remark":string, "gname":string, "descr":string, "voucher":string, "checkin":date, "checkout":date, "guestname":string, "segcode":string, "amt_nett":Decimal, "service":Decimal, "vat":Decimal, "zinr":string, "deptno":int, "nationality":string, "resnr":int, "book_source":string, "resname":string})
    shift_list_list, Shift_list = create_model("Shift_list", {"shift":int, "ftime":int, "ttime":int})

    Buffguest = create_buffer("Buffguest",Guest)
    Gbuff = create_buffer("Gbuff",Guest)
    Shift_buff = Shift_list
    shift_buff_list = shift_list_list

    B_artikel = create_buffer("B_artikel",Artikel)


    db_session = local_storage.db_session

    log_debug = []

    def generate_output():
        nonlocal gtot, output_list_list, curr_date, descr1, voucher_no, ind, indexing, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, serv, vat, netto, temp_str, hoteldept, shift, temp1, temp2, counter, isoutletshift, guest, artikel, queasy, htparam, bill, bill_line, res_line, reservation, sourccod, segment, genstat, guestseg, debitor, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line, h_journal
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal buffguest, gbuff, shift_buff, b_artikel


        nonlocal output_list, shift_list, buffguest, gbuff, shift_buff, b_artikel
        nonlocal output_list_list, shift_list_list
        
        return {"gtot": gtot, "output-list": output_list_list}

    def handle_null_date(inp_date:date):

        nonlocal gtot, output_list_list, curr_date, descr1, voucher_no, ind, indexing, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, serv, vat, netto, temp_str, hoteldept, shift, temp1, temp2, counter, isoutletshift, guest, artikel, queasy, htparam, bill, bill_line, res_line, reservation, sourccod, segment, genstat, guestseg, debitor, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line, h_journal
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal buffguest, gbuff, shift_buff, b_artikel


        nonlocal output_list, shift_list, buffguest, gbuff, shift_buff, b_artikel
        nonlocal output_list_list, shift_list_list

        if inp_date == None:
            return " " * 8
        else:
            return to_string(inp_date)


    def handle_null_char(inp_char:string):

        nonlocal gtot, output_list_list, curr_date, descr1, voucher_no, ind, indexing, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, serv, vat, netto, temp_str, hoteldept, shift, temp1, temp2, counter, isoutletshift, guest, artikel, queasy, htparam, bill, bill_line, res_line, reservation, sourccod, segment, genstat, guestseg, debitor, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line, h_journal
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal buffguest, gbuff, shift_buff, b_artikel


        nonlocal output_list, shift_list, buffguest, gbuff, shift_buff, b_artikel
        nonlocal output_list_list, shift_list_list

        if inp_char == None:
            return ""
        else:

            if num_entries(inp_char, "|") > 1:
                inp_char = replace_str(inp_char, "|", "-")
            return inp_char


    def custom_record():

        nonlocal gtot, output_list_list, curr_date, descr1, voucher_no, ind, indexing, gdelimiter, serv, vat, netto, temp_str, hoteldept, shift, temp1, temp2, counter, isoutletshift, guest, artikel, queasy, htparam, bill, bill_line, res_line, reservation, sourccod, segment, genstat, guestseg, debitor, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line, h_journal
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal buffguest, gbuff, shift_buff, b_artikel

        nonlocal output_list, shift_list, buffguest, gbuff, shift_buff, b_artikel
        nonlocal output_list_list, shift_list_list

        roomnumber:string = ""
        zinrdate:date = None
        billnumber:int = 0
        curr_str:string = ""
        curr_resnr:int = 0
        journdate:date = None
        temp_resnr:Decimal = to_decimal("0.0")
        temp_gastnr:Decimal = to_decimal("0.0")
        temp_descr:string = ""
        artikelnr:int = 0
        queasy_str:string = ""

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

        if htparam:
            journdate = htparam.fdate
        """
09/24/24227   0001338550100Lodging (Room Revenue)                            Front Office      1    341550                05:05:51$$  09/24/24                        ",
   
        """
        roomnumber = substring(output_list.sstr, 8, 6)
        roomnumber = roomnumber.strip()
        tmp_mm = substring(output_list.sstr, 0, 2)
        tmp_dd = substring(output_list.sstr, 3, 2)
        tmp_yy = substring(output_list.sstr, 6, 2)
        # perubahan output_list.sstr 09/24/24 -> membuat string parsing berubah
        # zinrdate = date_mdy(substring(output_list.s, 0, 8))
        if tmp_dd.strip() !="" and tmp_mm.strip() !="" and tmp_yy.strip() !="":
            zinrdate = date(to_int(tmp_yy)+2000, to_int(tmp_mm), to_int(tmp_dd))
        else:
            zinrdate = None
            
        billnumber = to_int(substring(output_list.str, 14, 9))
        artikelnr = to_int(substring(output_list.str, 23, 4))
        curr_str = " "
        curr_resnr = 0

        if output_list.mb.lower()  == ("*").lower() :

            bill = get_cache (Bill, {"rechnr": [(eq, billnumber)]})

            bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"zinr": [(eq, roomnumber)]})

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, roomnumber)]})

            # Rd 13/8/2025
            # if res_line available
            if res_line:
                # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()

                # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                if guest and reservation:
                    output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.checkin = res_line.ankunft
                    output_list.checkout = res_line.abreise
                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                    output_list.nationality = guest.nation1
                    output_list.resnr = res_line.resnr
                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                    if reservation.resart != 0:

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.book_source = sourccod.bezeich

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    output_list.segcode = segment.bezeich
                else:
                    output_list.segcode = ""

        # Rd 13/8/2025
        # if matches(substring(str, 77, 12),r"*T O T A L*"):
        if matches(substring(output_list.str, 77, 12),r"*T O T A L*"):
            output_list.guestname = ""
            output_list.segcode = ""
            output_list.checkin = None
            output_list.checkout = None
            output_list.str = substring(output_list.str, 0, 122)

        # if matches(substring(str, 77, 12),r"*Grand TOTAL*"):
        if matches(substring(output_list.str, 77, 12),r"*Grand TOTAL*"):
            output_list.guestname = ""
            output_list.segcode = ""
            output_list.checkin = None
            output_list.checkout = None
            output_list.str = substring(output_list.str, 0, 122)

        if num_entries(output_list.gname, "|") >= 2:
            output_list.gname = entry(0, output_list.gname, "|")
            output_list.guestname = entry(0, output_list.gname, "|")

        if matches(output_list.descr,r"*[*"):
            temp_resnr =  to_decimal("0")
            temp_gastnr =  to_decimal("0")
            temp_descr = entry(0, output_list.descr, "]")

            if matches(temp_descr,r"*Guest*") and num_entries(temp_descr, "#") >= 2:
                temp_gastnr =  to_decimal(to_decimal(entry(0 , entry(1 , temp_descr , "#") , " ")))
            else:

                if num_entries(temp_descr, "#") >= 2:
                    temp_resnr =  to_decimal(to_decimal(entry(0 , entry(1 , temp_descr , "#") , " ")))

                elif num_entries(output_list.descr, "[") > 1:

                    if num_entries(entry(0, output_list.descr, "[") , "/") <= 1:

                        b_artikel = get_cache (Artikel, {"artnr": [(eq, artikelnr)]})
                        temp_resnr = to_decimal(substring(entry(0, output_list.descr, "[") , length(b_artikel.bezeich) + 2 - 1))

            if temp_resnr != 0:

                # res_line = get_cache (Res_line, {"resnr": [(eq, int(temp_resnr))],"reslinnr": [(eq, 1)]})
                res_line = db_session.query(Res_line).filter(Res_line.resnr == int(temp_resnr), Res_line.reslinnr == 1).first()

                # Rd, 13/8/2025
                # if available res_line
                if res_line:
                    # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                    reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                    # buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                    buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()  

                    # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                    guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                    # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                    gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                    if guest and reservation:
                        output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.checkin = res_line.ankunft
                        output_list.checkout = res_line.abreise
                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                        output_list.nationality = guest.nation1
                        output_list.resnr = res_line.resnr
                        output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                        if reservation.resart != 0:

                            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                            if sourccod:
                                output_list.book_source = sourccod.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        output_list.segcode = segment.bezeich
                    else:
                        output_list.segcode = ""

            elif temp_gastnr != 0:

                # guest = get_cache (Guest, {"gastnr": [(eq, int(temp_gastnr))]})
                guest = db_session.query(Guest).filter(Guest.gastnr == int(temp_gastnr)).first()


                if guest:
                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.nationality = guest.nation1

        elif matches(output_list.descr,r"*#*"):
            temp_resnr =  to_decimal("0")
            temp_gastnr =  to_decimal("0")
            temp_descr = entry(0, output_list.descr, "]")

            if matches(temp_descr,r"*Guest*") and num_entries(temp_descr, "#") >= 2:
                temp_gastnr =  to_decimal(to_decimal(entry(0 , entry(1 , temp_descr , "#") , " ")))
            else:

                if num_entries(temp_descr, "#") >= 2:
                    temp_resnr =  to_decimal(to_decimal(entry(0 , entry(1 , temp_descr , "#") , " ")))

                elif num_entries(output_list.descr, "[") > 1:

                    b_artikel = get_cache (Artikel, {"artnr": [(eq, artikelnr)]})
                    temp_resnr = to_decimal(substring(entry(0, output_list.descr, "[") , length(b_artikel.bezeich) + 2 - 1))

            if temp_resnr != 0:

                res_line = get_cache (Res_line, {"resnr": [(eq, int(temp_resnr))],"reslinnr": [(eq, 1)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                # buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()

                # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()


                # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()


                if guest and reservation:
                    output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.checkin = res_line.ankunft
                    output_list.checkout = res_line.abreise
                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                    output_list.nationality = guest.nation1
                    output_list.resnr = res_line.resnr
                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                    if reservation.resart != 0:

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.book_source = sourccod.bezeich

                # segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                segment = db_session.query(Segment).filter(Segment.segmentcode == reservation.segmentcode).first()

                if segment:
                    output_list.segcode = segment.bezeich
                else:
                    output_list.segcode = ""

            elif temp_gastnr != 0:

                # guest = get_cache (Guest, {"gastnr": [(eq, int(temp_gastnr))]})
                guest = db_session.query(Guest).filter(Guest.gastnr == int(temp_gastnr)).first()


                if guest:
                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.nationality = guest.nation1

        if roomnumber != "" and billnumber == 0:

            if zinrdate >= journdate:

                res_line = get_cache (Res_line, {"zinr": [(eq, roomnumber)],"ankunft": [(eq, zinrdate)]})
                # res_line = db_session.query(Res_line).filter(Res_line.zinr == roomnumber, Res_line.ankunft == zinrdate).first()

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                # reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()


                buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                # buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                # guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                # gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                if guest and reservation:
                    output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.checkin = res_line.ankunft
                    output_list.checkout = res_line.abreise
                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                    output_list.nationality = guest.nation1
                    output_list.resnr = res_line.resnr
                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                    if reservation.resart != 0:

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.book_source = sourccod.bezeich

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    output_list.segcode = segment.bezeich
                else:
                    output_list.segcode = ""

            elif zinrdate < journdate:

                genstat = get_cache (Genstat, {"datum": [(eq, zinrdate)],"zinr": [(eq, roomnumber)]})

                if genstat:

                    # reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})
                    reservation = db_session.query(Reservation).filter(Reservation.resnr == genstat.resnr).first()

                    # res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)]})
                    res_line = db_session.query(Res_line).filter(Res_line.resnr == reservation.resnr).first()

                    # buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                    buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()

                    # guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})
                    guest = db_session.query(Guest).filter(Guest.gastnr == genstat.gastnrmember).first()

                    # gbuff = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})
                    gbuff = db_session.query(Guest).filter(Guest.gastnr == genstat.gastnr).first()

                    if guest and reservation:
                        output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.checkin = genstat.res_date[0]
                        output_list.checkout = genstat.res_date[1]
                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                        if buffguest:
                            output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                        else:
                            output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1
                        output_list.nationality = guest.nation1
                        output_list.resnr = genstat.resnr
                        output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                        if reservation.resart != 0:

                            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                            if sourccod:
                                output_list.book_source = sourccod.bezeich

                    # segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                    segment = db_session.query(Segment).filter(Segment.segmentcode == reservation.segmentcode).first()

                    if segment:
                        output_list.segcode = segment.bezeich
                    else:
                        output_list.segcode = ""
        roomnumber = ""

        if output_list.ns != "" and handle_null_char (output_list.gname) != "" and bill:

            # buffguest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
            buffguest = db_session.query(Guest).filter(Guest.gastnr == bill.gastnr).first()

            # guestseg = get_cache (Guestseg, {"gastnr": [(eq, buffguest.gastnr)]})
            guestseg = db_session.query(Guestseg).filter(Guestseg.gastnr == buffguest.gastnr).first()

            if guestseg:

                segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

                if segment:
                    output_list.segcode = segment.bezeich
                else:
                    output_list.segcode = "UNKNOWN"
            else:
                output_list.segcode = "UNKNOWN"

        if billjournal and exclude_artrans == False and artikel.artart != 4:

            debitor = get_cache (Debitor, {"rechnr": [(eq, billjournal.rechnr)],"zahlkonto": [(eq, billjournal.artnr)],"rgdatum": [(eq, billjournal.bill_datum)],"zinr": [(eq, billjournal.zinr)],"saldo": [(eq, billjournal.betrag)],"transzeit": [(eq, billjournal.zeit)]})

            if debitor:

                b_artikel = get_cache (Artikel, {"artnr": [(eq, debitor.artnr)]})

                if b_artikel:
                    output_list.descr = "A/R Transfer from " + to_string(debitor.artnr) + " " + b_artikel.bezeich
        queasy = Queasy()
        db_session.add(queasy)
# """
#             Visa[Deposit #96252]                                                                                1234                                    Sembodo, Yaksa           Sembodo, Yaksa                                                                                                                                      09/24/2409/25/24ECO-ONLINE 0        96252ONLINE TRAVEL AGENTTIKET.COM,                 0.00               0.00               0.00",

# """
        counter = counter + 1
        # queasy_str = to_string(output_list.c, "x(2)") +\
        #         to_string(handle_null_char (output_list.zinr) , "x(6)") +\
        #         to_string(handle_null_char (output_list.ns) , "x(1)") +\
        #         to_string(handle_null_char (output_list.mb) , "x(1)") +\
        #         to_string(handle_null_char (output_list.shift) , "x(2)") +\
        #         to_string(handle_null_char (output_list.descr) , "x(50)") +\
        #         to_string(handle_null_char (output_list.voucher) , "x(40)") +\
        #         to_string(handle_null_char (output_list.guestname) , "x(25)") +\
        #         to_string(handle_null_char (output_list.gname) , "x(24)") +\
        #         to_string(handle_null_char (output_list.remark) , "x(124)") +\
        #         to_string(handle_null_date (output_list.checkin)) +\
        #         to_string(handle_null_date (output_list.checkout)) +\
        #         to_string(handle_null_char (output_list.segcode) , "X(20)") +\
        #         to_string(output_list.deptno , ">9") +\
        #         to_string(handle_null_char (output_list.nationality) , "X(5)") +\
        #         to_string(output_list.resnr , ">>>>>>>>>9") +\
        #         to_string(handle_null_char (output_list.book_source) , "X(20)") +\
        #         to_string(handle_null_char (output_list.resname) , "X(25)") +\
        #         " " + to_string(output_list.amt_nett , "->>>,>>>,>>>,>>9.99") +\
        #         " " + to_string(output_list.service , "->>>,>>>,>>>,>>9.99") +\
        #         " " + to_string(output_list.vat , "->>>,>>>,>>>,>>9.99")
        queasy_str = to_string(output_list.c, "x(2)") +\
                format_fixed_length(handle_null_char (output_list.zinr) , 6) +\
                format_fixed_length(handle_null_char (output_list.ns) , 1) +\
                format_fixed_length(handle_null_char (output_list.mb) , 1) +\
                format_fixed_length(handle_null_char (output_list.shift) , 2) +\
                format_fixed_length(handle_null_char (output_list.descr) , 50) +\
                format_fixed_length(handle_null_char (output_list.voucher) , 40) +\
                format_fixed_length(handle_null_char (output_list.guestname) , 25) +\
                format_fixed_length(handle_null_char (output_list.gname) , 24) +\
                format_fixed_length(handle_null_char (output_list.remark) , 124) +\
                format_fixed_length(handle_null_date (output_list.checkin), 8) +\
                format_fixed_length(handle_null_date (output_list.checkout), 8) +\
                format_fixed_length(handle_null_char (output_list.segcode) , 20) +\
                to_string(output_list.deptno , ">9") +\
                format_fixed_length(handle_null_char (output_list.nationality) , 5) +\
                to_string(output_list.resnr , ">>>>>>>>>9") +\
                format_fixed_length(handle_null_char (output_list.book_source) , 20) +\
                format_fixed_length(handle_null_char (output_list.resname) , 25) +\
                " " + to_string(output_list.amt_nett , "->>>,>>>,>>>,>>9.99") +\
                " " + to_string(output_list.service , "->>>,>>>,>>>,>>9.99") +\
                " " + to_string(output_list.vat , "->>>,>>>,>>>,>>9.99")
        queasy.key = 280
        queasy.char1 = "FO Transaction"
        queasy.char2 = id_flag
        queasy.char3 = output_list.sstr + "|" + queasy_str
        queasy.number1 = counter

        if mi_break:
            queasy.logi1 = mi_break
        else:
            queasy.logi1 = mi_break

        if bill:
            pass

        if res_line:
            pass

        if reservation:
            pass

        if guest:
            pass

        if buffguest:
            pass

        if gbuff:
            pass

        if sourccod:
            pass

        if segment:
            pass

        if h_bill:
            pass

        if genstat:
            pass

        if bk_veran:
            pass

        if arrangement:
            pass

        if argt_line:
            pass

        if h_journal:
            pass

        if shift_list:
            pass

        if shift_buff:
            pass

        if hoteldpt:
            pass


    def journal_list():

        nonlocal gtot, output_list_list, descr1, voucher_no, ind, indexing, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, serv, vat, netto, temp_str, hoteldept, shift, temp1, temp2, counter, isoutletshift, guest, artikel, queasy, htparam, bill, bill_line, res_line, reservation, sourccod, segment, genstat, guestseg, debitor, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line, h_journal
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal buffguest, gbuff, shift_buff, b_artikel


        nonlocal output_list, shift_list, buffguest, gbuff, shift_buff, b_artikel
        nonlocal output_list_list, shift_list_list

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
        output_list_list.clear()

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artnr >= from_art) & 
                 (Artikel.artnr <= to_art) & 
                 (Artikel.departement >= from_dept) & 
                 (Artikel.departement <= to_dept)).order_by((Artikel.departement * 10000 + Artikel.artnr)).all():

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
                        do_it = True

                        if (mi_onlyjournal  and billjournal.bediener_nr == 0) or (mi_excljournal  and billjournal.bediener_nr != 0):
                            do_it = False

                        if exclude_artrans and billjournal.kassarapport:
                            do_it = False

                        if not mi_showrelease and billjournal.betrag == 0:
                            do_it = False

                        if do_it  and exclude_artrans  and artikel.artart != 4:

                            debitor = get_cache (Debitor, {"rechnr": [(eq, billjournal.rechnr)],"zahlkonto": [(eq, billjournal.artnr)],"rgdatum": [(eq, billjournal.bill_datum)],"zinr": [(eq, billjournal.zinr)],"saldo": [(eq, billjournal.betrag)],"transzeit": [(eq, billjournal.zeit)]})

                            if debitor:
                                do_it = False

                        if do_it:
                            it_exist = True
                            output_list = Output_list()
                            output_list_list.append(output_list)
                            if (billjournal.bediener_nr == 0 and mi_onlyjournal == False) or (billjournal.bediener_nr != 0 and mi_excljournal == False):
                                output_list.remark = billjournal.stornogrund

                            if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                                if billjournal.rechnr > 0:
                                    
                                    if billjournal.bediener_nr == 0 and mi_onlyjournal == False:
                                        
                                        # bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})
                                        bill = db_session.query(Bill).filter(Bill.rechnr == billjournal.rechnr).first()
                                        # print(f"/{billjournal.zinr}/{billjournal.rechnr}/")
                                        log_debug.append(f"0.Bill: {billjournal.bezeich} Rechnr: {to_string(billjournal.rechnr)}, Room:{billjournal.zinr}")
                                        if bill and billjournal.zinr != "":
                                            log_debug.append(f"1.Bill found ResNr: {to_string(bill.resnr)}, Room:{billjournal.zinr}")
                                            # res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, bill.zinr)]})
                                            res_line = db_session.query(Res_line).filter(Res_line.resnr == bill.resnr, 
                                                                                         Res_line.zinr == bill.zinr).first()

                                            # Rd 13/8/2025
                                            # if res_line
                                            if res_line:
                                                log_debug.append(f"2Res_line found Resnr: {to_string(res_line.resnr)}, Room: {res_line.zinr}")
                                                # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                                reservation = db_session.query(Reservation).filter(Reservation.resnr == bill.resnr).first()

                                                # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                                                # buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                                                buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()

                                                # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                                gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                                                if guest and reservation:
                                                    log_debug.append(f"Guest and Reservation found")
                                                    output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                    output_list.checkin = res_line.ankunft
                                                    output_list.checkout = res_line.abreise
                                                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                    output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                                                    output_list.nationality = guest.nation1
                                                    output_list.resnr = res_line.resnr
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                    if reservation.resart != 0:

                                                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                                                        if sourccod:
                                                            output_list.book_source = sourccod.bezeich

                                                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                                                    if segment:
                                                        output_list.segcode = segment.bezeich
                                                    else:
                                                        output_list.segcode = ""

                                        elif bill:
                                            log_debug.append(f"Elif Bill.")
                                            if bill.resnr == 0 and bill.bilname.strip() != "":
                                                log_debug.append(f"Bill with no reservation but with billname: {bill.bilname}")
                                                output_list.gname = bill.bilname
                                                output_list.guestname = bill.bilname
                                            else:

                                                # gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
                                                gbuff = db_session.query(Guest).filter(Guest.gastnr == bill.gastnr).first()
                                                log_debug.append(f"Bill gbuff Gastnr: {to_string(bill.gastnr)}")
                                                if gbuff:
                                                    log_debug.append(f"Bill gbuff found: {gbuff.name}")
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.nationality = gbuff.nation1

                                    elif billjournal.bediener_nr != 0 and mi_excljournal == False:

                                        h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                                        if h_bill:

                                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                                if res_line:

                                                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                                    # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                    guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                                                    # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                                    gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                                                    output_list.checkin = res_line.ankunft
                                                    output_list.checkout = res_line.abreise
                                                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                    output_list.gname = h_bill.bilname
                                                    output_list.nationality = guest.nation1
                                                    output_list.resnr = res_line.resnr
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                    if reservation and reservation.resart != 0:

                                                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                                                        if sourccod:
                                                            output_list.book_source = sourccod.bezeich

                                                    if h_bill.bilname == "":

                                                        # buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                                                        buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()

                                                        if buffguest:
                                                            output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

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

                                                # guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})
                                                guest = db_session.query(Guest).filter(Guest.gastnr == h_bill.resnr).first()


                                                if guest:
                                                    output_list.guestname = guest.name + "," + guest.vorname1
                                                    output_list.gname = h_bill.bilname
                                                    output_list.nationality = guest.nation1


                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == h_bill.segmentcode).first()

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif h_bill.resnr == 0 and h_bill.bilname != "":
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == h_bill.segmentcode).first()

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif billjournal.betriebsnr == 0:

                                                bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                                                if bill:

                                                    # res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})
                                                    res_line = db_session.query(Res_line).filter(Res_line.resnr == bill.resnr, Res_line.reslinnr == bill.reslinnr).first()

                                                    if res_line:

                                                        # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                                        reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                                                        # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                        guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                                                        # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                                        gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                                                        output_list.checkin = res_line.ankunft
                                                        output_list.checkout = res_line.abreise
                                                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                        output_list.gname = bill.name
                                                        output_list.nationality = guest.nation1
                                                        output_list.resnr = res_line.resnr
                                                        output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                        if reservation and reservation.resart != 0:

                                                            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                                                            if sourccod:
                                                                output_list.book_source = sourccod.bezeich

                                                        # genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})
                                                        genstat = db_session.query(Genstat).filter(Genstat.resnr == res_line.resnr).first()

                                                        # segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                                                        segment = db_session.query(Segment).filter(Segment.segmentcode == genstat.segmentcode).first()


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
                                                output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.nationality = gbuff.nation1

                                    elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                                        lviresnr = -1
                                        lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, "[#") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, " "))

                                        # reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})
                                        reservation = db_session.query(Reservation).filter(Reservation.resnr == lviresnr).first()

                                        if reservation:

                                            gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.nationality = gbuff.nation1

                                            if reservation.resart != 0:

                                                # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                                                sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                                                if sourccod:
                                                    output_list.book_source = sourccod.bezeich

                                    elif get_index(billjournal.bezeich, " #") > 0 and billjournal.departement == 0:
                                        lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, " #") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, "]"))

                                        # reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})
                                        reservation = db_session.query(Reservation).filter(Reservation.resnr == lviresnr).first()


                                        if reservation:

                                            # gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
                                            gbuff = db_session.query(Guest).filter(Guest.gastnr == reservation.gastnr).first()

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.nationality = gbuff.nation1

                                            if reservation.resart != 0:

                                                # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                                                sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                                                if sourccod:
                                                    output_list.book_source = sourccod.bezeich
                            else:

                                # arrangement = get_cache (Arrangement, {"artnr_logis": [(eq, artikel.artnr)],"intervall": [(eq, artikel.departement)]})
                                arrangement = db_session.query(Arrangement).filter(Arrangement.artnr_logis == artikel.artnr, Arrangement.intervall == artikel.departement).first()

                                if arrangement:

                                    # h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.departement)]})
                                    h_bill = db_session.query(H_bill).filter(H_bill.rechnr == billjournal.rechnr, H_bill.departement == billjournal.departement).first()

                                    if h_bill:

                                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                            # res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})
                                            res_line = db_session.query(Res_line).filter(Res_line.resnr == h_bill.resnr, Res_line.reslinnr == h_bill.reslinnr).first()


                                            if res_line:
                                                output_list.resnr = res_line.resnr
                                                output_list.guestname = res_line.name
                                                output_list.gname = h_bill.bilname

                                                # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                                gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                                                if gbuff:
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                                reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                                                if reservation and reservation.resart != 0:

                                                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                                                    if sourccod:
                                                        output_list.book_source = sourccod.bezeich

                                                # genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})
                                                genstat = db_session.query(Genstat).filter(Genstat.resnr == res_line.resnr).first()

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == genstat.segmentcode).first()

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich
                                            else:
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                        elif h_bill.resnr > 0:

                                            # guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})
                                            guest = db_session.query(Guest).filter(Guest.gastnr == h_bill.resnr).first()

                                            if guest:
                                                output_list.guestname = guest.name + "," + guest.vorname1
                                                output_list.gname = h_bill.bilname
                                                output_list.nationality = guest.nation1


                                            else:
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                            # segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})
                                            segment = db_session.query(Segment).filter(Segment.segmentcode == h_bill.segmentcode).first()

                                            if not segment:
                                                output_list.segcode = ""
                                            else:
                                                output_list.segcode = segment.bezeich

                                        elif h_bill.resnr == 0:
                                            output_list.guestname = h_bill.bilname
                                            output_list.gname = h_bill.bilname

                                            # segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})
                                            segment = db_session.query(Segment).filter(Segment.segmentcode == h_bill.segmentcode).first()

                                            if not segment:
                                                output_list.segcode = ""
                                            else:
                                                output_list.segcode = segment.bezeich
                                else:

                                    # argt_line = get_cache (Argt_line, {"argt_artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)]})
                                    argt_line = db_session.query(Argt_line).filter(Argt_line.argt_artnr == artikel.artnr, Argt_line.departement == artikel.departement).first()

                                    if argt_line:
                                        hoteldept = billjournal.departement

                                        if matches(billjournal.bezeich, ("*<*")) and matches(billjournal.bezeich, ("*>*")):
                                            hoteldept = to_int(substring(billjournal.bezeich, get_index(billjournal.bezeich, "<") + 1 - 1, get_index(billjournal.bezeich, ">") - get_index(billjournal.bezeich, "<") - 1))

                                        h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, hoteldept)]})

                                        if h_bill:

                                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                                if res_line:

                                                    # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                                    reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                                                    # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                    guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                                                    # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                                    gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                                                    output_list.checkin = res_line.ankunft
                                                    output_list.checkout = res_line.abreise
                                                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                    output_list.gname = h_bill.bilname
                                                    output_list.nationality = guest.nation1
                                                    output_list.resnr = res_line.resnr
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                    if reservation and reservation.resart != 0:

                                                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                                                        if sourccod:
                                                            output_list.book_source = sourccod.bezeich

                                                    # genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})
                                                    genstat = db_session.query(Genstat).filter(Genstat.resnr == res_line.resnr).first()

                                                    # segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                                                    segment = db_session.query(Segment).filter(Segment.segmentcode == genstat.segmentcode).first()

                                                    if not segment:
                                                        output_list.segcode = ""
                                                    else:
                                                        output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                            elif h_bill.resnr > 0:

                                                # guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})
                                                guest = db_session.query(Guest).filter(Guest.gastnr == h_bill.resnr).first()


                                                if guest:
                                                    output_list.guestname = guest.name + "," + guest.vorname1
                                                    output_list.gname = h_bill.bilname
                                                    output_list.nationality = guest.nation1


                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == h_bill.segmentcode).first()

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif h_bill.resnr == 0:
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == h_bill.segmentcode).first()

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                            if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                output_list.bezeich = artikel.bezeich

                            if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                shift = 0

                                if billjournal.betriebsnr != 0 and isoutletshift :

                                    h_journal = get_cache (H_journal, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                                    if h_journal:

                                        shift_list = query(shift_list_list, filters=(lambda shift_list: shift_list.ftime <= h_journal.zeit and shift_list.ttime >= h_journal.zeit), first=True)

                                        if shift_list:
                                            shift = shift_list.shift
                                        else:

                                            shift_buff = query(shift_buff_list, filters=(lambda shift_buff: shift_buff.ftime >= shift_buff.ttime), first=True)

                                            if shift_buff:
                                                shift = shift_buff.shift
                                output_list.c = to_string(billjournal.betriebsnr, "99")
                                output_list.shift = to_string(shift, "99")

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

                                if matches(billjournal.bezeich,r"*Deposit*") and billjournal.rechnr != 0:

                                    if not long_digit:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                    else:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                else:

                                    if not long_digit:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + "      " + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                    else:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + to_string("", "x(6)") + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
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
                                    output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                else:
                                    output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                qty = qty + billjournal.anzahl
                                gqty = gqty + billjournal.anzahl

                                if foreign_flag:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.fremdwaehrng)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.fremdwaehrng)
                                else:
                                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                                    tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

                            elif mi_excljournal:

                                # hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})
                                hoteldpt = db_session.query(Hoteldpt).filter(Hoteldpt.num == billjournal.departement).first()

                                if hoteldpt:
                                    deptname = hoteldpt.depart
                                output_list.zinr = billjournal.zinr
                                output_list.deptno = billjournal.departement

                                if not long_digit:
                                    output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                else:
                                    output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
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
                                temp_str = substring(str, 100)
                                output_list.sstr =  substring(str, 0, 95)
                                output_list.sstr =  output_list.sstr + to_string(res_line.erwachs, "-9999") + temp_str
                                temp_str = ""
                            custom_record()


                elif sorttype == 1:

                    for billjournal in db_session.query(Billjournal).filter(
                             (Billjournal.artnr == artikel.artnr) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == curr_date)).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():
                        do_it = True

                        if (mi_onlyjournal  and billjournal.bediener_nr == 0) or (mi_excljournal  and billjournal.bediener_nr != 0):
                            do_it = False

                        if exclude_artrans and billjournal.kassarapport:
                            do_it = False

                        if not mi_showrelease and billjournal.betrag == 0:
                            do_it = False

                        if do_it  and exclude_artrans  and artikel.artart != 4:

                            debitor = get_cache (Debitor, {"rechnr": [(eq, billjournal.rechnr)],"zahlkonto": [(eq, billjournal.artnr)],"rgdatum": [(eq, billjournal.bill_datum)],"zinr": [(eq, billjournal.zinr)],"saldo": [(eq, billjournal.betrag)],"transzeit": [(eq, billjournal.zeit)]})

                            if debitor:
                                do_it = False

                        if do_it:
                            it_exist = True
                            output_list = Output_list()
                            output_list_list.append(output_list)


                            if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                output_list.remark = billjournal.stornogrund

                            if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                                if billjournal.rechnr > 0:

                                    if billjournal.bediener_nr == 0 and mi_onlyjournal == False:

                                        # bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})
                                        bill = db_session.query(Bill).filter(Bill.rechnr == billjournal.rechnr).first()

                                        if bill and billjournal.zinr != "":

                                            # res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, bill.zinr)]})
                                            res_line = db_session.query(Res_line).filter(Res_line.resnr == bill.resnr, Res_line.zinr == bill.zinr).first()
                                            
                                            # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                            reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                                            # buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                                            buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()  

                                            # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                            guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                                            # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                            gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                                            if guest and reservation:
                                                output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                output_list.checkin = res_line.ankunft
                                                output_list.checkout = res_line.abreise
                                                output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                                                output_list.nationality = guest.nation1
                                                output_list.resnr = res_line.resnr
                                                output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                if reservation.resart != 0:

                                                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                                                    if sourccod:
                                                        output_list.book_source = sourccod.bezeich

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == reservation.segmentcode).first()

                                                if segment:
                                                    output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.segcode = ""

                                        elif bill:

                                            if bill.resnr == 0 and bill.bilname != "":
                                                output_list.gname = bill.bilname
                                                output_list.guestname = bill.bilname
                                            else:

                                                # gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
                                                gbuff = db_session.query(Guest).filter(Guest.gastnr == bill.gastnr).first()

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.nationality = gbuff.nation1

                                    elif billjournal.bediener_nr != 0 and mi_excljournal == False:

                                        h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                                        if h_bill:

                                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                                # res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})
                                                res_line = db_session.query(Res_line).filter(Res_line.resnr == h_bill.resnr, Res_line.reslinnr == h_bill.reslinnr).first()

                                                if res_line:

                                                    # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                                    reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                                                    # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                    guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()


                                                    # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                                    gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()
                                                    
                                                    output_list.checkin = res_line.ankunft
                                                    output_list.checkout = res_line.abreise
                                                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                    output_list.gname = h_bill.bilname
                                                    output_list.nationality = guest.nation1
                                                    output_list.resnr = res_line.resnr
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                    if reservation and reservation.resart != 0:

                                                        # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                                                        sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                                                        if sourccod:
                                                            output_list.book_source = sourccod.bezeich

                                                    if h_bill.bilname == "":

                                                        # buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                                                        buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()

                                                        if buffguest:
                                                            output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1

                                                    # genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})
                                                    genstat = db_session.query(Genstat).filter(Genstat.resnr == res_line.resnr).first()

                                                    # segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                                                    segment = db_session.query(Segment).filter(Segment.segmentcode == genstat.segmentcode).first()

                                                    if not segment:
                                                        output_list.segcode = ""
                                                    else:
                                                        output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                            elif h_bill.resnr > 0:

                                                # guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})
                                                guest = db_session.query(Guest).filter(Guest.gastnr == h_bill.resnr).first()

                                                if guest:
                                                    output_list.guestname = guest.name + "," + guest.vorname1
                                                    output_list.gname = h_bill.bilname
                                                    output_list.nationality = guest.nation1


                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == h_bill.segmentcode).first()

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif h_bill.resnr == 0 and h_bill.bilname != "":
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == h_bill.segmentcode).first()

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich

                                            elif billjournal.betriebsnr == 0:

                                                # bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})
                                                bill = db_session.query(Bill).filter(Bill.rechnr == billjournal.rechnr).first()

                                                if bill:

                                                    # res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})
                                                    res_line = db_session.query(Res_line).filter(Res_line.resnr == bill.resnr, Res_line.reslinnr == bill.reslinnr).first()

                                                    if res_line:

                                                        # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                                        reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                                                        # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                        guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                                                        # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                                        gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()


                                                        output_list.checkin = res_line.ankunft
                                                        output_list.checkout = res_line.abreise
                                                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                        output_list.gname = bill.name
                                                        output_list.nationality = guest.nation1
                                                        output_list.resnr = res_line.resnr
                                                        output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                        if reservation and reservation.resart != 0:

                                                            # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                                                            sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                                                            if sourccod:
                                                                output_list.book_source = sourccod.bezeich

                                                        # genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})
                                                        genstat = db_session.query(Genstat).filter(Genstat.resnr == res_line.resnr).first()

                                                        # segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                                                        segment = db_session.query(Segment).filter(Segment.segmentcode == genstat.segmentcode).first()

                                                        if not segment:
                                                            output_list.segcode = ""
                                                        else:
                                                            output_list.segcode = segment.bezeich
                                else:

                                    if artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                                        lviresnr = -1
                                        lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, "[#") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, " "))

                                        # reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})
                                        reservation = db_session.query(Reservation).filter(Reservation.resnr == lviresnr).first()

                                        if reservation:

                                            # gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
                                            gbuff = db_session.query(Guest).filter(Guest.gastnr == reservation.gastnr).first()

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.nationality = gbuff.nation1

                                            if reservation.resart != 0:

                                                # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                                                sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                                                if sourccod:
                                                    output_list.book_source = sourccod.bezeich

                                    elif get_index(billjournal.bezeich, " #") > 0 and billjournal.departement == 0:
                                        lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, " #") + 2 - 1)
                                        lviresnr = to_int(entry(0, lvcs, "]"))

                                        # reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})
                                        reservation = db_session.query(Reservation).filter(Reservation.resnr == lviresnr).first()

                                        if reservation:

                                            # gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
                                            gbuff = db_session.query(Guest).filter(Guest.gastnr == reservation.gastnr).first()

                                            if gbuff:
                                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                output_list.nationality = gbuff.nation1

                                            if reservation.resart != 0:

                                                # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                                                sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                                                if sourccod:
                                                    output_list.book_source = sourccod.bezeich
                            else:

                                # arrangement = get_cache (Arrangement, {"artnr_logis": [(eq, artikel.artnr)],"intervall": [(eq, artikel.departement)]})
                                arrangement = db_session.query(Arrangement).filter(Arrangement.artnr_logis == artikel.artnr, Arrangement.intervall == artikel.departement).first()

                                if arrangement:

                                    # h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.departement)]})
                                    h_bill = db_session.query(H_bill).filter(H_bill.rechnr == billjournal.rechnr, H_bill.departement == billjournal.departement).first()

                                    if h_bill:

                                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                            # res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})
                                            res_line = db_session.query(Res_line).filter(Res_line.resnr == h_bill.resnr, Res_line.reslinnr == h_bill.reslinnr).first()

                                            if res_line:
                                                output_list.resnr = res_line.resnr
                                                output_list.guestname = res_line.name
                                                output_list.gname = h_bill.bilname

                                                # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                                gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                                                if gbuff and gbuff.segment3 != 0:
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                                reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                                                if reservation and reservation.resart != 0:

                                                    # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                                                    sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                                                    if sourccod:
                                                        output_list.book_source = sourccod.bezeich

                                                # genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})
                                                genstat = db_session.query(Genstat).filter(Genstat.resnr == res_line.resnr).first()

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == genstat.segmentcode).first()

                                                if not segment:
                                                    output_list.segcode = ""
                                                else:
                                                    output_list.segcode = segment.bezeich
                                            else:
                                                output_list.guestname = h_bill.bilname
                                                output_list.gname = h_bill.bilname

                                        elif h_bill.resnr > 0:

                                            # guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})
                                            guest = db_session.query(Guest).filter(Guest.gastnr == h_bill.resnr).first()


                                            if guest:
                                                output_list.guestname = guest.name + "," + guest.vorname1
                                                output_list.gname = h_bill.bilname
                                                output_list.nationality = guest.nation1


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

                                    # argt_line = get_cache (Argt_line, {"argt_artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)]})
                                    argt_line = db_session.query(Argt_line).filter(Argt_line.argt_artnr == artikel.artnr, Argt_line.departement == artikel.departement).first()

                                    if argt_line:
                                        hoteldept = billjournal.departement

                                        if matches(billjournal.bezeich, ("*<*")) and matches(billjournal.bezeich, ("*>*")):
                                            hoteldept = to_int(substring(billjournal.bezeich, get_index(billjournal.bezeich, "<") + 1 - 1, get_index(billjournal.bezeich, ">") - get_index(billjournal.bezeich, "<") - 1))

                                        # h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, hoteldept)]})
                                        h_bill = db_session.query(H_bill).filter(H_bill.rechnr == billjournal.rechnr, H_bill.departement == hoteldept).first()

                                        if h_bill:

                                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                                if res_line:

                                                    # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                                    reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                                                    # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                                    guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                                                    # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                                    gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()


                                                    output_list.checkin = res_line.ankunft
                                                    output_list.checkout = res_line.abreise
                                                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                    output_list.gname = h_bill.bilname
                                                    output_list.nationality = guest.nation1
                                                    output_list.resnr = res_line.resnr
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                    if reservation and reservation.resart != 0:

                                                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                                                        if sourccod:
                                                            output_list.book_source = sourccod.bezeich

                                                    # genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})
                                                    genstat = db_session.query(Genstat).filter(Genstat.resnr == res_line.resnr).first()

                                                    # segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                                                    segment = db_session.query(Segment).filter(Segment.segmentcode == genstat.segmentcode).first()

                                                    if not segment:
                                                        output_list.segcode = ""
                                                    else:
                                                        output_list.segcode = segment.bezeich
                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                            elif h_bill.resnr > 0:

                                                # guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})
                                                guest = db_session.query(Guest).filter(Guest.gastnr == h_bill.resnr).first()

                                                if guest:
                                                    output_list.guestname = guest.name + "," + guest.vorname1
                                                    output_list.gname = h_bill.bilname
                                                    output_list.nationality = guest.nation1


                                                else:
                                                    output_list.guestname = h_bill.bilname
                                                    output_list.gname = h_bill.bilname

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == h_bill.segmentcode).first()

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
                                shift = 0

                                if billjournal.betriebsnr != 0 and isoutletshift :

                                    h_journal = get_cache (H_journal, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                                    if h_journal:

                                        shift_list = query(shift_list_list, filters=(lambda shift_list: shift_list.ftime <= h_journal.zeit and shift_list.ttime >= h_journal.zeit), first=True)

                                        if shift_list:
                                            shift = shift_list.shift
                                        else:

                                            shift_buff = query(shift_buff_list, filters=(lambda shift_buff: shift_buff.ftime >= shift_buff.ttime), first=True)

                                            if shift_buff:
                                                shift = shift_buff.shift
                                output_list.c = to_string(billjournal.betriebsnr, "99")
                                output_list.shift = to_string(shift, "99")

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

                                if matches(billjournal.bezeich,r"*Deposit*") and billjournal.rechnr != 0:

                                    if not long_digit:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                    else:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + to_string(billjournal.betriebsnr, ">>>>>>") + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                else:

                                    if not long_digit:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + to_string("", "x(6)") + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                    else:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + to_string("", "x(6)") + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
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
                                    output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                else:
                                    output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
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
                                temp_str = substring(str, 100)
                                output_list.sstr =  substring(str, 0, 95)
                                output_list.sstr =  output_list.sstr + to_string(res_line.erwachs, "-9999") + temp_str
                                temp_str = ""
                            custom_record()


                elif sorttype == 2:

                    if mi_post :

                        for billjournal in db_session.query(Billjournal).filter(
                                 (Billjournal.artnr == artikel.artnr) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == curr_date) & (Billjournal.anzahl == 0)).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():
                            do_it = True

                            if (mi_onlyjournal  and billjournal.bediener_nr == 0) or (mi_excljournal  and billjournal.bediener_nr != 0):
                                do_it = False

                            if exclude_artrans and billjournal.kassarapport:
                                do_it = False

                            if not mi_showrelease and billjournal.betrag == 0:
                                do_it = False

                            if do_it  and exclude_artrans  and artikel.artart != 4:

                                debitor = get_cache (Debitor, {"rechnr": [(eq, billjournal.rechnr)],"zahlkonto": [(eq, billjournal.artnr)],"rgdatum": [(eq, billjournal.bill_datum)],"zinr": [(eq, billjournal.zinr)],"saldo": [(eq, billjournal.betrag)],"transzeit": [(eq, billjournal.zeit)]})

                                if debitor:
                                    do_it = False

                            if do_it:
                                it_exist = True
                                output_list = Output_list()
                                output_list_list.append(output_list)


                                if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                    output_list.remark = billjournal.stornogrund

                                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                                    if billjournal.rechnr > 0:

                                        bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                                        if bill and billjournal.zinr != "":

                                            # res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, bill.zinr)]})
                                            res_line = db_session.query(Res_line).filter(Res_line.resnr == bill.resnr, Res_line.zinr == bill.zinr).first()
                                            
                                            # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                            reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                                            # buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                                            buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()  

                                            # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                            guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                                            # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                            gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                                            if guest and reservation:
                                                output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                output_list.checkin = res_line.ankunft
                                                output_list.checkout = res_line.abreise
                                                output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                                output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                                                output_list.nationality = guest.nation1
                                                output_list.resnr = res_line.resnr
                                                output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                                if reservation.resart != 0:

                                                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                                                    if sourccod:
                                                        output_list.book_source = sourccod.bezeich

                                                # segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == reservation.segmentcode).first()

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
                                                        output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                        output_list.nationality = gbuff.nation1
                                    else:

                                        if artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                                            lviresnr = -1
                                            lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, "[#") + 2 - 1)
                                            lviresnr = to_int(entry(0, lvcs, " "))

                                            # reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})
                                            reservation = db_session.query(Reservation).filter(Reservation.resnr == lviresnr).first()

                                            if reservation:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.nationality = gbuff.nation1

                                                if reservation.resart != 0:

                                                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                                                    if sourccod:
                                                        output_list.book_source = sourccod.bezeich

                                        elif get_index(billjournal.bezeich, " #") > 0 and billjournal.departement == 0:
                                            lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, " #") + 2 - 1)
                                            lviresnr = to_int(entry(0, lvcs, "]"))

                                            # reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})
                                            reservation = db_session.query(Reservation).filter(Reservation.resnr == lviresnr).first()

                                            if reservation:

                                                gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.nationality = gbuff.nation1

                                                if reservation.resart != 0:

                                                    # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                                                    sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                                                    if sourccod:
                                                        output_list.book_source = sourccod.bezeich
                                else:
                                    pass

                                if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                    output_list.bezeich = artikel.bezeich

                                if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                    shift = 0

                                    if billjournal.betriebsnr != 0 and isoutletshift :

                                        h_journal = get_cache (H_journal, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                                        if h_journal:

                                            shift_list = query(shift_list_list, filters=(lambda shift_list: shift_list.ftime <= h_journal.zeit and shift_list.ttime >= h_journal.zeit), first=True)

                                            if shift_list:
                                                shift = shift_list.shift
                                            else:

                                                shift_buff = query(shift_buff_list, filters=(lambda shift_buff: shift_buff.ftime >= shift_buff.ttime), first=True)

                                                if shift_buff:
                                                    shift = shift_buff.shift
                                    output_list.c = to_string(billjournal.betriebsnr, "99")
                                    output_list.shift = to_string(shift, "99")

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
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                    else:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
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
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                    else:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
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
                                    temp_str = substring(str, 100)
                                    output_list.sstr =  substring(str, 0, 95)
                                    output_list.sstr =  output_list.sstr + to_string(res_line.erwachs, "-9999") + temp_str
                                    temp_str = ""
                                custom_record()

                    else:

                        for billjournal in db_session.query(Billjournal).filter(
                                 (Billjournal.artnr == artikel.artnr) & (Billjournal.departement == artikel.departement) & (Billjournal.sysdate == curr_date) & (Billjournal.anzahl == 0)).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():
                            do_it = True

                            if (mi_onlyjournal  and billjournal.bediener_nr == 0) or (mi_excljournal  and billjournal.bediener_nr != 0):
                                do_it = False

                            if exclude_artrans and billjournal.kassarapport:
                                do_it = False

                            if not mi_showrelease and billjournal.betrag == 0:
                                do_it = False

                            if do_it  and exclude_artrans  and artikel.artart != 4:

                                debitor = get_cache (Debitor, {"rechnr": [(eq, billjournal.rechnr)],"zahlkonto": [(eq, billjournal.artnr)],"rgdatum": [(eq, billjournal.bill_datum)],"zinr": [(eq, billjournal.zinr)],"saldo": [(eq, billjournal.betrag)],"transzeit": [(eq, billjournal.zeit)]})

                                if debitor:
                                    do_it = False

                            if do_it:
                                it_exist = True
                                output_list = Output_list()
                                output_list_list.append(output_list)


                                if (billjournal.bediener_nr != 0 and mi_excljournal == False) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False):
                                    output_list.remark = billjournal.stornogrund

                                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                                    # bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})
                                    bill = db_session.query(Bill).filter(Bill.rechnr == billjournal.rechnr).first()
                                    

                                    if bill and billjournal.zinr != "":

                                        # res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, bill.zinr)]})
                                        res_line = db_session.query(Res_line).filter(Res_line.resnr == bill.resnr, Res_line.zinr == bill.zinr).first()

                                        # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                        reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()

                                        # buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                                        buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()  

                                        # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                        guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                                        # gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                                        gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                                        if guest and reservation:
                                            output_list.str = output_list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                            output_list.checkin = res_line.ankunft
                                            output_list.checkout = res_line.abreise
                                            output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                            output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                                            output_list.nationality = guest.nation1
                                            output_list.resnr = res_line.resnr
                                            output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                                            if reservation.resart != 0:

                                                sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                                                if sourccod:
                                                    output_list.book_source = sourccod.bezeich

                                            # segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                            segment = db_session.query(Segment).filter(Segment.segmentcode == reservation.segmentcode).first()

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

                                                # gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
                                                gbuff = db_session.query(Guest).filter(Guest.gastnr == bill.gastnr).first()

                                                if gbuff:
                                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                                    output_list.nationality = gbuff.nation1

                                if (billjournal.bediener_nr != 0 and mi_excljournal == False and billjournal.anzahl == 0) or (billjournal.bediener_nr == 0 and mi_onlyjournal == False and billjournal.anzahl == 0):
                                    output_list.bezeich = artikel.bezeich

                                if billjournal.bediener_nr != 0 and mi_excljournal == False:
                                    shift = 0

                                    if billjournal.betriebsnr != 0 and isoutletshift :

                                        h_journal = get_cache (H_journal, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                                        if h_journal:

                                            shift_list = query(shift_list_list, filters=(lambda shift_list: shift_list.ftime <= h_journal.zeit and shift_list.ttime >= h_journal.zeit), first=True)

                                            if shift_list:
                                                shift = shift_list.shift
                                            else:

                                                shift_buff = query(shift_buff_list, filters=(lambda shift_buff: shift_buff.ftime >= shift_buff.ttime), first=True)

                                                if shift_buff:
                                                    shift = shift_buff.shift
                                    output_list.c = to_string(billjournal.betriebsnr, "99")
                                    output_list.shift = to_string(shift, "99")

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

                                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})

                                    if hoteldpt:
                                        deptname = hoteldpt.depart
                                    output_list.zinr = billjournal.zinr
                                    output_list.deptno = billjournal.departement

                                    if matches(billjournal.bezeich,r"*Deposit*") and billjournal.rechnr != 0:

                                        if not long_digit:
                                            output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                        else:
                                            output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                    else:

                                        if not long_digit:
                                            output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + "      " + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                        else:
                                            output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + "      " + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
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
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (descr1) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
                                    else:
                                        output_list.sstr =  to_string(handle_null_date (billjournal.bill_datum) ) + to_string(handle_null_char (billjournal.zinr) , "x(6)") + to_string(billjournal.rechnr, "999999999") + to_string(billjournal.artnr, "9999") + to_string(handle_null_char (billjournal.bezeich) , "x(50)") + to_string(handle_null_char (deptname) , "x(12)") + format_fixed_length(str(billjournal.betriebsnr), 6) + format_fixed_length(str(billjournal.anzahl), 5) + format_fixed_length(to_string(amount), 22) + to_string(billjournal.zeit, "HH:MM:SS") + to_string(handle_null_char (billjournal.userinit) , "x(4)") + to_string(handle_null_date (billjournal.sysdate)) + to_string(handle_null_char (voucher_no) , "x(24)")
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
                                    temp_str = substring(str, 100)
                                    output_list.sstr =  substring(str, 0, 95)
                                    output_list.sstr =  output_list.sstr + to_string(res_line.erwachs, "-9999") + temp_str
                                    temp_str = ""
                            custom_record()


            if it_exist:
                output_list = Output_list()
                output_list_list.append(output_list)

                if not long_digit:
                    output_list.sstr =  to_string("", "x(77)") + to_string("T O T A L ", "x(12)") + to_string("", "x(6)") + format_fixed_length(str(qty), 6) + format_fixed_length(to_string(sub_tot), 22)
                    output_list.amt_nett =  to_decimal(t_amt)
                    output_list.service =  to_decimal(t_service)
                    output_list.vat =  to_decimal(t_vat)
                    t_amt =  to_decimal("0")
                    t_service =  to_decimal("0")
                    t_vat =  to_decimal("0")
                else:
                    output_list.sstr =  to_string("", "x(77)") + to_string("T O T A L ", "x(12)") + to_string("", "x(6)") + format_fixed_length(str(qty), 6) + format_fixed_length(to_string(sub_tot), 22)
                    output_list.amt_nett =  to_decimal(t_amt)
                    output_list.service =  to_decimal(t_service)
                    output_list.vat =  to_decimal(t_vat)
                    t_amt =  to_decimal("0")
                    t_service =  to_decimal("0")
                    t_vat =  to_decimal("0")
                custom_record()
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            output_list.sstr =  to_string("", "x(77)") +\
                    to_string("Grand TOTAL ", "x(12)") +\
                    to_string("", "x(6)") +\
                    format_fixed_length(to_string(gqty), 5) +\
                    format_fixed_length(to_string(tot), 22)
            output_list.amt_nett =  to_decimal(tot_amt)
            output_list.service =  to_decimal(tot_service)
            output_list.vat =  to_decimal(tot_vat)


        else:
            output_list.sstr =  to_string("", "x(77)") +\
                    to_string("Grand TOTAL ", "x(12)") +\
                    to_string("", "x(6)") +\
                    format_fixed_length(to_string(gqty), 5) +\
                    format_fixed_length(to_string(tot), 22)
            output_list.amt_nett =  to_decimal(tot_amt)
            output_list.service =  to_decimal(tot_service)
            output_list.vat =  to_decimal(tot_vat)


        gtot =  to_decimal(tot)
        custom_record()

    if from_date == None:
        return generate_output()

    if to_date == None:
        return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 5) & (Queasy.number3 != 0)).order_by(Queasy.number1).all():
        shift_list = Shift_list()
        shift_list_list.append(shift_list)

        shift_list.shift = queasy.number3
        temp1 = to_string(queasy.number1, "9999")
        temp2 = to_string(queasy.number2, "9999")
        shift_list.ftime = (to_int(substring(temp1, 0, 2)) * 3600) + (to_int(substring(temp1, 2, 2)) * 60)
        shift_list.ttime = (to_int(substring(temp2, 0, 2)) * 3600) + (to_int(substring(temp2, 2, 2)) * 60)
        isoutletshift = True

    journal_list()

    return generate_output()