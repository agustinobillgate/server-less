#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 28-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import Genstat, Bediener, Segment, Res_line, Res_history

genlist_data, Genlist = create_model_like(Genstat, {"rsv_name":string, "nat_str":string, "ctry_str":string, "source_str":string, "segment_str":string, "rec_gen":int})

def correct_statistic_btn_updatebl(genlist_data:[Genlist], rec_gen:int, user_init:string):

    prepare_cache ([Genstat, Bediener, Segment, Res_line, Res_history])

    genstat = bediener = segment = res_line = res_history = None

    genlist = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal genstat, bediener, segment, res_line, res_history
        nonlocal rec_gen, user_init


        nonlocal genlist

        return {}

    def res_history():

        nonlocal genstat, bediener, segment, res_line, res_history
        nonlocal rec_gen, user_init


        nonlocal genlist

        temp_segment:string = ""

        segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

        res_line = get_cache (Res_line, {"resnr": [(eq, genlist.resnr)]})
        temp_segment = segment.bezeich
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.resnr = genlist.resnr
        res_history.reslinnr = res_line.reslinnr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Segment"
        res_history.aenderung = "Reservation " + to_string(genlist.resnr) + ", Segment has been changed from " +\
                temp_segment + " to " + genlist.segment_str


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    genlist = query(genlist_data, first=True)
    while None != genlist:

        genstat = get_cache (Genstat, {"_recid": [(eq, genlist.rec_gen)]})
        res_history()
        buffer_copy(genlist, genstat,except_fields=["genlist.datum","genlist.zinr"])

        if (genstat.zipreis == 0) and ((genstat.erwachs + genstat.kind1) > 0):
            genstat.res_logic[2] = True
        else:
            genstat.res_logic[2] = False
        pass

        genlist = query(genlist_data, next=True)
    pass

    return generate_output()