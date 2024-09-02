from functions.additional_functions import *
import decimal
from models import Queasy

def egsource_btn_exitbl(source:[Source], case_type:int, rec_id:int):
    fl_code = 0
    queasy = None

    source = queri = None

    source_list, Source = create_model_like(Queasy)

    Queri = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, queasy
        nonlocal queri


        nonlocal source, queri
        nonlocal source_list
        return {"fl_code": fl_code}

    def fill_new_queasy():

        nonlocal fl_code, queasy
        nonlocal queri


        nonlocal source, queri
        nonlocal source_list


        queasy.key = 130
        queasy.number1 = source.number1
        queasy.char1 = source.char1

    source = query(source_list, first=True)

    if case_type == 1:

        queri = db_session.query(Queri).filter(
                (Queri.number1 == SOURCE.number1) &  (Queri.key == 130)).first()

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = db_session.query(Queri).filter(
                    (Queri.char1 == SOURCE.char1) &  (Queri.key == 130)).first()

            if queri:
                fl_code = 2

                return generate_output()
            else:
                queasy = Queasy()
                db_session.add(queasy)

                fill_new_queasy()
                fl_code = 3

    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == rec_id)).first()

        queri = db_session.query(Queri).filter(
                (Queri.number1 == source.number1) &  (Queri.number2 == 0) &  (Queri.deci2 == 0) &  (Queri.key == 130) &  (Queri._recid != queasy._recid)).first()

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = db_session.query(Queri).filter(
                    (Queri.char1 == source.char1) &  (Queri.number2 == 0) &  (Queri.deci2 == 0) &  (Queri.key == 130) &  (Queri._recid != queasy._recid)).first()

            if queri:
                fl_code = 2

                return generate_output()
            else:

                queasy = db_session.query(Queasy).first()
                queasy.number1 = source.number1
                queasy.char1 = source.char1

                queasy = db_session.query(Queasy).first()
                fl_code = 3

    return generate_output()