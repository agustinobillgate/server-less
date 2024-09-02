from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Queasy, Htparam, Bediener, Hoteldpt, Tisch, H_artikel, H_bill, H_bill_line, Artikel

def selforder_viewordered_itembl(user_init:str, dept:int, table_no:int, session_parameter:str):
    mess_result = ""
    user_name = ""
    dept_name = ""
    guest_name = ""
    pax = 0
    room = ""
    total_tax = 0
    total_service = 0
    total_price = 0
    total_payment = 0
    grand_total = 0
    sessionexpired = False
    hold_payment = False
    bill_number = 0
    payment_method = ""
    ordered_item_list = []
    mess_str:str = ""
    i_str:int = 0
    mess_token:str = ""
    mess_keyword:str = ""
    mess_value:str = ""
    orderdatetime:str = ""
    gname:str = ""
    order_i:int = 0
    serv_perc:decimal = 0
    mwst_perc:decimal = 0
    fact:decimal = 1
    mmwst1:decimal = 0
    mwst:decimal = 0
    h_service:decimal = 0
    h_mwst:decimal = 0
    incl_service:bool = False
    incl_mwst:bool = False
    gst_logic:bool = False
    serv_disc:bool = True
    vat_disc:bool = True
    f_discart:int = -1
    amount:decimal = 0
    price_decimal:int = 0
    tax:decimal = 0
    serv:decimal = 0
    service:decimal = 0
    vat:decimal = 0
    vat2:decimal = 0
    fact_scvat:decimal = 1
    serv_vat:bool = False
    tax_vat:bool = False
    ct:str = ""
    l_deci:int = 2
    tot_amount:decimal = 0
    bill_date110:date = None
    bill_date:date = None
    service_taxable:bool = False
    sesion_id:str = ""
    servtax_use_foart:bool = False
    dynamic_qr:bool = False
    room_serviceflag:bool = False
    rm_no:str = ""
    str1:str = ""
    count_i:int = 0
    alpha_flag:bool = False
    found_bill:int = 0
    billno:int = 0
    do_it:bool = False
    queasy = htparam = bediener = hoteldpt = tisch = h_artikel = h_bill = h_bill_line = artikel = None

    ordered_item = bqsy = bposted = qrqsy = queasyorderbill = orderbill = orderbill_line = orderbill_posted = bufforder = sosqsy = q_takentable = searchbill = mergebill = hbuff = abuff = None

    ordered_item_list, Ordered_item = create_model("Ordered_item", {"table_nr":int, "order_nr":int, "nr":int, "bezeich":str, "qty":int, "sp_req":str, "confirm":bool, "remarks":str, "order_date":str, "price":decimal, "subtotal":decimal, "subtotalprice":decimal, "artnr":int, "service":decimal, "tax":decimal, "bill_date":date, "order_status":str, "count_amount":bool, "posted":bool, "article_type":str, "pricetaxserv":decimal, "webpost_flag":bool, "hbline_recid":int, "hbline_time":int, "item_str":str, "bline_str":str, "amount":decimal, "cancel_str":str})

    Bqsy = Queasy
    Bposted = Queasy
    Qrqsy = Queasy
    Queasyorderbill = Queasy
    Orderbill = Queasy
    Orderbill_line = Queasy
    Orderbill_posted = Queasy
    Bufforder = Ordered_item
    bufforder_list = ordered_item_list

    Sosqsy = Queasy
    Q_takentable = Queasy
    Searchbill = Queasy
    Mergebill = Queasy
    Hbuff = H_artikel
    Abuff = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, user_name, dept_name, guest_name, pax, room, total_tax, total_service, total_price, total_payment, grand_total, sessionexpired, hold_payment, bill_number, payment_method, ordered_item_list, mess_str, i_str, mess_token, mess_keyword, mess_value, orderdatetime, gname, order_i, serv_perc, mwst_perc, fact, mmwst1, mwst, h_service, h_mwst, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, price_decimal, tax, serv, service, vat, vat2, fact_scvat, serv_vat, tax_vat, ct, l_deci, tot_amount, bill_date110, bill_date, service_taxable, sesion_id, servtax_use_foart, dynamic_qr, room_serviceflag, rm_no, str1, count_i, alpha_flag, found_bill, billno, do_it, queasy, htparam, bediener, hoteldpt, tisch, h_artikel, h_bill, h_bill_line, artikel
        nonlocal bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable, searchbill, mergebill, hbuff, abuff


        nonlocal ordered_item, bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable, searchbill, mergebill, hbuff, abuff
        nonlocal ordered_item_list
        return {"mess_result": mess_result, "user_name": user_name, "dept_name": dept_name, "guest_name": guest_name, "pax": pax, "room": room, "total_tax": total_tax, "total_service": total_service, "total_price": total_price, "total_payment": total_payment, "grand_total": grand_total, "sessionexpired": sessionexpired, "hold_payment": hold_payment, "bill_number": bill_number, "payment_method": payment_method, "ordered-item": ordered_item_list}

    def query_order():

        nonlocal mess_result, user_name, dept_name, guest_name, pax, room, total_tax, total_service, total_price, total_payment, grand_total, sessionexpired, hold_payment, bill_number, payment_method, ordered_item_list, mess_str, i_str, mess_token, mess_keyword, mess_value, orderdatetime, gname, order_i, serv_perc, mwst_perc, fact, mmwst1, mwst, h_service, h_mwst, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, price_decimal, tax, serv, service, vat, vat2, fact_scvat, serv_vat, tax_vat, ct, l_deci, tot_amount, bill_date110, bill_date, service_taxable, sesion_id, servtax_use_foart, dynamic_qr, room_serviceflag, rm_no, str1, count_i, alpha_flag, found_bill, billno, do_it, queasy, htparam, bediener, hoteldpt, tisch, h_artikel, h_bill, h_bill_line, artikel
        nonlocal bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable, searchbill, mergebill, hbuff, abuff


        nonlocal ordered_item, bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable, searchbill, mergebill, hbuff, abuff
        nonlocal ordered_item_list

        posted_flag:bool = False
        itemposted_flag:bool = False
        bill_nr:int = 0
        art_type:str = ""
        art_discfood:int = 0
        art_discbev:int = 0
        art_discother:int = 0
        art_voucher:int = 0
        art_paycash:int = 0
        art_cc:str = ""
        loop_cc:int = 0
        art_cl:str = ""
        loop_cl:int = 0
        art_paycc:int = 0
        art_paycl:int = 0
        art_reczeit:str = ""
        do_it:bool = False
        Searchbill = Queasy
        Mergebill = Queasy

        searchbill = db_session.query(Searchbill).filter(
                (Searchbill.key == 225) &  (Searchbill.number1 == dept) &  (func.lower(Searchbill.char1) == "orderbill") &  (func.lower(Searchbill.char3) == (session_parameter).lower()) &  (Searchbill.number3 != 0)).first()

        if searchbill:
            mess_str = searchbill.char2
            for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                mess_token = entry(i_str - 1, mess_str, "|")
                mess_keyword = entry(0, mess_token, " == ")
                mess_value = entry(1, mess_token, " == ")

                if mess_keyword.lower()  == "RN":
                    room = mess_value

                elif mess_keyword.lower()  == "PX":
                    pax = to_int(mess_value)

                elif mess_keyword.lower()  == "NM":
                    gname = mess_value

                elif mess_keyword.lower()  == "DT":
                    orderdatetime = mess_value

                elif mess_keyword.lower()  == "BL":
                    bill_number = to_int(mess_value)

            for orderbill in db_session.query(Orderbill).filter(
                    (Orderbill.key == 225) &  (Orderbill.number1 == dept) &  (func.lower(Orderbill.char1) == "orderbill") &  (func.lower(Orderbill.char3) == (session_parameter).lower()) &  (Orderbill.logi1)).all():
                mess_str = orderbill.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, " == ")
                    mess_value = entry(1, mess_token, " == ")

                    if mess_keyword.lower()  == "BL":
                        bill_nr = to_int(mess_value)

                if bill_nr != 0:
                    bill_number = bill_nr
                    posted_flag = True
                    break

            for orderbill in db_session.query(Orderbill).filter(
                    (Orderbill.key == 225) &  (Orderbill.number1 == dept) &  (func.lower(Orderbill.char1) == "orderbill") &  (func.lower(Orderbill.char3) == (session_parameter).lower()) &  (Orderbill.logi1)).all():

                for orderbill_line in db_session.query(Orderbill_line).filter(
                        (Orderbill_line.key == 225) &  (func.lower(Orderbill_line.char1) == "orderbill_line") &  (Orderbill_line.number2 == orderbill.number2) &  (Orderbill_line.number1 == orderbill.number3)).all():
                    total_payment = orderbill.deci1
                    guest_name = gname.upper()
                    itemposted_flag = orderbill.logi3

                    if num_entries(orderbill_line.char2, "|") >= 4:
                        sesion_id = entry(3, orderbill_line.char2, "|")

                    if sesion_id.lower()  == (session_parameter).lower() :
                        mess_str = orderbill_line.char3

                        ordered_item = query(ordered_item_list, filters=(lambda ordered_item :ordered_item.item_str == orderbill_line.char3 and ordered_item.bline_str == orderbill_line.char2), first=True)

                        if not ordered_item:
                            ordered_item = Ordered_item()
                            ordered_item_list.append(ordered_item)

                            ordered_item.table_nr = orderbill.number2
                            ordered_item.order_nr = orderbill_line.number1
                            ordered_item.bezeich = entry(2, mess_str, "|")
                            ordered_item.qty = to_int(entry(3, mess_str, "|"))
                            ordered_item.sp_req = entry(5, mess_str, "|")
                            ordered_item.confirm = orderbill_line.logi2
                            ordered_item.remarks = ""
                            ordered_item.order_date = entry(2, orderbill_line.char2, "|")
                            ordered_item.nr = orderbill_line.number3
                            ordered_item.price = decimal.Decimal(entry(4, mess_str, "|"))
                            ordered_item.subtotal = ordered_item.price * ordered_item.qty
                            ordered_item.artnr = to_int(entry(1, mess_str, "|"))
                            ordered_item.bill_date = orderbill.date1
                            ordered_item.posted = orderbill_line.logi3
                            ordered_item.article_type = "SALES"
                            ordered_item.item_str = orderbill_line.char3
                            ordered_item.bline_str = orderbill_line.char2
                            ordered_item.webpost_flag = True

                            if num_entries(orderbill_line.char3, "|") >= 7:
                                ordered_item.hbline_recid = to_int(entry(6, orderbill_line.char3, "|"))
                                ordered_item.hbline_time = to_int(entry(7, orderbill_line.char3, "|"))

                                if num_entries(orderbill_line.char3, "|") >= 9:
                                    ordered_item.cancel_str = entry(8, orderbill_line.char3, "|")

                            if itemposted_flag == False:
                                ordered_item.order_status = "WAIT FOR WAITER CONFIRM"
                                ordered_item.sp_req = "WAIT FOR WAITER CONFIRM" + " - " + ordered_item.sp_req
                                ordered_item.count_amount = False

                            elif itemposted_flag :

                                if ordered_item.confirm == False:
                                    ordered_item.price = 0
                                    ordered_item.subtotal = 0
                                    ordered_item.order_status = "ORDER CANCELED"
                                    ordered_item.sp_req = "ORDER CANCELED" + " - " + ordered_item.sp_req
                                    ordered_item.count_amount = False
                                else:
                                    ordered_item.order_status = "ORDER POSTED"
                                    ordered_item.sp_req = "ORDER POSTED" + " - " + ordered_item.sp_req
                                    ordered_item.count_amount = True

            if bill_number != 0:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 557)).first()
                art_discfood = htparam.finteger

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 596)).first()
                art_discbev = htparam.finteger

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 556)).first()
                art_discother = htparam.finteger

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 1001)).first()
                art_voucher = htparam.finteger

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 855)).first()
                art_paycash = htparam.finteger

                for h_artikel in db_session.query(H_artikel).filter(
                        (H_artikel.departement == dept) &  (H_artikel.artart == 7) &  (H_artikel.activeflag)).all():
                    art_cc = art_cc + to_string(h_artikel.artnr) + ":"

                for h_artikel in db_session.query(H_artikel).filter(
                        (H_artikel.departement == dept) &  (H_artikel.artart == 2) &  (H_artikel.activeflag)).all():
                    art_cl = art_cl + to_string(h_artikel.artnr) + ";"

                h_bill = db_session.query(H_bill).filter(
                        (H_bill.departement == dept) &  (H_bill.rechnr == bill_number)).first()

                if h_bill:

                    if h_bill.flag == 0:
                        do_it = True
                    else:
                        do_it = False
                do_it = True

                if do_it:

                    for h_bill_line in db_session.query(H_bill_line).filter(
                            (H_bill_line.departement == dept) &  (H_bill_line.rechnr == bill_number)).all():

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.departement == dept) &  (H_artikel.artnr == h_bill_line.artnr)).first()

                        if h_artikel:

                            if h_artikel.artart != 0 and h_artikel.artart != 5:
                                payment_method = h_artikel.bezeich.upper()
                                break

                            elif h_artikel.artart != 0 and h_artikel.artart == 5:
                                payment_method = h_artikel.bezeich.upper()
                                break

                    for h_bill_line in db_session.query(H_bill_line).filter(
                            (H_bill_line.departement == dept) &  (H_bill_line.rechnr == bill_number)).all():

                        ordered_item = query(ordered_item_list, filters=(lambda ordered_item :ordered_item.hbline_recid == to_int(h_bill_line._recid) and ordered_item.hbline_time == h_bill_line.zeit), first=True)

                        if ordered_item:
                            1
                        else:

                            h_artikel = db_session.query(H_artikel).filter(
                                    (H_artikel.departement == dept) &  (H_artikel.artnr == h_bill_line.artnr)).first()

                            if h_artikel:

                                if h_artikel.artart == 0:
                                    art_type = "SALES"

                                elif h_artikel.artart == 5:
                                    art_type = "DEPOSIT"

                            if h_bill_line.anzahl < 0:
                                art_type = "VOID"
                            else:

                                if h_bill_line.artnr == art_discfood:
                                    art_type = "DISCOUNT FOOD"

                                elif h_bill_line.artnr == art_discbev:
                                    art_type = "DISCOUNT BEV"

                                elif h_bill_line.artnr == art_discother:
                                    art_type = "DISCOUNT OTHER"

                                elif h_bill_line.artnr == art_voucher:
                                    art_type = "VOUCHER"

                                elif h_bill_line.artnr == art_paycash:
                                    art_type = "PAYMENT CASH"
                                else:
                                    for loop_cc in range(1,num_entries(art_cc, ":")  + 1) :
                                        art_paycc = to_int(entry(loop_cc - 1, art_cc, ":"))

                                        if h_bill_line.artnr == art_paycc:
                                            art_type = "PAYMENT CCARD"
                                    for loop_cl in range(1,num_entries(art_cl, ";")  + 1) :
                                        art_paycl = to_int(entry(loop_cl - 1, art_cl, ";"))

                                        if h_bill_line.artnr == art_paycl:
                                            art_type = "PAYMENT CLEDGER"
                            ordered_item = Ordered_item()
                            ordered_item_list.append(ordered_item)

                            ordered_item.table_nr = h_bill_line.tischnr
                            ordered_item.order_nr = 0
                            ordered_item.bezeich = h_bill_line.bezeich
                            ordered_item.qty = h_bill_line.anzahl
                            ordered_item.sp_req = ""
                            ordered_item.confirm = True
                            ordered_item.remarks = ""
                            ordered_item.order_date = to_string(h_bill_line.bill_datum)
                            ordered_item.nr = 0
                            ordered_item.price = h_bill_line.nettobetrag
                            ordered_item.price = round(ordered_item.price, 2)
                            ordered_item.subtotal = h_bill_line.nettobetrag * h_bill_line.anzahl
                            ordered_item.artnr = h_bill_line.artnr
                            ordered_item.bill_date = h_bill_line.bill_datum
                            ordered_item.posted = True
                            ordered_item.article_type = art_type
                            ordered_item.count_amount = True

                            if ordered_item.qty > 1:
                                ordered_item.price = ordered_item.price / ordered_item.qty
                                ordered_item.subtotal = h_bill_line.nettobetrag

                            if ordered_item.posted == False:
                                ordered_item.order_status = "WAIT FOR WAITER CONFIRM"
                                ordered_item.sp_req = "WAIT FOR WAITER CONFIRM" + " - " + ordered_item.sp_req
                                ordered_item.count_amount = False

                            elif ordered_item.posted :

                                if ordered_item.confirm == False:
                                    ordered_item.price = 0
                                    ordered_item.subtotal = 0
                                    ordered_item.order_status = "ORDER CANCELED"
                                    ordered_item.sp_req = "ORDER CANCELED" + " - " + ordered_item.sp_req
                                    ordered_item.count_amount = False
                                else:
                                    ordered_item.order_status = "ORDER POSTED"
                                    ordered_item.sp_req = "ORDER POSTED" + " - " + ordered_item.sp_req
                                    ordered_item.count_amount = True

                    h_bill = db_session.query(H_bill).filter(
                            (H_bill.rechnr == bill_number) &  (H_bill.departement == dept)).first()

                    if h_bill:

                        if h_bill.flag == 0:

                            h_bill_line_obj_list = []
                            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement)).filter(
                                    (H_bill_line.rechnr == bill_number) &  (H_bill_line.departement == dept)).all():
                                if h_bill_line._recid in h_bill_line_obj_list:
                                    continue
                                else:
                                    h_bill_line_obj_list.append(h_bill_line._recid)


                                tot_amount = tot_amount + h_bill_line.betrag
                        else:
                            tot_amount = 0
            mess_result = "0_Order found success!"
        else:
            mess_result = "1_No order found!"

            return

    def cal_servat(depart:int, h_artnr:int, service_code:int, mwst_code:int, inpdate:date):

        nonlocal mess_result, user_name, dept_name, guest_name, pax, room, total_tax, total_service, total_price, total_payment, grand_total, sessionexpired, hold_payment, bill_number, payment_method, ordered_item_list, mess_str, i_str, mess_token, mess_keyword, mess_value, orderdatetime, gname, order_i, serv_perc, mwst_perc, fact, mmwst1, mwst, h_service, h_mwst, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, price_decimal, tax, serv, service, vat, vat2, fact_scvat, serv_vat, tax_vat, ct, l_deci, tot_amount, bill_date110, bill_date, service_taxable, sesion_id, servtax_use_foart, dynamic_qr, room_serviceflag, rm_no, str1, count_i, alpha_flag, found_bill, billno, do_it, queasy, htparam, bediener, hoteldpt, tisch, h_artikel, h_bill, h_bill_line, artikel
        nonlocal bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable, searchbill, mergebill, hbuff, abuff


        nonlocal ordered_item, bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable, searchbill, mergebill, hbuff, abuff
        nonlocal ordered_item_list

        serv% = 0
        mwst% = 0
        servat = 0
        serv_htp:decimal = 0
        vat_htp:decimal = 0
        vat2:decimal = 0

        def generate_inner_output():
            return serv%, mwst%, servat
        Hbuff = H_artikel
        Abuff = Artikel

        if servtax_use_foart:

            hbuff = db_session.query(Hbuff).filter(
                    (Hbuff.artnr == h_artnr) &  (Hbuff.departement == depart)).first()

            abuff = db_session.query(Abuff).filter(
                    (Abuff.artnr == hbuff.artnrfront) &  (Abuff.departement == depart)).first()
            serv%, mwst%, vat2, servat = get_output(calc_servtaxesbl(1, abuff.artnr, abuff.departement, inpdate))
            mwst% = mwst% + vat2


        else:

            if service_code != 0:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == service_code)).first()
                serv_htp = htparam.fdecimal / 100

            if mwst_code != 0:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == mwst_code)).first()
                vat_htp = htparam.fdecimal / 100

            if service_taxable:
                serv% = serv_htp
                mwst% = (1 + serv_htp) * vat_htp
                servat = 1 + serv% + mwst%


            else:
                serv% = serv_htp
                mwst% = vat_htp
                servat = 1 + serv% + mwst%


        return generate_inner_output()

    if session_parameter == None or session_parameter == "":
        mess_result = "1_Session Parameter can't be null value!"

        return generate_output()

    if dept == None or dept == 0:
        mess_result = "1_Department can't be null value!"

        return generate_output()

    if user_init == None or user_init == "":
        mess_result = "1_User Initials can't be null value!"

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 468)).first()

    if htparam:
        serv_disc = htparam.flogic

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 469)).first()

    if htparam:
        vat_disc = htparam.flogic

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()

    if htparam.finteger != 0:
        f_discart = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 376)).first()

    if htparam:

        if not htparam.flogic and entry(0, htparam.fchar, ";") == "GST(MA)":
            gst_logic = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 135)).first()
    incl_service = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 134)).first()
    incl_mwst = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 479)).first()
    service_taxable = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if bediener:
        user_name = bediener.username.upper()

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()

    if hoteldpt:
        dept_name = hoteldpt.depart.upper()
        servtax_use_foart = hoteldpt.defult

    qrqsy = db_session.query(Qrqsy).filter(
            (Qrqsy.key == 230) &  (func.lower(Qrqsy.char1) == (session_parameter).lower())).first()

    if qrqsy:
        sessionexpired = qrqsy.logi1

    for sosqsy in db_session.query(Sosqsy).filter(
            (Sosqsy.key == 222) &  (Sosqsy.number1 == 1) &  (Sosqsy.betriebsnr == dept)).all():

        if sosqsy.number2 == 14:
            dynamic_qr = sosqsy.logi1

        if sosqsy.number2 == 21:
            room_serviceflag = sosqsy.logi1

    if room_serviceflag:

        q_takentable = db_session.query(Q_takentable).filter(
                (Q_takentable.key == 225) &  (func.lower(Q_takentable.char1) == "taken_table") &  (Q_takentable.number2 == table_no) &  (entry(0, Q_takentable.char3, "|Q_takentable.Q_takentable.") == (session_parameter).lower()) &  (num_entries(Q_takentable.char3, "|Q_takentable.Q_takentable.") == 3)).first()

        if q_takentable:
            str1 = entry(2, q_takentable.char3, "|")
            rm_no = entry(0, str1, "$")

        if rm_no != "":
            for count_i in range(65,90 + 1) :

                if re.match(".*" + chr(count_i,rm_no) + "*"):
                    alpha_flag = True

            if not alpha_flag:
                count_i = 0
                for count_i in range(97,122 + 1) :

                    if re.match(".*" + chr(count_i,rm_no) + "*"):
                        alpha_flag = True

        if alpha_flag:

            tisch = db_session.query(Tisch).filter(
                    (Tisch.departement == dept) &  (Tischnr == table_no)).first()

            if tisch:
                room = substring(tisch.bezeich, 5)
        else:
            room = to_string(table_no)
    query_order()

    if mess_result.lower()  == "1_No order found!":
        billno = to_int(session_parameter)

        if billno != 0 and billno != None:
            do_it = True

        if do_it:

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 225) &  (Queasy.number1 == dept) &  (func.lower(Queasy.char1) == "orderbill")).all():
                mess_str = queasy.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, " == ")
                    mess_value = entry(1, mess_token, " == ")

                    if mess_keyword.lower()  == "BL":
                        found_bill = to_int(mess_value)
                        break

                if found_bill == billno:
                    session_parameter = queasy.char3
                    break
                else:
                    mess_result = "1_No order found!"
            query_order()

    for ordered_item in query(ordered_item_list):

        if order_i != ordered_item.order_nr:
            order_i = ordered_item.order_nr

        for bufforder in query(bufforder_list, filters=(lambda bufforder :bufforder.order_nr == order_i)):
            ordered_item.subtotalprice = ordered_item.subtotalprice + bufforder.subtotal

    for ordered_item in query(ordered_item_list, filters=(lambda ordered_item :ordered_item.count_amount)):

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.departement == dept) &  (H_artikel.artnr == ordered_item.artnr)).first()

        if h_artikel:
            mmwst1 = 0
            h_service = 0
            h_mwst = 0
            service = 0
            mwst = 0
            serv%, mwst%, fact = cal_servat(h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, ordered_item.bill_date)
            amount = ordered_item.price * (1 + serv% + mwst% + service)

            if not serv_disc and h_artikel.artnr == f_discart:
                pass
            else:
                h_service = amount / fact * serv%
                h_service = round(h_service, 2)

            if not vat_disc and h_artikel.artnr == f_discart:
                pass
            else:
                h_mwst = amount / fact * mwst%
                h_mwst = round(h_mwst, 2)

            if not incl_service:
                amount = amount - h_service
                service = service + h_service

            if not incl_mwst:
                amount = amount - h_mwst
                mwst = mwst + h_mwst
                mmwst1 = mmwst1 + h_mwst


            ordered_item.service = service
            ordered_item.tax = mmwst1

            if ordered_item.service == None:
                ordered_item.service = 0

            if ordered_item.tax == None:
                ordered_item.tax = 0
            ordered_item.service = ordered_item.service * ordered_item.qty
            ordered_item.tax = ordered_item.tax * ordered_item.qty

            if ordered_item.article_type.lower()  == "VOID":
                ordered_item.price = ordered_item.price / ordered_item.qty
                ordered_item.service = ordered_item.service / ordered_item.qty
                ordered_item.tax = ordered_item.tax / ordered_item.qty
                ordered_item.subtotal = ordered_item.price * ordered_item.qty
                ordered_item.price = ordered_item.price
                ordered_item.subtotal = ordered_item.subtotal
                ordered_item.service = ordered_item.service
                ordered_item.tax = ordered_item.tax

            if (ordered_item.article_type.lower()  == "SALES" or ordered_item.article_type.lower().lower()  == "VOID"):
                ordered_item.priceTaxServ = (ordered_item.price * ordered_item.qty) + ordered_item.service + ordered_item.tax
            else:
                ordered_item.priceTaxServ = ordered_item.subtotal

        if (re.match(".*PAYMENT.*",ordered_item.article_type) or re.match(".*VOUCHER.*",ordered_item.article_type) or re.match(".*DEPOSIT.*",ordered_item.article_type)):
            ordered_item.tax = 0
            ordered_item.service = 0
        total_price = total_price + ordered_item.subtotal
        total_tax = total_tax + ordered_item.tax
        total_service = total_service + ordered_item.service
    total_price = to_int(round(total_price, 2))
    total_tax = total_tax - 0.01
    total_tax = to_int(round(total_tax, 2))
    total_service = to_int(round(total_service, 2))
    grand_total = to_int(round(tot_amount, 2))

    return generate_output()