#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Arrangement, Artikel, Argt_line, Reslin_queasy, Fixleist, Guest, Reservation, Segment, Ratecode, Bill, Master

zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})

def abf_list_3bl(fdate:date, bfast_artnr:int, bfast_dept:int, incl_accom:bool, zikat_list_list:[Zikat_list]):

    prepare_cache ([Htparam, Arrangement, Argt_line, Fixleist, Guest, Reservation, Segment, Ratecode])

    abf_list_list = []
    mxtime_dayuse:int = 0
    param_561:string = ""
    htparam = res_line = arrangement = artikel = argt_line = reslin_queasy = fixleist = guest = reservation = segment = ratecode = bill = master = None

    abf_list = zikat_list = None

    abf_list_list, Abf_list = create_model("Abf_list", {"zinr":string, "name":string, "segmentcode":int, "ankunft":date, "anztage":int, "abreise":date, "kurzbez":string, "arrangement":string, "zimmeranz":int, "erwachs":int, "kind1":int, "gratis":int, "resnr":int, "bemerk":string, "gastnr":int, "resstatus":int, "resname":string, "address":string, "city":string, "comments":string, "datum":date, "nation1":string, "bezeich":string, "zipreis":Decimal, "code":string, "id":string, "bezeichnung":string, "mobil_telefon":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal abf_list_list, mxtime_dayuse, param_561, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, bill, master
        nonlocal fdate, bfast_artnr, bfast_dept, incl_accom


        nonlocal abf_list, zikat_list
        nonlocal abf_list_list

        return {"abf-list": abf_list_list}

    def disp_arlist():

        nonlocal abf_list_list, mxtime_dayuse, param_561, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, bill, master
        nonlocal fdate, bfast_artnr, bfast_dept, incl_accom


        nonlocal abf_list, zikat_list
        nonlocal abf_list_list

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
        abf_list_list.clear()

        res_line_obj_list = {}
        for res_line in db_session.query(Res_line).filter(
                 ((Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)) & (Res_line.active_flag == 1) & (((Res_line.ankunft <= fdate) & (Res_line.abreise >= fdate)) | ((Res_line.ankunft == fdate) & (Res_line.abreise == fdate) & (Res_line.ankzeit <= mxtime_dayuse))) & (Res_line.l_zuordnung[inc_value(2)] <= 1)).order_by(Res_line.zinr).all():
            zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            do_it = False
            roflag = True
            qty = 0

            if incl_accom and res_line.l_zuordnung[2] == 1:
                do_it = False

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:

                    argt_line_obj_list = {}
                    for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == bfast_artnr)).filter(
                             (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).yield_per(100):
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        do_it = True
                        roflag = False
                        epreis =  to_decimal(argt_line.betrag)


                        break

            if incl_accom and res_line.l_zuordnung[2] == 0:
                do_it = False

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:

                    argt_line_obj_list = {}
                    for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == bfast_artnr)).filter(
                             (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).yield_per(100):
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        do_it = True
                        roflag = False
                        epreis =  to_decimal(argt_line.betrag)


                        break

            if res_line.l_zuordnung[2] == 0:

                if (res_line.erwachs + res_line.kind1 + res_line.gratis + res_line.l_zuordnung[3]) == 0:
                    pass
                else:

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    if arrangement:

                        argt_line_obj_list = {}
                        for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == bfast_artnr)).filter(
                                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).yield_per(100):
                            if argt_line_obj_list.get(argt_line._recid):
                                continue
                            else:
                                argt_line_obj_list[argt_line._recid] = True


                            do_it = True
                            roflag = False
                            epreis =  to_decimal(argt_line.betrag)


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

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, res_line.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                    if not reslin_queasy:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"number1": [(eq, bfast_dept)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})
                do_it = None != reslin_queasy
                roflag = not do_it

            if not do_it:

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr) & (Fixleist.artnr == bfast_artnr) & (Fixleist.departement == bfast_dept)).order_by(Fixleist._recid).all():
                    dont_post = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not dont_post:
                        do_it = True
                        qty = qty + fixleist.number

            if do_it:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                ratecode = get_cache (Ratecode, {"code": [(eq, res_line.arrangement)]})
                abf_list = Abf_list()
                abf_list_list.append(abf_list)


                if not roflag:
                    buffer_copy(res_line, abf_list)
                else:
                    buffer_copy(res_line, abf_list,except_fields=["erwachs","kind1","gratis"])
                    abf_list.erwachs = 0


                abf_list.segmentcode = reservation.segmentcode
                abf_list.kurzbez = zikat_list.kurzbez
                abf_list.erwachs = abf_list.erwachs + qty
                abf_list.gastnr = res_line.gastnr
                abf_list.resname = reservation.name
                abf_list.zipreis =  to_decimal(res_line.zipreis)
                abf_list.id = reservation.useridanlage

                if segment:
                    abf_list.bezeich = segment.bezeich
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
                abf_list.comments = rsv_remark
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
                abf_list.bemerk = resline_remark

                if abf_list.comments != "":
                    abf_list.comments = abf_list.comments + chr_unicode(10)
                abf_list.comments = abf_list.comments + resline_remark
                resline_remark = ""

                if not roflag:
                    abf_list.kind1 = abf_list.kind1 + res_line.l_zuordnung[3]

                if ratecode:
                    abf_list.code = ratecode.code

                if guest:
                    abf_list.address = guest.adresse1
                    abf_list.city = guest.wohnort + " " + guest.plz
                    abf_list.nation1 = guest.nation1
                    abf_list.mobil_telefon = guest.mobil_telefon

                if res_line.resstatus == 11 and res_line.l_zuordnung[2] == 0:
                    abf_list.name = abf_list.name + " *"

                if res_line.resstatus == 11 and res_line.l_zuordnung[2] == 1:
                    abf_list.name = abf_list.name + " **"

                if res_line.resstatus == 13 and res_line.l_zuordnung[2] == 0:
                    abf_list.name = abf_list.name + " *"

                if res_line.resstatus == 13 and res_line.l_zuordnung[2] == 1:
                    abf_list.name = abf_list.name + " **"


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal abf_list_list, mxtime_dayuse, param_561, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, bill, master
        nonlocal fdate, bfast_artnr, bfast_dept, incl_accom


        nonlocal abf_list, zikat_list
        nonlocal abf_list_list

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
    disp_arlist()

    return generate_output()