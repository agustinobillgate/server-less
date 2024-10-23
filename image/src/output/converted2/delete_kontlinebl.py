from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Kontline, Zimkateg

def delete_kontlinebl(case_type:int, kontignr:int, kontcode:str, gastno:int):
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

        kontline = db_session.query(Kontline).filter(
                 (Kontline.kontignr == kontignr) & (Kontline.gastnr == gastno)).first()

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == kontline.zikatnr)).first()

        if zimkateg:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 152)).first()

            if queasy and zimkateg.typ != 0:
                zikatnr = zimkateg.typ
            else:
                zikatnr = zimkateg.zikatnr
        for curr_date in date_range(kontline.ankunft,kontline.abreise) :

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.date1 == curr_date) & (Queasy.number1 == zikatnr)).first()

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = db_session.query(Qsy).filter(
                         (Qsy._recid == queasy._recid)).first()

                if qsy:
                    qsy.logi2 = True
                    pass

        kontline = db_session.query(Kontline).filter(
                 (Kontline.kontignr == kontignr) & (Kontline.gastnr == gastno)).first()

        if kontline:
            db_session.delete(kontline)
            pass
            success_flag = True


    elif case_type == 2:

        kontline = db_session.query(Kontline).filter(
                 (func.lower(Kontline.kontcode) == (kontcode).lower()) & (Kontline.kontstatus == gastno)).first()
        while None != kontline:

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == kontline.zikatnr)).first()

            if zimkateg:

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 152)).first()

                if queasy and zimkateg.typ != 0:
                    zikatnr = zimkateg.typ
                else:
                    zikatnr = zimkateg.zikatnr
            for curr_date in date_range(kontline.ankunft,kontline.abreise) :

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 171) & (Queasy.date1 == curr_date) & (Queasy.number1 == zikatnr) & (Queasy.char1 == "")).first()

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    qsy = db_session.query(Qsy).filter(
                             (Qsy._recid == queasy._recid)).first()

                    if qsy:
                        qsy.logi2 = True
                        pass

            kline = db_session.query(Kline).filter(
                     (Kline._recid == kontline._recid)).first()
            kline_list.remove(kline)

            curr_recid = kontline._recid
            kontline = db_session.query(Kontline).filter(
                     (func.lower(Kontline.kontcode) == (kontcode).lower())).filter(Kontline._recid > curr_recid).first()

    return generate_output()