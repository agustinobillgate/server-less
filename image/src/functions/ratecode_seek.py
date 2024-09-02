from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from models import Res_line, Arrangement, Ratecode

def ratecode_seek(resnr:int, reslinnr:int, prcode:str, datum:date):
    s_recid = 0
    ct:str = ""
    argtno:int = 0
    rmcatno:int = 0
    w_day:int = 0
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    res_line = arrangement = ratecode = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_recid, ct, argtno, rmcatno, w_day, wd_array, res_line, arrangement, ratecode


        return {"s_recid": s_recid}


    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement == res_line.arrangement)).first()

    if arrangement:
        argtno = arrangement.argtnr
    rmcatno = res_line.zikatnr
    w_day = wd_array[get_weekday(datum - 1) - 1]
    ct = res_line.zimmer_wunsch

    if re.match(".*\$CODE\$.*",ct):
        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
        prcode = substring(ct, 0,1 + get_index(ct, ";") - 1)

    ratecode = db_session.query(Ratecode).filter(
            (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == w_day) &  (Ratecode.erwachs == res_line.erwachs) &  (Ratecode.kind1 == res_line.kind1) &  (Ratecode.kind2 == res_line.kind2)).first()

    ratecode = db_session.query(Ratecode).filter(
            (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == w_day) &  (Ratecode.erwachs == res_line.erwachs) &  (Ratecode.kind1 == res_line.kind1) &  (Ratecode.kind2 == res_line.kind2)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == 0) &  (Ratecode.erwachs == res_line.erwachs) &  (Ratecode.kind1 == res_line.kind1) &  (Ratecode.kind2 == res_line.kind2)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == 0) &  (Ratecode.erwachs == res_line.erwachs) &  (Ratecode.kind1 == res_line.kind1) &  (Ratecode.kind2 == res_line.kind2)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == w_day) &  (Ratecode.erwachs == res_line.erwachs)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == w_day) &  (Ratecode.erwachs == res_line.erwachs)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == 0) &  (Ratecode.erwachs == res_line.erwachs)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == 0) &  (Ratecode.erwachs == res_line.erwachs)).first()

    if ratecode:
        s_recid = ratecode._recid

    return generate_output()