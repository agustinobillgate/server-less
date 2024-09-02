from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Hoteldpt, H_journal, H_artikel, H_bill, Res_line, Guest

def rest_billjourn_journal_list_webbl(from_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, price_decimal:int):
    booking_journbill_list_list = []
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    htparam = hoteldpt = h_journal = h_artikel = h_bill = res_line = guest = None

    booking_journbill_list = None

    booking_journbill_list_list, Booking_journbill_list = create_model("Booking_journbill_list", {"datum":date, "tabelno":str, "billno":int, "artno":int, "descr":str, "qty":int, "sales":decimal, "payment":decimal, "depart":str, "id":str, "zeit":str, "gname":str, "rmno":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal booking_journbill_list_list, disc_art1, disc_art2, disc_art3, htparam, hoteldpt, h_journal, h_artikel, h_bill, res_line, guest


        nonlocal booking_journbill_list
        nonlocal booking_journbill_list_list
        return {"booking-journbill-list": booking_journbill_list_list}

    def journal_list():

        nonlocal booking_journbill_list_list, disc_art1, disc_art2, disc_art3, htparam, hoteldpt, h_journal, h_artikel, h_bill, res_line, guest


        nonlocal booking_journbill_list
        nonlocal booking_journbill_list_list

        qty:int = 0
        sub_tot:decimal = 0
        tot:decimal = 0
        sub_tot1:decimal = 0
        tot1:decimal = 0
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        curr_guest:str = ""
        curr_room:str = ""
        booking_journbill_list_list.clear()

        if from_art == 0:

            for hoteldpt in db_session.query(Hoteldpt).filter(
                    (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():
                sub_tot = 0
                sub_tot1 = 0
                it_exist = False
                qty = 0
                for curr_date in range(from_date,to_date + 1) :

                    for h_journal in db_session.query(H_journal).filter(
                            (H_journal.bill_datum == curr_date) &  (H_journal.departement == hoteldpt.num)).all():

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.artnr == h_journal.artnr) &  (H_artikel.departement == h_journal.departement)).first()
                        it_exist = True
                        curr_guest = ""
                        curr_room = ""

                        h_bill = db_session.query(H_bill).filter(
                                (H_bill.rechnr == h_journal.rechnr) &  (H_bill.departement == h_journal.departement)).first()

                        if h_bill:

                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                res_line = db_session.query(Res_line).filter(
                                        (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

                                if res_line:
                                    curr_guest = res_line.name
                                    curr_room = res_line.zinr

                            elif h_bill.resnr > 0:

                                guest = db_session.query(Guest).filter(
                                        (Guest.gastnr == h_bill.resnr)).first()

                                if guest:
                                    curr_guest = guest.name + "," + guest.vorname1
                                    curr_room = ""

                            elif h_bill.resnr == 0:
                                curr_guest = h_bill.bilname
                                curr_room = ""

                        if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) and h_journal.betrag == 0:
                            1
                        else:
                            booking_journbill_list = Booking_journbill_list()
                            booking_journbill_list_list.append(booking_journbill_list)

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
                                    booking_journbill_list.sales = h_journal.betrag
                                    booking_journbill_list.payment = 0
                                else:
                                    booking_journbill_list.sales = h_journal.betrag
                                    booking_journbill_list.payment = 0
                                sub_tot = sub_tot + h_journal.betrag
                                tot = tot + h_journal.betrag

                            elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 9) == "To Table ":

                                if price_decimal == 2:
                                    booking_journbill_list.sales = h_journal.betrag
                                    booking_journbill_list.payment = 0
                                else:
                                    booking_journbill_list.sales = h_journal.betrag
                                    booking_journbill_list.payment = 0
                                sub_tot = sub_tot + h_journal.betrag
                                tot = tot + h_journal.betrag

                            elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 11) == "From Table ":

                                if price_decimal == 2:
                                    booking_journbill_list.sales = h_journal.betrag
                                    booking_journbill_list.payment = 0
                                else:
                                    booking_journbill_list.sales = h_journal.betrag
                                    booking_journbill_list.payment = 0
                                sub_tot = sub_tot + h_journal.betrag
                                tot = tot + h_journal.betrag
                            else:

                                if price_decimal == 2:
                                    booking_journbill_list.sales = 0
                                    booking_journbill_list.payment = h_journal.betrag
                                else:
                                    booking_journbill_list.sales = 0
                                    booking_journbill_list.payment = h_journal.betrag
                                sub_tot1 = sub_tot1 + h_journal.betrag
                                tot1 = tot1 + h_journal.betrag
                            booking_journbill_list.id = to_string(h_journal.kellner_nr, "999")
                            booking_journbill_list.zeit = to_string(h_journal.zeit, "HH:MM:SS")
                            booking_journbill_list.rmno = curr_room
                            qty = qty + h_journal.anzahl

                    if it_exist:
                        booking_journbill_list = Booking_journbill_list()
                        booking_journbill_list_list.append(booking_journbill_list)


                        if price_decimal == 2:
                            booking_journbill_list.descr = "T O T A L"
                            booking_journbill_list.qty = qty
                            booking_journbill_list.sales = sub_tot
                            booking_journbill_list.payment = sub_tot1


                        else:
                            booking_journbill_list.descr = "T O T A L"
                            booking_journbill_list.qty = qty
                            booking_journbill_list.sales = sub_tot
                            booking_journbill_list.payment = sub_tot1


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()
    disc_art1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 596)).first()
    disc_art2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 556)).first()
    disc_art3 = htparam.finteger
    journal_list()

    return generate_output()