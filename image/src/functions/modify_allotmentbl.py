from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpdate import htpdate
from models import Res_line, Bediener, Kontline, Queasy, Counters

def modify_allotmentbl(i_case:int, user_init:str, reslin_list:[Reslin_list], s_list:[S_list]):
    overbook = 0
    allotcode = ""
    curr_resnr:int = 0
    curr_reslinnr:int = 0
    kontignr:int = 0
    zikatnr:int = 0
    argt:str = ""
    erwachs:int = 0
    ankunft:date = None
    abreise:date = None
    qty:int = 0
    qty1:int = 0
    res_line = bediener = kontline = queasy = counters = None

    reslin_list = s_list = kline = kline1 = kline2 = None

    reslin_list_list, Reslin_list = create_model_like(Res_line)
    s_list_list, S_list = create_model("S_list", {"datum":date, "tag":str, "qty":int, "occ":int, "vac":int, "ovb":int})

    Kline = Kontline
    Kline1 = Kontline
    Kline2 = Kontline

    db_session = local_storage.db_session

    def generate_output():
        nonlocal overbook, allotcode, curr_resnr, curr_reslinnr, kontignr, zikatnr, argt, erwachs, ankunft, abreise, qty, qty1, res_line, bediener, kontline, queasy, counters
        nonlocal kline, kline1, kline2


        nonlocal reslin_list, s_list, kline, kline1, kline2
        nonlocal reslin_list_list, s_list_list
        return {"overbook": overbook, "allotcode": allotcode}

    def create_slist():

        nonlocal overbook, allotcode, curr_resnr, curr_reslinnr, kontignr, zikatnr, argt, erwachs, ankunft, abreise, qty, qty1, res_line, bediener, kontline, queasy, counters
        nonlocal kline, kline1, kline2


        nonlocal reslin_list, s_list, kline, kline1, kline2
        nonlocal reslin_list_list, s_list_list

        weekdays:[str] = ["", "", "", "", "", "", "", "", ""]
        d:date = None
        arrival:date = None
        depart:date = None
        Kline = Kontline
        qty1 = qty

        if reslin_list.active_flag == 0:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == curr_resnr) &  (Res_line.reslinnr == curr_reslinnr)).first()

            if res_line.kontignr != 0:

                kline = db_session.query(Kline).filter(
                        (Kline.gastnr == res_line.gastnr) &  (Kline.kontignr == res_line.kontignr) &  (Kline.kontstatus == 1)).first()

                if kline and kline.kontcode == kontline.kontcode:
                    qty1 = qty - res_line.zimmeranz
        for d in range(ankunft,abreise - 1 + 1) :
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.datum = d
            s_list.qty = kontline.zimmeranz
            s_list.vac = kontline.zimmeranz
            s_list.tag = weekdays[get_weekday(s_list.datum) - 1]
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

        nonlocal overbook, allotcode, curr_resnr, curr_reslinnr, kontignr, zikatnr, argt, erwachs, ankunft, abreise, qty, qty1, res_line, bediener, kontline, queasy, counters
        nonlocal kline, kline1, kline2


        nonlocal reslin_list, s_list, kline, kline1, kline2
        nonlocal reslin_list_list, s_list_list

        weekdays:[str] = ["", "", "", "", "", "", "", "", ""]
        d:date = None
        arrival:date = None
        depart:date = None
        qty1:int = 0
        Kline = Kontline
        qty1 = qty

        if reslin_list.active_flag == 0:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == curr_resnr) &  (Res_line.reslinnr == curr_reslinnr)).first()
            qty1 = qty - res_line.zimmeranz
        for d in range(ankunft,abreise - 1 + 1) :

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

        nonlocal overbook, allotcode, curr_resnr, curr_reslinnr, kontignr, zikatnr, argt, erwachs, ankunft, abreise, qty, qty1, res_line, bediener, kontline, queasy, counters
        nonlocal kline, kline1, kline2


        nonlocal reslin_list, s_list, kline, kline1, kline2
        nonlocal reslin_list_list, s_list_list

        anz:int = 0
        d1:date = None
        i:int = 0
        changed:bool = False
        create_it:bool = False
        Kline = Kontline
        Kline1 = Kontline
        Kline2 = Kontline

        for s_list in query(s_list_list):
            create_it = True

            kline1 = db_session.query(Kline1).filter(
                    (Kline1.gastnr == kontline.gastnr) &  (Kline1.kontcode == kontline.kontcode) &  (Kline1.zikatnr == kontline.zikatnr) &  (Kline1.arrangement == kontline.arrangement) &  (Kline1.ankunft <= s_list.datum) &  (Kline1.abreise >= s_list.datum)).first()

            if s_list.qty != kline1.zimmeranz:
                changed = True

                if kline1.ankunft == s_list.datum and kline1.abreise == s_list.datum:
                    create_it = False
                    kline1.zimmeranz = s_list.qty

                elif kline1.ankunft == s_list.datum and kline1.abreise > s_list.datum:
                    kline1.abreise = s_list.datum + 1

                elif kline1.abreise == s_list.datum:
                    kline1.abreise = s_list.datum - 1


                else:

                    counters = db_session.query(Counters).filter(
                            (Counters.counter_no == 10)).first()
                    counters = counters + 1

                    counters = db_session.query(Counters).first()
                    kline2 = Kline2()
                    db_session.add(kline2)

                    buffer_copy(kline1, kline2,except_fields=["kontignr","ankunft"])
                    kline2.kontignr = counters
                    kline2.ankunft = s_list.datum + 1
                    kline2.bediener_nr = bediener.nr
                    kline2.resdat = get_current_date()
                    kline2.bemerk = kontline.bemerk


                    kline1.abreise = s_list.datum - 1

                if create_it:

                    counters = db_session.query(Counters).filter(
                            (Counters.counter_no == 10)).first()
                    counters = counters + 1

                    counters = db_session.query(Counters).first()
                    kline = Kline()
                    db_session.add(kline)

                    buffer_copy(kline1, kline,except_fields=["kontignr","ankunft","abreise"])
                    kline.kontignr = counters
                    kline.useridanlage = ""
                    kline.ankunft = s_list.datum
                    kline.abreise = s_list.datum
                    kline.zimmeranz = s_list.qty
                    kline.bediener_nr = bediener.nr
                    kline.resdat = get_current_date()
                    kline.bemerk = kontline.bemerk

        if changed:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 147) &  (Queasy.number1 == kontline.gastnr)).first()

            if queasy:

                for kline in db_session.query(Kline).filter(
                        (Kline.gastnr == kontline.gastnr) &  (Kline.kontstatus == 1) &  (Kline.kontcode == kontline.kontcode) &  (Kline._recid != kontline._recid)).all():
                    kline.pr_code = queasy.char3


    def check_slist1():

        nonlocal overbook, allotcode, curr_resnr, curr_reslinnr, kontignr, zikatnr, argt, erwachs, ankunft, abreise, qty, qty1, res_line, bediener, kontline, queasy, counters
        nonlocal kline, kline1, kline2


        nonlocal reslin_list, s_list, kline, kline1, kline2
        nonlocal reslin_list_list, s_list_list


        Kline = Kontline

        for s_list in query(s_list_list):

            kline = db_session.query(Kline).filter(
                    (Kline.kontcode == kontline.kontcode) &  (Kline.ankunft == s_list.datum)).first()

            if kline and kline.zimmeranz < s_list.qty:

                kline = db_session.query(Kline).first()
                kline.zimmeranz = s_list.qty

                kline = db_session.query(Kline).first()


    reslin_list = query(reslin_list_list, first=True)

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if reslin_list.kontignr > 0:

        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == reslin_list.kontignr) &  (Kontline.kontstatus == 1)).first()

    elif reslin_list.kontignr < 0:

        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == - reslin_list.kontignr) &  (Kontline.kontstatus == 1)).first()

    if not kontline:

        return generate_output()
    overbook = kontline.overbook
    allotcode = kontline.kontcode

    if i_case == 2:

        if reslin_list.kontignr > 0:
            check_slist()

        elif reslin_list.kontignr < 0:
            check_slist1()

        return generate_output()
    curr_resnr = reslin_list.resnr
    curr_reslinnr = reslin_list.reslinnr
    kontignr = reslin_list.kontignr
    zikatnr = reslin_list.zikatnr
    argt = reslin_list.arrangement
    erwachs = reslin_list.erwachs
    ankunft = reslin_list.ankunft
    abreise = reslin_list.abreise
    qty = reslin_list.zimmeranz

    if abreise == ankunft:
        abreise = ankunft + 1

    if reslin_list.active_flag == 1:
        ankunft = get_output(htpdate(87))

    if abreise == ankunft:

        return generate_output()

    if kontignr > 0:
        create_slist()
    else:
        create_slist1()

    return generate_output()