#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, H_journal, H_artikel, Hoteldpt, H_bill, Res_line, Guest

def rest_billjourn_journal_list_webbl(from_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, price_decimal:int):

    prepare_cache ([Htparam, H_journal, H_artikel, Hoteldpt, H_bill, Res_line, Guest])

    booking_journbill_list_data = []
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    htparam = h_journal = h_artikel = hoteldpt = h_bill = res_line = guest = None

    booking_journbill_list = None

    booking_journbill_list_data, Booking_journbill_list = create_model("Booking_journbill_list", {"datum":date, "tabelno":string, "billno":int, "artno":int, "descr":string, "qty":int, "sales":Decimal, "payment":Decimal, "depart":string, "id":string, "zeit":string, "gname":string, "rmno":string, "st_optable":string, "ct_optable":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal booking_journbill_list_data, disc_art1, disc_art2, disc_art3, htparam, h_journal, h_artikel, hoteldpt, h_bill, res_line, guest
        nonlocal from_art, from_dept, to_dept, from_date, to_date, price_decimal


        nonlocal booking_journbill_list
        nonlocal booking_journbill_list_data

        return {"booking-journbill-list": booking_journbill_list_data}

    def journal_list():

        nonlocal booking_journbill_list_data, disc_art1, disc_art2, disc_art3, htparam, h_journal, h_artikel, hoteldpt, h_bill, res_line, guest
        nonlocal from_art, from_dept, to_dept, from_date, to_date, price_decimal


        nonlocal booking_journbill_list
        nonlocal booking_journbill_list_data

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        sub_tot1:Decimal = to_decimal("0.0")
        tot1:Decimal = to_decimal("0.0")
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        curr_guest:string = ""
        curr_room:string = ""
        bill_no:int = 0
        dept_no:int = 0
        curr_time:string = ""
        art_pay:int = 0
        buf_hjournal = None
        buf_hart = None
        Buf_hjournal =  create_buffer("Buf_hjournal",H_journal)
        Buf_hart =  create_buffer("Buf_hart",H_artikel)
        booking_journbill_list_data.clear()

        if from_art == 0:

            for hoteldpt in db_session.query(Hoteldpt).filter(
                     (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
                sub_tot =  to_decimal("0")
                sub_tot1 =  to_decimal("0")
                it_exist = False
                qty = 0
                bill_no = 0
                dept_no = hoteldpt.num
                curr_time = ""
                art_pay = 0
                for curr_date in date_range(from_date,to_date) :

                    for h_journal in db_session.query(H_journal).filter(
                             (H_journal.bill_datum == curr_date) & (H_journal.departement == hoteldpt.num)).order_by(H_journal.rechnr, H_journal.sysdate, H_journal.zeit).all():

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)]})
                        it_exist = True
                        curr_guest = ""
                        curr_room = ""

                        h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                        if h_bill:

                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                if res_line:
                                    curr_guest = res_line.name
                                    curr_room = res_line.zinr

                            elif h_bill.resnr > 0:

                                guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                if guest:
                                    curr_guest = guest.name + "," + guest.vorname1
                                    curr_room = ""

                            elif h_bill.resnr == 0:
                                curr_guest = h_bill.bilname
                                curr_room = ""

                        if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) and h_journal.betrag == 0:
                            pass
                        else:
                            booking_journbill_list = Booking_journbill_list()
                            booking_journbill_list_data.append(booking_journbill_list)

                            booking_journbill_list.gname = curr_guest
                            booking_journbill_list.datum = h_journal.bill_datum
                            booking_journbill_list.tabelno = to_string(h_journal.tischnr, ">>>9")
                            booking_journbill_list.billno = h_journal.rechnr
                            booking_journbill_list.artno = h_journal.artnr
                            booking_journbill_list.descr = h_journal.bezeich
                            booking_journbill_list.depart = hoteldpt.depart
                            booking_journbill_list.qty = h_journal.anzahl

                            if h_artikel and h_artikel.artart == 0:

                                if price_decimal == 2:
                                    booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                    booking_journbill_list.payment =  to_decimal("0")
                                else:
                                    booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                    booking_journbill_list.payment =  to_decimal("0")

                                if bill_no != h_journal.rechnr and dept_no == h_journal.departement:
                                    curr_time = to_string(h_journal.zeit, "HH:MM:SS")
                                booking_journbill_list.st_optable = curr_time
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

                            elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 9) == ("To Table ").lower() :

                                if price_decimal == 2:
                                    booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                    booking_journbill_list.payment =  to_decimal("0")
                                else:
                                    booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                    booking_journbill_list.payment =  to_decimal("0")
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

                            elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 11) == ("From Table ").lower() :

                                if price_decimal == 2:
                                    booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                    booking_journbill_list.payment =  to_decimal("0")
                                else:
                                    booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                    booking_journbill_list.payment =  to_decimal("0")
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
                            else:

                                if price_decimal == 2:
                                    booking_journbill_list.sales =  to_decimal("0")
                                    booking_journbill_list.payment =  to_decimal(h_journal.betrag)
                                else:
                                    booking_journbill_list.sales =  to_decimal("0")
                                    booking_journbill_list.payment =  to_decimal(h_journal.betrag)

                                buf_hjournal = get_cache (H_journal, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)],"anzahl": [(gt, 0)],"betrag": [(lt, 0)]})

                                if buf_hjournal:

                                    buf_hart = get_cache (H_artikel, {"artnr": [(eq, buf_hjournal.artnr)],"departement": [(eq, buf_hjournal.departement)],"artart": [(ne, 0)]})

                                    if buf_hart:
                                        booking_journbill_list.ct_optable = to_string(buf_hjournal.zeit, "HH:MM:SS")
                                sub_tot1 =  to_decimal(sub_tot1) + to_decimal(h_journal.betrag)
                                tot1 =  to_decimal(tot1) + to_decimal(h_journal.betrag)
                            booking_journbill_list.id = to_string(h_journal.kellner_nr, "999")
                            booking_journbill_list.zeit = to_string(h_journal.zeit, "HH:MM:SS")
                            booking_journbill_list.rmno = curr_room
                            qty = qty + h_journal.anzahl
                            bill_no = h_journal.rechnr

                    if it_exist:
                        booking_journbill_list = Booking_journbill_list()
                        booking_journbill_list_data.append(booking_journbill_list)


                        if price_decimal == 2:
                            booking_journbill_list.descr = "T O T A L"
                            booking_journbill_list.qty = qty
                            booking_journbill_list.sales =  to_decimal(sub_tot)
                            booking_journbill_list.payment =  to_decimal(sub_tot1)


                        else:
                            booking_journbill_list.descr = "T O T A L"
                            booking_journbill_list.qty = qty
                            booking_journbill_list.sales =  to_decimal(sub_tot)
                            booking_journbill_list.payment =  to_decimal(sub_tot1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
    disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
    disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
    disc_art3 = htparam.finteger
    journal_list()

    return generate_output()