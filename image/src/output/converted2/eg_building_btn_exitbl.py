#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

build_list, Build = create_model("Build")

def eg_building_btn_exitbl(build_list:[Build], case_type:int, rec_id:int):

    prepare_cache ([Queasy])

    fl_code = 0
    queasy = None

    queri = build = None

    Queri = create_buffer("Queri",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, queasy
        nonlocal case_type, rec_id
        nonlocal queri


        nonlocal queri, build

        return {"fl_code": fl_code}

    def fill_new_queasy():

        nonlocal fl_code, queasy
        nonlocal case_type, rec_id
        nonlocal queri


        nonlocal queri, build


        queasy.key = 135
        queasy.number1 = build.number1
        queasy.char1 = build.char1


    build = query(build_list, first=True)

    if case_type == 1:

        queri = get_cache (Queasy, {"number1": [(eq, build.number1)],"key": [(eq, 135)]})

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = get_cache (Queasy, {"char1": [(eq, build.char1)],"key": [(eq, 135)]})

            if queri:
                fl_code = 2

                return generate_output()
            else:
                queasy = Queasy()
                db_session.add(queasy)

                fill_new_queasy()
                fl_code = 3

    elif case_type == 2:

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

        queri = get_cache (Queasy, {"char1": [(eq, build.char1)],"key": [(eq, 135)],"_recid": [(ne, queasy._recid)]})

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = get_cache (Queasy, {"number1": [(eq, build.number1)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"key": [(eq, 135)],"_recid": [(ne, queasy._recid)]})

            if queri:
                fl_code = 2

                return generate_output()
            else:

                queri = get_cache (Queasy, {"number1": [(eq, build.number1)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"key": [(eq, 135)],"_recid": [(ne, queasy._recid)]})

                if queri:
                    fl_code = 3

                    return generate_output()
                else:

                    queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
                    pass
                    queasy.number1 = build.number1
                    queasy.char1 = build.char1
                    pass
                    fl_code = 4

    return generate_output()