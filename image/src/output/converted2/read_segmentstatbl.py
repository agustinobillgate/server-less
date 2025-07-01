#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Segmentstat

def read_segmentstatbl(case_type:int, int1:int, int2:int, int3:int, int4:int, int5:int, date1:date, date2:date, deci1:Decimal):
    t_segmentstat_list = []
    segmentstat = None

    t_segmentstat = None

    t_segmentstat_list, T_segmentstat = create_model_like(Segmentstat)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_segmentstat_list, segmentstat
        nonlocal case_type, int1, int2, int3, int4, int5, date1, date2, deci1


        nonlocal t_segmentstat
        nonlocal t_segmentstat_list

        return {"t-segmentstat": t_segmentstat_list}

    def assign_it():

        nonlocal t_segmentstat_list, segmentstat
        nonlocal case_type, int1, int2, int3, int4, int5, date1, date2, deci1


        nonlocal t_segmentstat
        nonlocal t_segmentstat_list


        t_segmentstat = T_segmentstat()
        t_segmentstat_list.append(t_segmentstat)

        buffer_copy(segmentstat, t_segmentstat)


    if case_type == 1:

        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.segmentcode == int1) & (Segmentstat.datum >= date1)).order_by(Segmentstat.datum).all():
            assign_it()

    return generate_output()