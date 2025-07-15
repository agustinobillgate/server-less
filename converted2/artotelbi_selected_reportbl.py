#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from functions.calc_servvat import calc_servvat
from models import Guest, Nation, Res_line, Genstat, Zimkateg, Paramtext, Htparam, Segment, Sourccod, Reslin_queasy, Waehrung, Arrangement, Queasy, Bediener, Reservation, Umsatz, Artikel, Zwkum, Hoteldpt, Budget, Akt_code, Zinrstat, Zimmer

def artotelbi_selected_reportbl(start_date:date, end_date:date, cur_file:string):

    prepare_cache ([Guest, Nation, Res_line, Zimkateg, Paramtext, Htparam, Sourccod, Waehrung, Arrangement, Queasy, Bediener, Reservation, Umsatz, Artikel, Zwkum, Hoteldpt, Budget, Akt_code, Zinrstat])

    htl_name = ""
    success_flag = False
    his_res_data = []
    future_res_data = []
    rev_list_data = []
    budget_umsatz_data = []
    b1_list_data = []
    exclude_article:string = ""
    datum:date = None
    datum2:date = None
    ci_date:date = None
    sysdate:date = None
    i:int = 0
    j:int = 0
    iftask:string = ""
    curr_i:int = 0
    curr_date:date = None
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
    tot_food:Decimal = to_decimal("0.0")
    tot_beverage:Decimal = to_decimal("0.0")
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
    bill_resnr:int = 0
    bill_reslinnr:int = 0
    bill_parentnr:int = 0
    bill_gastnr:int = 0
    ex_article:string = ""
    t_reslinnr:int = 0
    lreturn:bool = False
    hoappparam:string = ""
    vhost:string = ""
    vservice:string = ""
    htl_code:string = ""
    storage_dur:int = 0
    query_str:string = ""
    guest = nation = res_line = genstat = zimkateg = paramtext = htparam = segment = sourccod = reslin_queasy = waehrung = arrangement = queasy = bediener = reservation = umsatz = artikel = zwkum = hoteldpt = budget = akt_code = zinrstat = zimmer = None

    his_res = temp_res = future_res = rev_list = b1_list = budget_umsatz = gbuff = gbuff2 = natbuff = bufres_line = buf_genstat = buf_zimkateg = None

    his_res_data, His_res = create_model("His_res", {"resnr":int, "reslinnr":int, "staydate":date, "ci_date":date, "co_date":date, "nbrofroom":int, "room_type_name":string, "rm_rev":Decimal, "fb_rev":Decimal, "other_rev":Decimal, "resstatus":int, "reserveid":int, "reservename":string, "bookdate":date, "booktime":string, "rate_code":string, "nationality":string, "segmentcode":string, "cancel_date":date, "zinr":string, "memozinr":string, "food_rev":Decimal, "beverage_rev":Decimal, "card_type":string, "company_code":string, "source_code":string, "adult":int, "child":int, "infant":int, "compliment":int, "compliment_ch":int, "age":string, "argtnr":int, "res_logi":bool, "rtc":string, "arrangement":string, "voucher_nr":string, "rm_rate":Decimal, "fixed_rate":bool, "currency":string, "guestname":string, "bill_receiver":string, "bill_instruction":string, "purpose":string, "grpname":string, "letterno":int, "localregion":string, "cancel_reason":string, "code":string, "early_booking":string, "bona_fide":string, "tot_tax":Decimal, "tot_svc":Decimal}, {"res_logi": True})
    temp_res_data, Temp_res = create_model_like(His_res)
    future_res_data, Future_res = create_model_like(His_res)
    rev_list_data, Rev_list = create_model("Rev_list", {"dept":int, "s_dept":string, "datum":date, "s_grp":string, "subgrp":int, "s_subgrp":string, "revart":int, "s_revart":string, "amount":Decimal})
    b1_list_data, B1_list = create_model("B1_list", {"datum":date, "zinr":string, "betriebsnr":int, "bezeich":string, "zimmeranz":int, "personen":int, "argtumsatz":Decimal, "logisumsatz":Decimal})
    budget_umsatz_data, Budget_umsatz = create_model("Budget_umsatz", {"datum":date, "department":int, "s_dept":string, "umsatzart":int, "s_umsatzart":string, "zwkum":Decimal, "budget":Decimal})

    Gbuff = create_buffer("Gbuff",Guest)
    Gbuff2 = create_buffer("Gbuff2",Guest)
    Natbuff = create_buffer("Natbuff",Nation)
    Bufres_line = create_buffer("Bufres_line",Res_line)
    Buf_genstat = create_buffer("Buf_genstat",Genstat)
    Buf_zimkateg = create_buffer("Buf_zimkateg",Zimkateg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htl_name, success_flag, his_res_data, future_res_data, rev_list_data, budget_umsatz_data, b1_list_data, exclude_article, datum, datum2, ci_date, sysdate, i, j, iftask, curr_i, curr_date, fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_fb, tot_food, tot_beverage, do_it1, vat_proz, do_it, serv_taxable, serv, vat, netto, serv_betrag, outstr, outstr1, revcode, rechnr_nottax, bill_date, bill_resnr, bill_reslinnr, bill_parentnr, bill_gastnr, ex_article, t_reslinnr, lreturn, hoappparam, vhost, vservice, htl_code, storage_dur, query_str, guest, nation, res_line, genstat, zimkateg, paramtext, htparam, segment, sourccod, reslin_queasy, waehrung, arrangement, queasy, bediener, reservation, umsatz, artikel, zwkum, hoteldpt, budget, akt_code, zinrstat, zimmer
        nonlocal start_date, end_date, cur_file
        nonlocal gbuff, gbuff2, natbuff, bufres_line, buf_genstat, buf_zimkateg


        nonlocal his_res, temp_res, future_res, rev_list, b1_list, budget_umsatz, gbuff, gbuff2, natbuff, bufres_line, buf_genstat, buf_zimkateg
        nonlocal his_res_data, temp_res_data, future_res_data, rev_list_data, b1_list_data, budget_umsatz_data

        return {"htl_name": htl_name, "success_flag": success_flag, "his-res": his_res_data, "future-res": future_res_data, "rev-list": rev_list_data, "budget-umsatz": budget_umsatz_data, "b1-list": b1_list_data}


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

    if paramtext:
        htl_name = trim(paramtext.ptexte)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate - timedelta(days=1)
        ci_date = htparam.fdate

    if end_date > bill_date:
        end_date = bill_date

    if cur_file == "HISTORY":

        genstat = db_session.query(Genstat).filter(
                 ((Genstat.datum >= start_date) & (Genstat.datum <= end_date)) & (Genstat.resstatus != 0) & (Genstat.zikatnr != 0) & (Genstat.res_logic[inc_value(1)])).first()
        while None != genstat:

            his_res = query(his_res_data, filters=(lambda his_res: his_res.zinr == genstat.zinr and his_res.staydate == genstat.datum and his_res.resnr == genstat.resnr and his_res.reslinnr == genstat.res_int[0]), first=True)

            if not his_res:
                his_res = His_res()
                his_res_data.append(his_res)

                his_res.zinr = genstat.zinr
                his_res.resnr = genstat.resnr
                his_res.reslinnr = genstat.res_int[0]
                his_res.ci_date = genstat.res_date[0]
                his_res.co_date = genstat.res_date[1]
                his_res.adult = genstat.erwachs
                his_res.child = genstat.kind1
                his_res.compliment = genstat.gratis
                his_res.staydate = genstat.datum
                his_res.res_logi = genstat.res_logi[1]
                his_res.arrangement = genstat.argt
                his_res.rm_rate =  to_decimal(genstat.zipreis)
                his_res.nbrofroom = 1


                his_res.rm_rev =  to_decimal(genstat.logis)
                his_res.fb_rev =  to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])
                his_res.other_rev =  to_decimal(genstat.res_deci[4] + genstat.res_deci[5] + genstat.res_deci[0])

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:
                    his_res.segmentcode = segment.bezeich

                sourccod = get_cache (Sourccod, {"source_code": [(eq, genstat.source)]})

                if sourccod:
                    his_res.source_code = sourccod.bezeich

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})
                his_res.fixed_rate = None != reslin_queasy

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, genstat.wahrungsnr)]})

                if waehrung:
                    his_res.currency = waehrung.wabkurz

                res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                if arrangement:
                    his_res.argtnr = arrangement.argtnr

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                if zimkateg:
                    his_res.room_type_name = zimkateg.kurzbez

                buf_zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.l_zuordnung[0])]})

                if buf_zimkateg:
                    his_res.rtc = buf_zimkateg.kurzbez

                if res_line:

                    if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if matches(iftask,r"*$CODE$*"):
                                his_res.rate_code = entry(2, iftask, "$")

                    gbuff2 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

                    if gbuff2:
                        his_res.bill_receiver = replace_str(gbuff2.name + ", " + gbuff2.vorname1, chr_unicode(10) , "")
                    his_res.reserveid = res_line.gastnr
                    his_res.booktime = substring(res_line.reserve_char, 8, 5)
                    his_res.nbrofroom = res_line.zimmeranz
                    his_res.compliment_ch = res_line.l_zuordnung[3]

                    if num_entries(res_line.memozinr, ";") >= 2:
                        his_res.memozinr = entry(1, res_line.memozinr, ";")
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :

                        if matches(entry(i - 1, res_line.zimmer_wunsch, ";"),r"*ChAge*"):
                            his_res.age = substring(entry(i - 1, res_line.zimmer_wunsch, ";") , 5)

                        if matches(entry(i - 1, res_line.zimmer_wunsch, ";"),r"*SEGM_PUR*"):

                            queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, to_int(substring(entry(1, zimmer_wunsch, ";") , 8)))]})

                            if not queasy:

                                queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, to_int(substring(entry(2, zimmer_wunsch, ";") , 8)))]})

                            if queasy:
                                his_res.purpose = queasy.char3

                    if res_line.ankunft != res_line.abreise:
                        datum2 = res_line.abreise - timedelta(days=1)
                    else:
                        datum2 = res_line.abreise
                    for datum in date_range(res_line.ankunft,datum2) :

                        if datum >= start_date and datum <= end_date:
                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))
                            his_res.tot_tax =  to_decimal(tot_vat)
                            his_res.tot_svc =  to_decimal(tot_service)

                    guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

                    if guest:

                        if guest.karteityp == 0:
                            his_res.card_type = "Individual"

                        elif guest.karteityp == 1:
                            his_res.card_type = "Company"

                        elif guest.karteityp == 1:
                            his_res.card_type = "Travel Agent"
                        his_res.company_code = entry(0, guest.steuernr, "|")

                        if guest.vorname1 != "":
                            his_res.reservename = guest.name + " " + guest.vorname1
                        else:
                            his_res.reservename = guest.name

                        bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                        if bediener:
                            his_res.code = bediener.username

                    if res_line.resstatus == 6:
                        his_res.resstatus = 6

                        if not genstat.res_logic[1]:
                            his_res.nbrofroom = 0

                    elif res_line.resstatus == 13:
                        his_res.resstatus = 13
                        his_res.nbrofroom = 0
                        his_res.adult = 0
                        his_res.child = 0

                    elif res_line.resstatus == 8:

                        if not genstat.res_logic[1]:
                            his_res.nbrofroom = 0

                        elif genstat.resstatus == 13:
                            his_res.resstatus = 14
                            his_res.nbrofroom = 0
                            his_res.adult = 0
                            his_res.child = 0

                        elif genstat.resstatus == 6:
                            his_res.resstatus = 8

                        elif genstat.resstatus == 8:
                            his_res.resstatus = 8

                    nation = get_cache (Nation, {"natcode": [(eq, 0)],"nationnr": [(eq, genstat.nation)]})

                    if nation:
                        his_res.nationality = nation.bezeich

                    if genstat.gastnrmember == res_line.gastnrmember:

                        natbuff = get_cache (Nation, {"untergruppe": [(eq, 1)],"natcode": [(ne, 0)],"nationnr": [(eq, genstat.domestic)]})

                        if natbuff:
                            his_res.localregion = natbuff.bezeich


                    else:
                        his_res.localregion = ""

                reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                if reservation:
                    his_res.voucher_nr = reservation.vesrdepot
                    his_res.grpname = reservation.groupname
                    his_res.letterno = reservation.briefnr
                    his_res.cancel_reason = replace_str(reservation.vesrdepot2, chr_unicode(10) , "")

                    if reservation.resdat != None:
                        his_res.bookdate = reservation.resdat

            curr_recid = genstat._recid
            genstat = db_session.query(Genstat).filter(
                     ((Genstat.datum >= start_date) & (Genstat.datum <= end_date)) & (Genstat.resstatus != 0) & (Genstat.zikatnr != 0) & (Genstat.res_logic[inc_value(1)]) & (Genstat._recid > curr_recid)).first()
    elif cur_file == "OUTLET":

        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= start_date) & (Umsatz.datum <= end_date)).order_by(Umsatz._recid).all():
            netto =  to_decimal("0")

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel and (artikel.artart == 0 or artikel.artart == 8):
                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))

                if vat == 1:
                    netto =  to_decimal(umsatz.betrag) * to_decimal("100") / to_decimal(vat_proz)


                else:

                    if serv == 1:
                        serv_betrag =  to_decimal(netto)

                    elif vat > 0:
                        netto =  to_decimal(umsatz.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                        serv_betrag =  to_decimal(netto) * to_decimal(serv)

                    if serv == 0 or vat == 0:
                        netto =  to_decimal(umsatz.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat))

                zwkum = get_cache (Zwkum, {"departement": [(eq, artikel.departement)],"zknr": [(eq, artikel.zwkum)]})

                rev_list = query(rev_list_data, filters=(lambda rev_list: rev_list.dept == umsatz.departement and rev_list.datum == umsatz.datum and rev_list.subgrp == zwkum.zknr and rev_list.s_revart == artikel.bezeich), first=True)

                if not rev_list:
                    rev_list = Rev_list()
                    rev_list_data.append(rev_list)


                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, umsatz.departement)]})
                    rev_list.dept = umsatz.departement
                    rev_list.datum = umsatz.datum
                    rev_list.subgrp = zwkum.zknr
                    rev_list.s_subgrp = zwkum.bezeich
                    rev_list.revart = artikel.umsatzart
                    rev_list.s_revart = artikel.bezeich

                    if hoteldpt:
                        rev_list.s_dept = hoteldpt.depart

                    if artikel.umsatz == 1:
                        rev_list.s_grp = "Lodging"
                    elif artikel.umsatz == 3:
                        rev_list.s_grp = "Food"
                    elif artikel.umsatz == 4:
                        rev_list.s_grp = "Other"
                    elif artikel.umsatz == 5:
                        rev_list.s_grp = "Food"
                    elif artikel.umsatz == 6:
                        rev_list.s_grp = "Beverage"
                rev_list.amount =  to_decimal(rev_list.amount) + to_decimal(netto)
    elif artikel.umsatz == "BUDGET":

        for budget in db_session.query(Budget).filter(
                 (Budget.datum >= start_date)).order_by(Budget.datum).all():

            artikel = get_cache (Artikel, {"departement": [(eq, budget.departement)],"artnr": [(eq, budget.artnr)]})

            if artikel and artikel.umsatzart > 0:

                budget_umsatz = query(budget_umsatz_data, filters=(lambda budget_umsatz: budget_umsatz.datum == budget.datum and budget_umsatz.department == budget.departement and budget_umsatz.s_umsatzart == artikel.bezeich), first=True)

                if not budget_umsatz:
                    budget_umsatz = Budget_umsatz()
                    budget_umsatz_data.append(budget_umsatz)

                    budget_umsatz.datum = budget.datum
                    budget_umsatz.department = budget.departement
                    budget_umsatz.umsatzart = artikel.umsatzart
                    budget_umsatz.s_umsatzart = artikel.bezeich
                    budget_umsatz.zwkum =  to_decimal(artikel.zwkum)
                    budget_umsatz.budget =  to_decimal(budget.betrag)

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, budget.departement)]})

                    if hoteldpt:
                        budget_umsatz.s_dept = hoteldpt.depart
    elif artikel.umsatz == "COMPETITOR":

        zinrstat_obj_list = {}
        zinrstat = Zinrstat()
        akt_code = Akt_code()
        for zinrstat.datum, zinrstat.zinr, zinrstat.betriebsnr, zinrstat.zimmeranz, zinrstat.personen, zinrstat.argtumsatz, zinrstat.logisumsatz, zinrstat._recid, akt_code.bezeich, akt_code._recid in db_session.query(Zinrstat.datum, Zinrstat.zinr, Zinrstat.betriebsnr, Zinrstat.zimmeranz, Zinrstat.personen, Zinrstat.argtumsatz, Zinrstat.logisumsatz, Zinrstat._recid, Akt_code.bezeich, Akt_code._recid).join(Akt_code,(Akt_code.aktionscode == Zinrstat.betriebsnr) & (Akt_code.aktiongrup == 4)).filter(
                 (Zinrstat.zinr == ("Competitor").lower()) & (Zinrstat.datum >= start_date) & (Zinrstat.datum <= end_date)).order_by(Zinrstat._recid).all():
            if zinrstat_obj_list.get(zinrstat._recid):
                continue
            else:
                zinrstat_obj_list[zinrstat._recid] = True


            b1_list = B1_list()
            b1_list_data.append(b1_list)

            b1_list.datum = zinrstat.datum
            b1_list.zinr = zinrstat.zinr
            b1_list.betriebsnr = zinrstat.betriebsnr
            b1_list.bezeich = akt_code.bezeich
            b1_list.zimmeranz = zinrstat.zimmeranz
            b1_list.personen = zinrstat.personen
            b1_list.argtumsatz =  to_decimal(zinrstat.argtumsatz)
            b1_list.logisumsatz =  to_decimal(zinrstat.logisumsatz)


    elif artikel.umsatz == "FUTURE":
        temp_res_data.clear()

        for res_line in db_session.query(Res_line).filter(
                 (((Res_line.ankunft >= ci_date) | (Res_line.abreise > ci_date)) & (Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 12) & (Res_line.resstatus != 10) & (Res_line.resstatus != 4)) | ((Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.gastnr > 0)).order_by(Res_line.resnr).all():

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
            do_it = None != segment and segment.vip_level == 0

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if do_it and zimmer:

                queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, ci_date)],"date2": [(ge, ci_date)]})

                if zimmer.sleeping:

                    if queasy and queasy.number3 == res_line.gastnr:
                        do_it = False
                else:

                    if queasy and queasy.number3 != res_line.gastnr:
                        pass
                    else:
                        do_it = False

            if do_it:
                temp_res = Temp_res()
                temp_res_data.append(temp_res)

                temp_res.resnr = res_line.resnr
                temp_res.reslinnr = res_line.reslinnr
                temp_res.ci_date = res_line.ankunft
                temp_res.co_date = res_line.abreise
                temp_res.booktime = substring(res_line.reserve_char, 8, 5)
                temp_res.adult = res_line.erwachs
                temp_res.child = res_line.kind1
                temp_res.infant = res_line.kind2
                temp_res.compliment = res_line.gratis
                temp_res.compliment_ch = res_line.l_zuordnung[3]
                temp_res.resstatus = res_line.resstatus
                temp_res.zinr = res_line.zinr
                temp_res.arrangement = res_line.arrangement
                temp_res.rm_rate =  to_decimal(res_line.zipreis)

                if num_entries(res_line.memozinr, ";") >= 2:
                    temp_res.memozinr = entry(1, res_line.memozinr, ";")

                if res_line.cancelled != None:
                    temp_res.cancel_date = res_line.cancelled
                else:
                    temp_res.cancel_date = 01/01/01

                gbuff2 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

                if gbuff2:
                    temp_res.bill_receiver = replace_str(gbuff2.name + ", " + gbuff2.vorname1, chr_unicode(10) , "")

                buf_zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.l_zuordnung[0])]})

                if buf_zimkateg:
                    temp_res.rtc = buf_zimkateg.kurzbez


                for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :

                    if matches(entry(i - 1, res_line.zimmer_wunsch, ";"),r"*ChAge*"):
                        temp_res.age = substring(entry(i - 1, res_line.zimmer_wunsch, ";") , 5)

                    if matches(entry(i - 1, res_line.zimmer_wunsch, ";"),r"*SEGM_PUR*"):

                        queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, to_int(substring(entry(1, zimmer_wunsch, ";") , 8)))]})

                        if not queasy:

                            queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, to_int(substring(entry(2, zimmer_wunsch, ";") , 8)))]})

                        if queasy:
                            temp_res.purpose = queasy.char3

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
                temp_res.fixed_rate = None != reslin_queasy

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:
                    temp_res.argtnr = arrangement.argtnr

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    temp_res.currency = waehrung.wabkurz

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:
                    temp_res.room_type_name = zimkateg.kurzbez

                if res_line.resstatus == 11 or res_line.resstatus == 13 or res_line.zimmerfix or res_line.ankunft == res_line.abreise:
                    temp_res.nbrofroom = 0
                else:
                    temp_res.nbrofroom = res_line.zimmeranz

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if guest:
                    temp_res.company_code = entry(0, guest.steuernr, "|")
                    temp_res.reserveid = guest.gastnr

                    if guest.karteityp == 0:
                        temp_res.card_type = "Individual"

                    elif guest.karteityp == 1:
                        temp_res.card_type = "Company"

                    elif guest.karteityp == 1:
                        temp_res.card_type = "Travel Agent"

                    if guest.vorname1 != "":
                        temp_res.reservename = guest.name + " " + guest.vorname1
                    else:
                        temp_res.reservename = guest.name

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        temp_res.code = bediener.username

                gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if gbuff:

                    nation = get_cache (Nation, {"kurzbez": [(eq, gbuff.nation1)]})

                    if nation:
                        temp_res.nationality = nation.bezeich

                    nation = get_cache (Nation, {"kurzbez": [(eq, gbuff.nation2)]})

                    if nation:
                        temp_res.localregion = nation.bezeich

                if reservation:
                    temp_res.bookdate = reservation.resdat
                    temp_res.voucher_nr = reservation.vesrdepot
                    temp_res.grpname = reservation.groupname
                    temp_res.cancel_reason = replace_str(reservation.vesrdepot2, chr_unicode(10) , "")

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        temp_res.segmentcode = segment.bezeich

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        temp_res.source_code = sourccod.bezeich

                if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if matches(iftask,r"*$CODE$*"):
                            temp_res.rate_code = entry(2, iftask, "$")

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                for datum in date_range(res_line.ankunft,datum2) :

                    if datum >= ci_date:
                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))
                        tot_food =  to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner)
                        future_res = Future_res()
                        future_res_data.append(future_res)

                        buffer_copy(temp_res, future_res)
                        future_res.staydate = datum
                        future_res.rm_rev =  to_decimal(net_lodg)
                        future_res.food_rev =  to_decimal(tot_food)
                        future_res.beverage_rev =  to_decimal("0")
                        future_res.other_rev =  to_decimal(tot_other)
                        future_res.tot_tax =  to_decimal(tot_vat)
                        future_res.tot_svc =  to_decimal(tot_service)
                        future_res.fb_rev =  to_decimal(tot_food) + to_decimal(tot_beverage)


                temp_res_data.remove(temp_res)
                pass
    success_flag = True

    return generate_output()