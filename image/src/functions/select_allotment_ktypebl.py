from functions.additional_functions import *
import decimal
from models import Kontline, Zimkateg, Queasy

def select_allotment_ktypebl(kontignr:int, gastnr:int, zikatno:int):
    ktype = 0
    rmtype = ""
    kline_list = []
    tokcounter:int = 0
    mesvalue:str = ""
    kontline = zimkateg = queasy = None

    kline = None

    kline_list, Kline = create_model_like(Kontline)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ktype, rmtype, kline_list, tokcounter, mesvalue, kontline, zimkateg, queasy


        nonlocal kline
        nonlocal kline_list
        return {"ktype": ktype, "rmtype": rmtype, "kline": kline_list}

    zimkateg = db_session.query(Zimkateg).filter(
            (Zimkateg.zikatnr == zikatno)).first()
    rmtype = zimkateg.kurzbez

    kontline = db_session.query(Kontline).filter(
            (Kontline.gastnr == gastnr) &  (Kontline.betriebsnr == 0) &  (Kontline.kontstat == 1)).first()

    if kontline:
        ktype = 0

    kontline = db_session.query(Kontline).filter(
            (Kontline.gastnr == gastnr) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).first()

    if kontline:
        ktype = ktype + 2

    if ktype == -1:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 147)).all():
            for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
                mesvalue = entry(tokcounter - 1, queasy.char3, ",")

                if to_int(mesvalue) == gastnr:
                    ktype = 0
                    gastnr = queasy.number1


                    break

    kontline = db_session.query(Kontline).filter(
            (Kontline.kontignr == kontignr) &  (Kontline.kontstat == 1)).first()

    if kontline:
        kline = Kline()
        kline_list.append(kline)

        buffer_copy(kontline, kline)

    return generate_output()