#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Htparam, H_journal, Hoteldpt, H_artikel, H_bill, Res_line

def rest_billjourn_journal_list1_webbl(from_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, price_decimal:int, excl_paydisc:bool):

    prepare_cache ([Guest, Htparam, H_journal, Hoteldpt, H_artikel, H_bill, Res_line])

    booking_journbill_list_data = []
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    guest = htparam = h_journal = hoteldpt = h_artikel = h_bill = res_line = None

    booking_journbill_list = gbuff = None

    booking_journbill_list_data, Booking_journbill_list = create_model("Booking_journbill_list", {"datum":date, "tabelno":string, "billno":int, "artno":int, "descr":string, "qty":int, "sales":Decimal, "payment":Decimal, "depart":string, "id":string, "zeit":string, "gname":string, "rmno":string, "st_optable":string, "ct_optable":string, "art_type":int, "resname":string, "resnr":int}, {"art_type": -1})

    Gbuff = create_buffer("Gbuff",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal booking_journbill_list_data, disc_art1, disc_art2, disc_art3, guest, htparam, h_journal, hoteldpt, h_artikel, h_bill, res_line
        nonlocal from_art, from_dept, to_dept, from_date, to_date, price_decimal, excl_paydisc
        nonlocal gbuff


        nonlocal booking_journbill_list, gbuff
        nonlocal booking_journbill_list_data

        return {"booking-journbill-list": booking_journbill_list_data}

    def journal_list():

        nonlocal booking_journbill_list_data, disc_art1, disc_art2, disc_art3, guest, htparam, h_journal, hoteldpt, h_artikel, h_bill, res_line
        nonlocal from_art, from_dept, to_dept, from_date, to_date, price_decimal, excl_paydisc
        nonlocal gbuff


        nonlocal booking_journbill_list, gbuff
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
        curr_time_pay:string = ""
        count_i:int = 0
        pay_exist:bool = False
        curr_compta:string = ""
        curr_resnr:int = 0
        buf_hjournal = None
        Buf_hjournal =  create_buffer("Buf_hjournal",H_journal)
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
                curr_time_pay = ""
                count_i = 0
                for curr_date in date_range(from_date,to_date) :
                    it_exist = False

                    for h_journal in db_session.query(H_journal).filter(
                             (H_journal.bill_datum == curr_date) & (H_journal.departement == hoteldpt.num)).order_by(H_journal.rechnr, H_journal.sysdate, H_journal.zeit).all():

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)]})
                        it_exist = True
                        curr_guest = ""
                        curr_room = ""
                        curr_compta = ""
                        curr_resnr = 0

                        h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                        if h_bill:

                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                if res_line:

                                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                                    curr_guest = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                                    curr_room = res_line.zinr
                                    curr_resnr = res_line.resnr

                                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                                    if gbuff:
                                        curr_compta = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                                else:
                                    curr_guest = h_bill.bilname
                                    curr_room = ""


                            else:
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

                            if curr_resnr != 0:
                                booking_journbill_list.resname = curr_compta
                                booking_journbill_list.resnr = curr_resnr

                            if h_artikel:
                                booking_journbill_list.art_type = h_artikel.artart

                            if h_artikel and h_artikel.artart == 0:

                                if price_decimal == 2:
                                    booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                    booking_journbill_list.payment =  to_decimal("0")
                                else:
                                    booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                    booking_journbill_list.payment =  to_decimal("0")

                                if bill_no != h_journal.rechnr and dept_no == h_journal.departement and h_journal.anzahl > 0:
                                    count_i = 0
                                    curr_time = to_string(h_journal.zeit, "HH:MM:SS")
                                else:
                                    count_i = 0

                                    for buf_hjournal in db_session.query(Buf_hjournal).filter(
                                             (Buf_hjournal.rechnr == h_journal.rechnr) & (Buf_hjournal.departement == h_journal.departement) & (Buf_hjournal.bill_datum == h_journal.bill_datum) & (Buf_hjournal.anzahl > 0) & (Buf_hjournal.betrag < 0)).order_by(Buf_hjournal.zeit.desc()).yield_per(100):
                                        pay_exist = True
                                        break

                                    if not pay_exist:
                                        booking_journbill_list.ct_optable = to_string(h_journal.zeit, "HH:MM:SS")

                                if (h_journal.anzahl > 0) or (h_journal.anzahl < 0 and pay_exist):
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
                                sub_tot1 =  to_decimal(sub_tot1) + to_decimal(h_journal.betrag)
                                tot1 =  to_decimal(tot1) + to_decimal(h_journal.betrag)
                                count_i = count_i + 1

                                if count_i == 1:

                                    for buf_hjournal in db_session.query(Buf_hjournal).filter(
                                             (Buf_hjournal.rechnr == h_journal.rechnr) & (Buf_hjournal.departement == h_journal.departement) & (Buf_hjournal.bill_datum == h_journal.bill_datum) & (Buf_hjournal.anzahl > 0) & (Buf_hjournal.betrag < 0)).order_by(Buf_hjournal.zeit.desc()).yield_per(100):
                                        curr_time_pay = to_string(buf_hjournal.zeit, "HH:MM:SS")
                                        break
                                booking_journbill_list.ct_optable = curr_time_pay
                            booking_journbill_list.id = to_string(h_journal.kellner_nr)
                            booking_journbill_list.zeit = to_string(h_journal.zeit, "HH:MM:SS")
                            booking_journbill_list.rmno = curr_room

                            if excl_paydisc:

                                if (h_artikel and h_artikel.artart != 0) or (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) or (matches(h_journal.bezeich,r"*DISC*")) or (h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 4) == ("RmNo").lower()) or (h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 8) == ("Transfer").lower()):
                                    booking_journbill_list.qty = 0
                                qty = qty + booking_journbill_list.qty
                            else:
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