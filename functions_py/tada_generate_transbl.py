#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill_line, Queasy, Bill, Res_line, Reservation, Segment, Sourccod, Guest, Zimmer

def tada_generate_transbl(from_date:date, to_date:date):

    prepare_cache ([Bill_line, Queasy, Bill, Res_line, Reservation, Segment, Sourccod, Guest, Zimmer])

    sftp_localpath = ""
    filetimestamp = ""
    terminalid = ""
    output_list_data = []
    deptnr:int = 0
    programid:string = ""
    walletid:string = ""
    tada_sku:string = ""
    tada_item:string = ""
    segment_list:string = ""
    prefix:string = ""
    phnumb:string = ""
    bill_line = queasy = bill = res_line = reservation = segment = sourccod = guest = zimmer = None

    output_list = bline = None

    output_list_data, Output_list = create_model("Output_list", {"timestamp":string, "billnumber":int, "amount":Decimal, "terminalid":string, "phone":string, "programid":string, "walletid":string, "sku":string, "itemname":string, "qty":string, "price":Decimal, "price_str":string, "paymentmethod":string, "zinr":string, "resnr":int, "reslinnr":int, "gastnrmember":int, "segment":string, "sob":string, "send_date":date, "data_date":date})

    Bline = create_buffer("Bline",Bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sftp_localpath, filetimestamp, terminalid, output_list_data, deptnr, programid, walletid, tada_sku, tada_item, segment_list, prefix, phnumb, bill_line, queasy, bill, res_line, reservation, segment, sourccod, guest, zimmer
        nonlocal from_date, to_date
        nonlocal bline


        nonlocal output_list, bline
        nonlocal output_list_data

        return {"sftp_localpath": sftp_localpath, "filetimestamp": filetimestamp, "terminalid": terminalid, "output-list": output_list_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 1) & (Queasy.betriebsnr == 1)).order_by(Queasy._recid).all():

        if queasy.number2 == 6:
            programid = queasy.char2

        elif queasy.number2 == 7:
            walletid = queasy.char2

        elif queasy.number2 == 11:
            terminalid = queasy.char2

        elif queasy.number2 == 17:
            sftp_localpath = queasy.char2

        elif queasy.number2 == 18:
            segment_list = queasy.char2

        elif queasy.number2 == 19:
            deptnr = to_int(queasy.char2)

    for bill_line in db_session.query(Bill_line).filter(
             (Bill_line.bill_datum >= from_date) & (Bill_line.bill_datum <= to_date) & (Bill_line.departemen == 0) & (Bill_line.artnr == 99) & (Bill_line.betrag > 0)).order_by(Bill_line._recid).all():

        bill = get_cache (Bill, {"rechnr": [(eq, bill_line.rechnr)]})

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"zinr": [(eq, bill_line.zinr)]})

        if res_line:

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            zimmer = get_cache (Zimmer, {"zinr": [(eq, bill_line.zinr)]})

            output_list = query(output_list_data, filters=(lambda output_list: output_list.billnumber == bill.rechnr), first=True)

            if not output_list:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.timestamp = to_string(get_year(get_current_date()) , "9999") + "-" + to_string(get_month(get_current_date()) , "99") + "-" + to_string(get_day(get_current_date()) , "99") + "T" + to_string(get_current_time_in_seconds(), "HH:MM:SS") + "Z"
                output_list.billnumber = bill.rechnr
                output_list.terminalid = terminalid
                output_list.programid = programid
                output_list.walletid = walletid
                output_list.zinr = res_line.zinr
                output_list.resnr = res_line.resnr
                output_list.reslinnr = res_line.reslinnr
                output_list.gastnrmember = res_line.gastnrmember
                output_list.segment = segment.bezeich
                output_list.sob = sourccod.bezeich
                output_list.send_date = get_current_date()
                output_list.data_date = res_line.abreise
                output_list.price = ( to_decimal(bill_line.betrag) / to_decimal(1.21) )
                output_list.price_str = trim(to_string(bill_line.betrag / 1.21, "->>>>>>>>9")) + ";"
                output_list.amount = ( to_decimal(bill_line.betrag) / to_decimal(1.21) )
                output_list.sku = bill_line.zinr + ";"
                output_list.itemname = zimmer.bezeich + ";"
                output_list.qty = "1;"

                if guest.mobil_telefon != "":
                    output_list.phone = guest.mobil_telefon
                else:
                    output_list.phone = guest.telefon

                if output_list.phone != "":
                    prefix = substring(output_list.phone, 0, 1)
                    phnumb = substring(output_list.phone, 1, length(output_list.phone))

                    if prefix.lower()  == ("0").lower() :
                        prefix = "+62"
                        output_list.phone = prefix + phnumb
            else:
                output_list.sku = bill_line.zinr + ";" + output_list.sku
                output_list.itemname = zimmer.bezeich + ";" + output_list.itemname
                output_list.qty = "1" + ";" + output_list.qty
                output_list.price = ( to_decimal(bill_line.betrag) / to_decimal(1.21)) + to_decimal(output_list.price)
                output_list.price_str = trim(to_string(bill_line.betrag / 1.21, "->>>>>>>>9")) + ";" + output_list.price_str
                output_list.amount = ( to_decimal(bill_line.betrag) / to_decimal(1.21)) + to_decimal(output_list.amount)

    for output_list in query(output_list_data, filters=(lambda output_list: output_list.amount == 0)):
        output_list_data.remove(output_list)

    for output_list in query(output_list_data):

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == output_list.billnumber) & (Bill_line.zinr == output_list.zinr) & (Bill_line.betrag < 0)).order_by(Bill_line._recid).all():
            output_list.paymentmethod = bill_line.bezeich

        if length(output_list.itemname) > 0:
            output_list.itemname = substring(output_list.itemname, 0, length(output_list.itemname) - 1)

        if length(output_list.price_str) > 0:
            output_list.price_str = substring(output_list.price_str, 0, length(output_list.price_str) - 1)

        if length(output_list.sku) > 0:
            output_list.sku = substring(output_list.sku, 0, length(output_list.sku) - 1)

        if length(output_list.qty) > 0:
            output_list.qty = substring(output_list.qty, 0, length(output_list.qty) - 1)

    if segment_list != "":

        for output_list in query(output_list_data, filters=(lambda output_list: not matches(segment_list,r"*" + output_list.segment + r"*"))):
            output_list_data.remove(output_list)

    return generate_output()