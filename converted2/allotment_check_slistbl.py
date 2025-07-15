#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.next_counterbl import next_counterbl
from functions.write_kontlinebl import write_kontlinebl
from functions.read_kontlinebl import read_kontlinebl
from models import Kontline, Counters, Bediener

s_list_data, S_list = create_model("S_list", {"datum":date, "tag":string, "qty":int, "occ":int, "vac":int, "ovb":int})

def allotment_check_slistbl(s_list_data:[S_list], gastnr:int, kontcode:string, zikatnr:int, arrangement:string, erwachs:int, kind1:int, overbooking:int, ruecktage:int, rueckdatum:date, ansprech:string, bemerk:string, kontignr:int, userinit:string):

    prepare_cache ([Bediener])

    changed = False
    success_flag = False
    anz:int = 0
    d1:date = None
    i:int = 0
    kontline = counters = bediener = None

    t_kontline2 = t_counters = s_list = allotment_list = None

    t_kontline2_data, T_kontline2 = create_model_like(Kontline)
    t_counters_data, T_counters = create_model_like(Counters)
    allotment_list_data, Allotment_list = create_model_like(Kontline, {"kurzbez":string, "userinit":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal changed, success_flag, anz, d1, i, kontline, counters, bediener
        nonlocal gastnr, kontcode, zikatnr, arrangement, erwachs, kind1, overbooking, ruecktage, rueckdatum, ansprech, bemerk, kontignr, userinit


        nonlocal t_kontline2, t_counters, s_list, allotment_list
        nonlocal t_kontline2_data, t_counters_data, allotment_list_data

        return {"changed": changed, "success_flag": success_flag}


    for s_list in query(s_list_data):
        i = i + 1

        if anz == 0:
            anz = s_list.qty
            d1 = s_list.datum

        if s_list.qty != anz:
            changed = True
            t_counters_data = get_output(next_counterbl(10))

            t_counters = query(t_counters_data, first=True)
            t_kontline2_data.clear()

            bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})
            t_kontline2 = T_kontline2()
            t_kontline2_data.append(t_kontline2)

            t_kontline2.kontignr = t_counters.counter
            t_kontline2.gastnr = gastnr
            t_kontline2.useridanlage = ""
            t_kontline2.kontcode = kontcode
            t_kontline2.ankunft = d1
            t_kontline2.abreise = s_list.datum - timedelta(days=1)
            t_kontline2.zikatnr = zikatnr
            t_kontline2.arrangement = arrangement
            t_kontline2.zimmeranz = anz
            t_kontline2.erwachs = erwachs
            t_kontline2.kind1 = kind1
            t_kontline2.overbooking = overbooking
            t_kontline2.ruecktage = ruecktage
            t_kontline2.rueckdatum = rueckdatum
            t_kontline2.ansprech = ansprech
            t_kontline2.bediener_nr = bediener.nr
            t_kontline2.resdat = get_current_date()
            t_kontline2.bemerk = bemerk
            t_kontline2.ankunft = d1
            t_kontline2.zimmeranz = anz
            d1 = s_list.datum
            anz = s_list.qty


            success_flag = get_output(write_kontlinebl(2, t_kontline2_data))

    if changed:
        t_kontline2_data = get_output(read_kontlinebl(10, t_counters.counter, None, gastnr, "", None))

        t_kontline2 = query(t_kontline2_data, first=True)
        t_kontline2.ankunft = d1
        t_kontline2.zimmeranz = anz


        success_flag = get_output(write_kontlinebl(1, t_kontline2_data))

    elif i == 1:
        t_kontline2_data = get_output(read_kontlinebl(10, kontignr, None, gastnr, "", None))

        t_kontline2 = query(t_kontline2_data, first=True)
        t_kontline2.ankunft = d1
        t_kontline2.zimmeranz = anz


        success_flag = get_output(write_kontlinebl(1, t_kontline2_data))

    return generate_output()