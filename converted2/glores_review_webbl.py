#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Kontline, Guest, Zimkateg, Guest_pr, Res_line, Reservation

def glores_review_webbl(pvilanguage:int, delflag:bool, from_date:date, to_date:date, ci_date:date, resflag1:bool, gflag:bool, cflag:bool, from_name:string, to_name:string):

    prepare_cache ([Bediener, Kontline, Guest, Zimkateg, Guest_pr, Res_line, Reservation])

    str_detail_data = []
    str_summary_data = []
    sum_list_data = []
    lvcarea:string = "glores-review"
    loopi:int = 0
    str_parse:string = ""
    bediener = kontline = guest = zimkateg = guest_pr = res_line = reservation = None

    sum_list = output_list = str_detail = str_summary = k_list = res_list = usr = allot_list = None

    sum_list_data, Sum_list = create_model("Sum_list", {"datum":date, "gastnr":int, "firma":string, "kontcode":string, "zikatnr":int, "kurzbez":string, "erwachs":int, "kind1":int, "gloanz":int, "gresanz":int, "resanz":int, "resnrstr":string})
    output_list_data, Output_list = create_model("Output_list", {"str":string})
    str_detail_data, Str_detail = create_model("Str_detail", {"company_name":string, "address":string, "city":string, "glorescode":string, "pricecode":string, "start_date":string, "pax":string, "ending_date":string, "rmcat":string, "argt":string, "id":string, "chgid":string, "create_date":string, "comments":string, "dates_period":string, "dates_number":[string,31], "dates_str":[string,31], "reserved_room":[string,31], "used_reservation":[string,31], "not_used":[string,31], "avail_room":[string,31], "overbooking":[string,31], "reservations":string, "residents":string, "cancel_res":string})
    str_summary_data, Str_summary = create_model("Str_summary", {"total_reserve":[string,31], "used_reserve":[string,31], "not_used":[string,31]})
    k_list_data, K_list = create_model("K_list", {"gastnr":int, "bediener_nr":int, "kontcode":string, "ankunft":date, "zikatnr":int, "argt":string, "zimmeranz":[int,31], "erwachs":int, "kind1":int, "ruecktage":int, "overbooking":int, "abreise":date, "useridanlage":string, "resdate":date, "bemerk":string})
    res_list_data, Res_list = create_model("Res_list", {"flag":string, "count":int, "s1":string})
    allot_list_data, Allot_list = create_model_like(Kontline)

    Usr = create_buffer("Usr",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_detail_data, str_summary_data, sum_list_data, lvcarea, loopi, str_parse, bediener, kontline, guest, zimkateg, guest_pr, res_line, reservation
        nonlocal pvilanguage, delflag, from_date, to_date, ci_date, resflag1, gflag, cflag, from_name, to_name
        nonlocal usr


        nonlocal sum_list, output_list, str_detail, str_summary, k_list, res_list, usr, allot_list
        nonlocal sum_list_data, output_list_data, str_detail_data, str_summary_data, k_list_data, res_list_data, allot_list_data

        return {"str-detail": str_detail_data, "str-summary": str_summary_data, "sum-list": sum_list_data}

    def create_list(del_flag:bool):

        nonlocal str_detail_data, str_summary_data, sum_list_data, lvcarea, loopi, str_parse, bediener, kontline, guest, zimkateg, guest_pr, res_line, reservation
        nonlocal pvilanguage, delflag, from_date, to_date, ci_date, resflag1, gflag, cflag, from_name, to_name
        nonlocal usr


        nonlocal sum_list, output_list, str_detail, str_summary, k_list, res_list, usr, allot_list
        nonlocal sum_list_data, output_list_data, str_detail_data, str_summary_data, k_list_data, res_list_data, allot_list_data

        datum:date = None
        usr_init:string = ""
        i:int = 0
        count:int = 0
        currresnr:int = 0
        anz1:List[int] = create_empty_list(31,0)
        anz2:List[int] = create_empty_list(31,0)
        t_anz0:List[int] = create_empty_list(31,0)
        t_anz1:List[int] = create_empty_list(31,0)
        t_anz2:List[int] = create_empty_list(31,0)
        avail_allotm:List[int] = create_empty_list(31,0)
        overbook:List[int] = create_empty_list(31,0)
        do_it:bool = False
        wday:List[string] = ["SU", "MO", "TU", "WE", "TH", "FR", "SA", "SU"]
        loopdatum:int = 0
        loopdatstr:int = 0

        if del_flag:
            output_list_data.clear()
        allot_list_data.clear()
        k_list_data.clear()
        res_list_data.clear()
        sum_list_data.clear()
        for i in range(1,31 + 1) :
            t_anz0[i - 1] = 0
            t_anz1[i - 1] = 0
            t_anz2[i - 1] = 0
            avail_allotm[i - 1] = 0
            overbook[i - 1] = 0
        create_alist()

        k_list = query(k_list_data, first=True)

        if k_list:
            do_it = True
        else:
            do_it = False

        if do_it:

            guest_obj_list = {}
            for guest in db_session.query(Guest).filter(
                     ((Guest.gastnr.in_(list(set([k_list.gastnr for k_list in k_list_data])))))).order_by(Guest.name, k_list.ankunft).all():
                if guest_obj_list.get(guest._recid):
                    continue
                else:
                    guest_obj_list[guest._recid] = True

                k_list = query(k_list_data, (lambda k_list: (guest.gastnr == k_list.gastnr)), first=True)

                usr = get_cache (Bediener, {"nr": [(eq, k_list.bediener_nr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, k_list.zikatnr)]})
                str_detail = Str_detail()
                str_detail_data.append(str_detail)

                output_list = Output_list()
                output_list_data.append(output_list)

                str = translateExtended ("Company Name :", lvcarea, "") + " " + guest.name + ", " + guest.anredefirma
                output_list = Output_list()
                output_list_data.append(output_list)

                str = translateExtended ("Address :", lvcarea, "") + " " + guest.adresse1 + " " + guest.adresse2
                output_list = Output_list()
                output_list_data.append(output_list)

                str = translateExtended ("City :", lvcarea, "") + " " + guest.wohnort + " " + guest.plz
                output_list = Output_list()
                output_list_data.append(output_list)

                str = translateExtended ("Code :", lvcarea, "") + " " + k_list.kontcode + " " + translateExtended ("PriceCode :", lvcarea, "") + " "

                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

                if guest_pr:
                    str = str + guest_pr.code
                output_list = Output_list()
                output_list_data.append(output_list)

                str = translateExtended ("Start", lvcarea, "") + " " + to_string(k_list.ankunft) + " " + translateExtended ("Pax", lvcarea, "") + " " + to_string(k_list.erwachs) + "/" + to_string(k_list.kind1)
                output_list = Output_list()
                output_list_data.append(output_list)

                str = translateExtended ("Ending", lvcarea, "") + " " + to_string(k_list.abreise) + " " + translateExtended ("RmCat", lvcarea, "") + " "

                if zimkateg:
                    str = str + to_string(zimkateg.kurzbez, "x(6)")
                else:
                    str = str + " "

                if usr:
                    usr_init = usr.userinit
                else:
                    usr_init = " "
                str = str + " " + translateExtended ("Arg", lvcarea, "") + " " + to_string(k_list.argt, "x(5)") + " " + translateExtended ("ID", lvcarea, "") + " " + to_string(usr_init) + " " + translateExtended ("ChgID", lvcarea, "") + " " + to_string(k_list.useridanlage, "x(2)") + " " + translateExtended ("Date", lvcarea, "") + " " + to_string(k_list.resdat)

                if k_list.bemerk != "":
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    str = translateExtended ("Comment :", lvcarea, "") + " " + k_list.bemerk
                output_list = Output_list()
                output_list_data.append(output_list)

                str = translateExtended ("Dates :", lvcarea, "") + " " + to_string(from_date) + " - " + to_string(to_date)
                str_detail.company_name = guest.name
                str_detail.address = guest.adresse1
                str_detail.city = guest.wohnort + " " + guest.plz
                str_detail.glorescode = k_list.kontcode
                str_detail.pricecode = guest_pr.code
                str_detail.start_date = to_string(k_list.ankunft)
                str_detail.pax = to_string(k_list.erwachs) + "/" + to_string(k_list.kind1)
                str_detail.ending_date = to_string(k_list.abreise)
                str_detail.rmcat = to_string(zimkateg.kurzbez, "x(6)")
                str_detail.argt = to_string(k_list.argt, "x(5)")
                str_detail.id = to_string(usr_init)
                str_detail.chgid = to_string(k_list.useridanlage, "x(2)")
                str_detail.create_date = to_string(k_list.resdat)
                str_detail.comments = k_list.bemerk
                str_detail.dates_period = to_string(from_date) + " - " + to_string(to_date)

                output_list = Output_list()
                output_list_data.append(output_list)

                str = " "
                datum = from_date
                loopdatum = 0
                while datum <= to_date:
                    str = str + to_string(get_day(datum) , "99 ")
                    loopdatum = loopdatum + 1
                    str_detail.dates_number[loopdatum - 1] = to_string(get_day(datum) , "99")


                    datum = datum + timedelta(days=1)
                output_list = Output_list()
                output_list_data.append(output_list)

                str = " "
                datum = from_date
                loopdatstr = 0
                while datum <= to_date:
                    str = str + wday[get_weekday(datum) - 1] + " "
                    loopdatstr = loopdatstr + 1
                    str_detail.dates_str[loopdatstr - 1] = wday[get_weekday(datum) - 1]


                    datum = datum + timedelta(days=1)
                output_list = Output_list()
                output_list_data.append(output_list)

                for i in range(1,108 + 1) :
                    str = str + "-"
                output_list = Output_list()
                output_list_data.append(output_list)

                str = to_string(translateExtended ("Reserved Room", lvcarea, "") , "x(15)")
                datum = from_date
                i = 1
                while datum <= to_date:

                    if datum >= k_list.ankunft and datum <= k_list.abreise and datum >= (ci_date):
                        t_anz0[i - 1] = t_anz0[i - 1] + k_list.zimmeranz[i - 1]
                        str = str + to_string(k_list.zimmeranz[i - 1], "-99")
                        str_detail.reserved_room[i - 1] = to_string(k_list.zimmeranz[i - 1], "-99")


                    else:
                        str = str + " 00"
                        str_detail.reserved_room[i - 1] = "00"
                    i = i + 1
                    datum = datum + timedelta(days=1)
                for i in range(1,31 + 1) :
                    anz1[i - 1] = 0
                    anz2[i - 1] = 0

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.gastnr == k_list.gastnr) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < from_date)) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.kontignr == 0)).order_by(Res_line.resnr).all():
                    for datum in date_range(from_date,to_date) :

                        if res_line.ankunft <= datum and res_line.abreise > datum:

                            sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.datum == datum and sum_list.gastnr == res_line.gastnr and sum_list.zikatnr == res_line.zikatnr and sum_list.erwachs >= res_line.erwachs), first=True)

                            if not sum_list:

                                sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.datum == datum and sum_list.gastnr == res_line.gastnr and sum_list.zikatnr == res_line.zikatnr), first=True)

                            if sum_list:
                                sum_list.resanz = sum_list.resanz + res_line.zimmeranz

                            if currresnr != res_line.resnr:
                                currresnr = res_line.resnr
                                sum_list.resnrstr = sum_list.resnrstr +\
                                        trim(to_string(res_line.resnr, ">>>>>>>9")) + "; "


                count = 0

                res_line_obj_list = {}
                res_line = Res_line()
                kontline = Kontline()
                for res_line.abreise, res_line.gastnr, res_line.zikatnr, res_line.erwachs, res_line.zimmeranz, res_line.resnr, res_line.ankunft, res_line.kind1, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line._recid, kontline.gastnr, kontline.kontcode, kontline.bediener_nr, kontline.ankunft, kontline.zikatnr, kontline.arrangement, kontline.erwachs, kontline.kind1, kontline.ruecktage, kontline.overbooking, kontline.abreise, kontline.useridanlage, kontline.resdat, kontline.bemerk, kontline.zimmeranz, kontline._recid in db_session.query(Res_line.abreise, Res_line.gastnr, Res_line.zikatnr, Res_line.erwachs, Res_line.zimmeranz, Res_line.resnr, Res_line.ankunft, Res_line.kind1, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Kontline.gastnr, Kontline.kontcode, Kontline.bediener_nr, Kontline.ankunft, Kontline.zikatnr, Kontline.arrangement, Kontline.erwachs, Kontline.kind1, Kontline.ruecktage, Kontline.overbooking, Kontline.abreise, Kontline.useridanlage, Kontline.resdat, Kontline.bemerk, Kontline.zimmeranz, Kontline._recid).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) & (Kontline.kontcode == k_list.kontcode) & (Kontline.betriebsnr == 1) & (Kontline.kontstatus == 1)).filter(
                         (Res_line.gastnr == k_list.gastnr) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < from_date)) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.kontignr < 0)).order_by(Res_line.ankunft, Res_line.abreise, Res_line.resnr).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                    for datum in date_range(from_date,to_date) :

                        if res_line.ankunft <= datum and res_line.abreise > datum:

                            sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.datum == datum and sum_list.gastnr == res_line.gastnr and sum_list.kontcode == k_list.kontcode), first=True)

                            if sum_list:
                                sum_list.gresanz = sum_list.gresanz + res_line.zimmeranz

                    if resflag1 and res_line.active_flag == 0:
                        res_list = Res_list()
                        res_list_data.append(res_list)

                        res_list.flag = "r"
                        count = count + 1
                        res_list.count = count
                        s1 = " " + translateExtended ("ResNo", lvcarea, "") + " " + to_string(res_line.resnr, ">>>>>>9") + " " + translateExtended ("Arrival", lvcarea, "") + " " + to_string(res_line.ankunft) + " " + translateExtended ("Qty", lvcarea, "") + " " + to_string(res_line.zimmeranz, "99") + " " + translateExtended ("Pax", lvcarea, "") + " " + to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) + " " + translateExtended ("Departure", lvcarea, "") + " " + to_string(res_line.abreise) + " " + translateExtended ("ID", lvcarea, "") + " " + to_string(reservation.useridanlage, "x(2)") + " " + translateExtended ("ChgID", lvcarea, "") + " " + to_string(res_line.changed_id, "x(2)")

                        if res_line.bemerk != "":
                            res_list = Res_list()
                            res_list_data.append(res_list)

                            count = count + 1
                            res_list.flag = "r"
                            s1 = translateExtended ("Comment :", lvcarea, "") + " " + res_line.bemerk

                    if gflag and res_line.active_flag == 2:
                        res_list = Res_list()
                        res_list_data.append(res_list)

                        res_list.flag = "g"
                        count = count + 1
                        res_list.count = count
                        s1 = " " + translateExtended ("ResNo", lvcarea, "") + " " + to_string(res_line.resnr, ">>>>>>9") + " " + translateExtended ("Arrival", lvcarea, "") + " " + to_string(res_line.ankunft) + " " + translateExtended ("Qty", lvcarea, "") + " " + to_string(res_line.zimmeranz, "99") + " " + translateExtended ("Pax", lvcarea, "") + " " + to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) + " " + translateExtended ("Departure", lvcarea, "") + " " + to_string(res_line.abreise) + " " + translateExtended ("ID", lvcarea, "") + " " + to_string(reservation.useridanlage, "x(2)") + " " + translateExtended ("ChgID", lvcarea, "") + " " + to_string(res_line.changed_id, "x(2)")

                        if res_line.bemerk != "":
                            res_list = Res_list()
                            res_list_data.append(res_list)

                            count = count + 1
                            res_list.flag = "g"
                            s1 = translateExtended ("Comment :", lvcarea, "") + " " + res_line.bemerk
                    datum = from_date
                    i = 1
                    while datum <= to_date:

                        if datum >= res_line.ankunft and datum < res_line.abreise:
                            anz1[i - 1] = anz1[i - 1] + res_line.zimmeranz
                        i = i + 1
                        datum = datum + timedelta(days=1)
                datum = from_date
                i = 1
                while datum <= to_date:
                    anz2[i - 1] = k_list.zimmeranz[i - 1] - anz1[i - 1]
                    i = i + 1
                    datum = datum + timedelta(days=1)
                i = 1
                datum = from_date
                while datum <= to_date:
                    t_anz1[i - 1] = t_anz1[i - 1] + anz1[i - 1]
                    t_anz2[i - 1] = t_anz2[i - 1] + anz2[i - 1]
                    i = i + 1
                    datum = datum + timedelta(days=1)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.str = to_string(translateExtended ("Used Rservation", lvcarea, "") , "x(15)")
                datum = from_date
                i = 1
                while datum <= to_date:
                    str = str + to_string(anz1[i - 1], "-99")
                    str_detail.used_reservation[i - 1] = to_string(anz1[i - 1], "-99")


                    i = i + 1
                    datum = datum + timedelta(days=1)
                output_list = Output_list()
                output_list_data.append(output_list)

                str = to_string(translateExtended ("Not used", lvcarea, "") , "x(15)")
                datum = from_date
                i = 1
                while datum <= to_date:

                    if anz2[i - 1] > 0:
                        str = str + to_string(anz2[i - 1], "-99")
                        str_detail.not_used[i - 1] = to_string(anz2[i - 1], "-99")


                    else:
                        str = str + " 00"
                        str_detail.not_used[i - 1] = "00"


                    i = i + 1
                    datum = datum + timedelta(days=1)
                output_list = Output_list()
                output_list_data.append(output_list)

                str = to_string(translateExtended ("Available", lvcarea, "") , "x(15)")
                datum = from_date
                i = 1
                while datum <= to_date:

                    if datum >= (ci_date + timedelta(days=k_list.ruecktage)):

                        if anz2[i - 1] > 0:
                            avail_allotm[i - 1] = anz2[i - 1]
                            str = str + to_string(avail_allotm[i - 1], "-99")
                            str_detail.avail_room[i - 1] = to_string(avail_allotm[i - 1], "-99")


                        else:
                            avail_allotm[i - 1] = 0
                            str = str + " 00"
                            str_detail.avail_room[i - 1] = "00"


                    else:
                        avail_allotm[i - 1] = 0
                        str = str + " 00"
                        str_detail.avail_room[i - 1] = "00"


                    i = i + 1
                    datum = datum + timedelta(days=1)
                output_list = Output_list()
                output_list_data.append(output_list)

                str = to_string(translateExtended ("Overbooking", lvcarea, "") , "x(15)")
                datum = from_date
                i = 1
                while datum <= to_date:

                    if datum >= (ci_date + timedelta(days=k_list.ruecktage)):

                        if anz2[i - 1] < 0:
                            overbook[i - 1] = - anz2[i - 1]
                            str = str + to_string(overbook[i - 1], "-99")
                            str_detail.overbooking[i - 1] = to_string(overbook[i - 1], "-99")


                        else:
                            overbook[i - 1] = 0
                            str = str + " 00"
                            str_detail.overbooking[i - 1] = "00"


                    else:
                        overbook[i - 1] = 0
                        str = str + " 00"
                        str_detail.overbooking[i - 1] = "00"


                    i = i + 1
                    datum = datum + timedelta(days=1)

                if resflag1:
                    i = 1
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    str = translateExtended ("Reservations :", lvcarea, "") + " "

                    for res_list in query(res_list_data, filters=(lambda res_list: res_list.flag.lower()  == ("r").lower()), sort_by=[("count",False)]):

                        if i > 1:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            str = " " + s1
                        else:
                            str = str + s1
                        i = i + 1
                        str_detail.reservations = s1

                if gflag:
                    i = 1
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    str = translateExtended ("Residents :", lvcarea, "") + " "

                    for res_list in query(res_list_data, filters=(lambda res_list: res_list.flag.lower()  == ("g").lower()), sort_by=[("count",False)]):

                        if i > 1:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            str = " " + s1
                        else:
                            str = str + s1
                        i = i + 1
                        str_detail.residents = s1

                if cflag:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    kontline = Kontline()
                    for res_line.abreise, res_line.gastnr, res_line.zikatnr, res_line.erwachs, res_line.zimmeranz, res_line.resnr, res_line.ankunft, res_line.kind1, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line._recid, kontline.gastnr, kontline.kontcode, kontline.bediener_nr, kontline.ankunft, kontline.zikatnr, kontline.arrangement, kontline.erwachs, kontline.kind1, kontline.ruecktage, kontline.overbooking, kontline.abreise, kontline.useridanlage, kontline.resdat, kontline.bemerk, kontline.zimmeranz, kontline._recid in db_session.query(Res_line.abreise, Res_line.gastnr, Res_line.zikatnr, Res_line.erwachs, Res_line.zimmeranz, Res_line.resnr, Res_line.ankunft, Res_line.kind1, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Kontline.gastnr, Kontline.kontcode, Kontline.bediener_nr, Kontline.ankunft, Kontline.zikatnr, Kontline.arrangement, Kontline.erwachs, Kontline.kind1, Kontline.ruecktage, Kontline.overbooking, Kontline.abreise, Kontline.useridanlage, Kontline.resdat, Kontline.bemerk, Kontline.zimmeranz, Kontline._recid).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) & (Kontline.kontcode == k_list.kontcode) & (Kontline.betriebsnr == 1) & (Kontline.kontstatus == 1)).filter(
                             (Res_line.kontignr < 0) & (Res_line.gastnr == kontline.gastnr) & (Res_line.resstatus == 9)).order_by(Res_line.ankunft, Res_line.abreise, Res_line.resnr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                        res_list = Res_list()
                        res_list_data.append(res_list)

                        res_list.flag = "c"
                        count = count + 1
                        res_list.count = count
                        s1 = " " + translateExtended ("ResNo", lvcarea, "") + " " + to_string(res_line.resnr, ">>>>>>9") + " " + translateExtended ("Arrival", lvcarea, "") + " " + to_string(res_line.ankunft) + " " + translateExtended ("Qty", lvcarea, "") + " " + to_string(res_line.zimmeranz, "99") + " " + translateExtended ("Pax", lvcarea, "") + " " + to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) + " " + translateExtended ("Departure", lvcarea, "") + " " + to_string(res_line.abreise) + " " + translateExtended ("ID", lvcarea, "") + " " + to_string(reservation.useridanlage, "x(2)") + " " + translateExtended ("ChgID", lvcarea, "") + " " + to_string(res_line.changed_id, "x(2)")

                        if res_line.bemerk != "":
                            res_list = Res_list()
                            res_list_data.append(res_list)

                            count = count + 1
                            res_list.flag = "r"
                            s1 = translateExtended ("Comment :", lvcarea, "") + " " + res_line.bemerk
                    i = 1
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    str = translateExtended ("Cancelled :", lvcarea, "") + " "

                    for res_list in query(res_list_data, filters=(lambda res_list: res_list.flag.lower()  == ("c").lower()), sort_by=[("count",False)]):

                        if i > 1:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            str = " " + s1
                        else:
                            str = str + s1
                        str_detail.cancel_res = s1


                        i = i + 1
                output_list = Output_list()
                output_list_data.append(output_list)

                for i in range(1,108 + 1) :
                    str = str + "="
                output_list = Output_list()
                output_list_data.append(output_list)

        count = 2
        for i in range(1,31 + 1) :

            if t_anz0[i - 1] >= 100:
                count = 3

        if count == 3:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_data.append(output_list)

            while datum <= to_date:

                if i <= 1:
                    str = to_string(translateExtended ("Total Reserve", lvcarea, "") , "x(14)") + to_string(t_anz0[i - 1], "->>>9")
                else:
                    str = str + to_string(t_anz0[i - 1], "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
            i = 2
            datum = from_date + timedelta(days=1)
            output_list = Output_list()
            output_list_data.append(output_list)

            str = " "
            while datum <= to_date:
                str = str + to_string(t_anz0[i - 1], "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
        else:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_data.append(output_list)

            while datum <= to_date:

                if i <= 1:
                    str = to_string(translateExtended ("Total Reserve", lvcarea, "") , "x(15)") + to_string(t_anz0[i - 1], "->9")
                else:
                    str = str + to_string(t_anz0[i - 1], "->9")
                i = i + 1
                datum = datum + timedelta(days=1)
        count = 2
        for i in range(1,31 + 1) :

            if t_anz1[i - 1] >= 100:
                count = 3

        if count == 3:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_data.append(output_list)

            while datum <= to_date:

                if i <= 1:
                    str = to_string(translateExtended ("Used Reserve", lvcarea, "") , "x(15)") + to_string(t_anz1[i - 1], "->>>>9")
                else:
                    str = str + to_string(t_anz1[i - 1], "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
            i = 2
            datum = from_date + timedelta(days=1)
            output_list = Output_list()
            output_list_data.append(output_list)

            str = " "
            while datum <= to_date:
                str = str + to_string(t_anz1[i - 1], "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
        else:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_data.append(output_list)

            while datum <= to_date:

                if i <= 1:
                    str = to_string(translateExtended ("Used Reserve", lvcarea, "") , "x(15)") + to_string(t_anz1[i - 1], "->9")
                else:
                    str = str + to_string(t_anz1[i - 1], "->9")
                i = i + 1
                datum = datum + timedelta(days=1)
        count = 2
        for i in range(1,31 + 1) :

            if t_anz2[i - 1] >= 100:
                count = 3

        if count == 3:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_data.append(output_list)

            while datum <= to_date:

                if t_anz2[i - 1] > 0:

                    if i <= 1:
                        str = to_string(translateExtended ("Not used", lvcarea, "") , "x(15)") + to_string(t_anz2[i - 1], "->>>>9")
                    else:
                        str = str + to_string(t_anz2[i - 1], "->>>>9")
                else:

                    if i <= 1:
                        str = to_string(translateExtended ("Not used", lvcarea, "") , "x(15)") + to_string(0, "->>>>9")
                    else:
                        str = str + to_string(0, "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
            i = 2
            datum = from_date + timedelta(days=1)
            output_list = Output_list()
            output_list_data.append(output_list)

            str = " "
            while datum <= to_date:
                str = str + to_string(t_anz2[i - 1], "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
        else:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_data.append(output_list)

            while datum <= to_date:

                if t_anz2[i - 1] > 0:

                    if i <= 1:
                        str = to_string(translateExtended ("Not used", lvcarea, "") , "x(15)") + to_string(t_anz2[i - 1], "->9")
                    else:
                        str = str + to_string(t_anz2[i - 1], "->9")
                else:

                    if i <= 1:
                        str = to_string(translateExtended ("Not used", lvcarea, "") , "x(15)") + to_string(0, "->9")
                    else:
                        str = str + to_string(0, "->9")
                i = i + 1
                datum = datum + timedelta(days=1)


    def create_alist():

        nonlocal str_detail_data, str_summary_data, sum_list_data, lvcarea, loopi, str_parse, bediener, kontline, guest, zimkateg, guest_pr, res_line, reservation
        nonlocal pvilanguage, delflag, from_date, to_date, ci_date, resflag1, gflag, cflag, from_name, to_name
        nonlocal usr


        nonlocal sum_list, output_list, str_detail, str_summary, k_list, res_list, usr, allot_list
        nonlocal sum_list_data, output_list_data, str_detail_data, str_summary_data, k_list_data, res_list_data, allot_list_data

        curr_code:string = ""
        d:date = None
        d1:date = None
        d2:date = None
        i:int = 0

        kontline_obj_list = {}
        kontline = Kontline()
        guest = Guest()
        for kontline.gastnr, kontline.kontcode, kontline.bediener_nr, kontline.ankunft, kontline.zikatnr, kontline.arrangement, kontline.erwachs, kontline.kind1, kontline.ruecktage, kontline.overbooking, kontline.abreise, kontline.useridanlage, kontline.resdat, kontline.bemerk, kontline.zimmeranz, kontline._recid, guest.gastnr, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.wohnort, guest.plz, guest._recid in db_session.query(Kontline.gastnr, Kontline.kontcode, Kontline.bediener_nr, Kontline.ankunft, Kontline.zikatnr, Kontline.arrangement, Kontline.erwachs, Kontline.kind1, Kontline.ruecktage, Kontline.overbooking, Kontline.abreise, Kontline.useridanlage, Kontline.resdat, Kontline.bemerk, Kontline.zimmeranz, Kontline._recid, Guest.gastnr, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.wohnort, Guest.plz, Guest._recid).join(Guest,(Guest.gastnr == Kontline.gastnr) & (Guest.name >= (from_name).lower()) & (Guest.name <= (to_name).lower())).filter(
                 (Kontline.betriebsnr == 1) & (not_ (Kontline.ankunft > to_date)) & (not_ (Kontline.abreise < from_date)) & (Kontline.kontstatus == 1)).order_by(Guest.name, Kontline.kontcode, Kontline.ankunft).all():
            if kontline_obj_list.get(kontline._recid):
                continue
            else:
                kontline_obj_list[kontline._recid] = True

            if curr_code != kontline.kontcode:

                usr = get_cache (Bediener, {"nr": [(eq, kontline.bediener_nr)]})
                curr_code = kontline.kontcode
                k_list = K_list()
                k_list_data.append(k_list)

                k_list.gastnr = guest.gastnr
                k_list.kontcode = curr_code
                k_list.ankunft = kontline.ankunft
                k_list.zikatnr = kontline.zikatnr
                k_list.argt = kontline.arrangement
                k_list.erwachs = kontline.erwachs
                k_list.kind1 = kontline.kind1
                k_list.ruecktage = kontline.ruecktage
                k_list.overbooking = kontline.overbooking
                k_list.abreise = kontline.abreise
                k_list.useridanlage = kontline.useridanlage
                k_list.resdat = kontline.resdat
                k_list.bemerk = kontline.bemerk

                if usr:
                    k_list.bediener_nr = usr.nr
            else:
                k_list.abreise = kontline.abreise

            if from_date > kontline.ankunft:
                d1 = from_date
            else:
                d1 = kontline.ankunft

            if to_date < kontline.abreise:
                d2 = to_date
            else:
                d2 = kontline.abreise
            i = (d1 - from_date).days
            for d in date_range(d1,d2) :
                sum_list = Sum_list()
                sum_list_data.append(sum_list)


                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, k_list.zikatnr)]})
                sum_list.datum = d
                sum_list.gastnr = kontline.gastnr
                sum_list.firma = guest.name
                sum_list.kontcode = kontline.kontcode
                sum_list.zikatnr = kontline.zikatnr
                sum_list.gloanz = kontline.zimmeranz
                sum_list.erwachs = kontline.erwachs
                sum_list.kind1 = kontline.kind1

                if zimkateg:
                    sum_list.kurzbez = zimkateg.kurzbez


                i = i + 1

                if d >= kontline.ankunft and d <= kontline.abreise:
                    k_list.zimmeranz[i - 1] = kontline.zimmeranz

    create_list(delflag)
    str_summary = Str_summary()
    str_summary_data.append(str_summary)


    for output_list in query(output_list_data):

        if matches(output_list.str,r"*total reserve*"):
            str_parse = substring(output_list.str, 14)
            for loopi in range(1,num_entries(str_parse, " ")  + 1) :

                if loopi <= 31:
                    str_summary.total_reserve[loopi - 1] = entry(loopi - 1, str_parse, " ")

        elif matches(output_list.str,r"*used reserve*"):
            str_parse = substring(output_list.str, 14)
            for loopi in range(1,num_entries(str_parse, " ")  + 1) :

                if loopi <= 31:
                    str_summary.used_reserve[loopi - 1] = entry(loopi - 1, str_parse, " ")

        elif matches(output_list.str,r"*not used*"):
            str_parse = substring(output_list.str, 14)
            for loopi in range(1,num_entries(str_parse, " ")  + 1) :

                if loopi <= 31:
                    str_summary.not_used[loopi - 1] = entry(loopi - 1, str_parse, " ")

    return generate_output()