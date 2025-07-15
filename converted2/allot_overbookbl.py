#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.res_overbookbl import res_overbookbl
from models import Kontline, Bediener, Htparam, Zimkateg, Res_line, Queasy, Counters

def allot_overbookbl(pvilanguage:int, res_mode:string, curr_resnr:int, curr_reslinnr:int, kontignr:int, zikatnr:int, bed_setup:int, argt:string, erwachs:int, ankunft:date, abreise:date, qty:int, user_init:string):

    prepare_cache ([Kontline, Bediener, Htparam, Zimkateg, Res_line, Counters])

    error_flag = False
    msg_str = ""
    lvcarea:string = "allot-overbook"
    cutoff_date:date = None
    changed:bool = False
    ci_date:date = None
    overbook:int = 0
    datum:date = None
    error_code:int = 0
    qty1:int = 0
    answer:bool = False
    res_overbook:bool = False
    overmax:bool = False
    overanz:int = 0
    overdate:date = None
    incl_allot:bool = False
    zimkateg_overbook:int = 0
    kontline = bediener = htparam = zimkateg = res_line = queasy = counters = None

    kline = allot_list = s_list = s_list1 = s_list1 = None

    allot_list_data, Allot_list = create_model("Allot_list", {"k_recid":int, "datum":date, "allot_exist":bool, "anz":int, "overbook":int, "cutoff":int})
    s_list_data, S_list = create_model("S_list", {"datum":date, "tag":string, "qty":int, "occ":int, "vac":int, "ovb":int})

    Kline = create_buffer("Kline",Kontline)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal pvilanguage, res_mode, curr_resnr, curr_reslinnr, kontignr, zikatnr, bed_setup, argt, erwachs, ankunft, abreise, qty, user_init
        nonlocal kline


        nonlocal kline, allot_list, s_list, s_list1, s_list1
        nonlocal allot_list_data, s_list_data

        return {"error_flag": error_flag, "msg_str": msg_str}

    def check_allotment():

        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal pvilanguage, res_mode, curr_resnr, curr_reslinnr, kontignr, zikatnr, bed_setup, argt, erwachs, ankunft, abreise, qty, user_init
        nonlocal kline


        nonlocal kline, allot_list, s_list, s_list1, s_list1
        nonlocal allot_list_data, s_list_data

        anz:int = 0
        datum:date = None
        kline = None
        Kline =  create_buffer("Kline",Kontline)

        res_line = get_cache (Res_line, {"resnr": [(eq, curr_resnr)],"reslinnr": [(eq, curr_reslinnr)]})
        for datum in date_range(ankunft,(abreise - 1)) :
            allot_list = Allot_list()
            allot_list_data.append(allot_list)

            allot_list.datum = datum

            kline = get_cache (Kontline, {"kontcode": [(eq, kontline.kontcode)],"kontstatus": [(eq, 1)],"ankunft": [(le, datum)],"abreise": [(ge, datum)]})

            if kline and kline.rueckdatum != None and ci_date > kline.rueckdatum and (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()):
                error_flag = True
                msg_str = translateExtended ("Today's date is beyond allotment's Cut-Off-Date :", lvcarea, "") + to_string(kline.rueckdatum)

                return

            if kline and kline.ruecktage > 0 and (datum - ci_date) < kline.ruecktage and (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()):
                error_flag = True
                msg_str = translateExtended ("arrival less than allotment's Cut-Off-Days :", lvcarea, "") + to_string(kline.ruecktage)

                return

            if kline:

                if res_mode.lower()  == ("inhouse").lower() :
                    anz = 0

                elif res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("new").lower() :

                    if res_line.kontignr < 0:
                        anz = 0
                    else:
                        anz = kline.ruecktage

                if datum >= (ci_date + timedelta(days=anz)):
                    allot_list.allot_exist = True
                    allot_list.k_recid = kline._recid
                    allot_list.anz = kline.zimmeranz - qty
                    allot_list.overbook = kline.overbooking
                    allot_list.cutoff = kline.ruecktage

        allot_list = query(allot_list_data, filters=(lambda allot_list: not allot_list.allot_exist), first=True)

        if allot_list:
            error_flag = True
            msg_str = translateExtended ("Date out of period range found", lvcarea, "") + " - " + to_string(allot_list.datum)

            return

        if kontignr > 0:

            queasy = get_cache (Queasy, {"key": [(eq, 147)],"number1": [(eq, kontline.gastnr)]})

            if not queasy:

                res_line_obj_list = {}
                res_line = Res_line()
                kline = Kontline()
                for res_line.reslinnr, res_line.zimmeranz, res_line.kontignr, res_line.ankunft, res_line.abreise, res_line.resnr, res_line._recid, kline.kontcode, kline.gastnr, kline.zimmeranz, kline.ankunft, kline.abreise, kline.zikatnr, kline.arrangement, kline.erwachs, kline.kind1, kline.overbooking, kline.ruecktage, kline.rueckdatum, kline.ansprech, kline.bemerk, kline._recid, kline.kontignr, kline.betriebsnr, kline.useridanlage, kline.bediener_nr, kline.resdat in db_session.query(Res_line.reslinnr, Res_line.zimmeranz, Res_line.kontignr, Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line._recid, Kline.kontcode, Kline.gastnr, Kline.zimmeranz, Kline.ankunft, Kline.abreise, Kline.zikatnr, Kline.arrangement, Kline.erwachs, Kline.kind1, Kline.overbooking, Kline.ruecktage, Kline.rueckdatum, Kline.ansprech, Kline.bemerk, Kline._recid, Kline.kontignr, Kline.betriebsnr, Kline.useridanlage, Kline.bediener_nr, Kline.resdat).join(Kline,(Kline.kontignr == Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1)).filter(
                         (Res_line.kontignr > 0) & (Res_line.gastnr == kontline.gastnr) & (Res_line.active_flag < 2) & (Res_line.resstatus <= 6)).order_by(Res_line._recid).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                        pass
                    else:
                        for datum in date_range(res_line.ankunft,(res_line.abreise - 1)) :

                            allot_list = query(allot_list_data, filters=(lambda allot_list: allot_list.datum == datum), first=True)

                            if allot_list:
                                allot_list.anz = allot_list.anz - res_line.zimmeranz

            else:

                res_line_obj_list = {}
                res_line = Res_line()
                kline = Kontline()
                for res_line.reslinnr, res_line.zimmeranz, res_line.kontignr, res_line.ankunft, res_line.abreise, res_line.resnr, res_line._recid, kline.kontcode, kline.gastnr, kline.zimmeranz, kline.ankunft, kline.abreise, kline.zikatnr, kline.arrangement, kline.erwachs, kline.kind1, kline.overbooking, kline.ruecktage, kline.rueckdatum, kline.ansprech, kline.bemerk, kline._recid, kline.kontignr, kline.betriebsnr, kline.useridanlage, kline.bediener_nr, kline.resdat in db_session.query(Res_line.reslinnr, Res_line.zimmeranz, Res_line.kontignr, Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line._recid, Kline.kontcode, Kline.gastnr, Kline.zimmeranz, Kline.ankunft, Kline.abreise, Kline.zikatnr, Kline.arrangement, Kline.erwachs, Kline.kind1, Kline.overbooking, Kline.ruecktage, Kline.rueckdatum, Kline.ansprech, Kline.bemerk, Kline._recid, Kline.kontignr, Kline.betriebsnr, Kline.useridanlage, Kline.bediener_nr, Kline.resdat).join(Kline,(Kline.kontignr == Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1)).filter(
                         (Res_line.kontignr > 0) & (Res_line.active_flag < 2) & (Res_line.resstatus <= 6)).order_by(Res_line._recid).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                        pass
                    else:
                        for datum in date_range(res_line.ankunft,(res_line.abreise - 1)) :

                            allot_list = query(allot_list_data, filters=(lambda allot_list: allot_list.datum == datum), first=True)

                            if allot_list:
                                allot_list.anz = allot_list.anz - res_line.zimmeranz


        elif kontignr < 0:

            res_line_obj_list = {}
            res_line = Res_line()
            kline = Kontline()
            for res_line.reslinnr, res_line.zimmeranz, res_line.kontignr, res_line.ankunft, res_line.abreise, res_line.resnr, res_line._recid, kline.kontcode, kline.gastnr, kline.zimmeranz, kline.ankunft, kline.abreise, kline.zikatnr, kline.arrangement, kline.erwachs, kline.kind1, kline.overbooking, kline.ruecktage, kline.rueckdatum, kline.ansprech, kline.bemerk, kline._recid, kline.kontignr, kline.betriebsnr, kline.useridanlage, kline.bediener_nr, kline.resdat in db_session.query(Res_line.reslinnr, Res_line.zimmeranz, Res_line.kontignr, Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line._recid, Kline.kontcode, Kline.gastnr, Kline.zimmeranz, Kline.ankunft, Kline.abreise, Kline.zikatnr, Kline.arrangement, Kline.erwachs, Kline.kind1, Kline.overbooking, Kline.ruecktage, Kline.rueckdatum, Kline.ansprech, Kline.bemerk, Kline._recid, Kline.kontignr, Kline.betriebsnr, Kline.useridanlage, Kline.bediener_nr, Kline.resdat).join(Kline,(Kline.kontignr == - Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1)).filter(
                     (Res_line.kontignr < 0) & (Res_line.active_flag < 2) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4)).order_by(Res_line._recid).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                    pass
                else:
                    for datum in date_range(res_line.ankunft,(res_line.abreise - 1)) :

                        allot_list = query(allot_list_data, filters=(lambda allot_list: allot_list.datum == datum), first=True)

                        if allot_list:
                            allot_list.anz = allot_list.anz - res_line.zimmeranz


        allot_list = query(allot_list_data, filters=(lambda allot_list:(allot_list.anz + allot_list.overbook) < 0), first=True)

        if allot_list:
            error_flag = True

            if res_mode.lower()  == ("inhouse").lower() :
                cutoff_date = ci_date
            else:
                cutoff_date = ankunft - timedelta(days=allot_list.cutoff)

            if kontignr > 0:
                msg_str = translateExtended ("Allotment: Overbooking found on :", lvcarea, "") + to_string(allot_list.datum) + chr_unicode(10) + translateExtended ("Cut-off Date :", lvcarea, "") + to_string(cutoff_date) + chr_unicode(10) + translateExtended ("Maxium Overbooking :", lvcarea, "") + to_string(allot_list.overbook) + " " + translateExtended ("Actual Overbooking :", lvcarea, "") + to_string(- allot_list.anz)

            elif kontignr < 0:
                msg_str = translateExtended ("Global Reservation: Overbooking found on :", lvcarea, "") + to_string(allot_list.datum) + chr_unicode(10) + translateExtended ("Maxium Overbooking :", lvcarea, "") + to_string(allot_list.overbook) + " " + translateExtended ("Actual Overbooking :", lvcarea, "") + to_string(- allot_list.anz)

            if substring(bediener.perm, 35, 1) >= ("2").lower() :
                msg_str = msg_str + chr_unicode(2) + "&Q" + translateExtended ("Do you wish to modify the record?", lvcarea, "")

            return

        allot_list = query(allot_list_data, filters=(lambda allot_list: allot_list.anz < 0), first=True)

        if allot_list:

            if kontignr > 0:
                msg_str = "&W" + (translateExtended ("Allotment: Overbooking = ", lvcarea, "") + to_string(- allot_list.anz) + " - " + to_string(allot_list.datum)) + "\\"

            elif kontignr < 0:
                msg_str = "&W" + (translateExtended ("Global Reservation: Overbooking = ", lvcarea, "") + to_string(- allot_list.anz) + " - " + to_string(allot_list.datum)) + "\\"


    def create_slist():

        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal pvilanguage, res_mode, curr_resnr, curr_reslinnr, kontignr, zikatnr, bed_setup, argt, erwachs, ankunft, abreise, qty, user_init
        nonlocal kline


        nonlocal kline, allot_list, s_list, s_list1, s_list1
        nonlocal allot_list_data, s_list_data

        weekdays:List[string] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        d:date = None
        arrival:date = None
        depart:date = None
        kline = None
        Kline =  create_buffer("Kline",Kontline)
        qty1 = qty

        if res_mode.lower()  == ("modify").lower() :

            res_line = get_cache (Res_line, {"resnr": [(eq, curr_resnr)],"reslinnr": [(eq, curr_reslinnr)]})

            if res_line.kontignr != 0:

                kline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"kontstatus": [(eq, 1)]})

                if kline and kline.kontcode == kontline.kontcode:
                    qty1 = qty - res_line.zimmeranz
        for d in date_range(kontline.ankunft,kontline.abreise) :
            s_list = S_list()
            s_list_data.append(s_list)

            s_list.datum = d
            s_list.qty = kontline.zimmeranz
            s_list.vac = kontline.zimmeranz
            s_list.tag = weekdays[get_weekday(s_list.datum) - 1]

            if d >= ankunft and d <= (abreise - timedelta(days=1)):
                s_list.vac = s_list.vac - qty1
                s_list.occ = s_list.occ + qty1

        queasy = get_cache (Queasy, {"key": [(eq, 147)],"number1": [(eq, kontline.gastnr)]})

        if not queasy:

            res_line_obj_list = {}
            res_line = Res_line()
            kline = Kontline()
            for res_line.reslinnr, res_line.zimmeranz, res_line.kontignr, res_line.ankunft, res_line.abreise, res_line.resnr, res_line._recid, kline.kontcode, kline.gastnr, kline.zimmeranz, kline.ankunft, kline.abreise, kline.zikatnr, kline.arrangement, kline.erwachs, kline.kind1, kline.overbooking, kline.ruecktage, kline.rueckdatum, kline.ansprech, kline.bemerk, kline._recid, kline.kontignr, kline.betriebsnr, kline.useridanlage, kline.bediener_nr, kline.resdat in db_session.query(Res_line.reslinnr, Res_line.zimmeranz, Res_line.kontignr, Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line._recid, Kline.kontcode, Kline.gastnr, Kline.zimmeranz, Kline.ankunft, Kline.abreise, Kline.zikatnr, Kline.arrangement, Kline.erwachs, Kline.kind1, Kline.overbooking, Kline.ruecktage, Kline.rueckdatum, Kline.ansprech, Kline.bemerk, Kline._recid, Kline.kontignr, Kline.betriebsnr, Kline.useridanlage, Kline.bediener_nr, Kline.resdat).join(Kline,(Kline.kontignr == Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1)).filter(
                     (Res_line.kontignr > 0) & (Res_line.gastnr == kontline.gastnr) & (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6)).order_by(Res_line._recid).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                    arrival = ankunft
                    depart = abreise


                else:
                    arrival = res_line.ankunft
                    depart = res_line.abreise

                if depart <= kontline.ankunft or arrival > kontline.abreise:
                    pass
                else:
                    for d in date_range(arrival,(depart - 1)) :

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.datum == d), first=True)

                        if s_list:
                            s_list.vac = s_list.vac - res_line.zimmeranz
                            s_list.occ = s_list.occ + res_line.zimmeranz

        else:

            res_line_obj_list = {}
            res_line = Res_line()
            kline = Kontline()
            for res_line.reslinnr, res_line.zimmeranz, res_line.kontignr, res_line.ankunft, res_line.abreise, res_line.resnr, res_line._recid, kline.kontcode, kline.gastnr, kline.zimmeranz, kline.ankunft, kline.abreise, kline.zikatnr, kline.arrangement, kline.erwachs, kline.kind1, kline.overbooking, kline.ruecktage, kline.rueckdatum, kline.ansprech, kline.bemerk, kline._recid, kline.kontignr, kline.betriebsnr, kline.useridanlage, kline.bediener_nr, kline.resdat in db_session.query(Res_line.reslinnr, Res_line.zimmeranz, Res_line.kontignr, Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line._recid, Kline.kontcode, Kline.gastnr, Kline.zimmeranz, Kline.ankunft, Kline.abreise, Kline.zikatnr, Kline.arrangement, Kline.erwachs, Kline.kind1, Kline.overbooking, Kline.ruecktage, Kline.rueckdatum, Kline.ansprech, Kline.bemerk, Kline._recid, Kline.kontignr, Kline.betriebsnr, Kline.useridanlage, Kline.bediener_nr, Kline.resdat).join(Kline,(Kline.kontignr == Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1)).filter(
                     (Res_line.kontignr > 0) & (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6)).order_by(Res_line._recid).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                    arrival = ankunft
                    depart = abreise


                else:
                    arrival = res_line.ankunft
                    depart = res_line.abreise

                if depart <= kontline.ankunft or arrival > kontline.abreise:
                    pass
                else:
                    for d in date_range(arrival,(depart - 1)) :

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.datum == d), first=True)

                        if s_list:
                            s_list.vac = s_list.vac - res_line.zimmeranz
                            s_list.occ = s_list.occ + res_line.zimmeranz


        for s_list in query(s_list_data, filters=(lambda s_list: s_list.vac < 0)):
            s_list.ovb = - s_list.vac
            s_list.vac = 0


    def create_slist1():

        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal pvilanguage, res_mode, curr_resnr, curr_reslinnr, kontignr, zikatnr, bed_setup, argt, erwachs, ankunft, abreise, qty, user_init
        nonlocal kline


        nonlocal kline, allot_list, s_list, s_list1, s_list1
        nonlocal allot_list_data, s_list_data

        weekdays:List[string] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        d:date = None
        arrival:date = None
        depart:date = None
        kline = None
        Kline =  create_buffer("Kline",Kontline)
        qty1 = qty

        if res_mode.lower()  == ("modify").lower() :

            res_line = get_cache (Res_line, {"resnr": [(eq, curr_resnr)],"reslinnr": [(eq, curr_reslinnr)]})
            qty1 = qty - res_line.zimmeranz
        for d in date_range(ankunft,abreise) :

            kline = get_cache (Kontline, {"kontcode": [(eq, kontline.kontcode)],"ankunft": [(eq, d)]})

            if kline:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.datum = d
                s_list.qty = kline.zimmeranz
                s_list.vac = kline.zimmeranz - qty1
                s_list.tag = weekdays[get_weekday(s_list.datum) - 1]
                s_list.occ = qty1

        res_line_obj_list = {}
        res_line = Res_line()
        kline = Kontline()
        for res_line.reslinnr, res_line.zimmeranz, res_line.kontignr, res_line.ankunft, res_line.abreise, res_line.resnr, res_line._recid, kline.kontcode, kline.gastnr, kline.zimmeranz, kline.ankunft, kline.abreise, kline.zikatnr, kline.arrangement, kline.erwachs, kline.kind1, kline.overbooking, kline.ruecktage, kline.rueckdatum, kline.ansprech, kline.bemerk, kline._recid, kline.kontignr, kline.betriebsnr, kline.useridanlage, kline.bediener_nr, kline.resdat in db_session.query(Res_line.reslinnr, Res_line.zimmeranz, Res_line.kontignr, Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line._recid, Kline.kontcode, Kline.gastnr, Kline.zimmeranz, Kline.ankunft, Kline.abreise, Kline.zikatnr, Kline.arrangement, Kline.erwachs, Kline.kind1, Kline.overbooking, Kline.ruecktage, Kline.rueckdatum, Kline.ansprech, Kline.bemerk, Kline._recid, Kline.kontignr, Kline.betriebsnr, Kline.useridanlage, Kline.bediener_nr, Kline.resdat).join(Kline,(Kline.kontignr == - Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1)).filter(
                 (Res_line.kontignr < 0) & (Res_line.gastnr == kontline.gastnr) & (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                arrival = ankunft
                depart = abreise
            else:
                arrival = res_line.ankunft
                depart = res_line.abreise
            for d in date_range(arrival,(depart - 1)) :

                s_list = query(s_list_data, filters=(lambda s_list: s_list.datum == d), first=True)

                if s_list:
                    s_list.vac = s_list.vac - res_line.zimmeranz
                    s_list.occ = s_list.occ + res_line.zimmeranz

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.vac < 0)):
            s_list.ovb = - s_list.vac
            s_list.vac = 0


    def check_slist():

        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal pvilanguage, res_mode, curr_resnr, curr_reslinnr, kontignr, zikatnr, bed_setup, argt, erwachs, ankunft, abreise, qty, user_init
        nonlocal kline


        nonlocal kline, allot_list, s_list, s_list1, s_list1
        nonlocal allot_list_data, s_list_data

        changed = False
        anz:int = 0
        d1:date = None
        i:int = 0
        kline = None

        def generate_inner_output():
            return (changed)

        S_list1 = S_list
        s_list1_data = s_list_data
        Kline =  create_buffer("Kline",Kontline)

        for s_list1 in query(s_list1_data):
            i = i + 1

            if anz == 0:
                anz = s_list1.qty
                d1 = s_list1.datum

            if s_list1.qty != anz:
                changed = True

                counters = get_cache (Counters, {"counter_no": [(eq, 10)]})
                counters.counter = counters.counter + 1
                pass
                kline = Kontline()
                db_session.add(kline)

                kline.betriebsnr = to_int(kontignr < 0)
                kline.kontignr = counters.counter
                kline.gastnr = kontline.gastnr
                kline.useridanlage = ""
                kline.kontcode = kontline.kontcode
                kline.ankunft = d1
                kline.abreise = s_list1.datum - timedelta(days=1)
                kline.zikatnr = kontline.zikatnr
                kline.arrangement = kontline.arrangement
                kline.zimmeranz = anz
                kline.erwachs = kontline.erwachs
                kline.kind1 = kontline.kind1
                kline.overbooking = kontline.overbooking
                kline.ruecktage = kontline.ruecktage
                kline.rueckdatum = kontline.rueckdatum
                kline.ansprech = kontline.ansprech
                kline.bediener_nr = bediener.nr
                kline.resdat = get_current_date()
                kline.bemerk = kontline.bemerk


                d1 = s_list1.datum
                anz = s_list1.qty

        if changed:

            kline = get_cache (Kontline, {"_recid": [(eq, kontline._recid)]})
            kline.ankunft = d1
            kline.zimmeranz = anz


            pass

        elif i == 1:

            kline = get_cache (Kontline, {"_recid": [(eq, kontline._recid)]})

            if kline.zimmeranz != anz:
                changed = True
                pass
                kline.ankunft = d1
                kline.zimmeranz = anz


                pass

        return generate_inner_output()


    def check_slist1():

        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal pvilanguage, res_mode, curr_resnr, curr_reslinnr, kontignr, zikatnr, bed_setup, argt, erwachs, ankunft, abreise, qty, user_init
        nonlocal kline


        nonlocal kline, allot_list, s_list, s_list1, s_list1
        nonlocal allot_list_data, s_list_data

        changed = False
        kline = None

        def generate_inner_output():
            return (changed)

        S_list1 = S_list
        s_list1_data = s_list_data
        Kline =  create_buffer("Kline",Kontline)

        for s_list1 in query(s_list1_data):

            kline = get_cache (Kontline, {"kontcode": [(eq, kontline.kontcode)],"ankunft": [(eq, s_list1.datum)]})

            if kline and kline.zimmeranz < s_list1.qty:
                changed = True
                pass
                kline.zimmeranz = s_list1.qty


                pass

        return generate_inner_output()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if kontignr > 0:

        kontline = get_cache (Kontline, {"kontignr": [(eq, kontignr)],"kontstatus": [(eq, 1)]})

        if not kontline:
            error_flag = True
            msg_str = translateExtended ("Allotment does not exist.", lvcarea, "")

            return generate_output()

    elif kontignr < 0:

        kontline = get_cache (Kontline, {"kontignr": [(eq, - kontignr)],"kontstatus": [(eq, 1)]})

        if not kontline:
            error_flag = True
            msg_str = translateExtended ("Global Reservation does not exist.", lvcarea, "")

            return generate_output()

    if (kontignr > 0) and (kontline.erwachs != 0) and (kontline.erwachs < erwachs):
        error_flag = True
        msg_str = translateExtended ("Number of adults does not match to selected AllotNo :", lvcarea, "") + to_string(kontline.kontignr)

        return generate_output()

    if kontline.zikatnr != 0 and (kontline.zikatnr != zikatnr):
        overmax = False

        if substring(bediener.perm, 35, 1) >= ("1").lower() :

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, kontline.zikatnr)]})
            res_overbook, overmax, overanz, overdate, incl_allot, msg_str, zimkateg_overbook = get_output(res_overbookbl(pvilanguage, res_mode, curr_resnr, curr_reslinnr, ankunft, abreise, qty, zimkateg.kurzbez, bed_setup, False))

        if not overmax:
            error_flag = True
            msg_str = translateExtended ("Room Type does not match to selected Code :", lvcarea, "") + to_string(kontline.kontignr)

            return generate_output()

    if kontline.arrangement.lower()  != "" and kontline.arrangement.lower()  != (argt).lower() :
        error_flag = True
        msg_str = translateExtended ("Arrangement does not match to selected Code :", lvcarea, "") + to_string(kontline.kontignr)

        return generate_output()

    if res_mode.lower()  == ("inhouse").lower()  and kontignr > 0:

        return generate_output()
    check_allotment()

    return generate_output()