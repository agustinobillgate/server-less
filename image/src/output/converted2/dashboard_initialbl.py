#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from functions.get_room_breakdown import get_room_breakdown
from models import Guest, Res_line, Htparam, Billjournal, Bill, Artikel, Hoteldpt, Reservation, Segment, Genstat, Zimkateg, H_bill_line, H_artikel, Zkstat, Outorder, Zimmer

def dashboard_initialbl(exclude_article:string):

    prepare_cache ([Guest, Res_line, Htparam, Billjournal, Bill, Hoteldpt, Reservation, Segment, Zimkateg, H_artikel, Zimmer])

    his_res_list = []
    his_inv_list = []
    future_res_list = []
    future_inv_list = []
    non_room_list = []
    datum:date = None
    datum2:date = None
    ci_date:date = None
    i:int = 0
    j:int = 0
    iftask:string = ""
    last_rechnr:int = 0
    curr_i:int = 0
    curr_date:date = None
    end_date:date = None
    fnet_lodg:Decimal = to_decimal("0.0")
    net_lodg:Decimal = to_decimal("0.0")
    tot_breakfast:Decimal = to_decimal("0.0")
    tot_lunch:Decimal = to_decimal("0.0")
    tot_dinner:Decimal = to_decimal("0.0")
    tot_other:Decimal = to_decimal("0.0")
    tot_rmrev:Decimal = to_decimal("0.0")
    tot_vat:Decimal = to_decimal("0.0")
    tot_service:Decimal = to_decimal("0.0")
    tot_fb:Decimal = to_decimal("0.0")
    do_it1:bool = False
    vat_proz:Decimal = 10
    do_it:bool = False
    serv_taxable:bool = False
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    serv_betrag:Decimal = to_decimal("0.0")
    outstr:string = ""
    outstr1:string = ""
    revcode:string = ""
    rechnr_nottax:int = 0
    bill_date:date = None
    pay_amount:Decimal = to_decimal("0.0")
    bill_resnr:int = 0
    bill_reslinnr:int = 0
    bill_parentnr:int = 0
    bill_gastnr:int = 0
    ex_article:string = ""
    t_reslinnr:int = 0
    lastyear:int = 0
    initdate:string = ""
    currdate:date = get_current_date()
    storage_dur:int = 0
    guest = res_line = htparam = billjournal = bill = artikel = hoteldpt = reservation = segment = genstat = zimkateg = h_bill_line = h_artikel = zkstat = outorder = zimmer = None

    his_res = his_inv = temp_res = future_res = future_inv = non_room = t_list = gbuff = bufhis_inv = buffuture_inv = bufres_line = hbill_buff = hbill_list = None

    his_res_list, His_res = create_model("His_res", {"number":int, "resnr":int, "reslinnr":int, "staydate":date, "ci_date":date, "co_date":date, "nbrofroom":int, "room_type":string, "rm_rev":Decimal, "fb_rev":Decimal, "other_rev":Decimal, "resstatus":string, "reserveid":int, "reservename":string, "bookdate":date, "rate_code":string, "nationality":string, "segmentcode":string, "cancel_date":string, "zinr":string})
    his_inv_list, His_inv = create_model("His_inv", {"datum":date, "room_type":string, "room_status":string, "qty":int, "zikatnr":int})
    temp_res_list, Temp_res = create_model_like(His_res)
    future_res_list, Future_res = create_model_like(His_res)
    future_inv_list, Future_inv = create_model_like(His_inv)
    non_room_list, Non_room = create_model("Non_room", {"postingdate":date, "departmentid":int, "departmentname":string, "rm_rev":Decimal, "fb_rev":Decimal, "other_rev":Decimal})
    t_list_list, T_list = create_model("T_list", {"departement":int, "rechnr":int, "bill_datum":date, "sysdate":date, "zeit":int, "fb":Decimal, "other":Decimal, "fb_service":Decimal, "other_service":Decimal, "pay":Decimal, "compli":Decimal})
    hbill_list_list, Hbill_list = create_model("Hbill_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":Decimal}, {"do_it": True})

    Gbuff = create_buffer("Gbuff",Guest)
    Bufhis_inv = His_inv
    bufhis_inv_list = his_inv_list

    Buffuture_inv = Future_inv
    buffuture_inv_list = future_inv_list

    Bufres_line = create_buffer("Bufres_line",Res_line)
    Hbill_buff = create_buffer("Hbill_buff",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal his_res_list, his_inv_list, future_res_list, future_inv_list, non_room_list, datum, datum2, ci_date, i, j, iftask, last_rechnr, curr_i, curr_date, end_date, fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_fb, do_it1, vat_proz, do_it, serv_taxable, serv, vat, netto, serv_betrag, outstr, outstr1, revcode, rechnr_nottax, bill_date, pay_amount, bill_resnr, bill_reslinnr, bill_parentnr, bill_gastnr, ex_article, t_reslinnr, lastyear, initdate, currdate, storage_dur, guest, res_line, htparam, billjournal, bill, artikel, hoteldpt, reservation, segment, genstat, zimkateg, h_bill_line, h_artikel, zkstat, outorder, zimmer
        nonlocal exclude_article
        nonlocal gbuff, bufhis_inv, buffuture_inv, bufres_line, hbill_buff


        nonlocal his_res, his_inv, temp_res, future_res, future_inv, non_room, t_list, gbuff, bufhis_inv, buffuture_inv, bufres_line, hbill_buff, hbill_list
        nonlocal his_res_list, his_inv_list, temp_res_list, future_res_list, future_inv_list, non_room_list, t_list_list, hbill_list_list

        return {"his-res": his_res_list, "his-inv": his_inv_list, "future-res": future_res_list, "future-inv": future_inv_list, "non-room": non_room_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    lastyear = get_year(ci_date) - 1
    initdate = "01/01/" + to_string(lastyear)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate - timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 162)]})

    if htparam:
        storage_dur = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1)]})

    if htparam.fdecimal != 0:
        vat_proz =  to_decimal(htparam.fdecimal)

    for billjournal in db_session.query(Billjournal).filter(
             (Billjournal.bill_datum >= (ci_date - timedelta(days=storage_dur))) & (Billjournal.bill_datum <= bill_date) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal._recid).all():
        do_it = True

        if last_rechnr != billjournal.rechnr:

            bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

            if not bill:
                bill_resnr = 0
                bill_reslinnr = 0
                bill_parentnr = 0
                bill_gastnr = 0


            else:
                bill_resnr = bill.resnr
                bill_reslinnr = bill.reslinnr
                bill_parentnr = bill.parent_nr
                bill_gastnr = bill.gastnr


            last_rechnr = billjournal.rechnr

        if do_it:

            artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.departement)]})
            do_it = None != artikel

            if do_it:
                do_it = (artikel.artart == 0 or artikel.artart == 8)

            if do_it:

                if exclude_article != "":
                    for j in range(1,num_entries(exclude_article, ";")  + 1) :
                        ex_article = entry(j - 1, exclude_article, ";")

                        if artikel.artnr == to_int(entry(0, ex_article, "-")) and artikel.departement == to_int(entry(1, ex_article, "-")):
                            do_it = False

        if do_it and matches(artikel.bezeich,r"*Remain*") and matches(artikel.bezeich,r"*Balance*"):
            do_it = False

        if do_it:

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, artikel.departement)]})
            revcode = "ATZ"

            if artikel.artart == 0:

                if artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6:
                    revcode = "ATM"

                if artikel.departement == 0 and artikel.umsatzart == 1:
                    revcode = "ATS"

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

                if serv == 0 or vat == 0:
                    netto =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat))

            if netto != 0:

                if (bill_reslinnr == 0 and bill_resnr > 0 and billjournal.zinr == "") or (bill_reslinnr == 0 and bill_resnr > 0 and billjournal.comment == ""):

                    his_res = query(his_res_list, filters=(lambda his_res: his_res.staydate == billjournal.bill_datum and his_res.resnr == bill_resnr and his_res.reslinnr == 0), first=True)

                    if not his_res:
                        his_res = His_res()
                        his_res_list.append(his_res)

                        his_res.staydate = billjournal.bill_datum
                        his_res.resnr = bill_resnr
                        his_res.reslinnr = 0
                        his_res.nbrofroom = 0
                        his_res.reserveid = bill_gastnr
                        his_res.resstatus = "CHECKEDOUT"

                        guest = get_cache (Guest, {"gastnr": [(eq, bill_gastnr)]})

                        if guest:

                            if guest.vorname1 != "":
                                his_res.reservename = guest.name + " " + guest.vorname1
                            else:
                                his_res.reservename = guest.name

                        res_line = db_session.query(Res_line).filter(
                                     (Res_line.resnr == bill_resnr) & ((Res_line.resstatus == 1) | (Res_line.resstatus == 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 8))).first()

                        if res_line:
                            his_res.ci_date = res_line.ankunft

                        res_line = db_session.query(Res_line).filter(
                                     (Res_line.resnr == bill_resnr) & ((Res_line.resstatus == 1) | (Res_line.resstatus == 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 8))).order_by(Res_line._recid.desc()).first()

                        if res_line:
                            his_res.co_date = res_line.abreise

                        reservation = get_cache (Reservation, {"resnr": [(eq, bill_resnr)]})

                        if reservation:

                            if reservation.resdat != None:
                                his_res.bookdate = reservation.resdat

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                            if segment:
                                his_res.segmentcode = segment.bezeich

                    if revcode.lower()  == ("ATS").lower() :
                        his_res.rm_rev =  to_decimal(his_res.rm_rev) + to_decimal(netto)

                    elif revcode.lower()  == ("ATM").lower() :
                        his_res.fb_rev =  to_decimal(his_res.fb_rev) + to_decimal(netto)

                    elif revcode.lower()  == ("ATZ").lower() :
                        his_res.other_rev =  to_decimal(his_res.other_rev) + to_decimal(netto)

                elif (bill_reslinnr != 0 and bill_resnr > 0) or (bill_reslinnr == 0 and bill_resnr > 0 and billjournal.zinr != ""):

                    if bill_reslinnr != 0:

                        his_res = query(his_res_list, filters=(lambda his_res: his_res.staydate == billjournal.bill_datum and bill_resnr == his_res.resnr and bill_reslinnr == his_res.reslinnr), first=True)
                        t_reslinnr = bill_reslinnr
                    else:

                        his_res = query(his_res_list, filters=(lambda his_res: his_res.staydate == billjournal.bill_datum and bill_resnr == his_res.resnr and to_int(entry(1, billjournal.comment, ";")) == his_res.reslinnr), first=True)
                        t_reslinnr = to_int(entry(1, billjournal.comment, ";"))

                    if not his_res:
                        his_res = His_res()
                        his_res_list.append(his_res)

                        his_res.zinr = billjournal.zinr
                        his_res.resnr = bill_resnr
                        his_res.reslinnr = t_reslinnr

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill_resnr)],"reslinnr": [(eq, t_reslinnr)]})

                        if res_line:
                            his_res.reserveid = res_line.gastnr

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                            if guest:

                                if guest.vorname1 != "":
                                    his_res.reservename = guest.name + " " + guest.vorname1
                                else:
                                    his_res.reservename = guest.name
                            his_res.ci_date = res_line.ankunft
                            his_res.co_date = res_line.abreise
                            his_res.staydate = billjournal.bill_datum

                            if billjournal.bill_datum < bill_date and billjournal.sysdate > bill_date:
                                his_res.nbrofroom = 0
                            else:
                                his_res.nbrofroom = res_line.zimmeranz

                            if his_res.staydate == his_res.co_date and his_res.ci_date != his_res.co_date:
                                his_res.nbrofroom = 0

                            if res_line.resstatus == 12:

                                bufres_line = get_cache (Res_line, {"resnr": [(eq, bill_resnr)],"reslinnr": [(eq, bill_parentnr)]})

                                if bufres_line:
                                    his_res.nbrofroom = 0

                                    genstat = get_cache (Genstat, {"resnr": [(eq, bufres_line.resnr)],"res_int[0]": [(eq, bufres_line.reslinnr)]})

                                    if genstat:

                                        if bufres_line.resstatus == 6:
                                            his_res.resstatus = "INHOUSE"

                                        elif bufres_line.resstatus == 13:
                                            his_res.resstatus = "INHOUSE(ROOM SHARER)"

                                        elif bufres_line.resstatus == 8:

                                            if genstat.resstatus == 13:
                                                his_res.resstatus = "CHECKEDOUT(ROOM SHARER)"

                                            elif genstat.resstatus == 6:
                                                his_res.resstatus = "CHECKEDOUT"

                                            elif genstat.resstatus == 8:
                                                his_res.resstatus = "CHECKEDOUT"
                            else:

                                genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)],"res_int[0]": [(eq, res_line.reslinnr)]})

                                if genstat:

                                    if res_line.resstatus == 6:
                                        his_res.resstatus = "INHOUSE"

                                    elif res_line.resstatus == 13:
                                        his_res.resstatus = "INHOUSE(ROOM SHARER)"
                                        his_res.nbrofroom = 0

                                    elif res_line.resstatus == 8:

                                        if genstat.resstatus == 13:
                                            his_res.resstatus = "CHECKEDOUT(ROOM SHARER)"
                                            his_res.nbrofroom = 0

                                        elif genstat.resstatus == 6:
                                            his_res.resstatus = "CHECKEDOUT"

                                        elif genstat.resstatus == 8:
                                            his_res.resstatus = "CHECKEDOUT"

                            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                            if zimkateg:
                                his_res.room_type = zimkateg.kurzbez

                            if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
                                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                    iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                                    if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                                        his_res.rate_code = substring(iftask, 10)

                            gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if gbuff:
                                his_res.nationality = gbuff.nation1

                        reservation = get_cache (Reservation, {"resnr": [(eq, bill_resnr)]})

                        if reservation:

                            if reservation.resdat != None:
                                his_res.bookdate = reservation.resdat

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                            if segment:
                                his_res.segmentcode = segment.bezeich

                    if revcode.lower()  == ("ATS").lower() :
                        his_res.rm_rev =  to_decimal(his_res.rm_rev) + to_decimal(netto)

                    elif revcode.lower()  == ("ATM").lower() :
                        his_res.fb_rev =  to_decimal(his_res.fb_rev) + to_decimal(netto)

                    elif revcode.lower()  == ("ATZ").lower() :
                        his_res.other_rev =  to_decimal(his_res.other_rev) + to_decimal(netto)

                elif bill_resnr == 0:

                    non_room = query(non_room_list, filters=(lambda non_room: non_room.departmentID == billjournal.departement and non_room.postingdate == billjournal.bill_datum), first=True)

                    if not non_room:
                        non_room = Non_room()
                        non_room_list.append(non_room)

                        non_room.departmentid = billjournal.departement
                        non_room.postingdate = billjournal.bill_datum

                        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})

                        if hoteldpt:
                            non_room.departmentname = hoteldpt.depart

                    if revcode.lower()  == ("ATM").lower() :
                        non_room.fb_rev =  to_decimal(non_room.fb_rev) + to_decimal(netto)

                    elif revcode.lower()  == ("ATZ").lower() :
                        non_room.other_rev =  to_decimal(non_room.other_rev) + to_decimal(netto)

                    elif revcode.lower()  == ("ATS").lower() :
                        non_room.rm_rev =  to_decimal(non_room.rm_rev) + to_decimal(netto)


    for h_bill_line in db_session.query(H_bill_line).filter(
             (H_bill_line.rechnr > 0) & (H_bill_line.bill_datum >= (ci_date - timedelta(days=storage_dur))) & (H_bill_line.bill_datum <= bill_date) & (H_bill_line.zeit >= 0) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():

        hbill_list = query(hbill_list_list, filters=(lambda hbill_list: hbill_list.dept == h_bill_line.departement and hbill_list.rechnr == h_bill_line.rechnr), first=True)

        if not hbill_list:
            hbill_list = Hbill_list()
            hbill_list_list.append(hbill_list)

            hbill_list.dept = h_bill_line.departement
            hbill_list.rechnr = h_bill_line.rechnr

            hbill_buff = db_session.query(Hbill_buff).filter(
                     (Hbill_buff.departement == h_bill_line.departement) & (Hbill_buff.rechnr == h_bill_line.rechnr) & (Hbill_buff.bill_datum > h_bill_line.bill_datum)).first()
            hbill_list.do_it = not None != hbill_buff

    for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it)):

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.artart == 0)).filter(
                 (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            hbill_list.tot_sales =  to_decimal(hbill_list.tot_sales) + to_decimal(h_bill_line.betrag)

    for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it)):

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & ((H_artikel.artart == 11) | (H_artikel.artart == 12))).filter(
                 (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            hbill_list.do_it = False

    for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it)):

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                 (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True

            t_list = query(t_list_list, filters=(lambda t_list: t_list.rechnr == h_bill_line.rechnr and t_list.departement == h_bill_line.departement and t_list.bill_datum == h_bill_line.bill_datum), first=True)

            if not t_list:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.rechnr = h_bill_line.rechnr
                t_list.departement = h_bill_line.departement
                t_list.bill_datum = h_bill_line.bill_datum
                t_list.sysdate = h_bill_line.sysdate
                t_list.zeit = h_bill_line.zeit

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

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
                    t_list.fb =  to_decimal(t_list.fb) + to_decimal(netto)
                    t_list.fb_service =  to_decimal(t_list.fb_service) + to_decimal(serv_betrag)


                else:
                    t_list.other =  to_decimal(t_list.other) + to_decimal(netto)
                    t_list.other_service =  to_decimal(t_list.other_service) + to_decimal(serv_betrag)

    for t_list in query(t_list_list):

        non_room = query(non_room_list, filters=(lambda non_room: non_room.departmentID == t_list.departement and non_room.postingdate == t_list.bill_datum), first=True)

        if not non_room:
            non_room = Non_room()
            non_room_list.append(non_room)

            non_room.departmentid = t_list.departement
            non_room.postingdate = t_list.bill_datum

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, t_list.departement)]})

            if hoteldpt:
                non_room.departmentname = hoteldpt.depart
        non_room.fb_rev =  to_decimal(non_room.fb_rev) + to_decimal(t_list.fb)
        non_room.other_rev =  to_decimal(non_room.other_rev) + to_decimal(t_list.other)

    res_line = db_session.query(Res_line).filter(
             ((Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.active_flag == 2) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft >= (ci_date - timedelta(days=storage_dur))) & (Res_line.ankunft <= bill_date)).first()
    while None != res_line:

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        temp_res = Temp_res()
        temp_res_list.append(temp_res)

        temp_res.resnr = res_line.resnr
        temp_res.reslinnr = res_line.reslinnr
        temp_res.ci_date = res_line.ankunft
        temp_res.co_date = res_line.abreise

        if res_line.betrieb_gastpay == 11:

            if res_line.resstatus == 9:
                temp_res.resstatus = "CANCELLED(ROOM SHARER)"

            elif res_line.resstatus == 10:
                temp_res.resstatus = "NO-SHOW(ROOM SHARER)"
            temp_res.nbrofroom = 0
        else:

            if res_line.resstatus == 9:
                temp_res.resstatus = "CANCELLED"

            elif res_line.resstatus == 10:
                temp_res.resstatus = "NO-SHOW"
            temp_res.nbrofroom = res_line.zimmeranz

        if res_line.cancelled != None:
            temp_res.cancel_date = to_string(get_month(res_line.cancelled) , "99") + "-" + to_string(get_day(res_line.cancelled) , "99") + "-" + to_string(get_year(res_line.cancelled) , "9999")

        if zimkateg:
            temp_res.room_type = zimkateg.kurzbez

        if guest:
            temp_res.reserveid = guest.gastnr

            if guest.vorname1 != "":
                temp_res.reservename = guest.name + " " + guest.vorname1
            else:
                temp_res.reservename = guest.name

        if gbuff:
            temp_res.nationality = gbuff.nation1

        if reservation:

            if reservation.resdat != None:
                temp_res.bookdate = reservation.resdat

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

            if segment:
                temp_res.segmentcode = segment.bezeich

        if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                    temp_res.rate_code = substring(iftask, 10)

        if res_line.ankunft != res_line.abreise:
            datum2 = res_line.abreise - timedelta(days=1)
        else:
            datum2 = res_line.abreise
        for datum in date_range(res_line.ankunft,datum2) :

            if datum >= (ci_date - timedelta(days=storage_dur)) and datum <= bill_date:
                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))
                tot_fb =  to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner)
                his_res = His_res()
                his_res_list.append(his_res)

                buffer_copy(temp_res, his_res)
                his_res.staydate = datum
                his_res.rm_rev =  to_decimal(net_lodg)
                his_res.fb_rev =  to_decimal(tot_fb)
                his_res.other_rev =  to_decimal(tot_other)


        temp_res_list.remove(temp_res)
        pass

        curr_recid = res_line._recid
        res_line = db_session.query(Res_line).filter(
                 ((Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.active_flag == 2) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft >= (ci_date - timedelta(days=storage_dur))) & (Res_line.ankunft <= bill_date) & (Res_line._recid > curr_recid)).first()

    genstat = get_cache (Genstat, {"datum": [(ge, (ci_date - storage_dur)),(le, bill_date)],"resstatus": [(ne, 0)],"res_logi[1]": [(eq, True)],"zikatnr": [(ne, 0)]})
    while None != genstat:

        if genstat.resstatus != 13 and genstat.zinr != "":

            if genstat.gratis != 0 or (genstat.zipreis == 0 and genstat.erwachs > 0):

                his_inv = query(his_inv_list, filters=(lambda his_inv: his_inv.datum == genstat.datum and his_inv.zikatnr == genstat.zikatnr and his_inv.room_status.lower()  == ("COMPLIMENT").lower()), first=True)

                if not his_inv:
                    his_inv = His_inv()
                    his_inv_list.append(his_inv)

                    his_inv.datum = genstat.datum
                    his_inv.zikatnr = genstat.zikatnr
                    his_inv.qty = 1
                    his_inv.room_status = "COMPLIMENT"


                else:
                    his_inv.qty = his_inv.qty + 1

            elif genstat.gratis == 0 and genstat.zipreis != 0 and genstat.erwachs > 0:

                his_inv = query(his_inv_list, filters=(lambda his_inv: his_inv.datum == genstat.datum and his_inv.zikatnr == genstat.zikatnr and his_inv.room_status.lower()  == ("OCCUPIED").lower()), first=True)

                if not his_inv:
                    his_inv = His_inv()
                    his_inv_list.append(his_inv)

                    his_inv.datum = genstat.datum
                    his_inv.zikatnr = genstat.zikatnr
                    his_inv.qty = 1
                    his_inv.room_status = "OCCUPIED"


                else:
                    his_inv.qty = his_inv.qty + 1

        his_res = query(his_res_list, filters=(lambda his_res: his_res.zinr == genstat.zinr and his_res.staydate == genstat.datum and his_res.resnr == genstat.resnr and his_res.reslinnr == genstat.res_int[0]), first=True)

        if not his_res:
            his_res = His_res()
            his_res_list.append(his_res)

            his_res.zinr = genstat.zinr
            his_res.resnr = genstat.resnr
            his_res.reslinnr = genstat.res_int[0]

            res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

            if res_line:
                his_res.reserveid = res_line.gastnr

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if guest:

                    if guest.vorname1 != "":
                        his_res.reservename = guest.name + " " + guest.vorname1
                    else:
                        his_res.reservename = guest.name
                his_res.ci_date = res_line.ankunft
                his_res.co_date = res_line.abreise
                his_res.staydate = genstat.datum
                his_res.nbrofroom = res_line.zimmeranz

                if res_line.resstatus == 6:
                    his_res.resstatus = "INHOUSE"

                elif res_line.resstatus == 13:
                    his_res.resstatus = "INHOUSE(ROOM SHARER)"
                    his_res.nbrofroom = 0

                elif res_line.resstatus == 8:

                    if genstat.resstatus == 13:
                        his_res.resstatus = "CHECKEDOUT(ROOM SHARER)"
                        his_res.nbrofroom = 0

                    elif genstat.resstatus == 6:
                        his_res.resstatus = "CHECKEDOUT"

                    elif genstat.resstatus == 8:
                        his_res.resstatus = "CHECKEDOUT"

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:
                    his_res.room_type = zimkateg.kurzbez

                if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                            his_res.rate_code = substring(iftask, 10)

                gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if gbuff:
                    his_res.nationality = gbuff.nation1

            reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

            if reservation:

                if reservation.resdat != None:
                    his_res.bookdate = reservation.resdat

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    his_res.segmentcode = segment.bezeich

        curr_recid = genstat._recid
        genstat = db_session.query(Genstat).filter(
                 (Genstat.datum >= (ci_date - timedelta(days=storage_dur))) & (Genstat.datum <= bill_date) & (Genstat.resstatus != 0) & (Genstat.res_logi[inc_value(1)]) & (Genstat.zikatnr != 0) & (Genstat._recid > curr_recid)).first()

    zkstat = get_cache (Zkstat, {"datum": [(ge, (ci_date - storage_dur)),(le, bill_date)],"zikatnr": [(ne, 0)]})
    while None != zkstat:

        his_inv = query(his_inv_list, filters=(lambda his_inv: his_inv.datum == zkstat.datum and his_inv.zikatnr == zkstat.zikatnr and his_inv.room_status.lower()  == ("AVAILABLE").lower()), first=True)

        if not his_inv:
            his_inv = His_inv()
            his_inv_list.append(his_inv)

            his_inv.datum = zkstat.datum
            his_inv.zikatnr = zkstat.zikatnr
            his_inv.qty = zkstat.anz100
            his_inv.room_status = "AVAILABLE"

        curr_recid = zkstat._recid
        zkstat = db_session.query(Zkstat).filter(
                 (Zkstat.datum >= (ci_date - timedelta(days=storage_dur))) & (Zkstat.datum <= bill_date) & (Zkstat.zikatnr != 0) & (Zkstat._recid > curr_recid)).first()

    outorder = get_cache (Outorder, {"gespende": [(ge, (ci_date - storage_dur))],"gespstart": [(le, bill_date)],"zinr": [(ne, "")],"betriebsnr": [(le, 1)]})
    while None != outorder:

        zimmer = get_cache (Zimmer, {"zinr": [(eq, outorder.zinr)]})

        if zimmer and zimmer.sleeping :
            for datum2 in date_range(outorder.gespstart,outorder.gespende) :

                if datum2 >= (ci_date - timedelta(days=storage_dur)) and datum2 <= bill_date:

                    his_inv = query(his_inv_list, filters=(lambda his_inv: his_inv.datum == datum2 and his_inv.room_type == zimmer.kbezeich and his_inv.room_status.lower()  == ("OUTOFORDER").lower()), first=True)

                    if not his_inv:
                        his_inv = His_inv()
                        his_inv_list.append(his_inv)

                        his_inv.datum = datum2
                        his_inv.qty = 1
                        his_inv.room_status = "OUTOFORDER"
                        his_inv.room_type = zimmer.kbezeich


                    else:
                        his_inv.qty = his_inv.qty + 1

        curr_recid = outorder._recid
        outorder = db_session.query(Outorder).filter(
                 (Outorder.gespende >= (ci_date - timedelta(days=storage_dur))) & (Outorder.gespstart <= bill_date) & (Outorder.zinr != "") & (Outorder.betriebsnr <= 1) & (Outorder._recid > curr_recid)).first()

    for his_inv in query(his_inv_list):

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, his_inv.zikatnr)]})

        if zimkateg and his_inv.room_type == "":
            his_inv.room_type = zimkateg.kurzbez

    for his_inv in query(his_inv_list, filters=(lambda his_inv: his_inv.room_status.lower()  == ("AVAILABLE").lower())):

        bufhis_inv = query(bufhis_inv_list, filters=(lambda bufhis_inv: bufhis_inv.room_status.lower()  == ("OCCUPIED").lower()  and bufhis_inv.datum == his_inv.datum and bufhis_inv.room_type == his_inv.room_type), first=True)

        if bufhis_inv:
            his_inv.qty = his_inv.qty - bufhis_inv.qty

        bufhis_inv = query(bufhis_inv_list, filters=(lambda bufhis_inv: bufhis_inv.room_status.lower()  == ("OUTOFORDER").lower()  and bufhis_inv.datum == his_inv.datum and bufhis_inv.room_type == his_inv.room_type), first=True)

        if bufhis_inv:
            his_inv.qty = his_inv.qty - bufhis_inv.qty

        bufhis_inv = query(bufhis_inv_list, filters=(lambda bufhis_inv: bufhis_inv.room_status.lower()  == ("COMPLIMENT").lower()  and bufhis_inv.datum == his_inv.datum and bufhis_inv.room_type == his_inv.room_type), first=True)

        if bufhis_inv:
            his_inv.qty = his_inv.qty - bufhis_inv.qty

    for res_line in db_session.query(Res_line).filter(
             (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft <= ci_date + timedelta(days=90)) & (Res_line.abreise >= ci_date)).order_by(Res_line._recid).all():
        do_it1 = True

        if res_line.zinr != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
            do_it1 = zimmer.sleeping

        if do_it1:

            if res_line.ankunft == res_line.abreise:
                end_date = res_line.abreise
            else:
                end_date = res_line.abreise - timedelta(days=1)
            for datum2 in date_range(res_line.ankunft,end_date) :

                if datum2 >= ci_date and datum2 <= ci_date + timedelta(days=90):

                    if res_line.gratis != 0 or (res_line.zipreis == 0 and res_line.erwachs > 0):

                        future_inv = query(future_inv_list, filters=(lambda future_inv: future_inv.datum == datum2 and future_inv.zikatnr == res_line.zikatnr and future_inv.room_status.lower()  == ("COMPLIMENT").lower()), first=True)

                        if not future_inv:
                            future_inv = Future_inv()
                            future_inv_list.append(future_inv)

                            future_inv.datum = datum2
                            future_inv.zikatnr = res_line.zikatnr
                            future_inv.qty = res_line.zimmeranz
                            future_inv.room_status = "COMPLIMENT"


                        else:
                            future_inv.qty = future_inv.qty + res_line.zimmeranz
                    else:

                        future_inv = query(future_inv_list, filters=(lambda future_inv: future_inv.datum == datum2 and future_inv.zikatnr == res_line.zikatnr and future_inv.room_status.lower()  == ("OCCUPIED").lower()), first=True)

                        if not future_inv:
                            future_inv = Future_inv()
                            future_inv_list.append(future_inv)

                            future_inv.datum = datum2
                            future_inv.zikatnr = res_line.zikatnr
                            future_inv.qty = res_line.zimmeranz
                            future_inv.room_status = "OCCUPIED"


                        else:
                            future_inv.qty = future_inv.qty + res_line.zimmeranz

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.sleeping)).order_by(Zimmer.zikatnr).all():

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

        if zimkateg.verfuegbarkeit:
            for datum in date_range(ci_date,ci_date + 90) :

                future_inv = query(future_inv_list, filters=(lambda future_inv: future_inv.zikatnr == zimkateg.zikatnr and future_inv.room_status.lower()  == ("AVAILABLE").lower()  and future_inv.datum == datum), first=True)

                if not future_inv:
                    future_inv = Future_inv()
                    future_inv_list.append(future_inv)

                    future_inv.zikatnr = zimkateg.zikatnr
                    future_inv.qty = 1
                    future_inv.datum = datum
                    future_inv.room_status = "AVAILABLE"


                else:
                    future_inv.qty = future_inv.qty + 1

    outorder = get_cache (Outorder, {"gespende": [(ge, ci_date)],"gespstart": [(le, ci_date + 90)],"zinr": [(ne, "")],"betriebsnr": [(le, 1)]})
    while None != outorder:

        zimmer = get_cache (Zimmer, {"zinr": [(eq, outorder.zinr)]})

        if zimmer and zimmer.sleeping :
            for datum2 in date_range(outorder.gespstart,outorder.gespende) :

                if datum2 >= ci_date and datum2 <= ci_date + timedelta(days=90):

                    future_inv = query(future_inv_list, filters=(lambda future_inv: future_inv.datum == datum2 and future_inv.room_type == zimmer.kbezeich and future_inv.room_status.lower()  == ("OUTOFORDER").lower()), first=True)

                    if not future_inv:
                        future_inv = Future_inv()
                        future_inv_list.append(future_inv)

                        future_inv.datum = datum2
                        future_inv.qty = 1
                        future_inv.room_status = "OUTOFORDER"
                        future_inv.room_type = zimmer.kbezeich


                    else:
                        future_inv.qty = future_inv.qty + 1

        curr_recid = outorder._recid
        outorder = db_session.query(Outorder).filter(
                 (Outorder.gespende >= ci_date) & (Outorder.gespstart <= ci_date + timedelta(days=90)) & (Outorder.zinr != "") & (Outorder.betriebsnr <= 1) & (Outorder._recid > curr_recid)).first()

    for future_inv in query(future_inv_list):

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, future_inv.zikatnr)]})

        if zimkateg and future_inv.room_type == "":
            future_inv.room_type = zimkateg.kurzbez

    for future_inv in query(future_inv_list, filters=(lambda future_inv: future_inv.room_status.lower()  == ("AVAILABLE").lower())):

        buffuture_inv = query(buffuture_inv_list, filters=(lambda buffuture_inv: buffuture_inv.room_status.lower()  == ("OCCUPIED").lower()  and buffuture_inv.datum == future_inv.datum and buffuture_inv.room_type == future_inv.room_type), first=True)

        if buffuture_inv:
            future_inv.qty = future_inv.qty - buffuture_inv.qty

        buffuture_inv = query(buffuture_inv_list, filters=(lambda buffuture_inv: buffuture_inv.room_status.lower()  == ("OUTOFORDER").lower()  and buffuture_inv.datum == future_inv.datum and buffuture_inv.room_type == future_inv.room_type), first=True)

        if buffuture_inv:
            future_inv.qty = future_inv.qty - buffuture_inv.qty

        buffuture_inv = query(buffuture_inv_list, filters=(lambda buffuture_inv: buffuture_inv.room_status.lower()  == ("COMPLIMENT").lower()  and buffuture_inv.datum == future_inv.datum and buffuture_inv.room_type == future_inv.room_type), first=True)

        if buffuture_inv:
            future_inv.qty = future_inv.qty - buffuture_inv.qty
    temp_res_list.clear()

    res_line = get_cache (Res_line, {"abreise": [(ge, ci_date)],"ankunft": [(le, ci_date + 90)],"resstatus": [(ne, 4),(ne, 8),(ne, 9),(ne, 10),(ne, 12),(ne, 99)],"active_flag": [(le, 1)],"l_zuordnung[2]": [(eq, 0)]})
    while None != res_line:

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        temp_res = Temp_res()
        temp_res_list.append(temp_res)

        temp_res.resnr = res_line.resnr
        temp_res.reslinnr = res_line.reslinnr
        temp_res.ci_date = res_line.ankunft
        temp_res.co_date = res_line.abreise

        if res_line.resstatus == 11 or res_line.resstatus == 13:
            temp_res.nbrofroom = 0
        else:
            temp_res.nbrofroom = res_line.zimmeranz

        if zimkateg:
            temp_res.room_type = zimkateg.kurzbez

        if guest:
            temp_res.reserveid = guest.gastnr

            if guest.vorname1 != "":
                temp_res.reservename = guest.name + " " + guest.vorname1
            else:
                temp_res.reservename = guest.name

        if gbuff:
            temp_res.nationality = gbuff.nation1

        if reservation:
            temp_res.bookdate = reservation.resdat

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

            if segment:
                temp_res.segmentcode = segment.bezeich

        if res_line.resstatus == 1:
            temp_res.resstatus = "GUARANTEED"

        elif res_line.resstatus == 2:
            temp_res.resstatus = "6PM"

        elif res_line.resstatus == 3:
            temp_res.resstatus = "TENTATIVE"

        elif res_line.resstatus == 5:
            temp_res.resstatus = "VERBAL CONFIRM"

        elif res_line.resstatus == 6:
            temp_res.resstatus = "INHOUSE"

        elif res_line.resstatus == 11:
            temp_res.resstatus = "ROOM SHARER"

        elif res_line.resstatus == 13:
            temp_res.resstatus = "INHOUSE(ROOM SHARER)"

        if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                    temp_res.rate_code = substring(iftask, 10)

        if res_line.ankunft != res_line.abreise:
            datum2 = res_line.abreise - timedelta(days=1)
        else:
            datum2 = res_line.abreise
        for datum in date_range(res_line.ankunft,datum2) :

            if datum >= ci_date and datum <= ci_date + timedelta(days=90):
                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))
                tot_fb =  to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner)
                future_res = Future_res()
                future_res_list.append(future_res)

                buffer_copy(temp_res, future_res)
                future_res.staydate = datum
                future_res.rm_rev =  to_decimal(net_lodg)
                future_res.fb_rev =  to_decimal(tot_fb)
                future_res.other_rev =  to_decimal(tot_other)


        temp_res_list.remove(temp_res)
        pass

        curr_recid = res_line._recid
        res_line = db_session.query(Res_line).filter(
                 (Res_line.abreise >= ci_date) & (Res_line.ankunft <= ci_date + timedelta(days=90)) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.active_flag <= 1) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line._recid > curr_recid)).first()

    return generate_output()