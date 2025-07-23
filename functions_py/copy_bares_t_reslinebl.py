#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd 23/7/2025
# 
#-------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Bk_raum
from datetime import datetime, date

def safe_parse_date(date_input):
    if isinstance(date_input, date):
        return date_input  # already parsed
    if date_input:
        try:
            return datetime.strptime(date_input, "%m/%d/%y").date()
        except ValueError:
            raise ValueError(f"Invalid date format: {date_input}")
    return None
    
def copy_bares_t_reslinebl(frdate:date, todate:date, rraum:string):

    prepare_cache ([Bk_raum])

    t_resline_data = []
    bk_reser = bk_raum = None

    t_resline = bkraum = resline = None

    t_resline_data, T_resline = create_model_like(Bk_reser, {"vorbereit":int})

    Bkraum = create_buffer("Bkraum",Bk_raum)
    Resline = create_buffer("Resline",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_resline_data, bk_reser, bk_raum
        nonlocal frdate, todate, rraum
        nonlocal bkraum, resline


        nonlocal t_resline, bkraum, resline
        nonlocal t_resline_data

        return {"t-resline": t_resline_data}
    
    print("Date:", frdate, todate)    
    # for resline in db_session.query(Resline).filter(
    #             (Resline.datum >= frdate) & (Resline.datum <= todate)
    #         ).order_by(Resline._recid).all():
    #     pass
        # bkraum = get_cache (Bk_raum, {"raum": [(eq, resline.raum)],"lu_raum": [(eq, rraum)]})

        # if bkraum:
        #     t_resline = T_resline()
        #     t_resline_data.append(t_resline)

        #     buffer_copy(resline, t_resline)
        #     t_resline.vorbereit = bkraum.vorbereit

    return generate_output()