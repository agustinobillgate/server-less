#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Kontline, Zimkateg

def delete_kontlinebl(case_type:int, kontignr:int, kontcode:string, gastno:int):

    prepare_cache ([Queasy, Zimkateg])

    success_flag = False
    curr_date:date = None
    zikatnr:int = 0
    queasy = kontline = zimkateg = None

    qsy = kline = None

    Qsy = create_buffer("Qsy",Queasy)
    Kline = create_buffer("Kline",Kontline)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, curr_date, zikatnr, queasy, kontline, zimkateg
        nonlocal case_type, kontignr, kontcode, gastno
        nonlocal qsy, kline


        nonlocal qsy, kline

        return {"success_flag": success_flag}


    if case_type == 1:

        kontline = get_cache (Kontline, {"kontignr": [(eq, kontignr)],"gastnr": [(eq, gastno)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, kontline.zikatnr)]})

        if zimkateg:

            queasy = get_cache (Queasy, {"key": [(eq, 152)]})

            if queasy and zimkateg.typ != 0:
                zikatnr = zimkateg.typ
            else:
                zikatnr = zimkateg.zikatnr
        for curr_date in date_range(kontline.ankunft,kontline.abreise) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"number1": [(eq, zikatnr)]})

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass

        kontline = get_cache (Kontline, {"kontignr": [(eq, kontignr)],"gastnr": [(eq, gastno)]})

        if kontline:
            db_session.delete(kontline)
            pass
            success_flag = True


    elif case_type == 2:

        kontline = get_cache (Kontline, {"kontcode": [(eq, kontcode)],"kontstatus": [(eq, gastno)]})
        while None != kontline:

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, kontline.zikatnr)]})

            if zimkateg:

                queasy = get_cache (Queasy, {"key": [(eq, 152)]})

                if queasy and zimkateg.typ != 0:
                    zikatnr = zimkateg.typ
                else:
                    zikatnr = zimkateg.zikatnr
            for curr_date in date_range(kontline.ankunft,kontline.abreise) :

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"number1": [(eq, zikatnr)],"char1": [(eq, "")]})

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                    if qsy:
                        qsy.logi2 = True
                        pass
                        pass

            kline = db_session.query(Kline).filter(
                     (Kline._recid == kontline._recid)).first()
            db_session.delete(kline)

            curr_recid = kontline._recid
            kontline = db_session.query(Kontline).filter(
                     (Kontline.kontcode == (kontcode).lower()) & (Kontline._recid > curr_recid)).first()

    return generate_output()