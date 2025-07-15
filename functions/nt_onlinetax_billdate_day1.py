from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_bill_line, Nightaudit, Htparam, Billjournal, Artikel, Hoteldpt, H_artikel, Nitehist

def nt_onlinetax_billdate_day1():
    n:int = 1
    do_it:bool = False
    vat_artnr:List[int] = [0, 0, 0, 0, 0]
    revcode:str = ""
    serv_taxable:bool = False
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    netto:decimal = to_decimal("0.0")
    serv_betrag:decimal = to_decimal("0.0")
    outstr:str = ""
    outstr1:str = ""
    rechnr_nottax:int = 0
    htl_name:str = ""
    qtystr:str = "1"
    failed:bool = False
    lvi:int = 0
    lvcleft:str = ""
    lvctemp:str = ""
    nopd:str = ""
    logname:str = "IFDPP/DPPBRI.LOG"
    versioninfo:str = ""
    lvctmp:str = ""
    lvitmp:int = 0
    lnfeed:str = ""
    npause:int = 0
    check_duplicate:bool = False
    it_exist:bool = False
    request_sent:bool = False
    debug_mode:bool = False
    debug_code:int = 0
    bill_date:date = None
    counter:int = 0
    under_line:bool = True
    i_counter:int = 0
    progname:str = "nt-onlinetax.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 1
    service_code:int = 0
    vat_proz:decimal = 10
    service_proz:decimal = 10
    h_bill_line = nightaudit = htparam = billjournal = artikel = hoteldpt = h_artikel = nitehist = None

    s_list = fo_list = vat_list = j_list = t_list = hbill_list = hbill_buff = None

    s_list_list, S_list = create_model("S_list", {"rechnr":int, "bill_datum":str, "cdtrx":str, "amount":decimal, "bezeich":str})
    fo_list_list, Fo_list = create_model("Fo_list", {"rechnr":int, "artnr":int, "departement":int, "zeit":int, "bill_datum":date, "cdtrx":str, "amount":decimal, "bezeich":str})
    vat_list_list, Vat_list = create_model("Vat_list", {"rechnr":int, "zeit":int, "bill_datum":date, "service_amt":decimal, "departement":int})
    j_list_list, J_list = create_model("J_list", {"rechnr":int, "bill_datum":str, "cdtrx":str, "amount":decimal, "bezeich":str})
    t_list_list, T_list = create_model("T_list", {"departement":int, "rechnr":int, "bill_datum":date, "sysdate":date, "zeit":int, "fb":decimal, "other":decimal, "fb_service":decimal, "other_service":decimal, "pay":decimal, "compli":decimal})
    hbill_list_list, Hbill_list = create_model("Hbill_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":decimal}, {"do_it": True})

    Hbill_buff = create_buffer("Hbill_buff",H_bill_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, vat2, fact, netto, serv_betrag, outstr, outstr1, rechnr_nottax, htl_name, qtystr, failed, lvi, lvcleft, lvctemp, nopd, logname, versioninfo, lvctmp, lvitmp, lnfeed, npause, check_duplicate, it_exist, request_sent, debug_mode, debug_code, bill_date, counter, under_line, i_counter, progname, night_type, reihenfolge, line_nr, service_code, vat_proz, service_proz, h_bill_line, nightaudit, htparam, billjournal, artikel, hoteldpt, h_artikel, nitehist
        nonlocal hbill_buff


        nonlocal s_list, fo_list, vat_list, j_list, t_list, hbill_list, hbill_buff
        nonlocal s_list_list, fo_list_list, vat_list_list, j_list_list, t_list_list, hbill_list_list

        return {}

    def datetime2char(datum:date, zeit:int):

        nonlocal n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, vat2, fact, netto, serv_betrag, outstr, outstr1, rechnr_nottax, htl_name, qtystr, failed, lvi, lvcleft, lvctemp, nopd, logname, versioninfo, lvctmp, lvitmp, lnfeed, npause, check_duplicate, it_exist, request_sent, debug_mode, debug_code, bill_date, counter, under_line, i_counter, progname, night_type, reihenfolge, line_nr, service_code, vat_proz, service_proz, h_bill_line, nightaudit, htparam, billjournal, artikel, hoteldpt, h_artikel, nitehist
        nonlocal hbill_buff


        nonlocal s_list, fo_list, vat_list, j_list, t_list, hbill_list, hbill_buff
        nonlocal s_list_list, fo_list_list, vat_list_list, j_list_list, t_list_list, hbill_list_list

        str:str = ""
        str = to_string(get_year(datum) , "9999") +\
                to_string(get_month(datum) , "99") +\
                to_string(get_day(datum) , "99") +\
                substring(to_string(zeit, "HH:MM:SS") , 0, 2) +\
                substring(to_string(zeit, "HH:MM:SS") , 3, 2) +\
                substring(to_string(zeit, "HH:MM:SS") , 6, 2)


        return str


    def dec2char(d:decimal):

        nonlocal n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, vat2, fact, netto, serv_betrag, outstr, outstr1, rechnr_nottax, htl_name, qtystr, failed, lvi, lvcleft, lvctemp, nopd, logname, versioninfo, lvctmp, lvitmp, lnfeed, npause, check_duplicate, it_exist, request_sent, debug_mode, debug_code, bill_date, counter, under_line, i_counter, progname, night_type, reihenfolge, line_nr, service_code, vat_proz, service_proz, h_bill_line, nightaudit, htparam, billjournal, artikel, hoteldpt, h_artikel, nitehist
        nonlocal hbill_buff


        nonlocal s_list, fo_list, vat_list, j_list, t_list, hbill_list, hbill_buff
        nonlocal s_list_list, fo_list_list, vat_list_list, j_list_list, t_list_list, hbill_list_list

        str:str = ""
        d = to_decimal(round(d , 2))
        str = trim(to_string(d, "->>>>>>>>>>>9.99"))


        str = replace_str(str, ",", ".")
        return str


    def step_1():

        nonlocal n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, vat2, fact, netto, serv_betrag, outstr, outstr1, rechnr_nottax, htl_name, qtystr, failed, lvi, lvcleft, lvctemp, nopd, logname, versioninfo, lvctmp, lvitmp, lnfeed, npause, check_duplicate, it_exist, request_sent, debug_mode, debug_code, bill_date, counter, under_line, i_counter, progname, night_type, reihenfolge, line_nr, service_code, vat_proz, service_proz, h_bill_line, nightaudit, htparam, billjournal, artikel, hoteldpt, h_artikel, nitehist
        nonlocal hbill_buff


        nonlocal s_list, fo_list, vat_list, j_list, t_list, hbill_list, hbill_buff
        nonlocal s_list_list, fo_list_list, vat_list_list, j_list_list, t_list_list, hbill_list_list

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.bill_datum == bill_date) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal.rechnr, Billjournal.departement, Billjournal.artnr).all():
            do_it = True

            if do_it:

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == billjournal.artnr) & (Artikel.departement == billjournal.departement)).first()
                do_it = None != artikel and (artikel.mwst_code != 0 or artikel.service_code != 0)

                if do_it:
                    do_it = (artikel.artart == 0 or artikel.artart == 8)

            if do_it and re.match(r".*Remain.*",artikel.bezeich, re.IGNORECASE) and re.match(r".*Balance.*",artikel.bezeich, re.IGNORECASE):
                do_it = False

            if do_it:

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == artikel.departement)).first()
                revcode = "ATZ"

                if artikel.artart == 0:

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6:
                        revcode = "ATM"

                elif artikel.artart == 8:
                    revcode = "ATS"
                serv =  to_decimal("0")
                vat =  to_decimal("0")
                netto =  to_decimal("0")
                serv_betrag =  to_decimal("0")


                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))

                if vat == 1:
                    netto =  to_decimal(billjournal.betrag) * to_decimal("100") / to_decimal(vat_proz)


                else:

                    if serv == 1:
                        serv_betrag =  to_decimal(netto)

                    elif vat > 0:
                        netto =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                        serv_betrag =  to_decimal(netto) * to_decimal(serv)

                if netto != 0:

                    fo_list = query(fo_list_list, filters=(lambda fo_list: fo_list.artnr == billjournal.artnr and fo_list.departement == billjournal.departement and fo_list.rechnr == billjournal.rechnr and fo_list.bill_datum == billjournal.bill_datum), first=True)

                    if not fo_list:
                        fo_list = Fo_list()
                        fo_list_list.append(fo_list)

                        buffer_copy(billjournal, fo_list)
                        fo_list.cdtrx = revcode
                    fo_list.amount =  to_decimal(fo_list.amount) + to_decimal(netto)

                if serv_betrag != 0:

                    vat_list = query(vat_list_list, filters=(lambda vat_list: vat_list.rechnr == billjournal.rechnr and vat_list.bill_datum == billjournal.bill_datum), first=True)

                    if not vat_list:
                        vat_list = Vat_list()
                        vat_list_list.append(vat_list)

                        buffer_copy(billjournal, vat_list)
                    vat_list.service_amt =  to_decimal(vat_list.service_amt) + to_decimal(serv_betrag)

        for fo_list in query(fo_list_list, filters=(lambda fo_list: fo_list.amount != 0)):
            i_counter = i_counter + 1
            outstr = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") + to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" + chr(34) + to_string(fo_list.rechnr) + chr(34) + "|" + chr(34) + fo_list.cdtrx + chr(34) + "|" + chr(34) + datetime2char (fo_list.bill_datum, fo_list.zeit) + chr(34) + "|" + chr(34) + fo_list.bezeich + chr(34) + "|" + chr(34) + dec2char (fo_list.amount) + chr(34) + "|" + chr(34) + "1" + chr(34) + chr(2) + to_string(fo_list.departement)
            add_line(outstr)

        for vat_list in query(vat_list_list, filters=(lambda vat_list: vat_list.service_amt != 0)):
            i_counter = i_counter + 1
            outstr = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") + to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" + chr(34) + to_string(vat_list.rechnr) + chr(34) + "|" + chr(34) + "ATV" + chr(34) + "|" + chr(34) + datetime2char (vat_list.bill_datum, vat_list.zeit) + chr(34) + "|" + chr(34) + "Service Charge" + chr(34) + "|" + chr(34) + dec2char (vat_list.service_amt) + chr(34) + "|" + chr(34) + "1" + chr(34) + chr(2) + to_string(vat_list.departement)
            add_line(outstr)

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr > 0) & (H_bill_line.bill_datum == bill_date) & (H_bill_line.zeit >= 0) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():

            hbill_list = query(hbill_list_list, filters=(lambda hbill_list: hbill_list.dept == h_bill_line.departement and hbill_list.rechnr == h_bill_line.rechnr), first=True)

            if not hbill_list:
                hbill_list = Hbill_list()
                hbill_list_list.append(hbill_list)

                hbill_list.dept = h_bill_line.departement
                hbill_list.rechnr = h_bill_line.rechnr

                hbill_buff = db_session.query(Hbill_buff).filter(
                         (Hbill_buff.departement == h_bill_line.departement) & (Hbill_buff.rechnr == h_bill_line.rechnr) & (Hbill_buff.sysdate > h_bill_line.sysdate)).first()
                hbill_list.do_it = not None != hbill_buff

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

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.sysdate == bill_date)).order_by(H_bill_line._recid).all():

                if h_bill_line.artnr == 0:

                    if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                        if hbill_list.i_fact <= 0:
                            hbill_list.i_fact = hbill_list.i_fact + 1
                    else:

                        if hbill_list.i_fact >= 0:
                            hbill_list.i_fact = hbill_list.i_fact - 1
                else:

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.departement == h_bill_line.departement) & (H_artikel.artnr == h_bill_line.artnr)).first()

                    if h_artikel.artart == 2 or h_artikel.artart == 6 or h_artikel.artart == 7:

                        if not re.match(r".*(Change).*",h_bill_line.bezeich, re.IGNORECASE):

                            if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                                if hbill_list.i_fact <= 0:
                                    hbill_list.i_fact = hbill_list.i_fact + 1
                            else:

                                if hbill_list.i_fact > 0:
                                    hbill_list.i_fact = hbill_list.i_fact - 1

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it and hbill_list.i_fact != 0)):

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)

                t_list = query(t_list_list, filters=(lambda t_list: t_list.rechnr == h_bill_line.rechnr and t_list.departement == h_bill_line.departement and t_list.bill_datum == h_bill_line.bill_datum), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.rechnr = h_bill_line.rechnr
                    t_list.departement = h_bill_line.departement
                    t_list.bill_datum = h_bill_line.bill_datum
                    t_list.sysdate = h_bill_line.sysdate
                    t_list.zeit = h_bill_line.zeit

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                if artikel.artart == 9:
                    pass
                else:
                    netto =  to_decimal("0")
                    serv_betrag =  to_decimal("0")


                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, h_bill_line.bill_datum, artikel.service_code, artikel.mwst_code))

                    if vat == 1:
                        netto =  to_decimal(h_bill_line.betrag) * to_decimal("100") / to_decimal(vat_proz)
                        serv_betrag =  to_decimal("0")


                    else:

                        if serv == 1:
                            serv_betrag =  to_decimal(netto)
                            netto =  to_decimal("0")

                        elif vat > 0:
                            netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                            serv_betrag =  to_decimal(netto) * to_decimal(serv)

                    if artikel.umsatzart == 3 or artikel.umsatzart >= 5:
                        t_list.fb =  to_decimal(t_list.fb) + to_decimal((netto) * to_decimal(hbill_list.i_fact) )
                        t_list.fb_service =  to_decimal(t_list.fb_service) + to_decimal((serv_betrag) * to_decimal(hbill_list.i_fact) )


                    else:
                        t_list.other =  to_decimal(t_list.other) + to_decimal((netto) * to_decimal(hbill_list.i_fact) )
                        t_list.other_service =  to_decimal(t_list.other_service) + to_decimal((serv_betrag) * to_decimal(hbill_list.i_fact) )

        for t_list in query(t_list_list, filters=(lambda t_list: t_list.fb != 0 or t_list.other != 0)):

            hoteldpt = db_session.query(Hoteldpt).filter(
                     (Hoteldpt.num == t_list.departement)).first()

            if t_list.fb != 0:
                i_counter = i_counter + 1
                outstr = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") +\
                        to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" +\
                        chr(34) + to_string(t_list.rechnr) + chr(34) + "|" +\
                        chr(34) + "ATM" + chr(34) + "|" +\
                        chr(34) + datetime2char (t_list.bill_datum, t_list.zeit) + chr(34) + "|" +\
                        chr(34) + "Food and Beverage" + chr(34) + "|" +\
                        chr(34) + dec2char (t_list.fb) + chr(34) + "|" +\
                        chr(34) + "1" + chr(34) + chr(2) + to_string(t_list.departement)


                add_line(outstr)

            if t_list.fb_service != 0:
                i_counter = i_counter + 1
                outstr1 = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") +\
                        to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" +\
                        chr(34) + to_string(t_list.rechnr) + chr(34) + "|" +\
                        chr(34) + "ATV" + chr(34) + "|" +\
                        chr(34) + datetime2char (t_list.bill_datum, t_list.zeit) + chr(34) + "|" +\
                        chr(34) + "Service Charge Food and Beverage" + chr(34) + "|" +\
                        chr(34) + dec2char (t_list.fb_service) + chr(34) + "|" +\
                        chr(34) + "1" + chr(34) + chr(2) + to_string(t_list.departement)


                add_line(outstr1)

            if t_list.other != 0:
                i_counter = i_counter + 1
                outstr = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") +\
                        to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" +\
                        chr(34) + to_string(t_list.rechnr) + chr(34) + "|" +\
                        chr(34) + "ATZ" + chr(34) + "|" +\
                        chr(34) + datetime2char (t_list.bill_datum, t_list.zeit) + chr(34) + "|" +\
                        chr(34) + "Other Revenue" + chr(34) + "|" +\
                        chr(34) + dec2char (t_list.other) + chr(34) + "|" +\
                        chr(34) + "1" + chr(34) + chr(2) + to_string(t_list.departement)


                add_line(outstr)

            if t_list.other_service != 0:
                i_counter = i_counter + 1
                outstr1 = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") +\
                        to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" +\
                        chr(34) + to_string(t_list.rechnr) + chr(34) + "|" +\
                        chr(34) + "ATV" + chr(34) + "|" +\
                        chr(34) + datetime2char (t_list.bill_datum, t_list.zeit) + chr(34) + "|" +\
                        chr(34) + "Service Charge Other Revenue" + chr(34) + "|" +\
                        chr(34) + dec2char (t_list.other_service) + chr(34) + "|" +\
                        chr(34) + "1" + chr(34) + chr(2) + to_string(t_list.departement)


                add_line(outstr1)
        fo_list_list.clear()
        vat_list_list.clear()
        hbill_list_list.clear()
        t_list_list.clear()


    def step_2():

        nonlocal n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, vat2, fact, netto, serv_betrag, outstr, outstr1, rechnr_nottax, htl_name, qtystr, failed, lvi, lvcleft, lvctemp, nopd, logname, versioninfo, lvctmp, lvitmp, lnfeed, npause, check_duplicate, it_exist, request_sent, debug_mode, debug_code, bill_date, counter, under_line, i_counter, progname, night_type, reihenfolge, line_nr, service_code, vat_proz, service_proz, h_bill_line, nightaudit, htparam, billjournal, artikel, hoteldpt, h_artikel, nitehist
        nonlocal hbill_buff


        nonlocal s_list, fo_list, vat_list, j_list, t_list, hbill_list, hbill_buff
        nonlocal s_list_list, fo_list_list, vat_list_list, j_list_list, t_list_list, hbill_list_list

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.bill_datum == bill_date - timedelta(days=1)) & (Billjournal.sysdate == bill_date) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal.rechnr, Billjournal.departement, Billjournal.artnr).all():
            do_it = True

            if do_it:

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == billjournal.artnr) & (Artikel.departement == billjournal.departement)).first()
                do_it = None != artikel and (artikel.mwst_code != 0 or artikel.service_code != 0)

                if do_it:
                    do_it = (artikel.artart == 0 or artikel.artart == 8)

            if do_it and re.match(r".*Remain.*",artikel.bezeich, re.IGNORECASE) and re.match(r".*Balance.*",artikel.bezeich, re.IGNORECASE):
                do_it = False

            if do_it:

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == artikel.departement)).first()
                revcode = "ATZ"

                if artikel.artart == 0:

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6:
                        revcode = "ATM"

                elif artikel.artart == 8:
                    revcode = "ATS"
                serv =  to_decimal("0")
                vat =  to_decimal("0")
                netto =  to_decimal("0")
                serv_betrag =  to_decimal("0")


                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))

                if vat == 1:
                    netto =  to_decimal(billjournal.betrag) * to_decimal("100") / to_decimal(vat_proz)


                else:

                    if serv == 1:
                        serv_betrag =  to_decimal(netto)

                    elif vat > 0:
                        netto =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                        serv_betrag =  to_decimal(netto) * to_decimal(serv)

                if netto != 0:

                    fo_list = query(fo_list_list, filters=(lambda fo_list: fo_list.artnr == billjournal.artnr and fo_list.departement == billjournal.departement and fo_list.rechnr == billjournal.rechnr and fo_list.bill_datum == billjournal.bill_datum), first=True)

                    if not fo_list:
                        fo_list = Fo_list()
                        fo_list_list.append(fo_list)

                        buffer_copy(billjournal, fo_list)
                        fo_list.cdtrx = revcode
                    fo_list.amount =  to_decimal(fo_list.amount) + to_decimal(netto)

                if serv_betrag != 0:

                    vat_list = query(vat_list_list, filters=(lambda vat_list: vat_list.rechnr == billjournal.rechnr and vat_list.bill_datum == billjournal.bill_datum), first=True)

                    if not vat_list:
                        vat_list = Vat_list()
                        vat_list_list.append(vat_list)

                        buffer_copy(billjournal, vat_list)
                    vat_list.service_amt =  to_decimal(vat_list.service_amt) + to_decimal(serv_betrag)

        for fo_list in query(fo_list_list, filters=(lambda fo_list: fo_list.amount != 0)):
            i_counter = i_counter + 1
            outstr = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") + to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" + chr(34) + to_string(fo_list.rechnr) + chr(34) + "|" + chr(34) + fo_list.cdtrx + chr(34) + "|" + chr(34) + datetime2char (fo_list.bill_datum, fo_list.zeit) + chr(34) + "|" + chr(34) + fo_list.bezeich + chr(34) + "|" + chr(34) + dec2char (fo_list.amount) + chr(34) + "|" + chr(34) + "1" + chr(34) + chr(2) + to_string(fo_list.departement)
            add_line(outstr)

        for vat_list in query(vat_list_list, filters=(lambda vat_list: vat_list.service_amt != 0)):
            i_counter = i_counter + 1
            outstr = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") + to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" + chr(34) + to_string(vat_list.rechnr) + chr(34) + "|" + chr(34) + "ATV" + chr(34) + "|" + chr(34) + datetime2char (vat_list.bill_datum, vat_list.zeit) + chr(34) + "|" + chr(34) + "Service Charge" + chr(34) + "|" + chr(34) + dec2char (vat_list.service_amt) + chr(34) + "|" + chr(34) + "1" + chr(34) + chr(2) + to_string(vat_list.departement)
            add_line(outstr)

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr > 0) & (H_bill_line.bill_datum == bill_date - timedelta(days=1)) & (H_bill_line.sysdate == bill_date) & (H_bill_line.zeit >= 0) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():

            hbill_list = query(hbill_list_list, filters=(lambda hbill_list: hbill_list.dept == h_bill_line.departement and hbill_list.rechnr == h_bill_line.rechnr), first=True)

            if not hbill_list:
                hbill_list = Hbill_list()
                hbill_list_list.append(hbill_list)

                hbill_list.dept = h_bill_line.departement
                hbill_list.rechnr = h_bill_line.rechnr

                hbill_buff = db_session.query(Hbill_buff).filter(
                         (Hbill_buff.departement == h_bill_line.departement) & (Hbill_buff.rechnr == h_bill_line.rechnr) & (Hbill_buff.sysdate > h_bill_line.sysdate)).first()
                hbill_list.do_it = not None != hbill_buff

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

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.sysdate == bill_date)).order_by(H_bill_line._recid).all():

                if h_bill_line.artnr == 0:

                    if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                        if hbill_list.i_fact <= 0:
                            hbill_list.i_fact = hbill_list.i_fact + 1
                    else:

                        if hbill_list.i_fact >= 0:
                            hbill_list.i_fact = hbill_list.i_fact - 1
                else:

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.departement == h_bill_line.departement) & (H_artikel.artnr == h_bill_line.artnr)).first()

                    if h_artikel.artart == 2 or h_artikel.artart == 6 or h_artikel.artart == 7:

                        if not re.match(r".*(Change).*",h_bill_line.bezeich, re.IGNORECASE):

                            if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                                if hbill_list.i_fact <= 0:
                                    hbill_list.i_fact = hbill_list.i_fact + 1
                            else:

                                if hbill_list.i_fact >= 0:
                                    hbill_list.i_fact = hbill_list.i_fact - 1

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it and hbill_list.i_fact != 0)):

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)

                t_list = query(t_list_list, filters=(lambda t_list: t_list.rechnr == h_bill_line.rechnr and t_list.departement == h_bill_line.departement and t_list.bill_datum == h_bill_line.bill_datum), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.rechnr = h_bill_line.rechnr
                    t_list.departement = h_bill_line.departement
                    t_list.bill_datum = h_bill_line.bill_datum
                    t_list.sysdate = h_bill_line.sysdate
                    t_list.zeit = h_bill_line.zeit

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                if artikel.artart == 9:
                    pass
                else:
                    netto =  to_decimal("0")
                    serv_betrag =  to_decimal("0")


                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, h_bill_line.bill_datum, artikel.service_code, artikel.mwst_code))

                    if vat == 1:
                        netto =  to_decimal(h_bill_line.betrag) * to_decimal("100") / to_decimal(vat_proz)
                        serv_betrag =  to_decimal("0")


                    else:

                        if serv == 1:
                            serv_betrag =  to_decimal(netto)
                            netto =  to_decimal("0")

                        elif vat > 0:
                            netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                            serv_betrag =  to_decimal(netto) * to_decimal(serv)

                    if artikel.umsatzart == 3 or artikel.umsatzart >= 5:
                        t_list.fb =  to_decimal(t_list.fb) + to_decimal((netto) * to_decimal(hbill_list.i_fact) )
                        t_list.fb_service =  to_decimal(t_list.fb_service) + to_decimal((serv_betrag) * to_decimal(hbill_list.i_fact) )


                    else:
                        t_list.other =  to_decimal(t_list.other) + to_decimal((netto) * to_decimal(hbill_list.i_fact) )
                        t_list.other_service =  to_decimal(t_list.other_service) + to_decimal((serv_betrag) * to_decimal(hbill_list.i_fact) )

        for t_list in query(t_list_list, filters=(lambda t_list: t_list.fb != 0 or t_list.other != 0)):

            hoteldpt = db_session.query(Hoteldpt).filter(
                     (Hoteldpt.num == t_list.departement)).first()

            if t_list.fb != 0:
                i_counter = i_counter + 1
                outstr = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") +\
                        to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" +\
                        chr(34) + to_string(t_list.rechnr) + chr(34) + "|" +\
                        chr(34) + "ATM" + chr(34) + "|" +\
                        chr(34) + datetime2char (t_list.bill_datum, t_list.zeit) + chr(34) + "|" +\
                        chr(34) + "Food and Beverage" + chr(34) + "|" +\
                        chr(34) + dec2char (t_list.fb) + chr(34) + "|" +\
                        chr(34) + "1" + chr(34) + chr(2) + to_string(t_list.departement)


                add_line(outstr)

            if t_list.fb_service != 0:
                i_counter = i_counter + 1
                outstr1 = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") +\
                        to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" +\
                        chr(34) + to_string(t_list.rechnr) + chr(34) + "|" +\
                        chr(34) + "ATV" + chr(34) + "|" +\
                        chr(34) + datetime2char (t_list.bill_datum, t_list.zeit) + chr(34) + "|" +\
                        chr(34) + "Service Charge Food and Beverage" + chr(34) + "|" +\
                        chr(34) + dec2char (t_list.fb_service) + chr(34) + "|" +\
                        chr(34) + "1" + chr(34) + chr(2) + to_string(t_list.departement)


                add_line(outstr1)

            if t_list.other != 0:
                i_counter = i_counter + 1
                outstr = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") +\
                        to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" +\
                        chr(34) + to_string(t_list.rechnr) + chr(34) + "|" +\
                        chr(34) + "ATZ" + chr(34) + "|" +\
                        chr(34) + datetime2char (t_list.bill_datum, t_list.zeit) + chr(34) + "|" +\
                        chr(34) + "Other Revenue" + chr(34) + "|" +\
                        chr(34) + dec2char (t_list.other) + chr(34) + "|" +\
                        chr(34) + "1" + chr(34) + chr(2) + to_string(t_list.departement)


                add_line(outstr)

            if t_list.other_service != 0:
                i_counter = i_counter + 1
                outstr1 = chr(34) + to_string(get_year(bill_date) - 2000, "99") + to_string(get_month(bill_date) , "99") +\
                        to_string(get_day(bill_date) , "99") + to_string(i_counter, "999999") + chr(34) + "|" +\
                        chr(34) + to_string(t_list.rechnr) + chr(34) + "|" +\
                        chr(34) + "ATV" + chr(34) + "|" +\
                        chr(34) + datetime2char (t_list.bill_datum, t_list.zeit) + chr(34) + "|" +\
                        chr(34) + "Service Charge Other Revenue" + chr(34) + "|" +\
                        chr(34) + dec2char (t_list.other_service) + chr(34) + "|" +\
                        chr(34) + "1" + chr(34) + chr(2) + to_string(t_list.departement)


                add_line(outstr1)
        fo_list_list.clear()
        vat_list_list.clear()
        hbill_list_list.clear()
        t_list_list.clear()


    def remove_revenue(dept:int, billno:int, amount:decimal):

        nonlocal n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, vat2, fact, netto, serv_betrag, outstr, outstr1, rechnr_nottax, htl_name, qtystr, failed, lvi, lvcleft, lvctemp, nopd, logname, versioninfo, lvctmp, lvitmp, lnfeed, npause, check_duplicate, it_exist, request_sent, debug_mode, debug_code, bill_date, counter, under_line, i_counter, progname, night_type, reihenfolge, line_nr, service_code, vat_proz, service_proz, h_bill_line, nightaudit, htparam, billjournal, artikel, hoteldpt, h_artikel, nitehist
        nonlocal hbill_buff


        nonlocal s_list, fo_list, vat_list, j_list, t_list, hbill_list, hbill_buff
        nonlocal s_list_list, fo_list_list, vat_list_list, j_list_list, t_list_list, hbill_list_list

        p_sign:int = 1
        multiple_result:decimal = to_decimal("0.0")
        fb_netto:decimal = to_decimal("0.0")
        fb_service:decimal = to_decimal("0.0")
        other_netto:decimal = to_decimal("0.0")
        other_service:decimal = to_decimal("0.0")
        hbuff = None
        Hbuff =  create_buffer("Hbuff",H_artikel)

        h_bill_line_obj_list = []
        for h_bill_line, hbuff in db_session.query(H_bill_line, Hbuff).join(Hbuff,(Hbuff.artnr == H_bill_line.artnr) & (Hbuff.departement == H_bill_line.departement) & (Hbuff.artart == 0)).filter(
                 (H_bill_line.rechnr == billno) & (H_bill_line.departement == dept) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == hbuff.artnrfront) & (Artikel.departement == hbuff.departement)).first()
            serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
            netto =  to_decimal(p_sign) * to_decimal(h_bill_line.betrag) / to_decimal(fact)
            serv_betrag =  to_decimal(netto) * to_decimal(serv)

            if artikel.umsatzart == 3 or artikel.umsatzart >= 5:
                fb_netto =  to_decimal(fb_netto) + to_decimal(netto)
                fb_service =  to_decimal(fb_service) + to_decimal(serv_betrag)


            else:
                other_netto =  to_decimal(other_netto) + to_decimal(netto)
                other_service =  to_decimal(other_service) + to_decimal(serv_betrag)


        multiple_result = ( to_decimal(fb_netto) + to_decimal(other_netto)) * to_decimal(amount)

        if multiple_result < 0:
            p_sign = -1
        t_list.fb =  to_decimal(t_list.fb) + to_decimal(p_sign) * to_decimal(fb_netto)
        t_list.fb_service =  to_decimal(t_list.fb_service) + to_decimal(p_sign) * to_decimal(fb_service)
        t_list.other =  to_decimal(t_list.other) + to_decimal(p_sign) * to_decimal(fb_netto)
        t_list.other_service =  to_decimal(t_list.other_service) + to_decimal(p_sign) * to_decimal(fb_service)


    def add_line(s:str):

        nonlocal n, do_it, vat_artnr, revcode, serv_taxable, serv, vat, vat2, fact, netto, serv_betrag, outstr, outstr1, rechnr_nottax, htl_name, qtystr, failed, lvi, lvcleft, lvctemp, nopd, logname, versioninfo, lvctmp, lvitmp, lnfeed, npause, check_duplicate, it_exist, request_sent, debug_mode, debug_code, bill_date, counter, under_line, i_counter, progname, night_type, reihenfolge, line_nr, service_code, vat_proz, service_proz, h_bill_line, nightaudit, htparam, billjournal, artikel, hoteldpt, h_artikel, nitehist
        nonlocal hbill_buff


        nonlocal s_list, fo_list, vat_list, j_list, t_list, hbill_list, hbill_buff
        nonlocal s_list_list, fo_list_list, vat_list_list, j_list_list, t_list_list, hbill_list_list

        nitehist = db_session.query(Nitehist).filter(
                 (Nitehist.datum == bill_date) & (Nitehist.reihenfolge == reihenfolge) & (Nitehist.line_nr == line_nr)).first()

        if not nitehist:
            nitehist = Nitehist()
            db_session.add(nitehist)

            nitehist.datum = bill_date
            nitehist.reihenfolge = reihenfolge
            nitehist.line_nr = line_nr


        nitehist.line = s
        line_nr = line_nr + 1

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if not nightaudit:

        return generate_output()
    reihenfolge = nightaudit.reihenfolge

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 132)).first()

    if htparam.feldtyp == 1:
        vat_artnr[0] = htparam.finteger

    elif htparam.feldtyp == 5:
        for counter in range(1,num_entries(htparam.fchar, ";")  + 1) :

            if trim(entry(counter - 1, htparam.fchar, ";")) != "" and counter <= 5:
                vat_artnr[counter - 1] = to_int(trim(entry(counter - 1, htparam.fchar, ";")))

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 479)).first()
    serv_taxable = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 1)).first()

    if htparam.fdecimal != 0:
        vat_proz =  to_decimal(htparam.fdecimal)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 136)).first()
    service_code = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == service_code)).first()

    if htparam and htparam.fdecimal != 0:
        service_proz =  to_decimal(htparam.fdecimal)
    step_2()
    step_1()
    add_line("END-OF-RECORD")

    return generate_output()