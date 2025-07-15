#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

t_mapping_nation_data, T_mapping_nation = create_model("T_mapping_nation", {"nationvhp":string, "nationbe":string, "descr":string, "nr":int})

def bookengine_mapping_nation_btn_exit_webbl(t_mapping_nation_data:[T_mapping_nation], bookengid:int, user_init:string):

    prepare_cache ([Queasy, Bediener, Res_history])

    be_name:string = ""
    changedstr:string = ""
    queasy = bediener = res_history = None

    t_mapping_nation = nameqsy = buffqsy = None

    Nameqsy = create_buffer("Nameqsy",Queasy)
    Buffqsy = create_buffer("Buffqsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal be_name, changedstr, queasy, bediener, res_history
        nonlocal bookengid, user_init
        nonlocal nameqsy, buffqsy


        nonlocal t_mapping_nation, nameqsy, buffqsy

        return {}

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    nameqsy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, bookengid)]})

    if nameqsy:
        be_name = nameqsy.char1 + "|Country"

    buffqsy = get_cache (Queasy, {"key": [(eq, 165)]})

    t_mapping_nation = query(t_mapping_nation_data, first=True)

    if not buffqsy and t_mapping_nation:

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Booking Engine Interface"


            res_history.aenderung = chr_unicode(40) + be_name + chr_unicode(41) + " New Country Mapping Has Been Created"
            pass
    changedstr = ""

    for t_mapping_nation in query(t_mapping_nation_data):

        queasy = get_cache (Queasy, {"key": [(eq, 165)],"number1": [(eq, bookengid)],"number2": [(eq, t_mapping_nation.nr)]})

        if queasy:

            if queasy.char2 != t_mapping_nation.nationbe:
                changedstr = changedstr + queasy.char1 + "=" + queasy.char2 + ">>" + t_mapping_nation.nationbe + " "
            queasy.char2 = t_mapping_nation.nationbe
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 165
            queasy.number1 = bookengid
            queasy.number2 = t_mapping_nation.nr
            queasy.char1 = t_mapping_nation.nationvhp

    if changedstr != "":
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Booking Engine Interface"


        res_history.aenderung = chr_unicode(40) + be_name + chr_unicode(41) + " " + changedstr

    return generate_output()