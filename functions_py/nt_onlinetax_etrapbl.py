#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 26/11/2025, Update with_for_update
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import H_bill_line, Queasy, Htparam, Paramtext, Billjournal, Artikel, Hoteldpt, H_artikel

def nt_onlinetax_etrapbl(fdate:date, tdate:date):

    prepare_cache ([Queasy, Htparam, Paramtext, Billjournal, H_artikel])

    hotel_name = ""
    hotel_id = ""
    tlist_data = []
    bill_date:date = None
    do_it:bool = False
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    serv_betrag:Decimal = to_decimal("0.0")
    vat_betrag:Decimal = to_decimal("0.0")
    serv_taxable:bool = False
    service_code:int = 0
    vat_proz:Decimal = 10
    service_proz:Decimal = 10
    count_int:int = 0
    datum:date = None
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    h_bill_line = queasy = htparam = paramtext = billjournal = artikel = hoteldpt = h_artikel = None

    tlist = hbill_list = hbill_buff = bline = bqueasy = tqueasy = None

    tlist_data, Tlist = create_model("Tlist", {"invno":string, "datum_trx":string, "subtotal":Decimal, "diskon":Decimal, "service":Decimal, "other":Decimal, "pajak":Decimal, "amount":Decimal, "depart":int})
    hbill_list_data, Hbill_list = create_model("Hbill_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":Decimal}, {"do_it": True})

    Hbill_buff = create_buffer("Hbill_buff",H_bill_line)
    Bline = create_buffer("Bline",H_bill_line)
    Bqueasy = create_buffer("Bqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hotel_name, hotel_id, tlist_data, bill_date, do_it, serv, vat, netto, serv_betrag, vat_betrag, serv_taxable, service_code, vat_proz, service_proz, count_int, datum, disc_art1, disc_art2, disc_art3, h_bill_line, queasy, htparam, paramtext, billjournal, artikel, hoteldpt, h_artikel
        nonlocal fdate, tdate
        nonlocal hbill_buff, bline, bqueasy, tqueasy


        nonlocal tlist, hbill_list, hbill_buff, bline, bqueasy, tqueasy
        nonlocal tlist_data, hbill_list_data

        return {"hotel_name": hotel_name, "hotel_id": hotel_id, "tlist": tlist_data}

    def datetime2char(datum:date, zeit:int):

        nonlocal hotel_name, hotel_id, tlist_data, bill_date, do_it, serv, vat, netto, serv_betrag, vat_betrag, serv_taxable, service_code, vat_proz, service_proz, count_int, disc_art1, disc_art2, disc_art3, h_bill_line, queasy, htparam, paramtext, billjournal, artikel, hoteldpt, h_artikel
        nonlocal fdate, tdate
        nonlocal hbill_buff, bline, bqueasy, tqueasy


        nonlocal tlist, hbill_list, hbill_buff, bline, bqueasy, tqueasy
        nonlocal tlist_data, hbill_list_data

        str:string = ""
        str = to_string(get_year(datum) , "9999") + "-" +\
                to_string(get_month(datum) , "99") + "-" +\
                to_string(get_day(datum) , "99") + " " +\
                substring(to_string(zeit, "HH:MM:SS") , 0, 2) + ":" +\
                substring(to_string(zeit, "HH:MM:SS") , 3, 2) + ":" +\
                substring(to_string(zeit, "HH:MM:SS") , 6, 2)


        return str


    def step_1(bill_date:date):

        nonlocal hotel_name, hotel_id, tlist_data, do_it, serv, vat, netto, serv_betrag, vat_betrag, serv_taxable, service_code, vat_proz, service_proz, count_int, datum, disc_art1, disc_art2, disc_art3, h_bill_line, queasy, htparam, paramtext, billjournal, artikel, hoteldpt, h_artikel
        nonlocal fdate, tdate
        nonlocal hbill_buff, bline, bqueasy, tqueasy


        nonlocal tlist, hbill_list, hbill_buff, bline, bqueasy, tqueasy
        nonlocal tlist_data, hbill_list_data

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.bill_datum == bill_date) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal.rechnr, Billjournal.departement, Billjournal.artnr).all():
            do_it = True

            if do_it:

                artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.departement)]})
                do_it = None != artikel and (artikel.mwst_code != 0 or artikel.service_code != 0)

                if do_it:
                    do_it = (artikel.artart == 0 or artikel.artart == 8)

            if do_it and matches(artikel.bezeich,r"*Remain*") and matches(artikel.bezeich,r"*Balance*"):
                do_it = False

            if do_it:

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, artikel.departement)]})
                serv =  to_decimal("0")
                vat =  to_decimal("0")
                netto =  to_decimal("0")
                serv_betrag =  to_decimal("0")
                vat_betrag =  to_decimal("0")


                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))

                if vat == 1:
                    netto =  to_decimal(billjournal.betrag) * to_decimal("100") / to_decimal(vat_proz)


                else:

                    if serv == 1:
                        serv_betrag =  to_decimal(netto)

                    elif vat > 0:
                        netto =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                        serv_betrag =  to_decimal(netto) * to_decimal(serv)
                        vat_betrag =  to_decimal(netto) * to_decimal(vat)

                if netto != 0:

                    tlist = query(tlist_data, filters=(lambda tlist: tlist.invno == to_string(billjournal.rechnr) and tlist.depart == billjournal.departement), first=True)

                    if not tlist:
                        tlist = Tlist()
                        tlist_data.append(tlist)

                        tlist.invno = to_string(billjournal.rechnr)
                        tlist.depart = billjournal.departement


                    tlist.subtotal =  to_decimal(tlist.subtotal) + to_decimal(netto)
                    tlist.service =  to_decimal(tlist.service) + to_decimal(serv_betrag)
                    tlist.pajak =  to_decimal(tlist.pajak) + to_decimal(vat_betrag)
                    tlist.datum_trx = datetime2char (billjournal.bill_datum, billjournal.zeit)
                    tlist.amount =  to_decimal(tlist.amount) + to_decimal(billjournal.betrag)

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr > 0) & (H_bill_line.bill_datum == bill_date) & (H_bill_line.zeit >= 0) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():

            hbill_list = query(hbill_list_data, filters=(lambda hbill_list: hbill_list.dept == h_bill_line.departement and hbill_list.rechnr == h_bill_line.rechnr), first=True)

            if not hbill_list:
                hbill_list = Hbill_list()
                hbill_list_data.append(hbill_list)

                hbill_list.dept = h_bill_line.departement
                hbill_list.rechnr = h_bill_line.rechnr

                hbill_buff = db_session.query(Hbill_buff).filter(
                         (Hbill_buff.departement == h_bill_line.departement) & (Hbill_buff.rechnr == h_bill_line.rechnr) & (Hbill_buff.bill_datum > h_bill_line.bill_datum)).first()
                hbill_list.do_it = not None != hbill_buff

        for hbill_list in query(hbill_list_data, filters=(lambda hbill_list: hbill_list.do_it)):

            h_bill_line_obj_list = {}
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True


                hbill_list.tot_sales =  to_decimal(hbill_list.tot_sales) + to_decimal(h_bill_line.betrag)

        for hbill_list in query(hbill_list_data, filters=(lambda hbill_list: hbill_list.do_it  and hbill_list.tot_sales != 0)):

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.bill_datum == bill_date)).order_by(H_bill_line.zeit.desc()).all():

                if h_bill_line.artnr == 0:

                    if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                        if hbill_list.i_fact <= 0:
                            hbill_list.i_fact = hbill_list.i_fact + 1
                    else:

                        if hbill_list.i_fact >= 0:
                            hbill_list.i_fact = hbill_list.i_fact - 1
                else:

                    h_artikel = get_cache (H_artikel, {"departement": [(eq, h_bill_line.departement)],"artnr": [(eq, h_bill_line.artnr)]})

                    if h_artikel.artart == 2 or h_artikel.artart == 6 or h_artikel.artart == 7:

                        if not matches(h_bill_line.bezeich,r"*(Change)*"):

                            if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                                if hbill_list.i_fact <= 0:
                                    hbill_list.i_fact = hbill_list.i_fact + 1
                            else:

                                if hbill_list.i_fact > 0:
                                    hbill_list.i_fact = hbill_list.i_fact - 1

        for hbill_list in query(hbill_list_data, filters=(lambda hbill_list: hbill_list.do_it and hbill_list.i_fact != 0)):

            h_bill_line_obj_list = {}
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True

                if h_artikel.artart == 0 or h_artikel.artart == 8:
                    serv =  to_decimal("0")
                    vat =  to_decimal("0")
                    netto =  to_decimal("0")
                    serv_betrag =  to_decimal("0")
                    vat_betrag =  to_decimal("0")

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                    if artikel:
                        serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, h_bill_line.bill_datum, artikel.service_code, artikel.mwst_code))

                        if vat == 1:
                            netto =  to_decimal(h_bill_line.betrag) * to_decimal("100") / to_decimal(vat_proz)


                        else:

                            if serv == 1:
                                serv_betrag =  to_decimal(netto)

                            elif vat > 0:
                                netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                                serv_betrag =  to_decimal(netto) * to_decimal(serv)
                                vat_betrag =  to_decimal(netto) * to_decimal(vat)

                        if netto != 0:

                            tlist = query(tlist_data, filters=(lambda tlist: tlist.invno == to_string(h_bill_line.rechnr) and tlist.depart == h_bill_line.departement), first=True)

                            if not tlist:
                                tlist = Tlist()
                                tlist_data.append(tlist)

                                tlist.invno = to_string(h_bill_line.rechnr)
                                tlist.depart = h_bill_line.departement


                            tlist.subtotal =  to_decimal(tlist.subtotal) + to_decimal(netto)
                            tlist.service =  to_decimal(tlist.service) + to_decimal(serv_betrag)
                            tlist.pajak =  to_decimal(tlist.pajak) + to_decimal(vat_betrag)
                            tlist.datum_trx = datetime2char (h_bill_line.bill_datum, h_bill_line.zeit)
                            tlist.amount =  to_decimal(tlist.amount) + to_decimal(h_bill_line.betrag)


    def decode_string(in_str:string):

        nonlocal hotel_name, hotel_id, tlist_data, bill_date, do_it, serv, vat, netto, serv_betrag, vat_betrag, serv_taxable, service_code, vat_proz, service_proz, count_int, datum, disc_art1, disc_art2, disc_art3, h_bill_line, queasy, htparam, paramtext, billjournal, artikel, hoteldpt, h_artikel
        nonlocal fdate, tdate
        nonlocal hbill_buff, bline, bqueasy, tqueasy


        nonlocal tlist, hbill_list, hbill_buff, bline, bqueasy, tqueasy
        nonlocal tlist_data, hbill_list_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    serv_taxable = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1)]})

    if htparam.fdecimal != 0:
        vat_proz =  to_decimal(htparam.fdecimal)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 136)]})
    service_code = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, service_code)]})

    if htparam and htparam.fdecimal != 0:
        service_proz =  to_decimal(htparam.fdecimal)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

    if htparam:
        disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam:
        disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    if htparam:
        disc_art3 = htparam.finteger

    queasy = get_cache (Queasy, {"key": [(eq, 291)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 291
        queasy.date1 = fdate
        queasy.date2 = get_current_date()


    else:

        if (queasy.date1 + 1) > fdate:
            pass
        else:
            fdate = queasy.date1 + timedelta(days=1)

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

    if paramtext:
        hotel_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        hotel_id = decode_string(paramtext.ptexte)
    for datum in date_range(fdate,tdate) :
        step_1(datum)

        bqueasy = get_cache (Queasy, {"key": [(eq, 291)]})

        if bqueasy:

            if datum >= (bqueasy.date1 + 1):

                # tqueasy = get_cache (Queasy, {"key": [(eq, 291)]})
                tqueasy = db_session.query(Queasy).filter(
                         (Queasy.key == 291)).with_for_update().first()

                if tqueasy:
                    pass
                    tqueasy.date1 = datum
                    tqueasy.date2 = get_current_date()


                    pass
                    pass

    return generate_output()