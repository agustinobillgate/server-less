from functions.additional_functions import *
import decimal
from models import Queasy

def eg_building_btn_exitbl(build:[Build], case_type:int, rec_id:int):
    fl_code = 0
    queasy = None

    queri = build = None

    build_list, Build = create_model("Build")

    Queri = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, queasy
        nonlocal queri


        nonlocal queri, build
        nonlocal build_list
        return {"fl_code": fl_code}

    def fill_new_queasy():

        nonlocal fl_code, queasy
        nonlocal queri


        nonlocal queri, build
        nonlocal build_list


        queasy.key = 135
        queasy.number1 = build.number1
        queasy.char1 = build.char1

    build = query(build_list, first=True)

    if case_type == 1:

        queri = db_session.query(Queri).filter(
                (Queri.number1 == build.number1) &  (Queri.key == 135)).first()

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = db_session.query(Queri).filter(
                    (Queri.char1 == build.char1) &  (Queri.key == 135)).first()

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
                (Queri.char1 == build.char1) &  (Queri.key == 135) &  (Queri._recid != queasy._recid)).first()

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = db_session.query(Queri).filter(
                    (Queri.number1 == build.number1 and Queri.number2 == 0 and Queri.deci2 == 0 and Queri.key == 135) &  (Queri._recid != queasy._recid)).first()

            if queri:
                fl_code = 2

                return generate_output()
            else:

                queri = db_session.query(Queri).filter(
                        (Queri.number1 == build.number1 and Queri.number2 == 0 and Queri.deci2 == 0 and Queri.key == 135) &  (Queri._recid != queasy._recid)).first()

                if queri:
                    fl_code = 3

                    return generate_output()
                else:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy._recid == rec_id)).first()

                    queasy = db_session.query(Queasy).first()
                    queasy.number1 = build.number1
                    queasy.char1 = build.char1

                    queasy = db_session.query(Queasy).first()
                    fl_code = 4

    return generate_output()