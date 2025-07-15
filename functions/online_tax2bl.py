from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.calc_servvat import calc_servvat
from models import H_bill_line, Billjournal, Artikel, Hoteldpt, H_bill, H_artikel

def online_tax2bl(curr_date:date, from_time:int, to_time:int, if_time:int, if_date:date):
    revenue_list_list = []
    log_list_list = []
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

    log_list = revenue_list = fo_list = j_list = s_list = t_list = hbill_list = hbill_buff = None

    log_list_list, Log_list = create_model("Log_list", {"log_ct":str})
    revenue_list_list, Revenue_list = create_model("Revenue_list", {"sysdate":date, "zeit":int, "bill_datum":date, "departement":int, "rechnr":int, "artnr":int, "bezeich":str, "cdtrx":str, "betrag":decimal, "serv_betrag":decimal, "vat_betrag":decimal})
    fo_list_list, Fo_list = create_model("Fo_list", {"rechnr":int, "artnr":int, "departement":int, "zeit":int, "sysdate":date, "bill_datum":date, "cdtrx":str, "amount":decimal, "betrag":decimal, "serv_betrag":decimal, "vat_betrag":decimal, "bezeich":str})
    j_list_list, J_list = create_model("J_list", {"rechnr":int, "bill_datum":str, "cdtrx":str, "amount":decimal, "bezeich":str})
    s_list_list, S_list = create_model("S_list", {"rechnr":int, "bill_datum":str, "cdtrx":str, "amount":decimal, "bezeich":str})
    t_list_list, T_list = create_model("T_list", {"departement":int, "artnr":int, "bezeich":str, "rechnr":int, "bill_datum":date, "sysdate":date, "zeit":int, "fb":decimal, "other":decimal, "fb_service":decimal, "other_service":decimal, "fb_vat":decimal, "other_vat":decimal, "pay":decimal, "compli":decimal, "cdtrx":str}, {"cdtrx": ""})
    hbill_list_list, Hbill_list = create_model("Hbill_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":decimal}, {"do_it": True})

    Hbill_buff = create_buffer("Hbill_buff",H_bill_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal revenue_list_list, log_list_list, n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, netto, serv_betrag, vat_betrag, outstr, outstr1, rechnr_nottax, price_decimal, service_code, vat_proz, service_proz, i_counter, transdesc, delta_time, h_bill_line, billjournal, artikel, hoteldpt, h_bill, h_artikel
        nonlocal curr_date, from_time, to_time, if_time, if_date
        nonlocal hbill_buff


        nonlocal log_list, revenue_list, fo_list, j_list, s_list, t_list, hbill_list, hbill_buff
        nonlocal log_list_list, revenue_list_list, fo_list_list, j_list_list, s_list_list, t_list_list, hbill_list_list

        return {"revenue-list": revenue_list_list, "log-list": log_list_list}

    def step_1(to_date:date, start_time:int, end_time:int):

        nonlocal revenue_list_list, log_list_list, n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, netto, serv_betrag, vat_betrag, outstr, outstr1, rechnr_nottax, price_decimal, service_code, vat_proz, service_proz, i_counter, transdesc, delta_time, h_bill_line, billjournal, artikel, hoteldpt, h_bill, h_artikel
        nonlocal curr_date, from_time, to_time, if_time, if_date
        nonlocal hbill_buff


        nonlocal log_list, revenue_list, fo_list, j_list, s_list, t_list, hbill_list, hbill_buff
        nonlocal log_list_list, revenue_list_list, fo_list_list, j_list_list, s_list_list, t_list_list, hbill_list_list

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

            if billjournal.departement == 15:
                pass

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


                revenue_list = Revenue_list()
                revenue_list_list.append(revenue_list)

                buffer_copy(billjournal, revenue_list)
                revenue_list.cdtrx = revcode
                revenue_list.serv_betrag =  to_decimal(serv_betrag)
                revenue_list.vat_betrag =  to_decimal(vat_betrag)
                revenue_list.betrag =  to_decimal(netto)


                log_list = Log_list()
                log_list_list.append(log_list)

                log_list.log_ct = to_string(billjournal.departement, "99") +\
                        "-" + to_string(billjournal.artnr, "9999") +\
                        " " + artikel.bezeich +\
                        " | " + to_string(billjournal.bill_datum) +\
                        " | " + to_string(billjournal.sysdate) +\
                        "-" + to_string(billjournal.zeit, "HH:MM:SS")

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

                t_list = query(t_list_list, filters=(lambda t_list: t_list.rechnr == h_bill_line.rechnr and t_list.departement == h_bill_line.departement and t_list.bill_datum == h_bill_line.bill_datum), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    buffer_copy(h_bill_line, t_list,except_fields=["bezeich"])

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


                        t_list.bezeich = t_list.bezeich + h_bill_line.bezeich + "^" + to_string(h_bill_line.anzahl) + "^" + to_string(h_bill_line.epreis) + "|"

                        if artikel.umsatzart == 3 or artikel.umsatzart >= 5:
                            t_list.fb =  to_decimal(t_list.fb) + to_decimal((netto) * to_decimal(hbill_list.i_fact) )
                            t_list.fb_service =  to_decimal(t_list.fb_service) + to_decimal((serv_betrag) * to_decimal(hbill_list.i_fact) )
                            t_list.fb_vat =  to_decimal(t_list.fb_vat) + to_decimal((vat_betrag) * to_decimal(hbill_list.i_fact) )


                        else:
                            t_list.other =  to_decimal(t_list.other) + to_decimal((netto) * to_decimal(hbill_list.i_fact) )
                            t_list.other_service =  to_decimal(t_list.other_service) + to_decimal((serv_betrag) * to_decimal(hbill_list.i_fact) )
                            t_list.other_vat =  to_decimal(t_list.other_vat) + to_decimal((vat_betrag) * to_decimal(hbill_list.i_fact) )


                        log_list = Log_list()
                        log_list_list.append(log_list)

                        log_list.log_ct = to_string(t_list.departement, "99") +\
                                "-" + to_string(t_list.artnr, "9999") +\
                                " " + artikel.bezeich +\
                                " | " + to_string(t_list.bill_datum) +\
                                " | " + to_string(t_list.sysdate) +\
                                "-" + to_string(t_list.zeit, "HH:MM:SS")

            if t_list and substring(t_list.bezeich, len(t_list.bezeich) - 1) == "|":
                t_list.bezeich = substring(t_list.bezeich, 0, len(t_list.bezeich) - 1)

        for t_list in query(t_list_list, filters=(lambda t_list: t_list.fb != 0 or t_list.other != 0)):

            hoteldpt = db_session.query(Hoteldpt).filter(
                     (Hoteldpt.num == t_list.departement)).first()

            if t_list.fb != 0:
                revenue_list = Revenue_list()
                revenue_list_list.append(revenue_list)

                buffer_copy(t_list, revenue_list)
                revenue_list.betrag =  to_decimal(t_list.fb)
                revenue_list.serv_betrag =  to_decimal(t_list.fb_service)
                revenue_list.vat_betrag =  to_decimal(t_list.fb_vat)
                revenue_list.cdtrx = "FB"

            if t_list.other != 0:
                revenue_list = Revenue_list()
                revenue_list_list.append(revenue_list)

                buffer_copy(t_list, revenue_list)
                revenue_list.betrag =  to_decimal(t_list.other)
                revenue_list.serv_betrag =  to_decimal(t_list.other_service)
                revenue_list.vat_betrag =  to_decimal(t_list.other_vat)
                revenue_list.cdtrx = "OTHER"


        t_list_list.clear()
        hbill_list_list.clear()

    price_decimal = get_output(htpint(491))

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
            log_list = Log_list()
            log_list_list.append(log_list)

            log_list.log_ct = "Step 1: " + to_string(curr_date) + " " +\
                    to_string(from_time, "HH:MM:SS") + "-" +\
                    to_string(to_time, "HH:MM:SS")

        elif from_time < 0:
            from_time = from_time + 3600 * 24
            curr_date = curr_date - timedelta(days=1)


            step_1(curr_date, from_time, 24 * 3600 - 1)
            log_list = Log_list()
            log_list_list.append(log_list)

            log_list.log_ct = "Step 1: " + to_string(curr_date) + " " +\
                    to_string(from_time, "HH:MM:SS") + "-" +\
                    to_string(24 * 3600 - 1, "HH:MM:SS")

            if to_time > 0:
                curr_date = curr_date + timedelta(days=1)


                step_1(curr_date, 0, to_time)
                log_list = Log_list()
                log_list_list.append(log_list)

                log_list.log_ct = "Step 1: " + to_string(curr_date) + " " +\
                        to_string(0, "HH:MM:SS") + "-" +\
                        to_string(to_time, "HH:MM:SS")


        else:
            step_1(curr_date, from_time, to_time)
            log_list = Log_list()
            log_list_list.append(log_list)

            log_list.log_ct = "Step 1: " + to_string(curr_date) + " " +\
                    to_string(from_time, "HH:MM:SS") + "-" +\
                    to_string(to_time, "HH:MM:SS")


    else:
        step_1(curr_date, from_time, to_time)
        log_list = Log_list()
        log_list_list.append(log_list)

        log_list.log_ct = "Step 1: " + to_string(curr_date) + " " +\
                to_string(from_time, "HH:MM:SS") + "-" +\
                to_string(to_time, "HH:MM:SS")

    return generate_output()