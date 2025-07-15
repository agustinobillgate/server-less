from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.get_room_breakdown_bi import get_room_breakdown_bi
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.calc_servvat import calc_servvat
from models import Guest, Nation, Res_line, Genstat, Zimkateg, Htparam, Reservation, Waehrung, Reslin_queasy, Queasy, Arrangement, Artikel, Segment, Zimmer, Sourccod, Brief, Umsatz, Zwkum, Hoteldpt, Akt_code, Zinrstat, Budget, Zkstat, Outorder

def bi_avalon_initialbl():
    success_flag = False
    his_res_list = []
    his_inv_list = []
    future_res_list = []
    future_inv_list = []
    t_zimmer_list = []
    t_zimkateg_list = []
    t_arrangement_list = []
    t_ratecode_list = []
    t_bill_instruction_list = []
    t_segment_list = []
    t_segmentgrp_list = []
    t_sourccod_list = []
    t_brief_list = []
    t_nation_list = []
    t_region_list = []
    t_cancelreason_list = []
    t_cardtype_list = []
    rev_list_list = []
    b1_list_list = []
    budget_umsatz_list = []
    exclude_article:str = ""
    datum:date = None
    datum2:date = None
    ci_date:date = None
    sysdate:date = None
    i:int = 0
    j:int = 0
    iftask:str = ""
    last_rechnr:int = 0
    ivalue:str = ""
    curr_i:int = 0
    curr_date:date = None
    start_date:date = None
    fnet_lodg:decimal = to_decimal("0.0")
    net_lodg:decimal = to_decimal("0.0")
    tot_breakfast:decimal = to_decimal("0.0")
    tot_lunch:decimal = to_decimal("0.0")
    tot_dinner:decimal = to_decimal("0.0")
    tot_other:decimal = to_decimal("0.0")
    tot_rmrev:decimal = to_decimal("0.0")
    tot_vat:decimal = to_decimal("0.0")
    tot_service:decimal = to_decimal("0.0")
    tot_fb:decimal = to_decimal("0.0")
    tot_food:decimal = to_decimal("0.0")
    tot_beverage:decimal = to_decimal("0.0")
    do_it1:bool = False
    vat_proz:decimal = 10
    do_it:bool = False
    serv_taxable:bool = False
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    netto:decimal = to_decimal("0.0")
    serv_betrag:decimal = to_decimal("0.0")
    outstr:str = ""
    outstr1:str = ""
    revcode:str = ""
    rechnr_nottax:int = 0
    bill_date:date = None
    bill_resnr:int = 0
    bill_reslinnr:int = 0
    bill_parentnr:int = 0
    bill_gastnr:int = 0
    ex_article:str = ""
    t_reslinnr:int = 0
    lreturn:bool = False
    hoappparam:str = ""
    vhost:str = ""
    vservice:str = ""
    htl_code:str = ""
    storage_dur:int = 0
    serv1:decimal = to_decimal("0.0")
    serv2:decimal = to_decimal("0.0")
    vat1:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    vat3:decimal = to_decimal("0.0")
    vat4:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    fact1:decimal = to_decimal("0.0")
    fact2:decimal = to_decimal("0.0")
    query_str:str = ""
    guest = nation = res_line = genstat = zimkateg = htparam = reservation = waehrung = reslin_queasy = queasy = arrangement = artikel = segment = zimmer = sourccod = brief = umsatz = zwkum = hoteldpt = akt_code = zinrstat = budget = zkstat = outorder = None

    his_res = his_inv = t_bediener = t_salesbud = temp_res = future_res = future_inv = t_segment = t_segmentgrp = t_sourccod = t_zimmer = t_zimkateg = t_arrangement = t_ratecode = t_brief = t_nation = t_region = t_bill_instruction = t_cancelreason = t_cardtype = rev_list = b1_list = budget_umsatz = deposit_list = gbuff = gbuff2 = natbuff = bufres_line = buf_genstat = buf_zimkateg = None

    his_res_list, His_res = create_model("His_res", {"resnr":int, "reslinnr":int, "staydate":date, "ci_date":date, "co_date":date, "nbrofroom":int, "room_type_name":str, "rm_rev":decimal, "fb_rev":decimal, "other_rev":decimal, "resstatus":int, "reserveid":int, "reservename":str, "bookdate":date, "booktime":str, "rate_code":str, "nationality":str, "segmentcode":int, "cancel_date":date, "zinr":str, "memozinr":str, "food_rev":decimal, "beverage_rev":decimal, "card_type":int, "company_code":str, "source_code":int, "adult":int, "child":int, "infant":int, "compliment":int, "compliment_ch":int, "age":str, "argtnr":int, "res_logi":bool, "rtc":str, "arrangement":str, "voucher_nr":str, "rm_rate":decimal, "fixed_rate":bool, "currency":str, "guestname":str, "bill_receiver":str, "bill_instruction":str, "purpose":str, "grpname":str, "letterno":int, "localregion":str, "cancel_reason":str, "code":str, "early_booking":str, "bona_fide":str, "tot_tax":decimal, "tot_svc":decimal}, {"res_logi": True})
    his_inv_list, His_inv = create_model("His_inv", {"datum":date, "tot_room":int, "inactive_room":int, "active_room":int, "ooo_room":int, "oos_room":int})
    t_bediener_list, T_bediener = create_model("T_bediener", {"userinit":str, "username":str})
    t_salesbud_list, T_salesbud = create_model("T_salesbud", {"jahr":int, "monat":int, "argtumsatz":decimal, "f_b_umsatz":decimal, "sonst_umsatz":decimal, "room_nights":int, "id":str})
    temp_res_list, Temp_res = create_model_like(His_res)
    future_res_list, Future_res = create_model_like(His_res)
    future_inv_list, Future_inv = create_model_like(His_inv)
    t_segment_list, T_segment = create_model("T_segment", {"segmentcode":int, "segmentgrup":int, "bezeich":str, "bemerkung":str})
    t_segmentgrp_list, T_segmentgrp = create_model("T_segmentgrp", {"segmentgrup":int, "bezeich":str})
    t_sourccod_list, T_sourccod = create_model("T_sourccod", {"source_code":int, "bezeich":str})
    t_zimmer_list, T_zimmer = create_model("T_zimmer", {"roomno":str, "room_type":str})
    t_zimkateg_list, T_zimkateg = create_model("T_zimkateg", {"bezeich":str, "kurzbez":str})
    t_arrangement_list, T_arrangement = create_model("T_arrangement", {"arrangement":str, "argt_bez":str})
    t_ratecode_list, T_ratecode = create_model("T_ratecode", {"code":str, "bezeich":str})
    t_brief_list, T_brief = create_model("T_brief", {"briefnr":int, "bezeich":str})
    t_nation_list, T_nation = create_model("T_nation", {"kurzbez":str, "bezeich":str})
    t_region_list, T_region = create_model("T_region", {"kurzbez":str, "bezeich":str})
    t_bill_instruction_list, T_bill_instruction = create_model("T_bill_instruction", {"number1":int, "char1":str})
    t_cancelreason_list, T_cancelreason = create_model("T_cancelreason", {"number1":int, "char3":str})
    t_cardtype_list, T_cardtype = create_model("T_cardtype", {"number":int, "bezeich":str})
    rev_list_list, Rev_list = create_model("Rev_list", {"dept":int, "s_dept":str, "datum":date, "s_grp":str, "subgrp":int, "s_subgrp":str, "revart":int, "s_revart":str, "amount":decimal})
    b1_list_list, B1_list = create_model("B1_list", {"datum":date, "zinr":str, "betriebsnr":int, "bezeich":str, "zimmeranz":int, "personen":int, "argtumsatz":decimal, "logisumsatz":decimal})
    budget_umsatz_list, Budget_umsatz = create_model("Budget_umsatz", {"datum":date, "department":int, "s_dept":str, "umsatzart":int, "s_umsatzart":str, "zwkum":decimal, "budget":decimal})
    deposit_list_list, Deposit_list = create_model("Deposit_list", {"grpflag":bool, "resnr":int, "reser_name":str, "groupname":str, "resli_name":str, "ankunft":date, "limitdate":date, "depositgef":decimal, "depositbez":decimal, "depositbez2":decimal, "zahldatum":date, "zahlkonto":int, "zahldatum2":date, "zahlkonto2":int})

    Gbuff = create_buffer("Gbuff",Guest)
    Gbuff2 = create_buffer("Gbuff2",Guest)
    Natbuff = create_buffer("Natbuff",Nation)
    Bufres_line = create_buffer("Bufres_line",Res_line)
    Buf_genstat = create_buffer("Buf_genstat",Genstat)
    Buf_zimkateg = create_buffer("Buf_zimkateg",Zimkateg)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, his_res_list, his_inv_list, future_res_list, future_inv_list, t_zimmer_list, t_zimkateg_list, t_arrangement_list, t_ratecode_list, t_bill_instruction_list, t_segment_list, t_segmentgrp_list, t_sourccod_list, t_brief_list, t_nation_list, t_region_list, t_cancelreason_list, t_cardtype_list, rev_list_list, b1_list_list, budget_umsatz_list, exclude_article, datum, datum2, ci_date, sysdate, i, j, iftask, last_rechnr, ivalue, curr_i, curr_date, start_date, fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_fb, tot_food, tot_beverage, do_it1, vat_proz, do_it, serv_taxable, serv, vat, netto, serv_betrag, outstr, outstr1, revcode, rechnr_nottax, bill_date, bill_resnr, bill_reslinnr, bill_parentnr, bill_gastnr, ex_article, t_reslinnr, lreturn, hoappparam, vhost, vservice, htl_code, storage_dur, serv1, serv2, vat1, vat2, vat3, vat4, fact, fact1, fact2, query_str, guest, nation, res_line, genstat, zimkateg, htparam, reservation, waehrung, reslin_queasy, queasy, arrangement, artikel, segment, zimmer, sourccod, brief, umsatz, zwkum, hoteldpt, akt_code, zinrstat, budget, zkstat, outorder
        nonlocal gbuff, gbuff2, natbuff, bufres_line, buf_genstat, buf_zimkateg


        nonlocal his_res, his_inv, t_bediener, t_salesbud, temp_res, future_res, future_inv, t_segment, t_segmentgrp, t_sourccod, t_zimmer, t_zimkateg, t_arrangement, t_ratecode, t_brief, t_nation, t_region, t_bill_instruction, t_cancelreason, t_cardtype, rev_list, b1_list, budget_umsatz, deposit_list, gbuff, gbuff2, natbuff, bufres_line, buf_genstat, buf_zimkateg
        nonlocal his_res_list, his_inv_list, t_bediener_list, t_salesbud_list, temp_res_list, future_res_list, future_inv_list, t_segment_list, t_segmentgrp_list, t_sourccod_list, t_zimmer_list, t_zimkateg_list, t_arrangement_list, t_ratecode_list, t_brief_list, t_nation_list, t_region_list, t_bill_instruction_list, t_cancelreason_list, t_cardtype_list, rev_list_list, b1_list_list, budget_umsatz_list, deposit_list_list
        return {"success_flag": success_flag, "his-res": his_res_list, "his-inv": his_inv_list, "future-res": future_res_list, "future-inv": future_inv_list, "t-zimmer": t_zimmer_list, "t-zimkateg": t_zimkateg_list, "t-arrangement": t_arrangement_list, "t-ratecode": t_ratecode_list, "t-bill-instruction": t_bill_instruction_list, "t-segment": t_segment_list, "t-segmentgrp": t_segmentgrp_list, "t-sourccod": t_sourccod_list, "t-brief": t_brief_list, "t-nation": t_nation_list, "t-region": t_region_list, "t-cancelreason": t_cancelreason_list, "t-cardtype": t_cardtype_list, "rev-list": rev_list_list, "b1-list": b1_list_list, "budget-umsatz": budget_umsatz_list}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    sysdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate - timedelta(days=1)
    storage_dur = get_year(bill_date) - 1
    start_date = date_mdy(1, 1, storage_dur)

    res_line = db_session.query(Res_line).filter(
             ((Res_line.resstatus == 9) | (Res_line.resstatus == 10) & (Res_line.active_flag == 2)) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft >= start_date) & (Res_line.ankunft <= bill_date)).first()
    while None != res_line:

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == res_line.resnr)).first()

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == res_line.zikatnr)).first()

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnr)).first()

        gbuff = db_session.query(Gbuff).filter(
                 (Gbuff.gastnr == res_line.gastnrmember)).first()

        gbuff2 = db_session.query(Gbuff2).filter(
                 (Gbuff2.gastnr == res_line.gastnrpay)).first()

        buf_zimkateg = db_session.query(Buf_zimkateg).filter(
                 (Buf_zimkateg.zikatnr == res_line.l_zuordnung[0)]).first()
        temp_res = Temp_res()
        temp_res_list.append(temp_res)

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
        temp_res.guestname = replace_str(res_line.name, chr(10) , "")
        temp_res.bill_instruction = res_line.code
        temp_res.zinr = res_line.zinr

        if num_entries(res_line.memozinr, ";") >= 2:
            temp_res.memozinr = entry(1, res_line.memozinr, ";")

        if gbuff2:
            temp_res.bill_receiver = replace_str(gbuff2.name + ", " + gbuff2.vorname1, chr(10) , "")

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

        if waehrung:
            temp_res.currency = waehrung.wabkurz

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key).op("~")(("*arrangement*".lower().replace("*",".*")))) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).first()
        temp_res.fixed_rate = None != reslin_queasy
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :

            if re.match(r".*ChAge.*",entry(i - 1, res_line.zimmer_wunsch, ";"), re.IGNORECASE):
                temp_res.age = substring(entry(i - 1, res_line.zimmer_wunsch, ";") , 5)

            if re.match(r".*SEGM_PUR.*",entry(i - 1, res_line.zimmer_wunsch, ";"), re.IGNORECASE):

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 143) & (Queasy.number1 == to_int(substring(entry(1, zimmer_wunsch, ";") , 8)))).first()

                if queasy:
                    temp_res.purpose = queasy.char3

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == res_line.arrangement)).first()

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

        if guest:
            temp_res.card_type = guest.karteityp
            temp_res.company_code = entry(0, guest.steuernr, "|")
            temp_res.reserveid = guest.gastnr
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
            temp_res.cancel_reason = replace_str(reservation.vesrdepot2, chr(10) , "")

            if reservation.resdat != None:
                temp_res.bookdate = reservation.resdat

        if re.match(r".*\$OrigCode\$.*",res_line.zimmer_wunsch, re.IGNORECASE):
            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                    temp_res.rate_code = substring(iftask, 10)

        if res_line.ankunft != res_line.abreise:
            datum2 = res_line.abreise - timedelta(days=1)
        else:
            datum2 = res_line.abreise
        for datum in date_range(res_line.ankunft,datum2) :

            if datum >= start_date and datum <= bill_date:
                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_beverage = get_output(get_room_breakdown_bi(res_line._recid, datum, curr_i, curr_date))
                tot_food =  to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner)
                his_res = His_res()
                his_res_list.append(his_res)

                buffer_copy(temp_res, his_res)
                his_res.staydate = datum
                his_res.rm_rev =  to_decimal(net_lodg)
                his_res.food_rev =  to_decimal(tot_food)
                his_res.beverage_rev =  to_decimal(tot_beverage)
                his_res.other_rev =  to_decimal(tot_other)
                his_res.tot_tax =  to_decimal(tot_vat)
                his_res.tot_svc =  to_decimal(tot_service)
                his_res.fb_rev =  to_decimal(tot_food) + to_decimal(tot_beverage)


        temp_res_list.remove(temp_res)
        pass

        curr_recid = res_line._recid
        res_line = db_session.query(Res_line).filter(
                 ((Res_line.resstatus == 9) | (Res_line.resstatus == 10) & (Res_line.active_flag == 2)) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft >= start_date) & (Res_line.ankunft <= bill_date)).filter(Res_line._recid > curr_recid).first()

    genstat = db_session.query(Genstat).filter(
             ((Genstat.datum >= start_date) & (Genstat.datum <= bill_date)) & (Genstat.resstatus != 0) & (Genstat.zikatnr != 0) & (Genstat.res_logic[inc_value(1))]).first()
    while None != genstat:

        his_res = query(his_res_list, filters=(lambda his_res: his_res.zinr == genstat.zinr and his_res.staydate == genstat.datum and his_res.resnr == genstat.resnr and his_res.reslinnr == genstat.res_int[0]), first=True)

        if not his_res:
            his_res = His_res()
            his_res_list.append(his_res)

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

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key).op("~")(("*arrangement*".lower().replace("*",".*")))) & (Reslin_queasy.resnr == genstat.resnr) & (Reslin_queasy.reslinnr == genstat.res_int[0)]).first()
            his_res.fixed_rate = None != reslin_queasy

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == genstat.wahrungsnr)).first()

            if waehrung:
                his_res.currency = waehrung.wabkurz

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == genstat.resnr) & (Res_line.reslinnr == genstat.res_int[0)]).first()

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == genstat.argt)).first()

            if arrangement:
                his_res.argtnr = arrangement.argtnr

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == arrangement.argt_artikelnr) & (Artikel.departement == 0)).first()

                if artikel:
                    serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))
                    his_res.tot_tax =  to_decimal(vat1) + to_decimal(vat2)
                    his_res.tot_svc =  to_decimal(serv1)

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == genstat.zikatnr)).first()

            if zimkateg:
                his_res.room_type_name = zimkateg.kurzbez

            buf_zimkateg = db_session.query(Buf_zimkateg).filter(
                     (Buf_zimkateg.zikatnr == res_line.l_zuordnung[0)]).first()

            if buf_zimkateg:
                his_res.rtc = buf_zimkateg.kurzbez

            if res_line:

                if re.match(r".*\$OrigCode\$.*",res_line.zimmer_wunsch, re.IGNORECASE):
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                            his_res.rate_code = substring(iftask, 10)

                gbuff2 = db_session.query(Gbuff2).filter(
                         (Gbuff2.gastnr == res_line.gastnrpay)).first()

                if gbuff2:
                    his_res.bill_receiver = replace_str(gbuff2.name + ", " + gbuff2.vorname1, chr(10) , "")


                his_res.reserveid = res_line.gastnr
                his_res.booktime = substring(res_line.reserve_char, 8, 5)
                his_res.nbrofroom = res_line.zimmeranz
                his_res.compliment_ch = res_line.l_zuordnung[3]
                his_res.guestname = replace_str(res_line.name, chr(10) , "")
                his_res.bill_instruction = res_line.code

                if num_entries(res_line.memozinr, ";") >= 2:
                    his_res.memozinr = entry(1, res_line.memozinr, ";")
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :

                    if re.match(r".*ChAge.*",entry(i - 1, res_line.zimmer_wunsch, ";"), re.IGNORECASE):
                        his_res.age = substring(entry(i - 1, res_line.zimmer_wunsch, ";") , 5)

                    if re.match(r".*SEGM_PUR.*",entry(i - 1, res_line.zimmer_wunsch, ";"), re.IGNORECASE):

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 143) & (Queasy.number1 == to_int(substring(entry(1, zimmer_wunsch, ";") , 8)))).first()

                        if queasy:
                            his_res.purpose = queasy.char3

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == genstat.gastnr)).first()

                if guest:
                    his_res.company_code = entry(0, guest.steuernr, "|")

                    if guest.vorname1 != "":
                        his_res.reservename = guest.name + " " + guest.vorname1
                    else:
                        his_res.reservename = guest.name
                    his_res.card_type = guest.karteityp

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

                if genstat.gastnrmember == res_line.gastnrmember:

                    natbuff = db_session.query(Natbuff).filter(
                             (Natbuff.untergruppe == 1) & (Natbuff.natcode != 0) & (Natbuff.nationnr == genstat.domestic)).first()

                    if natbuff:
                        his_res.localregion = natbuff.kurzbez


                else:
                    his_res.localregion = ""

            nation = db_session.query(Nation).filter(
                     (Nation.natcode == 0) & (Nation.nationnr == genstat.nation)).first()

            if nation:
                his_res.nationality = nation.kurzbez

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == genstat.resnr)).first()

            if reservation:
                his_res.voucher_nr = reservation.vesrdepot
                his_res.grpname = reservation.groupname
                his_res.letterno = reservation.briefnr
                his_res.cancel_reason = replace_str(reservation.vesrdepot2, chr(10) , "")

                if reservation.resdat != None:
                    his_res.bookdate = reservation.resdat

        curr_recid = genstat._recid
        genstat = db_session.query(Genstat).filter(
                 ((Genstat.datum >= start_date) & (Genstat.datum <= bill_date)) & (Genstat.resstatus != 0) & (Genstat.zikatnr != 0) & (Genstat.res_logic[inc_value(1))]).filter(Genstat._recid > curr_recid).first()
    temp_res_list.clear()

    for res_line in db_session.query(Res_line).filter(
             (((Res_line.ankunft >= ci_date) | (Res_line.abreise > ci_date)) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 12) & (Res_line.resstatus != 10) & (Res_line.resstatus != 4)) | ((Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.gastnr > 0)).order_by(Res_line.resnr).all():

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == res_line.resnr)).first()

        segment = db_session.query(Segment).filter(
                 (Segment.segmentcode == reservation.segmentcode)).first()
        do_it = None != segment and segment.vip_level == 0

        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.zinr == res_line.zinr)).first()

        if do_it and zimmer:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 14) & (Queasy.char1 == res_line.zinr) & (Queasy.date1 <= ci_date) & (Queasy.date2 >= ci_date)).first()

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
            temp_res_list.append(temp_res)

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
            temp_res.guestname = replace_str(res_line.name, chr(10) , "")
            temp_res.bill_instruction = res_line.code

            if num_entries(res_line.memozinr, ";") >= 2:
                temp_res.memozinr = entry(1, res_line.memozinr, ";")

            if res_line.cancelled != None:
                temp_res.cancel_date = res_line.cancelled

            gbuff2 = db_session.query(Gbuff2).filter(
                     (Gbuff2.gastnr == res_line.gastnrpay)).first()

            if gbuff2:
                temp_res.bill_receiver = replace_str(gbuff2.name + ", " + gbuff2.vorname1, chr(10) , "")

            buf_zimkateg = db_session.query(Buf_zimkateg).filter(
                     (Buf_zimkateg.zikatnr == res_line.l_zuordnung[0)]).first()

            if buf_zimkateg:
                temp_res.rtc = buf_zimkateg.kurzbez


            for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :

                if re.match(r".*ChAge.*",entry(i - 1, res_line.zimmer_wunsch, ";"), re.IGNORECASE):
                    temp_res.age = substring(entry(i - 1, res_line.zimmer_wunsch, ";") , 5)

                if re.match(r".*SEGM_PUR.*",entry(i - 1, res_line.zimmer_wunsch, ";"), re.IGNORECASE):

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 143) & (Queasy.number1 == to_int(substring(entry(1, zimmer_wunsch, ";") , 8)))).first()

                    if queasy:
                        temp_res.purpose = queasy.char3

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key).op("~")(("*arrangement*".lower().replace("*",".*")))) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).first()
            temp_res.fixed_rate = None != reslin_queasy

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == res_line.arrangement)).first()

            if arrangement:
                temp_res.argtnr = arrangement.argtnr

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

            if waehrung:
                temp_res.currency = waehrung.wabkurz

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

            if zimkateg:
                temp_res.room_type_name = zimkateg.kurzbez

            if res_line.ankunft == res_line.abreise or res_line.resstatus == 11 or res_line.resstatus == 13 or res_line.zimmerfix:
                temp_res.nbrofroom = 0
            else:
                temp_res.nbrofroom = res_line.zimmeranz

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnr)).first()

            if guest:
                temp_res.card_type = guest.karteityp
                temp_res.company_code = entry(0, guest.steuernr, "|")
                temp_res.reserveid = guest.gastnr
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
                temp_res.cancel_reason = replace_str(reservation.vesrdepot2, chr(10) , "")

                deposit_list = query(deposit_list_list, filters=(lambda deposit_list: deposit_list.resnr == reservation.resnr and reservation.depositgef > 0), first=True)

                if not deposit_list:
                    deposit_list = Deposit_list()
                    deposit_list_list.append(deposit_list)

                    deposit_list.grpflag = reservation.grpflag
                    deposit_list.resnr = reservation.resnr
                    deposit_list.reser_name = reservation.name
                    deposit_list.groupname = reservation.groupname
                    deposit_list.resli_name = res_line.name
                    deposit_list.ankunft = res_line.ankunft
                    deposit_list.depositgef =  to_decimal(reservation.depositgef)
                    deposit_list.depositbez =  to_decimal(reservation.depositbez)
                    deposit_list.depositbez2 =  to_decimal(reservation.depositbez2)
                    deposit_list.zahlkonto = reservation.zahlkonto
                    deposit_list.zahlkonto2 = reservation.zahlkonto2

                    if reservation.limitdate != None:
                        deposit_list.limitdate = reservation.limitdate

                    if reservation.zahldatum != None:
                        deposit_list.zahldatum = reservation.zahldatum

                    if reservation.zahldatum2 != None:
                        deposit_list.zahldatum2 = reservation.zahldatum2

            if re.match(r".*\$OrigCode\$.*",res_line.zimmer_wunsch, re.IGNORECASE):
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                        temp_res.rate_code = substring(iftask, 10)

            if res_line.ankunft != res_line.abreise:
                datum2 = res_line.abreise - timedelta(days=1)
            else:
                datum2 = res_line.abreise
            for datum in date_range(res_line.ankunft,datum2) :

                if datum >= sysdate:
                    fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_beverage = get_output(get_room_breakdown_bi(res_line._recid, datum, curr_i, curr_date))
                    tot_food =  to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner)
                    future_res = Future_res()
                    future_res_list.append(future_res)

                    buffer_copy(temp_res, future_res)
                    future_res.staydate = datum
                    future_res.rm_rev =  to_decimal(net_lodg)
                    future_res.food_rev =  to_decimal(tot_food)
                    future_res.beverage_rev =  to_decimal(tot_beverage)
                    future_res.other_rev =  to_decimal(tot_other)
                    future_res.tot_tax =  to_decimal(tot_vat)
                    future_res.tot_svc =  to_decimal(tot_service)
                    future_res.fb_rev =  to_decimal(tot_food) + to_decimal(tot_beverage)


            temp_res_list.remove(temp_res)
            pass

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.zinr != "")).order_by(Zimmer._recid).all():

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == zimmer.zikatnr)).first()

        if zimkateg:
            t_zimmer = T_zimmer()
            t_zimmer_list.append(t_zimmer)

            t_zimmer.roomno = zimmer.zinr
            t_zimmer.room_type = zimkateg.kurzbez

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_list.append(t_zimkateg)

        t_zimkateg.bezeichnung = zimkateg.bezeichnung
        t_zimkateg.kurzbez = zimkateg.kurzbez

    for arrangement in db_session.query(Arrangement).order_by(Arrangement._recid).all():
        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        t_arrangement.arrangement = arrangement.arrangement
        t_arrangement.argt_bez = arrangement.argt_bez

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2) & (Queasy.char1 != "")).order_by(Queasy._recid).all():
        t_ratecode = T_ratecode()
        t_ratecode_list.append(t_ratecode)

        t_ratecode.code = queasy.char1
        t_ratecode.bezeich = queasy.char2

    for segment in db_session.query(Segment).order_by(Segment._recid).all():
        t_segment = T_segment()
        t_segment_list.append(t_segment)

        t_segment.segmentcode = segment.segmentcode
        t_segment.segmentgrup = segment.segmentgrup
        t_segment.bezeich = segment.bezeich
        t_segment.bemerkung = segment.bemerkung

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 26) & (Queasy.char3 != "")).order_by(Queasy._recid).all():
        t_segmentgrp = T_segmentgrp()
        t_segmentgrp_list.append(t_segmentgrp)

        t_segmentgrp.segmentgrup = queasy.number1
        t_segmentgrp.bezeich = queasy.char3

    for sourccod in db_session.query(Sourccod).order_by(Sourccod._recid).all():
        t_sourccod = T_sourccod()
        t_sourccod_list.append(t_sourccod)

        t_sourccod.source_code = sourccod.source_code
        t_sourccod.bezeich = sourccod.bezeich

    for brief in db_session.query(Brief).order_by(Brief._recid).all():
        t_brief = T_brief()
        t_brief_list.append(t_brief)

        t_brief.briefnr = brief.briefnr
        t_brief.bezeich = brief.briefbezeich

    for nation in db_session.query(Nation).filter(
             (Nation.kurzbez != "") & (Nation.natcode == 0)).order_by(Nation._recid).all():
        t_nation = T_nation()
        t_nation_list.append(t_nation)

        t_nation.kurzbez = nation.kurzbez
        t_nation.bezeich = nation.bezeich

    for nation in db_session.query(Nation).filter(
             (Nation.kurzbez != "") & (Nation.untergruppe == 1) & (Nation.natcode != 0)).order_by(Nation._recid).all():
        t_region = T_region()
        t_region_list.append(t_region)

        t_region.kurzbez = nation.kurzbez
        t_region.bezeich = nation.bezeich

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 9)).order_by(Queasy._recid).all():
        t_bill_instruction = T_bill_instruction()
        t_bill_instruction_list.append(t_bill_instruction)

        t_bill_instruction.number1 = queasy.number1
        t_bill_instruction.char1 = queasy.char1

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 32)).order_by(Queasy._recid).all():
        t_cancelreason = T_cancelreason()
        t_cancelreason_list.append(t_cancelreason)

        t_cancelreason.number1 = queasy.number1
        t_cancelreason.char3 = queasy.char3

    for umsatz in db_session.query(Umsatz).filter(
             (Umsatz.datum >= start_date) & (Umsatz.datum <= bill_date)).order_by(Umsatz._recid).all():
        netto =  to_decimal("0")

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == umsatz.artnr) & (Artikel.departement == umsatz.departement)).first()

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

            zwkum = db_session.query(Zwkum).filter(
                     (Zwkum.departement == artikel.departement) & (Zwkum.zknr == artikel.zwkum)).first()

            rev_list = query(rev_list_list, filters=(lambda rev_list: rev_list.dept == umsatz.departement and rev_list.datum == umsatz.datum and rev_list.subgrp == zwkum.zknr and rev_list.s_revart == artikel.bezeich), first=True)

            if not rev_list:
                rev_list = Rev_list()
                rev_list_list.append(rev_list)


                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == umsatz.departement)).first()
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

    zinrstat_obj_list = []
    for zinrstat, akt_code in db_session.query(Zinrstat, Akt_code).join(Akt_code,(Akt_code.aktionscode == Zinrstat.betriebsnr) & (Akt_code.aktiongrup == 4)).filter(
             (func.lower(Zinrstat.zinr) == ("Competitor").lower()) & (Zinrstat.datum >= start_date) & (Zinrstat.datum <= bill_date)).order_by(Zinrstat._recid).all():
        if zinrstat._recid in zinrstat_obj_list:
            continue
        else:
            zinrstat_obj_list.append(zinrstat._recid)


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.datum = zinrstat.datum
        b1_list.zinr = zinrstat.zinr
        b1_list.betriebsnr = zinrstat.betriebsnr
        b1_list.bezeich = akt_code.bezeich
        b1_list.zimmeranz = zinrstat.zimmeranz
        b1_list.personen = zinrstat.personen
        b1_list.argtumsatz =  to_decimal(zinrstat.argtumsatz)
        b1_list.logisumsatz =  to_decimal(zinrstat.logisumsatz)

    for budget in db_session.query(Budget).filter(
             (Budget.datum >= start_date)).order_by(Budget.datum).all():

        artikel = db_session.query(Artikel).filter(
                 (Artikel.departement == budget.departement) & (Artikel.artnr == budget.artnr)).first()

        if artikel and artikel.umsatzart > 0:

            budget_umsatz = query(budget_umsatz_list, filters=(lambda budget_umsatz: budget_umsatz.datum == budget.datum and budget_umsatz.department == budget.departement and budget_umsatz.s_umsatzart == artikel.bezeich), first=True)

            if not budget_umsatz:
                budget_umsatz = Budget_umsatz()
                budget_umsatz_list.append(budget_umsatz)

                budget_umsatz.datum = budget.datum
                budget_umsatz.department = budget.departement
                budget_umsatz.umsatzart = artikel.umsatzart
                budget_umsatz.s_umsatzart = artikel.bezeich
                budget_umsatz.zwkum =  to_decimal(artikel.zwkum)
                budget_umsatz.budget =  to_decimal(budget.betrag)

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == budget.departement)).first()

                if hoteldpt:
                    budget_umsatz.s_dept = hoteldpt.depart
    for datum in date_range(start_date,bill_date) :

        his_inv = query(his_inv_list, filters=(lambda his_inv: his_inv.datum == datum), first=True)

        if not his_inv:
            his_inv = His_inv()
            his_inv_list.append(his_inv)

            his_inv.datum = datum

            zinrstat = db_session.query(Zinrstat).filter(
                     (func.lower(Zinrstat.zinr) == ("tot-rm").lower()) & (Zinrstat.datum == datum)).first()
            while None != zinrstat :
                his_inv.tot_room = his_inv.tot_room + zinrstat.zimmeranz

                curr_recid = zinrstat._recid
                zinrstat = db_session.query(Zinrstat).filter(
                         (func.lower(Zinrstat.zinr) == ("tot-rm").lower()) & (Zinrstat.datum == datum)).filter(Zinrstat._recid > curr_recid).first()

            zkstat = db_session.query(Zkstat).filter(
                     (Zkstat.datum == datum)).first()
            while None != zkstat:
                his_inv.active_room = his_inv.active_room + zkstat.anz100

                curr_recid = zkstat._recid
                zkstat = db_session.query(Zkstat).filter(
                         (Zkstat.datum == datum)).filter(Zkstat._recid > curr_recid).first()
            his_inv.inactive_room = his_inv.tot_room - his_inv.active_room

            zinrstat = db_session.query(Zinrstat).filter(
                     (func.lower(Zinrstat.zinr) == ("ooo").lower()) & (Zinrstat.datum == datum)).first()
            while None != zinrstat :
                his_inv.ooo_room = his_inv.ooo_room + zinrstat.zimmeranz

                curr_recid = zinrstat._recid
                zinrstat = db_session.query(Zinrstat).filter(
                         (func.lower(Zinrstat.zinr) == ("ooo").lower()) & (Zinrstat.datum == datum)).filter(Zinrstat._recid > curr_recid).first()

            zinrstat = db_session.query(Zinrstat).filter(
                     (func.lower(Zinrstat.zinr) == ("oos").lower()) & (Zinrstat.datum == datum)).first()
            while None != zinrstat :
                his_inv.oos_room = his_inv.oos_room + zinrstat.zimmeranz

                curr_recid = zinrstat._recid
                zinrstat = db_session.query(Zinrstat).filter(
                         (func.lower(Zinrstat.zinr) == ("oos").lower()) & (Zinrstat.datum == datum)).filter(Zinrstat._recid > curr_recid).first()
    for datum in date_range(ci_date,ci_date + 366) :

        future_inv = query(future_inv_list, filters=(lambda future_inv: future_inv.datum == datum), first=True)

        if not future_inv:
            future_inv = Future_inv()
            future_inv_list.append(future_inv)

            future_inv.datum = datum

            zinrstat = db_session.query(Zinrstat).filter(
                     (func.lower(Zinrstat.zinr) == ("tot-rm").lower())).order_by(Zinrstat._recid.desc()).first()

            if zinrstat:
                future_inv.tot_room = zinrstat.zimmeranz

            zkstat = db_session.query(Zkstat).filter(
                     (Zkstat.datum == datum)).first()
            while None != zkstat:
                future_inv.active_room = future_inv.active_room + zkstat.anz100

                curr_recid = zkstat._recid
                zkstat = db_session.query(Zkstat).filter(
                         (Zkstat.datum == datum)).filter(Zkstat._recid > curr_recid).first()
            future_inv.inactive_room = future_inv.tot_room - future_inv.active_room

            outorder = db_session.query(Outorder).filter(
                     (Outorder.gespende >= datum) & (Outorder.gespstart <= datum) & (Outorder.zinr != "") & (Outorder.betriebsnr <= 1)).first()
            while None != outorder:
                future_inv.ooo_room = future_inv.ooo_room + 1

                curr_recid = outorder._recid
                outorder = db_session.query(Outorder).filter(
                         (Outorder.gespende >= datum) & (Outorder.gespstart <= datum) & (Outorder.zinr != "") & (Outorder.betriebsnr <= 1)).filter(Outorder._recid > curr_recid).first()

            outorder = db_session.query(Outorder).filter(
                     (Outorder.gespende >= datum) & (Outorder.gespstart <= datum) & (Outorder.zinr != "") & (Outorder.betriebsnr >= 3)).first()
            while None != outorder:
                future_inv.oos_room = future_inv.oos_room + 1

                curr_recid = outorder._recid
                outorder = db_session.query(Outorder).filter(
                         (Outorder.gespende >= datum) & (Outorder.gespstart <= datum) & (Outorder.zinr != "") & (Outorder.betriebsnr >= 3)).filter(Outorder._recid > curr_recid).first()
    for i in range(0,2 + 1) :
        t_cardtype = T_cardtype()
        t_cardtype_list.append(t_cardtype)

        t_cardtype.number = i

        if i == 0:
            t_cardtype.bezeich = "Individual"

        elif i == 1:
            t_cardtype.bezeich = "Company"

        elif i == 2:
            t_cardtype.bezeich = "Travel Agent"
    success_flag = True

    return generate_output()