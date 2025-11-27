#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Segmentstat

def segm_budgetbl(fdate:date, tdate:date, datum:date, segmentcode:int, room:int, person:int, logis:Decimal, delta_rm:int, delta_pax:int):

    prepare_cache ([Segmentstat])

    segmentstat = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal segmentstat
        nonlocal fdate, tdate, datum, segmentcode, room, person, logis, delta_rm, delta_pax

        return {}


    if fdate == None:

        return generate_output()

    if tdate == None:

        return generate_output()
    for datum in date_range(fdate,tdate) :

        # segmentstat = get_cache (Segmentstat, {"datum": [(eq, datum)],"segmentcode": [(eq, segmentcode)]})
        segmentstat = db_session.query(Segmentstat).filter(
                 (Segmentstat.datum == datum) &
                 (Segmentstat.segmentcode == segmentcode)).with_for_update().first()

        if not segmentstat:
            segmentstat = Segmentstat()
            db_session.add(segmentstat)

            segmentstat.datum = datum
            segmentstat.segmentcode = segmentcode


        pass
        segmentstat.budzimmeranz = room
        segmentstat.budpersanz = person
        segmentstat.budlogis =  to_decimal(logis)

        if delta_rm > 0:
            segmentstat.budzimmeranz = segmentstat.budzimmeranz + 1
            delta_rm = delta_rm - 1

        if delta_pax > 0:
            segmentstat.budpersanz = segmentstat.budpersanz + 1
            delta_pax = delta_pax - 1


        pass
        pass

    return generate_output()