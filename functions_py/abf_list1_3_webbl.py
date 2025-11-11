#using conversion tools version: 1.0.0.119
#------------------------------------------
# Rd, 22/8/2025
# add zimmeranz = res_line, defaulnya ambil = 1, 
# di python tidak bisa ambil default
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Genstat, Arrangement, Artikel, Argt_line, Reslin_queasy, Fixleist, Guest, Reservation, Segment, Ratecode, Mc_guest, Mc_types, Mealcoup, Waehrung, Bill, Master

zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})

def abf_list1_3_webbl(fdate:date, bfast_artnr:int, bfast_dept:int, show_bfast_rate:bool, zikat_list_data:[Zikat_list]):

    prepare_cache ([Res_line, Arrangement, Artikel, Argt_line, Reslin_queasy, Fixleist, Guest, Reservation, Segment, Ratecode, Mc_guest, Mc_types, Mealcoup, Waehrung])

    abf_list_data = []
    diffcidate:int = 0
    p_87:date = None
    num_of_day:int = 0
    exchg_rate:Decimal = 1
    dont_post:bool = False
    res_line = genstat = arrangement = artikel = argt_line = reslin_queasy = fixleist = guest = reservation = segment = ratecode = mc_guest = mc_types = mealcoup = waehrung = bill = master = None

    abf_list = zikat_list = t_argt_ratelist = None

    abf_list_data, Abf_list = create_model("Abf_list", {"zinr":string, "name":string, "segmentcode":int, "ankunft":date, "anztage":int, "abreise":date, "kurzbez":string, "arrangement":string, "zimmeranz":int, "erwachs":int, "kind1":int, "kind2":int, "gratis":int, "resnr":int, "bemerk":string, "gastnr":int, "resstatus":int, "resname":string, "address":string, "city":string, "comments":string, "datum":date, "nation1":string, "bezeich":string, "zipreis":Decimal, "code":string, "id":string, "bezeichnung":string, "mobil_telefon":string, "bfast_consume":int, "mcard_number":string, "mcard_type":string, "bfast_revenue":Decimal, "c_bfast_revenue":Decimal, "i_bfast_revenue":Decimal})
    t_argt_ratelist_data, T_argt_ratelist = create_model("T_argt_ratelist", {"bfast_artnr":int, "bfast_dept":int, "argtnr":int, "based_on_adult":bool, "based_on_child":bool, "based_on_infant":bool, "adult_qty":int, "child_qty":int, "infant_qty":int, "fixliest_qty":int, "rate_adult":Decimal, "rate_child":Decimal, "rate_infant":Decimal, "do_it":bool, "room_only":bool}, {"room_only": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal abf_list_data, diffcidate, p_87, num_of_day, exchg_rate, dont_post, res_line, genstat, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, mealcoup, waehrung, bill, master
        nonlocal fdate, bfast_artnr, bfast_dept, show_bfast_rate


        nonlocal abf_list, zikat_list, t_argt_ratelist
        nonlocal abf_list_data, t_argt_ratelist_data

        return {"abf-list": abf_list_data}

    def disp_arlist1():

        nonlocal abf_list_data, diffcidate, p_87, num_of_day, exchg_rate, dont_post, res_line, genstat, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, mealcoup, waehrung, bill, master
        nonlocal fdate, bfast_artnr, bfast_dept, show_bfast_rate


        nonlocal abf_list, zikat_list, t_argt_ratelist
        nonlocal abf_list_data, t_argt_ratelist_data

        do_it:bool = False
        roflag:bool = False
        epreis:Decimal = to_decimal("0.0")
        qty:int = 0
        qty_argt:int = 0
        i:int = 0
        str:string = ""
        contcode:string = ""
        rline = None
        Rline =  create_buffer("Rline",Res_line)
        abf_list_data.clear()

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


            t_argt_ratelist_data.clear()

            if (genstat.erwachs + genstat.kind1 + genstat.gratis + genstat.kind3) == 0:
                pass
            else:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                if arrangement:

                    argt_line_obj_list = {}
                    argt_line = Argt_line()
                    artikel = Artikel()
                    for argt_line.argt_artnr, argt_line.argtnr, argt_line.betriebsnr, argt_line.betrag, argt_line.vt_percnt, argt_line._recid, artikel.betriebsnr, artikel._recid in db_session.query(Argt_line.argt_artnr, Argt_line.argtnr, Argt_line.betriebsnr, Argt_line.betrag, Argt_line.vt_percnt, Argt_line._recid, Artikel.betriebsnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == bfast_dept) & (Artikel.zwkum == bfast_artnr)).filter(
                             (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line.betrag.desc()).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        t_argt_ratelist = T_argt_ratelist()
                        t_argt_ratelist_data.append(t_argt_ratelist)

                        t_argt_ratelist.do_it = True
                        t_argt_ratelist.room_only = False
                        t_argt_ratelist.bfast_artnr = argt_line.argt_artnr
                        t_argt_ratelist.bfast_dept = bfast_dept
                        t_argt_ratelist.argtnr = argt_line.argtnr

                        if argt_line.vt_percnt == 0:
                            t_argt_ratelist.based_on_adult = True

                            if argt_line.betriebsnr == 0:
                                t_argt_ratelist.adult_qty = genstat.erwachs
                            else:
                                t_argt_ratelist.adult_qty = argt_line.betriebsnr
                            t_argt_ratelist.rate_adult =  to_decimal(argt_line.betrag)

                        elif argt_line.vt_percnt == 1:
                            t_argt_ratelist.rate_child =  to_decimal(argt_line.betrag)
                            t_argt_ratelist.based_on_child = True
                            t_argt_ratelist.child_qty = genstat.kind1

                        elif argt_line.vt_percnt == 2:
                            t_argt_ratelist.rate_infant =  to_decimal(argt_line.betrag)
                            t_argt_ratelist.based_on_infant = True
                            t_argt_ratelist.infant_qty = genstat.kind2
                else:
                    t_argt_ratelist = T_argt_ratelist()
                    t_argt_ratelist_data.append(t_argt_ratelist)

            contcode = ""
            pass
            for i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                str = entry(i - 1, genstat.res_char[1], ";")

                if substring(str, 0, 6) == ("$CODE$").lower() :
                    contcode = substring(str, 6)
                    break

            for t_argt_ratelist in query(t_argt_ratelist_data):

                if t_argt_ratelist.do_it:

                    if t_argt_ratelist.based_on_adult:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, bfast_dept)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                        if reslin_queasy:
                            t_argt_ratelist.rate_adult =  to_decimal("0")

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == bfast_dept) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == bfast_artnr) & (Reslin_queasy.resnr == genstat.resnr) & (Reslin_queasy.reslinnr == genstat.res_int[0]) & (Reslin_queasy.date1 <= fdate) & (Reslin_queasy.date2 >= fdate) & (Reslin_queasy.deci1 > 0)).order_by(Reslin_queasy._recid).all():
                                t_argt_ratelist.rate_adult =  to_decimal(t_argt_ratelist.rate_adult) + to_decimal(reslin_queasy.deci1)
                        else:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, genstat.res_int[1])],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, genstat.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci1": [(gt, 0)]})

                            if reslin_queasy:
                                t_argt_ratelist.rate_adult =  to_decimal("0")

                                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                         (Reslin_queasy.key == ("argt-line").lower()) & (Reslin_queasy.char1 == (contcode).lower()) & (Reslin_queasy.number1 == genstat.res_int[1]) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == bfast_artnr) & (Reslin_queasy.resnr == bfast_dept) & (Reslin_queasy.reslinnr == genstat.zikatnr) & (Reslin_queasy.date1 <= fdate) & (Reslin_queasy.date2 >= fdate) & (Reslin_queasy.deci1 > 0)).order_by(Reslin_queasy._recid).all():
                                    t_argt_ratelist.rate_adult =  to_decimal(t_argt_ratelist.rate_adult) + to_decimal(reslin_queasy.deci1)

                    elif t_argt_ratelist.based_on_child:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, bfast_dept)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci2": [(gt, 0)]})

                        if reslin_queasy:
                            t_argt_ratelist.rate_child =  to_decimal("0")

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == bfast_dept) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == bfast_artnr) & (Reslin_queasy.resnr == genstat.resnr) & (Reslin_queasy.reslinnr == genstat.res_int[0]) & (Reslin_queasy.date1 <= fdate) & (Reslin_queasy.date2 >= fdate) & (Reslin_queasy.deci2 > 0)).order_by(Reslin_queasy._recid).all():
                                t_argt_ratelist.rate_child =  to_decimal(t_argt_ratelist.rate_child) + to_decimal(reslin_queasy.deci2)
                        else:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, genstat.res_int[1])],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, genstat.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci2": [(gt, 0)]})

                            if reslin_queasy:
                                t_argt_ratelist.rate_child =  to_decimal("0")

                                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                         (Reslin_queasy.key == ("argt-line").lower()) & (Reslin_queasy.char1 == (contcode).lower()) & (Reslin_queasy.number1 == genstat.res_int[1]) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == bfast_artnr) & (Reslin_queasy.resnr == bfast_dept) & (Reslin_queasy.reslinnr == genstat.zikatnr) & (Reslin_queasy.date1 <= fdate) & (Reslin_queasy.date2 >= fdate) & (Reslin_queasy.deci2 > 0)).order_by(Reslin_queasy._recid).all():
                                    t_argt_ratelist.rate_child =  to_decimal(t_argt_ratelist.rate_child) + to_decimal(reslin_queasy.deci2)

                    elif t_argt_ratelist.based_on_infant:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, bfast_dept)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci3": [(gt, 0)]})

                        if reslin_queasy:
                            t_argt_ratelist.rate_infant =  to_decimal("0")

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == bfast_dept) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == bfast_artnr) & (Reslin_queasy.resnr == genstat.resnr) & (Reslin_queasy.reslinnr == genstat.res_int[0]) & (Reslin_queasy.date1 <= fdate) & (Reslin_queasy.date2 >= fdate) & (Reslin_queasy.deci3 > 0)).order_by(Reslin_queasy._recid).all():
                                t_argt_ratelist.rate_infant =  to_decimal(t_argt_ratelist.rate_infant) + to_decimal(reslin_queasy.deci3)
                        else:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, genstat.res_int[1])],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, bfast_artnr)],"resnr": [(eq, bfast_dept)],"reslinnr": [(eq, genstat.zikatnr)],"date1": [(le, fdate)],"date2": [(ge, fdate)],"deci3": [(gt, 0)]})

                            if reslin_queasy:
                                t_argt_ratelist.rate_infant =  to_decimal("0")

                                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                         (Reslin_queasy.key == ("argt-line").lower()) & (Reslin_queasy.char1 == (contcode).lower()) & (Reslin_queasy.number1 == genstat.res_int[1]) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == bfast_artnr) & (Reslin_queasy.resnr == bfast_dept) & (Reslin_queasy.reslinnr == genstat.zikatnr) & (Reslin_queasy.date1 <= fdate) & (Reslin_queasy.date2 >= fdate) & (Reslin_queasy.deci3 > 0)).order_by(Reslin_queasy._recid).all():
                                    t_argt_ratelist.rate_infant =  to_decimal(t_argt_ratelist.rate_infant) + to_decimal(reslin_queasy.deci3)
                else:

                    for fixleist in db_session.query(Fixleist).filter(
                             (Fixleist.resnr == genstat.resnr) & (Fixleist.reslinnr == genstat.res_int[0]) & (Fixleist.artnr == t_argt_ratelist.bfast_artnr) & (Fixleist.departement == t_argt_ratelist.bfast_dept)).order_by(Fixleist._recid).all():
                        dont_post = check_fixleist_posted1(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                        if not dont_post:
                            t_argt_ratelist.do_it = True
                            t_argt_ratelist.fixliest_qty = t_argt_ratelist.fixliest_qty + fixleist.number

            t_argt_ratelist = query(t_argt_ratelist_data, filters=(lambda t_argt_ratelist: t_argt_ratelist.do_it), first=True)

            if t_argt_ratelist:

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                ratecode = get_cache (Ratecode, {"code": [(eq, genstat.argt)]})
                abf_list = Abf_list()
                abf_list_data.append(abf_list)


                if not t_argt_ratelist.room_only:
                    buffer_copy(genstat, abf_list)
                else:
                    buffer_copy(genstat, abf_list,except_fields=["erwachs","kind1","gratis","datum"])
                    abf_list.erwachs = 0


                abf_list.datum = genstat.datum
                abf_list.segmentcode = reservation.segmentcode
                abf_list.kurzbez = zikat_list.kurzbez
                abf_list.erwachs = abf_list.erwachs + t_argt_ratelist.fixliest_qty
                abf_list.gastnr = genstat.gastnr
                abf_list.resname = reservation.name
                abf_list.comments = reservation.bemerk
                abf_list.zipreis =  to_decimal(genstat.zipreis)
                abf_list.ankunft = genstat.res_date[0]
                abf_list.abreise = genstat.res_date[1]
                abf_list.arrangement = genstat.argt
                abf_list.id = reservation.useridanlage

                if segment:
                    abf_list.bezeich = segment.bezeich

                if abf_list.comments != "":
                    abf_list.comments = abf_list.comments + chr_unicode(10)

                rline = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                if rline:
                    abf_list.bemerk = abf_list.comments + rline.bemerk
                    # Rd, 22/8/2025, krn hasil total adult di web,
                    abf_list.zimmeranz = rline.zimmeranz

                   

                if abf_list.comments != "":
                    abf_list.comments = abf_list.comments + chr_unicode(10)

                if not t_argt_ratelist.room_only:
                    abf_list.kind1 = abf_list.kind1 + genstat.kind3

                if ratecode:
                    abf_list.code = ratecode.code

                if guest:
                    abf_list.address = guest.adresse1
                    abf_list.city = guest.wohnort + " " + guest.plz
                    abf_list.name = guest.name
                    abf_list.comments = abf_list.comments + guest.bemerkung
                    abf_list.nation1 = guest.nation1
                    abf_list.mobil_telefon = guest.mobil_telefon

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

                    if mc_guest:
                        abf_list.mcard_number = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            abf_list.mcard_type = mc_types.bezeich
                diffcidate = (fdate - res_line.ankunft).days

                if diffcidate > 32:
                    num_of_day = diffcidate - 32
                else:
                    num_of_day = diffcidate

                mealcoup = get_cache (Mealcoup, {"resnr": [(eq, genstat.resnr)],"zinr": [(eq, genstat.zinr)],"name": [(eq, "breakfast")]})

                if mealcoup:
                    abf_list.bfast_consume = mealcoup.verbrauch[num_of_day - 1]

                if show_bfast_rate:

                    for t_argt_ratelist in query(t_argt_ratelist_data, filters=(lambda t_argt_ratelist: t_argt_ratelist.do_it)):

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == t_argt_ratelist.bfast_artnr) & (Artikel.departement == t_argt_ratelist.bfast_dept) & (Artikel.betriebsnr != 0) & (Artikel.pricetab)).first()

                        if artikel:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                            if waehrung:
                                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                                if t_argt_ratelist.based_on_adult:
                                    abf_list.bfast_revenue =  to_decimal(abf_list.bfast_revenue) + to_decimal(t_argt_ratelist.rate_adult) * to_decimal(t_argt_ratelist.adult_qty) * to_decimal(exchg_rate)

                                elif t_argt_ratelist.based_on_child:
                                    abf_list.c_bfast_revenue =  to_decimal(abf_list.c_bfast_revenue) + to_decimal(t_argt_ratelist.rate_child) * to_decimal(t_argt_ratelist.child_qty) * to_decimal(exchg_rate)

                                elif t_argt_ratelist.based_on_infant:
                                    abf_list.i_bfast_revenue =  to_decimal(abf_list.i_bfast_revenue) + to_decimal(t_argt_ratelist.rate_infant) * to_decimal(t_argt_ratelist.infant_qty) * to_decimal(exchg_rate)
                        else:

                            if t_argt_ratelist.based_on_adult:
                                abf_list.bfast_revenue =  to_decimal(abf_list.bfast_revenue) + to_decimal(t_argt_ratelist.rate_adult) * to_decimal(t_argt_ratelist.adult_qty)

                            elif t_argt_ratelist.based_on_child:
                                abf_list.c_bfast_revenue =  to_decimal(abf_list.c_bfast_revenue) + to_decimal(t_argt_ratelist.rate_child) * to_decimal(t_argt_ratelist.child_qty)

                            elif t_argt_ratelist.based_on_infant:
                                abf_list.i_bfast_revenue =  to_decimal(abf_list.i_bfast_revenue) + to_decimal(t_argt_ratelist.rate_infant) * to_decimal(t_argt_ratelist.infant_qty)
                else:
                    abf_list.bfast_revenue =  to_decimal("0")
                    abf_list.c_bfast_revenue =  to_decimal("0")
                    abf_list.i_bfast_revenue =  to_decimal("0")


    def check_fixleist_posted1(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal abf_list_data, diffcidate, p_87, num_of_day, exchg_rate, dont_post, res_line, genstat, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, mc_guest, mc_types, mealcoup, waehrung, bill, master
        nonlocal fdate, bfast_artnr, bfast_dept, show_bfast_rate


        nonlocal abf_list, zikat_list, t_argt_ratelist
        nonlocal abf_list_data, t_argt_ratelist_data

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

    disp_arlist1()

    return generate_output()