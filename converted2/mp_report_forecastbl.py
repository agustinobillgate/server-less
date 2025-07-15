#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_raum

def mp_report_forecastbl(reporttype:int):

    prepare_cache ([Bk_raum])

    t_raum_data = []
    forecast:Decimal = to_decimal("0.0")
    daycount:int = 0
    bk_raum = None

    t_raum = None

    t_raum_data, T_raum = create_model("T_raum", {"nr":int, "raum":string, "bezeich":string, "forecast":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_raum_data, forecast, daycount, bk_raum
        nonlocal reporttype


        nonlocal t_raum
        nonlocal t_raum_data

        return {"t-raum": t_raum_data}

    if reporttype == 3:

        for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
            t_raum = T_raum()
            t_raum_data.append(t_raum)

            t_raum.raum = bk_raum.raum
            t_raum.bezeich = bk_raum.bezeich

        for bk_event_detail in query(bk_event_detail_data):
            daycount = bk_event_detail.end_date - bk_event_detail.start_date + 1

            t_raum = query(t_raum_data, filters=(lambda t_raum: t_raum.bezeich == bk_event_detail.venue), first=True)

            if t_raum:
                forecast =  to_decimal(bk_event_detail.atendees) * to_decimal(bk_event_detail.amount)
                t_raum.forecast = ( to_decimal(t_raum.forecast) + to_decimal(forecast)) * to_decimal(daycount)

    elif reporttype == 4:

        for bk_queasy in query(bk_queasy_data, filters=(lambda bk_queasy: bk_queasy.key == 5)):
            t_raum = T_raum()
            t_raum_data.append(t_raum)

            t_raum.nr = bk_queasy.number1
            t_raum.raum = bk_queasy.char1
            t_raum.bezeich = bk_queasy.char2
            t_raum.forecast =  to_decimal("0")

        for t_raum in query(t_raum_data):

            bk_master = db_session.query(Bk_master).filter(
                     (Bk_master.restype == t_raum.nr)).first()
            while None != bk_master:

                bk_event_detail = db_session.query(Bk_event_detail).filter(
                         (Bk_event_detail.block_id == bk_master.block_id)).first()
                while None != bk_event_detail:
                    forecast =  to_decimal(bk_event_detail.atendees) * to_decimal(bk_event_detail.amount)
                    t_raum.forecast =  to_decimal(t_raum.forecast) + to_decimal(forecast)

                    curr_recid = bk_event_detail._recid
                    bk_event_detail = db_session.query(Bk_event_detail).filter(
                             (Bk_event_detail.block_id == bk_master.block_id) & (Bk_event_detail._recid > curr_recid)).first()

                curr_recid = bk_master._recid
                bk_master = db_session.query(Bk_master).filter(
                         (Bk_master.restype == t_raum.nr) & (Bk_master._recid > curr_recid)).first()

    return generate_output()