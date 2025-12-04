#using conversion tools version: 1.0.0.119

# ====================================
# Rulita, 03/12/2025
# Fixing error datetime timezone
# ====================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import H_bill_line, Nightaudit, Htparam, Nitehist, H_bill, Guest, Mc_guest, H_artikel, Artikel
from datetime import datetime, timezone, timedelta

def nt_fbloyaltyprog(bill_no:int):

    prepare_cache ([H_bill_line, Nightaudit, Htparam, Nitehist, H_bill, Mc_guest, H_artikel, Artikel])

    bill_datum:date = None
    line_nr:int = 0
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    serv_betrag:Decimal = to_decimal("0.0")
    vat_proz:Decimal = 10
    do_it:bool = False
    allocated_point:int = None
    ci_date:date = None
    s_arttype:List[string] = ["Room", "Food", "Beverage", "Other", "other"]
    reihenfolge:int = 0
    outstr:string = ""
    tprice:Decimal = to_decimal("0.0")
    tservis:int = 0
    disc_food_art:int = 0
    disc_bev_art:int = 0
    disc_other_art:int = 0
    progname:string = "nt-fbloyaltyprog.p"
    h_bill_line = nightaudit = htparam = nitehist = h_bill = guest = mc_guest = h_artikel = artikel = None

    res_list = tline_list = tlist = hbill_list = hbill_buff = tline_buff = None

    res_list_data, Res_list = create_model("Res_list", {"gastnr":int, "gastpay":int, "resnr":int, "reslinnr":int, "s_reslin":int, "ankunft":date, "abreise":date, "cardnum":string})
    tline_list_data, Tline_list = create_model("Tline_list", {"datum":date, "artnr":int, "arttype":int, "rechnr":int, "reslinnr":int, "s_reslin":int, "dept":int, "bezeich":string, "price":Decimal, "email":string, "pax":int, "zeit":int, "checkin":date, "checkout":date, "rcode":string, "rtype":string, "ankzeit":int, "abrezeit":int, "resnr":int, "breslin":int, "gastnr":int, "gastpay":int})
    tlist_data, Tlist = create_model("Tlist", {"departement":int, "rechnr":int, "reslinnr":int, "s_reslin":int, "saldo":Decimal, "discount":Decimal, "created":string, "pax":int, "usr":string, "checkin":string, "checkout":string, "ankzeit":int, "abrezeit":int, "service":int, "resnr":int, "breslin":int, "gastnr":int, "gastpay":int})
    hbill_list_data, Hbill_list = create_model("Hbill_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":Decimal, "i_ledger":int, "lname":string, "vorname1":string, "pax":int, "cardnum":string}, {"do_it": True, "pax": 1})

    Hbill_buff = create_buffer("Hbill_buff",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, nightaudit, htparam, nitehist, h_bill, guest, mc_guest, h_artikel, artikel
        nonlocal bill_no
        nonlocal hbill_buff


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, tline_buff
        nonlocal res_list_data, tline_list_data, tlist_data, hbill_list_data

        return {}

    def add_line(s:string, bill_date:date):

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, nightaudit, htparam, nitehist, h_bill, guest, mc_guest, h_artikel, artikel
        nonlocal bill_no
        nonlocal hbill_buff


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, tline_buff
        nonlocal res_list_data, tline_list_data, tlist_data, hbill_list_data


        line_nr = 0

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == bill_date) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            line_nr = line_nr + 1
        nitehist = Nitehist()
        db_session.add(nitehist)

        nitehist.datum = bill_date
        nitehist.reihenfolge = reihenfolge
        nitehist.line_nr = line_nr + 1
        nitehist.line = s


    def resto_points():

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, nightaudit, htparam, nitehist, h_bill, guest, mc_guest, h_artikel, artikel
        nonlocal bill_no
        nonlocal hbill_buff


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, tline_buff
        nonlocal res_list_data, tline_list_data, tlist_data, hbill_list_data

        art_type:int = 0

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == bill_no) & (H_bill_line.bill_datum == bill_datum) & (H_bill_line.zeit >= 0) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():

            hbill_list = query(hbill_list_data, filters=(lambda hbill_list: hbill_list.dept == h_bill_line.departement and hbill_list.rechnr == h_bill_line.rechnr), first=True)

            if not hbill_list:

                h_bill = get_cache (H_bill, {"rechnr": [(eq, h_bill_line.rechnr)],"departement": [(eq, h_bill_line.departement)],"flag": [(eq, 1)]})

                if h_bill:
                    hbill_list = Hbill_list()
                    hbill_list_data.append(hbill_list)

                    hbill_list.dept = h_bill_line.departement
                    hbill_list.rechnr = h_bill_line.rechnr

                    if matches(h_bill.bilname,r"*,*"):
                        hbill_list.lname = entry(0, h_bill.bilname, ",")
                        hbill_list.vorname1 = entry(1, h_bill.bilname, ",")
                    else:
                        hbill_list.lname = h_bill.bilname

                    if h_bill.belegung > 0:
                        hbill_list.pax = h_bill.belegung

        for hbill_list in query(hbill_list_data, filters=(lambda hbill_list: hbill_list.lname != "")):

            guest = get_cache (Guest, {"name": [(eq, hbill_list.lname)],"vorname1": [(eq, hbill_list.vorname1)]})
            while None != guest :

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)],"cardnum": [(ne, "")]})

                if mc_guest:
                    hbill_list.cardnum = mc_guest.cardnum

                curr_recid = guest._recid
                guest = db_session.query(Guest).filter(
                         (Guest.name == hbill_list.lname) & (Guest.vorname1 == hbill_list.vorname1) & (Guest._recid > curr_recid)).first()

        for hbill_list in query(hbill_list_data, filters=(lambda hbill_list: hbill_list.do_it)):

            h_bill_line_obj_list = {}
            h_bill_line = H_bill_line()
            h_artikel = H_artikel()
            for h_bill_line.departement, h_bill_line.rechnr, h_bill_line.betrag, h_bill_line.artnr, h_bill_line.bezeich, h_bill_line.tischnr, h_bill_line.zeit, h_bill_line._recid, h_artikel.artart, h_artikel.artnrfront, h_artikel.departement, h_artikel._recid in db_session.query(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.betrag, H_bill_line.artnr, H_bill_line.bezeich, H_bill_line.tischnr, H_bill_line.zeit, H_bill_line._recid, H_artikel.artart, H_artikel.artnrfront, H_artikel.departement, H_artikel._recid).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True


                hbill_list.tot_sales =  to_decimal(hbill_list.tot_sales) + to_decimal(h_bill_line.betrag)

        for hbill_list in query(hbill_list_data, filters=(lambda hbill_list: hbill_list.do_it  and hbill_list.tot_sales >= 0)):

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.bill_datum == bill_datum)).order_by(H_bill_line._recid).all():

                if h_bill_line.artnr == 0:

                    if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                        if hbill_list.i_fact <= 0:
                            hbill_list.i_fact = hbill_list.i_fact + 1
                    else:

                        if hbill_list.i_fact >= 0:
                            hbill_list.i_fact = hbill_list.i_fact - 1

                elif hbill_list.tot_sales == 0:

                    if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                        if hbill_list.i_fact <= 0:
                            hbill_list.i_fact = hbill_list.i_fact + 1
                else:

                    h_artikel = get_cache (H_artikel, {"departement": [(eq, h_bill_line.departement)],"artnr": [(eq, h_bill_line.artnr)]})

                    if h_artikel.artart == 2 or h_artikel.artart == 6 or h_artikel.artart == 7:

                        if not matches(h_bill_line.bezeich,r"*(Change)*"):

                            if h_artikel.artart == 2:

                                if h_bill_line.betrag < 0:
                                    hbill_list.i_ledger = hbill_list.i_ledger + 1
                                else:
                                    hbill_list.i_ledger = hbill_list.i_ledger - 1

                            if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                                if hbill_list.i_fact <= 0:
                                    hbill_list.i_fact = hbill_list.i_fact + 1
                            else:

                                if hbill_list.i_fact >= 0:
                                    hbill_list.i_fact = hbill_list.i_fact - 1

        for hbill_list in query(hbill_list_data, filters=(lambda hbill_list: hbill_list.do_it and hbill_list.i_fact > 0)):

            h_bill_line_obj_list = {}
            h_bill_line = H_bill_line()
            h_artikel = H_artikel()
            for h_bill_line.departement, h_bill_line.rechnr, h_bill_line.betrag, h_bill_line.artnr, h_bill_line.bezeich, h_bill_line.tischnr, h_bill_line.zeit, h_bill_line._recid, h_artikel.artart, h_artikel.artnrfront, h_artikel.departement, h_artikel._recid in db_session.query(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.betrag, H_bill_line.artnr, H_bill_line.bezeich, H_bill_line.tischnr, H_bill_line.zeit, H_bill_line._recid, H_artikel.artart, H_artikel.artnrfront, H_artikel.departement, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                if artikel.artart == 9:
                    art_type = 5

                elif artikel.artart == 0:

                    if artikel.umsatzart == 1:
                        art_type = 1
                    elif artikel.umsatzart == 2:
                        art_type = 1
                    elif artikel.umsatzart == 4:
                        art_type = 4
                    elif artikel.umsatzart == 5:
                        art_type = 2
                    elif artikel.umsatzart == 6:
                        art_type = 3
                    else:
                        art_type = 4

                if h_bill_line.artnr == disc_food_art or h_bill_line.artnr == disc_bev_art or h_bill_line.artnr == disc_food_art:

                    if substring(h_bill_line.bezeich, 0, 3) == ("BEN").lower()  or substring(h_bill_line.bezeich, 0, 3) == ("VOU").lower() :

                        tline_list = query(tline_list_data, filters=(lambda tline_list: tline_list.rechnr == h_bill_line.rechnr and tline_list.artnr == disc_food_art and tline_list.dept == h_bill_line.departement and tline_list.rcode == entry(0, h_bill_line.bezeich, "-")), first=True)
                    else:

                        tline_list = query(tline_list_data, filters=(lambda tline_list: tline_list.rechnr == h_bill_line.rechnr and tline_list.artnr == disc_food_art and tline_list.dept == h_bill_line.departement), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_data.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = h_bill_line.rechnr
                        tline_list.resnr = h_bill_line.tischnr
                        tline_list.artnr = disc_food_art
                        tline_list.dept = h_bill_line.departement
                        tline_list.bezeich = "Discount"
                        tline_list.datum = bill_datum
                        tline_list.zeit = h_bill_line.zeit
                        tline_list.email = hbill_list.cardnum
                        tline_list.pax = hbill_list.pax

                        if substring(h_bill_line.bezeich, 0, 3) == ("BEN").lower()  or substring(h_bill_line.bezeich, 0, 3) == ("VOU").lower() :
                            tline_list.rcode = entry(0, h_bill_line.bezeich, "-")
                    tline_list.price =  to_decimal(tline_list.price) - to_decimal(h_bill_line.betrag)


                else:

                    tline_list = query(tline_list_data, filters=(lambda tline_list: tline_list.rechnr == h_bill_line.rechnr and tline_list.artnr == h_bill_line.artnr and tline_list.bezeich == h_bill_line.bezeich and tline_list.dept == h_bill_line.departement), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_data.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = h_bill_line.rechnr
                        tline_list.resnr = h_bill_line.tischnr
                        tline_list.artnr = h_bill_line.artnr
                        tline_list.dept = h_bill_line.departement
                        tline_list.bezeich = h_bill_line.bezeich
                        tline_list.datum = bill_datum
                        tline_list.zeit = h_bill_line.zeit
                        tline_list.email = hbill_list.cardnum
                        tline_list.pax = hbill_list.pax


                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(h_bill_line.betrag)


    def create_nitehis():

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, nightaudit, htparam, nitehist, h_bill, guest, mc_guest, h_artikel, artikel
        nonlocal bill_no
        nonlocal hbill_buff


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, tline_buff
        nonlocal res_list_data, tline_list_data, tlist_data, hbill_list_data

        date1:date = None
        time1:int = 0
        date2:date = None
        time2:string = ""
        date3:date = None
        time3:int = 0
        date4:date = None
        time4:string = ""
        nbuff = None
        Nbuff =  create_buffer("Nbuff",Nitehist)
        Tline_buff = Tline_list
        tline_buff_data = tline_list_data

        for tline_list in query(tline_list_data, filters=(lambda tline_list: tline_list.price > 0), sort_by=[("dept",False),("rechnr",False)]):
            tline_list.bezeich = replace_str(tline_list.bezeich, "|", "")
            outstr = "L" + "|" + to_string(tline_list.rechnr + tline_list.s_reslin) + "|" + to_string(tline_list.dept) + "|" + tline_list.bezeich + "|" + to_string(tline_list.price) + "|" + tline_list.rcode + "|" + tline_list.rtype + "|" + to_string(tline_list.resnr) + "|" + to_string(tline_list.reslinnr, "999") + "|" + to_string(tline_list.breslin) + "|" + to_string(tline_list.gastnr) + "|" + to_string(tline_list.gastpay)
            add_line(outstr, bill_datum)

            tlist = query(tlist_data, filters=(lambda tlist: tlist.departement == tline_list.dept and tlist.rechnr == tline_list.rechnr), first=True)

            if not tlist:
                date1 = bill_datum
                time1 = tline_list.zeit
                date3 = get_current_date()
                time3 = get_current_time_in_seconds()


                date2, time2 = convert_time(date1, time1)
                date4, time4 = convert_time(date3, time3)
                tlist = Tlist()
                tlist_data.append(tlist)

                tlist.departement = tline_list.dept
                tlist.rechnr = tline_list.rechnr
                tlist.resnr = tline_list.resnr
                tlist.reslinnr = tline_list.reslinnr
                tlist.s_reslin = tline_list.s_reslin
                tlist.breslin = tline_list.breslin
                tlist.gastnr = tline_list.gastnr
                tlist.gastpay = tline_list.gastpay
                tlist.usr = tline_list.email
                tlist.departement = tline_list.dept
                tlist.created = to_string(get_year(date4) , "9999") + "-" + to_string(get_month(date4) , "99") + "-" +\
                        to_string(get_day(date4) , "99") + "-T" + time4
                tlist.checkin = to_string(get_year(date2) , "9999") + "-" + to_string(get_month(date2) , "99") + "-" + to_string(get_day(date2) , "99") + "-T" + time2
                tlist.checkout = to_string(get_year(date2) , "9999") + "-" + to_string(get_month(date2) , "99") +\
                        "-" + to_string(get_day(date2) , "99") + "-T" + time2
                tlist.pax = tline_list.pax

            if tline_list.dept >= 1 and tline_list.bezeich.lower()  == ("Discount").lower() :
                tlist.discount =  to_decimal(tlist.discount) + to_decimal(tline_list.price)
                tlist.saldo =  to_decimal(tlist.saldo) - to_decimal(tline_list.price)


            else:
                tlist.saldo =  to_decimal(tlist.saldo) + to_decimal(tline_list.price)


                tlist.service = tlist.saldo * 0.1

        for tlist in query(tlist_data):
            outstr = "H|SEND=0|" + to_string(tlist.rechnr + tlist.s_reslin) + "|" + tlist.usr + "|" + to_string(tlist.saldo) + "|" + to_string(tlist.departement) + "|" + to_string(tlist.created) + "|" + to_string(tlist.checkin) + "|" + to_string(tlist.checkout) + "|" + to_string(tlist.pax, "999") + "|" + to_string(tlist.discount) + "|" + to_string(tlist.reslinnr, "999") + "|" + to_string(tlist.service) + "|" + to_string(tlist.resnr) + "|" + to_string(tlist.breslin) + "|" + to_string(tlist.gastnr) + "|" + to_string(tlist.gastpay)
            add_line(outstr, bill_datum)


    def convert_time(inp_date:date, inp_time:int):

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, nightaudit, htparam, nitehist, h_bill, guest, mc_guest, h_artikel, artikel
        nonlocal bill_no
        nonlocal hbill_buff


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, tline_buff
        nonlocal res_list_data, tline_list_data, tlist_data, hbill_list_data

        out_date = None
        out_time = ""
        dtstoredtime = None
        newdatetime = None
        tmp_time:string = ""
        tz:int = 0
        d:int = 0
        m:int = 0
        yy:int = 0
        hh:int = 0
        mm:int = 0
        ss:int = 0
        str_yy:int = 0

        def generate_inner_output():
            return (out_date, out_time)

        tmp_time = to_string(inp_time, "hh:mm:ss")
        str_yy = to_int(to_string(get_year(inp_date)))
        d = to_int(to_string(get_day(inp_date)))
        m = to_int(to_string(get_month(inp_date)))
        yy = to_int(to_string(get_year(inp_date)))
        hh = to_int(entry(0, to_string(tmp_time) , chr_unicode(58)))
        mm = to_int(entry(1, to_string(tmp_time) , chr_unicode(58)))
        ss = to_int(entry(2, to_string(tmp_time) , chr_unicode(58)))

        # Rulita, 03/12/2025
        # Fixing error datetime timezone
        # tz = to_int(entry(1, to_string(get_current_time_in_seconds()ZONE, 'hh:mm:ss') , chr_unicode(58)))
        # dtstoredtime = DATETIME_TZ (m, d, yy, hh, mm, ss, 0, 0)

        # newdatetime = DATETIME_TZ (dtstoredtime, - (tz * 60))
        # out_date = date_mdy(entry(0, to_string(newdatetime) , chr_unicode(32)))
        # out_time = entry(0, entry(1, to_string(newdatetime) , chr_unicode(32)) , chr_unicode(46))
        
        _local_offset = datetime.now().astimezone().utcoffset()
        tz = int((_local_offset.total_seconds() if _local_offset else 0) // 3600)

        dtstoredtime = datetime(yy, m, d, hh, mm, ss, tzinfo=timezone.utc)

        newdatetime = dtstoredtime - timedelta(minutes=tz * 60)
        out_date = date_mdy(get_month(newdatetime.date()), get_day(newdatetime.date()), get_year(newdatetime.date()))
        out_time = newdatetime.strftime('%H:%M:%S')

        return generate_inner_output()

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if not nightaudit:

        return generate_output()
    reihenfolge = nightaudit.reihenfolge

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate
    bill_datum = ci_date

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1)]})

    if htparam:

        if htparam.fdecimal != 0:
            vat_proz =  to_decimal(htparam.fdecimal)
    disc_other_art = get_output(htpint(556))
    disc_food_art = get_output(htpint(557))
    disc_bev_art = get_output(htpint(596))
    resto_points()
    create_nitehis()

    return generate_output()