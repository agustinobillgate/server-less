from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.res_overbookbl import res_overbookbl
from models import Kontline, Bediener, Htparam, Zimkateg, Res_line, Queasy, Counters

def allot_overbookbl(pvilanguage:int, res_mode:str, curr_resnr:int, curr_reslinnr:int, kontignr:int, zikatnr:int, bed_setup:int, argt:str, erwachs:int, ankunft:date, abreise:date, qty:int, user_init:str):
    error_flag = False
    msg_str = ""
    lvcarea:str = "allot_overbook"
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

    kline = allot_list = s_list = s_list1 = None

    allot_list_list, Allot_list = create_model("Allot_list", {"k_recid":int, "datum":date, "allot_exist":bool, "anz":int, "overbook":int, "cutoff":int})
    s_list_list, S_list = create_model("S_list", {"datum":date, "tag":str, "qty":int, "occ":int, "vac":int, "ovb":int})

    Kline = Kontline
    S_list1 = S_list
    s_list1_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal kline, s_list1


        nonlocal kline, allot_list, s_list, s_list1
        nonlocal allot_list_list, s_list_list
        return {"error_flag": error_flag, "msg_str": msg_str}

    def check_allotment():

        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal kline, s_list1


        nonlocal kline, allot_list, s_list, s_list1
        nonlocal allot_list_list, s_list_list

        anz:int = 0
        datum:date = None
        Kline = Kontline

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == curr_resnr) &  (Res_line.reslinnr == curr_reslinnr)).first()
        for datum in range(ankunft,(abreise - 1)  + 1) :
            allot_list = Allot_list()
            allot_list_list.append(allot_list)

            allot_list.datum = datum

            kline = db_session.query(Kline).filter(
                    (Kline.kontcode == kontline.kontcode) &  (Kline.kontstatus == 1) &  (Kline.datum >= Kline.ankunft) &  (Kline.datum <= Kline.abreise)).first()

            if kline and kline.rueckdatum != None and ci_date > kline.rueckdatum and (res_mode.lower()  == "new" or res_mode.lower().lower()  == "insert"):
                error_flag = True
                msg_str = translateExtended ("Today's date is beyond allotment's Cut_Off_Date :", lvcarea, "") + to_string(kline.rueckdatum)

                return

            if kline and kline.ruecktage > 0 and (datum - ci_date) < kline.ruecktage and (res_mode.lower()  == "new" or res_mode.lower().lower()  == "insert"):
                error_flag = True
                msg_str = translateExtended ("arrival less than allotment's Cut_Off_Days :", lvcarea, "") + to_string(kline.ruecktage)

                return

            if kline:

                if res_mode.lower()  == "inhouse":
                    anz = 0

                elif res_mode.lower()  == "modify" or res_mode.lower()  == "new":

                    if res_line.kontignr < 0:
                        anz = 0
                    else:
                        anz = kline.ruecktage

                if datum >= (ci_date + anz):
                    allot_list.allot_exist = True
                    allot_list.k_recid = kline._recid
                    allot_list.anz = kline.zimmeranz - qty
                    allot_list.overbook = kline.overbooking
                    allot_list.cutoff = kline.ruecktage

        allot_list = query(allot_list_list, filters=(lambda allot_list :not allot_list.allot_exist), first=True)

        if allot_list:
            error_flag = True
            msg_str = translateExtended ("Date out of period range found", lvcarea, "") + " - " + to_string(allot_list.datum)

            return

        if kontignr > 0:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 147) &  (Queasy.number1 == kontline.gastnr)).first()

            if not queasy:

                res_line_obj_list = []
                for res_line, kline in db_session.query(Res_line, Kline).join(Kline,(Kline.kontignr == Res_line.kontignr) &  (Kline.kontcode == kontline.kontcode) &  (Kline.kontstatus == 1)).filter(
                        (Res_line.kontignr > 0) &  (Res_line.gastnr == kontline.gastnr) &  (Res_line.active_flag < 2) &  (Res_line.resstatus <= 6)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                        1
                    else:
                        for datum in range(res_line.ankunft,(res_line.abreise - 1)  + 1) :

                            allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == datum), first=True)

                            if allot_list:
                                allot_list.anz = allot_list.anz - res_line.zimmeranz

            else:

                res_line_obj_list = []
                for res_line, kline in db_session.query(Res_line, Kline).join(Kline,(Kline.kontignr == Res_line.kontignr) &  (Kline.kontcode == kontline.kontcode) &  (Kline.kontstatus == 1)).filter(
                        (Res_line.kontignr > 0) &  (Res_line.active_flag < 2) &  (Res_line.resstatus <= 6)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                        1
                    else:
                        for datum in range(res_line.ankunft,(res_line.abreise - 1)  + 1) :

                            allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == datum), first=True)

                            if allot_list:
                                allot_list.anz = allot_list.anz - res_line.zimmeranz


        elif kontignr < 0:

            res_line_obj_list = []
            for res_line, kline in db_session.query(Res_line, Kline).join(Kline,(Kline.kontignr == - Res_line.kontignr) &  (Kline.kontcode == kontline.kontcode) &  (Kline.kontstatus == 1)).filter(
                    (Res_line.kontignr < 0) &  (Res_line.active_flag < 2) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 3) &  (Res_line.resstatus != 4)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                    1
                else:
                    for datum in range(res_line.ankunft,(res_line.abreise - 1)  + 1) :

                        allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == datum), first=True)

                        if allot_list:
                            allot_list.anz = allot_list.anz - res_line.zimmeranz


        allot_list = query(allot_list_list, filters=(lambda allot_list :(allot_list.anz + allot_list.overbook) < 0), first=True)

        if allot_list:
            error_flag = True

            if res_mode.lower()  == "inhouse":
                cutoff_date = ci_date
            else:
                cutoff_date = ankunft - allot_list.cutoff

            if kontignr > 0:
                msg_str = translateExtended ("Allotment: Overbooking found on :", lvcarea, "") + to_string(allot_list.datum) + chr(10) + translateExtended ("Cut_off Date :", lvcarea, "") + to_string(cutoff_date) + chr(10) + translateExtended ("Maxium Overbooking :", lvcarea, "") + to_string(allot_list.overbook) + "  " + translateExtended ("Actual Overbooking :", lvcarea, "") + to_string(- allot_list.anz)

            elif kontignr < 0:
                msg_str = translateExtended ("Global Reservation: Overbooking found on :", lvcarea, "") + to_string(allot_list.datum) + chr(10) + translateExtended ("Maxium Overbooking :", lvcarea, "") + to_string(allot_list.overbook) + "  " + translateExtended ("Actual Overbooking :", lvcarea, "") + to_string(- allot_list.anz)

            if substring(bediener.perm, 35, 1) >= "2":
                msg_str = msg_str + chr(2) + "&Q" + translateExtended ("Do you wish to modify the record?", lvcarea, "")

            return

        allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.anz < 0), first=True)

        if allot_list:

            if kontignr > 0:
                msg_str = "&W" + (translateExtended ("Allotment: Overbooking  ==  ", lvcarea, "") + to_string(- allot_list.anz) + " - " + to_string(allot_list.datum)) + "\\"

            elif kontignr < 0:
                msg_str = "&W" + (translateExtended ("Global Reservation: Overbooking  ==  ", lvcarea, "") + to_string(- allot_list.anz) + " - " + to_string(allot_list.datum)) + "\\"

    def create_slist():

        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal kline, s_list1


        nonlocal kline, allot_list, s_list, s_list1
        nonlocal allot_list_list, s_list_list

        weekdays:[str] = ["", "", "", "", "", "", "", "", ""]
        d:date = None
        arrival:date = None
        depart:date = None
        Kline = Kontline
        qty1 = qty

        if res_mode.lower()  == "modify":

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == curr_resnr) &  (Res_line.reslinnr == curr_reslinnr)).first()

            if res_line.kontignr != 0:

                kline = db_session.query(Kline).filter(
                        (Kline.kontignr == res_line.kontignr) &  (Kline.kontstatus == 1)).first()

                if kline and kline.kontcode == kontline.kontcode:
                    qty1 = qty - res_line.zimmeranz
        for d in range(kontline.ankunft,kontline.abreise + 1) :
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.datum = d
            s_list.qty = kontline.zimmeranz
            s_list.vac = kontline.zimmeranz
            s_list.tag = weekdays[get_weekday(s_list.datum) - 1]

            if d >= ankunft and d <= (abreise - 1):
                s_list.vac = s_list.vac - qty1
                s_list.occ = s_list.occ + qty1

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 147) &  (Queasy.number1 == kontline.gastnr)).first()

        if not queasy:

            res_line_obj_list = []
            for res_line, kline in db_session.query(Res_line, Kline).join(Kline,(Kline.kontignr == Res_line.kontignr) &  (Kline.kontcode == kontline.kontcode) &  (Kline.kontstatus == 1)).filter(
                    (Res_line.kontignr > 0) &  (Res_line.gastnr == kontline.gastnr) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                    arrival = ankunft
                    depart = abreise


                else:
                    arrival = res_line.ankunft
                    depart = res_line.abreise

                if depart <= kontline.ankunft or arrival > kontline.abreise:
                    1
                else:
                    for d in range(arrival,(depart - 1)  + 1) :

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.datum == d), first=True)

                        if s_list:
                            s_list.vac = s_list.vac - res_line.zimmeranz
                            s_list.occ = s_list.occ + res_line.zimmeranz

        else:

            res_line_obj_list = []
            for res_line, kline in db_session.query(Res_line, Kline).join(Kline,(Kline.kontignr == Res_line.kontignr) &  (Kline.kontcode == kontline.kontcode) &  (Kline.kontstatus == 1)).filter(
                    (Res_line.kontignr > 0) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                    arrival = ankunft
                    depart = abreise


                else:
                    arrival = res_line.ankunft
                    depart = res_line.abreise

                if depart <= kontline.ankunft or arrival > kontline.abreise:
                    1
                else:
                    for d in range(arrival,(depart - 1)  + 1) :

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.datum == d), first=True)

                        if s_list:
                            s_list.vac = s_list.vac - res_line.zimmeranz
                            s_list.occ = s_list.occ + res_line.zimmeranz


        for s_list in query(s_list_list, filters=(lambda s_list :s_list.vac < 0)):
            s_list.ovb = - s_list.vac
            s_list.vac = 0

    def create_slist1():

        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal kline, s_list1


        nonlocal kline, allot_list, s_list, s_list1
        nonlocal allot_list_list, s_list_list

        weekdays:[str] = ["", "", "", "", "", "", "", "", ""]
        d:date = None
        arrival:date = None
        depart:date = None
        Kline = Kontline
        qty1 = qty

        if res_mode.lower()  == "modify":

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == curr_resnr) &  (Res_line.reslinnr == curr_reslinnr)).first()
            qty1 = qty - res_line.zimmeranz
        for d in range(ankunft,abreise + 1) :

            kline = db_session.query(Kline).filter(
                    (Kline.kontcode == kontline.kontcode) &  (Kline.ankunft == d)).first()

            if kline:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.datum = d
                s_list.qty = kline.zimmeranz
                s_list.vac = kline.zimmeranz - qty1
                s_list.tag = weekdays[get_weekday(s_list.datum) - 1]
                s_list.occ = qty1

        res_line_obj_list = []
        for res_line, kline in db_session.query(Res_line, Kline).join(Kline,(Kline.kontignr == - Res_line.kontignr) &  (Kline.kontcode == kontline.kontcode) &  (Kline.kontstatus == 1)).filter(
                (Res_line.kontignr < 0) &  (Res_line.gastnr == kontline.gastnr) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if res_line.resnr == curr_resnr and res_line.reslinnr == curr_reslinnr:
                arrival = ankunft
                depart = abreise
            else:
                arrival = res_line.ankunft
                depart = res_line.abreise
            for d in range(arrival,(depart - 1)  + 1) :

                s_list = query(s_list_list, filters=(lambda s_list :s_list.datum == d), first=True)

                if s_list:
                    s_list.vac = s_list.vac - res_line.zimmeranz
                    s_list.occ = s_list.occ + res_line.zimmeranz

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.vac < 0)):
            s_list.ovb = - s_list.vac
            s_list.vac = 0

    def check_slist():

        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal kline, s_list1


        nonlocal kline, allot_list, s_list, s_list1
        nonlocal allot_list_list, s_list_list

        changed = False
        anz:int = 0
        d1:date = None
        i:int = 0

        def generate_inner_output():
            return changed
        S_list1 = S_list
        Kline = Kontline

        for s_list1 in query(s_list1_list):
            i = i + 1

            if anz == 0:
                anz = s_list1.qty
                d1 = s_list1.datum

            if s_list1.qty != anz:
                changed = True

                counters = db_session.query(Counters).filter(
                        (Counters.counter_no == 10)).first()
                counters = counters + 1

                counters = db_session.query(Counters).first()
                kline = Kline()
                db_session.add(kline)

                kline.betriebsnr = to_int(kontignr < 0)
                kline.kontignr = counters
                kline.gastnr = kontline.gastnr
                kline.useridanlage = ""
                kline.kontcode = kontline.kontcode
                kline.ankunft = d1
                kline.abreise = s_list1.datum - 1
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

            kline = db_session.query(Kline).filter(
                    (Kline._recid == kontline._recid)).first()
            kline.ankunft = d1
            kline.zimmeranz = anz

            kline = db_session.query(Kline).first()

        elif i == 1:

            kline = db_session.query(Kline).filter(
                    (Kline._recid == kontline._recid)).first()

            if kline.zimmeranz != anz:
                changed = True

                kline = db_session.query(Kline).first()
                kline.ankunft = d1
                kline.zimmeranz = anz

                kline = db_session.query(Kline).first()


        return generate_inner_output()

    def check_slist1():

        nonlocal error_flag, msg_str, lvcarea, cutoff_date, changed, ci_date, overbook, datum, error_code, qty1, answer, res_overbook, overmax, overanz, overdate, incl_allot, zimkateg_overbook, kontline, bediener, htparam, zimkateg, res_line, queasy, counters
        nonlocal kline, s_list1


        nonlocal kline, allot_list, s_list, s_list1
        nonlocal allot_list_list, s_list_list

        changed = False

        def generate_inner_output():
            return changed
        S_list1 = S_list
        Kline = Kontline

        for s_list1 in query(s_list1_list):

            kline = db_session.query(Kline).filter(
                    (Kline.kontcode == kontline.kontcode) &  (Kline.ankunft == s_list1.datum)).first()

            if kline and kline.zimmeranz < s_list1.qty:
                changed = True

                kline = db_session.query(Kline).first()
                kline.zimmeranz = s_list1.qty

                kline = db_session.query(Kline).first()


        return generate_inner_output()


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if kontignr > 0:

        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == kontignr) &  (Kontline.kontstatus == 1)).first()

        if not kontline:
            error_flag = True
            msg_str = translateExtended ("Allotment does not exist.", lvcarea, "")

            return generate_output()

    elif kontignr < 0:

        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == - kontignr) &  (Kontline.kontstatus == 1)).first()

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

        if substring(bediener.perm, 35, 1) >= "1":

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == kontline.zikatnr)).first()
            res_overbook, overmax, overanz, overdate, incl_allot, msg_str, zimkateg_overbook = get_output(res_overbookbl(pvilanguage, res_mode, curr_resnr, curr_reslinnr, ankunft, abreise, qty, zimkateg.kurzbez, bed_setup, False))

        if not overmax:
            error_flag = True
            msg_str = translateExtended ("Room Type does not match to selected Code :", lvcarea, "") + to_string(kontline.kontignr)

            return generate_output()

    if kontline.arrangement.lower()  != "" and kontline.arrangement.lower()  != (argt).lower() :
        error_flag = True
        msg_str = translateExtended ("Arrangement does not match to selected Code :", lvcarea, "") + to_string(kontline.kontignr)

        return generate_output()

    if res_mode.lower()  == "inhouse" and kontignr > 0:

        return generate_output()
    check_allotment()

    return generate_output()