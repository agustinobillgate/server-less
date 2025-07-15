#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.next_counterbl import next_counterbl
from functions.write_kontlinebl import write_kontlinebl
from models import Kontline, Counters, Bediener

def allotment_create_allbl(curr_mode:string, user_init:string, gastnr:int, zikatnr1:int, argt:string, comments:string, kontcode:string, ankunft:date, abreise:date, zikatnr:int, zimmeranz:int, erwachs:int, kind1:int, overbooking:int, ruecktage:int, rueckdatum:date, kontignr:int, ansprech:string):

    prepare_cache ([Bediener])

    success_flag = False
    kontline = counters = bediener = None

    t_kontline2 = t_counters = None

    t_kontline2_data, T_kontline2 = create_model_like(Kontline)
    t_counters_data, T_counters = create_model_like(Counters)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, kontline, counters, bediener
        nonlocal curr_mode, user_init, gastnr, zikatnr1, argt, comments, kontcode, ankunft, abreise, zikatnr, zimmeranz, erwachs, kind1, overbooking, ruecktage, rueckdatum, kontignr, ansprech


        nonlocal t_kontline2, t_counters
        nonlocal t_kontline2_data, t_counters_data

        return {"success_flag": success_flag}

    t_kontline2_data.clear()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if curr_mode.lower()  == ("new").lower() :
        t_counters_data = get_output(next_counterbl(10))

        t_counters = query(t_counters_data, first=True)
        t_kontline2 = T_kontline2()
        t_kontline2_data.append(t_kontline2)

        t_kontline2.kontcode = kontcode
        t_kontline2.ankunft = ankunft
        t_kontline2.abreise = abreise
        t_kontline2.zikatnr = zikatnr
        t_kontline2.arrangement = argt
        t_kontline2.zimmeranz = zimmeranz
        t_kontline2.erwachs = erwachs
        t_kontline2.kind1 = kind1
        t_kontline2.overbooking = overbooking
        t_kontline2.ruecktage = ruecktage
        t_kontline2.rueckdatum = rueckdatum
        t_kontline2.kontignr = t_counters.counter
        t_kontline2.bemerk = comments
        t_kontline2.gastnr = gastnr
        t_kontline2.useridanlage = ""
        t_kontline2.ansprech = ansprech

    if curr_mode.lower()  == ("chg").lower() :
        t_kontline2 = T_kontline2()
        t_kontline2_data.append(t_kontline2)

        t_kontline2.kontcode = kontcode
        t_kontline2.ankunft = ankunft
        t_kontline2.abreise = abreise
        t_kontline2.zikatnr = zikatnr
        t_kontline2.arrangement = argt
        t_kontline2.zimmeranz = zimmeranz
        t_kontline2.erwachs = erwachs
        t_kontline2.kind1 = kind1
        t_kontline2.overbooking = overbooking
        t_kontline2.ruecktage = ruecktage
        t_kontline2.rueckdatum = rueckdatum
        t_kontline2.kontignr = kontignr
        t_kontline2.arrangement = argt
        t_kontline2.bemerk = comments
        t_kontline2.gastnr = gastnr
        t_kontline2.bediener_nr = bediener.nr
        t_kontline2.ansprech = ansprech


    t_kontline2.zikatnr = zikatnr1

    if curr_mode.lower()  == ("new").lower() :
        t_kontline2.bediener_nr = bediener.nr

    if curr_mode.lower()  == ("chg").lower() :
        t_kontline2.useridanlage = bediener.userinit

    if curr_mode.lower()  == ("new").lower() :
        success_flag = get_output(write_kontlinebl(2, t_kontline2_data))

    elif curr_mode.lower()  == ("chg").lower() :
        success_flag = get_output(write_kontlinebl(1, t_kontline2_data))

    return generate_output()