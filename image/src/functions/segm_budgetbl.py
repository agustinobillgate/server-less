from functions.additional_functions import *
import decimal
from datetime import date
from models import Segmentstat

def segm_budgetbl(fdate:date, tdate:date, datum:date, segmentcode:int, room:int, person:int, logis:decimal, delta_rm:int, delta_pax:int):
    segmentstat = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal segmentstat


        return {}

    for datum in range(fdate,tdate + 1) :

        segmentstat = db_session.query(Segmentstat).filter(
                (Segmentstat.datum == datum) &  (Segmentstat.segmentcode == segmentcode)).first()

        if not segmentstat:
            segmentstat = Segmentstat()
            db_session.add(segmentstat)

            segmentstat.datum = datum
            segmentstat.segmentcode = segmentcode


        segmentstat.budzimmeranz = room
        segmentstat.budpersanz = person
        segmentstat.budlogis = logis

        if delta_rm > 0:
            segmentstat.budzimmeranz = segmentstat.budzimmeranz + 1
            delta_rm = delta_rm - 1

        if delta_pax > 0:
            segmentstat.budpersanz = segmentstat.budpersanz + 1
            delta_pax = delta_pax - 1

    return generate_output()