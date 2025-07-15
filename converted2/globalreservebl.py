#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimkateg, Kontline, Bediener, Counters, Res_line

k_list_data, K_list = create_model_like(Kontline)

def globalreservebl(case_type:int, k_list_data:[K_list], rmcat:string, gastnr:int, curr_mode:string, last_code:string, argt:string, comments:string, user_init:string):

    prepare_cache ([Zimkateg, Kontline, Bediener, Counters, Res_line])

    msg_int = 0
    globalreserve_list_data = []
    allot_list_data = []
    katnr:int = 0
    ok:bool = False
    error:bool = False
    zimkateg = kontline = bediener = counters = res_line = None

    allot_list = z_list = k_list = globalreserve_list = kline = None

    allot_list_data, Allot_list = create_model("Allot_list", {"datum":date, "anz":int})
    z_list_data, Z_list = create_model_like(Zimkateg)
    globalreserve_list_data, Globalreserve_list = create_model("Globalreserve_list", {"kontcode":string, "ankunft":date, "abreise":date, "kurzbez":string, "arrangement":string, "zimmeranz":int, "erwachs":int, "kind1":int, "kind2":int, "userinit":string, "useridanlage":string, "resdat":date, "ansprech":string, "bemerk":string, "kontignr":int, "zikatnr":int, "overbooking":int, "ruecktage":int, "rueckdatum":date})

    Kline = create_buffer("Kline",Kontline)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_int, globalreserve_list_data, allot_list_data, katnr, ok, error, zimkateg, kontline, bediener, counters, res_line
        nonlocal case_type, rmcat, gastnr, curr_mode, last_code, argt, comments, user_init
        nonlocal kline


        nonlocal allot_list, z_list, k_list, globalreserve_list, kline
        nonlocal allot_list_data, z_list_data, globalreserve_list_data

        return {"msg_int": msg_int, "globalreserve-list": globalreserve_list_data, "allot-list": allot_list_data}

    def create_allotment():

        nonlocal msg_int, globalreserve_list_data, allot_list_data, katnr, ok, error, zimkateg, kontline, bediener, counters, res_line
        nonlocal case_type, rmcat, gastnr, curr_mode, last_code, argt, comments, user_init
        nonlocal kline


        nonlocal allot_list, z_list, k_list, globalreserve_list, kline
        nonlocal allot_list_data, z_list_data, globalreserve_list_data

        n:int = 1
        datum:date = None
        last_code = k_list.kontcode
        for datum in date_range(k_list.ankunft,k_list.abreise) :

            counters = get_cache (Counters, {"counter_no": [(eq, 10)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 10
                counters.counter_bez = "Allotment counter"
            counters.counter = counters.counter + 1
            kontline = Kontline()
            db_session.add(kontline)

            kontline.kontignr = counters.counter
            pass
            kontline.gastnr = gastnr
            kontline.useridanlage = ""
            kontline.betriebsnr = 1
            kontline.kontcode = k_list.kontcode
            kontline.ankunft = datum
            kontline.abreise = datum
            kontline.zikatnr = zimkateg.zikatnr
            kontline.arrangement = argt
            kontline.zimmeranz = k_list.zimmeranz
            kontline.erwachs = k_list.erwachs
            kontline.kind1 = k_list.kind1
            kontline.kind2 = k_list.kind2
            kontline.overbooking = k_list.overbooking
            kontline.ruecktage = k_list.ruecktage
            kontline.rueckdatum = k_list.rueckdatum
            kontline.ansprech = k_list.ansprech
            kontline.resdat = get_current_date()
            kontline.bemerk = comments
            kontline.bediener_nr = bediener.nr


            pass


    def chg_allotment():

        nonlocal msg_int, globalreserve_list_data, allot_list_data, katnr, ok, error, zimkateg, kontline, bediener, counters, res_line
        nonlocal case_type, rmcat, gastnr, curr_mode, last_code, argt, comments, user_init
        nonlocal kline


        nonlocal allot_list, z_list, k_list, globalreserve_list, kline
        nonlocal allot_list_data, z_list_data, globalreserve_list_data

        n:int = 1
        last_code = k_list.kontcode

        kontline = get_cache (Kontline, {"kontignr": [(eq, k_list.kontignr)],"gastnr": [(eq, gastnr)]})

        if kontline:
            kontline.betriebsnr = 1
            kontline.kontcode = k_list.kontcode
            kontline.ankunft = k_list.ankunft
            kontline.abreise = k_list.abreise
            kontline.zikatnr = zimkateg.zikatnr
            kontline.arrangement = argt
            kontline.zimmeranz = k_list.zimmeranz
            kontline.erwachs = k_list.erwachs
            kontline.kind1 = k_list.kind1
            kontline.kind2 = k_list.kind2
            kontline.overbooking = k_list.overbooking
            kontline.ruecktage = k_list.ruecktage
            kontline.rueckdatum = k_list.rueckdatum
            kontline.ansprech = k_list.ansprech
            kontline.resdat = get_current_date()
            kontline.bemerk = comments
            kontline.useridanlage = bediener.userinit


        pass


    def check_allotment():

        nonlocal msg_int, globalreserve_list_data, allot_list_data, katnr, ok, error, zimkateg, kontline, bediener, counters, res_line
        nonlocal case_type, rmcat, gastnr, curr_mode, last_code, argt, comments, user_init
        nonlocal kline


        nonlocal allot_list, z_list, k_list, globalreserve_list, kline
        nonlocal allot_list_data, z_list_data, globalreserve_list_data

        error = False
        datum:date = None
        d1:date = None
        d2:date = None
        kline = None

        def generate_inner_output():
            return (error)

        Kline =  create_buffer("Kline",Kontline)
        allot_list_data.clear()

        res_line_obj_list = {}
        res_line = Res_line()
        kline = Kontline()
        for res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line._recid, kline.zikatnr, kline.kontcode, kline.ankunft, kline.abreise, kline.arrangement, kline.zimmeranz, kline.erwachs, kline.kind1, kline.kind2, kline.useridanlage, kline.resdat, kline.ansprech, kline.bemerk, kline.kontignr, kline.overbooking, kline.ruecktage, kline.rueckdatum, kline.gastnr, kline.betriebsnr, kline.bediener_nr, kline._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line._recid, Kline.zikatnr, Kline.kontcode, Kline.ankunft, Kline.abreise, Kline.arrangement, Kline.zimmeranz, Kline.erwachs, Kline.kind1, Kline.kind2, Kline.useridanlage, Kline.resdat, Kline.ansprech, Kline.bemerk, Kline.kontignr, Kline.overbooking, Kline.ruecktage, Kline.rueckdatum, Kline.gastnr, Kline.betriebsnr, Kline.bediener_nr, Kline._recid).join(Kline,(Kline.kontignr == - Res_line.kontignr) & (Kline.kontcode == k_list.kontcode) & (Kline.kontstatus == 1)).filter(
                 (Res_line.kontignr < 0) & (Res_line.gastnr == gastnr) & (Res_line.active_flag < 2) & (Res_line.resstatus < 11) & (not_ (Res_line.ankunft > k_list.abreise)) & (not_ (Res_line.abreise < k_list.ankunft))).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if res_line.ankunft >= k_list.ankunft:
                d1 = res_line.ankunft
            else:
                d1 = k_list.ankunft

            if res_line.abreise <= k_list.abreise:
                d2 = res_line.abreise - timedelta(days=1)
            else:
                d2 = k_list.abreise
            for datum in date_range(d1,d2) :

                allot_list = query(allot_list_data, filters=(lambda allot_list: allot_list.datum == datum), first=True)

                if not allot_list:
                    allot_list = Allot_list()
                    allot_list_data.append(allot_list)

                    allot_list.datum = datum
                    allot_list.anz = k_list.zimmeranz
                allot_list.anz = allot_list.anz - res_line.zimmeranz

        allot_list = query(allot_list_data, filters=(lambda allot_list:(allot_list.anz + k_list.overbooking) < 0), first=True)

        if allot_list:
            error = True
            msg_int = 7

        return generate_inner_output()


    def open_query():

        nonlocal msg_int, globalreserve_list_data, allot_list_data, katnr, ok, error, zimkateg, kontline, bediener, counters, res_line
        nonlocal case_type, rmcat, gastnr, curr_mode, last_code, argt, comments, user_init
        nonlocal kline


        nonlocal allot_list, z_list, k_list, globalreserve_list, kline
        nonlocal allot_list_data, z_list_data, globalreserve_list_data

        kontline_obj_list = {}
        for kontline, bediener in db_session.query(Kontline, Bediener).join(Bediener,(Bediener.nr == Kontline.bediener_nr)).filter(
                 (Kontline.gastnr == gastnr) & (Kontline.kontignr > 0) & (Kontline.betriebsnr == 1) & (Kontline.kontstatus == 1)).order_by(Kontline.kontcode, Kontline.zikatnr, Kontline.ankunft).all():
            z_list = query(z_list_data, (lambda z_list: z_list.zikatnr == kontline.zikatnr), first=True)
            if not z_list:
                continue

            if kontline_obj_list.get(kontline._recid):
                continue
            else:
                kontline_obj_list[kontline._recid] = True


            globalreserve_list = Globalreserve_list()
            globalreserve_list_data.append(globalreserve_list)

            globalreserve_list.kontcode = kontline.kontcode
            globalreserve_list.ankunft = kontline.ankunft
            globalreserve_list.abreise = kontline.abreise
            globalreserve_list.kurzbez = z_list.kurzbez
            globalreserve_list.arrangement = kontline.arrangement
            globalreserve_list.zimmeranz = kontline.zimmeranz
            globalreserve_list.erwachs = kontline.erwachs
            globalreserve_list.kind1 = kontline.kind1
            globalreserve_list.kind2 = kontline.kind2
            globalreserve_list.userinit = bediener.userinit
            globalreserve_list.useridanlage = kontline.useridanlage
            globalreserve_list.resdat = kontline.resdat
            globalreserve_list.ansprech = kontline.ansprech
            globalreserve_list.bemerk = kontline.bemerk
            globalreserve_list.kontignr = kontline.kontignr
            globalreserve_list.zikatnr = kontline.zikatnr
            globalreserve_list.overbooking = kontline.overbooking
            globalreserve_list.ruecktage = kontline.ruecktage
            globalreserve_list.rueckdatum = kontline.rueckdatum


    def create_zlist():

        nonlocal msg_int, globalreserve_list_data, allot_list_data, katnr, ok, error, zimkateg, kontline, bediener, counters, res_line
        nonlocal case_type, rmcat, gastnr, curr_mode, last_code, argt, comments, user_init
        nonlocal kline


        nonlocal allot_list, z_list, k_list, globalreserve_list, kline
        nonlocal allot_list_data, z_list_data, globalreserve_list_data


        z_list = Z_list()
        z_list_data.append(z_list)

        z_list.zikatnr = 0
        z_list.kurzbez = ""

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            z_list = Z_list()
            z_list_data.append(z_list)

            z_list.zikatnr = zimkateg.zikatnr
            z_list.kurzbez = zimkateg.kurzbez

    if case_type == 2:
        create_zlist()
        open_query()

        return generate_output()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    k_list = query(k_list_data, first=True)

    if k_list.kontcode == "" or k_list.ankunft == None or k_list.abreise == None or k_list.zimmeranz == 0:
        msg_int = 1

        return generate_output()

    if k_list.abreise < k_list.ankunft:
        msg_int = 2

        return generate_output()

    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmcat)]})

    if not zimkateg:
        msg_int = 3

        return generate_output()
    katnr = zimkateg.zikatnr

    kline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"betriebsnr": [(eq, 1)],"kontcode": [(eq, k_list.kontcode)],"kontignr": [(ne, k_list.kontignr)],"zikatnr": [(ne, katnr)],"kontstatus": [(eq, 1)]})

    if kline:
        msg_int = 4

        return generate_output()

    kline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, k_list.kontcode)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)],"kontignr": [(ne, k_list.kontignr)],"ankunft": [(gt, k_list.abreise)],"abreise": [(lt, k_list.ankunft)],"zikatnr": [(eq, katnr)]})

    if kline:
        msg_int = 5

        return generate_output()
    error = check_allotment()

    if error:
        msg_int = 6

        return generate_output()

    if curr_mode.lower()  == ("new").lower() :
        create_allotment()

    elif curr_mode.lower()  == ("chg").lower() :
        chg_allotment()

    return generate_output()