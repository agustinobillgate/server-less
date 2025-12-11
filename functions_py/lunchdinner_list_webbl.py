#using conversion tools version: 1.0.0.117

# ========================================================
# Rulita, 16-09-2025
# Issue : Fixing zimmeranz defaul int 1 
# ========================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Zimkateg, Res_line, Arrangement, Artikel, Argt_line, Reslin_queasy, Fixleist, Guest, Reservation, Segment, Ratecode, Mc_guest, Mc_types, Waehrung, Genstat, Bill, Master

def lunchdinner_list_webbl(v_key:int, fdate:date, incl_accom:bool, incl_guarantee:bool, show_lunchdinner_rate:bool):

    prepare_cache ([Htparam, Zimkateg, Arrangement, Artikel, Argt_line, Fixleist, Guest, Reservation, Segment, Ratecode, Mc_guest, Mc_types, Waehrung])

    lunchdinner_list_data = []
    mxtime_dayuse:int = 0
    param_561:string = ""
    diffcidate:int = 0
    p_87:date = None
    num_of_day:int = 0
    lunch_artnr:int = 0
    dinner_artnr:int = 0
    bfast_dept:int = 0
    exchg_rate:Decimal = 1
    qty_argt:int = 0
    htparam = zimkateg = res_line = arrangement = artikel = argt_line = reslin_queasy = fixleist = guest = reservation = segment = ratecode = mc_guest = mc_types = waehrung = genstat = bill = master = None

    lunchdinner_list = zikat_list = None

    lunchdinner_list_data, Lunchdinner_list = create_model("Lunchdinner_list", {"zinr":string, "name":string, "segmentcode":int, "ankunft":date, "anztage":int, "abreise":date, "kurzbez":string, "arrangement":string, "zimmeranz":int, "erwachs":int, "kind1":int, "gratis":int, "resnr":int, "bemerk":string, "gastnr":int, "resstatus":int, "resname":string, "address":string, "city":string, "comments":string, "datum":date, "nation1":string, "bezeich":string, "zipreis":Decimal, "code":string, "id":string, "bezeichnung":string, "mobil_telefon":string, "bfast_consume":int, "mcard_number":string, "mcard_type":string, "lunch_revenue":Decimal, "dinner_revenue":Decimal},
    default_values={
        "zimmeranz": 1
    })  # Rulita
    zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string}, {"selected": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lunchdinner_list_data, mxtime_dayuse, param_561, diffcidate, p_87, num_of_day, lunch_artnr, dinner_artnr, bfast_dept, exchg_rate, qty_argt, htparam, zimkateg, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, waehrung, genstat, bill, master
        nonlocal v_key, fdate, incl_accom, incl_guarantee, show_lunchdinner_rate


        nonlocal lunchdinner_list, zikat_list
        nonlocal lunchdinner_list_data, zikat_list_data

        return {"lunchdinner-list": lunchdinner_list_data}

    def create_lunch():

        nonlocal lunchdinner_list_data, mxtime_dayuse, param_561, diffcidate, p_87, num_of_day, lunch_artnr, dinner_artnr, bfast_dept, exchg_rate, qty_argt, htparam, zimkateg, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, waehrung, genstat, bill, master
        nonlocal v_key, fdate, incl_accom, incl_guarantee, show_lunchdinner_rate


        nonlocal lunchdinner_list, zikat_list
        nonlocal lunchdinner_list_data, zikat_list_data

        do_it:bool = False
        roflag:bool = False
        epreis:Decimal = to_decimal("0.0")
        qty:int = 0
        i:int = 0
        str:string = ""
        contcode:string = ""
        c:int = 0
        b:int = 0
        resline_remark:string = ""
        rsv_remark:string = ""
        dont_post:bool = False
        lunchdinner_list_data.clear()

        res_line_obj_list = {}
        for res_line in db_session.query(Res_line).filter(
                 ((Res_line.resstatus != 3) & (Res_line.resstatus != 2) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)) & (Res_line.active_flag == 1) & (Res_line.l_zuordnung[inc_value(2)] <= 1)).order_by(Res_line.zinr).all():
            zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            do_it = False
            roflag = True
            qty = 0
            num_of_day = 0
            epreis =  to_decimal("0")

            if incl_accom and res_line.l_zuordnung[2] == 1:
                do_it = False

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:

                    argt_line_obj_list = {}
                    argt_line = Argt_line()
                    artikel = Artikel()
                    for argt_line.betrag, argt_line.betriebsnr, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.betrag, Argt_line.betriebsnr, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == lunch_artnr)).filter(
                             (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        do_it = True
                        roflag = False
                        epreis =  to_decimal(argt_line.betrag)

                        if argt_line.vt_percnt == 0:

                            if argt_line.betriebsnr == 0:
                                qty_argt = res_line.erwachs
                            else:
                                qty_argt = argt_line.betriebsnr

                        elif argt_line.vt_percnt == 1:
                            qty_argt = res_line.kind1

                        elif argt_line.vt_percnt == 2:
                            qty_argt = res_line.kind2
                        break

            if res_line.l_zuordnung[2] == 0:

                if (res_line.erwachs + res_line.kind1 + res_line.gratis + res_line.l_zuordnung[3]) == 0:
                    pass
                else:

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    if arrangement:

                        argt_line_obj_list = {}
                        argt_line = Argt_line()
                        artikel = Artikel()
                        for argt_line.betrag, argt_line.betriebsnr, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.betrag, Argt_line.betriebsnr, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == lunch_artnr)).filter(
                                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                            if argt_line_obj_list.get(argt_line._recid):
                                continue
                            else:
                                argt_line_obj_list[argt_line._recid] = True


                            do_it = True
                            roflag = False
                            epreis =  to_decimal(argt_line.betrag)

                            if argt_line.vt_percnt == 0:

                                if argt_line.betriebsnr == 0:
                                    qty_argt = res_line.erwachs
                                else:
                                    qty_argt = argt_line.betriebsnr

                            elif argt_line.vt_percnt == 1:
                                qty_argt = res_line.kind1

                            elif argt_line.vt_percnt == 2:
                                qty_argt = res_line.kind2
                            break

            if do_it and epreis == 0:
                contcode = ""
                pass
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                        break

                if contcode != "":

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, lunch_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, res_line.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                    if not reslin_queasy:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"number1": [(eq, bfast_dept)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, lunch_artnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})
                do_it = None != reslin_queasy
                roflag = not do_it

                if do_it:
                    epreis =  to_decimal(reslin_queasy.deci1)

            if not do_it:

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr) & (Fixleist.artnr == lunch_artnr) & (Fixleist.departement == bfast_dept)).order_by(Fixleist._recid).all():
                    dont_post = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not dont_post:
                        do_it = True
                        qty = qty + fixleist.number

            if do_it:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                ratecode = get_cache (Ratecode, {"code": [(eq, res_line.arrangement)]})
                lunchdinner_list = Lunchdinner_list()
                lunchdinner_list_data.append(lunchdinner_list)


                if not roflag:
                    buffer_copy(res_line, lunchdinner_list)
                else:
                    buffer_copy(res_line, lunchdinner_list,except_fields=["erwachs","kind1","gratis"])
                    lunchdinner_list.erwachs = 0

                lunchdinner_list.zimmeranz = res_line.zimmeranz
                lunchdinner_list.segmentcode = reservation.segmentcode
                lunchdinner_list.kurzbez = zikat_list.kurzbez
                lunchdinner_list.erwachs = lunchdinner_list.erwachs + qty
                lunchdinner_list.gastnr = res_line.gastnr
                lunchdinner_list.resname = reservation.name
                lunchdinner_list.zipreis =  to_decimal(res_line.zipreis)
                lunchdinner_list.id = reservation.useridanlage

                if segment:
                    lunchdinner_list.bezeich = segment.bezeich
                rsv_remark = reservation.bemerk
                rsv_remark = replace_str(rsv_remark, chr_unicode(10) , "")
                rsv_remark = replace_str(rsv_remark, chr_unicode(13) , "")
                rsv_remark = replace_str(rsv_remark, "~n", "")
                rsv_remark = replace_str(rsv_remark, "\\n", "")
                rsv_remark = replace_str(rsv_remark, "~r", "")
                rsv_remark = replace_str(rsv_remark, "~r~n", "")
                rsv_remark = replace_str(rsv_remark, "&nbsp;", " ")
                rsv_remark = replace_str(rsv_remark, "</p>", "</p></p>")
                rsv_remark = replace_str(rsv_remark, "</p>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<BR>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<li>", "")
                rsv_remark = replace_str(rsv_remark, "</li>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<div>", "")
                rsv_remark = replace_str(rsv_remark, "</div>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, chr_unicode(10) + chr_unicode(13) , "")

                if length(rsv_remark) < 3:
                    rsv_remark = replace_str(rsv_remark, chr_unicode(32) , "")

                if length(rsv_remark) < 3:
                    rsv_remark = ""

                if rsv_remark == None:
                    rsv_remark = ""
                lunchdinner_list.comments = rsv_remark
                rsv_remark = ""
                resline_remark = res_line.bemerk
                resline_remark = replace_str(resline_remark, chr_unicode(10) , "")
                resline_remark = replace_str(resline_remark, chr_unicode(13) , "")
                resline_remark = replace_str(resline_remark, "~n", "")
                resline_remark = replace_str(resline_remark, "\\n", "")
                resline_remark = replace_str(resline_remark, "~r", "")
                resline_remark = replace_str(resline_remark, "~r~n", "")
                resline_remark = replace_str(resline_remark, "&nbsp;", " ")
                resline_remark = replace_str(resline_remark, "</p>", "</p></p>")
                resline_remark = replace_str(resline_remark, "</p>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<BR>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<li>", "")
                resline_remark = replace_str(resline_remark, "</li>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<div>", "")
                resline_remark = replace_str(resline_remark, "</div>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, chr_unicode(10) + chr_unicode(13) , "")

                if length(resline_remark) < 3:
                    resline_remark = replace_str(resline_remark, chr_unicode(32) , "")

                if length(resline_remark) < 3:
                    resline_remark = ""

                if resline_remark == None:
                    resline_remark = ""
                lunchdinner_list.bemerk = resline_remark

                if lunchdinner_list.comments != "":
                    lunchdinner_list.comments = lunchdinner_list.comments + chr_unicode(10)
                lunchdinner_list.comments = lunchdinner_list.comments + resline_remark
                resline_remark = ""

                if not roflag:
                    lunchdinner_list.kind1 = lunchdinner_list.kind1 + res_line.l_zuordnung[3]

                if ratecode:
                    lunchdinner_list.code = ratecode.code

                if guest:
                    lunchdinner_list.address = guest.adresse1
                    lunchdinner_list.city = guest.wohnort + " " + guest.plz
                    lunchdinner_list.nation1 = guest.nation1
                    lunchdinner_list.mobil_telefon = guest.mobil_telefon

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

                    if mc_guest:
                        lunchdinner_list.mcard_number = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            lunchdinner_list.mcard_type = mc_types.bezeich

                if res_line.resstatus == 11 and res_line.l_zuordnung[2] == 0:
                    lunchdinner_list.name = lunchdinner_list.name + " *"

                if res_line.resstatus == 11 and res_line.l_zuordnung[2] == 1:
                    lunchdinner_list.name = lunchdinner_list.name + " **"

                if res_line.resstatus == 13 and res_line.l_zuordnung[2] == 0:
                    lunchdinner_list.name = lunchdinner_list.name + " *"

                if res_line.resstatus == 13 and res_line.l_zuordnung[2] == 1:
                    lunchdinner_list.name = lunchdinner_list.name + " **"

                if show_lunchdinner_rate:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == lunch_artnr) & (Artikel.departement == bfast_dept) & (Artikel.betriebsnr != 0) & (Artikel.pricetab)).first()

                    if artikel:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                        if waehrung:
                            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                            lunchdinner_list.lunch_revenue =  to_decimal(epreis) * to_decimal(qty_argt) * to_decimal(exchg_rate)
                    else:
                        lunchdinner_list.lunch_revenue =  to_decimal(epreis) * to_decimal(qty_argt)
                else:
                    lunchdinner_list.lunch_revenue =  to_decimal("0")


    def create_lunch_guarantee():

        nonlocal lunchdinner_list_data, mxtime_dayuse, param_561, diffcidate, p_87, num_of_day, lunch_artnr, dinner_artnr, bfast_dept, exchg_rate, qty_argt, htparam, zimkateg, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, waehrung, genstat, bill, master
        nonlocal v_key, fdate, incl_accom, incl_guarantee, show_lunchdinner_rate


        nonlocal lunchdinner_list, zikat_list
        nonlocal lunchdinner_list_data, zikat_list_data

        do_it:bool = False
        roflag:bool = False
        epreis:Decimal = to_decimal("0.0")
        qty:int = 0
        i:int = 0
        str:string = ""
        contcode:string = ""
        c:int = 0
        b:int = 0
        resline_remark:string = ""
        rsv_remark:string = ""
        dont_post:bool = False
        lunchdinner_list_data.clear()

        res_line_obj_list = {}
        for res_line in db_session.query(Res_line).filter(
                 ((Res_line.resstatus != 3) & (Res_line.resstatus != 2) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)) & (Res_line.active_flag <= 1) & (Res_line.l_zuordnung[inc_value(2)] <= 1)).order_by(Res_line.zinr).all():
            zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            do_it = False
            roflag = True
            qty = 0
            num_of_day = 0
            epreis =  to_decimal("0")

            if incl_accom and res_line.l_zuordnung[2] == 1:
                do_it = False

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:

                    argt_line_obj_list = {}
                    argt_line = Argt_line()
                    artikel = Artikel()
                    for argt_line.betrag, argt_line.betriebsnr, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.betrag, Argt_line.betriebsnr, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == lunch_artnr)).filter(
                             (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        do_it = True
                        roflag = False
                        epreis =  to_decimal(argt_line.betrag)

                        if argt_line.vt_percnt == 0:

                            if argt_line.betriebsnr == 0:
                                qty_argt = res_line.erwachs
                            else:
                                qty_argt = argt_line.betriebsnr

                        elif argt_line.vt_percnt == 1:
                            qty_argt = res_line.kind1

                        elif argt_line.vt_percnt == 2:
                            qty_argt = res_line.kind2
                        break

            if res_line.l_zuordnung[2] == 0:

                if (res_line.erwachs + res_line.kind1 + res_line.gratis + res_line.l_zuordnung[3]) == 0:
                    pass
                else:

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    if arrangement:

                        argt_line_obj_list = {}
                        argt_line = Argt_line()
                        artikel = Artikel()
                        for argt_line.betrag, argt_line.betriebsnr, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.betrag, Argt_line.betriebsnr, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == lunch_artnr)).filter(
                                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                            if argt_line_obj_list.get(argt_line._recid):
                                continue
                            else:
                                argt_line_obj_list[argt_line._recid] = True


                            do_it = True
                            roflag = False
                            epreis =  to_decimal(argt_line.betrag)

                            if argt_line.vt_percnt == 0:

                                if argt_line.betriebsnr == 0:
                                    qty_argt = res_line.erwachs
                                else:
                                    qty_argt = argt_line.betriebsnr

                            elif argt_line.vt_percnt == 1:
                                qty_argt = res_line.kind1

                            elif argt_line.vt_percnt == 2:
                                qty_argt = res_line.kind2
                            break

            if do_it and epreis == 0:
                contcode = ""
                pass
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                        break

                if contcode != "":

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, lunch_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, res_line.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                    if not reslin_queasy:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"number1": [(eq, bfast_dept)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, lunch_artnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})
                do_it = None != reslin_queasy
                roflag = not do_it

                if do_it:
                    epreis =  to_decimal(reslin_queasy.deci1)

            if not do_it:

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr) & (Fixleist.artnr == lunch_artnr) & (Fixleist.departement == bfast_dept)).order_by(Fixleist._recid).all():
                    dont_post = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not dont_post:
                        do_it = True
                        qty = qty + fixleist.number

            if do_it:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                ratecode = get_cache (Ratecode, {"code": [(eq, res_line.arrangement)]})
                lunchdinner_list = Lunchdinner_list()
                lunchdinner_list_data.append(lunchdinner_list)


                if not roflag:
                    buffer_copy(res_line, lunchdinner_list)
                else:
                    buffer_copy(res_line, lunchdinner_list,except_fields=["erwachs","kind1","gratis"])
                    lunchdinner_list.erwachs = 0

                lunchdinner_list.zimmeranz = res_line.zimmeranz
                lunchdinner_list.segmentcode = reservation.segmentcode
                lunchdinner_list.kurzbez = zikat_list.kurzbez
                lunchdinner_list.erwachs = lunchdinner_list.erwachs + qty
                lunchdinner_list.gastnr = res_line.gastnr
                lunchdinner_list.resname = reservation.name
                lunchdinner_list.zipreis =  to_decimal(res_line.zipreis)
                lunchdinner_list.id = reservation.useridanlage

                if segment:
                    lunchdinner_list.bezeich = segment.bezeich
                rsv_remark = reservation.bemerk
                rsv_remark = replace_str(rsv_remark, chr_unicode(10) , "")
                rsv_remark = replace_str(rsv_remark, chr_unicode(13) , "")
                rsv_remark = replace_str(rsv_remark, "~n", "")
                rsv_remark = replace_str(rsv_remark, "\\n", "")
                rsv_remark = replace_str(rsv_remark, "~r", "")
                rsv_remark = replace_str(rsv_remark, "~r~n", "")
                rsv_remark = replace_str(rsv_remark, "&nbsp;", " ")
                rsv_remark = replace_str(rsv_remark, "</p>", "</p></p>")
                rsv_remark = replace_str(rsv_remark, "</p>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<BR>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<li>", "")
                rsv_remark = replace_str(rsv_remark, "</li>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<div>", "")
                rsv_remark = replace_str(rsv_remark, "</div>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, chr_unicode(10) + chr_unicode(13) , "")

                if length(rsv_remark) < 3:
                    rsv_remark = replace_str(rsv_remark, chr_unicode(32) , "")

                if length(rsv_remark) < 3:
                    rsv_remark = ""

                if rsv_remark == None:
                    rsv_remark = ""
                lunchdinner_list.comments = rsv_remark
                rsv_remark = ""
                resline_remark = res_line.bemerk
                resline_remark = replace_str(resline_remark, chr_unicode(10) , "")
                resline_remark = replace_str(resline_remark, chr_unicode(13) , "")
                resline_remark = replace_str(resline_remark, "~n", "")
                resline_remark = replace_str(resline_remark, "\\n", "")
                resline_remark = replace_str(resline_remark, "~r", "")
                resline_remark = replace_str(resline_remark, "~r~n", "")
                resline_remark = replace_str(resline_remark, "&nbsp;", " ")
                resline_remark = replace_str(resline_remark, "</p>", "</p></p>")
                resline_remark = replace_str(resline_remark, "</p>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<BR>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<li>", "")
                resline_remark = replace_str(resline_remark, "</li>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<div>", "")
                resline_remark = replace_str(resline_remark, "</div>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, chr_unicode(10) + chr_unicode(13) , "")

                if length(resline_remark) < 3:
                    resline_remark = replace_str(resline_remark, chr_unicode(32) , "")

                if length(resline_remark) < 3:
                    resline_remark = ""

                if resline_remark == None:
                    resline_remark = ""
                lunchdinner_list.bemerk = resline_remark

                if lunchdinner_list.comments != "":
                    lunchdinner_list.comments = lunchdinner_list.comments + chr_unicode(10)
                lunchdinner_list.comments = lunchdinner_list.comments + resline_remark
                resline_remark = ""

                if not roflag:
                    lunchdinner_list.kind1 = lunchdinner_list.kind1 + res_line.l_zuordnung[3]

                if ratecode:
                    lunchdinner_list.code = ratecode.code

                if guest:
                    lunchdinner_list.address = guest.adresse1
                    lunchdinner_list.city = guest.wohnort + " " + guest.plz
                    lunchdinner_list.nation1 = guest.nation1
                    lunchdinner_list.mobil_telefon = guest.mobil_telefon

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

                    if mc_guest:
                        lunchdinner_list.mcard_number = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            lunchdinner_list.mcard_type = mc_types.bezeich

                if res_line.resstatus == 11 and res_line.l_zuordnung[2] == 0:
                    lunchdinner_list.name = lunchdinner_list.name + " *"

                if res_line.resstatus == 11 and res_line.l_zuordnung[2] == 1:
                    lunchdinner_list.name = lunchdinner_list.name + " **"

                if res_line.resstatus == 13 and res_line.l_zuordnung[2] == 0:
                    lunchdinner_list.name = lunchdinner_list.name + " *"

                if res_line.resstatus == 13 and res_line.l_zuordnung[2] == 1:
                    lunchdinner_list.name = lunchdinner_list.name + " **"

                if show_lunchdinner_rate:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == lunch_artnr) & (Artikel.departement == bfast_dept) & (Artikel.betriebsnr != 0) & (Artikel.pricetab)).first()

                    if artikel:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                        if waehrung:
                            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                            lunchdinner_list.lunch_revenue =  to_decimal(epreis) * to_decimal(qty_argt) * to_decimal(exchg_rate)
                    else:
                        lunchdinner_list.lunch_revenue =  to_decimal(epreis) * to_decimal(qty_argt)
                else:
                    lunchdinner_list.lunch_revenue =  to_decimal("0")


    def create_dinner():

        nonlocal lunchdinner_list_data, mxtime_dayuse, param_561, diffcidate, p_87, num_of_day, lunch_artnr, dinner_artnr, bfast_dept, exchg_rate, qty_argt, htparam, zimkateg, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, waehrung, genstat, bill, master
        nonlocal v_key, fdate, incl_accom, incl_guarantee, show_lunchdinner_rate


        nonlocal lunchdinner_list, zikat_list
        nonlocal lunchdinner_list_data, zikat_list_data

        do_it:bool = False
        roflag:bool = False
        epreis:Decimal = to_decimal("0.0")
        qty:int = 0
        i:int = 0
        str:string = ""
        contcode:string = ""
        c:int = 0
        b:int = 0
        resline_remark:string = ""
        rsv_remark:string = ""
        dont_post:bool = False
        lunchdinner_list_data.clear()

        res_line_obj_list = {}
        for res_line in db_session.query(Res_line).filter(
                 ((Res_line.resstatus != 3) & (Res_line.resstatus != 2) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)) & (Res_line.active_flag == 1) & (Res_line.l_zuordnung[inc_value(2)] <= 1)).order_by(Res_line.zinr).all():
            zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            do_it = False
            roflag = True
            qty = 0
            num_of_day = 0
            epreis =  to_decimal("0")

            if incl_accom and res_line.l_zuordnung[2] == 1:
                do_it = False

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:

                    argt_line_obj_list = {}
                    argt_line = Argt_line()
                    artikel = Artikel()
                    for argt_line.betrag, argt_line.betriebsnr, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.betrag, Argt_line.betriebsnr, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == dinner_artnr)).filter(
                             (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        do_it = True
                        roflag = False
                        epreis =  to_decimal(argt_line.betrag)

                        if argt_line.vt_percnt == 0:

                            if argt_line.betriebsnr == 0:
                                qty_argt = res_line.erwachs
                            else:
                                qty_argt = argt_line.betriebsnr

                        elif argt_line.vt_percnt == 1:
                            qty_argt = res_line.kind1

                        elif argt_line.vt_percnt == 2:
                            qty_argt = res_line.kind2
                        break

            if res_line.l_zuordnung[2] == 0:

                if (res_line.erwachs + res_line.kind1 + res_line.gratis + res_line.l_zuordnung[3]) == 0:
                    pass
                else:

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    if arrangement:

                        argt_line_obj_list = {}
                        argt_line = Argt_line()
                        artikel = Artikel()
                        for argt_line.betrag, argt_line.betriebsnr, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.betrag, Argt_line.betriebsnr, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == dinner_artnr)).filter(
                                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                            if argt_line_obj_list.get(argt_line._recid):
                                continue
                            else:
                                argt_line_obj_list[argt_line._recid] = True


                            do_it = True
                            roflag = False
                            epreis =  to_decimal(argt_line.betrag)

                            if argt_line.vt_percnt == 0:

                                if argt_line.betriebsnr == 0:
                                    qty_argt = res_line.erwachs
                                else:
                                    qty_argt = argt_line.betriebsnr

                            elif argt_line.vt_percnt == 1:
                                qty_argt = res_line.kind1

                            elif argt_line.vt_percnt == 2:
                                qty_argt = res_line.kind2
                            break

            if do_it and epreis == 0:
                contcode = ""
                pass
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                        break

                if contcode != "":

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, dinner_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, res_line.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                    if not reslin_queasy:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"number1": [(eq, bfast_dept)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, dinner_artnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})
                do_it = None != reslin_queasy
                roflag = not do_it

                if do_it:
                    epreis =  to_decimal(reslin_queasy.deci1)

            if not do_it:

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr) & (Fixleist.artnr == dinner_artnr) & (Fixleist.departement == bfast_dept)).order_by(Fixleist._recid).all():
                    dont_post = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not dont_post:
                        do_it = True
                        qty = qty + fixleist.number

            if do_it:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                ratecode = get_cache (Ratecode, {"code": [(eq, res_line.arrangement)]})
                lunchdinner_list = Lunchdinner_list()
                lunchdinner_list_data.append(lunchdinner_list)


                if not roflag:
                    buffer_copy(res_line, lunchdinner_list)
                else:
                    buffer_copy(res_line, lunchdinner_list,except_fields=["erwachs","kind1","gratis"])
                    lunchdinner_list.erwachs = 0

                lunchdinner_list.zimmeranz = res_line.zimmeranz
                lunchdinner_list.segmentcode = reservation.segmentcode
                lunchdinner_list.kurzbez = zikat_list.kurzbez
                lunchdinner_list.erwachs = lunchdinner_list.erwachs + qty
                lunchdinner_list.gastnr = res_line.gastnr
                lunchdinner_list.resname = reservation.name
                lunchdinner_list.zipreis =  to_decimal(res_line.zipreis)
                lunchdinner_list.id = reservation.useridanlage

                if segment:
                    lunchdinner_list.bezeich = segment.bezeich
                rsv_remark = reservation.bemerk
                rsv_remark = replace_str(rsv_remark, chr_unicode(10) , "")
                rsv_remark = replace_str(rsv_remark, chr_unicode(13) , "")
                rsv_remark = replace_str(rsv_remark, "~n", "")
                rsv_remark = replace_str(rsv_remark, "\\n", "")
                rsv_remark = replace_str(rsv_remark, "~r", "")
                rsv_remark = replace_str(rsv_remark, "~r~n", "")
                rsv_remark = replace_str(rsv_remark, "&nbsp;", " ")
                rsv_remark = replace_str(rsv_remark, "</p>", "</p></p>")
                rsv_remark = replace_str(rsv_remark, "</p>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<BR>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<li>", "")
                rsv_remark = replace_str(rsv_remark, "</li>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<div>", "")
                rsv_remark = replace_str(rsv_remark, "</div>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, chr_unicode(10) + chr_unicode(13) , "")

                if length(rsv_remark) < 3:
                    rsv_remark = replace_str(rsv_remark, chr_unicode(32) , "")

                if length(rsv_remark) < 3:
                    rsv_remark = ""

                if rsv_remark == None:
                    rsv_remark = ""
                lunchdinner_list.comments = rsv_remark
                rsv_remark = ""
                resline_remark = res_line.bemerk
                resline_remark = replace_str(resline_remark, chr_unicode(10) , "")
                resline_remark = replace_str(resline_remark, chr_unicode(13) , "")
                resline_remark = replace_str(resline_remark, "~n", "")
                resline_remark = replace_str(resline_remark, "\\n", "")
                resline_remark = replace_str(resline_remark, "~r", "")
                resline_remark = replace_str(resline_remark, "~r~n", "")
                resline_remark = replace_str(resline_remark, "&nbsp;", " ")
                resline_remark = replace_str(resline_remark, "</p>", "</p></p>")
                resline_remark = replace_str(resline_remark, "</p>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<BR>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<li>", "")
                resline_remark = replace_str(resline_remark, "</li>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<div>", "")
                resline_remark = replace_str(resline_remark, "</div>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, chr_unicode(10) + chr_unicode(13) , "")

                if length(resline_remark) < 3:
                    resline_remark = replace_str(resline_remark, chr_unicode(32) , "")

                if length(resline_remark) < 3:
                    resline_remark = ""

                if resline_remark == None:
                    resline_remark = ""
                lunchdinner_list.bemerk = resline_remark

                if lunchdinner_list.comments != "":
                    lunchdinner_list.comments = lunchdinner_list.comments + chr_unicode(10)
                lunchdinner_list.comments = lunchdinner_list.comments + resline_remark
                resline_remark = ""

                if not roflag:
                    lunchdinner_list.kind1 = lunchdinner_list.kind1 + res_line.l_zuordnung[3]

                if ratecode:
                    lunchdinner_list.code = ratecode.code

                if guest:
                    lunchdinner_list.address = guest.adresse1
                    lunchdinner_list.city = guest.wohnort + " " + guest.plz
                    lunchdinner_list.nation1 = guest.nation1
                    lunchdinner_list.mobil_telefon = guest.mobil_telefon

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

                    if mc_guest:
                        lunchdinner_list.mcard_number = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            lunchdinner_list.mcard_type = mc_types.bezeich

                if res_line.resstatus == 11 and res_line.l_zuordnung[2] == 0:
                    lunchdinner_list.name = lunchdinner_list.name + " *"

                if res_line.resstatus == 11 and res_line.l_zuordnung[2] == 1:
                    lunchdinner_list.name = lunchdinner_list.name + " **"

                if res_line.resstatus == 13 and res_line.l_zuordnung[2] == 0:
                    lunchdinner_list.name = lunchdinner_list.name + " *"

                if res_line.resstatus == 13 and res_line.l_zuordnung[2] == 1:
                    lunchdinner_list.name = lunchdinner_list.name + " **"

                if show_lunchdinner_rate:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == dinner_artnr) & (Artikel.departement == bfast_dept) & (Artikel.betriebsnr != 0) & (Artikel.pricetab)).first()

                    if artikel:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                        if waehrung:
                            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                            lunchdinner_list.dinner_revenue =  to_decimal(epreis) * to_decimal(qty_argt) * to_decimal(exchg_rate)
                    else:
                        lunchdinner_list.dinner_revenue =  to_decimal(epreis) * to_decimal(qty_argt)
                else:
                    lunchdinner_list.dinner_revenue =  to_decimal("0")


    def create_dinner_guarantee():

        nonlocal lunchdinner_list_data, mxtime_dayuse, param_561, diffcidate, p_87, num_of_day, lunch_artnr, dinner_artnr, bfast_dept, exchg_rate, qty_argt, htparam, zimkateg, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, waehrung, genstat, bill, master
        nonlocal v_key, fdate, incl_accom, incl_guarantee, show_lunchdinner_rate


        nonlocal lunchdinner_list, zikat_list
        nonlocal lunchdinner_list_data, zikat_list_data

        do_it:bool = False
        roflag:bool = False
        epreis:Decimal = to_decimal("0.0")
        qty:int = 0
        i:int = 0
        str:string = ""
        contcode:string = ""
        c:int = 0
        b:int = 0
        resline_remark:string = ""
        rsv_remark:string = ""
        dont_post:bool = False
        lunchdinner_list_data.clear()

        res_line_obj_list = {}
        for res_line in db_session.query(Res_line).filter(
                 ((Res_line.resstatus != 3) & (Res_line.resstatus != 2) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)) & (Res_line.active_flag <= 1) & (Res_line.l_zuordnung[inc_value(2)] <= 1)).order_by(Res_line.zinr).all():
            zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            do_it = False
            roflag = True
            qty = 0
            num_of_day = 0
            epreis =  to_decimal("0")

            if incl_accom and res_line.l_zuordnung[2] == 1:
                do_it = False

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:

                    argt_line_obj_list = {}
                    argt_line = Argt_line()
                    artikel = Artikel()
                    for argt_line.betrag, argt_line.betriebsnr, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.betrag, Argt_line.betriebsnr, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == dinner_artnr)).filter(
                             (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        do_it = True
                        roflag = False
                        epreis =  to_decimal(argt_line.betrag)

                        if argt_line.vt_percnt == 0:

                            if argt_line.betriebsnr == 0:
                                qty_argt = res_line.erwachs
                            else:
                                qty_argt = argt_line.betriebsnr

                        elif argt_line.vt_percnt == 1:
                            qty_argt = res_line.kind1

                        elif argt_line.vt_percnt == 2:
                            qty_argt = res_line.kind2
                        break

            if res_line.l_zuordnung[2] == 0:

                if (res_line.erwachs + res_line.kind1 + res_line.gratis + res_line.l_zuordnung[3]) == 0:
                    pass
                else:

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    if arrangement:

                        argt_line_obj_list = {}
                        argt_line = Argt_line()
                        artikel = Artikel()
                        for argt_line.betrag, argt_line.betriebsnr, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.betrag, Argt_line.betriebsnr, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == dinner_artnr)).filter(
                                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                            if argt_line_obj_list.get(argt_line._recid):
                                continue
                            else:
                                argt_line_obj_list[argt_line._recid] = True


                            do_it = True
                            roflag = False
                            epreis =  to_decimal(argt_line.betrag)

                            if argt_line.vt_percnt == 0:

                                if argt_line.betriebsnr == 0:
                                    qty_argt = res_line.erwachs
                                else:
                                    qty_argt = argt_line.betriebsnr

                            elif argt_line.vt_percnt == 1:
                                qty_argt = res_line.kind1

                            elif argt_line.vt_percnt == 2:
                                qty_argt = res_line.kind2
                            break

            if do_it and epreis == 0:
                contcode = ""
                pass
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                        break

                if contcode != "":

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, dinner_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, res_line.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                    if not reslin_queasy:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"number1": [(eq, bfast_dept)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, dinner_artnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})
                do_it = None != reslin_queasy
                roflag = not do_it

                if do_it:
                    epreis =  to_decimal(reslin_queasy.deci1)

            if not do_it:

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr) & (Fixleist.artnr == dinner_artnr) & (Fixleist.departement == bfast_dept)).order_by(Fixleist._recid).all():
                    dont_post = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not dont_post:
                        do_it = True
                        qty = qty + fixleist.number

            if do_it:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                ratecode = get_cache (Ratecode, {"code": [(eq, res_line.arrangement)]})
                lunchdinner_list = Lunchdinner_list()
                lunchdinner_list_data.append(lunchdinner_list)


                if not roflag:
                    buffer_copy(res_line, lunchdinner_list)
                else:
                    buffer_copy(res_line, lunchdinner_list,except_fields=["erwachs","kind1","gratis"])
                    lunchdinner_list.erwachs = 0

                lunchdinner_list.zimmeranz = res_line.zimmeranz
                lunchdinner_list.segmentcode = reservation.segmentcode
                lunchdinner_list.kurzbez = zikat_list.kurzbez
                lunchdinner_list.erwachs = lunchdinner_list.erwachs + qty
                lunchdinner_list.gastnr = res_line.gastnr
                lunchdinner_list.resname = reservation.name
                lunchdinner_list.zipreis =  to_decimal(res_line.zipreis)
                lunchdinner_list.id = reservation.useridanlage

                if segment:
                    lunchdinner_list.bezeich = segment.bezeich
                rsv_remark = reservation.bemerk
                rsv_remark = replace_str(rsv_remark, chr_unicode(10) , "")
                rsv_remark = replace_str(rsv_remark, chr_unicode(13) , "")
                rsv_remark = replace_str(rsv_remark, "~n", "")
                rsv_remark = replace_str(rsv_remark, "\\n", "")
                rsv_remark = replace_str(rsv_remark, "~r", "")
                rsv_remark = replace_str(rsv_remark, "~r~n", "")
                rsv_remark = replace_str(rsv_remark, "&nbsp;", " ")
                rsv_remark = replace_str(rsv_remark, "</p>", "</p></p>")
                rsv_remark = replace_str(rsv_remark, "</p>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<BR>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<li>", "")
                rsv_remark = replace_str(rsv_remark, "</li>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, "<div>", "")
                rsv_remark = replace_str(rsv_remark, "</div>", chr_unicode(13))
                rsv_remark = replace_str(rsv_remark, chr_unicode(10) + chr_unicode(13) , "")

                if length(rsv_remark) < 3:
                    rsv_remark = replace_str(rsv_remark, chr_unicode(32) , "")

                if length(rsv_remark) < 3:
                    rsv_remark = ""

                if rsv_remark == None:
                    rsv_remark = ""
                lunchdinner_list.comments = rsv_remark
                rsv_remark = ""
                resline_remark = res_line.bemerk
                resline_remark = replace_str(resline_remark, chr_unicode(10) , "")
                resline_remark = replace_str(resline_remark, chr_unicode(13) , "")
                resline_remark = replace_str(resline_remark, "~n", "")
                resline_remark = replace_str(resline_remark, "\\n", "")
                resline_remark = replace_str(resline_remark, "~r", "")
                resline_remark = replace_str(resline_remark, "~r~n", "")
                resline_remark = replace_str(resline_remark, "&nbsp;", " ")
                resline_remark = replace_str(resline_remark, "</p>", "</p></p>")
                resline_remark = replace_str(resline_remark, "</p>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<BR>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<li>", "")
                resline_remark = replace_str(resline_remark, "</li>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, "<div>", "")
                resline_remark = replace_str(resline_remark, "</div>", chr_unicode(13))
                resline_remark = replace_str(resline_remark, chr_unicode(10) + chr_unicode(13) , "")

                if length(resline_remark) < 3:
                    resline_remark = replace_str(resline_remark, chr_unicode(32) , "")

                if length(resline_remark) < 3:
                    resline_remark = ""

                if resline_remark == None:
                    resline_remark = ""
                lunchdinner_list.bemerk = resline_remark

                if lunchdinner_list.comments != "":
                    lunchdinner_list.comments = lunchdinner_list.comments + chr_unicode(10)
                lunchdinner_list.comments = lunchdinner_list.comments + resline_remark
                resline_remark = ""

                if not roflag:
                    lunchdinner_list.kind1 = lunchdinner_list.kind1 + res_line.l_zuordnung[3]

                if ratecode:
                    lunchdinner_list.code = ratecode.code

                if guest:
                    lunchdinner_list.address = guest.adresse1
                    lunchdinner_list.city = guest.wohnort + " " + guest.plz
                    lunchdinner_list.nation1 = guest.nation1
                    lunchdinner_list.mobil_telefon = guest.mobil_telefon

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

                    if mc_guest:
                        lunchdinner_list.mcard_number = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            lunchdinner_list.mcard_type = mc_types.bezeich

                if res_line.resstatus == 11 and res_line.l_zuordnung[2] == 0:
                    lunchdinner_list.name = lunchdinner_list.name + " *"

                if res_line.resstatus == 11 and res_line.l_zuordnung[2] == 1:
                    lunchdinner_list.name = lunchdinner_list.name + " **"

                if res_line.resstatus == 13 and res_line.l_zuordnung[2] == 0:
                    lunchdinner_list.name = lunchdinner_list.name + " *"

                if res_line.resstatus == 13 and res_line.l_zuordnung[2] == 1:
                    lunchdinner_list.name = lunchdinner_list.name + " **"

                if show_lunchdinner_rate:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == dinner_artnr) & (Artikel.departement == bfast_dept) & (Artikel.betriebsnr != 0) & (Artikel.pricetab)).first()

                    if artikel:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                        if waehrung:
                            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                            lunchdinner_list.dinner_revenue =  to_decimal(epreis) * to_decimal(qty_argt) * to_decimal(exchg_rate)
                    else:
                        lunchdinner_list.dinner_revenue =  to_decimal(epreis) * to_decimal(qty_argt)
                else:
                    lunchdinner_list.dinner_revenue =  to_decimal("0")


    def create_statlunch():

        nonlocal lunchdinner_list_data, mxtime_dayuse, param_561, diffcidate, p_87, num_of_day, lunch_artnr, dinner_artnr, bfast_dept, exchg_rate, qty_argt, htparam, zimkateg, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, waehrung, genstat, bill, master
        nonlocal v_key, fdate, incl_accom, incl_guarantee, show_lunchdinner_rate


        nonlocal lunchdinner_list, zikat_list
        nonlocal lunchdinner_list_data, zikat_list_data

        do_it:bool = False
        roflag:bool = False
        epreis:Decimal = to_decimal("0.0")
        qty:int = 0
        i:int = 0
        str:string = ""
        contcode:string = ""
        rline = None
        dont_post:bool = False
        Rline =  create_buffer("Rline",Res_line)
        lunchdinner_list_data.clear()

        genstat_obj_list = {}
        for genstat, res_line in db_session.query(Genstat, Res_line).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).filter(
                 ((Genstat.resstatus != 3) & (Genstat.resstatus != 4) & (Genstat.resstatus != 8) & (Genstat.resstatus != 9) & (Genstat.resstatus != 10) & (Genstat.resstatus != 12)) & (Genstat.datum == fdate)).order_by(Genstat.zinr).all():
            zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = False
            roflag = True
            qty = 0
            epreis =  to_decimal("0")

            if (genstat.erwachs + genstat.kind1 + genstat.gratis + genstat.kind3) == 0:
                pass
            else:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                if arrangement:

                    argt_line_obj_list = {}
                    argt_line = Argt_line()
                    artikel = Artikel()
                    for argt_line.betrag, argt_line.betriebsnr, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.betrag, Argt_line.betriebsnr, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == lunch_artnr)).filter(
                             (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        do_it = True
                        roflag = False
                        epreis =  to_decimal(argt_line.betrag)

                        if argt_line.vt_percnt == 0:

                            if argt_line.betriebsnr == 0:
                                qty_argt = genstat.erwachs
                            else:
                                qty_argt = argt_line.betriebsnr

                        elif argt_line.vt_percnt == 1:
                            qty_argt = genstat.kind1

                        elif argt_line.vt_percnt == 2:
                            qty_argt = genstat.kind2
                        break

            if do_it and epreis == 0:
                contcode = ""
                pass
                for i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                    str = entry(i - 1, genstat.res_char[1], ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                        break

                if contcode != "":

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, genstat.res_int[1])],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, lunch_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, genstat.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                    if not reslin_queasy:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"number1": [(eq, bfast_dept)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, lunch_artnr)],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})
                do_it = None != reslin_queasy
                roflag = not do_it

                if do_it:
                    epreis =  to_decimal(reslin_queasy.deci1)

            if not do_it:

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == genstat.resnr) & (Fixleist.reslinnr == genstat.res_int[0]) & (Fixleist.artnr == lunch_artnr) & (Fixleist.departement == bfast_dept)).order_by(Fixleist._recid).all():
                    dont_post = check_fixleist_posted1(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not dont_post:
                        do_it = True
                        qty = qty + fixleist.number

            if do_it:

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                ratecode = get_cache (Ratecode, {"code": [(eq, genstat.argt)]})
                lunchdinner_list = Lunchdinner_list()
                lunchdinner_list_data.append(lunchdinner_list)


                if not roflag:
                    buffer_copy(genstat, lunchdinner_list)
                else:
                    buffer_copy(genstat, lunchdinner_list,except_fields=["erwachs","kind1","gratis","datum"])
                    lunchdinner_list.erwachs = 0


                lunchdinner_list.datum = genstat.datum
                lunchdinner_list.datum = genstat.datum
                lunchdinner_list.segmentcode = reservation.segmentcode
                lunchdinner_list.kurzbez = zikat_list.kurzbez
                lunchdinner_list.erwachs = lunchdinner_list.erwachs + qty
                lunchdinner_list.gastnr = genstat.gastnr
                lunchdinner_list.resname = reservation.name
                lunchdinner_list.comments = reservation.bemerk
                lunchdinner_list.bezeich = segment.bezeich
                lunchdinner_list.zipreis =  to_decimal(genstat.zipreis)
                lunchdinner_list.ankunft = genstat.res_date[0]
                lunchdinner_list.abreise = genstat.res_date[1]
                lunchdinner_list.arrangement = genstat.argt
                lunchdinner_list.id = reservation.useridanlage

                if lunchdinner_list.comments != "":
                    lunchdinner_list.comments = lunchdinner_list.comments + chr_unicode(10)

                rline = db_session.query(Rline).filter(
                         (Rline.resnr == genstat.resnr) & (Rline.reslinnr == genstat.res_int[0])).first()

                if rline:
                    lunchdinner_list.bemerk = lunchdinner_list.comments + rline.bemerk

                if lunchdinner_list.comments != "":
                    lunchdinner_list.comments = lunchdinner_list.comments + chr_unicode(10)

                if not roflag:
                    lunchdinner_list.kind1 = lunchdinner_list.kind1 + genstat.kind3

                if ratecode:
                    lunchdinner_list.code = ratecode.code

                if guest:
                    lunchdinner_list.address = guest.adresse1
                    lunchdinner_list.city = guest.wohnort + " " + guest.plz
                    lunchdinner_list.name = guest.name
                    lunchdinner_list.comments = lunchdinner_list.comments + guest.bemerkung
                    lunchdinner_list.nation1 = guest.nation1
                    lunchdinner_list.mobil_telefon = guest.mobil_telefon

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

                    if mc_guest:
                        lunchdinner_list.mcard_number = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            lunchdinner_list.mcard_type = mc_types.bezeich

                if show_lunchdinner_rate:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == lunch_artnr) & (Artikel.departement == bfast_dept) & (Artikel.betriebsnr != 0) & (Artikel.pricetab)).first()

                    if artikel:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                        if waehrung:
                            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                            lunchdinner_list.lunch_revenue =  to_decimal(epreis) * to_decimal(qty_argt) * to_decimal(exchg_rate)
                    else:
                        lunchdinner_list.lunch_revenue =  to_decimal(epreis) * to_decimal(qty_argt)
                else:
                    lunchdinner_list.lunch_revenue =  to_decimal("0")


    def create_statdinner():

        nonlocal lunchdinner_list_data, mxtime_dayuse, param_561, diffcidate, p_87, num_of_day, lunch_artnr, dinner_artnr, bfast_dept, exchg_rate, qty_argt, htparam, zimkateg, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, waehrung, genstat, bill, master
        nonlocal v_key, fdate, incl_accom, incl_guarantee, show_lunchdinner_rate


        nonlocal lunchdinner_list, zikat_list
        nonlocal lunchdinner_list_data, zikat_list_data

        do_it:bool = False
        roflag:bool = False
        epreis:Decimal = to_decimal("0.0")
        qty:int = 0
        i:int = 0
        str:string = ""
        contcode:string = ""
        rline = None
        dont_post:bool = False
        Rline =  create_buffer("Rline",Res_line)
        lunchdinner_list_data.clear()

        genstat_obj_list = {}
        for genstat, res_line in db_session.query(Genstat, Res_line).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).filter(
                 ((Genstat.resstatus != 3) & (Genstat.resstatus != 4) & (Genstat.resstatus != 8) & (Genstat.resstatus != 9) & (Genstat.resstatus != 10) & (Genstat.resstatus != 12)) & (Genstat.datum == fdate)).order_by(Genstat.zinr).all():
            zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = False
            roflag = True
            qty = 0
            epreis =  to_decimal("0")

            if (genstat.erwachs + genstat.kind1 + genstat.gratis + genstat.kind3) == 0:
                pass
            else:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                if arrangement:

                    argt_line_obj_list = {}
                    argt_line = Argt_line()
                    artikel = Artikel()
                    for argt_line.betrag, argt_line.betriebsnr, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.betrag, Argt_line.betriebsnr, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == dinner_artnr)).filter(
                             (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        do_it = True
                        roflag = False
                        epreis =  to_decimal(argt_line.betrag)

                        if argt_line.vt_percnt == 0:

                            if argt_line.betriebsnr == 0:
                                qty_argt = genstat.erwachs
                            else:
                                qty_argt = argt_line.betriebsnr

                        elif argt_line.vt_percnt == 1:
                            qty_argt = genstat.kind1

                        elif argt_line.vt_percnt == 2:
                            qty_argt = genstat.kind2
                        break

            if do_it and epreis == 0:
                contcode = ""
                pass
                for i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                    str = entry(i - 1, genstat.res_char[1], ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                        break

                if contcode != "":

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, genstat.res_int[1])],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, dinner_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, genstat.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                    if not reslin_queasy:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"number1": [(eq, bfast_dept)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, dinner_artnr)],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})
                do_it = None != reslin_queasy
                roflag = not do_it

                if do_it:
                    epreis =  to_decimal(reslin_queasy.deci1)

            if not do_it:

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == genstat.resnr) & (Fixleist.reslinnr == genstat.res_int[0]) & (Fixleist.artnr == dinner_artnr) & (Fixleist.departement == bfast_dept)).order_by(Fixleist._recid).all():
                    dont_post = check_fixleist_posted1(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not dont_post:
                        do_it = True
                        qty = qty + fixleist.number

            if do_it:

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                ratecode = get_cache (Ratecode, {"code": [(eq, genstat.argt)]})
                lunchdinner_list = Lunchdinner_list()
                lunchdinner_list_data.append(lunchdinner_list)


                if not roflag:
                    buffer_copy(genstat, lunchdinner_list)
                else:
                    buffer_copy(genstat, lunchdinner_list,except_fields=["erwachs","kind1","gratis","datum"])
                    lunchdinner_list.erwachs = 0


                lunchdinner_list.datum = genstat.datum
                lunchdinner_list.segmentcode = reservation.segmentcode
                lunchdinner_list.kurzbez = zikat_list.kurzbez
                lunchdinner_list.erwachs = lunchdinner_list.erwachs + qty
                lunchdinner_list.gastnr = genstat.gastnr
                lunchdinner_list.resname = reservation.name
                lunchdinner_list.comments = reservation.bemerk
                lunchdinner_list.bezeich = segment.bezeich
                lunchdinner_list.zipreis =  to_decimal(genstat.zipreis)
                lunchdinner_list.ankunft = genstat.res_date[0]
                lunchdinner_list.abreise = genstat.res_date[1]
                lunchdinner_list.arrangement = genstat.argt
                lunchdinner_list.id = reservation.useridanlage

                if lunchdinner_list.comments != "":
                    lunchdinner_list.comments = lunchdinner_list.comments + chr_unicode(10)

                rline = db_session.query(Rline).filter(
                         (Rline.resnr == genstat.resnr) & (Rline.reslinnr == genstat.res_int[0])).first()

                if rline:
                    lunchdinner_list.bemerk = lunchdinner_list.comments + rline.bemerk

                if lunchdinner_list.comments != "":
                    lunchdinner_list.comments = lunchdinner_list.comments + chr_unicode(10)

                if not roflag:
                    lunchdinner_list.kind1 = lunchdinner_list.kind1 + genstat.kind3

                if ratecode:
                    lunchdinner_list.code = ratecode.code

                if guest:
                    lunchdinner_list.address = guest.adresse1
                    lunchdinner_list.city = guest.wohnort + " " + guest.plz
                    lunchdinner_list.name = guest.name
                    lunchdinner_list.comments = lunchdinner_list.comments + guest.bemerkung
                    lunchdinner_list.nation1 = guest.nation1
                    lunchdinner_list.mobil_telefon = guest.mobil_telefon

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

                    if mc_guest:
                        lunchdinner_list.mcard_number = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            lunchdinner_list.mcard_type = mc_types.bezeich

                if show_lunchdinner_rate:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == dinner_artnr) & (Artikel.departement == bfast_dept) & (Artikel.betriebsnr != 0) & (Artikel.pricetab)).first()

                    if artikel:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                        if waehrung:
                            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                            lunchdinner_list.dinner_revenue =  to_decimal(epreis) * to_decimal(qty_argt) * to_decimal(exchg_rate)
                    else:
                        lunchdinner_list.dinner_revenue =  to_decimal(epreis) * to_decimal(qty_argt)
                else:
                    lunchdinner_list.dinner_revenue =  to_decimal("0")


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal lunchdinner_list_data, mxtime_dayuse, param_561, diffcidate, p_87, num_of_day, lunch_artnr, dinner_artnr, bfast_dept, exchg_rate, qty_argt, htparam, zimkateg, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, waehrung, genstat, bill, master
        nonlocal v_key, fdate, incl_accom, incl_guarantee, show_lunchdinner_rate


        nonlocal lunchdinner_list, zikat_list
        nonlocal lunchdinner_list_data, zikat_list_data

        dont_post = False
        master_flag:bool = False
        delta:int = 0
        start_date:date = None
        invoice = None

        def generate_inner_output():
            return (dont_post)

        Invoice =  create_buffer("Invoice",Bill)

        master = get_cache (Master, {"resnr": [(eq, res_line.resnr)],"active": [(eq, True)],"flag": [(eq, 0)]})

        if master and master.umsatzart[1] :
            master_flag = True

        if master_flag:

            invoice = db_session.query(Invoice).filter(
                     (Invoice.resnr == res_line.resnr) & (Invoice.reslinnr == 0)).first()
        else:

            invoice = db_session.query(Invoice).filter(
                     (Invoice.zinr == res_line.zinr) & (Invoice.resnr == res_line.resnr) & (Invoice.reslinnr == res_line.reslinnr) & (Invoice.billtyp == 0) & (Invoice.billnr == 1) & (Invoice.flag == 0)).first()

        if not dont_post:

            if fakt_modus == 2:

                if res_line.ankunft != fdate:
                    dont_post = True

            elif fakt_modus == 3:

                if (res_line.ankunft + 1) != fdate:
                    dont_post = True

            elif fakt_modus == 4:

                if get_day(fdate) != 1:
                    dont_post = True

            elif fakt_modus == 5:

                if get_day(fdate + 1) != 1:
                    dont_post = True

            elif fakt_modus == 6:

                if lfakt == None:
                    delta = 0
                else:
                    delta = (lfakt - res_line.ankunft).days

                    if delta < 0:
                        delta = 0
                start_date = res_line.ankunft + timedelta(days=delta)

                if (res_line.abreise - start_date) < intervall:
                    start_date = res_line.ankunft

                if fdate > (start_date + timedelta(days=(intervall - 1))):
                    dont_post = True

                if fdate < start_date:
                    dont_post = True

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 561)]})

    if htparam:
        param_561 = trim(htparam.fchar)

    if param_561 != "":
        mxtime_dayuse = to_int(substring(param_561, 0, 2)) * 3600 + to_int(substring(param_561, 3, 2)) * 60

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        p_87 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})

    if htparam:
        lunch_artnr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})

    if htparam:
        dinner_artnr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 126)]})

    if htparam:
        bfast_dept = htparam.finteger

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.kurzbez).all():
        zikat_list = Zikat_list()
        zikat_list_data.append(zikat_list)

        zikat_list.zikatnr = zimkateg.zikatnr
        zikat_list.kurzbez = zimkateg.kurzbez
        zikat_list.bezeich = zimkateg.bezeichnung

    if fdate >= p_87:

        if v_key == 1:
            if not incl_guarantee:
                create_lunch()
            else:
                create_lunch_guarantee()
        
        elif v_key == 2:
            if not incl_guarantee:
                create_dinner()
            else:
                create_dinner_guarantee()
        
    else:
        if v_key == 1:
            create_statlunch()
        elif v_key == 2:
            create_statdinner()

    return generate_output()