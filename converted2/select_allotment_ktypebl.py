#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Kontline, Zimkateg, Queasy

def select_allotment_ktypebl(kontignr:int, gastnr:int, zikatno:int):

    prepare_cache ([Zimkateg, Queasy])

    ktype = -1
    rmtype = ""
    kline_data = []
    tokcounter:int = 0
    mesvalue:string = ""
    kontline = zimkateg = queasy = None

    kline = None

    kline_data, Kline = create_model_like(Kontline)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ktype, rmtype, kline_data, tokcounter, mesvalue, kontline, zimkateg, queasy
        nonlocal kontignr, gastnr, zikatno


        nonlocal kline
        nonlocal kline_data

        return {"gastnr": gastnr, "ktype": ktype, "rmtype": rmtype, "kline": kline_data}

    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zikatno)]})
    rmtype = zimkateg.kurzbez

    kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})

    if kontline:
        ktype = 0

    kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

    if kontline:
        ktype = ktype + 2

    if ktype == -1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 147)).order_by(Queasy._recid).yield_per(100):
            for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
                mesvalue = entry(tokcounter - 1, queasy.char3, ",")

                if to_int(mesvalue) == gastnr:
                    ktype = 0
                    gastnr = queasy.number1


                    break

    kontline = get_cache (Kontline, {"kontignr": [(eq, kontignr)],"kontstatus": [(eq, 1)]})

    if kontline:
        kline = Kline()
        kline_data.append(kline)

        buffer_copy(kontline, kline)

    return generate_output()