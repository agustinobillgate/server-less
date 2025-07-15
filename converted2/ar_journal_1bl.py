#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Artikel, Billjournal, Bill, Hoteldpt

def ar_journal_1bl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date):

    prepare_cache ([Artikel, Billjournal, Bill, Hoteldpt])

    output_list_data = []
    long_digit:bool = False
    qty:int = 0
    sub_tot:Decimal = to_decimal("0.0")
    tot:Decimal = to_decimal("0.0")
    curr_date:date = None
    last_dept:int = -1
    it_exist:bool = False
    descr1:string = ""
    voucher_no:string = ""
    ind:int = 0
    gdelimiter:string = ""
    cnt:int = 0
    i:int = 0
    artikel = billjournal = bill = hoteldpt = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"datum":date, "room_no":string, "bill_no":int, "art_no":int, "description":string, "voucher_no":string, "departement":string, "qty":int, "amount":Decimal, "zeit":string, "id":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, long_digit, qty, sub_tot, tot, curr_date, last_dept, it_exist, descr1, voucher_no, ind, gdelimiter, cnt, i, artikel, billjournal, bill, hoteldpt
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}


    output_list_data.clear()

    for artikel in db_session.query(Artikel).filter(
             (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.departement >= from_dept) & (Artikel.departement <= to_dept)).order_by((Artikel.departement * 10000 + Artikel.artnr)).all():
        sub_tot =  to_decimal("0")
        it_exist = False
        qty = 0
        for curr_date in date_range(from_date,to_date) :

            for billjournal in db_session.query(Billjournal).filter(
                     (Billjournal.artnr == artikel.artnr) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == curr_date) & (Billjournal.anzahl != 0)).order_by(Billjournal.sysdate, Billjournal.zeit, Billjournal.zinr).all():
                it_exist = True

                bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                if bill:

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, bill.billtyp)]})
                output_list = Output_list()
                output_list_data.append(output_list)


                if hoteldpt:
                    output_list.datum = billjournal.bill_datum
                    output_list.room_no = billjournal.zinr
                    output_list.bill_no = billjournal.rechnr
                    output_list.art_no = billjournal.artnr
                    output_list.description = billjournal.bezeich
                    output_list.departement = hoteldpt.depart
                    output_list.qty = billjournal.anzahl
                    output_list.amount =  to_decimal(billjournal.betrag)
                    output_list.zeit = to_string(billjournal.zeit, "HH:MM:SS")
                    output_list.id = billjournal.userinit


                else:
                    output_list.datum = billjournal.bill_datum
                    output_list.room_no = billjournal.zinr
                    output_list.bill_no = billjournal.rechnr
                    output_list.art_no = billjournal.artnr
                    output_list.description = billjournal.bezeich
                    output_list.qty = billjournal.anzahl
                    output_list.amount =  to_decimal(billjournal.betrag)
                    output_list.zeit = to_string(billjournal.zeit, "HH:MM:SS")
                    output_list.id = billjournal.userinit


                descr1 = ""
                voucher_no = ""

                if substring(billjournal.bezeich, 0, 1) == ("*").lower()  or billjournal.kassarapport:
                    descr1 = billjournal.bezeich
                    voucher_no = ""

                elif substring(billjournal.bezeich, 0, 19) == ("Release A/R Payment").lower() :
                    output_list.description = substring(billjournal.bezeich, 0, 19)
                    voucher_no = ""


                else:

                    if not artikel.bezaendern:
                        ind = get_index(billjournal.bezeich, "/")

                        if ind != 0:
                            gdelimiter = "/"
                        else:
                            ind = get_index(billjournal.bezeich, "]")

                            if ind != 0:
                                gdelimiter = "]"

                        if ind != 0:

                            if ind > length(artikel.bezeich):
                                descr1 = entry(0, billjournal.bezeich, gdelimiter)
                                voucher_no = substring(billjournal.bezeich, (ind + 1) - 1)


                            else:
                                cnt = num_entries(artikel.bezeich, gdelimiter)
                                for i in range(1,cnt + 1) :

                                    if descr1 == "":
                                        descr1 = entry(i - 1, billjournal.bezeich, gdelimiter)
                                    else:
                                        descr1 = descr1 + "/" + entry(i - 1, billjournal.bezeich, gdelimiter)
                                voucher_no = substring(billjournal.bezeich, length(descr1) + 2 - 1)

                            if gdelimiter.lower()  == ("]").lower() :
                                descr1 = descr1 + gdelimiter
                        else:
                            descr1 = billjournal.bezeich
                    else:
                        ind = num_entries(billjournal.bezeich, "/")

                        if ind <= 1:
                            descr1 = billjournal.bezeich
                            voucher_no = ""


                        else:
                            descr1 = entry(0, billjournal.bezeich, "/")
                            voucher_no = entry(1, billjournal.bezeich, "/")

                        if descr1 == "" or descr1 == " ":
                            descr1 = artikel.bezeich
                output_list.voucher_no = voucher_no
                qty = qty + billjournal.anzahl

                if billjournal.anzahl != 0:
                    sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)
                    tot =  to_decimal(tot) + to_decimal(billjournal.betrag)

        if it_exist:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.departement = "T O T A L"
            output_list.qty = qty
            output_list.amount =  to_decimal(sub_tot)


    output_list = Output_list()
    output_list_data.append(output_list)

    output_list.departement = "Grand TOTAL"
    output_list.amount =  to_decimal(tot)

    return generate_output()