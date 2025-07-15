#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Queasy, Htparam, Bediener, Hoteldpt, Tisch, H_artikel, H_bill, H_bill_line, Artikel

def selforder_viewordered_itembl(user_init:string, dept:int, table_no:int, session_parameter:string):

    prepare_cache ([Queasy, Htparam, Bediener, Hoteldpt, Tisch, H_artikel, H_bill, H_bill_line, Artikel])

    mess_result = ""
    user_name = ""
    dept_name = ""
    guest_name = ""
    pax = 0
    room = ""
    total_tax = to_decimal("0.0")
    total_service = to_decimal("0.0")
    total_price = to_decimal("0.0")
    total_payment = to_decimal("0.0")
    grand_total = to_decimal("0.0")
    sessionexpired = False
    hold_payment = False
    bill_number = 0
    payment_method = ""
    ordered_item_data = []
    mess_str:string = ""
    i_str:int = 0
    mess_token:string = ""
    mess_keyword:string = ""
    mess_value:string = ""
    orderdatetime:string = ""
    gname:string = ""
    order_i:int = 0
    serv_perc:Decimal = to_decimal("0.0")
    mwst_perc:Decimal = to_decimal("0.0")
    fact:Decimal = 1
    mmwst1:Decimal = to_decimal("0.0")
    mwst:Decimal = to_decimal("0.0")
    h_service:Decimal = to_decimal("0.0")
    h_mwst:Decimal = to_decimal("0.0")
    incl_service:bool = False
    incl_mwst:bool = False
    gst_logic:bool = False
    serv_disc:bool = True
    vat_disc:bool = True
    f_discart:int = -1
    amount:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    tax:Decimal = to_decimal("0.0")
    serv:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact_scvat:Decimal = 1
    serv_vat:bool = False
    tax_vat:bool = False
    ct:string = ""
    l_deci:int = 2
    tot_amount:Decimal = to_decimal("0.0")
    bill_date110:date = None
    bill_date:date = None
    service_taxable:bool = False
    sesion_id:string = ""
    servtax_use_foart:bool = False
    dynamic_qr:bool = False
    room_serviceflag:bool = False
    rm_no:string = ""
    str1:string = ""
    count_i:int = 0
    alpha_flag:bool = False
    found_bill:int = 0
    billno:int = 0
    do_it:bool = False
    queasy = htparam = bediener = hoteldpt = tisch = h_artikel = h_bill = h_bill_line = artikel = None

    ordered_item = bqsy = bposted = qrqsy = queasyorderbill = orderbill = orderbill_line = orderbill_posted = bufforder = sosqsy = q_takentable = None

    ordered_item_data, Ordered_item = create_model("Ordered_item", {"table_nr":int, "order_nr":int, "nr":int, "bezeich":string, "qty":int, "sp_req":string, "confirm":bool, "remarks":string, "order_date":string, "price":Decimal, "subtotal":Decimal, "subtotalprice":Decimal, "artnr":int, "service":Decimal, "tax":Decimal, "bill_date":date, "order_status":string, "count_amount":bool, "posted":bool, "article_type":string, "pricetaxserv":Decimal, "webpost_flag":bool, "hbline_recid":int, "hbline_time":int, "item_str":string, "bline_str":string, "amount":Decimal, "cancel_str":string})

    Bqsy = create_buffer("Bqsy",Queasy)
    Bposted = create_buffer("Bposted",Queasy)
    Qrqsy = create_buffer("Qrqsy",Queasy)
    Queasyorderbill = create_buffer("Queasyorderbill",Queasy)
    Orderbill = create_buffer("Orderbill",Queasy)
    Orderbill_line = create_buffer("Orderbill_line",Queasy)
    Orderbill_posted = create_buffer("Orderbill_posted",Queasy)
    Bufforder = Ordered_item
    bufforder_data = ordered_item_data

    Sosqsy = create_buffer("Sosqsy",Queasy)
    Q_takentable = create_buffer("Q_takentable",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, user_name, dept_name, guest_name, pax, room, total_tax, total_service, total_price, total_payment, grand_total, sessionexpired, hold_payment, bill_number, payment_method, ordered_item_data, mess_str, i_str, mess_token, mess_keyword, mess_value, orderdatetime, gname, order_i, serv_perc, mwst_perc, fact, mmwst1, mwst, h_service, h_mwst, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, price_decimal, tax, serv, service, vat, vat2, fact_scvat, serv_vat, tax_vat, ct, l_deci, tot_amount, bill_date110, bill_date, service_taxable, sesion_id, servtax_use_foart, dynamic_qr, room_serviceflag, rm_no, str1, count_i, alpha_flag, found_bill, billno, do_it, queasy, htparam, bediener, hoteldpt, tisch, h_artikel, h_bill, h_bill_line, artikel
        nonlocal user_init, dept, table_no, session_parameter
        nonlocal bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable


        nonlocal ordered_item, bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable
        nonlocal ordered_item_data

        return {"mess_result": mess_result, "user_name": user_name, "dept_name": dept_name, "guest_name": guest_name, "pax": pax, "room": room, "total_tax": total_tax, "total_service": total_service, "total_price": total_price, "total_payment": total_payment, "grand_total": grand_total, "sessionexpired": sessionexpired, "hold_payment": hold_payment, "bill_number": bill_number, "payment_method": payment_method, "ordered-item": ordered_item_data}

    def query_order():

        nonlocal mess_result, user_name, dept_name, guest_name, pax, room, total_tax, total_service, total_price, total_payment, grand_total, sessionexpired, hold_payment, bill_number, payment_method, ordered_item_data, mess_str, i_str, mess_token, mess_keyword, mess_value, orderdatetime, gname, order_i, serv_perc, mwst_perc, fact, mmwst1, mwst, h_service, h_mwst, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, price_decimal, tax, serv, service, vat, vat2, fact_scvat, serv_vat, tax_vat, ct, l_deci, tot_amount, bill_date110, bill_date, service_taxable, sesion_id, servtax_use_foart, dynamic_qr, room_serviceflag, rm_no, str1, count_i, alpha_flag, found_bill, billno, queasy, htparam, bediener, hoteldpt, tisch, h_artikel, h_bill, h_bill_line, artikel
        nonlocal user_init, dept, table_no, session_parameter
        nonlocal bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable


        nonlocal ordered_item, bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable
        nonlocal ordered_item_data

        posted_flag:bool = False
        itemposted_flag:bool = False
        bill_nr:int = 0
        searchbill = None
        mergebill = None
        art_type:string = ""
        art_discfood:int = 0
        art_discbev:int = 0
        art_discother:int = 0
        art_voucher:int = 0
        art_paycash:int = 0
        art_cc:string = ""
        loop_cc:int = 0
        art_cl:string = ""
        loop_cl:int = 0
        art_paycc:int = 0
        art_paycl:int = 0
        art_reczeit:string = ""
        do_it:bool = False
        Searchbill =  create_buffer("Searchbill",Queasy)
        Mergebill =  create_buffer("Mergebill",Queasy)

        searchbill = get_cache (Queasy, {"key": [(eq, 225)],"number1": [(eq, dept)],"char1": [(eq, "orderbill")],"char3": [(eq, session_parameter)],"number3": [(ne, 0)]})

        if searchbill:
            mess_str = searchbill.char2
            for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                mess_token = entry(i_str - 1, mess_str, "|")
                mess_keyword = entry(0, mess_token, "=")
                mess_value = entry(1, mess_token, "=")

                if mess_keyword.lower()  == ("RN").lower() :
                    room = mess_value

                elif mess_keyword.lower()  == ("PX").lower() :
                    pax = to_int(mess_value)

                elif mess_keyword.lower()  == ("NM").lower() :
                    gname = mess_value

                elif mess_keyword.lower()  == ("DT").lower() :
                    orderdatetime = mess_value

                elif mess_keyword.lower()  == ("BL").lower() :
                    bill_number = to_int(mess_value)

            for orderbill in db_session.query(Orderbill).filter(
                     (Orderbill.key == 225) & (Orderbill.number1 == dept) & (Orderbill.char1 == ("orderbill").lower()) & (Orderbill.char3 == (session_parameter).lower()) & (Orderbill.logi1)).order_by(Orderbill.number2).yield_per(100):
                mess_str = orderbill.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, "=")
                    mess_value = entry(1, mess_token, "=")

                    if mess_keyword.lower()  == ("BL").lower() :
                        bill_nr = to_int(mess_value)

                if bill_nr != 0:
                    bill_number = bill_nr
                    posted_flag = True
                    break

            for orderbill in db_session.query(Orderbill).filter(
                     (Orderbill.key == 225) & (Orderbill.number1 == dept) & (Orderbill.char1 == ("orderbill").lower()) & (Orderbill.char3 == (session_parameter).lower()) & (Orderbill.logi1)).order_by(Orderbill.number2, Orderbill.number3).all():
                mess_str = orderbill.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, "=")
                    mess_value = entry(1, mess_token, "=")

                    if mess_keyword.lower()  == ("DT").lower() :
                        orderdatetime = mess_value

                for orderbill_line in db_session.query(Orderbill_line).filter(
                         (Orderbill_line.key == 225) & (Orderbill_line.char1 == ("orderbill-line").lower()) & (Orderbill_line.number2 == orderbill.number2) & (Orderbill_line.number1 == orderbill.number3) & (Orderbill_line.date1 == orderbill.date1) & (entry(2, Orderbill_line.char2, "|") == (orderdatetime).lower())).order_by(Orderbill_line.number1).all():
                    total_payment =  to_decimal(orderbill.deci1)
                    guest_name = gname.upper()
                    itemposted_flag = orderbill.logi3

                    if num_entries(orderbill_line.char2, "|") >= 4:
                        sesion_id = entry(3, orderbill_line.char2, "|")

                    if sesion_id.lower()  == (session_parameter).lower() :
                        mess_str = orderbill_line.char3

                        ordered_item = query(ordered_item_data, filters=(lambda ordered_item: ordered_item.item_str == orderbill_line.char3 and ordered_item.bline_str == orderbill_line.char2), first=True)

                        if not ordered_item:
                            ordered_item = Ordered_item()
                            ordered_item_data.append(ordered_item)

                            ordered_item.table_nr = orderbill.number2
                            ordered_item.order_nr = orderbill_line.number1
                            ordered_item.bezeich = entry(2, mess_str, "|")
                            ordered_item.qty = to_int(entry(3, mess_str, "|"))
                            ordered_item.sp_req = entry(5, mess_str, "|")
                            ordered_item.confirm = orderbill_line.logi2
                            ordered_item.remarks = ""
                            ordered_item.order_date = entry(2, orderbill_line.char2, "|")
                            ordered_item.nr = orderbill_line.number3
                            ordered_item.price =  to_decimal(to_decimal(entry(4 , mess_str , "|")) )
                            ordered_item.subtotal =  to_decimal(ordered_item.price) * to_decimal(ordered_item.qty)
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
                                    ordered_item.price =  to_decimal("0")
                                    ordered_item.subtotal =  to_decimal("0")
                                    ordered_item.order_status = "ORDER CANCELED"
                                    ordered_item.sp_req = "ORDER CANCELED" + " - " + ordered_item.sp_req
                                    ordered_item.count_amount = False
                                else:
                                    ordered_item.order_status = "ORDER POSTED"
                                    ordered_item.sp_req = "ORDER POSTED" + " - " + ordered_item.sp_req
                                    ordered_item.count_amount = True

            if bill_number != 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
                art_discfood = htparam.finteger

                htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
                art_discbev = htparam.finteger

                htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
                art_discother = htparam.finteger

                htparam = get_cache (Htparam, {"paramnr": [(eq, 1001)]})
                art_voucher = htparam.finteger

                htparam = get_cache (Htparam, {"paramnr": [(eq, 855)]})
                art_paycash = htparam.finteger

                for h_artikel in db_session.query(H_artikel).filter(
                         (H_artikel.departement == dept) & (H_artikel.artart == 7) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():
                    art_cc = art_cc + to_string(h_artikel.artnr) + ":"

                for h_artikel in db_session.query(H_artikel).filter(
                         (H_artikel.departement == dept) & (H_artikel.artart == 2) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():
                    art_cl = art_cl + to_string(h_artikel.artnr) + ";"

                h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"rechnr": [(eq, bill_number)]})

                if h_bill:

                    if h_bill.flag == 0:
                        do_it = True
                    else:
                        do_it = False
                do_it = True

                if do_it:

                    for h_bill_line in db_session.query(H_bill_line).filter(
                             (H_bill_line.departement == dept) & (H_bill_line.rechnr == bill_number)).order_by(H_bill_line._recid).yield_per(100):

                        h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, h_bill_line.artnr)]})

                        if h_artikel:

                            if h_artikel.artart != 0 and h_artikel.artart != 5:
                                payment_method = h_artikel.bezeich.upper()
                                break

                            elif h_artikel.artart != 0 and h_artikel.artart == 5:
                                payment_method = h_artikel.bezeich.upper()
                                break

                    for h_bill_line in db_session.query(H_bill_line).filter(
                             (H_bill_line.departement == dept) & (H_bill_line.rechnr == bill_number)).order_by(H_bill_line.bill_datum.desc(), H_bill_line.zeit.desc()).all():

                        ordered_item = query(ordered_item_data, filters=(lambda ordered_item: ordered_item.hbline_recid == to_int(h_bill_line._recid) and ordered_item.hbline_time == h_bill_line.zeit), first=True)

                        if ordered_item:
                            pass
                        else:

                            h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, h_bill_line.artnr)]})

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
                            ordered_item_data.append(ordered_item)

                            ordered_item.table_nr = h_bill_line.tischnr
                            ordered_item.order_nr = 0
                            ordered_item.bezeich = h_bill_line.bezeich
                            ordered_item.qty = h_bill_line.anzahl
                            ordered_item.sp_req = ""
                            ordered_item.confirm = True
                            ordered_item.remarks = ""
                            ordered_item.order_date = to_string(h_bill_line.bill_datum)
                            ordered_item.nr = 0
                            ordered_item.price =  to_decimal(h_bill_line.nettobetrag)
                            ordered_item.price = to_decimal(round(ordered_item.price , 2))
                            ordered_item.subtotal =  to_decimal(h_bill_line.nettobetrag) * to_decimal(h_bill_line.anzahl)
                            ordered_item.artnr = h_bill_line.artnr
                            ordered_item.bill_date = h_bill_line.bill_datum
                            ordered_item.posted = True
                            ordered_item.article_type = art_type
                            ordered_item.count_amount = True

                            if ordered_item.qty > 1:
                                ordered_item.price =  to_decimal(ordered_item.price) / to_decimal(ordered_item.qty)
                                ordered_item.subtotal =  to_decimal(h_bill_line.nettobetrag)

                            if ordered_item.posted == False:
                                ordered_item.order_status = "WAIT FOR WAITER CONFIRM"
                                ordered_item.sp_req = "WAIT FOR WAITER CONFIRM" + " - " + ordered_item.sp_req
                                ordered_item.count_amount = False

                            elif ordered_item.posted :

                                if ordered_item.confirm == False:
                                    ordered_item.price =  to_decimal("0")
                                    ordered_item.subtotal =  to_decimal("0")
                                    ordered_item.order_status = "ORDER CANCELED"
                                    ordered_item.sp_req = "ORDER CANCELED" + " - " + ordered_item.sp_req
                                    ordered_item.count_amount = False
                                else:
                                    ordered_item.order_status = "ORDER POSTED"
                                    ordered_item.sp_req = "ORDER POSTED" + " - " + ordered_item.sp_req
                                    ordered_item.count_amount = True

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, bill_number)],"departement": [(eq, dept)]})

                    if h_bill:

                        if h_bill.flag == 0:

                            h_bill_line_obj_list = {}
                            h_bill_line = H_bill_line()
                            h_artikel = H_artikel()
                            for h_bill_line.artnr, h_bill_line._recid, h_bill_line.zeit, h_bill_line.tischnr, h_bill_line.bezeich, h_bill_line.anzahl, h_bill_line.bill_datum, h_bill_line.nettobetrag, h_bill_line.betrag, h_artikel.artnr, h_artikel.artart, h_artikel.bezeich, h_artikel.departement, h_artikel.service_code, h_artikel.mwst_code, h_artikel._recid, h_artikel.artnrfront in db_session.query(H_bill_line.artnr, H_bill_line._recid, H_bill_line.zeit, H_bill_line.tischnr, H_bill_line.bezeich, H_bill_line.anzahl, H_bill_line.bill_datum, H_bill_line.nettobetrag, H_bill_line.betrag, H_artikel.artnr, H_artikel.artart, H_artikel.bezeich, H_artikel.departement, H_artikel.service_code, H_artikel.mwst_code, H_artikel._recid, H_artikel.artnrfront).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).filter(
                                     (H_bill_line.rechnr == bill_number) & (H_bill_line.departement == dept)).order_by(H_bill_line._recid).all():
                                if h_bill_line_obj_list.get(h_bill_line._recid):
                                    continue
                                else:
                                    h_bill_line_obj_list[h_bill_line._recid] = True


                                tot_amount =  to_decimal(tot_amount) + to_decimal(h_bill_line.betrag)
                        else:
                            tot_amount =  to_decimal("0")
            mess_result = "0-Order found success!"
        else:
            mess_result = "1-No order found!"

            return


    def cal_servat(depart:int, h_artnr:int, service_code:int, mwst_code:int, inpdate:date):

        nonlocal mess_result, user_name, dept_name, guest_name, pax, room, total_tax, total_service, total_price, total_payment, grand_total, sessionexpired, hold_payment, bill_number, payment_method, ordered_item_data, mess_str, i_str, mess_token, mess_keyword, mess_value, orderdatetime, gname, order_i, serv_perc, mwst_perc, fact, mmwst1, mwst, h_service, h_mwst, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, price_decimal, tax, serv, service, vat, fact_scvat, serv_vat, tax_vat, ct, l_deci, tot_amount, bill_date110, bill_date, service_taxable, sesion_id, servtax_use_foart, dynamic_qr, room_serviceflag, rm_no, str1, count_i, alpha_flag, found_bill, billno, do_it, queasy, htparam, bediener, hoteldpt, tisch, h_artikel, h_bill, h_bill_line, artikel
        nonlocal user_init, dept, table_no, session_parameter
        nonlocal bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable


        nonlocal ordered_item, bqsy, bposted, qrqsy, queasyorderbill, orderbill, orderbill_line, orderbill_posted, bufforder, sosqsy, q_takentable
        nonlocal ordered_item_data

        serv_perc = to_decimal("0.0")
        mwst_perc = to_decimal("0.0")
        servat = to_decimal("0.0")
        serv_htp:Decimal = to_decimal("0.0")
        vat_htp:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        hbuff = None
        abuff = None

        def generate_inner_output():
            return (serv_perc, mwst_perc, servat)

        Hbuff =  create_buffer("Hbuff",H_artikel)
        Abuff =  create_buffer("Abuff",Artikel)

        if servtax_use_foart:

            hbuff = get_cache (H_artikel, {"artnr": [(eq, h_artnr)],"departement": [(eq, depart)]})

            abuff = get_cache (Artikel, {"artnr": [(eq, hbuff.artnrfront)],"departement": [(eq, depart)]})
            serv_perc, mwst_perc, vat2, servat = get_output(calc_servtaxesbl(1, abuff.artnr, abuff.departement, inpdate))
            mwst_perc =  to_decimal(mwst_perc) + to_decimal(vat2)


        else:

            if service_code != 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, service_code)]})
                serv_htp =  to_decimal(htparam.fdecimal) / to_decimal("100")

            if mwst_code != 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, mwst_code)]})
                vat_htp =  to_decimal(htparam.fdecimal) / to_decimal("100")

            if service_taxable:
                serv_perc =  to_decimal(serv_htp)
                mwst_perc = ( to_decimal("1") + to_decimal(serv_htp)) * to_decimal(vat_htp)
                servat =  to_decimal("1") + to_decimal(serv_perc) + to_decimal(mwst_perc)


            else:
                serv_perc =  to_decimal(serv_htp)
                mwst_perc =  to_decimal(vat_htp)
                servat =  to_decimal("1") + to_decimal(serv_perc) + to_decimal(mwst_perc)

        return generate_inner_output()


    if session_parameter == None or session_parameter == "":
        mess_result = "1-Session Parameter can't be null value!"

        return generate_output()

    if dept == None or dept == 0:
        mess_result = "1-Department can't be null value!"

        return generate_output()

    if user_init == None or user_init == "":
        mess_result = "1-User Initials can't be null value!"

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 468)]})

    if htparam:
        serv_disc = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 469)]})

    if htparam:
        vat_disc = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam.finteger != 0:
        f_discart = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 376)]})

    if htparam:

        if not htparam.flogical and entry(0, htparam.fchar, ";") == ("GST(MA)").lower() :
            gst_logic = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})
    incl_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
    incl_mwst = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    service_taxable = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        user_name = bediener.username.upper()

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})

    if hoteldpt:
        dept_name = hoteldpt.depart.upper()
        servtax_use_foart = hoteldpt.defult

    qrqsy = get_cache (Queasy, {"key": [(eq, 230)],"char1": [(eq, session_parameter)]})

    if qrqsy:
        sessionexpired = qrqsy.logi1

    for sosqsy in db_session.query(Sosqsy).filter(
             (Sosqsy.key == 222) & (Sosqsy.number1 == 1) & (Sosqsy.betriebsnr == dept)).order_by(Sosqsy._recid).all():

        if sosqsy.number2 == 14:
            dynamic_qr = sosqsy.logi1

        if sosqsy.number2 == 21:
            room_serviceflag = sosqsy.logi1

    if room_serviceflag:

        q_takentable = db_session.query(Q_takentable).filter(
                 (Q_takentable.key == 225) & (Q_takentable.char1 == ("taken-table").lower()) & (Q_takentable.number2 == table_no) & (entry(0, Q_takentable.char3, "|") == (session_parameter).lower()) & (num_entries(Q_takentable.char3, "|") == 3)).first()

        if q_takentable:
            str1 = entry(2, q_takentable.char3, "|")
            rm_no = entry(0, str1, "$")

        if rm_no != "":
            for count_i in range(65,90 + 1) :

                if matches(rm_no,r"*" + chr_unicode(count_i) + r"*"):
                    alpha_flag = True

            if not alpha_flag:
                count_i = 0
                for count_i in range(97,122 + 1) :

                    if matches(rm_no,r"*" + chr_unicode(count_i) + r"*"):
                        alpha_flag = True

        if alpha_flag:

            tisch = get_cache (Tisch, {"departement": [(eq, dept)],"tischnr": [(eq, table_no)]})

            if tisch:
                room = substring(tisch.bezeich, 5)
        else:
            room = to_string(table_no)
    query_order()

    if mess_result.lower()  == ("1-No order found!").lower() :
        billno = to_int(session_parameter)

        if billno != 0 and billno != None:
            do_it = True

        if do_it:

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 225) & (Queasy.number1 == dept) & (Queasy.char1 == ("orderbill").lower())).order_by(Queasy._recid).yield_per(100):
                mess_str = queasy.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, "=")
                    mess_value = entry(1, mess_token, "=")

                    if mess_keyword.lower()  == ("BL").lower() :
                        found_bill = to_int(mess_value)
                        break

                if found_bill == billno:
                    session_parameter = queasy.char3
                    break
                else:
                    mess_result = "1-No order found!"
            query_order()

    for ordered_item in query(ordered_item_data, sort_by=[("order_nr",False)]):

        if order_i != ordered_item.order_nr:
            order_i = ordered_item.order_nr

        for bufforder in query(bufforder_data, filters=(lambda bufforder: bufforder.order_nr == order_i)):
            ordered_item.subtotalprice =  to_decimal(ordered_item.subtotalprice) + to_decimal(bufforder.subtotal)

    for ordered_item in query(ordered_item_data, filters=(lambda ordered_item: ordered_item.count_amount), sort_by=[("order_nr",False)]):

        h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, ordered_item.artnr)]})

        if h_artikel:
            mmwst1 =  to_decimal("0")
            h_service =  to_decimal("0")
            h_mwst =  to_decimal("0")
            service =  to_decimal("0")
            mwst =  to_decimal("0")
            serv_perc, mwst_perc, fact = cal_servat(h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, ordered_item.bill_date)
            amount =  to_decimal(ordered_item.price) * to_decimal((1) + to_decimal(serv_perc) + to_decimal(mwst_perc) + to_decimal(service))

            if not serv_disc and h_artikel.artnr == f_discart:
                pass
            else:
                h_service =  to_decimal(amount) / to_decimal(fact) * to_decimal(serv_perc)
                h_service = to_decimal(round(h_service , 2))

            if not vat_disc and h_artikel.artnr == f_discart:
                pass
            else:
                h_mwst =  to_decimal(amount) / to_decimal(fact) * to_decimal(mwst_perc)
                h_mwst = to_decimal(round(h_mwst , 2))

            if not incl_service:
                amount =  to_decimal(amount) - to_decimal(h_service)
                service =  to_decimal(service) + to_decimal(h_service)

            if not incl_mwst:
                amount =  to_decimal(amount) - to_decimal(h_mwst)
                mwst =  to_decimal(mwst) + to_decimal(h_mwst)
                mmwst1 =  to_decimal(mmwst1) + to_decimal(h_mwst)


            ordered_item.service =  to_decimal(service)
            ordered_item.tax =  to_decimal(mmwst1)

            if ordered_item.service == None:
                ordered_item.service =  to_decimal("0")

            if ordered_item.tax == None:
                ordered_item.tax =  to_decimal("0")
            ordered_item.service =  to_decimal(ordered_item.service) * to_decimal(ordered_item.qty)
            ordered_item.tax =  to_decimal(ordered_item.tax) * to_decimal(ordered_item.qty)

            if ordered_item.article_type.lower()  == ("VOID").lower() :
                ordered_item.price =  to_decimal(ordered_item.price) / to_decimal(ordered_item.qty)
                ordered_item.service =  to_decimal(ordered_item.service) / to_decimal(ordered_item.qty)
                ordered_item.tax =  to_decimal(ordered_item.tax) / to_decimal(ordered_item.qty)
                ordered_item.subtotal =  to_decimal(ordered_item.price) * to_decimal(ordered_item.qty)
                ordered_item.price =  to_decimal(ordered_item.price)
                ordered_item.subtotal =  to_decimal(ordered_item.subtotal)
                ordered_item.service =  to_decimal(ordered_item.service)
                ordered_item.tax =  to_decimal(ordered_item.tax)

            if (ordered_item.article_type.lower()  == ("SALES").lower()  or ordered_item.article_type.lower()  == ("VOID").lower()):
                ordered_item.pricetaxserv = ( to_decimal(ordered_item.price) * to_decimal(ordered_item.qty)) + to_decimal(ordered_item.service) + to_decimal(ordered_item.tax)
            else:
                ordered_item.pricetaxserv =  to_decimal(ordered_item.subtotal)

        if matches((ordered_item.article_type,r"*PAYMENT*") or matches(ordered_item.article_type,r"*VOUCHER*") or matches(ordered_item.article_type,r"*DEPOSIT*")):
            ordered_item.tax =  to_decimal("0")
            ordered_item.service =  to_decimal("0")
        total_price =  to_decimal(total_price) + to_decimal(ordered_item.subtotal)
        total_tax =  to_decimal(total_tax) + to_decimal(ordered_item.tax)
        total_service =  to_decimal(total_service) + to_decimal(ordered_item.service)
    total_price = to_decimal(to_int(round(total_price , 2)))
    total_tax =  to_decimal(total_tax) - to_decimal(0.01)
    total_tax = to_decimal(to_int(round(total_tax , 2)))
    total_service = to_decimal(to_int(round(total_service , 2)))
    grand_total = to_decimal(to_int(round(tot_amount , 2)))

    return generate_output()