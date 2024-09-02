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

    Qsy = Queasy
    Kline = Kontline

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, curr_date, zikatnr, queasy, kontline, zimkateg
        nonlocal qsy, kline


        nonlocal qsy, kline
        return {"success_flag": success_flag}


    if case_type == 1:

        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == kontignr) &  (Kontline.gastnr == gastno)).first()

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == kontline.zikatnr)).first()

        if zimkateg:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 152)).first()

            if queasy and zimkateg.typ != 0:
                zikatnr = zimkateg.typ
            else:
                zikatnr = zimkateg.zikatnr
        for curr_date in range(kontline.ankunft,kontline.abreise + 1) :

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (Queasy.date1 == curr_date) &  (Queasy.number1 == zikatnr)).first()

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()

                if qsy:
                    qsy.logi2 = True

                    qsy = db_session.query(Qsy).first()


        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == kontignr) &  (Kontline.gastnr == gastno)).first()

        if kontline:
            db_session.delete(kontline)

            success_flag = True


    elif case_type == 2:

        kontline = db_session.query(Kontline).filter(
                (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower()) &  (Kontline.kontstat == gastno)).first()
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
            for curr_date in range(kontline.ankunft,kontline.abreise + 1) :

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 171) &  (Queasy.date1 == curr_date) &  (Queasy.number1 == zikatnr) &  (Queasy.char1 == "")).first()

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    qsy = db_session.query(Qsy).filter(
                            (Qsy._recid == queasy._recid)).first()

                    if qsy:
                        qsy.logi2 = True

                        qsy = db_session.query(Qsy).first()


            kline = db_session.query(Kline).filter(
                    (Kline._recid == kontline._recid)).first()
            db_session.delete(kline)

            kontline = db_session.query(Kontline).filter(
                    (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower())).first()

    return generate_output()