#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kontline, Queasy

t_kontline_data, T_kontline = create_model_like(Kontline)

def write_kontlinebl(case_type:int, t_kontline_data:[T_kontline]):

    prepare_cache ([Queasy])

    success_flag = False
    curr_date:date = None
    kontline = queasy = None

    t_kontline = qsy = None

    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, curr_date, kontline, queasy
        nonlocal case_type
        nonlocal qsy


        nonlocal t_kontline, qsy

        return {"success_flag": success_flag}

    t_kontline = query(t_kontline_data, first=True)

    if not t_kontline:

        return generate_output()

    if case_type == 1:
        for curr_date in date_range(t_kontline.ankunft,t_kontline.abreise) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"number1": [(eq, t_kontline.zikatnr)],"char1": [(eq, "")]})

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass

        kontline = get_cache (Kontline, {"kontignr": [(eq, t_kontline.kontignr)]})

        if kontline:
            buffer_copy(t_kontline, kontline)
            pass
            success_flag = True
    elif case_type == 2:
        for curr_date in date_range(t_kontline.ankunft,t_kontline.abreise) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"number1": [(eq, t_kontline.zikatnr)],"char1": [(eq, "")]})

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass
        kontline = Kontline()
        db_session.add(kontline)

        buffer_copy(t_kontline, kontline)
        success_flag = True
        pass

    return generate_output()