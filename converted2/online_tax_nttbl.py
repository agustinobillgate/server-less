from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import H_bill_line, Billjournal, Artikel, Hoteldpt, H_bill, H_artikel

def online_tax_nttbl(curr_date:date, from_time:int, to_time:int, if_time:int, if_date:date):
    tlist_list = []
    n:int = 1
    do_it:bool = False
    vat_artnr:List[int] = [0, 0, 0, 0, 0]
    revcode:str = ""
    serv_taxable:bool = False
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    netto:decimal = to_decimal("0.0")
    serv_betrag:decimal = to_decimal("0.0")
    vat_betrag:decimal = to_decimal("0.0")
    outstr:str = ""
    outstr1:str = ""
    rechnr_nottax:int = 0
    price_decimal:int = 0
    service_code:int = 0
    vat_proz:decimal = 10
    service_proz:decimal = 10
    i_counter:int = 0
    transdesc:str = ""
    delta_time:int = 0
    h_bill_line = billjournal = artikel = hoteldpt = h_bill = h_artikel = None

    log_list = tlist = j_list = s_list = t_list = hbill_list = hbill_buff = None

    log_list_list, Log_list = create_model("Log_list", {"log_ct":str})
    tlist_list, Tlist = create_model("Tlist", {"datum":date, "depart":int, "nopd":str, "pjk_type":int, "trans_type":int, "cabang":str, "masa_pajak":str, "billno":int, "qty":int, "invoice":int, "amount":decimal, "pajak":decimal, "timestamp":str, "bezeich":str})
    j_list_list, J_list = create_model("J_list", {"rechnr":int, "bill_datum":str, "cdtrx":str, "amount":decimal, "bezeich":str})
    s_list_list, S_list = create_model("S_list", {"rechnr":int, "bill_datum":str, "cdtrx":str, "amount":decimal, "bezeich":str})
    t_list_list, T_list = create_model("T_list", {"departement":int, "artnr":int, "bezeich":str, "rechnr":int, "bill_datum":date, "sysdate":date, "zeit":int, "fb":decimal, "other":decimal, "fb_service":decimal, "other_service":decimal, "fb_vat":decimal, "other_vat":decimal, "pay":decimal, "compli":decimal, "cdtrx":str}, {"cdtrx": ""})
    hbill_list_list, Hbill_list = create_model("Hbill_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":decimal}, {"do_it": True})

    Hbill_buff = create_buffer("Hbill_buff",H_bill_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tlist_list, n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, netto, serv_betrag, vat_betrag, outstr, outstr1, rechnr_nottax, price_decimal, service_code, vat_proz, service_proz, i_counter, transdesc, delta_time, h_bill_line, billjournal, artikel, hoteldpt, h_bill, h_artikel
        nonlocal curr_date, from_time, to_time, if_time, if_date
        nonlocal hbill_buff


        nonlocal log_list, tlist, j_list, s_list, t_list, hbill_list, hbill_buff
        nonlocal log_list_list, tlist_list, j_list_list, s_list_list, t_list_list, hbill_list_list

        return {"tlist": tlist_list}

    def datetime2char(datum:date, zeit:int):

        nonlocal tlist_list, n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, netto, serv_betrag, vat_betrag, outstr, outstr1, rechnr_nottax, price_decimal, service_code, vat_proz, service_proz, i_counter, transdesc, delta_time, h_bill_line, billjournal, artikel, hoteldpt, h_bill, h_artikel
        nonlocal curr_date, from_time, to_time, if_time, if_date
        nonlocal hbill_buff


        nonlocal log_list, tlist, j_list, s_list, t_list, hbill_list, hbill_buff
        nonlocal log_list_list, tlist_list, j_list_list, s_list_list, t_list_list, hbill_list_list

        str:str = ""
        str = to_string(get_year(datum) , "9999") + "-" +\
                to_string(get_month(datum) , "99") + "-" +\
                to_string(get_day(datum) , "99") + " " +\
                substring(to_string(zeit, "HH:MM:SS") , 0, 2) + ":" +\
                substring(to_string(zeit, "HH:MM:SS") , 3, 2) + ":" +\
                substring(to_string(zeit, "HH:MM:SS") , 6, 2)


        return str


    def step_1(to_date:date, start_time:int, end_time:int):

        nonlocal tlist_list, n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, netto, serv_betrag, vat_betrag, outstr, outstr1, rechnr_nottax, price_decimal, service_code, vat_proz, service_proz, i_counter, transdesc, delta_time, h_bill_line, billjournal, artikel, hoteldpt, h_bill, h_artikel
        nonlocal curr_date, from_time, to_time, if_time, if_date
        nonlocal hbill_buff


        nonlocal log_list, tlist, j_list, s_list, t_list, hbill_list, hbill_buff
        nonlocal log_list_list, tlist_list, j_list_list, s_list_list, t_list_list, hbill_list_list

        pay_amount:decimal = to_decimal("0.0")

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.sysdate == to_date) & (Billjournal.zeit >= start_time) & (Billjournal.zeit <= end_time) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal.rechnr, Billjournal.departement, Billjournal.artnr).all():
            do_it = True

            if do_it:

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == billjournal.artnr) & (Artikel.departement == billjournal.departement)).first()
                do_it = None != artikel and (artikel.mwst_code != 0 or artikel.service_code != 0)

                if do_it:
                    do_it = (artikel.artart == 0 or artikel.artart == 8)

            if not artikel:
                log_list = Log_list()
                log_list_list.append(log_list)

                log_list.log_ct = to_string(billjournal.departement, "99") +\
                        "-" + to_string(billjournal.artnr, "9999") +\
                        " Artikel not found"

            if artikel and artikel.mwst_code == 0 and (artikel.artart == 0 or artikel.artart == 8):
                log_list = Log_list()
                log_list_list.append(log_list)

                log_list.log_ct = to_string(billjournal.departement, "99") +\
                        "-" + to_string(billjournal.artnr, "9999") +\
                        " " + artikel.bezeich + " vat = 0"

            if do_it and re.match(r".*Remain.*",artikel.bezeich, re.IGNORECASE) and re.match(r".*Balance.*",artikel.bezeich, re.IGNORECASE):
                do_it = False
                log_list = Log_list()
                log_list_list.append(log_list)

                log_list.log_ct = to_string(billjournal.departement, "99") +\
                        "-" + to_string(billjournal.artnr, "9999") +\
                        " " + artikel.bezeich

            if do_it:

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == artikel.departement)).first()
                revcode = "OTHER"

                if artikel.artart == 0:

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6:
                        revcode = "FB"

                elif artikel.artart == 8:
                    revcode = "LODGING"
                serv =  to_decimal("0")
                vat =  to_decimal("0")
                netto =  to_decimal("0")
                serv_betrag =  to_decimal("0")
                vat_betrag =  to_decimal("0")


                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))

                if vat == 1:
                    vat_betrag =  to_decimal(billjournal.betrag)

                elif serv == 1:
                    serv_betrag =  to_decimal(billjournal.betrag)
                else:
                    netto =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                    serv_betrag =  to_decimal(netto) * to_decimal(serv)
                    vat_betrag =  to_decimal(netto) * to_decimal(vat)
                    netto = to_decimal(round(netto , 2))
                    vat_betrag = to_decimal(round(vat_betrag , 2))
                    serv_betrag = to_decimal(round(serv_betrag , 2))


                tlist = Tlist()
                tlist_list.append(tlist)

                tlist.datum = billjournal.bill_datum
                tlist.trans_type = 0
                tlist.cabang = "000"
                tlist.masa_pajak = to_string(get_month(billjournal.bill_datum) , "99") + to_string(get_year(billjournal.bill_datum) , "9999")
                tlist.billno = billjournal.rechnr
                tlist.qty = billjournal.anzahl
                tlist.invoice = billjournal.rechnr
                tlist.amount =  to_decimal(billjournal.betrag)
                tlist.pajak =  to_decimal(vat_betrag)
                tlist.timestamp = datetime2char (billjournal.bill_datum, billjournal.zeit)
                tlist.bezeich = billjournal.bezeich
                tlist.depart = billjournal.departement
                tlist.pjk_type = 3

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr > 0) & (H_bill_line.sysdate == to_date) & (H_bill_line.zeit >= start_time) & (H_bill_line.zeit <= end_time)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():

            h_bill = db_session.query(H_bill).filter(
                     (H_bill.rechnr == h_bill_line.rechnr) & (H_bill.departement == h_bill_line.departement)).first()

            hbill_list = query(hbill_list_list, filters=(lambda hbill_list: hbill_list.dept == h_bill_line.departement and hbill_list.rechnr == h_bill_line.rechnr), first=True)

            if not hbill_list:
                hbill_list = Hbill_list()
                hbill_list_list.append(hbill_list)

                hbill_list.dept = h_bill_line.departement
                hbill_list.rechnr = h_bill_line.rechnr
                hbill_list.do_it = (h_bill.flag == 1) or (h_bill.saldo == 0)

                if hbill_list.do_it:

                    hbill_buff = db_session.query(Hbill_buff).filter(
                             (Hbill_buff.departement == h_bill_line.departement) & (Hbill_buff.rechnr == h_bill_line.rechnr) & (Hbill_buff.sysdate > h_bill_line.sysdate)).first()
                    hbill_list.do_it = not None != hbill_buff

                    if hbill_list.do_it and h_bill.flag == 0:
                        log_list = Log_list()
                        log_list_list.append(log_list)

                        log_list.log_ct = to_string(get_current_time_in_seconds(), "HH:MM:SS") +\
                                " " + to_string(h_bill.departement, "99") +\
                                "-" + to_string(h_bill.rechnr) +\
                                " opened but zero balanced h-bill"

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it)):

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)


                hbill_list.tot_sales =  to_decimal(hbill_list.tot_sales) + to_decimal(h_bill_line.betrag)

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it  and hbill_list.tot_sales != 0)):
            pay_amount =  to_decimal("0")

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.sysdate == to_date)).order_by(H_bill_line.zeit.desc()).all():

                if h_bill_line.artnr == 0:
                    pay_amount =  to_decimal(pay_amount) + to_decimal(h_bill_line.betrag)
                else:

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.departement == h_bill_line.departement) & (H_artikel.artnr == h_bill_line.artnr)).first()

                    if h_artikel.artart == 2 or h_artikel.artart == 6 or h_artikel.artart == 7:
                        pay_amount =  to_decimal(pay_amount) + to_decimal(h_bill_line.betrag)
                hbill_list.i_fact = to_int(pay_amount != 0)

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it and hbill_list.i_fact != 0)):
            transdesc = ""

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                if artikel.artart == 9:
                    pass
                else:
                    netto =  to_decimal("0")
                    serv_betrag =  to_decimal("0")
                    vat_betrag =  to_decimal("0")


                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, h_bill_line.bill_datum, artikel.service_code, artikel.mwst_code))

                    if vat != 0 or serv != 0:

                        if vat == 1:
                            vat_betrag =  to_decimal(h_bill_line.betrag)

                        elif serv == 1:
                            serv_betrag =  to_decimal(h_bill_line.betrag)
                        else:
                            netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                            serv_betrag =  to_decimal(netto) * to_decimal(serv)
                            vat_betrag =  to_decimal(netto) * to_decimal(vat)
                            netto = to_decimal(round(netto , 2))
                            vat_betrag = to_decimal(round(vat_betrag , 2))
                            serv_betrag = to_decimal(round(serv_betrag , 2))


                        tlist = Tlist()
                        tlist_list.append(tlist)

                        tlist.datum = h_bill_line.bill_datum
                        tlist.trans_type = 0
                        tlist.cabang = "000"
                        tlist.masa_pajak = to_string(get_month(h_bill_line.bill_datum) , "99") + to_string(get_year(h_bill_line.bill_datum) , "9999")
                        tlist.billno = h_bill_line.rechnr
                        tlist.qty = h_bill_line.anzahl
                        tlist.invoice = h_bill_line.rechnr
                        tlist.amount =  to_decimal(h_bill_line.betrag)
                        tlist.pajak =  to_decimal(vat_betrag)
                        tlist.timestamp = datetime2char (h_bill_line.bill_datum, h_bill_line.zeit)
                        tlist.bezeich = h_bill_line.bezeich
                        tlist.depart = h_bill_line.departement
                        tlist.pjk_type = 8


        hbill_list_list.clear()

    if get_current_date() > if_date:
        to_time = 24 * 3600 - 1
        delta_time = if_time - get_current_time_in_seconds()

        if delta_time > 0:
            from_time = from_time - delta_time
        delta_time = 0
    else:
        delta_time = if_time - get_current_time_in_seconds()

    if delta_time > 0:
        from_time = from_time - delta_time
        to_time = to_time - delta_time

        if to_time < 0:
            from_time = from_time + 3600 * 24
            to_time = to_time + 3600 * 24
            curr_date = curr_date - timedelta(days=1)


            step_1(curr_date, from_time, to_time)

        elif from_time < 0:
            from_time = from_time + 3600 * 24
            curr_date = curr_date - timedelta(days=1)


            step_1(curr_date, from_time, 24 * 3600 - 1)

            if to_time > 0:
                curr_date = curr_date + timedelta(days=1)


                step_1(curr_date, 0, to_time)
        else:
            step_1(curr_date, from_time, to_time)
    else:
        step_1(curr_date, from_time, to_time)

    return generate_output()