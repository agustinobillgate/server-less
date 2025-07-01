#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Arrangement, Artikel, Argt_line, Reslin_queasy, Fixleist, Guest, Reservation, Segment, Ratecode, Genstat, Bill, Master

def abf_list_1bl(fdate:date, tdate:date, bfast_artnr:int, bfast_dept:int):

    prepare_cache ([Htparam, Arrangement, Argt_line, Fixleist, Guest, Reservation, Segment, Ratecode])

    abf_list_list = []
    datum:date = None
    to_date:date = None
    htparam = res_line = arrangement = artikel = argt_line = reslin_queasy = fixleist = guest = reservation = segment = ratecode = genstat = bill = master = None

    abf_list = None

    abf_list_list, Abf_list = create_model("Abf_list", {"zinr":string, "name":string, "segmentcode":int, "ankunft":date, "anztage":int, "abreise":date, "kurzbez":string, "arrangement":string, "zimmeranz":int, "erwachs":int, "kind1":int, "gratis":int, "resnr":int, "bemerk":string, "gastnr":int, "resstatus":int, "resname":string, "address":string, "city":string, "comments":string, "nation1":string, "bezeich":string, "zipreis":Decimal, "code":string, "id":string, "bezeichnung":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal abf_list_list, datum, to_date, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, genstat, bill, master
        nonlocal fdate, tdate, bfast_artnr, bfast_dept


        nonlocal abf_list
        nonlocal abf_list_list

        return {"abf-list": abf_list_list}

    def disp_arlist():

        nonlocal abf_list_list, datum, to_date, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, genstat, bill, master
        nonlocal fdate, tdate, bfast_artnr, bfast_dept


        nonlocal abf_list
        nonlocal abf_list_list

        do_it:bool = False
        roflag:bool = False
        epreis:Decimal = to_decimal("0.0")
        qty:int = 0
        i:int = 0
        str:string = ""
        contcode:string = ""
        dont_post:bool = False
        abf_list_list.clear()

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.ankunft < fdate) & (Res_line.abreise >= fdate) & ((Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)) & (Res_line.active_flag <= 1) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr).all():
            do_it = False
            roflag = True
            qty = 0

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

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, guest_pr.code)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, res_line.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                if not reslin_queasy:

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, guest_pr.code)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, bfast_dept)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})
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

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.resnr)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, res_line.argt_typ)]})

                ratecode = get_cache (Ratecode, {"code": [(eq, res_line.arrangement)]})
                abf_list = Abf_list()
                abf_list_list.append(abf_list)


                if not roflag:
                    buffer_copy(res_line, abf_list)
                else:
                    buffer_copy(res_line, abf_list,except_fields=["erwachs","kind1","gratis"])
                    abf_list.erwachs = 0


                abf_list.segmentcode = reservation.segmentcode
                abf_list.erwachs = abf_list.erwachs + qty
                abf_list.gastnr = res_line.gastnr
                abf_list.resname = reservation.name
                abf_list.comments = reservation.bemerk
                abf_list.bezeich = segment.bezeich
                abf_list.zipreis =  to_decimal(res_line.zipreis)
                abf_list.id = reservation.useridanlage

                if abf_list.comments != "":
                    abf_list.comments = abf_list.comments + chr_unicode(10)
                abf_list.comments = abf_list.comments + res_line.bemerk

                if not roflag:
                    abf_list.kind1 = abf_list.kind1 + res_line.l_zuordnung[3]

                if zimkateg:
                    abf_list.kurzbez = zimkateg.kurzbez

                if ratecode:
                    abf_list.code = ratecode.code

                if guest:
                    abf_list.nation1 = guest.nation1
                    abf_list.address = guest.adresse1
                    abf_list.city = guest.wohnort + " " + guest.plz


    def disp_arlist1():

        nonlocal abf_list_list, datum, to_date, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, genstat, bill, master
        nonlocal fdate, tdate, bfast_artnr, bfast_dept


        nonlocal abf_list
        nonlocal abf_list_list

        do_it:bool = False
        roflag:bool = False
        epreis:Decimal = to_decimal("0.0")
        qty:int = 0
        i:int = 0
        str:string = ""
        contcode:string = ""
        dont_post:bool = False
        abf_list_list.clear()

        for genstat in db_session.query(Genstat).filter(
                 ((Genstat.resstatus != 3) & (Genstat.resstatus != 4) & (Genstat.resstatus != 8) & (Genstat.resstatus != 9) & (Genstat.resstatus != 10) & (Genstat.resstatus != 12)) & (Genstat.datum >= fdate) & (Genstat.datum <= tdate)).order_by(Genstat.zinr).all():
            do_it = False
            roflag = True
            qty = 0

            if (genstat.erwachs + genstat.kind1 + genstat.gratis + genstat.kind3) == 0:
                pass
            else:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

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
                for i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                    str = entry(i - 1, genstat.res_char[1], ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                        break

                if contcode != "":

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, guest_pr.code)],"number1": [(eq, genstat.res_int[1])],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, genstat.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                if not reslin_queasy:

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, guest_pr.code)],"number1": [(eq, genstat.res_int[1])],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, bfast_dept)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})
                do_it = None != reslin_queasy
                roflag = not do_it

            if not do_it:

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == genstat.resnr) & (Fixleist.artnr == bfast_artnr) & (Fixleist.departement == bfast_dept)).order_by(Fixleist._recid).all():
                    dont_post = check_fixleist_posted1(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not dont_post:
                        do_it = True
                        qty = qty + fixleist.number

            if do_it:

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                ratecode = get_cache (Ratecode, {"code": [(eq, genstat.argt)]})
                abf_list = Abf_list()
                abf_list_list.append(abf_list)


                if not roflag:
                    buffer_copy(genstat, abf_list)
                else:
                    buffer_copy(genstat, abf_list,except_fields=["erwachs","kind1","gratis","datum"])
                    abf_list.erwachs = 0


                abf_list.segmentcode = reservation.segmentcode
                abf_list.erwachs = abf_list.erwachs + qty
                abf_list.gastnr = genstat.gastnr
                abf_list.resname = reservation.name
                abf_list.comments = reservation.bemerk
                abf_list.bezeich = segment.bezeich
                abf_list.zipreis =  to_decimal(genstat.zipreis)
                abf_list.ankunft = genstat.res_date[0]
                abf_list.abreise = genstat.res_date[1]
                abf_list.id = reservation.useridanlage

                if abf_list.comments != "":
                    abf_list.comments = abf_list.comments + chr_unicode(10)

                if not roflag:
                    abf_list.kind1 = abf_list.kind1 + genstat.kind1

                if zimkateg:
                    abf_list.kurzbez = zimkateg.kurzbez

                if ratecode:
                    abf_list.code = ratecode.code

                if guest:
                    abf_list.address = guest.adresse1
                abf_list.city = guest.wohnort + " " + guest.plz
                abf_list.nation1 = guest.nation1
                abf_list.name = guest.name
                abf_list.comments = abf_list.comments + guest.bemerkung


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal abf_list_list, datum, to_date, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, genstat, bill, master
        nonlocal fdate, tdate, bfast_artnr, bfast_dept


        nonlocal abf_list
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


    def check_fixleist_posted1(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal abf_list_list, datum, to_date, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, genstat, bill, master
        nonlocal fdate, tdate, bfast_artnr, bfast_dept


        nonlocal abf_list
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
                     (Invoice.resnr == genstat.resnr) & (Invoice.reslinnr == 0)).first()
        else:

            invoice = db_session.query(Invoice).filter(
                     (Invoice.zinr == genstat.zinr) & (Invoice.resnr == genstat.resnr) & (Invoice.reslinnr == genstat.res_int[0]) & (Invoice.billtyp == 0) & (Invoice.billnr == 1) & (Invoice.flag == 0)).first()

        if not dont_post:

            if fakt_modus == 2:

                if genstat.datum != fdate:
                    dont_post = True

            elif fakt_modus == 3:

                if (genstat.datum + 1) != fdate:
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
                    delta = (lfakt - genstat.datum).days

                    if delta < 0:
                        delta = 0
                start_date = genstat.datum + timedelta(days=delta)

                if (genstat.datum - start_date) < intervall:
                    start_date = genstat.datum

                if fdate > (start_date + timedelta(days=(intervall - 1))):
                    dont_post = True

                if fdate < start_date:
                    dont_post = True

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    datum = htparam.fdate

    if fdate > datum and tdate == datum:
        disp_arlist()

    elif fdate <= datum and tdate == datum:
        disp_arlist1()

    return generate_output()