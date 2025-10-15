#using conversion tools version: 1.0.0.117

# ===========================================
# Rulita, 15-10-2025
# Tiket ID : D776D3 | New Compile program IF 
# ===========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.get_room_breakdown_bi import get_room_breakdown_bi
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.calc_servvat import calc_servvat
from models import Guest, Nation, Res_line, Genstat, Zimkateg, Htparam, Reservation, Waehrung, Reslin_queasy, Queasy, Arrangement, Artikel, Segment, Zimmer, Sourccod, Brief, Umsatz, Zwkum, Hoteldpt, Akt_code, Zinrstat, Budget, Zkstat, Outorder

def bi_avalon_dailybl():

    prepare_cache ([Guest, Nation, Zimkateg, Htparam, Reservation, Waehrung, Queasy, Arrangement, Artikel, Zimmer, Sourccod, Brief, Umsatz, Zwkum, Hoteldpt, Akt_code, Budget])

    success_flag = False
    his_res_data = []
    his_inv_data = []
    future_res_data = []
    future_inv_data = []
    t_zimmer_data = []
    t_zimkateg_data = []
    t_arrangement_data = []
    t_ratecode_data = []
    t_bill_instruction_data = []
    t_segment_data = []
    t_segmentgrp_data = []
    t_sourccod_data = []
    t_brief_data = []
    t_nation_data = []
    t_region_data = []
    t_cancelreason_data = []
    t_cardtype_data = []
    rev_list_data = []
    b1_list_data = []
    budget_umsatz_data = []
    exclude_article:string = ""
    datum:date = None
    datum2:date = None
    ci_date:date = None
    sysdate:date = None
    i:int = 0
    j:int = 0
    iftask:string = ""
    last_rechnr:int = 0
    ivalue:string = ""
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
    serv1:Decimal = to_decimal("0.0")
    serv2:Decimal = to_decimal("0.0")
    vat1:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    vat3:Decimal = to_decimal("0.0")
    vat4:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    fact1:Decimal = to_decimal("0.0")
    fact2:Decimal = to_decimal("0.0")
    query_str:string = ""
    guest = nation = res_line = genstat = zimkateg = htparam = reservation = waehrung = reslin_queasy = queasy = arrangement = artikel = segment = zimmer = sourccod = brief = umsatz = zwkum = hoteldpt = akt_code = zinrstat = budget = zkstat = outorder = None

    his_res = his_inv = t_bediener = temp_res = future_res = future_inv = t_salesbud = t_segment = t_segmentgrp = t_sourccod = t_zimmer = t_zimkateg = t_arrangement = t_ratecode = t_brief = t_nation = t_region = t_bill_instruction = t_cancelreason = t_cardtype = rev_list = b1_list = budget_umsatz = deposit_list = gbuff = gbuff2 = natbuff = bufres_line = buf_genstat = buf_zimkateg = None

    his_res_data, His_res = create_model("His_res", {"resnr":int, "reslinnr":int, "staydate":date, "ci_date":date, "co_date":date, "nbrofroom":int, "room_type_name":string, "rm_rev":Decimal, "fb_rev":Decimal, "other_rev":Decimal, "resstatus":int, "reserveid":int, "reservename":string, "bookdate":date, "booktime":string, "rate_code":string, "nationality":string, "segmentcode":int, "cancel_date":date, "zinr":string, "memozinr":string, "food_rev":Decimal, "beverage_rev":Decimal, "card_type":int, "company_code":string, "source_code":int, "adult":int, "child":int, "infant":int, "compliment":int, "compliment_ch":int, "age":string, "argtnr":int, "res_logi":bool, "rtc":string, "arrangement":string, "voucher_nr":string, "rm_rate":Decimal, "fixed_rate":bool, "currency":string, "guestname":string, "bill_receiver":string, "bill_instruction":string, "purpose":string, "grpname":string, "letterno":int, "localregion":string, "cancel_reason":string, "code":string, "early_booking":string, "bona_fide":string, "tot_tax":Decimal, "tot_svc":Decimal}, {"res_logi": True})
    his_inv_data, His_inv = create_model("His_inv", {"datum":date, "tot_room":int, "inactive_room":int, "active_room":int, "ooo_room":int, "oos_room":int})
    t_bediener_data, T_bediener = create_model("T_bediener", {"userinit":string, "username":string})
    temp_res_data, Temp_res = create_model_like(His_res)
    future_res_data, Future_res = create_model_like(His_res)
    future_inv_data, Future_inv = create_model_like(His_inv)
    t_salesbud_data, T_salesbud = create_model("T_salesbud", {"jahr":int, "monat":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "room_nights":int, "id":string})
    t_segment_data, T_segment = create_model("T_segment", {"segmentcode":int, "segmentgrup":int, "bezeich":string, "bemerkung":string})
    t_segmentgrp_data, T_segmentgrp = create_model("T_segmentgrp", {"segmentgrup":int, "bezeich":string})
    t_sourccod_data, T_sourccod = create_model("T_sourccod", {"source_code":int, "bezeich":string})
    t_zimmer_data, T_zimmer = create_model("T_zimmer", {"roomno":string, "room_type":string})
    t_zimkateg_data, T_zimkateg = create_model("T_zimkateg", {"bezeich":string, "kurzbez":string})
    t_arrangement_data, T_arrangement = create_model("T_arrangement", {"arrangement":string, "argt_bez":string})
    t_ratecode_data, T_ratecode = create_model("T_ratecode", {"code":string, "bezeich":string})
    t_brief_data, T_brief = create_model("T_brief", {"briefnr":int, "bezeich":string})
    t_nation_data, T_nation = create_model("T_nation", {"kurzbez":string, "bezeich":string})
    t_region_data, T_region = create_model("T_region", {"kurzbez":string, "bezeich":string})
    t_bill_instruction_data, T_bill_instruction = create_model("T_bill_instruction", {"number1":int, "char1":string})
    t_cancelreason_data, T_cancelreason = create_model("T_cancelreason", {"number1":int, "char3":string})
    t_cardtype_data, T_cardtype = create_model("T_cardtype", {"number":int, "bezeich":string})
    rev_list_data, Rev_list = create_model("Rev_list", {"dept":int, "s_dept":string, "datum":date, "s_grp":string, "subgrp":int, "s_subgrp":string, "revart":int, "s_revart":string, "amount":Decimal})
    b1_list_data, B1_list = create_model("B1_list", {"datum":date, "zinr":string, "betriebsnr":int, "bezeich":string, "zimmeranz":int, "personen":int, "argtumsatz":Decimal, "logisumsatz":Decimal})
    budget_umsatz_data, Budget_umsatz = create_model("Budget_umsatz", {"datum":date, "department":int, "s_dept":string, "umsatzart":int, "s_umsatzart":string, "zwkum":Decimal, "budget":Decimal})
    deposit_list_data, Deposit_list = create_model("Deposit_list", {"grpflag":bool, "resnr":int, "reser_name":string, "groupname":string, "resli_name":string, "ankunft":date, "limitdate":date, "depositgef":Decimal, "depositbez":Decimal, "depositbez2":Decimal, "zahldatum":date, "zahlkonto":int, "zahldatum2":date, "zahlkonto2":int})

    Gbuff = create_buffer("Gbuff",Guest)
    Gbuff2 = create_buffer("Gbuff2",Guest)
    Natbuff = create_buffer("Natbuff",Nation)
    Bufres_line = create_buffer("Bufres_line",Res_line)
    Buf_genstat = create_buffer("Buf_genstat",Genstat)
    Buf_zimkateg = create_buffer("Buf_zimkateg",Zimkateg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, his_res_data, his_inv_data, future_res_data, future_inv_data, t_zimmer_data, t_zimkateg_data, t_arrangement_data, t_ratecode_data, t_bill_instruction_data, t_segment_data, t_segmentgrp_data, t_sourccod_data, t_brief_data, t_nation_data, t_region_data, t_cancelreason_data, t_cardtype_data, rev_list_data, b1_list_data, budget_umsatz_data, exclude_article, datum, datum2, ci_date, sysdate, i, j, iftask, last_rechnr, ivalue, curr_i, curr_date, end_date, fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_fb, tot_food, tot_beverage, do_it1, vat_proz, do_it, serv_taxable, serv, vat, netto, serv_betrag, outstr, outstr1, revcode, rechnr_nottax, bill_date, bill_resnr, bill_reslinnr, bill_parentnr, bill_gastnr, ex_article, t_reslinnr, lreturn, hoappparam, vhost, vservice, htl_code, serv1, serv2, vat1, vat2, vat3, vat4, fact, fact1, fact2, query_str, guest, nation, res_line, genstat, zimkateg, htparam, reservation, waehrung, reslin_queasy, queasy, arrangement, artikel, segment, zimmer, sourccod, brief, umsatz, zwkum, hoteldpt, akt_code, zinrstat, budget, zkstat, outorder
        nonlocal gbuff, gbuff2, natbuff, bufres_line, buf_genstat, buf_zimkateg


        nonlocal his_res, his_inv, t_bediener, temp_res, future_res, future_inv, t_salesbud, t_segment, t_segmentgrp, t_sourccod, t_zimmer, t_zimkateg, t_arrangement, t_ratecode, t_brief, t_nation, t_region, t_bill_instruction, t_cancelreason, t_cardtype, rev_list, b1_list, budget_umsatz, deposit_list, gbuff, gbuff2, natbuff, bufres_line, buf_genstat, buf_zimkateg
        nonlocal his_res_data, his_inv_data, t_bediener_data, temp_res_data, future_res_data, future_inv_data, t_salesbud_data, t_segment_data, t_segmentgrp_data, t_sourccod_data, t_zimmer_data, t_zimkateg_data, t_arrangement_data, t_ratecode_data, t_brief_data, t_nation_data, t_region_data, t_bill_instruction_data, t_cancelreason_data, t_cardtype_data, rev_list_data, b1_list_data, budget_umsatz_data, deposit_list_data

        return {"success_flag": success_flag, "his-res": his_res_data, "his-inv": his_inv_data, "future-res": future_res_data, "future-inv": future_inv_data, "t-zimmer": t_zimmer_data, "t-zimkateg": t_zimkateg_data, "t-arrangement": t_arrangement_data, "t-ratecode": t_ratecode_data, "t-bill-instruction": t_bill_instruction_data, "t-segment": t_segment_data, "t-segmentgrp": t_segmentgrp_data, "t-sourccod": t_sourccod_data, "t-brief": t_brief_data, "t-nation": t_nation_data, "t-region": t_region_data, "t-cancelreason": t_cancelreason_data, "t-cardtype": t_cardtype_data, "rev-list": rev_list_data, "b1-list": b1_list_data, "budget-umsatz": budget_umsatz_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    sysdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate - timedelta(days=1)

    res_line = db_session.query(Res_line).filter(
             ((Res_line.resstatus == 9) | (Res_line.resstatus == 10) & (Res_line.active_flag == 2)) & (Res_line.ankunft <= bill_date) & (Res_line.abreise >= bill_date - timedelta(days=1)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).first()
    while None != res_line:

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        gbuff2 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

        buf_zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.l_zuordnung[0])]})
        temp_res = Temp_res()
        temp_res_data.append(temp_res)

        temp_res.resnr = res_line.resnr
        temp_res.reslinnr = res_line.reslinnr
        temp_res.ci_date = res_line.ankunft
        temp_res.co_date = res_line.abreise
        temp_res.booktime = substring(res_line.reserve_char, 8, 5)
        temp_res.adult = res_line.erwachs
        temp_res.child = res_line.kind1
        temp_res.compliment = res_line.gratis
        temp_res.infant = res_line.kind2
        temp_res.compliment_ch = res_line.l_zuordnung[3]
        temp_res.arrangement = res_line.arrangement
        temp_res.rm_rate =  to_decimal(res_line.zipreis)
        temp_res.guestname = replace_str(res_line.NAME, chr_unicode(10) , "")
        temp_res.bill_instruction = res_line.code
        temp_res.zinr = res_line.zinr

        if num_entries(res_line.memozinr, ";") >= 2:
            temp_res.memozinr = entry(1, res_line.memozinr, ";")

        if gbuff2:
            temp_res.bill_receiver = replace_str(gbuff2.name + ", " + gbuff2.vorname1, chr_unicode(10) , "")

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

        if waehrung:
            temp_res.currency = waehrung.wabkurz

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (matches(Reslin_queasy.key,"*arrangement*")) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).first()
        temp_res.fixed_rate = None != reslin_queasy
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :

            if matches(entry(i - 1, res_line.zimmer_wunsch, ";"),r"*ChAge*"):
                temp_res.age = substring(entry(i - 1, res_line.zimmer_wunsch, ";") , 5)

            if matches(entry(i - 1, res_line.zimmer_wunsch, ";"),r"*SEGM_PUR*"):

                queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, to_int(substring(entry(1, zimmer_wunsch, ";") , 8)))]})

                if queasy:
                    temp_res.purpose = queasy.char3

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if arrangement:
            temp_res.argtnr = arrangement.argtnr

        if zimkateg:
            temp_res.room_type_name = zimkateg.kurzbez

        if buf_zimkateg:
            temp_res.rtc = buf_zimkateg.kurzbez

        if res_line.betrieb_gastpay == 11:

            if res_line.resstatus == 9:
                temp_res.resstatus = 15

            elif res_line.resstatus == 10:
                temp_res.resstatus = 16
            temp_res.nbrofroom = 0
        else:

            if res_line.resstatus == 9:
                temp_res.resstatus = 9

            elif res_line.resstatus == 10:
                temp_res.resstatus = 10
            temp_res.nbrofroom = res_line.zimmeranz

        if res_line.cancelled != None:
            temp_res.cancel_date = res_line.cancelled
        else:
            temp_res.cancel_date = date_mdy(1, 1, 1970)

        if guest:
            temp_res.card_type = guest.karteityp
            temp_res.company_code = entry(0, guest.steuernr, "|")
            temp_res.reserveid = guest.gastnr
            temp_res.code = guest.phonetik3
            temp_res.nationality = guest.nation1
            temp_res.localregion = guest.nation2

            if guest.vorname1 != "":
                temp_res.reservename = guest.name + " " + guest.vorname1
            else:
                temp_res.reservename = guest.name

        if reservation:
            temp_res.voucher_nr = reservation.vesrdepot
            temp_res.source_code = reservation.resart
            temp_res.segmentcode = reservation.segmentcode
            temp_res.grpname = reservation.groupname
            temp_res.letterno = reservation.briefnr
            temp_res.cancel_reason = replace_str(reservation.vesrdepot2, chr_unicode(10) , "")

            if reservation.resdat != None:
                temp_res.bookdate = reservation.resdat

        if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                    temp_res.rate_code = substring(iftask, 10)

        if temp_res.rate_code == " " or temp_res.rate_code == None or temp_res.rate_code == "":

            if matches(res_line.zimmer_wunsch,r"*$CODE$*"):
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(iftask, 0, 6) == ("$CODE$").lower() :
                        temp_res.rate_code = substring(iftask, 6)

        if res_line.ankunft != res_line.abreise:
            datum2 = res_line.abreise - timedelta(days=1)
        else:
            datum2 = res_line.abreise
        for datum in date_range(res_line.ankunft,datum2) :

            if datum <= bill_date and datum >= bill_date - timedelta(days=1):
                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_beverage = get_output(get_room_breakdown_bi(res_line._recid, datum, curr_i, curr_date))
                tot_food =  to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner)
                his_res = His_res()
                his_res_data.append(his_res)

                buffer_copy(temp_res, his_res)
                his_res.staydate = datum
                his_res.rm_rev =  to_decimal(net_lodg)
                his_res.food_rev =  to_decimal(tot_food)
                his_res.beverage_rev =  to_decimal(tot_beverage)
                his_res.other_rev =  to_decimal(tot_other)
                his_res.tot_tax =  to_decimal(tot_vat)
                his_res.tot_svc =  to_decimal(tot_service)
                his_res.fb_rev =  to_decimal(tot_food) + to_decimal(tot_beverage)


        temp_res_data.remove(temp_res)
        pass

        curr_recid = res_line._recid
        res_line = db_session.query(Res_line).filter(
                 ((Res_line.resstatus == 9) | (Res_line.resstatus == 10) & (Res_line.active_flag == 2)) & (Res_line.ankunft <= bill_date) & (Res_line.abreise >= bill_date - timedelta(days=1)) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line._recid > curr_recid)).first()

    genstat = db_session.query(Genstat).filter(
             ((Genstat.datum <= bill_date) & (Genstat.datum >= bill_date - timedelta(days=1))) & (Genstat.resstatus != 0) & (Genstat.zikatnr != 0) & (Genstat.res_logic[inc_value(1)])).first()
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
            his_res.source_code = genstat.source
            his_res.segmentcode = genstat.segmentcode
            his_res.res_logi = genstat.res_logi[1]
            his_res.arrangement = genstat.argt
            his_res.rm_rate =  to_decimal(genstat.zipreis)
            his_res.nbrofroom = 1


            his_res.rm_rev =  to_decimal(genstat.logis)
            his_res.fb_rev =  to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])
            his_res.other_rev =  to_decimal(genstat.res_deci[4] + genstat.res_deci[5] + genstat.res_deci[0])

            if his_res.cancel_date == None:
                his_res.cancel_date = date_mdy(1, 1, 1970)

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (matches(Reslin_queasy.key,"*arrangement*")) & (Reslin_queasy.resnr == genstat.resnr) & (Reslin_queasy.reslinnr == genstat.res_int[0])).first()
            his_res.fixed_rate = None != reslin_queasy

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, genstat.wahrungsnr)]})

            if waehrung:
                his_res.currency = waehrung.wabkurz

            res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

            if arrangement:
                his_res.argtnr = arrangement.argtnr

                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

                if artikel:
                    serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))
                    his_res.tot_tax =  to_decimal(vat1) + to_decimal(vat2)
                    his_res.tot_svc =  to_decimal(serv1)

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

                        if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                            his_res.rate_code = substring(iftask, 10)

                if his_res.rate_code == " " or his_res.rate_code == None or his_res.rate_code == "":

                    if matches(res_line.zimmer_wunsch,r"*$CODE$*"):
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(iftask, 0, 6) == ("$CODE$").lower() :
                                his_res.rate_code = substring(iftask, 6)

                gbuff2 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

                if gbuff2:
                    his_res.bill_receiver = replace_str(gbuff2.name + ", " + gbuff2.vorname1, chr_unicode(10) , "")


                his_res.reserveid = res_line.gastnr
                his_res.booktime = substring(res_line.reserve_char, 8, 5)
                his_res.nbrofroom = res_line.zimmeranz
                his_res.compliment_ch = res_line.l_zuordnung[3]
                his_res.guestname = replace_str(res_line.NAME, chr_unicode(10) , "")
                his_res.bill_instruction = res_line.code

                if num_entries(res_line.memozinr, ";") >= 2:
                    his_res.memozinr = entry(1, res_line.memozinr, ";")
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :

                    if matches(entry(i - 1, res_line.zimmer_wunsch, ";"),r"*ChAge*"):
                        his_res.age = substring(entry(i - 1, res_line.zimmer_wunsch, ";") , 5)

                    if matches(entry(i - 1, res_line.zimmer_wunsch, ";"),r"*SEGM_PUR*"):

                        queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, to_int(substring(entry(1, zimmer_wunsch, ";") , 8)))]})

                        if queasy:
                            his_res.purpose = queasy.char3

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

                if guest:
                    his_res.company_code = entry(0, guest.steuernr, "|")
                    his_res.code = guest.phonetik3
                    his_res.card_type = guest.karteityp

                    if guest.vorname1 != "":
                        his_res.reservename = guest.name + " " + guest.vorname1
                    else:
                        his_res.reservename = guest.name

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
                his_res.nationality = nation.kurzbez

            natbuff = get_cache (Nation, {"untergruppe": [(eq, 1)],"natcode": [(ne, 0)],"nationnr": [(eq, genstat.domestic)]})

            if natbuff:
                his_res.localregion = natbuff.kurzbez

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
                 ((Genstat.datum <= bill_date) & (Genstat.datum >= bill_date - timedelta(days=1))) & (Genstat.resstatus != 0) & (Genstat.zikatnr != 0) & (Genstat.res_logic[inc_value(1)]) & (Genstat._recid > curr_recid)).first()
    temp_res_data.clear()

    for res_line in db_session.query(Res_line).filter(
             (((Res_line.ankunft >= ci_date) | (Res_line.abreise > ci_date)) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 12) & (Res_line.resstatus != 10) & (Res_line.resstatus != 4)) | ((Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.gastnr > 0)).order_by(Res_line.resnr).all():

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
            temp_res.guestname = replace_str(res_line.NAME, chr_unicode(10) , "")
            temp_res.bill_instruction = res_line.code

            if num_entries(res_line.memozinr, ";") >= 2:
                temp_res.memozinr = entry(1, res_line.memozinr, ";")

            if res_line.cancelled != None:
                temp_res.cancel_date = res_line.cancelled
            else:
                temp_res.cancel_date = date_mdy(1, 1, 1970)

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
                temp_res.card_type = guest.karteityp
                temp_res.company_code = entry(0, guest.steuernr, "|")
                temp_res.reserveid = guest.gastnr
                temp_res.code = guest.phonetik3
                temp_res.nationality = guest.nation1
                temp_res.localregion = guest.nation2

                if guest.vorname1 != "":
                    temp_res.reservename = guest.name + " " + guest.vorname1
                else:
                    temp_res.reservename = guest.name

            if reservation:
                temp_res.source_code = reservation.resart
                temp_res.bookdate = reservation.resdat
                temp_res.segmentcode = reservation.segmentcode
                temp_res.voucher_nr = reservation.vesrdepot
                temp_res.grpname = reservation.groupname
                temp_res.letterno = reservation.briefnr
                temp_res.cancel_reason = replace_str(reservation.vesrdepot2, chr_unicode(10) , "")

            if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                        temp_res.rate_code = substring(iftask, 10)

            if temp_res.rate_code == " " or temp_res.rate_code == None or temp_res.rate_code == "":

                if matches(res_line.zimmer_wunsch,r"*$CODE$*"):
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(iftask, 0, 6) == ("$CODE$").lower() :
                            temp_res.rate_code = substring(iftask, 6)

            if res_line.ankunft != res_line.abreise:
                datum2 = res_line.abreise - timedelta(days=1)
            else:
                datum2 = res_line.abreise
            for datum in date_range(res_line.ankunft,datum2) :

                if datum >= sysdate:
                    fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_beverage = get_output(get_room_breakdown_bi(res_line._recid, datum, curr_i, curr_date))
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
                    future_res.fb_rev =  to_decimal(tot_food) + to_decimal("0")


            temp_res_data.remove(temp_res)
            pass

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.zinr != "")).order_by(Zimmer._recid).all():

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

        if zimkateg:
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            t_zimmer.roomno = zimmer.zinr
            t_zimmer.room_type = zimkateg.kurzbez

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_data.append(t_zimkateg)

        t_zimkateg.bezeichnung = zimkateg.bezeichnung
        t_zimkateg.kurzbez = zimkateg.kurzbez

    for arrangement in db_session.query(Arrangement).order_by(Arrangement._recid).all():
        t_arrangement = T_arrangement()
        t_arrangement_data.append(t_arrangement)

        t_arrangement.arrangement = arrangement.arrangement
        t_arrangement.argt_bez = arrangement.argt_bez

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2) & (Queasy.char1 != "")).order_by(Queasy._recid).all():
        t_ratecode = T_ratecode()
        t_ratecode_data.append(t_ratecode)

        t_ratecode.code = queasy.char1
        t_ratecode.bezeich = queasy.char2

    for segment in db_session.query(Segment).order_by(Segment._recid).all():
        t_segment = T_segment()
        t_segment_data.append(t_segment)

        t_segment.segmentcode = segment.segmentcode
        t_segment.segmentgrup = segment.segmentgrup
        t_segment.bezeich = segment.bezeich
        t_segment.bemerkung = segment.bemerkung

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 26) & (Queasy.char3 != "")).order_by(Queasy._recid).all():
        t_segmentgrp = T_segmentgrp()
        t_segmentgrp_data.append(t_segmentgrp)

        t_segmentgrp.segmentgrup = queasy.number1
        t_segmentgrp.bezeich = queasy.char3

    for sourccod in db_session.query(Sourccod).order_by(Sourccod._recid).all():
        t_sourccod = T_sourccod()
        t_sourccod_data.append(t_sourccod)

        t_sourccod.source_code = sourccod.source_code
        t_sourccod.bezeich = sourccod.bezeich

    for brief in db_session.query(Brief).order_by(Brief._recid).all():
        t_brief = T_brief()
        t_brief_data.append(t_brief)

        t_brief.briefnr = brief.briefnr
        t_brief.bezeich = brief.briefbezeich

    for nation in db_session.query(Nation).filter(
             (Nation.kurzbez != "") & (Nation.natcode == 0)).order_by(Nation._recid).all():
        t_nation = T_nation()
        t_nation_data.append(t_nation)

        t_nation.kurzbez = nation.kurzbez
        t_nation.bezeich = nation.bezeich

    for nation in db_session.query(Nation).filter(
             (Nation.kurzbez != "") & (Nation.untergruppe == 1) & (Nation.natcode != 0)).order_by(Nation._recid).all():
        t_region = T_region()
        t_region_data.append(t_region)

        t_region.kurzbez = nation.kurzbez
        t_region.bezeich = nation.bezeich

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 9)).order_by(Queasy._recid).all():
        t_bill_instruction = T_bill_instruction()
        t_bill_instruction_data.append(t_bill_instruction)

        t_bill_instruction.number1 = queasy.number1
        t_bill_instruction.char1 = queasy.char1

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 32)).order_by(Queasy._recid).all():
        t_cancelreason = T_cancelreason()
        t_cancelreason_data.append(t_cancelreason)

        t_cancelreason.number1 = queasy.number1
        t_cancelreason.char3 = queasy.char3

    for umsatz in db_session.query(Umsatz).filter(
             (Umsatz.datum <= bill_date) & (Umsatz.datum >= bill_date - timedelta(days=6))).order_by(Umsatz._recid).all():
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

    zinrstat_obj_list = {}
    for zinrstat, akt_code in db_session.query(Zinrstat, Akt_code).join(Akt_code,(Akt_code.aktionscode == Zinrstat.betriebsnr) & (Akt_code.aktiongrup == 4)).filter(
             (Zinrstat.zinr == ("Competitor").lower()) & (Zinrstat.datum <= bill_date) & (Zinrstat.datum >= bill_date - timedelta(days=1))).order_by(Zinrstat._recid).all():
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

    for budget in db_session.query(Budget).filter(
             (Budget.datum >= bill_date - timedelta(days=1))).order_by(Budget.datum).all():

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
    for datum in date_range(bill_date - 1,bill_date) :

        his_inv = query(his_inv_data, filters=(lambda his_inv: his_inv.datum == datum), first=True)

        if not his_inv:
            his_inv = His_inv()
            his_inv_data.append(his_inv)

            his_inv.datum = datum

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "tot-rm")],"datum": [(eq, datum)]})
            while None != zinrstat :
                his_inv.tot_room = his_inv.tot_room + zinrstat.zimmeranz

                curr_recid = zinrstat._recid
                zinrstat = db_session.query(Zinrstat).filter(
                         (Zinrstat.zinr == ("tot-rm").lower()) & (Zinrstat.datum == datum) & (Zinrstat._recid > curr_recid)).first()

            zkstat = get_cache (Zkstat, {"datum": [(eq, datum)]})
            while None != zkstat:
                his_inv.active_room = his_inv.active_room + zkstat.anz100

                curr_recid = zkstat._recid
                zkstat = db_session.query(Zkstat).filter(
                         (Zkstat.datum == datum) & (Zkstat._recid > curr_recid)).first()
            his_inv.inactive_room = his_inv.tot_room - his_inv.active_room

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "ooo")],"datum": [(eq, datum)]})
            while None != zinrstat :
                his_inv.ooo_room = his_inv.ooo_room + zinrstat.zimmeranz

                curr_recid = zinrstat._recid
                zinrstat = db_session.query(Zinrstat).filter(
                         (Zinrstat.zinr == ("ooo").lower()) & (Zinrstat.datum == datum) & (Zinrstat._recid > curr_recid)).first()

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "oos")],"datum": [(eq, datum)]})
            while None != zinrstat :
                his_inv.oos_room = his_inv.oos_room + zinrstat.zimmeranz

                curr_recid = zinrstat._recid
                zinrstat = db_session.query(Zinrstat).filter(
                         (Zinrstat.zinr == ("oos").lower()) & (Zinrstat.datum == datum) & (Zinrstat._recid > curr_recid)).first()
    for datum in date_range(ci_date,ci_date + 366) :

        future_inv = query(future_inv_data, filters=(lambda future_inv: future_inv.datum == datum), first=True)

        if not future_inv:
            future_inv = Future_inv()
            future_inv_data.append(future_inv)

            future_inv.datum = datum

            zinrstat = db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("tot-rm").lower())).order_by(Zinrstat._recid.desc()).first()

            if zinrstat:
                future_inv.tot_room = zinrstat.zimmeranz

            zkstat = get_cache (Zkstat, {"datum": [(eq, datum)]})
            while None != zkstat:
                future_inv.active_room = future_inv.active_room + zkstat.anz100

                curr_recid = zkstat._recid
                zkstat = db_session.query(Zkstat).filter(
                         (Zkstat.datum == datum) & (Zkstat._recid > curr_recid)).first()
            future_inv.inactive_room = future_inv.tot_room - future_inv.active_room

            outorder = get_cache (Outorder, {"gespende": [(ge, datum)],"gespstart": [(le, datum)],"zinr": [(ne, "")],"betriebsnr": [(le, 1)]})
            while None != outorder:
                future_inv.ooo_room = future_inv.ooo_room + 1

                curr_recid = outorder._recid
                outorder = db_session.query(Outorder).filter(
                         (Outorder.gespende >= datum) & (Outorder.gespstart <= datum) & (Outorder.zinr != "") & (Outorder.betriebsnr <= 1) & (Outorder._recid > curr_recid)).first()

            outorder = get_cache (Outorder, {"gespende": [(ge, datum)],"gespstart": [(le, datum)],"zinr": [(ne, "")],"betriebsnr": [(ge, 3)]})
            while None != outorder:
                future_inv.oos_room = future_inv.oos_room + 1

                curr_recid = outorder._recid
                outorder = db_session.query(Outorder).filter(
                         (Outorder.gespende >= datum) & (Outorder.gespstart <= datum) & (Outorder.zinr != "") & (Outorder.betriebsnr >= 3) & (Outorder._recid > curr_recid)).first()
    for i in range(0,2 + 1) :
        t_cardtype = T_cardtype()
        t_cardtype_data.append(t_cardtype)

        t_cardtype.number = i

        if i == 0:
            t_cardtype.bezeich = "Individual"

        elif i == 1:
            t_cardtype.bezeich = "Company"

        elif i == 2:
            t_cardtype.bezeich = "Travel Agent"
    success_flag = True

    return generate_output()