#using conversion tools version: 1.0.0.105
#-----------------------------------------
# 17-July-25, update INT64() -> int(), 
# if available res_line
#-----------------------------------------

from functions.additional_functions import *
from sqlalchemy import func
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Guest, Artikel, Queasy, Htparam, Bill, Bill_line, Res_line, Reservation, Sourccod, Segment, Genstat, History, Guestseg, Debitor, Hoteldpt, Billjournal, H_bill, Bk_veran, Arrangement, Argt_line, H_journal, H_bill_line
from functions.more_additional_functions import format_fixed_length, handling_negative

from functions import log_program as lp
import traceback

def fo_journal_cld_3bl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, sorttype:int, exclude_artrans:bool, long_digit:bool, foreign_flag:bool, mi_onlyjournal:bool, mi_excljournal:bool, mi_post:bool, mi_showrelease:bool, mi_break:bool, id_flag:string):

    prepare_cache ([Guest, Artikel, Queasy, Htparam, Bill, Res_line, Reservation, Sourccod, Segment, Genstat, History, Guestseg, Debitor, Hoteldpt, Billjournal, H_bill, Bk_veran, H_journal, H_bill_line])

    gtot = to_decimal("0.0")
    output_list_data = []
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
    guest = artikel = queasy = htparam = bill = bill_line = res_line = reservation = sourccod = segment = genstat = history = guestseg = debitor = hoteldpt = billjournal = h_bill = bk_veran = arrangement = argt_line = h_journal = h_bill_line = None

    output_list = shift_list = buffguest = gbuff = shift_buff = b_artikel = None

    output_list_data, Output_list = create_model("Output_list", {"bezeich":string, "c":string, "ns":string, "mb":string, "shift":string, "dept":string, "str":string, "remark":string, "gname":string, "descr":string, "voucher":string, "checkin":date, "checkout":date, "guestname":string, "segcode":string, "amt_nett":Decimal, "service":Decimal, "vat":Decimal, "zinr":string, "deptno":int, "nationality":string, "resnr":int, "book_source":string, "resname":string})
    shift_list_data, Shift_list = create_model("Shift_list", {"shift":int, "ftime":int, "ttime":int})
    
    Buffguest = create_buffer("Buffguest",Guest)
    Gbuff = create_buffer("Gbuff",Guest)
    Shift_buff = Shift_list
    shift_buff_data = shift_list_data

    B_artikel = create_buffer("B_artikel",Artikel)

    db_session = local_storage.db_session

    # Oscar - start - create new session with same search_path for write operation to db and maintain yield__per connection still active
    search_path = db_session.execute(
        text("SELECT current_schema()")
    ).scalar()

    localBind = db_session.get_bind()
    localEngine = localBind.engine if isinstance(localBind, Connection) else localBind

    WriteSessionOnly = sessionmaker(bind=localEngine)

    write_session_only = WriteSessionOnly()

    write_session_only.execute(
        text(f"SET search_path TO {search_path}")
    )
    # Oscar - end - create new session with same search_path for write operation to db and maintain yield__per connection still active


    def generate_output():
        nonlocal gtot, output_list_data, curr_date, descr1, voucher_no, ind, indexing, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, serv, vat, netto, temp_str, hoteldept, shift, temp1, temp2, counter, isoutletshift, guest, artikel, queasy, htparam, bill, bill_line, res_line, reservation, sourccod, segment, genstat, history, guestseg, debitor, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line, h_journal, h_bill_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal buffguest, gbuff, shift_buff, b_artikel


        nonlocal output_list, shift_list, buffguest, gbuff, shift_buff, b_artikel
        nonlocal output_list_data, shift_list_data

        return {"gtot": gtot, "output-list": output_list_data}


    def handle_null_date(inp_date:date):

        nonlocal gtot, output_list_data, curr_date, descr1, voucher_no, ind, indexing, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, serv, vat, netto, temp_str, hoteldept, shift, temp1, temp2, counter, isoutletshift, guest, artikel, queasy, htparam, bill, bill_line, res_line, reservation, sourccod, segment, genstat, history, guestseg, debitor, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line, h_journal, h_bill_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal buffguest, gbuff, shift_buff, b_artikel


        nonlocal output_list, shift_list, buffguest, gbuff, shift_buff, b_artikel
        nonlocal output_list_data, shift_list_data

        if inp_date == None:
            return "" * 8
        else:
            return inp_date.strftime("%m/%d/%y")


    def handle_null_char(inp_char:string):

        nonlocal gtot, output_list_data, curr_date, descr1, voucher_no, ind, indexing, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, serv, vat, netto, temp_str, hoteldept, shift, temp1, temp2, counter, isoutletshift, guest, artikel, queasy, htparam, bill, bill_line, res_line, reservation, sourccod, segment, genstat, history, guestseg, debitor, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line, h_journal, h_bill_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal buffguest, gbuff, shift_buff, b_artikel


        nonlocal output_list, shift_list, buffguest, gbuff, shift_buff, b_artikel
        nonlocal output_list_data, shift_list_data

        if inp_char == None:
            return ""
        else:

            if num_entries(inp_char, "|") > 1:
                inp_char = replace_str(inp_char, "|", "-")
            return inp_char


    def custom_record(artikel_prev:Artikel=None, billjournal_prev:Billjournal=None):

        nonlocal gtot, output_list_data, curr_date, descr1, voucher_no, ind, indexing, gdelimiter, serv, vat, netto, temp_str, hoteldept, shift, temp1, temp2, counter, isoutletshift, guest, artikel, queasy, htparam, bill, bill_line, res_line, reservation, sourccod, segment, genstat, history, guestseg, debitor, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line, h_journal, h_bill_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal buffguest, gbuff, shift_buff, b_artikel

        nonlocal output_list, shift_list, buffguest, gbuff, shift_buff, b_artikel
        nonlocal output_list_data, shift_list_data

        roomnumber:string = ""
        zinrdate:date = date(1,1,1)
        billnumber:int = 0
        curr_str:string = ""
        curr_resnr:int = 0
        journdate:date = date(1,1,1)
        temp_resnr:Decimal = to_decimal("0.0")
        temp_gastnr:Decimal = to_decimal("0.0")
        temp_descr:string = ""
        artikelnr:int = 0
        queasy_str:string = ""

        # htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 110).first()

        if artikel_prev != None:
            artikel = artikel_prev
        if billjournal_prev != None:
            billjournal = billjournal_prev

        if htparam:
            journdate = htparam.fdate

        roomnumber = substring(output_list.str, 8, 6)
        roomnumber = roomnumber.strip()

        tmp_mm = substring(output_list.str, 0, 2)
        tmp_dd = substring(output_list.str, 3, 2)
        tmp_yy = substring(output_list.str, 6, 2)

        # perubahan output_list.sstr 09/24/24 -> membuat string parsing berubah
        # zinrdate = date_mdy(substring(output_list.s, 0, 8))
        if tmp_dd.strip() !="" and tmp_mm.strip() !="" and tmp_yy.strip() !="":
            zinrdate = date(to_int(tmp_yy)+2000, to_int(tmp_mm), to_int(tmp_dd))
        else:
            zinrdate = date(1,1,1)
            
        billnumber = to_int(substring(output_list.str, 14, 9))
        artikelnr = to_int(substring(output_list.str, 23, 9))
        curr_str = " "
        curr_resnr = 0

        if output_list.mb.lower()  == ("*").lower() :

            # bill = get_cache (Bill, {"rechnr": [(eq, billnumber)]})\
            bill = None
            bill = db_session.query(Bill).filter((Bill.rechnr == billnumber)).first()

            bill_line = None
            if bill:
                # bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"zinr": [(eq, roomnumber)]})
                bill_line = db_session.query(Bill_line).filter((Bill_line.rechnr == bill.rechnr) & (Bill_line.zinr == roomnumber)).first()

            res_line = None
            if bill_line:
                # res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, roomnumber)],"ankunft": [(le, zinrdate)],"abreise": [(ge, zinrdate)]})
                res_line = db_session.query(Res_line).filter((Res_line.resnr == bill.resnr) & (Res_line.zinr == roomnumber) & (Res_line.ankunft <= zinrdate) & (Res_line.abreise >= zinrdate)).first()

            # Rd 13/8/2025
            # if res_line available
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
                    output_list.str = output_list.str + format_fixed_length((guest.name + ", " + guest.vorname1 + " " + guest.anrede1), 50)
                    output_list.checkin = res_line.ankunft
                    output_list.checkout = res_line.abreise
                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                    output_list.nationality = guest.nation1
                    output_list.resnr = res_line.resnr
                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                    if reservation.resart != 0:

                        # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                        sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                        if sourccod:
                            output_list.book_source = sourccod.bezeich

                # segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                segment = db_session.query(Segment).filter(Segment.segmentcode == reservation.segmentcode).first()

                if segment:
                    output_list.segcode = segment.bezeich
                else:
                    output_list.segcode = ""

        # Rd 13/8/2025
        # if matches(substring(str, 77, 12),r"*T O T A L*"):
        if matches(substring(output_list.str, 82, 12),r"*T O T A L*"):
            output_list.guestname = ""
            output_list.segcode = ""
            output_list.checkin = None
            output_list.checkout = None
            output_list.str = format_fixed_length(substring(output_list.str, 0, 128), 221)

        # if matches(substring(str, 77, 12),r"*Grand TOTAL*"):
        if matches(substring(output_list.str, 82, 12),r"*Grand TOTAL*"):
            output_list.guestname = ""
            output_list.segcode = ""
            output_list.checkin = None
            output_list.checkout = None
            output_list.str = format_fixed_length(substring(output_list.str, 0, 128), 221)

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

                        # b_artikel = get_cache (Artikel, {"artnr": [(eq, artikelnr)],"departement": [(eq, output_list.deptno)]})
                        b_artikel = db_session.query(Artikel).filter((Artikel.artnr == artikelnr) & (Artikel.departement == output_list.deptno)).first()

                        if b_artikel:
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
                        output_list.str = output_list.str + format_fixed_length((guest.name + ", " + guest.vorname1 + " " + guest.anrede1), 50)
                        output_list.checkin = res_line.ankunft
                        output_list.checkout = res_line.abreise
                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                        output_list.nationality = guest.nation1
                        output_list.resnr = res_line.resnr
                        output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                        if reservation.resart != 0:

                            # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                            sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

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
                    output_list.resname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
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

                    # b_artikel = get_cache (Artikel, {"artnr": [(eq, artikelnr)]})
                    b_artikel = db_session.query(Artikel).filter(Artikel.artnr == artikelnr).first()

                    if b_artikel:
                        temp_resnr = to_decimal(substring(entry(0, output_list.descr, "[") , length(b_artikel.bezeich) + 2 - 1))

            if temp_resnr != 0:

                # res_line = get_cache (Res_line, {"resnr": [(eq, int(temp_resnr))],"reslinnr": [(eq, 1)]})
                res_line = db_session.query(Res_line).filter((Res_line.resnr == int(temp_resnr)) & (Res_line.reslinnr == 1)).first()

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
                        output_list.str = output_list.str + format_fixed_length((guest.name + ", " + guest.vorname1 + " " + guest.anrede1), 50)
                        output_list.checkin = res_line.ankunft
                        output_list.checkout = res_line.abreise
                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                        output_list.nationality = guest.nation1
                        output_list.resnr = res_line.resnr
                        output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                        if reservation.resart != 0:

                            # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                            sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

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
                    output_list.resname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.nationality = guest.nation1

        if roomnumber != "" and billnumber == 0:

            if zinrdate >= journdate:

                # res_line = get_cache (Res_line, {"zinr": [(eq, roomnumber)],"ankunft": [(eq, zinrdate)]})
                res_line = db_session.query(Res_line).filter(Res_line.zinr == roomnumber, Res_line.ankunft == zinrdate).first()

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
                        output_list.str = output_list.str +format_fixed_length((guest.name + ", " + guest.vorname1 + " " + guest.anrede1), 50)
                        output_list.checkin = res_line.ankunft
                        output_list.checkout = res_line.abreise
                        output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                        output_list.nationality = guest.nation1
                        output_list.resnr = res_line.resnr
                        output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                        if reservation.resart != 0:

                            # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                            sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                            if sourccod:
                                output_list.book_source = sourccod.bezeich

                    # segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                    segment = db_session.query(Segment).filter(Segment.segmentcode == reservation.segmentcode).first()

                    if segment:
                        output_list.segcode = segment.bezeich
                    else:
                        output_list.segcode = ""

            elif zinrdate < journdate:

                # genstat = get_cache (Genstat, {"datum": [(eq, zinrdate)],"zinr": [(eq, roomnumber)]})
                genstat = db_session.query(Genstat).filter((Genstat.datum == zinrdate) & (Genstat.zinr == roomnumber)).first()
                
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
                        output_list.str = output_list.str + format_fixed_length((guest.name + ", " + guest.vorname1 + " " + guest.anrede1), 50)
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

                            # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                            sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                            if sourccod:
                                output_list.book_source = sourccod.bezeich

                    # segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                    segment = db_session.query(Segment).filter(Segment.segmentcode == reservation.segmentcode).first()

                    if segment:
                        output_list.segcode = segment.bezeich
                    else:
                        output_list.segcode = ""

        if roomnumber != "" and not res_line:

            bill = db_session.query(Bill).filter(Bill.rechnr == billnumber).first()

            history = None
            if bill:
                history = db_session.query(History).filter((History.resnr == bill.resnr) & (History.zinr == roomnumber) & (History.ankunft <= zinrdate) & (History.abreise >= zinrdate)).first()

            res_line = None
            if history:
                res_line = db_session.query(Res_line).filter((Res_line.resnr == history.resnr) & (Res_line.reslinnr == history.reslinnr) & (Res_line.ankunft <= history.ankunft) & (History.abreise >= history.abreise)).first()

            if res_line:

                reservation = db_session.query(Reservation).filter((Reservation.resnr == res_line.resnr)).first()

                buffguest = db_session.query(Guest).filter((Guest.gastnr == res_line.gastnrpay)).first()

                guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                gbuff = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnr).first()

                if guest and reservation:
                    output_list.str = output_list.str + format_fixed_length((guest.name + ", " + guest.vorname1 + " " + guest.anrede1), 50)
                    output_list.checkin = res_line.ankunft
                    output_list.checkout = res_line.abreise
                    output_list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                    output_list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1
                    output_list.nationality = guest.nation1
                    output_list.resnr = res_line.resnr
                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

                    if reservation.resart != 0:

                        # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                        sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                        if sourccod:
                            output_list.book_source = sourccod.bezeich

                # segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                segment = db_session.query(Segment).filter(Segment.segmentcode == reservation.segmentcode).first()

                if segment:
                    output_list.segcode = segment.bezeich
                else:
                    output_list.segcode = ""

        roomnumber = ""

        if output_list.ns != "" and handle_null_char(output_list.gname) != "" and bill:

            # buffguest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
            buffguest = db_session.query(Guest).filter(Guest.gastnr == bill.gastnr).first()

            # guestseg = get_cache (Guestseg, {"gastnr": [(eq, buffguest.gastnr)]})
            guestseg = db_session.query(Guestseg).filter(Guestseg.gastnr == buffguest.gastnr).first()

            if guestseg:

                # segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                segment = db_session.query(Segment).filter(Segment.segmentcode == guestseg.segmentcode).first()

                if segment:
                    output_list.segcode = segment.bezeich
                else:
                    output_list.segcode = "UNKNOWN"
            else:
                output_list.segcode = "UNKNOWN"

        if billjournal and exclude_artrans == False and artikel.artart != 4:

            # debitor = get_cache (Debitor, {"rechnr": [(eq, billjournal.rechnr)],"zahlkonto": [(eq, billjournal.artnr)],"rgdatum": [(eq, billjournal.bill_datum)],"zinr": [(eq, billjournal.zinr)],"saldo": [(eq, billjournal.betrag)],"transzeit": [(eq, billjournal.zeit)]})
            debitor = db_session.query(Debitor).filter((Debitor.rechnr == billjournal.rechnr) & 
                                                       (Debitor.zahlkonto == billjournal.artnr) & 
                                                       (Debitor.rgdatum == billjournal.bill_datum) & 
                                                       (Debitor.zinr == billjournal.zinr) & 
                                                       (Debitor.saldo == billjournal.betrag) & 
                                                       (Debitor.transzeit == billjournal.zeit)).first()

            if debitor:

                # b_artikel = get_cache (Artikel, {"artnr": [(eq, debitor.artnr)]})
                b_artikel = db_session.query(Artikel).filter(Artikel.artnr == debitor.artnr).first()

                if b_artikel:
                    output_list.descr = "A/R Transfer from " + to_string(debitor.artnr) + " " + b_artikel.bezeich

        queasy = Queasy()

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
        queasy_str = format_fixed_length(output_list.c, 2) +\
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
                handling_negative(output_list.deptno , ">9") +\
                format_fixed_length(handle_null_char (output_list.nationality) , 5) +\
                handling_negative(output_list.resnr , "->>>>>>>>9") +\
                format_fixed_length(handle_null_char (output_list.book_source) , 20) +\
                format_fixed_length(handle_null_char (output_list.resname) , 25) +\
                " " + handling_negative(output_list.amt_nett , "->>>,>>>,>>>,>>9.99") +\
                " " + handling_negative(output_list.service , "->>>,>>>,>>>,>>9.99") +\
                " " + handling_negative(output_list.vat , "->>>,>>>,>>>,>>9.99")
        
        output_list.str = format_fixed_length(output_list.str, 220)
        
        queasy.key = 280
        queasy.char1 = "FO Transaction"
        queasy.char2 = id_flag
        queasy.char3 = output_list.str + "|" + queasy_str
        queasy.number1 = counter


        write_session_only.add(queasy)
        write_session_only.commit()

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

        nonlocal gtot, output_list_data, descr1, voucher_no, ind, indexing, gdelimiter, roomnumber, zinrdate, billnumber, curr_str, curr_resnr, serv, vat, netto, temp_str, hoteldept, shift, temp1, temp2, counter, isoutletshift, guest, artikel, queasy, htparam, bill, bill_line, res_line, reservation, sourccod, segment, genstat, history, guestseg, debitor, hoteldpt, billjournal, h_bill, bk_veran, arrangement, argt_line, h_journal, h_bill_line
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, mi_onlyjournal, mi_excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal buffguest, gbuff, shift_buff, b_artikel


        nonlocal output_list, shift_list, buffguest, gbuff, shift_buff, b_artikel

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
        output_list_data.clear()

        

        # for artikel in db_session.query(Artikel).filter((Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement >= from_dept) & (Artikel.departement <= to_dept)).order_by((Artikel.departement * 10000 + Artikel.artnr)).all():

        #     if last_dept != artikel.departement:
        #         hoteldpt = get_cache (Hoteldpt, {"num": [(eq, artikel.departement)]})

        #     last_dept = artikel.departement
        #     sub_tot =  to_decimal("0")
        #     it_exist = False
        #     qty = 0

        q_stmt = db_session.query(Artikel.departement,
                                    Artikel.artart,
                                    Artikel.artnr,
                                    Artikel.bezeich,
                                    Artikel.service_code,
                                    Artikel.mwst_code,
                                    Artikel.bezaendern,
                                    Artikel._recid,
                                    Billjournal.bediener_nr,
                                    Billjournal.kassarapport,
                                    Billjournal.betrag,
                                    Billjournal.rechnr,
                                    Billjournal.artnr,
                                    Billjournal.bill_datum,
                                    Billjournal.zinr,
                                    Billjournal.zeit,
                                    Billjournal.stornogrund,
                                    Billjournal.bezeich,
                                    Billjournal.betriebsnr,
                                    Billjournal.departement,
                                    Billjournal.anzahl,
                                    Billjournal.fremdwaehrng,
                                    Billjournal.userinit,
                                    Billjournal.sysdate,
                                    Billjournal._recid)\
        .outerjoin(Billjournal, (Billjournal.artnr == Artikel.artnr))\
        .filter((Artikel.artnr >= from_art) & 
                (Artikel.artnr <= to_art) &
                (Artikel.departement >= from_dept) & 
                (Artikel.departement <= to_dept) &
                (Billjournal.departement == Artikel.departement))\
        .order_by(Artikel.departement,
                    Artikel.artnr,
                    Billjournal.sysdate, 
                    Billjournal.zeit, 
                    Billjournal.zinr)
        
        if sorttype == 0:
            q_stmt = q_stmt.filter((Billjournal.anzahl != 0) & (Billjournal.bill_datum >= from_date) & (Billjournal.bill_datum <= to_date))
        elif sorttype == 1:
            q_stmt = q_stmt.filter((Billjournal.bill_datum >= from_date) & (Billjournal.bill_datum <= to_date))
        elif sorttype == 2:
            q_stmt = q_stmt.filter((Billjournal.anzahl == 0))
            if mi_post:
                q_stmt = q_stmt.filter((Billjournal.bill_datum >= from_date) & (Billjournal.bill_datum <= to_date))
            else:
                q_stmt = q_stmt.filter((Billjournal.sysdate >= from_date) & (Billjournal.sysdate <= to_date))

        artikel = Artikel()
        billjournal = Billjournal()
        
        curr_artikel_recid = "none"
        artikel_prev = None
        billjournal_prev = None

        for row in q_stmt.yield_per(100):

            (artikel_department, artikel_artart, artikel_artnr, artikel_bezeich, artikel_service_code, artikel_mwst_code, artikel_bezaendern, artikel_recid, billjournal_bediener_nr, billjournal_kassarapport, billjournal_betrag, billjournal_rechnr, billjournal_artnr, billjournal_bill_datum, billjournal_zinr, billjournal_zeit, billjournal_stornogrund, billjournal_bezeich, billjournal_betriebsnr, billjournal_departement, billjournal_anzahl, billjournal_fremdwaehrng, billjournal_userinit, billjournal_sysdate, billjournal_prev_recid) = row

            if curr_artikel_recid != artikel_recid:

                if curr_artikel_recid != "none":
                    if it_exist:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        if not long_digit:
                            output_list.str =  format_fixed_length("", 82) + format_fixed_length("T O T A L ", 12) + format_fixed_length("", 6) + handling_negative(qty, "-9999") + handling_negative(sub_tot, "->>,>>>,>>>,>>>,>>9.99")
                            output_list.amt_nett =  to_decimal(t_amt)
                            output_list.service =  to_decimal(t_service)
                            output_list.vat =  to_decimal(t_vat)
                            t_amt =  to_decimal("0")
                            t_service =  to_decimal("0")
                            t_vat =  to_decimal("0")
                        else:
                            output_list.str =  format_fixed_length("", 82) + format_fixed_length("T O T A L ", 12) + format_fixed_length("", 6) + handling_negative(qty, "-9999") + handling_negative(sub_tot, "->,>>>,>>>,>>>,>>>,>>9")
                            output_list.amt_nett =  to_decimal(t_amt)
                            output_list.service =  to_decimal(t_service)
                            output_list.vat =  to_decimal(t_vat)
                            t_amt =  to_decimal("0")
                            t_service =  to_decimal("0")
                            t_vat =  to_decimal("0")
                        
                        custom_record(artikel_prev, billjournal_prev)

                if last_dept != artikel_department:
                    # hoteldpt = get_cache (Hoteldpt, {"num": [(eq, artikel_department)]})
                    hoteldpt = db_session.query(Hoteldpt).filter(Hoteldpt.num == artikel_department).first()

                last_dept = artikel_department
                sub_tot =  to_decimal("0")
                it_exist = False
                qty = 0

                curr_artikel_recid = artikel_recid

            artikel_prev = Artikel()
            artikel_prev.departement = artikel_department
            artikel_prev.artart = artikel_artart
            artikel_prev.artnr = artikel_artnr
            artikel_prev.bezeich = artikel_bezeich
            artikel_prev.service_code = artikel_service_code
            artikel_prev.mwst_code = artikel_mwst_code
            artikel_prev.bezaendern = artikel_bezaendern
            artikel_prev._recid = artikel_recid

            billjournal_prev = Billjournal()
            billjournal_prev.bediener_nr = billjournal_bediener_nr
            billjournal_prev.kassarapport = billjournal_kassarapport
            billjournal_prev.betrag = billjournal_betrag
            billjournal_prev.rechnr = billjournal_rechnr
            billjournal_prev.artnr = billjournal_artnr
            billjournal_prev.bill_datum = billjournal_bill_datum
            billjournal_prev.zinr = billjournal_zinr
            billjournal_prev.zeit = billjournal_zeit
            billjournal_prev.stornogrund = billjournal_stornogrund
            billjournal_prev.bezeich = billjournal_bezeich
            billjournal_prev.betriebsnr = billjournal_betriebsnr
            billjournal_prev.departement = billjournal_departement
            billjournal_prev.anzahl = billjournal_anzahl
            billjournal_prev.fremdwaehrng = billjournal_fremdwaehrng
            billjournal_prev.userinit = billjournal_userinit
            billjournal_prev.sysdate = billjournal_sysdate
            billjournal_prev._recid = billjournal_prev_recid

            do_it = True

            if (mi_onlyjournal  and billjournal_bediener_nr == 0) or (mi_excljournal  and billjournal_bediener_nr != 0):
                do_it = False

            if exclude_artrans and billjournal_kassarapport:
                do_it = False

            if not mi_showrelease and billjournal_betrag == 0:
                do_it = False

            if do_it and exclude_artrans and artikel_artart != 4:
                # debitor = get_cache (Debitor, {"rechnr": [(eq, billjournal_rechnr)],"zahlkonto": [(eq, billjournal_artnr)],"rgdatum": [(eq, billjournal_bill_datum)],"zinr": [(eq, billjournal_zinr)],"saldo": [(eq, billjournal_betrag)],"transzeit": [(eq, billjournal_zeit)]})
                debitor = db_session.query(Debitor).filter((Debitor.rechnr == billjournal_rechnr) &
                                                            (Debitor.zahlkonto == billjournal_artnr) &
                                                            (Debitor.rgdatum == billjournal_bill_datum) &
                                                            (Debitor.zinr == billjournal_zinr) &
                                                            (Debitor.saldo == billjournal_betrag) &
                                                            (Debitor.transzeit == billjournal_zeit)).first()

                if debitor:
                    do_it = False

            if do_it:

                it_exist = True
                output_list = Output_list()
                output_list_data.append(output_list)

                if (billjournal_bediener_nr == 0 and mi_onlyjournal == False) or (billjournal_bediener_nr != 0 and mi_excljournal == False):
                    output_list.remark = billjournal_stornogrund

                if not matches(billjournal_bezeich, ("*<*")) and not matches(billjournal_bezeich, ("*>*")):

                    if billjournal_rechnr > 0:

                        if billjournal_bediener_nr == 0 and mi_onlyjournal == False:
                            
                            # bill = get_cache (Bill, {"rechnr": [(eq, billjournal_rechnr)]})
                            bill = db_session.query(Bill).filter(Bill.rechnr == billjournal_rechnr).first()

                            if bill and billjournal_zinr != "":
                                # res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, bill.zinr)]})
                                res_line = db_session.query(Res_line).filter(Res_line.resnr == bill.resnr, Res_line.zinr == bill.zinr).first()

                                # Rd 13/8/2025
                                # if res_line
                                if res_line:
                                    # reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                                    reservation = db_session.query(Reservation).filter(Reservation.resnr == bill.resnr).first()

                                    # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                    guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()

                                    # buffguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                                    buffguest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrpay).first()

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

                                            # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                                            sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                                            if sourccod:
                                                output_list.book_source = sourccod.bezeich

                                        # segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                        segment = db_session.query(Segment).filter(Segment.segmentcode == reservation.segmentcode).first()

                                        if segment:
                                            output_list.segcode = segment.bezeich
                                        else:
                                            output_list.segcode = ""

                            elif bill:
                                if bill.resnr == 0 and bill.bilname.strip() != "":
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

                        elif billjournal_bediener_nr != 0 and mi_excljournal == False:

                            # h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal_rechnr)],"departement": [(eq, billjournal_betriebsnr)]})
                            h_bill = db_session.query(H_bill).filter((H_bill.rechnr == billjournal_rechnr) & (H_bill.departement == billjournal_betriebsnr)).first()

                            if h_bill:

                                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                    # res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})
                                    res_line = db_session.query(Res_line).filter((Res_line.resnr == h_bill.resnr) & (Res_line.reslinnr == h_bill.reslinnr)).first()

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

                                        segment = None
                                        if genstat:
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

                                elif billjournal_betriebsnr == 0:

                                    # bill = get_cache (Bill, {"rechnr": [(eq, billjournal_rechnr)]})
                                    bill = db_session.query(Bill).filter(Bill.rechnr == billjournal_rechnr).first()

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

                                            segment = None
                                            if genstat:
                                                # segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                                                segment = db_session.query(Segment).filter(Segment.segmentcode == genstat.segmentcode).first()


                                            if not segment:
                                                output_list.segcode = ""
                                            else:
                                                output_list.segcode = segment.bezeich
                    else:

                        if get_index(billjournal_bezeich, " *BQT") > 0:

                            # bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, to_int(substring(billjournal_bezeich, get_index(billjournal_bezeich, " *bqt") + 5  - 1)))]})
                            bk_veran = db_session.query(Bk_veran).filter(Bk_veran.veran_nr == to_int(substring(billjournal_bezeich, get_index(billjournal_bezeich, " *bqt") + 5  - 1))).first()

                            if bk_veran:

                                # gbuff = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})
                                gbuff = db_session.query(Gbuff).filter(Gbuff.gastnr == bk_veran.gastnr).first()

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                    output_list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                    output_list.resname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                    output_list.nationality = gbuff.nation1

                        elif artikel_artart == 5 and get_index(billjournal_bezeich, " [#") > 0 and billjournal_departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal_bezeich, get_index(billjournal_bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            # reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})
                            reservation = db_session.query(Reservation).filter(Reservation.resnr == lviresnr).first()

                            if reservation:

                                # gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
                                gbuff = db_session.query(Gbuff).filter(Gbuff.gastnr == reservation.gastnr).first()

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

                        elif get_index(billjournal_bezeich, " #") > 0 and billjournal_departement == 0:
                            lvcs = substring(billjournal_bezeich, get_index(billjournal_bezeich, " #") + 2 - 1)
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

                    # arrangement = get_cache (Arrangement, {"artnr_logis": [(eq, artikel_artnr)],"intervall": [(eq, artikel_department)]})
                    arrangement = db_session.query(Arrangement).filter((Arrangement.artnr_logis == artikel_artnr) & (Arrangement.intervall == artikel_department)).first()

                    if arrangement:

                        # h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal_rechnr)],"departement": [(eq, billjournal_departement)]})
                        h_bill = db_session.query(H_bill).filter((H_bill.rechnr == billjournal_rechnr) & (H_bill.departement == billjournal_departement)).first()

                        if h_bill:

                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                # res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})
                                res_line = db_session.query(Res_line).filter((Res_line.resnr == h_bill.resnr) & (Res_line.reslinnr == h_bill.reslinnr)).first()


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

                                        # sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
                                        sourccod = db_session.query(Sourccod).filter(Sourccod.source_code == reservation.resart).first()

                                        if sourccod:
                                            output_list.book_source = sourccod.bezeich

                                    # genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})
                                    genstat = db_session.query(Genstat).filter(Genstat.resnr == res_line.resnr).first()

                                    segment = None
                                    if genstat:
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

                        # argt_line = get_cache (Argt_line, {"argt_artnr": [(eq, artikel_artnr)],"departement": [(eq, artikel_department)]})
                        argt_line = db_session.query(Argt_line).filter((Argt_line.argt_artnr == artikel_artnr) & (Argt_line.departement == artikel_department)).first()

                        if argt_line:
                            hoteldept = billjournal_departement

                            if matches(billjournal_bezeich, ("*<*")) and matches(billjournal_bezeich, ("*>*")):
                                hoteldept = to_int(substring(billjournal_bezeich, get_index(billjournal_bezeich, "<") + 1 - 1, get_index(billjournal_bezeich, ">") - get_index(billjournal_bezeich, "<") - 1))

                            # h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal_rechnr)],"departement": [(eq, hoteldept)]})


                            if h_bill:

                                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                    # res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})
                                    res_line = db_session.query(Res_line).filter((Res_line.resnr == h_bill.resnr) & (Res_line.reslinnr == h_bill.reslinnr)).first()

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

                                        # genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)]})
                                        genstat = db_session.query(Genstat).filter(Genstat.resnr == res_line.resnr).first()

                                        segment = None
                                        if genstat:
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

                if (billjournal_bediener_nr != 0 and mi_excljournal == False and billjournal_anzahl == 0) or (billjournal_bediener_nr == 0 and mi_onlyjournal == False and billjournal_anzahl == 0):
                    output_list.bezeich = artikel_bezeich

                if billjournal_bediener_nr != 0 and mi_excljournal == False:
                    shift = 0

                    if billjournal_betriebsnr != 0 and isoutletshift :

                        # h_journal = get_cache (H_journal, {"rechnr": [(eq, billjournal_rechnr)],"departement": [(eq, billjournal_betriebsnr)]})

                        # if h_journal:

                        #     shift_list = query(shift_list_data, filters=(lambda shift_list: shift_list.ftime <= h_journal.zeit and shift_list.ttime >= h_journal.zeit), first=True)

                        #     if shift_list:
                        #         shift = shift_list.shift
                        #     else:

                        #         shift_buff = query(shift_buff_data, filters=(lambda shift_buff: shift_buff.ftime >= shift_buff.ttime), first=True)

                        #         if shift_buff:
                        #             shift = shift_buff.shift

                        h_bill_line = db_session.query(H_bill_line).filter((H_bill_line.rechnr == billjournal_rechnr) & (H_bill_line.departement == billjournal_betriebsnr) & (H_bill_line.betriebsnr != 0)).first()
                        if h_bill_line:
                            shift = h_bill_line.betriebsnr

                    output_list.c = handling_negative(billjournal_betriebsnr, "99")
                    output_list.shift = handling_negative(shift, "99")

                elif billjournal_bediener_nr == 0 and mi_onlyjournal == False:

                    if bill:

                        if bill.reslinnr == 1 and bill.zinr == "":
                            output_list.c = "N"
                            output_list.ns = "*"

                        elif bill.reslinnr == 0:
                            output_list.c = "M"
                            output_list.mb = "*"

                if foreign_flag:
                    amount =  to_decimal(billjournal_fremdwaehrng)
                else:
                    amount =  to_decimal(billjournal_betrag)

                if mi_break :
                    serv =  to_decimal("0")
                    vat =  to_decimal("0")


                    serv, vat = get_output(calc_servvat(artikel_department, artikel_artnr, billjournal_bill_datum, artikel_service_code, artikel_mwst_code))
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

                if substring(billjournal_bezeich, 0, 1) == ("*").lower()  or billjournal_kassarapport:
                    descr1 = billjournal_bezeich
                    voucher_no = ""
                else:

                    if not artikel_bezaendern:
                        ind = num_entries(billjournal_bezeich, "]")

                        if ind >= 2:
                            gdelimiter = "]"
                        else:
                            ind = num_entries(billjournal_bezeich, "/")

                            if ind >= 2 and length(artikel_bezeich) <= get_index(billjournal_bezeich, "/") and billjournal_betrag != 0:
                                gdelimiter = "/"
                            else:
                                ind = num_entries(billjournal_bezeich, "|")

                                if ind >= 2:
                                    gdelimiter = "|"

                        if ind != 0:

                            if ind == 1:
                                descr1 = billjournal_bezeich
                                voucher_no = ""

                            elif ind == 2:
                                descr1 = entry(0, billjournal_bezeich, gdelimiter)
                                voucher_no = entry(1, billjournal_bezeich, gdelimiter)

                                if gdelimiter.lower()  == ("]").lower() :
                                    descr1 = descr1 + gdelimiter

                            elif ind > 2:
                                voucher_no = ""
                                descr1 = entry(0, billjournal_bezeich, gdelimiter)
                                for loopind in range(2,ind + 1) :
                                    voucher_no = voucher_no + entry(loopind - 1, billjournal_bezeich, gdelimiter) + gdelimiter
                                voucher_no = substring(voucher_no, 0, length(voucher_no) - 1)
                        else:
                            descr1 = billjournal_bezeich
                    else:
                        ind = num_entries(billjournal_bezeich, "/")

                        if ind == 1:
                            descr1 = billjournal_bezeich
                            voucher_no = ""

                        elif ind == 2:
                            descr1 = entry(0, billjournal_bezeich, "/")
                            voucher_no = entry(1, billjournal_bezeich, "/")

                        elif ind > 2:
                            descr1 = entry(0, billjournal_bezeich, "/")
                            for loopind in range(2,ind + 1) :
                                voucher_no = voucher_no + entry(loopind - 1, billjournal_bezeich, "/") + "/"
                            voucher_no = substring(voucher_no, 0, length(voucher_no) - 1)
                        else:
                            descr1 = billjournal_bezeich

                if output_list:
                    output_list.descr = format_fixed_length(descr1, 100)
                    output_list.voucher = format_fixed_length(voucher_no, 40)

                if billjournal_bediener_nr == 0 and mi_onlyjournal == False:

                    # hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal_departement)]})
                    hoteldpt = db_session.query(Hoteldpt).filter(Hoteldpt.num == billjournal_departement).first()

                    if hoteldpt:
                        deptname = hoteldpt.depart

                    output_list.zinr = billjournal_zinr
                    output_list.deptno = billjournal_departement

                    if matches(billjournal_bezeich,r"*Deposit*") and billjournal_bezeich.find("[") > 0 and billjournal_bezeich.find("#") and billjournal_rechnr != 0:
                        if not long_digit:
                            output_list.str = handle_null_date(billjournal_bill_datum) + format_fixed_length(handle_null_char(billjournal_zinr), 6) + handling_negative(billjournal_rechnr, "999999999") + handling_negative(billjournal_artnr, "9999") + format_fixed_length(handle_null_char(descr1), 50) + format_fixed_length(handle_null_char(deptname), 12) + handling_negative(billjournal_betriebsnr, ">>>>>9") + handling_negative(billjournal_anzahl, "-9999") + handling_negative(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(billjournal_zeit, "HH:MM:SS") + format_fixed_length(billjournal_userinit, 4) + handle_null_date(billjournal_sysdate) + format_fixed_length(handle_null_char(voucher_no), 24)
                        else:
                            output_list.str =  handle_null_date(billjournal_bill_datum) + format_fixed_length(handle_null_char (billjournal_zinr) , 6) + handling_negative(billjournal_rechnr, "999999999") + handling_negative(billjournal_artnr, "9999") + format_fixed_length(handle_null_char (billjournal_bezeich) , 50) + format_fixed_length(handle_null_char(deptname) , 12) + handling_negative(billjournal_betriebsnr, ">>>>>9") + handling_negative(billjournal_anzahl, "-9999") + handling_negative(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(billjournal_zeit, "HH:MM:SS") + format_fixed_length(handle_null_char(billjournal_userinit), 4) + handle_null_date(billjournal_sysdate) + format_fixed_length(handle_null_char(voucher_no), 24)
                    else:
                        if not long_digit:
                            output_list.str = handle_null_date(billjournal_bill_datum) + format_fixed_length(handle_null_char(billjournal_zinr), 6) + handling_negative(billjournal_rechnr, "999999999") + handling_negative(billjournal_artnr, "999999999") + format_fixed_length(handle_null_char(descr1), 50) + format_fixed_length(handle_null_char(deptname), 12) + format_fixed_length("", 6) + handling_negative(billjournal_anzahl, "-9999") + handling_negative(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(billjournal_zeit, "HH:MM:SS") + format_fixed_length(handle_null_char(billjournal_userinit), 4) + handle_null_date(billjournal_sysdate) + format_fixed_length(handle_null_char(voucher_no), 24)
                        else:
                            output_list.str =  handle_null_date(billjournal_bill_datum) + format_fixed_length(handle_null_char(billjournal_zinr), 6) + handling_negative(billjournal_rechnr, "999999999") + handling_negative(billjournal_artnr, "999999999") + format_fixed_length(handle_null_char(billjournal_bezeich), 50) + format_fixed_length(handle_null_char(deptname) , 12) + format_fixed_length("", 6) + handling_negative(billjournal_anzahl, "-9999") + handling_negative(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(billjournal_zeit, "HH:MM:SS") + format_fixed_length(handle_null_char(billjournal_userinit), 4) + handle_null_date(billjournal_sysdate) + format_fixed_length(handle_null_char(voucher_no), 24)
                    
                    qty = qty + billjournal_anzahl
                    gqty = gqty + billjournal_anzahl

                    if foreign_flag:
                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal_fremdwaehrng)
                        tot =  to_decimal(tot) + to_decimal(billjournal_fremdwaehrng)
                    else:
                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal_betrag)
                        tot =  to_decimal(tot) + to_decimal(billjournal_betrag)

                elif billjournal_bediener_nr != 0 and mi_excljournal == False:

                    # hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal_departement)]})
                    hoteldpt = db_session.query(Hoteldpt).filter(Hoteldpt.num == billjournal_departement).first()

                    if hoteldpt:
                        deptname = hoteldpt.depart

                    output_list.zinr = billjournal_zinr
                    output_list.deptno = billjournal_departement

                    if not long_digit:
                        output_list.str = handle_null_date(billjournal_bill_datum) + format_fixed_length(handle_null_char(billjournal_zinr) , 6) + handling_negative(billjournal_rechnr, "999999999") + handling_negative(billjournal_artnr, "999999999") + format_fixed_length(handle_null_char(descr1), 50) + format_fixed_length(handle_null_char(deptname) , 12) + handling_negative(billjournal_betriebsnr, ">>>>>9") + handling_negative(billjournal_anzahl, "-9999") + handling_negative(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(billjournal_zeit, "HH:MM:SS") + format_fixed_length(handle_null_char(billjournal_userinit) , 4) + handle_null_date(billjournal_sysdate) + format_fixed_length(handle_null_char (voucher_no) , 24)
                    else:
                        output_list.str = handle_null_date(billjournal_bill_datum) + format_fixed_length(handle_null_char(billjournal_zinr) , 6) + handling_negative(billjournal_rechnr, "999999999") + handling_negative(billjournal_artnr, "999999999") + format_fixed_length(handle_null_char(billjournal_bezeich), 50) + format_fixed_length(handle_null_char(deptname) , 12) + handling_negative(billjournal_betriebsnr, ">>>>>9") + handling_negative(billjournal_anzahl, "-9999") + handling_negative(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(billjournal_zeit, "HH:MM:SS") + format_fixed_length(handle_null_char(billjournal_userinit), 4) + handle_null_date(billjournal_sysdate) + format_fixed_length(handle_null_char(voucher_no), 24)

                    qty = qty + billjournal_anzahl
                    gqty = gqty + billjournal_anzahl

                    if foreign_flag:
                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal_fremdwaehrng)
                        tot =  to_decimal(tot) + to_decimal(billjournal_fremdwaehrng)
                    else:
                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal_betrag)
                        tot =  to_decimal(tot) + to_decimal(billjournal_betrag)

                elif mi_excljournal:

                    # hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal_departement)]})
                    hoteldpt = db_session.query(Hoteldpt).filter(Hoteldpt.num == billjournal_departement).first()

                    if hoteldpt:
                        deptname = hoteldpt.depart

                    output_list.zinr = billjournal_zinr
                    output_list.deptno = billjournal_departement

                    if not long_digit:
                        output_list.str =  handle_null_date(billjournal_bill_datum) + format_fixed_length(handle_null_char(billjournal_zinr) , 6) + handling_negative(billjournal_rechnr, "999999999") + handling_negative(billjournal_artnr, "999999999") + format_fixed_length(handle_null_char (descr1) , 50) + format_fixed_length(handle_null_char (deptname) , 12) + handling_negative(billjournal_betriebsnr, ">>>>>9") + handling_negative(billjournal_anzahl, "-9999") + handling_negative(amount, "->>,>>>,>>>,>>>,>>9.99") + to_string(billjournal_zeit, "HH:MM:SS") + format_fixed_length(handle_null_char(billjournal_userinit) , 4) + handle_null_date(billjournal_sysdate) + format_fixed_length(handle_null_char(voucher_no), 24)
                    else:
                        output_list.str =  handle_null_date(billjournal_bill_datum) + format_fixed_length(handle_null_char(billjournal_zinr) , 6) + handling_negative(billjournal_rechnr, "999999999") + handling_negative(billjournal_artnr, "999999999") + format_fixed_length(handle_null_char (billjournal_bezeich) , 50) + format_fixed_length(handle_null_char (deptname) , 12) + handling_negative(billjournal_betriebsnr, ">>>>>9") + handling_negative(billjournal_anzahl, "-9999") + handling_negative(amount, "->,>>>,>>>,>>>,>>>,>>9") + to_string(billjournal_zeit, "HH:MM:SS") + format_fixed_length(handle_null_char(billjournal_userinit) , 4) + handle_null_date(billjournal_sysdate) + format_fixed_length(handle_null_char(voucher_no), 24)

                    qty = qty + billjournal_anzahl
                    gqty = gqty + billjournal_anzahl

                    if foreign_flag:
                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal_fremdwaehrng)
                        tot =  to_decimal(tot) + to_decimal(billjournal_fremdwaehrng)
                    else:
                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal_betrag)
                        tot =  to_decimal(tot) + to_decimal(billjournal_betrag)

                if res_line and res_line.ankunft == res_line.abreise and artikel_department > 0:
                    qty = qty - billjournal_anzahl + res_line.erwachs
                    gqty = gqty - billjournal_anzahl + res_line.erwachs
                    temp_str = substring(output_list.str, 120)

                    output_list.str =  substring(output_list.str, 0, 95)
                    output_list.str =  output_list.str + handling_negative(res_line.erwachs, "-9999") + temp_str

                    temp_str = ""

                custom_record(artikel_prev, billjournal_prev)

        if curr_artikel_recid != "none":
            if it_exist:
                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    output_list.str =  to_string("", "x(82)") + to_string("T O T A L ", "x(12)") + to_string("", "x(6)") + handling_negative(qty, "-9999") + handling_negative(sub_tot, "->>,>>>,>>>,>>>,>>9.99")
                    output_list.amt_nett =  to_decimal(t_amt)
                    output_list.service =  to_decimal(t_service)
                    output_list.vat =  to_decimal(t_vat)
                    t_amt =  to_decimal("0")
                    t_service =  to_decimal("0")
                    t_vat =  to_decimal("0")
                else:
                    output_list.str =  to_string("", "x(82)") + to_string("T O T A L ", "x(12)") + to_string("", "x(6)") + handling_negative(qty, "-9999") + handling_negative(sub_tot, "->,>>>,>>>,>>>,>>>,>>9")
                    output_list.amt_nett =  to_decimal(t_amt)
                    output_list.service =  to_decimal(t_service)
                    output_list.vat =  to_decimal(t_vat)
                    t_amt =  to_decimal("0")
                    t_service =  to_decimal("0")
                    t_vat =  to_decimal("0")
                    
                custom_record(artikel_prev, billjournal_prev)

        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            output_list.str =  to_string("", "x(82)") +\
                    to_string("Grand TOTAL ", "x(12)") +\
                    to_string("", "x(6)") +\
                    handling_negative(gqty, "-9999") +\
                    handling_negative(tot, "->>,>>>,>>>,>>>,>>9.99")
            
            output_list.amt_nett =  to_decimal(tot_amt)
            output_list.service =  to_decimal(tot_service)
            output_list.vat =  to_decimal(tot_vat)
        else:
            output_list.str =  to_string("", "x(82)") +\
                    to_string("Grand TOTAL ", "x(12)") +\
                    to_string("", "x(6)") +\
                    handling_negative(gqty, "-9999") +\
                    handling_negative(tot, "->,>>>,>>>,>>>,>>>,>>9")
            
            output_list.amt_nett =  to_decimal(tot_amt)
            output_list.service =  to_decimal(tot_service)
            output_list.vat =  to_decimal(tot_vat)

        gtot =  to_decimal(tot)

        custom_record()

    if from_date == None:
        return generate_output()

    if to_date == None:
        return generate_output()

    # for queasy in db_session.query(Queasy).filter(
    #          (Queasy.key == 5) & (Queasy.number3 != 0)).order_by(Queasy.number1).all():
        
    #     shift_list = Shift_list()
    #     shift_list_data.append(shift_list)

    #     shift_list.shift = queasy.number3
    #     temp1 = to_string(queasy.number1, "9999")
    #     temp2 = to_string(queasy.number2, "9999")
    #     shift_list.ftime = (to_int(substring(temp1, 0, 2)) * 3600) + (to_int(substring(temp1, 2, 2)) * 60)
    #     shift_list.ttime = (to_int(substring(temp2, 0, 2)) * 3600) + (to_int(substring(temp2, 2, 2)) * 60)
    #     isoutletshift = True

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 5) & (Queasy.number3 != 0)).order_by(Queasy.number1).first()
    if queasy:
        isoutletshift = True

    try:
        journal_list()
    except Exception as e:
        tb = traceback.format_exc()
        lp.write_log("error",f"Exception occurred:\n{tb}\n")

    write_session_only.close()

    return generate_output()