#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line, Bediener, Kontline, Queasy, Counters

reslin_list_data, Reslin_list = create_model_like(Res_line)
s_list_data, S_list = create_model("S_list", {"datum":date, "tag":string, "qty":int, "occ":int, "vac":int, "ovb":int})

def modify_allotmentbl(i_case:int, user_init:string, reslin_list_data:[Reslin_list], s_list_data:[S_list]):

    prepare_cache ([Res_line, Bediener, Kontline, Queasy, Counters])

    overbook = 0
    allotcode = ""
    curr_resnr:int = 0
    curr_reslinnr:int = 0
    kontignr:int = 0
    zikatnr:int = 0
    argt:string = ""
    erwachs:int = 0
    ankunft:date = None
    abreise:date = None
    qty:int = 0
    qty1:int = 0
    res_line = bediener = kontline = queasy = counters = None

    reslin_list = s_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal overbook, allotcode, curr_resnr, curr_reslinnr, kontignr, zikatnr, argt, erwachs, ankunft, abreise, qty, qty1, res_line, bediener, kontline, queasy, counters
        nonlocal i_case, user_init


        nonlocal reslin_list, s_list

        return {"overbook": overbook, "allotcode": allotcode, "s-list": s_list_data}

    def create_slist():

        nonlocal overbook, allotcode, curr_resnr, curr_reslinnr, kontignr, zikatnr, argt, erwachs, ankunft, abreise, qty, qty1, res_line, bediener, kontline, queasy, counters
        nonlocal i_case, user_init


        nonlocal reslin_list, s_list

        weekdays:List[string] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        d:date = None
        arrival:date = None
        depart:date = None
        kline = None
        Kline =  create_buffer("Kline",Kontline)
        qty1 = qty

        if reslin_list.active_flag == 0:

            res_line = get_cache (Res_line, {"resnr": [(eq, curr_resnr)],"reslinnr": [(eq, curr_reslinnr)]})

            if res_line.kontignr != 0:

                kline = get_cache (Kontline, {"gastnr": [(eq, res_line.gastnr)],"kontignr": [(eq, res_line.kontignr)],"kontstatus": [(eq, 1)]})

                if kline and kline.kontcode == kontline.kontcode:
                    qty1 = qty - res_line.zimmeranz
        for d in date_range(ankunft,abreise - 1) :
            s_list = S_list()
            s_list_data.append(s_list)

            s_list.datum = d
            s_list.qty = kontline.zimmeranz
            s_list.vac = kontline.zimmeranz
            s_list.tag = weekdays[get_weekday(s_list.datum) - 1]
            s_list.vac = s_list.vac - qty1
            s_list.occ = s_list.occ + qty1

        queasy = get_cache (Queasy, {"key": [(eq, 147)],"number1": [(eq, kontline.gastnr)]})

        if not queasy:

            res_line_obj_list = {}
            res_line = Res_line()
            kline = Kontline()
            for res_line.gastnr, res_line.kontignr, res_line.zimmeranz, res_line.reslinnr, res_line.ankunft, res_line.abreise, res_line.resnr, res_line._recid, kline.kontcode, kline.zimmeranz, kline.gastnr, kline.ankunft, kline.abreise, kline.zikatnr, kline.arrangement, kline.bemerk, kline._recid, kline.overbooking, kline.kontignr, kline.useridanlage, kline.bediener_nr, kline.resdat, kline.pr_code in db_session.query(Res_line.gastnr, Res_line.kontignr, Res_line.zimmeranz, Res_line.reslinnr, Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line._recid, Kline.kontcode, Kline.zimmeranz, Kline.gastnr, Kline.ankunft, Kline.abreise, Kline.zikatnr, Kline.arrangement, Kline.bemerk, Kline._recid, Kline.overbooking, Kline.kontignr, Kline.useridanlage, Kline.bediener_nr, Kline.resdat, Kline.pr_code).join(Kline,(Kline.kontignr == Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1)).filter(
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
            for res_line.gastnr, res_line.kontignr, res_line.zimmeranz, res_line.reslinnr, res_line.ankunft, res_line.abreise, res_line.resnr, res_line._recid, kline.kontcode, kline.zimmeranz, kline.gastnr, kline.ankunft, kline.abreise, kline.zikatnr, kline.arrangement, kline.bemerk, kline._recid, kline.overbooking, kline.kontignr, kline.useridanlage, kline.bediener_nr, kline.resdat, kline.pr_code in db_session.query(Res_line.gastnr, Res_line.kontignr, Res_line.zimmeranz, Res_line.reslinnr, Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line._recid, Kline.kontcode, Kline.zimmeranz, Kline.gastnr, Kline.ankunft, Kline.abreise, Kline.zikatnr, Kline.arrangement, Kline.bemerk, Kline._recid, Kline.overbooking, Kline.kontignr, Kline.useridanlage, Kline.bediener_nr, Kline.resdat, Kline.pr_code).join(Kline,(Kline.kontignr == Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1)).filter(
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

        nonlocal overbook, allotcode, curr_resnr, curr_reslinnr, kontignr, zikatnr, argt, erwachs, ankunft, abreise, qty, res_line, bediener, kontline, queasy, counters
        nonlocal i_case, user_init


        nonlocal reslin_list, s_list

        weekdays:List[string] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        d:date = None
        arrival:date = None
        depart:date = None
        qty1:int = 0
        kline = None
        Kline =  create_buffer("Kline",Kontline)
        qty1 = qty

        if reslin_list.active_flag == 0:

            res_line = get_cache (Res_line, {"resnr": [(eq, curr_resnr)],"reslinnr": [(eq, curr_reslinnr)]})
            qty1 = qty - res_line.zimmeranz
        for d in date_range(ankunft,abreise - 1) :

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
        for res_line.gastnr, res_line.kontignr, res_line.zimmeranz, res_line.reslinnr, res_line.ankunft, res_line.abreise, res_line.resnr, res_line._recid, kline.kontcode, kline.zimmeranz, kline.gastnr, kline.ankunft, kline.abreise, kline.zikatnr, kline.arrangement, kline.bemerk, kline._recid, kline.overbooking, kline.kontignr, kline.useridanlage, kline.bediener_nr, kline.resdat, kline.pr_code in db_session.query(Res_line.gastnr, Res_line.kontignr, Res_line.zimmeranz, Res_line.reslinnr, Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line._recid, Kline.kontcode, Kline.zimmeranz, Kline.gastnr, Kline.ankunft, Kline.abreise, Kline.zikatnr, Kline.arrangement, Kline.bemerk, Kline._recid, Kline.overbooking, Kline.kontignr, Kline.useridanlage, Kline.bediener_nr, Kline.resdat, Kline.pr_code).join(Kline,(Kline.kontignr == - Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1)).filter(
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

        nonlocal overbook, allotcode, curr_resnr, curr_reslinnr, kontignr, zikatnr, argt, erwachs, ankunft, abreise, qty, qty1, res_line, bediener, kontline, queasy, counters
        nonlocal i_case, user_init


        nonlocal reslin_list, s_list

        anz:int = 0
        d1:date = None
        i:int = 0
        changed:bool = False
        create_it:bool = False
        kline = None
        kline1 = None
        kline2 = None
        Kline =  create_buffer("Kline",Kontline)
        Kline1 =  create_buffer("Kline1",Kontline)
        Kline2 =  create_buffer("Kline2",Kontline)

        for s_list in query(s_list_data, sort_by=[("datum",False)]):
            create_it = True

            kline1 = get_cache (Kontline, {"gastnr": [(eq, kontline.gastnr)],"kontcode": [(eq, kontline.kontcode)],"zikatnr": [(eq, kontline.zikatnr)],"arrangement": [(eq, kontline.arrangement)],"ankunft": [(le, s_list.datum)],"abreise": [(ge, s_list.datum)]})

            if s_list.qty != kline1.zimmeranz:
                changed = True

                if kline1.ankunft == s_list.datum and kline1.abreise == s_list.datum:
                    create_it = False
                    kline1.zimmeranz = s_list.qty

                elif kline1.ankunft == s_list.datum and kline1.abreise > s_list.datum:
                    kline1.abreise = s_list.datum + timedelta(days=1)

                elif kline1.abreise == s_list.datum:
                    kline1.abreise = s_list.datum - timedelta(days=1)


                else:

                    counters = get_cache (Counters, {"counter_no": [(eq, 10)]})
                    counters.counter = counters.counter + 1
                    pass
                    kline2 = Kontline()
                    db_session.add(kline2)

                    buffer_copy(kline1, kline2,except_fields=["kontignr","ankunft"])
                    kline2.kontignr = counters.counter
                    kline2.ankunft = s_list.datum + timedelta(days=1)
                    kline2.bediener_nr = bediener.nr
                    kline2.resdat = get_current_date()
                    kline2.bemerk = kontline.bemerk


                    kline1.abreise = s_list.datum - timedelta(days=1)

                if create_it:

                    counters = get_cache (Counters, {"counter_no": [(eq, 10)]})
                    counters.counter = counters.counter + 1
                    pass
                    kline = Kontline()
                    db_session.add(kline)

                    buffer_copy(kline1, kline,except_fields=["kontignr","ankunft","abreise"])
                    kline.kontignr = counters.counter
                    kline.useridanlage = ""
                    kline.ankunft = s_list.datum
                    kline.abreise = s_list.datum
                    kline.zimmeranz = s_list.qty
                    kline.bediener_nr = bediener.nr
                    kline.resdat = get_current_date()
                    kline.bemerk = kontline.bemerk

        if changed:

            queasy = get_cache (Queasy, {"key": [(eq, 147)],"number1": [(eq, kontline.gastnr)]})

            if queasy:

                for kline in db_session.query(Kline).filter(
                         (Kline.gastnr == kontline.gastnr) & (Kline.kontstatus == 1) & (Kline.kontcode == kontline.kontcode) & (Kline._recid != kontline._recid)).order_by(Kline._recid).all():
                    kline.pr_code = queasy.char3

    def check_slist1():

        nonlocal overbook, allotcode, curr_resnr, curr_reslinnr, kontignr, zikatnr, argt, erwachs, ankunft, abreise, qty, qty1, res_line, bediener, kontline, queasy, counters
        nonlocal i_case, user_init


        nonlocal reslin_list, s_list

        kline = None
        Kline =  create_buffer("Kline",Kontline)

        for s_list in query(s_list_data):

            kline = get_cache (Kontline, {"kontcode": [(eq, kontline.kontcode)],"ankunft": [(eq, s_list.datum)]})

            if kline and kline.zimmeranz < s_list.qty:
                pass
                kline.zimmeranz = s_list.qty


                pass

    reslin_list = query(reslin_list_data, first=True)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if reslin_list.kontignr > 0:

        kontline = get_cache (Kontline, {"kontignr": [(eq, reslin_list.kontignr)],"kontstatus": [(eq, 1)]})

    elif reslin_list.kontignr < 0:

        kontline = get_cache (Kontline, {"kontignr": [(eq, - reslin_list.kontignr)],"kontstatus": [(eq, 1)]})

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
        abreise = ankunft + timedelta(days=1)

    if reslin_list.active_flag == 1:
        ankunft = get_output(htpdate(87))

    if abreise == ankunft:

        return generate_output()

    if kontignr > 0:
        create_slist()
    else:
        create_slist1()

    return generate_output()