#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Arrangement, Ratecode

def ratecode_seek(resnr:int, reslinnr:int, prcode:string, datum:date):

    prepare_cache ([Res_line, Arrangement, Ratecode])

    s_recid = 0
    ct:string = ""
    argtno:int = 0
    rmcatno:int = 0
    w_day:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    tmp_date:date = None
    res_line = arrangement = ratecode = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_recid, ct, argtno, rmcatno, w_day, wd_array, tmp_date, res_line, arrangement, ratecode
        nonlocal resnr, reslinnr, prcode, datum

        return {"s_recid": s_recid}


    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

    if arrangement:
        argtno = arrangement.argtnr
    rmcatno = res_line.zikatnr
    tmp_date = datum - timedelta(days=1)
    w_day = wd_array[get_weekday(tmp_date) - 1]
    ct = res_line.zimmer_wunsch

    if matches(ct,r"*$CODE$*"):
        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
        prcode = substring(ct, 0, get_index(ct, ";") - 1)

    ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, w_day)],"erwachs": [(eq, res_line.erwachs)],"kind1": [(eq, res_line.kind1)],"kind2": [(eq, res_line.kind2)]})

    ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, w_day)],"erwachs": [(eq, res_line.erwachs)],"kind1": [(eq, res_line.kind1)],"kind2": [(eq, res_line.kind2)]})

    if not ratecode:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, 0)],"erwachs": [(eq, res_line.erwachs)],"kind1": [(eq, res_line.kind1)],"kind2": [(eq, res_line.kind2)]})

    if not ratecode:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, 0)],"erwachs": [(eq, res_line.erwachs)],"kind1": [(eq, res_line.kind1)],"kind2": [(eq, res_line.kind2)]})

    if not ratecode:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, w_day)],"erwachs": [(eq, res_line.erwachs)]})

    if not ratecode:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, w_day)],"erwachs": [(eq, res_line.erwachs)]})

    if not ratecode:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, 0)],"erwachs": [(eq, res_line.erwachs)]})

    if not ratecode:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, 0)],"erwachs": [(eq, res_line.erwachs)]})

    if ratecode:
        s_recid = ratecode._recid

    return generate_output()