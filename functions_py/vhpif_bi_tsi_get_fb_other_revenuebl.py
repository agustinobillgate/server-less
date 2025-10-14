#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 14-10-2025 
# Tiket ID : F50EA1 | New Compile program if 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Hoteldpt, H_artikel, Artikel, Gl_acct, Htparam, H_journal, H_bill, Res_line, Guest

def vhpif_bi_tsi_get_fb_other_revenuebl(datum:date):

    prepare_cache ([Hoteldpt, H_artikel, Artikel, Gl_acct, Htparam, H_journal, H_bill, Res_line, Guest])

    revenue_list_data = []
    from_dept:int = 0
    to_dept:int = 0
    coa_name:string = ""
    coa_number:string = ""
    service_rate:Decimal = to_decimal("0.0")
    vat_rate:Decimal = to_decimal("0.0")
    net_sales:Decimal = to_decimal("0.0")
    hoteldpt = h_artikel = artikel = gl_acct = htparam = h_journal = h_bill = res_line = guest = None

    revenue_list = booking_journbill_list = None

    revenue_list_data, Revenue_list = create_model("Revenue_list", {"datum":date, "time_str":string, "dept_number":int, "dept_name":string, "bill_number":int, "artikel_number":int, "artikel_desc":string, "coa_number":string, "coa_name":string, "qty":Decimal, "price_amount":Decimal, "sales_amount":Decimal})
    booking_journbill_list_data, Booking_journbill_list = create_model("Booking_journbill_list", {"datum":date, "tabelno":string, "billno":int, "artno":int, "descr":string, "qty":int, "sales":Decimal, "payment":Decimal, "depart":string, "id":string, "zeit":string, "gname":string, "rmno":string, "st_optable":string, "ct_optable":string, "art_type":int, "phone":string, "deptnr":int, "net_sales":Decimal}, {"art_type": -1})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal revenue_list_data, from_dept, to_dept, coa_name, coa_number, service_rate, vat_rate, net_sales, hoteldpt, h_artikel, artikel, gl_acct, htparam, h_journal, h_bill, res_line, guest
        nonlocal datum


        nonlocal revenue_list, booking_journbill_list
        nonlocal revenue_list_data, booking_journbill_list_data

        return {"revenue-list": revenue_list_data}

    def get_journal_bybill(from_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, price_decimal:int, excl_paydisc:bool):

        nonlocal revenue_list_data, coa_name, coa_number, service_rate, vat_rate, net_sales, hoteldpt, h_artikel, artikel, gl_acct, htparam, h_journal, h_bill, res_line, guest
        nonlocal datum


        nonlocal revenue_list, booking_journbill_list
        nonlocal revenue_list_data, booking_journbill_list_data

        disc_art1:int = 0
        disc_art2:int = 0
        disc_art3:int = 0
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
        curr_phone:string = ""
        buf_hjournal = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
        disc_art1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
        disc_art2 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
        disc_art3 = htparam.finteger
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
                curr_phone = ""
                for curr_date in date_range(from_date,to_date) :
                    it_exist = False

                    for h_journal in db_session.query(H_journal).filter(
                             (H_journal.bill_datum == curr_date) & (H_journal.departement == hoteldpt.num)).order_by(H_journal.rechnr, H_journal.sysdate, H_journal.zeit).all():

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)]})

                        artikel = get_cache (Artikel, {"departement": [(eq, h_artikel.departemen)],"artnr": [(eq, h_artikel.artnrfront)]})
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
                                    curr_phone = guest.mobil_telefon

                            elif h_bill.resnr == 0:
                                curr_guest = h_bill.bilname
                                curr_room = ""
                                curr_phone = ""

                        if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) and h_journal.betrag == 0:
                            pass
                        else:
                            booking_journbill_list = Booking_journbill_list()
                            booking_journbill_list_data.append(booking_journbill_list)

                            booking_journbill_list.gname = curr_guest
                            booking_journbill_list.phone = curr_phone
                            booking_journbill_list.datum = h_journal.bill_datum
                            booking_journbill_list.tabelno = to_string(h_journal.tischnr, ">>>9")
                            booking_journbill_list.billno = h_journal.rechnr
                            booking_journbill_list.artno = h_journal.artnr
                            booking_journbill_list.descr = h_journal.bezeich
                            booking_journbill_list.depart = hoteldpt.depart
                            booking_journbill_list.deptnr = hoteldpt.num
                            booking_journbill_list.qty = h_journal.anzahl

                            if h_artikel:
                                booking_journbill_list.art_type = h_artikel.artart

                            if h_artikel and h_artikel.artart == 0:
                                booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                booking_journbill_list.payment =  to_decimal("0")

                                if bill_no != h_journal.rechnr and dept_no == h_journal.departement and h_journal.anzahl > 0:
                                    count_i = 0
                                    curr_time = to_string(h_journal.zeit, "HH:MM:SS")
                                else:
                                    count_i = 0

                                    for buf_hjournal in db_session.query(Buf_hjournal).filter(
                                             (Buf_hjournal.rechnr == h_journal.rechnr) & (Buf_hjournal.departement == h_journal.departement) & (Buf_hjournal.bill_datum == h_journal.bill_datum) & (Buf_hjournal.anzahl > 0) & (Buf_hjournal.betrag < 0)).order_by(Buf_hjournal.zeit.desc()).all():
                                        pay_exist = True
                                        break

                                    if not pay_exist:
                                        booking_journbill_list.ct_optable = to_string(h_journal.zeit, "HH:MM:SS")

                                if (h_journal.anzahl > 0) or (h_journal.anzahl < 0 and pay_exist):
                                    booking_journbill_list.st_optable = curr_time
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

                            elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 9) == ("To Table ").lower() :
                                booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                booking_journbill_list.payment =  to_decimal("0")
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

                            elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 11) == ("From Table ").lower() :
                                booking_journbill_list.sales =  to_decimal(h_journal.betrag)
                                booking_journbill_list.payment =  to_decimal("0")
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
                            else:
                                booking_journbill_list.sales =  to_decimal("0")
                                booking_journbill_list.payment =  to_decimal(h_journal.betrag)
                                sub_tot1 =  to_decimal(sub_tot1) + to_decimal(h_journal.betrag)
                                tot1 =  to_decimal(tot1) + to_decimal(h_journal.betrag)
                                count_i = count_i + 1

                                if count_i == 1:

                                    for buf_hjournal in db_session.query(Buf_hjournal).filter(
                                             (Buf_hjournal.rechnr == h_journal.rechnr) & (Buf_hjournal.departement == h_journal.departement) & (Buf_hjournal.bill_datum == h_journal.bill_datum) & (Buf_hjournal.anzahl > 0) & (Buf_hjournal.betrag < 0)).order_by(Buf_hjournal.zeit.desc()).all():
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

                            if artikel:
                                service_rate =  to_decimal("0")
                                vat_rate =  to_decimal("0")
                                booking_journbill_list.net_sales =  to_decimal("0")


                                service_rate, vat_rate = get_output(calc_servvat(artikel.departemen, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))
                                booking_journbill_list.net_sales =  to_decimal(booking_journbill_list.sales) / to_decimal((1) + to_decimal(service_rate) + to_decimal(vat_rate))


    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num >= 0)).order_by(Hoteldpt.num).all():
        from_dept = hoteldpt.num
        break

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num >= 0)).order_by(Hoteldpt.num.desc()).all():
        to_dept = hoteldpt.num
        break
    get_journal_bybill(0, from_dept, to_dept, datum, datum, 0, False)

    for booking_journbill_list in query(booking_journbill_list_data, filters=(lambda booking_journbill_list: booking_journbill_list.billno != 0 and booking_journbill_list.sales != 0)):

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, booking_journbill_list.artno)],"departement": [(eq, booking_journbill_list.deptnr)]})

        if h_artikel:

            artikel = get_cache (Artikel, {"departement": [(eq, h_artikel.departemen)],"artnr": [(eq, h_artikel.artnrfront)]})

            if artikel:

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

                if gl_acct:
                    coa_name = gl_acct.bezeich
                    coa_number = gl_acct.fibukonto
                else:
                    coa_name = ""
                    coa_number = ""
            revenue_list = Revenue_list()
            revenue_list_data.append(revenue_list)

            revenue_list.datum = booking_journbill_list.datum
            revenue_list.time_str = booking_journbill_list.zeit
            revenue_list.dept_number = booking_journbill_list.deptnr
            revenue_list.dept_name = booking_journbill_list.depart
            revenue_list.bill_number = booking_journbill_list.billno
            revenue_list.artikel_number = booking_journbill_list.artno
            revenue_list.artikel_desc = booking_journbill_list.descr
            revenue_list.coa_number = coa_number
            revenue_list.coa_name = coa_name
            revenue_list.qty =  to_decimal(booking_journbill_list.qty)
            revenue_list.sales_amount = to_decimal(round(booking_journbill_list.net_sales , 2))
            revenue_list.price_amount =  to_decimal(h_artikel.epreis1)

    return generate_output()